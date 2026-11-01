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

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var layout: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://textures/environment-layout.json"))
	shop_layers = layout["shop_layers"]
	for layer_name in layout["layers"]:
		var part := Sprite2D.new()
		part.name = str(layer_name).replace("-", "_")
		part.centered = false
		part.texture = load("res://textures/environment/environment-%s.png" % layer_name)
		part.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		add_child(part)
		environment_nodes[layer_name] = part
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
		for i in range(idle["durations_ms"].size()):
			character.sprite_frames.add_frame("idle", load("res://textures/idle/frame-%02d.png" % i), float(idle["durations_ms"][i]) / 1000.0)
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
	if "--observe-run" in OS.get_cmdline_user_args():
		_observe_run()


func _update_status() -> void:
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
