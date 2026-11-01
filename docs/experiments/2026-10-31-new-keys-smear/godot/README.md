# Tote smear comparison fixture

This is an isolated Godot 4.7 project prepared for the experiment's eventual exports.
It has not been launched or engine-validated in this task.

## Export handoff contract

Place these files in the sibling `../exports/` directory. The project loads them by
absolute filesystem path using `Image.load_from_file`; it does not copy them into
`res://`, import them, or modify native Aseprite sources.

- `tote-clean-sheet.png`: horizontal strip of clean/no-smear frames.
- `tote-smear-sheet.png`: horizontal strip with the same cells, timing and registration;
  only the deliberately authored smear drawings differ.
- `tote-prop-sheet.png`: horizontal strip with the same cells; each cell is the
  transparent export of only the native tote-owner layers (rear handle, body/rim, and
  near handles), not a character composite. It is required for runtime-trail probes.
- `timing.json`: required metadata, in this exact minimal shape:

```json
{
  "frame_size": [256, 208],
  "frame_count": 8,
  "durations_ms": [120, 90, 70, 60, 90, 140, 160, 220],
  "phases": ["idle", "lift", "windup", "swing", "contact", "follow-through", "smear", "idle-return"],
  "contact_frames_1based": [5],
  "smear_frames_1based": [7],
  "target_rect_xywh": [210, 80, 12, 40],
  "trail_rects_xywh": [[150, 45, 106, 100]]
}
```

`frame_count` cells must be laid left-to-right; all three sheets must be exactly
`frame_count * 256` by `208` pixels; this applies to all three sheets. Each prop-sheet
cell must contain both opaque prop pixels and transparent background or startup fails.
The fixture never falls back to a full-character frame for a runtime trail. `target_rect_xywh` is optional and only places a
simple dummy at the swing front. When a declared contact frame is reached, the fixture
counts clean-sheet opaque pixels within that rectangle and records
`contact_opaque_pixels`; zero pixels emits a runtime error. This is a narrow contact
pixel-test, not combat collision or balance validation. `trail_rects_xywh` is optional
per-frame prop crop metadata; absent entries use `[150, 45, 106, 100]`, which excludes
the head/body and never ghosts the whole character.

## Runtime controls and evidence

Both panels animate from the same metadata clock. `A` is the default comparison:
**clean** on the left and **authored smear** on the right. Runtime afterimages are
always visibly labelled **RUNTIME TRAIL (NOT DRAWN SMEAR)**. They are a comparison aid,
not a substitute for drawn deformation. The effect can spawn only while entering or
leaving a declared smear frame, never through recovery or idle.

- `Space`/`R`: replay the attack
- `P`: pause; `F`: step one frame
- `A`: clean / authored-smear (default)
- `B`: clean / clean control
- `C`: clean / clean plus runtime trail (the independent runtime-trail probe)
- `D`: authored-smear / authored-smear plus runtime trail (hybrid probe)
- `1`: native 1x window; `2`: integer 2x window
- `Esc`: exit

Normal startup automatically runs three default `A` loops, captures each encountered
frame and exact idle return, then runs one `C` clean-plus-runtime-trail probe and
captures the declared `smear` phase before restoring `A` for interactive review.
It writes `event-log.json` with frame/phase/contact/loop and probe-state events.
A real dedicated-Godot-MCP observation is still required before those files are
treated as runtime evidence. Physical keyboard input is not asserted by the scripted
observation. `--interactive-only` is available only for local manual runs.
