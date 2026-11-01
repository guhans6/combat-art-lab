# Pass 01 observations

## Artifact and scope

- Requested profile: `gpt-6-luna`, maximum effort. Provider execution telemetry is not embedded in this artifact.
- Native document: `pass-01.aseprite` (128×192), with a locked source-derived seed layer and editable face/expression overlay.
- Export: `pass-01.png`; SHA-256 `11fdc75d43ed0e920dddeca17e30bc420521539359eddbe104a33c6274b68b27`.
- Review: `pass-01-review-sheet.png`, `pass-01-head-review.png`, and `pass-01-alpha-mattes.png`.
- Reproducible edit input: `../operations/pass-01-face-grid.json`.

## Construction and checks

- The source cutout was reduced to 128×192 using the frozen preparation recipe. The encoded seed was drawn into its own named layer; readback matched all 7,834 visible seed pixels and 35 visible colors.
- The correction added 8 visible pixels, with no alpha changes. Pixels outside the edit mask were unchanged. The exported image has binary alpha and 35 visible colors; its nontransparent bounds are `(32, 3, 104, 185)`.
- The alpha-coverage check flagged 26 interior transparent pixels as unexpected. The full coordinate list is retained in `pass-01-alpha-check.json`; the light, dark, and checker views are in `pass-01-alpha-mattes.png`. This flag remains unresolved for review.
- Aseprite/editor MCP call count through export: 58 of the 120-call budget, including 35 isolated smoke-check calls and 23 pass-01 calls. The pass-01 source was saved and exported before releasing the editor slot.

## Visual observations

The full-body silhouette, rightward three-quarter pose, clothing blocks, tote, and shoes remain legible against the approved reference. The new eye and mouth marks are visible in the enlarged head crop, but expression detail remains small at native canvas scale. The alpha-coverage finding and any art defects remain open pending defect-only review. This is a benchmark candidate, not user-approved art or a gameplay-validated asset.

## Review evidence

- `pass-01-properties.json` records image dimensions, bounds, alpha levels, palette size, and seed-difference counts.
- `pass-01-review-sheet.json` and `pass-01-head-review.json` record their review-panel inputs and scale.
- Aseprite MCP smoke results and limitations are recorded in `../scratch-smoke.md`.
