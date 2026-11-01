# Pass 02 observations

## Artifact and requested profile

- Requested configuration: `gpt-6-luna`, maximum effort. Provider compute and cost telemetry were not exposed in the trial artifacts.
- Native source: `pass-02.aseprite` (document `#129`, 128×192 RGB, one frame).
- PNG export: `pass-02.png`; SHA-256 `1f8a00710c5cfc6678d0a392b5c6c4453682b162bc893da1a50056a1c2c6edaf`.
- Review images: `pass-02-review-sheet.png`, `pass-02-head-review.png`, `pass-02-alpha-holes.png`, and `pass-02-source-hole-grid.png`.

## Art and native structure

The second pass redraws the eyes and mouth on a dedicated `Facial features` layer to make the unequal near/far eye shapes and rightward gaze more distinct, with a shallow curved mouth. Face changes are limited to the small face feature area; no silhouette pixels or alpha values changed. At native full-body size, the expression remains small; the head review is provided for close inspection and awaits supervisor review.

The native source has nine visible editable layers: `Face, neck, hands`, `Hair`, `Tote and strap`, `Shirt`, `Jacket`, `Jeans`, `Shoes`, `Contour details`, and `Facial features`. `scripts/prepare_semantic_layers.py` partitions the 7,834 visible seed pixels into those named parts, verifies that the unmodified partition recomposes the seed exactly, and records the face edits separately. `prep/semantic-pass02/draw-grids.json` is the exact grid input used for the nine native layers. `prep/semantic-pass02/part-isolation-sheet.png` shows each part in isolation.

## Technical checks

- Export size is 128×192; alpha is binary; visible bounds are `(32, 3, 104, 185)`; visible pixel count is 7,834; palette size is 35.
- `scripts/verify_export.py` reports that the actual Aseprite PNG matches the locally prepared layered composite exactly, has unchanged alpha from the seed, and changes 32 visible pixels from the seed, all within the face feature cleanup.
- Aseprite `sprite_info` reports nine named, visible, editable cels and one frame. `palette analyze` reports zero off-palette colors; it reports 11 near-duplicate color pairs already present in the source-derived 35-color palette.
- The raw alpha-coverage check flags 26 enclosed transparent pixels. Its warning coordinates are identical to pass 01, and all 26 are unchanged from the seed. Each corresponding 8×8 source block has 0–31 pixels above the source alpha threshold of 32, out of 64. I reviewed the source blocks in `pass-02-source-hole-grid.png` and the target locations in `pass-02-alpha-holes.png`; they fall in hair/face edge openings and the gap between the legs. The reviewed `--allow-holes` run passes with no missing solid-mask pixels. Raw and reviewed results are retained as `pass-02-alpha-check.json` and `pass-02-alpha-check-reviewed.json`.
- The first pass-02 review sheet had a centering error that clipped the approved figure. The corrected `pass-02-review-sheet.png` centers the complete crop on the 128×192 canvas; `pass-02-review-sheet-initial.png` preserves the earlier sheet. Head labels are shortened to fit at 1× and 4×.
- Aseprite MCP `look preview` returned a black-looking transparent preview in this headless session. I inspected the saved PNG and review sheets directly; the exported pixels match the local expected composite.

## Tool budget and remaining work

Pass 01 used 58 Aseprite/editor calls. Pass 02 used 22 calls (preflight, new document, inspection, palette/layer setup, nine draws, preview and ASCII inspection, save, export, and post-save inspection), for 80 of 120 total. One artistic pass remains. The proof-only duplicate edit, protection check, and fresh native reopen/export equality remain to be completed within the remaining 40 calls after supervisor review. This candidate is not user-approved and has no Godot/runtime validation.
