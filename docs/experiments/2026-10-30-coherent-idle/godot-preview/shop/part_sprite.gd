@tool
extends Sprite2D

@export_file("*.png") var image_path: String = "":
	set(value):
		image_path = value
		if is_inside_tree(): _load_pixels()

func _ready() -> void:
	_load_pixels()

func _load_pixels() -> void:
	if image_path.is_empty(): return
	var pixels := Image.new()
	var error := pixels.load_png_from_buffer(FileAccess.get_file_as_bytes(image_path))
	if error != OK or pixels.is_empty():
		push_error("SHOP_PART_LOAD_FAILED " + image_path)
		return
	texture = ImageTexture.create_from_image(pixels)
	centered = false
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
