extends Node2D
var actor: AnimatedSprite2D
var small: AnimatedSprite2D
var loops := 0
var events: Array = []
var captured: Dictionary = {}
var layout: Dictionary
func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	layout = JSON.parse_string(FileAccess.get_file_as_string("res://layout.json"))
	var frames := SpriteFrames.new()
	frames.remove_animation("default")
	frames.add_animation("idle")
	frames.set_animation_speed("idle", 1.0)
	frames.set_animation_loop("idle", true)
	for i in range(layout["files"].size()):
		var image := Image.load_from_file("res://textures/" + str(layout["files"][i]))
		assert(image != null and not image.is_empty())
		frames.add_frame("idle", ImageTexture.create_from_image(image), float(layout["durations_ms"][i]) / 1000.0)
	actor = AnimatedSprite2D.new()
	actor.centered = false
	actor.sprite_frames = frames
	actor.position = Vector2(130, 300-float(layout["feet_y"]))
	add_child(actor)
	small = AnimatedSprite2D.new()
	small.centered = false
	small.sprite_frames = frames
	var factor := 128.0 / float(layout["body_height"])
	small.scale = Vector2(factor,factor)
	small.position = Vector2(440,300-float(layout["feet_y"])*factor)
	add_child(small)
	for item in [["Provisional native study",Vector2(100,15)],["128px body at rest",Vector2(420,15)],["SAMPLE ONLY | reference-led grounded idle | fighter unchanged",Vector2(100,330)]]:
		var label := Label.new()
		label.text = item[0]
		label.position = item[1]
		label.add_theme_font_size_override("font_size",13)
		add_child(label)
	actor.frame_changed.connect(_frame_changed)
	actor.animation_looped.connect(_looped)
	actor.play("idle")
	small.play("idle")
	print("GROUNDED_IDLE_READY engine=%s frames=%d period_ms=%s" % [Engine.get_version_info()["string"],frames.get_frame_count("idle"),layout["durations_ms"]])
	_frame_changed()
func _frame_changed() -> void:
	events.append({"ms":Time.get_ticks_msec(),"frame":actor.frame,"root":[actor.position.x,actor.position.y]})
	if not captured.has(actor.frame):
		var current := actor.frame
		captured[current] = true
		await RenderingServer.frame_post_draw
		get_viewport().get_texture().get_image().save_png("res://evidence/runtime-frame-%02d.png" % current)
func _looped() -> void:
	loops += 1
	print("GROUNDED_IDLE_LOOP %d" % loops)
	if loops == 3:
		var record := {"engine":Engine.get_version_info()["string"],"loops":loops,"captured":captured.keys(),"events":events,"layout":layout,"viewport":[640,360],"filter":"nearest","display_server":DisplayServer.get_name()}
		var file := FileAccess.open("res://evidence/runtime.json",FileAccess.WRITE)
		file.store_string(JSON.stringify(record,"\t"))
		print("GROUNDED_IDLE_THREE_LOOPS_OK")
func _draw() -> void:
	# Temporary neutral environment: fixed architecture gives the body movement a ground reference.
	draw_rect(Rect2(0, 56, 640, 244), Color(0.12,0.14,0.17))
	for offset in [0,320]:
		draw_rect(Rect2(offset+82,112,160,188),Color(0.085,0.10,0.12))
		draw_rect(Rect2(offset+91,121,142,179),Color(0.15,0.17,0.20),false,4)
		draw_rect(Rect2(offset+106,130,112,170),Color(0.105,0.12,0.14))
		draw_rect(Rect2(offset+232,90,5,210),Color(0.16,0.18,0.20))
		draw_line(Vector2(offset+20,216),Vector2(offset+310,216),Color(0.15,0.17,0.19),1)
		draw_contact_shadow(offset)
	draw_rect(Rect2(0,300,640,24),Color(0.17,0.18,0.19))
	draw_line(Vector2(0,300),Vector2(640,300),Color(0.28,0.30,0.33),1)
	for x in range(0,640,80):
		draw_line(Vector2(x,300),Vector2(x+8,324),Color(0.20,0.21,0.22),1)
func draw_contact_shadow(offset: int) -> void:
	# Flat, fixed contact shadow; neither shadow nor floor rides with the sprite.
	draw_rect(Rect2(157 if offset == 0 else 468,297,50 if offset == 0 else 42,3),Color(0.065,0.075,0.085))
