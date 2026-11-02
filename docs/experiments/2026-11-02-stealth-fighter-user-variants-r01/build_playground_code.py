from pathlib import Path
w=Path('/private/tmp/fighter-user-variants-r01');p=w/'project';q=p/'stage.gd';s=q.read_text().replace('const DURATIONS := [700, 260, 500, 340]\n','').replace('var frames: Array[Texture2D] = []','var textures: Array[Texture2D] = []\nvar variants: Array = []\nvar choices := [0,1,2]\nvar display_height := 152.0').replace('var heights := [128.0, 152.0, 160.0]\n','').replace('var compare := false','var compare := true').replace('var frame_index := 0\n','')
s=s.replace('for i in range(4):\n\t\tframes.append(_texture("res://textures/idle-%d.png" % i))','variants = JSON.parse_string(FileAccess.get_file_as_string("res://variants.json"))\n\tfor info in variants:\n\t\ttextures.append(_texture("res://textures/"+str(info["file"])))')
s=s.replace('var factor: float = heights[index] / 240.0','var info: Dictionary = variants[choices[index]]\n\tvar factor: float = display_height / float(info["body_height"])').replace('return Rect2(center - 64.0 * factor, GROUND - 253.0 * factor, 128.0 * factor, 264.0 * factor)','return Rect2(center - float(info["native_canvas"][0])*0.5*factor, GROUND-float(info["feet_y"])*factor, float(info["native_canvas"][0])*factor, float(info["native_canvas"][1])*factor)')
s=s.replace('if frames.is_empty():','if textures.is_empty():').replace('var h: float = heights[i]','var h: float = display_height').replace('draw_texture_rect(frames[frame_index], actor_rect(i), false)','draw_texture_rect(textures[choices[i]], actor_rect(i), false)').replace('var label := "%s  /  %d px" % [char(65 + i), int(h)]','var label := "%s  /  %d px" % [str(variants[choices[i]]["label"]), int(h)]')
q.write_text(s)
old=(Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/godot/stealth-fighter-playground-r02/playground.gd')).read_text()
helpers=old[old.index('func _build_theme()'):old.index('func _process(')]
input_helpers=old[old.index('func _click('):old.index('func _setup_lighting(')]
lighting=old[old.index('func _setup_lighting('):old.index('func _run_checks(')]
s='''extends Control

const StageScript = preload("res://stage.gd")
const PRESETS := [[0,1,2],[0,3,4],[0,2,4]]
var stage
var compare := true
var selected := 1
var guides := false
var preset_index := 0
var choices := [0,1,2]
var compare_button: Button
var solo_button: Button
var slots: Array[Button] = []
var set_button: Button
var previous_button: Button
var next_button: Button
var reset_button: Button
var guide_button: Button
var height_slider: HSlider
var height_label: Label
var appearance: OptionButton
var capture_checks: Array = []
var world_canvas: CanvasLayer
var ambient: CanvasModulate
var fill_lights: Array[PointLight2D] = []
var lighting_mode := 0
var lighting_button: Button
var lighting_label: Label

func _ready() -> void:
	_build_theme()
	_label("THE QUIET KEEP",Vector2(40,22),30,Color("eee5d2"))
	_label("CURRENT A   /   APPEARANCE STUDY   /   STATIC POSES",Vector2(42,62),13,Color("9b9690"))
	_label("Same scene · same scale",Vector2(952,35),16,Color("b4a890"))
	lighting_button = _button("",Rect2(640,25,280,42),_cycle_lighting)
	lighting_label = _label("",Vector2(640,72),12,Color("9b9690"))
	compare_button = _button("Side by side",Rect2(40,100,168,42),func():_mode(true))
	solo_button = _button("Single",Rect2(216,100,120,42),func():_mode(false))
	for i in range(3):
		var index := i
		slots.append(_button("",Rect2(376+i*140,100,132,42),func():_select(index)))
	set_button = _button("Next set",Rect2(824,100,122,42),_next_set)
	previous_button = _button("‹ Look",Rect2(954,100,58,42),func():_cycle_variant(-1))
	next_button = _button("Look ›",Rect2(1020,100,58,42),func():_cycle_variant(1))
	reset_button = _button("Reset",Rect2(1086,100,154,42),_reset)
	stage = StageScript.new()
	stage.position = Vector2(40,158)
	stage.size = Vector2(1200,480)
	world_canvas = CanvasLayer.new()
	world_canvas.layer = -1
	add_child(world_canvas)
	world_canvas.add_child(stage)
	_setup_lighting()
	height_label = _label("",Vector2(40,666),16,Color("e0d4b9"))
	height_slider = HSlider.new()
	height_slider.position = Vector2(228,661)
	height_slider.size = Vector2(460,32)
	height_slider.min_value = 64
	height_slider.max_value = 240
	height_slider.step = 8
	height_slider.value = 152
	add_child(height_slider)
	height_slider.value_changed.connect(_height_changed)
	_label("64",Vector2(228,696),12,Color("8d8d94"))
	_label("240",Vector2(663,696),12,Color("8d8d94"))
	appearance = OptionButton.new()
	appearance.position = Vector2(746,655)
	appearance.size = Vector2(346,42)
	for i in range(stage.variants.size()):
		appearance.add_item(str(stage.variants[i]["label"]),i)
	appearance.item_selected.connect(_choose_variant)
	add_child(appearance)
	guide_button = _button("Guides",Rect2(1110,655,130,42),_toggle_guides)
	_label("Choose panel A / B / C, then change its look below.  Next set cycles through all supplied looks and the armor pair.",Vector2(40,720),14,Color("b4afa6"))
	_label("M  compare / single    1 / 2 / 3  panel    Left / Right  look    L  lighting    R  reset    F11  fullscreen",Vector2(40,747),13,Color("8d8d94"))
	_label("All poses held still at the same height. Image 2 supports Look 3. Backdrop: Luis Zuno / ansimuz · public domain",Vector2(40,777),12,Color("777b83"))
	_sync()
	print("APPEARANCE_STUDY_READY variants=5 static=true default_height=152 source_ids=[0,1,3,4,5]")
	if FileAccess.file_exists("res://RUN_CHECKS"):
		call_deferred("_run_checks")

'''+helpers+'''func _sync() -> void:
	stage.compare = compare
	stage.selected = selected
	stage.guides = guides
	stage.choices = choices.duplicate()
	height_slider.set_value_no_signal(stage.display_height)
	height_label.text = "All heights  ·  %d px"%int(stage.display_height)
	for i in range(3):
		slots[i].text = "%s · %s"%[char(65+i),str(stage.variants[choices[i]]["short"])]
		slots[i].modulate = Color.WHITE if i==selected else Color(0.7,0.7,0.7)
	compare_button.modulate = Color.WHITE if compare else Color(0.65,0.65,0.65)
	solo_button.modulate = Color.WHITE if not compare else Color(0.65,0.65,0.65)
	appearance.select(choices[selected])
	guide_button.text = "Guides: on"if guides else "Guides: off"
	_update_lighting()
	stage.queue_redraw()

func _mode(value: bool) -> void:
	compare = value
	_sync()
func _select(index: int) -> void:
	selected = index
	_sync()
func _choose_variant(index: int) -> void:
	choices[selected] = index
	_sync()
func _cycle_variant(direction: int) -> void:
	_choose_variant(posmod(choices[selected]+direction,stage.variants.size()))
func _height_changed(value: float) -> void:
	stage.display_height = value
	_sync()
func _next_set() -> void:
	preset_index = (preset_index+1)%PRESETS.size()
	choices.assign(PRESETS[preset_index])
	_sync()
func _toggle_guides() -> void:
	guides = not guides
	_sync()
func _reset() -> void:
	choices = [0,1,2]
	selected = 1
	compare = true
	guides = false
	preset_index = 0
	lighting_mode = 0
	stage.display_height = 152
	_sync()
func _input(event: InputEvent) -> void:
	if event is not InputEventKey or not event.pressed or event.echo:
		return
	match event.keycode:
		KEY_L:_cycle_lighting()
		KEY_M:_mode(not compare)
		KEY_1:_select(0)
		KEY_2:_select(1)
		KEY_3:_select(2)
		KEY_LEFT:_cycle_variant(-1)
		KEY_RIGHT:_cycle_variant(1)
		KEY_R:_reset()
		KEY_G:_toggle_guides()
		KEY_N:_next_set()
		KEY_F11:
			DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED if DisplayServer.window_get_mode()==DisplayServer.WINDOW_MODE_FULLSCREEN else DisplayServer.WINDOW_MODE_FULLSCREEN)
		_:return
	get_viewport().set_input_as_handled()

'''+input_helpers+lighting
s+='''func _run_checks() -> void:
	await get_tree().create_timer(0.3).timeout
	_check(compare and choices==[0,1,2]and stage.display_height==152,"default Original / Look1 / Look3 at152")
	await _capture("set-1")
	await _click(set_button)
	_check(choices==[0,3,4],"mouse next set shows Looks4and5")
	await _capture("set-2")
	await _key(KEY_N)
	_check(choices==[0,2,4],"keyboard next set shows armor pair3and5")
	await _capture("armor-pair")
	await _click(solo_button)
	_check(not compare,"mouse single view")
	await _click(slots[2])
	_check(selected==2,"mouse panel C")
	await _click(previous_button)
	_check(choices[2]==3,"mouse previous appearance")
	await _key(KEY_RIGHT)
	_check(choices[2]==4,"keyboard next appearance")
	# Test the actual PopupMenu->OptionButton signal route, not a physical menu click.
	appearance.get_popup().id_pressed.emit(1)
	await get_tree().process_frame
	_check(choices[2]==1 and appearance.get_selected_id()==1,"appearance popup selection signal")
	await _click(height_slider,Vector2(0.8,0.5))
	_check(stage.display_height!=152 and stage.display_height>=64 and stage.display_height<=240,"mouse changes common height")
	await _click(lighting_button)
	_check(lighting_mode==1,"mouse dim-room lighting")
	await _key(KEY_L)
	_check(lighting_mode==2,"keyboard lamp-fill lighting")
	await _click(guide_button)
	_check(guides,"mouse guides")
	await _click(reset_button)
	_check(compare and choices==[0,1,2]and stage.display_height==152 and lighting_mode==0 and not guides,"reset restores static152neutral comparison")
	_mode(false)
	for v in range(stage.variants.size()):
		_choose_variant(v)
		await _capture("single-look-%d-152"%int(stage.variants[v]["source_id"]))
		_height_changed(240)
		await _capture("native-look-%d"%int(stage.variants[v]["source_id"]))
		_height_changed(152)
		_cycle_lighting()
		_cycle_lighting()
		await _capture("lamp-look-%d-152"%int(stage.variants[v]["source_id"]))
		_cycle_lighting()
	await _key(KEY_R)
	_check(compare and choices==[0,1,2]and lighting_mode==0,"keyboard reset")
	var record := {"engine":Engine.get_version_info()["string"],"checks":capture_checks,"static":true,"source_ids":[0,1,3,4,5],"default_height":152,"viewport":[1280,800],"stage":[1200,480],"actor_native_rect":[576,305,128,264],"pixel_filter":"nearest","menu_test":"PopupMenu id_pressed signal route; not physical menu navigation"}
	var file := FileAccess.open("res://evidence/runtime-checks.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(record,"\\t"))
	print("APPEARANCE_CHECKS_COMPLETE ",JSON.stringify(capture_checks))
'''
(p/'playground.gd').write_text(s)
print('Built static appearance UI and fixed-scene renderer')
