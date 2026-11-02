extends Control

const StageScript = preload("res://stage.gd")
const DURATIONS := [700.0, 260.0, 500.0, 340.0]
const STARTS := [0.0, 700.0, 960.0, 1460.0]
const SPEEDS := [0.5, 1.0, 2.0]
var stage
var compare := true
var selected := 1
var paused := false
var guides := false
var phase_ms := 0.0
var speed_index := 1
var loops := 0
var compare_button: Button
var solo_button: Button
var slots: Array[Button] = []
var pause_button: Button
var previous_button: Button
var next_button: Button
var reset_button: Button
var speed_button: Button
var guide_button: Button
var height_slider: HSlider
var height_label: Label
var status_label: Label
var capture_checks: Array = []
var self_test := false

func _ready() -> void:
	_build_theme()
	_label("THE QUIET KEEP", Vector2(40,22), 30, Color("eee5d2"))
	_label("CURRENT A   /   IDLE & SCALE PLAYGROUND", Vector2(42,62), 13, Color("9b9690"))
	_label("Ruined cloister · fixed camera", Vector2(952,35), 16, Color("b4a890"))
	compare_button = _button("Side by side", Rect2(40,100,168,42), func(): _mode(true))
	solo_button = _button("Single", Rect2(216,100,120,42), func(): _mode(false))
	for i in range(3):
		var index := i
		slots.append(_button("", Rect2(376+i*140,100,132,42), func(): _select(index)))
	pause_button = _button("Pause", Rect2(824,100,122,42), _toggle_pause)
	previous_button = _button("‹", Rect2(954,100,48,42), func(): _step(-1))
	next_button = _button("›", Rect2(1010,100,48,42), func(): _step(1))
	reset_button = _button("Reset", Rect2(1080,100,160,42), _reset)
	stage = StageScript.new()
	stage.position = Vector2(40,158)
	stage.size = Vector2(1200,480)
	add_child(stage)
	height_label = _label("", Vector2(40,666), 16, Color("e0d4b9"))
	height_slider = HSlider.new()
	height_slider.position = Vector2(228,661)
	height_slider.size = Vector2(460,32)
	height_slider.min_value = 64
	height_slider.max_value = 240
	height_slider.step = 8
	height_slider.value = 128
	add_child(height_slider)
	height_slider.value_changed.connect(_height_changed)
	_label("64", Vector2(228,696), 12, Color("8d8d94"))
	_label("240", Vector2(663,696), 12, Color("8d8d94"))
	speed_button = _button("Speed · 1×", Rect2(746,655,164,42), _cycle_speed)
	guide_button = _button("Guides: off", Rect2(922,655,170,42), _toggle_guides)
	status_label = _label("", Vector2(1110,665), 14, Color("a7a19b"))
	_label("M  compare / single     1 / 2 / 3  select     Space  pause     , / .  step frame     R  reset     F11  fullscreen", Vector2(40,734), 14, Color("b4afa6"))
	_label("Heights are scene pixels. The world stays fixed; only the character scales.  |  Backdrop: Luis Zuno / ansimuz · public domain", Vector2(40,766), 12, Color("777b83"))
	_sync()
	print("PLAYGROUND_READY frames=4 durations_ms=[700,260,500,340] heights=[96,128,160] stage=1200x480 ground=400")
	self_test = FileAccess.file_exists("res://RUN_CHECKS")
	if self_test:
		call_deferred("_run_checks")

func _build_theme() -> void:
	var t := Theme.new()
	t.default_font_size = 16
	for kind in ["normal", "hover", "pressed", "focus"]:
		var box := StyleBoxFlat.new()
		box.bg_color = Color("252b30") if kind == "normal" else Color("373c40")
		box.border_color = Color("b29b70") if kind in ["pressed", "focus"] else Color("44474b")
		box.set_border_width_all(1)
		box.set_corner_radius_all(3)
		box.content_margin_left = 14
		box.content_margin_right = 14
		t.set_stylebox(kind, "Button", box)
	t.set_color("font_color", "Button", Color("d1c9b8"))
	t.set_color("font_hover_color", "Button", Color("fff2d7"))
	t.set_color("font_pressed_color", "Button", Color("fff2d7"))
	var track := StyleBoxFlat.new()
	track.bg_color = Color("343940")
	track.set_corner_radius_all(2)
	track.content_margin_top = 4
	track.content_margin_bottom = 4
	t.set_stylebox("slider", "HSlider", track)
	theme = t

func _label(text: String, point: Vector2, font_size: int, color: Color) -> Label:
	var label := Label.new()
	label.text = text
	label.position = point
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(label)
	return label

func _button(text: String, rect: Rect2, handler: Callable) -> Button:
	var button := Button.new()
	button.text = text
	button.position = rect.position
	button.size = rect.size
	button.focus_mode = Control.FOCUS_NONE
	button.pressed.connect(handler)
	add_child(button)
	return button

func _process(delta: float) -> void:
	if not paused:
		phase_ms += delta * 1000.0 * SPEEDS[speed_index]
		while phase_ms >= 1800.0:
			phase_ms -= 1800.0
			loops += 1
	stage.frame_index = _frame_at(phase_ms)
	stage.queue_redraw()
	status_label.text = "F%d / 4  ·  1.8s" % (stage.frame_index + 1)

func _frame_at(time: float) -> int:
	var end := 0.0
	for i in range(4):
		end += DURATIONS[i]
		if time < end:
			return i
	return 0

func _sync() -> void:
	stage.compare = compare
	stage.selected = selected
	stage.guides = guides
	height_slider.set_value_no_signal(stage.heights[selected])
	height_label.text = "%s height   ·   %d px" % [char(65+selected), int(stage.heights[selected])]
	for i in range(3):
		slots[i].text = "%s   %d px" % [char(65+i), int(stage.heights[i])]
		slots[i].modulate = Color.WHITE if i == selected else Color(0.7,0.7,0.7)
	compare_button.modulate = Color.WHITE if compare else Color(0.65,0.65,0.65)
	solo_button.modulate = Color.WHITE if not compare else Color(0.65,0.65,0.65)
	pause_button.text = "Play" if paused else "Pause"
	speed_button.text = "Speed · %s×" % SPEEDS[speed_index]
	guide_button.text = "Guides: on" if guides else "Guides: off"
	stage.frame_index = _frame_at(phase_ms)
	stage.queue_redraw()

func _mode(value: bool) -> void:
	compare = value
	_sync()
func _select(index: int) -> void:
	selected = index
	_sync()
func _height_changed(value: float) -> void:
	stage.heights[selected] = value
	_sync()
func _toggle_pause() -> void:
	paused = not paused
	_sync()
func _step(direction: int) -> void:
	paused = true
	phase_ms = STARTS[posmod(_frame_at(phase_ms)+direction,4)]
	_sync()
func _cycle_speed() -> void:
	speed_index = (speed_index+1)%3
	_sync()
func _toggle_guides() -> void:
	guides = not guides
	_sync()
func _reset() -> void:
	stage.heights = [96.0,128.0,160.0]
	selected = 1
	compare = true
	paused = false
	guides = false
	phase_ms = 0
	speed_index = 1
	_sync()

func _input(event: InputEvent) -> void:
	if event is not InputEventKey or not event.pressed or event.echo:
		return
	match event.keycode:
		KEY_M: _mode(not compare)
		KEY_1: _select(0)
		KEY_2: _select(1)
		KEY_3: _select(2)
		KEY_SPACE: _toggle_pause()
		KEY_COMMA: _step(-1)
		KEY_PERIOD: _step(1)
		KEY_R: _reset()
		KEY_G: _toggle_guides()
		KEY_F11:
			DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED if DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN else DisplayServer.WINDOW_MODE_FULLSCREEN)
		_: return
	get_viewport().set_input_as_handled()

func _click(control: Control, proportion := Vector2(0.5,0.5)) -> void:
	var point := control.get_global_rect().position + control.size * proportion
	for pressed in [true,false]:
		var event := InputEventMouseButton.new()
		event.position = point
		event.button_index = MOUSE_BUTTON_LEFT
		event.pressed = pressed
		Input.parse_input_event(event)
		await get_tree().process_frame

func _key(code: Key) -> void:
	for pressed in [true,false]:
		var event := InputEventKey.new()
		event.keycode = code
		event.pressed = pressed
		Input.parse_input_event(event)
		await get_tree().process_frame

func _capture(capture_name: String) -> void:
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("res://evidence/"+capture_name+".png")

func _check(condition: bool, check_name: String) -> void:
	capture_checks.append({"name":check_name,"passed":condition})
	if not condition:
		push_error("PLAYGROUND_CHECK_FAILED "+check_name)

func _run_checks() -> void:
	await get_tree().create_timer(5.8).timeout
	_check(loops>=3,"authored clock completes three loops")
	paused = true
	phase_ms = 0
	_sync()
	await _capture("compare")
	await _click(solo_button)
	_check(not compare,"mouse single view")
	await _click(slots[0])
	_check(selected==0,"mouse select A")
	await _click(height_slider, Vector2(0.8,0.5))
	_check(stage.heights[0]!=96 and stage.heights[0]>=64 and stage.heights[0]<=240,"mouse slider changes selected height")
	await _key(KEY_2)
	_check(selected==1,"keyboard select B")
	phase_ms = 0
	paused = true
	_sync()
	await _capture("single-128")
	var frozen := phase_ms
	await get_tree().create_timer(0.2).timeout
	_check(phase_ms==frozen,"pause holds timeline")
	await _click(next_button)
	_check(_frame_at(phase_ms)==1 and paused,"mouse step next pauses on transition")
	await _key(KEY_COMMA)
	_check(_frame_at(phase_ms)==0,"keyboard previous frame")
	await _key(KEY_SPACE)
	_check(not paused,"keyboard resume")
	await get_tree().create_timer(0.2).timeout
	_check(phase_ms>0,"resume advances timeline")
	await _click(speed_button)
	_check(speed_index==2,"mouse 2x speed")
	await _click(guide_button)
	_check(guides,"mouse guides")
	await _key(KEY_M)
	_check(compare,"keyboard comparison mode")
	await _click(reset_button)
	_check(compare and selected==1 and stage.heights==[96.0,128.0,160.0] and speed_index==1 and not paused and not guides,"mouse reset restores defaults")
	# Exact source-scale proof, one image per authored entry, no character recolor.
	_mode(false)
	_height_changed(240)
	paused = true
	for i in range(4):
		phase_ms = STARTS[i]
		_sync()
		await _capture("native-frame-%02d"%i)
	await _key(KEY_R)
	_check(compare and stage.heights==[96.0,128.0,160.0],"keyboard reset")
	var record := {"engine":Engine.get_version_info()["string"],"checks":capture_checks,"loops_before_checks":loops,"viewport":[1280,800],"stage":[1200,480],"actor_native_rect":[576,305,128,264],"source_body":240,"durations_ms":DURATIONS,"camera_changes_between_modes":false}
	var file := FileAccess.open("res://evidence/runtime-checks.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(record,"\t"))
	print("PLAYGROUND_CHECKS_COMPLETE ", JSON.stringify(capture_checks))
