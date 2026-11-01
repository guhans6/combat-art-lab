# Artist observations — 30 October 2026

## Exact sources opened

- `../inputs/character-scene.png` and `../inputs/character-closeup.png`: canonical identity and style. The character is a rightward three-quarter young woman with tied brown hair and loose fringe, olive open jacket, off-white shirt, wide blue jeans, pale sneakers, and a cream tote on a continuous shoulder strap. The close-up is the stronger face/material guide; the scene establishes the long-leg silhouette and grounded stance.
- `../inputs/neutral.aseprite` and `../inputs/neutral.png`: opened through the dedicated headless Aseprite MCP. The native is a 128×192 RGB document with one visible idle frame, 11 visible semantic layers plus one hidden source-seed layer (12 total), and a fixed palette. Visible bounds in the PNG are `(32,2)-(104,185)`; this is the provisional body rendering baseline.
- `../inputs/six-keys.png` (1774×887) and `../inputs/additional-keys.png` (2172×724): opened at native display size. Both are transparent pose sheets. The main sheet carries idle, draw-to-grip, rightward extension, long follow-through, extended continuation and shoulder return. The second carries a leftward wind-up, the weak upright recovery, and re-shouldering.

## Direct visual observations

- The pose sheets contain soft/partial-alpha edges and local red/blue fringe artifacts. These are contamination candidates only at reviewed silhouette edges; neither color is globally removable because skin and denim contain legitimate warm/cool marks.
- The generated pose art is more painterly and detailed than the neutral native. It is guidance for pose, silhouette and attachment relationships; pixel art will be rebuilt in the neutral's palette and visible material roles.
- The broad strike and lunge already read as useful macro keys. The weak upright recovery visually interrupts the swing: the arms straighten and the tote hangs vertically too early. The intermediate must show pelvis/thorax beginning to brake, both elbows folding while both hands share the handle bundle, and the bag staying slightly downstream before it settles toward the carry-side hip.
- The start/end idle source is kept byte/pixel-identical in the authored sequence. Facial expression, hair mass, costume colors, body proportions, and material lighting remain protected from redesign.

## Scale and anchor hypothesis

The main sheet's six source-alpha bounds at alpha ≥128 have heights 424, 422, 413, 414, 409 and 416 px. Candidate shared nearest-neighbor scale `0.4333` (median source height ≈415 px → ≈180 native px), not per-pose silhouette fitting. The second sheet's heights are 666, 699 and 696 px; candidate shared scale `0.264` (median ≈696 px → ≈184 native px). These values remain provisional until scaled pose/head envelopes, eyeline, pelvis height and leg proportions are compared against the neutral at 1×. Register by pelvis/root and foot landmarks, preserving authored lunge/toe pivots; tote width is not a centering anchor. The neutral 128×192 source is placed at x=64 on the 256×192 canvas, with no enlargement.

These are seed/placement values; actual registered pose anchors and alpha bounds will be recorded from the exported frames. Any source-seeded regions will be cleaned or redrawn in semantic native layers before being retained as a usable pose.

## Uncertain

- Input images are pose proposals, not accepted sprite frames or temporal playback.
- The source sheets do not determine exact in-betweens, game camera scale, bag contents, physics, or collision timing.
- Parent will choose the Godot dummy's active interval from the measured contact drawing; a single committed-contact drawing is the current artist proposal.
