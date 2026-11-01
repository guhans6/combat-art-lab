extends Node2D

var character: AnimatedSprite2D
var environment_nodes: Dictionary = {}
var shop_layers: Array = []
var status_label: Label
var shop_only := false
var capture_pending := false
var captured: Dictionary = {}
var frame_events: Array = []
var loop_count := 0
var modular_shop: Node2D

func _ready() -> void:
	if not _is_allowed_alpha_hole(1, 1, JSON.parse_string("[[1,1]]")):
		push_error("ART_LAB_ALPHA_COORDINATE_TEST_FAIL")
		return
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var layout: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://textures/environment-layout.json"))
	shop_layers = layout["shop_layers"]
	for layer_name in layout["layers"]:
		if layout["shop_layers"].has(layer_name):
			if layer_name == "05-near-shop-wall":
				var context := Sprite2D.new()
				context.centered = false
				context.texture = ImageTexture.create_from_image(_read_preview_png("res://shop/textures/context-residual.png"))
				add_child(context)
				environment_nodes["shop_context"] = context
			continue
		var part := Sprite2D.new()
		part.name = str(layer_name).replace("-", "_")
		part.centered = false
		part.texture = load("res://textures/environment/environment-%s.png" % layer_name)
		part.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		add_child(part)
		environment_nodes[layer_name] = part
	modular_shop = load("res://shop/shop.tscn").instantiate()
	add_child(modular_shop)
	character = AnimatedSprite2D.new()
	character.name = "StandingCharacter"
	character.centered = false
	character.position = Vector2(108, 48)
	character.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	character.sprite_frames = SpriteFrames.new()
	character.sprite_frames.remove_animation("default")
	character.sprite_frames.add_animation("idle")
	character.sprite_frames.set_animation_speed("idle", 1.0)
	character.sprite_frames.set_animation_loop("idle", true)
	if FileAccess.file_exists("res://textures/idle-layout.json"):
		var idle: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://textures/idle-layout.json"))
		var frame_directory: String = idle.get("frame_directory", "res://textures/idle")
		var coverage_region: Array = idle.get("alpha_review_region", [0, 55, 96, 205])
		var hole_exceptions: Array = idle.get("intentional_alpha_holes", [])
		for i in range(idle["durations_ms"].size()):
			var image := _read_preview_png("%s/frame-%02d.png" % [frame_directory, i])
			if image == null or image.is_empty() or _has_alpha_gaps(image, coverage_region, hole_exceptions[i] if i < hole_exceptions.size() else []):
				push_error("ART_LAB_ALPHA_FAIL frame=%d source=%s" % [i, frame_directory])
				return
			character.sprite_frames.add_frame("idle", ImageTexture.create_from_image(image), float(idle["durations_ms"][i]) / 1000.0)
		print("ART_LAB_ALPHA_OK frames=%d" % idle["durations_ms"].size())
	else:
		character.sprite_frames.add_frame("idle", load("res://textures/standing.png"), 1.0)
	add_child(character)
	character.frame_changed.connect(_frame_changed)
	character.animation_looped.connect(_animation_looped)
	character.play("idle")
	var hud := ColorRect.new()
	hud.position = Vector2(0,272)
	hud.size = Vector2(362,32)
	hud.color = Color(0.08,0.08,0.11)
	add_child(hud)
	status_label = Label.new()
	status_label.position = Vector2(5,274)
	status_label.add_theme_font_size_override("font_size",9)
	add_child(status_label)
	_update_status()
	print("ART_LAB_READY engine=%s viewport=%s frames=%d filter=nearest root=(108,48)" % [Engine.get_version_info()["string"],get_viewport_rect().size,character.sprite_frames.get_frame_count("idle")])
	await _capture("startup")
	_verify_modular_shop()
	if "--observe-run" in OS.get_cmdline_user_args():
		_observe_run()


func _update_status() -> void:
	if not is_instance_valid(status_label): return
	var mode := "Shop only" if shop_only else "Street scene"
	var playing := "Playing" if character.is_playing() else "Paused"
	status_label.text = "%s | %s %d/%d\nSpace pause  F step  B shop  1/2/3 size  Esc exit" % [mode,playing,character.frame+1,character.sprite_frames.get_frame_count("idle")]

func _frame_changed() -> void:
	if not is_instance_valid(status_label): return
	_update_status()
	frame_events.append({"time_ms":Time.get_ticks_msec(),"frame":character.frame,"root":[character.position.x,character.position.y]})
	if frame_events.size()>80: frame_events.pop_front()
	var output := FileAccess.open("res://evidence/frame-events.json",FileAccess.WRITE)
	output.store_string(JSON.stringify({"engine":Engine.get_version_info()["string"],"loop_count":loop_count,"events":frame_events},"\t"))
	if not captured.has(character.frame) and not capture_pending:
		captured[character.frame] = true
		_capture("frame-%02d" % character.frame)

func _animation_looped() -> void:
	loop_count += 1
	print("ART_LAB_LOOP %d" % loop_count)

func _capture(label: String) -> void:
	if DisplayServer.get_name() == "headless": return
	capture_pending = true
	await RenderingServer.frame_post_draw
	var image: Image = get_viewport().get_texture().get_image()
	var result := image.save_png("res://evidence/runtime-%s.png" % label)
	print("ART_LAB_CAPTURE %s error=%d size=%s" % [label,result,image.get_size()])
	capture_pending = false

func _unhandled_key_input(event: InputEvent) -> void:
	if not is_instance_valid(status_label): return
	if not event is InputEventKey or not event.pressed or event.echo: return
	match event.keycode:
		KEY_SPACE:
			if character.is_playing(): character.pause()
			else: character.play("idle")
		KEY_F:
			character.pause()
			character.frame = (character.frame+1) % character.sprite_frames.get_frame_count("idle")
		KEY_B:
			shop_only = not shop_only
			for layer_name in environment_nodes:
				environment_nodes[layer_name].visible = not shop_only or shop_layers.has(layer_name)
			character.visible = not shop_only
			_capture("shop-only" if shop_only else "scene")
		KEY_1, KEY_2, KEY_3:
			var factor: int = event.keycode - KEY_0
			get_window().size = Vector2i(362,304)*factor
		KEY_ESCAPE:
			get_tree().quit()
	_update_status()

func _observe_run() -> void:
	await get_tree().create_timer(6.2).timeout
	character.pause()
	character.frame = 3
	_update_status()
	await _capture("idle-closed-inspection")
	shop_only = true
	for layer_name in environment_nodes:
		environment_nodes[layer_name].visible = shop_layers.has(layer_name)
	character.visible = false
	_update_status()
	await _capture("shop-only")
	var output := FileAccess.open("res://evidence/observation.json", FileAccess.WRITE)
	output.store_string(JSON.stringify({"engine":Engine.get_version_info()["string"],"viewport":[get_viewport_rect().size.x,get_viewport_rect().size.y],"animation_frames":character.sprite_frames.get_frame_count("idle"),"loops_observed":loop_count,"nearest_filter":character.texture_filter==CanvasItem.TEXTURE_FILTER_NEAREST,"character_root":[character.position.x,character.position.y],"shop_parts":shop_layers,"engine_observation":"played loop; captured each frame, paused closed pose and isolated shop; OS keyboard interaction not exercised"},"\t"))
	shop_only = false
	for layer_name in environment_nodes: environment_nodes[layer_name].visible = true
	character.visible = true
	character.play("idle")
	_update_status()
	await _capture("final-scene")
	if "--quit-after-observation" in OS.get_cmdline_user_args(): get_tree().quit()


func _verify_modular_shop() -> void:
	await get_tree().create_timer(1.5).timeout
	character.pause()
	character.frame = 0
	await _capture("shop-refined-scene")
	modular_shop.props_enabled = false
	await _capture("shop-architecture-only")
	modular_shop.props_enabled = true
	var planter: Node2D = modular_shop.get_node("P09_small_planter")
	var baseline: Vector2 = planter.position
	planter.position.x += 8
	await _capture("shop-planter-moved")
	planter.position = baseline
	modular_shop.emitters_enabled = false
	await _capture("shop-emitters-off")
	modular_shop.emitters_enabled = true
	var second: Node2D = load("res://shop/shop.tscn").instantiate()
	second.position = Vector2(420, 0)
	add_child(second)
	planter.position.x += 8
	var independent: bool = second.get_node("P09_small_planter").position == baseline
	planter.position = baseline
	var ready_parts := 0
	for part in modular_shop.get_children():
		if part is Sprite2D and part.texture != null: ready_parts += 1
	var result := {"engine":Engine.get_version_info()["string"], "parts_with_textures":ready_parts, "second_instance_parts":second.get_child_count(), "instances_independent":independent, "props_visibility_exercised":true, "emitter_visibility_exercised":true, "planter_moved_native_pixels":8, "dynamic_lighting":false, "os_input_exercised":false}
	second.queue_free()
	var file := FileAccess.open("res://evidence/shop-modular-checks.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(result, "\t"))
	print("SHOP_MODULAR_CHECKS " + JSON.stringify(result))
	character.play("idle")
	await _capture("shop-final-scene")


func _has_alpha_gaps(image: Image, region: Array, allowed_holes: Array = []) -> bool:
	# Native-canvas connectivity first; ROI only selects solid body regions for review.
	var width: int = image.get_width()
	var height: int = image.get_height()
	var seen := PackedByteArray()
	seen.resize(width * height)
	var transparent := PackedByteArray()
	transparent.resize(width * height)
	for i in range(width * height):
		transparent[i] = 1 if image.get_pixel(i % width, floori(float(i) / float(width))).a == 0 else 0
	for start in range(width * height):
		if seen[start] == 1 or transparent[start] == 0: continue
		var queue: Array[int] = [start]
		var cursor := 0
		var exterior := false
		var in_body := false
		seen[start] = 1
		while cursor < queue.size():
			var i: int = queue[cursor]
			cursor += 1
			var x: int = i % width
			var y: int = floori(float(i) / float(width))
			exterior = exterior or x == 0 or x == width - 1 or y == 0 or y == height - 1
			in_body = in_body or (x >= region[0] and x < region[2] and y >= region[1] and y < region[3] and not _is_allowed_alpha_hole(x, y, allowed_holes))
			for delta in [Vector2i(-1, 0), Vector2i(1, 0), Vector2i(0, -1), Vector2i(0, 1)]:
				var nx: int = x + delta.x
				var ny: int = y + delta.y
				var next: int = ny * width + nx
				if nx >= 0 and nx < width and ny >= 0 and ny < height and seen[next] == 0 and transparent[next] == 1:
					seen[next] = 1
					queue.append(next)
		if in_body and not exterior: return true
	return false


func _read_preview_png(path: String) -> Image:
	var pixels := Image.new()
	var error := pixels.load_png_from_buffer(FileAccess.get_file_as_bytes(path))
	if error != OK:
		push_error("ART_LAB_PNG_LOAD_FAIL " + path)
	return pixels


func _is_allowed_alpha_hole(x: int, y: int, allowed: Array) -> bool:
	# JSON numeric coordinates arrive as floats; compare their integer positions.
	for point in allowed:
		if int(point[0]) == x and int(point[1]) == y: return true
	return false
