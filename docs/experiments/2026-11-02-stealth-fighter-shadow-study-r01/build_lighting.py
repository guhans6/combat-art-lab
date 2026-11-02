from pathlib import Path
import shutil
w=Path('/private/tmp/fighter-shadow-study-r01');p=w/'project';q=p/'stage.gd';s=q.read_text().replace('[96.0, 128.0, 160.0]','[128.0, 152.0, 160.0]').replace('var compare := true','var compare := false');q.write_text(s)
q=p/'playground.gd';s=q.read_text().replace('var compare := true','var compare := false').replace('stage.heights = [96.0,128.0,160.0]','stage.heights = [128.0,152.0,160.0]').replace('\tcompare = true\n\tpaused = false','\tcompare = false\n\tpaused = false').replace('height_slider.value = 128','height_slider.value = 152').replace('CURRENT A   /   IDLE & SCALE PLAYGROUND','CURRENT A   /   152 PX & LIGHTING STUDY').replace('PLAYGROUND_READY frames=4 durations_ms=[700,260,500,340] heights=[96,128,160]','SHADOW_STUDY_READY frames=4 durations_ms=[700,260,500,340] heights=[128,152,160]').replace('M  compare / single     1 / 2 / 3  select','L  lighting     M  compare / single     1 / 2 / 3  select')
s=s.replace('var self_test := false','var self_test := false\nvar world_canvas: CanvasLayer\nvar ambient: CanvasModulate\nvar fill_lights: Array[PointLight2D] = []\nvar lighting_mode := 0\nvar lighting_button: Button\nvar lighting_label: Label')
s=s.replace('\tcompare_button = _button(', '\tlighting_button = _button("", Rect2(640,25,280,42), _cycle_lighting)\n\tlighting_label = _label("", Vector2(640,72), 12, Color("9b9690"))\n\tcompare_button = _button(',1)
s=s.replace('\tadd_child(stage)\n','\tworld_canvas = CanvasLayer.new()\n\tworld_canvas.layer = -1\n\tadd_child(world_canvas)\n\tworld_canvas.add_child(stage)\n\t_setup_lighting()\n',1)
s=s.replace('\tstage.frame_index = _frame_at(phase_ms)\n\tstage.queue_redraw()\n\nfunc _mode', '\tstage.frame_index = _frame_at(phase_ms)\n\t_update_lighting()\n\tstage.queue_redraw()\n\nfunc _mode',1)
s=s.replace('\tspeed_index = 1\n\t_sync()\n\nfunc _input','\tspeed_index = 1\n\tlighting_mode = 0\n\t_sync()\n\nfunc _input',1)
s=s.replace('\t\tKEY_M: _mode(not compare)','\t\tKEY_L: _cycle_lighting()\n\t\tKEY_M: _mode(not compare)')
s=s[:s.index('func _run_checks() -> void:')]
s+='''func _setup_lighting() -> void:
	ambient = CanvasModulate.new()
	world_canvas.add_child(ambient)
	var gradient := Gradient.new()
	gradient.set_color(0, Color(1,1,1,1))
	gradient.set_color(1, Color(1,1,1,0))
	var light_texture := GradientTexture2D.new()
	light_texture.width = 512
	light_texture.height = 512
	light_texture.fill = GradientTexture2D.FILL_RADIAL
	light_texture.fill_from = Vector2(0.5,0.5)
	light_texture.fill_to = Vector2(1,0.5)
	light_texture.gradient = gradient
	for i in range(3):
		var light := PointLight2D.new()
		light.position = Vector2(240+i*400,458)
		light.texture = light_texture
		light.texture_scale = 0.9
		light.energy = 1.8
		light.color = Color(1.0,0.9,0.75)
		light.range_layer_min = -1
		light.range_layer_max = -1
		light.shadow_enabled = false
		world_canvas.add_child(light)
		fill_lights.append(light)

func _cycle_lighting() -> void:
	lighting_mode = (lighting_mode+1)%3
	_update_lighting()

func _update_lighting() -> void:
	ambient.color = Color.WHITE if lighting_mode==0 else Color(0.35,0.35,0.35,1)
	for light in fill_lights:
		light.enabled = lighting_mode==2
	lighting_button.text = ["Light: Sprite colors", "Light: Dim room", "Light: Lamp fill"][lighting_mode]
	lighting_label.text = ["Original painted colors. No scene light.", "35% room light; no fill.", "Same dim room + warm PointLight2D fill."][lighting_mode]

func _run_checks() -> void:
	await get_tree().create_timer(5.8).timeout
	_check(loops>=3,"three authored loops")
	_check(not compare and selected==1 and stage.heights==[128.0,152.0,160.0],"default Single152")
	paused = true
	phase_ms = 0
	_sync()
	await _capture("sprite-colors-152")
	await _click(lighting_button)
	_check(lighting_mode==1,"mouse selects dim room")
	await _capture("dim-room-152")
	await _key(KEY_L)
	_check(lighting_mode==2,"keyboard selects lamp fill")
	await _capture("lamp-fill-152")
	await _click(lighting_button)
	_check(lighting_mode==0,"mouse returns exact sprite colors")
	await _click(compare_button)
	_check(compare,"mouse comparison mode")
	await _capture("compare-128-152-160")
	await _click(solo_button)
	_check(not compare,"mouse single mode")
	await _click(slots[0])
	_check(selected==0,"mouse select A")
	await _click(height_slider, Vector2(0.8,0.5))
	_check(stage.heights[0]!=128 and stage.heights[0]>=64 and stage.heights[0]<=240,"mouse height slider")
	await _key(KEY_2)
	_check(selected==1,"keyboard selects B152")
	var frozen := phase_ms
	await get_tree().create_timer(0.2).timeout
	_check(phase_ms==frozen,"pause holds timeline")
	await _click(next_button)
	_check(_frame_at(phase_ms)==1 and paused,"mouse frame step")
	await _key(KEY_COMMA)
	_check(_frame_at(phase_ms)==0,"keyboard previous frame")
	await _key(KEY_SPACE)
	_check(not paused,"keyboard resume")
	await get_tree().create_timer(0.2).timeout
	_check(phase_ms>0,"resume advances timeline")
	await _click(speed_button)
	_check(speed_index==2,"mouse2x speed")
	await _click(guide_button)
	_check(guides,"mouse guides")
	await _click(reset_button)
	_check(not compare and selected==1 and stage.heights==[128.0,152.0,160.0] and lighting_mode==0 and not paused and not guides,"reset restores Single152 and neutral light")
	paused = true
	for i in range(4):
		phase_ms = STARTS[i]
		_sync()
		await _capture("source-152-frame-%02d"%i)
	_height_changed(240)
	for i in range(4):
		phase_ms = STARTS[i]
		_sync()
		await _capture("native-frame-%02d"%i)
	await _key(KEY_R)
	_check(not compare and stage.heights==[128.0,152.0,160.0] and lighting_mode==0,"keyboard reset152")
	var record := {"engine":Engine.get_version_info()["string"],"checks":capture_checks,"loops_before_checks":loops,"viewport":[1280,800],"stage":[1200,480],"actor_native_rect":[576,305,128,264],"source_body":240,"working_height":152,"durations_ms":DURATIONS,"lighting_modes":["source colors exact","ambient0.35","ambient0.35 plus warm PointLight2D1.8"],"normal_maps":false,"cast_shadow_occluders":false,"world_layer":-1,"ui_layer":0}
	var file := FileAccess.open("res://evidence/runtime-checks.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(record,"\\t"))
	print("SHADOW_STUDY_CHECKS_COMPLETE ", JSON.stringify(capture_checks))
'''
q.write_text(s)
q=p/'project.godot';q.write_text(q.read_text().replace('Current A — The Quiet Keep','Current A — 152px Lighting Study'))
t=w/'check-project';shutil.copytree(p,t);(t/'RUN_CHECKS').write_text('Isolated lighting/UI/protection checks.\n')
print('Created152px lighting study')
