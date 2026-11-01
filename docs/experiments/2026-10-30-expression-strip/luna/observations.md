# Registered references and baseline — before drawing

## Reference roles and visible cues

- `inputs/character-closeup.png` is the approved face, expression and hair authority. It shows the same right-facing three-quarter face, unequal near/far eyes, a small faint nose cue, a shallow closed smile with slightly raised and uneven corners, swept brown fringe, tied rear hair and pale tie. It is a painted reference, not a native pixel map.
- `inputs/character-scene.png` is the approved identity, body, outfit, pose, lighting and full-context authority. The same quiet face remains recognizable at scene scale. It supplies no neutral or surprised reference; those two expressions are new poses of the face, not new identity designs.
- The close-up and scene were opened directly. Review-only crops `reviews/approved-closeup-face-sourcecrop.png` `(520,170)-(820,470)` and `reviews/approved-scene-face-sourcecrop.png` `(460,130)-(820,520)` are crops of the originals, not construction sources. The original source dimensions/crop differ, so raw distances are not mapped as if the references shared a grid.

## Baseline inspection

- The exact native baseline was opened with Aseprite MCP and read before editing: 128×192 RGB, frame 1 at 100 ms, 12 layers, 255 palette entries. It is the pre-mouth-cleanup Luna6 full-body source, not an approved smile variant.
- The actual composited face is owned by `08-hair-tie-and-hair`; `07-face-and-neck` is transparent over the face region. This ownership was confirmed by native-layer ASCII/readback, not inferred from the layer names. All face changes therefore stay on the inherited visible owner without transferring pixels.
- Native/composited readback confirms the baseline is **not blank**: two warm marks exist at `(68,27)` and `(69,27)`. They sit at the registered lower-face mouth height. Their exact original intent is uncertain; I will treat them as the existing lower-face cluster and replace/reuse that cluster inside the mouth mask, never draw a second mouth beneath it.
- Approximate baseline landmarks, zero-based canvas coordinates: near-eye cluster `x62–66, y20–22`; far-eye cluster `x71–72, y19–21`; faint warm nose/cheek cue near `(71,24)`; inherited mouth pair `(68,27)/(69,27)`; lower face/chin skin around `y30`, with underjaw transition at `y31`. These are registration estimates, not exact source correspondences. Eye centers and nose/chin registration are medium confidence; mouth height/close-up mouth shape are higher confidence; exact small-grid curvature remains medium.
- The source close-up registration available from the direct crop and prior landmark notes is approximate: near eye `(655,289)`, far eye `(720,278)`, nose cue `(719,309)`, mouth corners `(675,336)/(707,336)`, mouth low point around `(690,342)`, chin around `(682,374)`. The source face turn differs slightly from the rasterized candidate, so these coordinates guide relative placement only.
- `reviews/baseline-face-coordinate-grid.png` and `reviews/baseline-head-grid-20x.png` show the actual baseline export with a neutral matte for pixel registration. Native RGBA outside an edited variant mask remains protected.

## Per-variant hypothesis and frozen scope

All coordinates are zero-based, half-open rectangles in the 128×192 canvas. Each candidate starts independently from the frozen baseline. Masks are recorded in `masks/` before drawing; the nose cue, fringe/hair boundary, cheek/jaw contour, alpha, body and all other layers are excluded.

| Variant | Hypothesis | Editable mask |
| --- | --- | --- |
| Neutral | A short, level, low-key closed line will read as a relaxed resting mouth while retaining the existing unequal, relaxed eyes and brows. | Mouth `[66,26,71,29)` only. |
| Subtle smile | One connected shallow curve, slightly uneven at the corners and softly weighted in the existing palette, will read as a friendly closed smile without a second mark. | Mouth `[66,26,71,29)` only. |
| Surprise | A small open cluster plus slightly wider eye openings and lifted, restrained brow accents will read as mild surprise while retaining the rightward gaze and unequal eyes. | Brows/eyes `[61,18,74,24)` plus mouth `[66,26,71,29)`. |

Protected registration landmarks: nose cue `(71,24)`; face/hair contour at `x≤60` or `x≥74`; jaw/underjaw from `y30` downward; all hair silhouette/fringe outside the declared interior features. No generic large O, teeth, blush, sweat, symmetry redraw, or pose/body change is planned.

## Review cautions

The baseline export is small; a change that reads only in the 8× crop does not pass. Judge expression at full-body 1× and compare each actual export with both approved source images and the unchanged baseline. The source crop is display-resampled for matched-height review only; no fractional transform is fed back into drawing. The user has rejected the earlier three-pixel mouth attempt, and the separate Sol candidate is still only pending user review, so neither is treated as approved or as the expression template.

## Luna6 first pass — construction and proof

- Three independent copies were made from the frozen baseline and saved as `passes/luna6-neutral.aseprite`, `passes/luna6-subtle-smile.aseprite`, and `passes/luna6-surprise.aseprite`. Each is one frame at 100 ms. The one-pass source of truth, exact colors/coordinates, and MCP operation results are in `operations/luna6-draw-log.json`.
- Neutral replaces both registered warm lower-face pixels with the same muted palette color `#744c40` at `(68,27)` and `(69,27)`, making a short level rest line.
- Subtle smile repaints the old two-pixel cluster, then draws a connected three-pixel shallow curve with `#744c40` at `(68,27)`, `(69,28)`, and `(70,27)`. The resulting baseline→variant diff is four pixels because `(69,27)` returns to the baseline skin tone.
- Surprise lightens the existing near- and far-eye sclera by one palette step at `(64,20)` and `(70,20)`. Its mouth is a warm-edged, vertical 1×2 opening: the warm upper-left edge `(68,27)` already existed in the baseline, while the dark cavity is `(69,27)`/`(69,28)`. No brow stroke was added: the fringe covers the registered brow area, and drawing there would risk changing the hair boundary. Thus brow lift remains a Sol-review opportunity, not a claimed result.
- Every Aseprite `draw` batch targeted only the existing `08-hair-tie-and-hair` cel. Native `read_pixels` confirms the only owner-cel diffs from the exact baseline are 2 pixels for neutral, 4 for subtle smile, and 4 for surprise. The exported composite diffs are the same coordinate sets. All are inside their frozen masks; alpha has zero changed pixels. The exact coordinate/color pairs and masks are recorded in `proof/verification.json` and `masks/`.
- Fresh reopen evidence: each saved native file was closed, reopened from disk, and exported again. Each reopened PNG is byte-identical to its original export. Reopened metadata remains 128×192 RGB, one 100 ms frame, original 12 layer names, and palette identical to baseline. Each 3× PNG is 384×576 and pixel-equal to nearest-neighbor scaling of its 1× export.
- Review sheets: `reviews/fullbody-strip-1x-matte.png`, `reviews/fullbody-strip-3x-matte.png`, and `reviews/head-strip-8x-matte.png` show baseline plus all candidates, composited on `#707070` so hidden transparent RGB cannot glow. `reviews/approved-closeup-vs-heads-8x.png` adds the approved face crop beside the 8× heads. The full approved original is `inputs/character-scene.png`; see also the approved close-up and scene crops in `reviews/`.
- MCP `validate` was not callable in the exposed tool list during this pass. The checks above are fresh native reopen, `sprite_info`, native owner-layer readback, exact exported-pixel diff, scale consistency, and visual preview. No Godot or motion validation was performed.
- Construction is not artistic approval. These are static first-pass comparison candidates only; user selection and Sol's independent review/rescue remain pending.
