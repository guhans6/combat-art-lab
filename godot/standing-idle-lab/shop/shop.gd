@tool
extends Node2D

@export var emitters_enabled := true:
	set(value):
		emitters_enabled = value
		if is_inside_tree(): _apply_visibility()
@export var props_enabled := true:
	set(value):
		props_enabled = value
		if is_inside_tree(): _apply_visibility()

func _ready() -> void:
	_apply_visibility()

func _apply_visibility() -> void:
	for part in get_children():
		if str(part.name).ends_with("emitter"): part.visible = emitters_enabled
		if str(part.name) in ["P07_chalkboard", "P08_large_planter", "P09_small_planter"]: part.visible = props_enabled
