# Isolated tote attack playback

This reuses the existing standing/shop Godot preview assets and nearest filtering;
production scenes/textures are untouched. `prepare_runtime.py` binds actual artist
PNG exports and metadata into a fresh `godot/` subdirectory. The first attack frame
is also the resting image; the native sequence must return to that same drawing.

`attack_preview.gd` plays the attack as a one-shot, tests the declared bag rectangle
against a dummy hurtbox only during the authored active interval, permits at most
one hit per attack, and returns to idle after animation_finished. Space starts the
same action; Escape exits. This is a bounded hitbox/timing prototype, not cloth or
rigid-body physics. The dummy placement is chosen from the contact key to exercise
the interaction; it does not establish a final gameplay attack range or balance.

The automated observation injects a Space press/release through
`Input.parse_input_event`, which the [official Input documentation](https://docs.godotengine.org/en/stable/classes/class_input.html#class-input-method-parse-input-event)
describes as feeding an input event into the game and generating input callbacks
(accessed30October2026). No OS keyboard/mouse operation is performed. Runtime JSON
records sent/received events separately and leaves physical_keyboard_tested=false.

The controller-fixture subdirectory uses three identical existing neutral images
and a synthetic100ms active interval. It proves controller/resource/input/hit/return
integration only, not attack art. Final artist attack playback gets its own target,
source hash, metadata, screenshots and debug evidence.

The first synthetic-input fixture exposed an observation-harness stall: awaiting a
return screenshot gated the next scheduled attack when no viewport redraw arrived.
The gameplay/controller loop now schedules its next input independently of capture,
and the capture requests a deferred main-thread force_draw before awaiting post_draw.
[RenderingServer documentation](https://docs.godotengine.org/en/stable/classes/class_renderingserver.html#class-renderingserver-method-force-draw)
confirms this redraw operation (accessed31October2026). The fixture failure and
rerun are retained; they concern evidence capture, not tote art quality.
