# Animation from generated references and native finishing

## Inputs may be a sheet or multiple images
Both are permitted. Attach the canonical identity/style references and the accepted native style sample to each request. A coherent short sheet is a useful first candidate when layout is manageable; individual key poses are useful when a sheet is cramped or one pose needs correction. These are options, not evidence that either always gives better consistency.

First define action, facing, camera, key phases and whether motion is in-place or travels. Weapon/equipment choices remain user art decisions. A blink or weight shift can be a technical motion smoke test, but does not replace the project's representative combat proof.

## Reference generation and selection
Use `prompts/04_ANIMATION_KEYPOSES.md` or `03_POSE_OR_VIEW.md`. Keep the original attachments available; do not rely on a previous generation's text description. Generate only missing phases/views. A requested frame count and equal slots are instructions, not a verified output layout.

Check every frame for clothing/accessory changes, head size, facial identity, palette shifts, disappearing hair/tote parts, inconsistent camera and anatomy. Intended anticipation/squash/expression changes are not automatically drift. Keep a pose brief so the distinction is explicit.

## Geometry and timing contract
- Use one common source-to-native scale for a coherent set; do not auto-fit each silhouette independently.
- Declare fixed output frame dimensions with margins for the full action envelope.
- Use actual measured pivot/contact landmarks, not an automatic bounding-box bottom. Register where each source image represents the shared root.
- Record intentional root displacement separately. A jump or lunge must not be flattened back onto the idle anchor.
- Declare frame order and duration explicitly. A four-pose storyboard is not automatically a finished four-frame attack or a loop.
- Keep one approved palette policy; quantizing every frame independently can change material colors between frames.

Independent source images may have genuinely different drawing scales. Correct that with measured anatomical references and documented transforms, not silhouette-box fitting. The bundled helper assumes the sources have already been brought to a coherent source scale; it cannot infer body dimensions.

## Native production
Trace, convert and/or redraw each accepted key pose using the selected static method. Build shared layer roles and palette behavior. Request/draw needed in-betweens instead of assuming interpolation creates correct anatomy. Keep effects separate so body motion remains inspectable.

Separate canonical raw source images, aligned guides, conversion seeds, native frames, exported frames and runtime metadata. Retain the reference and prompt used for every pose.

## Helper boundary
`scripts/reference_lab.py normalize` uses explicit crops, source anchors, one scale and optional output-space motion offsets. It refuses visible clipping and fresh-output overwrites. It writes equal-sized PNG frames, a sheet and processing metadata. It does not remove backgrounds, find characters, judge identity, create intermediate poses, fix timing or author Aseprite layers. Normalizing a flawed generated sheet does not make it a finished animation.

`templates/animation_layout.example.json` is a schema example with placeholder input paths, not an already executable animation job. `examples/normalization_smoke/` is a technical normalization test using the existing sprite with declared offsets, not new pose art.

## Actual validation
Inspect a contact sheet, onion-skin/played Aseprite view and recorded timing. Watch for foot skating, volume changes, texture flicker and root discontinuities. Review frame-by-frame at 1× plus intended playback speed. In Godot, verify import filtering, pivot, display size, timing and the actual action/contact behavior on the installed version before reporting success.

Aseprite and Godot mechanisms are documented in research sources S15–S16. No new animation or Godot playback is claimed by this kit.
