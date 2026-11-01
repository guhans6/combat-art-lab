# Luna 6 mouth-only correction observations

## Frozen task

- Baseline native: `inputs/luna6-fullbody-cleanup-baseline.aseprite`, SHA-256 `dbdf2f693872d2b3c5f102cea01bc1e2441d2452d790770b7b68effd6c563348`.
- Baseline composite: `inputs/luna6-fullbody-cleanup-baseline.png`, SHA-256 `c162e373a9b0ed72e2e82f91a6fe6608952444ed3ef9151534fcd29843b65def`.
- Approved close-up: `inputs/character-closeup.png`, SHA-256 `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7`.
- Approved scene: `inputs/character-scene.png`, SHA-256 `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae`.
- Native canvas/palette/layers: 128×192 RGB, 1 frame, 255-entry palette, 12 layers (11 visible, one hidden locked guide); read from reopened copied source with dedicated Aseprite MCP 0.8.2 on Aseprite 1.3.18.6-dev.
- Allowed change: only the small mouth mask below, on the actual owning visible layer. Eyes, all other facial pixels, outline, body, alpha, palette and every other native layer are locked.
- Artistic budget: one initial mouth pass. No artistic retry unless the parent explicitly flags expression failure.

## Direct observations before editing

The approved close-up and scene were opened directly. The close-up mouth is a closed, thin warm-brown stroke on the lower cheek, slightly uneven, with a shallow friendly upturn. There is no exposed tooth line and no open or pout shape. The reference face is softly modeled; the mouth reads quietly at full scene scale. Reference preview crops in `reviews/approved-closeup-face-preview-3x.png`, `approved-scene-face-preview-3x.png` and `approved-closeup-mouth-context-8x.png` are resampled review aids only, not construction sources.

The Luna 6 candidate was opened at native scale and inspected as a full composite and exact ASCII/color grid (`reviews/baseline-mouth-landmarks-12x.png`, `baseline-mouth-grid.png`). Its eyes and face boundary are present, but the lower-face region has no mouth mark. The observed 3×2 mask is centered beneath the eye line, above the lower face/neck transition, and avoids the existing warm cheek pixels at y=27 and the face edge at x≥72. Native `read_pixels(composite:false)` shows these six pixels live in `08-hair-tie-and-hair`; the same mask is transparent in `07-face-and-neck`. The hair layer is therefore the visible owner and received the correction without an ownership transfer.

## Frozen mask and hypothesis (set before drawing)

- Coordinate convention: zero-based canvas pixels, half-open rectangle.
- Mouth-only editable rectangle: `[68,28,71,30)`; x=68–70 and y=28–29, six pixels total. This exact region is also saved as `mouth-mask.json` before the edit.
- Confidence: medium on placement and low-to-medium on exact pixel curvature, because the reference crop is high-resolution/softly rendered while the target face is 128×192. The relative cue is the shallow closed smile below and slightly to the far side of the eyes.
- Hypothesis: a short three-pixel warm-brown stroke with a slight upward slant toward the right will supply the missing quiet, friendly intention at 1× without a cup/U-shaped mouth, pout, wide grin, nose mark, or extra facial detail.
- Explicit locks: every composite pixel outside the six-pixel rectangle; both eye clusters and their brows/fringe; face silhouette/outline; neck; all non-owner layers; alpha; frame/canvas; 255-color palette.
- Decision boundary: compare the exported face at 1× and integer enlargement with the approved originals and baseline. If the first result does not clearly read as a restrained closed smile, stop and report the limitation unless the parent explicitly authorizes the single possible correction.

## Review-triggered correction and final read

The initial three-pixel mark used the frozen first mask. Parent review of its 8× head comparison found it at the far-right lower-face edge, directly under the nearby warm facial patch, where it read as a protruding lip/pout. This met the stated correction condition. The actual approved reference mouth is inside the cheek below the eye line; the baseline's lower face has ample interior pixels before the profile contour. I froze the union correction mask `[65,28,71,30)` before editing, restored the three initial cells to their exact baseline skin colors, and applied the same short stroke two to three pixels inward at `(65,29)`, `(66,29)`, `(67,28)`. The one authorized correction was then exhausted.

The final three-panel head and full-body sheets use the approved reference, untouched Luna 6 baseline, and final correction at 1× and 8×. The close-up reference crop `(565,205)-(765,405)` is square and resampled to 26×26 for the head panel only; the scene crop `(390,210)-(830,1020)` is aspect-preserving at character height 192, rounded to 104×192 and centered on the 128×192 matte. Both are explicitly labeled preview resamples, not source pixel data. Parent review of the 8× head sheet says the inward mark reads as a closed slight smile and is acceptable for user review; this is not exact likeness approval. No further artistic correction is in budget.

The final export differs from the frozen baseline at exactly three composite coordinates: `(67,28)`, `(65,29)`, `(66,29)`, all inside the authorized mask, all recolored to existing palette entry `#744c40`. Alpha and visible-pixel counts are unchanged. Full-canvas native-layer comparisons confirm that only `08-hair-tie-and-hair` changes at those three pixels; the face/neck, eye pixels outside the mask, face outline, body, all other layers, hidden guide, layer metadata and palette are identical. A fresh native reopen exports a byte-identical PNG.

## Automation boundary

Reference crop, seed, and palette preparation were scripted. Agents chose semantic masks and bulk-filled the earlier cleanup; the mouth mask and pixel cluster were chosen by the agent from direct visual inspection, and both mouth edits were applied as native MCP batches. Pixel checks, hashes, and comparison sheets were automated; placement and expression judgments were visual judgments by the parent/model and remain subject to the user's review. The imported/converted seed and these local refinements do not constitute a full redraw of the character.

