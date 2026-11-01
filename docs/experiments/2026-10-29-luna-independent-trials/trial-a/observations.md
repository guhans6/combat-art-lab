# Trial A observations

## Frozen configuration

- Requested model: `gpt-5.6-luna`
- Requested reasoning effort: `max`
- Provider compute/cost: unobserved; do not infer from the request
- Construction mode: assisted reconstruction, converted seed plus authored native cleanup
- Target: one static full-body sprite on a 128x192 transparent canvas
- Framing: preserve the whole 1024x1536 source frame at exactly 1:8 scale; do not crop or trim
- Pass budget: three artifact passes maximum (initial plus two corrections)
- Editor-call budget: 120 Aseprite/editor calls maximum across the trial
- Animation/runtime scope: out of scope for this trial

## Equal inputs and frozen hashes

| Role | Original path | SHA-256 |
| --- | --- | --- |
| Production source | `docs/experiments/2026-10-29-clean-cutout-conversion/inputs/clean-generated-cutout-v1.png` | `12e971cc9e3cbfa7add2a17a62ff53d1f45b3c55197ce23c336a6447bed1f49e` |
| Identity/style scene | `assets/references/approved-2026-10-26/character-scene.png` | `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae` |
| Identity/expression close-up | `assets/references/approved-2026-10-26/character-closeup.png` | `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7` |

The three originals were copied unchanged into `input/` for this trial. The
production source is 1024x1536 RGBA; both supporting references are 1448x1086
RGBA. The source and supporting files were inspected visually before drawing.

## Visual brief

### Identity and structure to preserve

- Tall, natural full-body proportions with long wide-leg silhouette and relaxed stance.
- Three-quarter front view, head turned to the character's right, gaze also rightward.
- Brown tied-back hair with a pale tie, overlapping rear mass, broken fringe openings,
  and a few loose silhouette strands.
- Unequal near/far eye clusters, soft cheek/jaw, small nose indication, and a
  restrained slightly uneven smile that remains readable at native size.
- Olive open hooded jacket around an off-white shirt, broad blue jeans, cream tote
  with a continuous shoulder strap, and pale sneakers.
- Hands remain tucked into the jacket/jeans pockets; one leg angles outward.

### Secondary details that may simplify

Reduce tiny hair strands, blush texture, seam/fold count, sneaker stitching, and
small fabric specks before reducing any feature that changes the face turn,
expression, hair silhouette, clothing silhouette, or tote attachment.

### Rendering and palette rules

- Preserve source material relationships while removing any environmental glow from
  the transparent sprite; the scene's warm/cool lighting is not a fixed full-body tint.
- Use deliberate opaque pixel clusters, selective material-colored contours, and
  broad planes before detail. Avoid blur, interpolation, random texture, and blanket
  speckle removal.
- Start from source-derived colors after nearest-neighbor reduction. Add or merge
  colors only for a named readability problem; no fixed color-count target is imposed.
- Keep intentional transparency between the legs and in hair openings. Check alpha on
  both light and saturated contrasting backgrounds before accepting a pass.

## Source inspection notes

The production cutout presents the complete character centered vertically in a
transparent frame. It has a deliberately pixel-stepped dark contour and broad,
readable material planes already present in the source. At full view the face is
small but clearly turned right with a quiet smile; the tied brown hair, olive jacket,
white shirt, blue trousers, cream tote, and pale shoes are all distinct. The outer
frame shows no intended scene objects; transparent display was checked by compositing
the prepared seed on white and magenta backgrounds.

The approved scene confirms the long-leg silhouette, relaxed hands-in-pockets pose,
cream tote placement, and warm urban context. The close-up is the authority for the
face/hair hierarchy: rightward three-quarter turn, broken fringe, tied rear hair,
unequal eyes/rightward gaze, warm skin, and restrained asymmetric smile. The sprite
will retain neutral material colors rather than baking the scene's orange/blue glow.

## Provisional feature budget at 128x192

This is a working hypothesis, not a quality threshold. The seed keeps the source
framing, so the head is approximately 28-32 pixels wide at native size. Reserve a
coherent face plane within that envelope: near eye about 3-4 pixels across, far eye
about 2-3 pixels, a one-pixel nose/cheek indication, and a 2-3 pixel smile cluster.
Keep fringe openings and the hair-tie silhouette larger than isolated strand texture.
The broad jacket, shirt, denim, tote, and shoe masses should read without seams.

## Preparation and editor status

- Local source copies and hashes: complete.
- Deterministic seed recipe: complete in `scripts/prepare_seed.sh`.
- 128x192 nearest-neighbor RGBA seed: `work/converted-seed.png` (SHA-256
  `639cddf273ab9cded6db8d03ad93b2de28133497063c4fe2b960ce1beb6958fa`).
- Alpha-clean seed: `work/seed-alpha-clean.png` (SHA-256
  `1a02835a48ba3078c792d8047c0e6dc83f9cce2c45bed18fb40b5eba46354d52`). A
  reviewed threshold of 16 removed low-alpha halo samples and retained 7,844
  opaque visible pixels in bbox x32..103/y2..184 (72x183).
- Aseprite/editor calls: 116 supervisor-tracked observable calls; four remain in
  the fixed budget. Pass 02 and its proof artifacts are saved; the slot is released
  for defect-only review.
- Production state at release: reopened `passes/pass-02.aseprite` remains open,
  source-derived palette snapped to 254 visible colors, hidden locked source
  reference, corrected face overlay, and clipped raster regions for hair/face,
  jacket/shirt, jeans, and tote/shoes. `passes/pass-02.png` is the corrected
  transparent artifact; `pass-02-reopen.png` is byte-identical.
- Evidence limit: the candidate alpha bbox measures x32..103/y2..184, but the
  supervisor found a material omission/disagreement between the white and magenta
  comparison presentations. Full coverage and visual equivalence are not claimed.
- Pillow-based checks: unavailable in this environment (`PIL` is not installed);
  editor-native inspection and available ffprobe/sips checks will be recorded instead.
- No prior converted seeds, corrections, trial outputs, ledgers, or artistic scripts
  were inspected.
