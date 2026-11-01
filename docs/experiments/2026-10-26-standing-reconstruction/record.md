# Experiment: faithful editable standing reconstruction

- Date: 26 October 2026
- Status: constructed and locally verified; user visual review pending
- Question: how closely can the agent draw the finalized original character as an editable Aseprite asset?
- Baseline: revision 9e35c5c plus preserved uncommitted reference-study work. Aseprite Lua swatch edits were previously proven; a character reconstruction was not.
- Approved scope: one standing pose of the finalized character, internet drawing study, meaningful native layers, side-by-side fidelity review and a local revision proof. No computer use. No animation or Godot claim.
- Relevant decisions: ADR 0001; finalized original character approval in this conversation; current style guide.
- Tools: existing Aseprite 1.3.18.6-dev at `/Applications/Aseprite.app`; native Lua API; bundled Codex Python/Pillow for reference inspection, preview layout and file checks. No new tool/MCP/skill installed, no image-generation calls, no paid services.

## Plan and research applied

1. Preserve the supplied finalized scene, close-up and isolated character. Inspect dimensions and alpha. The isolated reference includes semi-transparent white fringe/debris; these are not character details.
2. Read artist tutorials before construction: [Saint11 cluster sketching](https://saint11.art/pixel_art_articles/article2/), [shading](https://saint11.art/pixel_art_articles/article4/), [anti-alias/banding](https://saint11.art/pixel_art_articles/article5/), and official Aseprite [Image](https://www.aseprite.org/api/image/) / [Sprite](https://www.aseprite.org/api/sprite/) APIs (accessed 2026-10-26). Written material was inspected; no claim of watching YouTube videos. Additional notes are in [construction principles](../../research/aseprite-reconstruction-principles.md).
3. Choose a provisional 128x192 grid (184px opaque character height). This supports a readable face and long-leg silhouette while keeping a visible pixel treatment. It is not an established native Until Then resolution; the user delegated size selection.
4. Author silhouette polygons, material planes, pixel lines and accents in Lua. Follow large-cluster-first construction, directional plane shading, selective outlines, fewer isolated accents, and separate semantic layers. Aseprite draws these instructions directly. The construction script reads no raster reference and does not import/downsample the character.
5. Compare the first pass with the reference. Preserve it, soften over-heavy denim/hair/olive contrast, correct neckline and fly seam, and reduce the mouth mark. Keep the refined result separate from a test-only tote-color edit.
6. Reopen the native source, inspect/export real layers, perform isolated revision, and regenerate the sprite in a fresh output directory from drawing instructions alone.

## Deliverables

- [Approved scene](../../../assets/references/approved-2026-10-26/character-scene.png), [close-up](../../../assets/references/approved-2026-10-26/character-closeup.png), [cutout](../../../assets/references/approved-2026-10-26/character-cutout.png) preserved unchanged.
- [Main native master](../../../assets/source/standing-v01/standing.aseprite), [drawing source](../../../assets/source/standing-v01/draw.lua), [native inspection/revision source](../../../assets/source/standing-v01/verify-and-revise.lua), [preview/check script](../../../assets/source/standing-v01/preview-and-check.py), and [run instructions](../../../assets/source/standing-v01/README.md).
- [Transparent export](../../../assets/export/standing-v01/standing.png).
- [Side-by-side comparison](../../../assets/previews/standing-v01/comparison.png), [actual-size comparison](../../../assets/previews/standing-v01/at-size.png), [face detail](../../../assets/previews/standing-v01/face-comparison.png), [actual source layers](../../../assets/previews/standing-v01/source-layers.png), [local edit proof](../../../assets/previews/standing-v01/revision-proof.png).
- First-pass native/script/PNG retained alongside final candidate for history. Tote revision test is a separate variant; cream tote remains in main source.
- [Native source checks](source-checks.json) and [export checks with exact artifact hashes](export-checks.json).

## Observed evidence

| Check | Target / method | Result |
| --- | --- | --- |
| Native construction | Actual Aseprite batch Lua, main master | Saved, reopened with 12 named layers, one frame and `standing-study` tag |
| Transparency | Actual exported pixels | Alpha is exactly 0 or 255; no white cutout fringe/debris imported |
| Export dimensions | Main PNG and native header | 128x192; opaque bounds (32,2) through (103,185); 45 visible opaque colors |
| Native reopen | Fresh Aseprite export after opening saved file | Decoded image bytes identical to original export |
| Fresh construction | Re-run draw.lua into ignored `.scratch/reconstruction/rebuild`, compare PNG | Exact PNG bytes reproduced; construction source contains no raster-reference load |
| Local revision | Reopen source, change base/light colors of `02-tote-body`, save/reopen separate native | 223 source pixels changed; all other 11 layer images identical. Composite changes 171 visible pixels, all inside tote layer; main master remains cream |
| Silhouette | Common-grid reference mask comparison after alpha/debris cleanup, no alignment optimization | IoU 0.9024. Shape-overlap diagnostic only: not a likeness percentage, face/style/color score or user approval |
| Visual fidelity | Inspected enlarged full-body, face and 1x preview | Recognizable clothing, pose and silhouette. Face/profile and hair mass differ; folds/seams/shoe details simplified and more geometric. Not exact |
| Gameplay scale | PNG viewed at 1x and integer enlargements | Static file review only; actual Godot camera and on-screen scale untested |
| Godot / motion | Not in current standing scope | Not run; no animation or timing proof |

## User feedback and next action

Original design is finalized; reconstruction v01 has no approval yet. Present the actual comparison rather than assigning a subjective similarity percentage. The next owner is the user for concrete likeness feedback, then the agent for focused corrections. Do not expand into attack assets before the user accepts this standing direction.

No commit, push, or remote asset publication was performed. Existing local reference-study changes were preserved. No repository-wide Definition of Done is implied; the completed boundary is one editable standing construction plus export/revision evidence.
