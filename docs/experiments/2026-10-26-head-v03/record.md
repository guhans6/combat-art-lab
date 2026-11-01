# Experiment: v03 identity correction, head only

- Date: 26 October 2026
- Status: v03 constructed and locally verified; user visual review pending
- Request: compare original isolated reference with v01/v02; correct only head, face, ears, bangs and hair. Preserve neck, shoulders, clothing, body, pose, tote and all previous versions. Native resolution/palette retained; no smoothing, blur, image-generation or computer use.
- Baseline: preserved v01 and v02 native files/exports; [baseline file hashes](baseline-hashes.json) captured before edits. The selected base is v02: its jaw is less elongated than v01, while its eye spacing/far-eye visibility and hair shape still need correction.
- Applicable guidance: current style guide, asset contract, ADR 0001 and validated-checkpoint protocol. No separate repository-wide Definition of Done exists.

## Comparison and plan

Crop each head using the same character coordinates: native x32..79, y0..31; original x256..639, y0..255. The original has eight times the pixel dimensions, so the original crop and native crops can be displayed at equivalent head sizes. Original reference pixels are not copied into the sprite. Any nearest-neighbor scaling is confined to explicitly labeled comparison previews.

The near/far dark pupil positions in v02 are x63/x71 (8px separation). v03 places them at x64/x70 (6px separation), both at y21 and toward the right edge of their respective eye clusters. The near eye retains the larger light area; the far eye is narrower/dimmer, with fewer dark iris pixels. Both have distinct whites and an intentionally uneven brow/lid contour. These coordinates describe the authored sprite, not measurements proving identical reference anatomy.

The other corrections are a fuller cheek-to-chin transition, understated nose cue, offset small smile, partial ear/hair overlap, uneven bang openings, and three overlapping tied-hair clumps with limited loose tips. Preserve overall head bounds and the pale hair tie; avoid extra highlights and fine-hair noise.

## Editing boundary

The [native editing script](../../../assets/source/standing-v03/edit-head.lua) opens the saved v02 master and edits four existing cels only: hair-back, skin-face, hair-front and face-features. It reads no reference raster.

Every draw operation is clipped to x34..79, y2..30, excluding a conservative neck notch x57..65 for y29 and later. Everything at y31 and below is locked, including the existing lower hair tips that meet the collar. Each edited layer also preserves all pixels outside this mask. This is deliberately stricter than simply restricting changes to a rectangular head crop.

Eight other layers remain unchanged. No global palette or body-color modification is performed. Native canvas remains 128x192 with the existing ground anchor and 12 named layers.

## Artifacts

- [Original / v01 / v02 starting comparison](../../../assets/previews/standing-v03/starting-head-comparison.png).
- [Original / v02 / v03 head comparison](../../../assets/previews/standing-v03/head-before-after.png).
- [All four heads](../../../assets/previews/standing-v03/all-heads-comparison.png), [large lossless comparison](../../../assets/previews/standing-v03/all-heads-comparison-16x.png), [native-size heads](../../../assets/previews/standing-v03/native-heads.png).
- [Native v03 master](../../../assets/source/standing-v03/standing.aseprite), [transparent export](../../../assets/export/standing-v03/standing.png), [script/run instructions](../../../assets/source/standing-v03/README.md).
- [Full-body scope comparison](../../../assets/previews/standing-v03/full-body-scope-comparison.png), [difference map](../../../assets/previews/standing-v03/head-only-difference.png), [editable-mask image](../../../assets/previews/standing-v03/editable-head-mask.png).
- [Native checks](source-checks.json), [independent export/scope/palette checks and artifact hashes](checks.json).

An earlier v03 head pass is preserved as `standing-head-pass01`; its far-eye dark cluster was reduced in the final candidate and the nose/smile marks were separated. Main deliverable is `standing.aseprite`.

## Observed verification

| Check | Evidence |
| --- | --- |
| v01/v02 preserved | Exact native and PNG hashes match the recorded baselines |
| Head-only composite changes | 369 changed pixels; zero outside the head mask |
| Neck/body preserved | Protected notch and all rows y31..191 are pixel-identical to v02, per layer and composite |
| Other layer preservation | Tote body, jeans, shoes, tee, jacket, hands, strap, guide each have zero changed pixels |
| Palette | 51 visible opaque colors; no color added relative to v02 |
| Native file | Saved/reopened by installed Aseprite, 12 layers / 1 frame / 128x192; reopened export identical |
| Eye placement | Verified separate pupil positions x64/x70 plus separate light clusters; both eyes distinguishable in visual native-size inspection |
| Preview quality | Original and sprites displayed at equivalent sizes; sprite enlargement uses nearest-neighbor only |
| Visual limits | Head identity remains an interpretation at 48x32 crop scale. Hair and expression are simplified; no exact match or user approval inferred |
| Engine / publication | No Godot playback, animation, commit or push |

Official [Cel](https://www.aseprite.org/api/cel/) and [Image](https://www.aseprite.org/api/image/) docs were rechecked for native cel replacement and coordinate handling on 26 October 2026. Existing artist-study principles were reused; no new integration or paid service was needed.

## Next action

User reviews v03 likeness against the original, primarily eyes, expression and hair. Agent makes any subsequent requested corrections inside the same head-only boundary. Neck/body remain locked unless the user changes scope explicitly. Keep v01, v02 and v03 as separate candidates.
