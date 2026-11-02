extends Control

const GROUND := 400.0
const DURATIONS := [700, 260, 500, 340]
var frames: Array[Texture2D] = []
var backdrop: Texture2D
var tiles: Texture2D
var heights := [128.0, 152.0, 160.0]
var selected := 1
var compare := false
var guides := false
var frame_index := 0
var font: Font

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	clip_contents = true
	font = ThemeDB.fallback_font
	for i in range(4):
		frames.append(_texture("res://textures/idle-%d.png" % i))
	backdrop = _texture("res://textures/backgrounds.png")
	tiles = _texture("res://textures/tileset.png")

func _texture(path: String) -> Texture2D:
	var image := Image.load_from_file(path)
	assert(image != null and not image.is_empty(), path)
	return ImageTexture.create_from_image(image)

func actor_rect(index: int) -> Rect2:
	var factor: float = heights[index] / 240.0
	var center: float = 200.0 + index * 400.0 if compare else 600.0
	return Rect2(center - 64.0 * factor, GROUND - 253.0 * factor, 128.0 * factor, 264.0 * factor)

func _draw() -> void:
	if frames.is_empty():
		return
	# Borrowed window bay repeated identically: world and camera stay fixed in every mode.
	draw_rect(Rect2(0, 0, 1200, 480), Color("27263b"))
	for bay in range(3):
		draw_texture_rect_region(backdrop, Rect2(bay * 400 + 40, 16, 320, 384), Rect2(0, 0, 160, 192))
	# Unchanged 32x16 source stone blocks, displayed at an integer 2x.
	draw_rect(Rect2(0, GROUND, 1200, 80), Color("201e2e"))
	for x in range(0, 1200, 64):
		draw_texture_rect_region(tiles, Rect2(x, GROUND, 64, 32), Rect2(64, 168, 32, 16))
		draw_texture_rect_region(tiles, Rect2(x, GROUND + 32, 64, 32), Rect2(64, 184, 32, 16))
	# Quiet fixed contact shadows follow scale, never the breathing phase.
	for i in range(3):
		if not compare and i != selected:
			continue
		var center: float = 200.0 + i * 400.0 if compare else 600.0
		var h: float = heights[i]
		draw_set_transform(Vector2(center, GROUND + 1), 0, Vector2(h * 0.16, 2))
		draw_circle(Vector2.ZERO, 1.0, Color(0.025, 0.025, 0.035, 0.65))
		draw_set_transform(Vector2.ZERO)
		draw_texture_rect(frames[frame_index], actor_rect(i), false)
		var label := "%s  /  %d px" % [char(65 + i), int(h)]
		var width := font.get_string_size(label, HORIZONTAL_ALIGNMENT_LEFT, -1, 16).x
		draw_string(font, Vector2(center - width * 0.5, GROUND - h - 20), label, HORIZONTAL_ALIGNMENT_LEFT, -1, 16, Color("ddccaa") if i == selected else Color("aaa6b8"))
		if guides:
			var gx := center + 72.0
			draw_line(Vector2(gx, GROUND), Vector2(gx, GROUND-h), Color("b8a575"), 1)
			for y in [GROUND, GROUND-h]:
				draw_line(Vector2(gx-5, y), Vector2(gx+5, y), Color("b8a575"), 1)
	if guides:
		for y in range(16, 401, 16):
			draw_line(Vector2(0,y), Vector2(1200,y), Color(0.7,0.7,0.8,0.09), 1)
		draw_line(Vector2(0, GROUND), Vector2(1200, GROUND), Color("c7b681"), 1)
