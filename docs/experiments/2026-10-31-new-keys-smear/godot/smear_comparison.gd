extends Node2D

# Public export contract (all files are sibling files, intentionally outside res://):
#   ../exports/tote-clean-sheet.png       horizontal 256x208 cells
#   ../exports/tote-smear-sheet.png       same cell count/order as clean
#   ../exports/tote-prop-sheet.png        isolated transparent tote-owner cells
#   ../exports/timing.json                see README for required fields
# Images are decoded at runtime with Image.load_from_file so this project never copies,
# imports, or mutates the artist's exported PNGs.

const CELL_SIZE := Vector2i(256, 208)
const VIEWPORT_SIZE := Vector2i(640, 280)
const LEFT_ROOT := Vector2(28, 39)
const RIGHT_ROOT := Vector2(356, 39)
const PANEL_SIZE := Vector2(284, 224)
const TRAIL_LIFETIME_MS := 85
const MAX_TRAIL_GHOSTS := 3

var meta: Dictionary = {}
var clean_frames: Array[ImageTexture] = []
var smear_frames: Array[ImageTexture] = []
var prop_frames: Array[ImageTexture] = []
var clean_source_images: Array[Image] = []
var smear_source_images: Array[Image] = []
var prop_source_images: Array[Image] = []
var clean_actor: Sprite2D
var smear_actor: Sprite2D
var clean_target: ColorRect
var smear_target: ColorRect
var status: Label
var left_title: Label
var right_title: Label
var left_uses_smear := false
var right_uses_smear := true
var current_frame := 0
var elapsed_in_frame_ms := 0.0
var running := false
var paused := false
var runtime_trail_enabled := false
var loop_count := 0
var contact_fired_this_loop := false
var started_ms := 0
var frame_events: Array = []
var loop_events: Array = []
var contact_events: Array = []
var contact_errors: Array = []
var captured_frames: Dictionary = {}
var capture_pending := false
var trail_ghosts: Array[Dictionary] = []
var auto_observe := true
var observation_stage := "primary"
var probe_events: Array = []

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	# The Godot MCP run schema does not pass user arguments. Observe by default, then
	# leave the scene open for interactive review; --interactive-only is optional locally.
	auto_observe = not ("--interactive-only" in OS.get_cmdline_user_args())
	if not _load_export_contract():
		return
	_build_scene()
	_set_probe("A", "startup-default")
	_set_frame(0, "ready")
	_capture("comparison-authored-smear-default")
	_write_event_log("ready")
	print("SMEAR_COMPARE_READY engine=%s frame_count=%d cell=%s filter=nearest exports=%s" % [Engine.get_version_info()["string"], clean_frames.size(), CELL_SIZE, _exports_dir()])
	if auto_observe:
		await get_tree().create_timer(0.25).timeout
		_start_replay("automatic-observation")

func _load_export_contract() -> bool:
	var timing_path := _exports_dir().path_join("timing.json")
	if not FileAccess.file_exists(timing_path):
		_fail("Missing timing metadata: " + timing_path)
		return false
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(timing_path))
	if not (parsed is Dictionary):
		_fail("timing.json is not a JSON object")
		return false
	meta = parsed
	var required := ["frame_count", "durations_ms", "phases", "contact_frames_1based"]
	for key in required:
		if not meta.has(key):
			_fail("timing.json missing required key: " + key)
			return false
	var count := int(meta["frame_count"])
	if count <= 0 or meta["durations_ms"].size() != count or meta["phases"].size() != count:
		_fail("frame_count, durations_ms, and phases must have the same positive length")
		return false
	var declared_size: Array = meta.get("frame_size", [CELL_SIZE.x, CELL_SIZE.y])
	if declared_size.size() != 2 or int(declared_size[0]) != CELL_SIZE.x or int(declared_size[1]) != CELL_SIZE.y:
		_fail("This fixture requires frame_size [256, 208]")
		return false
	clean_frames = _load_sheet(_exports_dir().path_join("tote-clean-sheet.png"), count, clean_source_images)
	smear_frames = _load_sheet(_exports_dir().path_join("tote-smear-sheet.png"), count, smear_source_images)
	prop_frames = _load_sheet(_exports_dir().path_join("tote-prop-sheet.png"), count, prop_source_images)
	if clean_frames.is_empty() or smear_frames.is_empty() or prop_frames.is_empty():
		return false
	if not _validate_prop_alpha():
		return false
	return true

func _load_sheet(path: String, frame_count: int, source_images: Array[Image]) -> Array[ImageTexture]:
	if not FileAccess.file_exists(path):
		_fail("Missing sheet: " + path)
		return []
	var sheet: Image = Image.load_from_file(path)
	if sheet == null or sheet.is_empty():
		_fail("Image.load_from_file failed: " + path)
		return []
	if sheet.get_height() != CELL_SIZE.y or sheet.get_width() != CELL_SIZE.x * frame_count:
		_fail("Unexpected sheet dimensions %s for %s; expected %dx%d" % [sheet.get_size(), path, CELL_SIZE.x * frame_count, CELL_SIZE.y])
		return []
	var textures: Array[ImageTexture] = []
	for index in frame_count:
		var cell := Image.create(CELL_SIZE.x, CELL_SIZE.y, false, Image.FORMAT_RGBA8)
		cell.blit_rect(sheet, Rect2i(index * CELL_SIZE.x, 0, CELL_SIZE.x, CELL_SIZE.y), Vector2i.ZERO)
		source_images.append(cell)
		textures.append(ImageTexture.create_from_image(cell))
	return textures

func _validate_prop_alpha() -> bool:
	for index in prop_source_images.size():
		var image: Image = prop_source_images[index]
		var has_opaque := false
		var has_transparent := false
		for y in image.get_height():
			for x in image.get_width():
				if image.get_pixel(x, y).a > 0.0:
					has_opaque = true
				else:
					has_transparent = true
		# Per-pixel alpha establishes the required transparent owner export without
		# relying on a format-introspection API that may differ across Godot versions.
		if not has_opaque or not has_transparent:
			_fail("tote-prop-sheet.png frame %d must be a nonempty transparent prop-owner cell" % (index + 1))
			return false
	return true

func _build_scene() -> void:
	left_title = _panel(LEFT_ROOT - Vector2(12, 27))
	right_title = _panel(RIGHT_ROOT - Vector2(12, 27))
	clean_actor = _actor(LEFT_ROOT)
	smear_actor = _actor(RIGHT_ROOT)
	clean_target = _target(LEFT_ROOT)
	smear_target = _target(RIGHT_ROOT)
	status = Label.new()
	status.position = Vector2(8, 246)
	status.add_theme_font_size_override("font_size", 9)
	add_child(status)
	_update_status()

func _panel(panel_position: Vector2) -> Label:
	var border := ColorRect.new()
	border.position = panel_position
	border.size = PANEL_SIZE
	border.color = Color(0.12, 0.14, 0.18, 1.0)
	add_child(border)
	var title_label := Label.new()
	title_label.position = panel_position + Vector2(4, 4)
	title_label.add_theme_font_size_override("font_size", 9)
	add_child(title_label)
	return title_label

func _actor(actor_position: Vector2) -> Sprite2D:
	var actor := Sprite2D.new()
	actor.centered = false
	actor.position = actor_position
	actor.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	add_child(actor)
	return actor

func _target(root: Vector2) -> ColorRect:
	var local: Array = meta.get("target_rect_xywh", [218, 106, 16, 54])
	var marker := ColorRect.new()
	marker.position = root + Vector2(float(local[0]), float(local[1]))
	marker.size = Vector2(float(local[2]), float(local[3]))
	marker.color = Color(0.35, 0.55, 0.72, 0.75)
	add_child(marker)
	return marker

func _process(delta: float) -> void:
	_update_trails()
	if not running or paused:
		return
	elapsed_in_frame_ms += delta * 1000.0
	while running and not paused:
		var duration: float = float(meta["durations_ms"][current_frame])
		if elapsed_in_frame_ms < duration:
			break
		elapsed_in_frame_ms -= duration
		if current_frame + 1 < clean_frames.size():
			_set_frame(current_frame + 1, "advance")
		else:
			_finish_loop()
			break

func _start_replay(reason: String) -> void:
	running = true
	paused = false
	contact_fired_this_loop = false
	elapsed_in_frame_ms = 0.0
	started_ms = Time.get_ticks_msec()
	_clear_trails()
	_set_frame(0, reason)
	print("SMEAR_COMPARE_REPLAY loop=%d reason=%s" % [loop_count + 1, reason])

func _set_frame(next: int, reason: String) -> void:
	if clean_actor == null or next < 0 or next >= clean_frames.size():
		return
	# A runtime afterimage tests only the authored smear transition, never recovery/idle.
	if runtime_trail_enabled and running and current_frame != next and (_is_smear_frame(current_frame) or _is_smear_frame(next)):
		_add_trail()
	current_frame = next
	clean_actor.texture = _frame_texture(left_uses_smear, current_frame)
	smear_actor.texture = _frame_texture(right_uses_smear, current_frame)
	var event: Dictionary = {"event":"frame", "frame_1based":current_frame + 1, "phase":meta["phases"][current_frame], "declared_elapsed_ms":_declared_elapsed_ms(current_frame), "actual_elapsed_ms":Time.get_ticks_msec() - started_ms, "reason":reason, "loop":loop_count + 1}
	frame_events.append(event)
	if _is_contact_frame(current_frame + 1) and not contact_fired_this_loop:
		contact_fired_this_loop = true
		var opaque_pixels: int = _contact_opaque_pixels(current_frame)
		clean_target.color = Color(0.95, 0.64, 0.28, 0.9)
		smear_target.color = Color(0.95, 0.64, 0.28, 0.9)
		contact_events.append({"event":"contact", "frame_1based":current_frame + 1, "phase":meta["phases"][current_frame], "declared_elapsed_ms":_declared_elapsed_ms(current_frame), "actual_elapsed_ms":Time.get_ticks_msec() - started_ms, "loop":loop_count + 1, "contact_opaque_pixels":opaque_pixels, "target_flash":true, "scope":"clean-frame alpha overlap with provisional dummy rectangle; not full combat collision"})
		if opaque_pixels == 0:
			var error: Dictionary = {"event":"declared-contact-zero-alpha", "frame_1based":current_frame + 1, "target_rect_xywh":meta.get("target_rect_xywh", [218, 106, 16, 54]), "loop":loop_count + 1}
			contact_errors.append(error)
			push_error("SMEAR_COMPARE_CONTACT_ALPHA_FAIL frame=%d: declared contact has zero clean-frame alpha pixels in target rectangle" % (current_frame + 1))
		print("SMEAR_COMPARE_CONTACT frame=%d loop=%d opaque=%d" % [current_frame + 1, loop_count + 1, opaque_pixels])
	_update_status()
	_write_event_log("frame")
	if not captured_frames.has(current_frame) and not capture_pending:
		captured_frames[current_frame] = true
		_capture("frame-%02d" % current_frame)
	if observation_stage == "clean-runtime-trail-probe" and _is_smear_frame(current_frame):
		_capture("probe-clean-runtime-trail-smear-%02d" % current_frame)

func _finish_loop() -> void:
	loop_count += 1
	running = false
	paused = false
	clean_target.color = Color(0.35, 0.55, 0.72, 0.75)
	smear_target.color = Color(0.35, 0.55, 0.72, 0.75)
	loop_events.append({"event":"idle_return", "loop":loop_count, "frame_1based":1, "declared_duration_ms":_declared_duration_ms(), "actual_elapsed_ms":Time.get_ticks_msec() - started_ms, "returned_to_idle":true})
	_set_frame(0, "idle-return")
	_write_event_log("idle-return")
	_capture("return-%02d" % loop_count)
	print("SMEAR_COMPARE_IDLE_RETURN loop=%d" % loop_count)
	if auto_observe and observation_stage == "primary" and loop_count < 3:
		await get_tree().create_timer(0.25).timeout
		_start_replay("automatic-observation")
	elif auto_observe and observation_stage == "primary":
		print("SMEAR_COMPARE_THREE_LOOPS_COMPLETE")
		await get_tree().create_timer(0.25).timeout
		observation_stage = "clean-runtime-trail-probe"
		_set_probe("C", "automatic-clean-runtime-trail-probe")
		_capture("comparison-clean-runtime-trail-start")
		_start_replay("automatic-clean-runtime-trail-probe")
	elif auto_observe and observation_stage == "clean-runtime-trail-probe":
		observation_stage = "complete"
		_set_probe("A", "automatic-restore-default")
		_capture("comparison-restored-authored-smear")
		_write_event_log("automatic-observation-complete")
		print("SMEAR_COMPARE_PROBE_COMPLETE restored=A interactive=true")

func _is_contact_frame(frame_1based: int) -> bool:
	for frame in meta["contact_frames_1based"]:
		if int(frame) == frame_1based:
			return true
	return false

func _contact_opaque_pixels(index: int) -> int:
	var rect_values: Array = meta.get("target_rect_xywh", [218, 106, 16, 54])
	var rect: Rect2i = Rect2i(int(rect_values[0]), int(rect_values[1]), int(rect_values[2]), int(rect_values[3])).intersection(Rect2i(Vector2i.ZERO, CELL_SIZE))
	var opaque: int = 0
	for y in range(rect.position.y, rect.end.y):
		for x in range(rect.position.x, rect.end.x):
			if clean_source_images[index].get_pixel(x, y).a > 0.0:
				opaque += 1
	return opaque

func _declared_elapsed_ms(index: int) -> int:
	var total := 0
	for i in range(index):
		total += int(meta["durations_ms"][i])
	return total

func _declared_duration_ms() -> int:
	var total := 0
	for value in meta["durations_ms"]:
		total += int(value)
	return total

func _is_smear_frame(index: int) -> bool:
	var declared: Array = meta.get("smear_frames_1based", [])
	for frame in declared:
		if int(frame) == index + 1:
			return true
	return str(meta["phases"][index]).to_lower() == "smear"

func _frame_texture(use_authored_smear: bool, index: int) -> ImageTexture:
	return smear_frames[index] if use_authored_smear else clean_frames[index]

func _set_probe(key: String, reason: String) -> void:
	match key:
		"A":
			left_uses_smear = false
			right_uses_smear = true
			runtime_trail_enabled = false
		"B":
			left_uses_smear = false
			right_uses_smear = false
			runtime_trail_enabled = false
		"C":
			left_uses_smear = false
			right_uses_smear = false
			runtime_trail_enabled = true
		"D":
			left_uses_smear = true
			right_uses_smear = true
			runtime_trail_enabled = true
		_:
			return
	_clear_trails()
	if clean_actor != null and not clean_frames.is_empty():
		clean_actor.texture = _frame_texture(left_uses_smear, current_frame)
		smear_actor.texture = _frame_texture(right_uses_smear, current_frame)
	left_title.text = "LEFT — " + ("AUTHORED SMEAR" if left_uses_smear else "NO SMEAR — clean")
	var right_label := "RIGHT — " + ("AUTHORED SMEAR" if right_uses_smear else "NO SMEAR — clean")
	if runtime_trail_enabled:
		right_label = "RIGHT — AUTHORED + TRAIL" if right_uses_smear else "RIGHT — RUNTIME TRAIL (not a drawn smear)"
	right_title.text = right_label
	probe_events.append({"event":"probe", "key":key, "reason":reason, "left":"authored_smear" if left_uses_smear else "clean", "right":"authored_smear" if right_uses_smear else "clean", "runtime_trail_on_right":runtime_trail_enabled, "time_ms":Time.get_ticks_msec()})
	_update_status()
	_write_event_log("probe-" + key)

func _add_trail() -> void:
	# Runtime trails derive only from the isolated native tote-owner export, never a
	# composite character frame. There is intentionally no fallback to full artwork.
	var source: Image = prop_source_images[current_frame]
	var crop: Rect2i = _trail_rect(current_frame)
	var prop_image: Image = Image.create(crop.size.x, crop.size.y, false, Image.FORMAT_RGBA8)
	prop_image.blit_rect(source, crop, Vector2i.ZERO)
	var ghost := Sprite2D.new()
	ghost.centered = false
	ghost.position = RIGHT_ROOT + Vector2(crop.position)
	ghost.texture = ImageTexture.create_from_image(prop_image)
	ghost.modulate = Color(0.7, 0.84, 1.0, 0.38)
	ghost.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	add_child(ghost)
	move_child(ghost, smear_actor.get_index())
	trail_ghosts.append({"node":ghost, "born_ms":Time.get_ticks_msec()})
	while trail_ghosts.size() > MAX_TRAIL_GHOSTS:
		var oldest: Dictionary = trail_ghosts.pop_front()
		oldest["node"].queue_free()

func _trail_rect(index: int) -> Rect2i:
	var declared: Array = meta.get("trail_rects_xywh", [])
	var values: Array = declared[index] if index < declared.size() else [150, 45, 106, 100]
	var fallback := Rect2i(150, 45, 106, 100)
	var requested: Rect2i = Rect2i(int(values[0]), int(values[1]), int(values[2]), int(values[3]))
	var bounded: Rect2i = requested.intersection(Rect2i(Vector2i.ZERO, CELL_SIZE))
	# Metadata may follow the tote arc, but it may not request a whole-character ghost.
	if bounded.size.x <= 0 or bounded.size.y <= 0 or bounded.size.x > 128 or bounded.size.y > 128:
		return fallback
	return bounded

func _frame_image(use_authored_smear: bool, index: int) -> Image:
	return smear_source_images[index] if use_authored_smear else clean_source_images[index]

func _update_trails() -> void:
	var now := Time.get_ticks_msec()
	for index in range(trail_ghosts.size() - 1, -1, -1):
		var entry: Dictionary = trail_ghosts[index]
		var age: float = now - int(entry["born_ms"])
		if age >= TRAIL_LIFETIME_MS:
			entry["node"].queue_free()
			trail_ghosts.remove_at(index)
		else:
			entry["node"].modulate.a = 0.38 * (1.0 - age / TRAIL_LIFETIME_MS)

func _clear_trails() -> void:
	for entry in trail_ghosts:
		entry["node"].queue_free()
	trail_ghosts.clear()

func _capture(label: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	capture_pending = true
	RenderingServer.call_deferred("force_draw")
	await RenderingServer.frame_post_draw
	var image: Image = get_viewport().get_texture().get_image()
	var result := image.save_png("res://evidence/runtime-%s.png" % label)
	print("SMEAR_COMPARE_CAPTURE %s error=%d" % [label, result])
	capture_pending = false

func _write_event_log(reason: String) -> void:
	var output := FileAccess.open("res://evidence/event-log.json", FileAccess.WRITE)
	output.store_string(JSON.stringify({
		"engine":Engine.get_version_info()["string"],
		"viewport":[VIEWPORT_SIZE.x, VIEWPORT_SIZE.y],
		"window_scale":2,
		"filter":"nearest",
		"asset_loading":"Image.load_from_file absolute sibling exports path",
		"source_exports":{"clean":_exports_dir().path_join("tote-clean-sheet.png"), "authored_smear":_exports_dir().path_join("tote-smear-sheet.png"), "isolated_prop_owners":_exports_dir().path_join("tote-prop-sheet.png"), "timing":_exports_dir().path_join("timing.json")},
		"runtime_trail":{"enabled":runtime_trail_enabled, "label":"RUNTIME TRAIL (NOT DRAWN SMEAR)", "lifetime_ms":TRAIL_LIFETIME_MS, "max_ghosts":MAX_TRAIL_GHOSTS, "scope":"isolated tote-owner export, then optional prop crop", "spawn_transitions":"entering or leaving declared smear frames only", "fallback_rect_xywh":[150, 45, 106, 100], "metadata_key":"trail_rects_xywh", "full_character_fallback":false},
		"probe_state":{"left":"authored_smear" if left_uses_smear else "clean", "right":"authored_smear" if right_uses_smear else "clean", "observation_stage":observation_stage},
		"probe_events":probe_events,
		"reason":reason,
		"frame_events":frame_events,
		"contact_events":contact_events,
		"contact_errors":contact_errors,
		"loop_events":loop_events,
		"timeline_note":"declared fields are authored metadata; actual_elapsed_ms is wall-clock observation and does not claim an FPS measurement",
		"captured_frame_indices_0based":captured_frames.keys(),
		"physical_keyboard_tested":false
	}, "\t"))

func _update_status() -> void:
	if status == null:
		return
	var state := "paused" if paused else ("playing" if running else "idle return")
	var trail := "ON — RUNTIME TRAIL (NOT DRAWN SMEAR)" if runtime_trail_enabled else "OFF"
	var phase := "awaiting exports"
	if not clean_frames.is_empty():
		phase = str(meta["phases"][current_frame])
	status.text = "F %d/%d %s | %s | trail:%s | loops:%d\nA clean/authored  B clean/clean  C clean/trail  D authored/trail\nSpace/R replay  P pause  F step  1 1x  2 2x  Esc exit" % [current_frame + 1, clean_frames.size(), phase, state, trail, loop_count]

func _unhandled_key_input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo:
		return
	match event.keycode:
		KEY_SPACE, KEY_R:
			_start_replay("keyboard")
		KEY_P:
			paused = not paused if running else false
		KEY_F:
			if not running:
				running = true
				paused = true
			_set_frame((current_frame + 1) % clean_frames.size(), "manual-step")
		KEY_A:
			_set_probe("A", "keyboard")
		KEY_B:
			_set_probe("B", "keyboard")
		KEY_C:
			_set_probe("C", "keyboard")
		KEY_D:
			_set_probe("D", "keyboard")
		KEY_1:
			get_window().size = VIEWPORT_SIZE
		KEY_2:
			get_window().size = VIEWPORT_SIZE * 2
		KEY_ESCAPE:
			get_tree().quit()
	_update_status()

func _exports_dir() -> String:
	return ProjectSettings.globalize_path("res://").path_join("..").path_join("exports").simplify_path()

func _fail(message: String) -> void:
	push_error("SMEAR_COMPARE_SETUP_FAIL " + message)
	var label := Label.new()
	label.position = Vector2(8, 8)
	label.text = "SETUP ERROR: " + message + "\nSee godot/README.md for the export contract."
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.size = Vector2(624, 70)
	add_child(label)
