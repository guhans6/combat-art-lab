extends Node2D

var actor: AnimatedSprite2D
var status: Label
var target: ColorRect
var meta: Dictionary
var frame_events: Array = []
var hit_events: Array = []
var completed: Array = []
var captured: Dictionary = {}
var capture_pending := false
var attack_running := false
var hit_registered := false
var attack_number := 0
var started_ms := 0
var root := Vector2(30, 69)
var hurtbox := Rect2()
var auto_observation := true
var synthetic_space_events_sent := 0
var space_events_received := 0
var live_rendered_frames: Dictionary = {}
var inspection_only_frames: Array = []

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	meta = JSON.parse_string(FileAccess.get_file_as_string("res://attack/metadata.json"))
	var layout: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://textures/environment-layout.json"))
	for layer_name in layout["layers"]:
		if layout["shop_layers"].has(layer_name):
			if layer_name == "05-near-shop-wall":
				var context := Sprite2D.new()
				context.centered = false
				context.texture = _texture("res://shop/textures/context-residual.png")
				add_child(context)
			continue
		var part := Sprite2D.new()
		part.centered = false
		part.texture = _texture("res://textures/environment/environment-%s.png" % layer_name)
		add_child(part)
	add_child(load("res://shop/shop.tscn").instantiate())
	actor = AnimatedSprite2D.new()
	actor.centered = false
	actor.position = root
	actor.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	actor.sprite_frames = SpriteFrames.new()
	actor.sprite_frames.remove_animation("default")
	actor.sprite_frames.add_animation("idle")
	actor.sprite_frames.add_frame("idle", _texture("res://attack/idle.png"), 1.0)
	actor.sprite_frames.add_animation("attack")
	actor.sprite_frames.set_animation_speed("attack", 1.0)
	actor.sprite_frames.set_animation_loop("attack", false)
	for i in range(meta["durations_ms"].size()):
		actor.sprite_frames.add_frame("attack", _texture("res://attack/frame-%02d.png" % i), float(meta["durations_ms"][i]) / 1000.0)
	add_child(actor)
	var active: int = int(meta["active_frames_1based"][0]) - 1
	var bounds: Array = meta["bag_bounds_xyxy"][active]
	var offsets: Array = meta["root_offsets"][active]
	var center := Vector2((float(bounds[0]) + float(bounds[2])) * 0.5, (float(bounds[1]) + float(bounds[3])) * 0.5) + root + Vector2(offsets[0], offsets[1])
	hurtbox = Rect2(center - Vector2(7, 22), Vector2(14, 44))
	target = ColorRect.new()
	target.position = hurtbox.position
	target.size = hurtbox.size
	target.color = Color(0.35, 0.5, 0.6, 0.85)
	add_child(target)
	var post := ColorRect.new()
	post.position = Vector2(center.x - 2, hurtbox.end.y)
	post.size = Vector2(4, maxf(1, 254 - hurtbox.end.y))
	post.color = Color(0.25, 0.22, 0.2)
	add_child(post)
	move_child(actor, get_child_count() - 1)
	var hud := ColorRect.new()
	hud.position = Vector2(0, 272)
	hud.size = Vector2(362, 32)
	hud.color = Color(0.08, 0.08, 0.11)
	add_child(hud)
	status = Label.new()
	status.position = Vector2(5, 274)
	status.add_theme_font_size_override("font_size", 9)
	add_child(status)
	actor.frame_changed.connect(_frame_changed)
	actor.animation_finished.connect(_attack_finished)
	actor.play("idle")
	_update_status()
	print("TOTE_READY engine=%s frames=%d filter=nearest viewport=%s" % [Engine.get_version_info()["string"], meta["durations_ms"].size(), get_viewport_rect().size])
	await _capture("startup")
	if auto_observation:
		await get_tree().create_timer(0.5).timeout
		_inject_space()

func _inject_space() -> void:
	synthetic_space_events_sent += 1
	var press := InputEventKey.new()
	press.keycode = KEY_SPACE
	press.pressed = true
	Input.parse_input_event(press)
	await get_tree().process_frame
	var release := InputEventKey.new()
	release.keycode = KEY_SPACE
	release.pressed = false
	Input.parse_input_event(release)

func _texture(path: String) -> ImageTexture:
	var pixels := Image.new()
	var result := pixels.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
	assert(result == OK, "TOTE_PNG_LOAD_FAIL " + path)
	return ImageTexture.create_from_image(pixels)

func _start_attack() -> void:
	if attack_running: return
	attack_number += 1
	attack_running = true
	hit_registered = false
	started_ms = Time.get_ticks_msec()
	actor.stop()
	actor.play("attack")
	actor.frame = 0
	_frame_changed()
	print("TOTE_ATTACK_START %d" % attack_number)

func _frame_changed() -> void:
	if not attack_running or actor.animation != "attack": return
	var index := actor.frame
	var offset: Array = meta["root_offsets"][index]
	actor.position = root + Vector2(offset[0], offset[1])
	frame_events.append({"attack":attack_number,"frame":index + 1,"elapsed_ms":Time.get_ticks_msec() - started_ms,"position":[actor.position.x, actor.position.y],"phase":meta["phases"][index]})
	if _is_active_frame(index + 1) and not hit_registered:
		var box: Array = meta["bag_bounds_xyxy"][index]
		var bag_rect := Rect2(actor.position + Vector2(box[0], box[1]), Vector2(float(box[2]) - float(box[0]), float(box[3]) - float(box[1])))
		if bag_rect.intersects(hurtbox):
			hit_registered = true
			hit_events.append({"attack":attack_number,"frame":index + 1,"elapsed_ms":Time.get_ticks_msec() - started_ms,"bag_rect":[bag_rect.position.x,bag_rect.position.y,bag_rect.size.x,bag_rect.size.y]})
			target.color = Color(0.95, 0.65, 0.3, 0.9)
			print("TOTE_HIT attack=%d frame=%d" % [attack_number,index + 1])
	_update_status()
	if not captured.has(index) and not capture_pending:
		captured[index] = true
		_capture("frame-%02d" % index)

func _is_active_frame(number: int) -> bool:
	for active in meta["active_frames_1based"]:
		if int(active) == number: return true
	return false

func _attack_finished() -> void:
	if actor.animation != "attack": return
	var duration := Time.get_ticks_msec() - started_ms
	attack_running = false
	actor.position = root
	actor.play("idle")
	completed.append({"attack":attack_number,"duration_ms":duration,"hit":hit_registered,"returned_to_idle":actor.animation == "idle" and actor.frame == 0,"state_after":str(actor.animation),"frame_after":actor.frame})
	target.color = Color(0.35, 0.5, 0.6, 0.85)
	_update_status()
	_write_evidence()
	print("TOTE_ATTACK_END %d duration=%d hits=%d" % [attack_number,duration,hit_events.size()])
	_capture("return-%02d" % attack_number)
	if auto_observation and attack_number < 3:
		await get_tree().create_timer(0.6).timeout
		_inject_space()
	elif auto_observation:
		print("TOTE_THREE_ATTACKS_COMPLETE")
		_inspect_missing_frames()

func _inspect_missing_frames() -> void:
	await get_tree().create_timer(0.1).timeout
	while capture_pending:
		await get_tree().process_frame
	for index in range(meta["durations_ms"].size()):
		if live_rendered_frames.has(index): continue
		actor.stop()
		actor.animation = "attack"
		actor.frame = index
		var offset: Array = meta["root_offsets"][index]
		actor.position = root + Vector2(offset[0], offset[1])
		await _capture("inspection-frame-%02d" % index)
		inspection_only_frames.append(index + 1)
	actor.position = root
	actor.play("idle")
	_update_status()
	_write_evidence()
	print("TOTE_FRAME_EVIDENCE live=%d inspection_only=%d" % [live_rendered_frames.size(),inspection_only_frames.size()])

func _write_evidence() -> void:
	var output := FileAccess.open("res://evidence/attack-observation.json", FileAccess.WRITE)
	output.store_string(JSON.stringify({"engine":Engine.get_version_info()["string"],"display_server":DisplayServer.get_name(),"viewport":[362,304],"native_frame_size":meta["canvas"],"filter":"nearest","window_scale":2,"base_root":[root.x,root.y],"source_sha256":meta["native_sha256"],"active_frames_1based":meta["active_frames_1based"],"authored_durations_ms":meta["durations_ms"],"completed":completed,"frame_events":frame_events,"hit_events":hit_events,"hurtbox":[hurtbox.position.x,hurtbox.position.y,hurtbox.size.x,hurtbox.size.y],"physical_keyboard_tested":false,"synthetic_space_events_sent":synthetic_space_events_sent,"space_events_received":space_events_received,"live_rendered_frames_0based":live_rendered_frames.keys(),"inspection_only_frames_1based":inspection_only_frames,"hit_method":"declared bag bounds intersect dummy hurtbox during authored active frames; at most one hit per attack"},"\t"))

func _capture(label: String) -> void:
	if DisplayServer.get_name() == "headless": return
	capture_pending = true
	RenderingServer.call_deferred("force_draw")
	await RenderingServer.frame_post_draw
	if label.begins_with("frame-"):
		if actor.animation != "attack" or not attack_running:
			capture_pending = false
			return
		label = "frame-%02d" % actor.frame
		live_rendered_frames[actor.frame] = true
	var pixels: Image = get_viewport().get_texture().get_image()
	var result := pixels.save_png("res://evidence/runtime-%s.png" % label)
	print("TOTE_CAPTURE %s error=%d" % [label,result])
	capture_pending = false

func _update_status() -> void:
	status.text = "Tote swing | %s | hits %d\nSpace attack  Esc exit | user approval pending" % [meta["phases"][actor.frame] if attack_running else "idle",hit_events.size()]

func _unhandled_key_input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo: return
	if event.keycode == KEY_SPACE:
		space_events_received += 1
		_start_attack()
	if event.keycode == KEY_ESCAPE: get_tree().quit()
