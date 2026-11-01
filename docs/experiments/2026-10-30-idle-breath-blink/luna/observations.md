# Registered references and baseline — before drawing

## Reference inspection

- Visually opened the approved scene and close-up before drawing. The scene anchors the tied brown hair, olive jacket, pale shirt, wide blue denim, cream tote, original standing pose and light. The close-up anchors the same turned face, unequal eyes, swept fringe/tie, faint nose cue and restrained closed smile. Neither image specifies breathing or blink timing.
- The canonical full-body reconstruction is a candidate representation of those references, not an approved production sprite. No styling choice or pose change is inferred from the old 96×216 standing-idle experiment.

## Exact baseline inspection

- Opened `docs/experiments/2026-10-30-expression-strip/luna/passes/luna6-neutral.aseprite` directly in the fresh headless Aseprite session and inspected its actual preview and pixel grid before editing.
- Native metadata: 128×192 RGB; one 100 ms frame; 12 layers; 255 palette entries; no tags. Visible layers, bottom-to-top: `00-shoes`, `01-denim`, `02a-jacket-left`, `02b-jacket-right`, `03-shirt`, `04-tote`, `05-tote-strap`, `06a-left-hand`, `06b-right-hand`, `07-face-and-neck`, `08-hair-tie-and-hair`. The hidden locked `guide-source-seed (hidden)` layer stays hidden and unchanged.
- The head/face and its expression marks are on `08-hair-tie-and-hair`; `07-face-and-neck` is transparent across the eye crop and carries the neck under the head. This was checked by actual layer preview/readback. The face-detail owner and eye locations were registered before freezing the masks.
- Near eye occupies the small native region around x62–66/y20–23; far eye detail is around x70–72/y20–21. The near-eye sclera/pupil are several very high-contrast pixels; the far eye is smaller and partly occluded by the fringe. Its y19 dark pixels are treated as hair/fringe and protected.
- Baseline is a single posed image with the expected fully planted shoes at the lower canvas and no active animation. The torso is split across jacket, shirt, tote/strap, hands and neck cels; the source has no stand-alone upper-body rig group. A 1px whole-cel translation trial exposed transparent coverage/garment gaps, so all such moves were reverted. The face-and-neck cel is full-canvas; native auto-review rejected moving it because it would shift the face, and it remained fixed. The first-pass breath cue is instead a tiny light shirt-fold pixel stepping upward over frames 2–3 and returning at frame 4. That may be too subtle to read as breathing; Sol review is expected to evaluate it.

## Construction hypothesis and uncertainty

- A small chest-cloth highlight shift may imply inhale and release without changing the pose or body volume. Readability is uncertain at 1× and is the leading open issue for independent review.
- A brief, asymmetric half/closed/half eyelid sequence may read at 1×. The far eye's overlap with fringe limits confidence; if closure needs changing fringe or head identity, retain the motion without that edit and record the limitation.

## First-pass outcome

- Blink pixels were drawn only on the registered `08-hair-tie-and-hair` owner. Review comparisons show no changed head-layer pixels outside `[62,20,67,24)` and `[70,20,73,22)`; the three lower-row far-eye pixels temporarily overwritten during construction were restored to exact baseline colors before the final save.
- Frame 1 vs. frames 2 and 3 changes only 2 and 3 composited pixels on the shirt fold. No cels move in the saved loop. The loop keeps the original standing silhouette, body, feet and head positions; the breath cue may not yet communicate motion strongly enough.
- The exact failed cel-translation attempt, rejected operation and all subsequent corrections are logged in [`first-pass-log.md`](operations/first-pass-log.md). The final native document is a review candidate, not approved animation art.

## Correction round 1 outcome

- Sol rejected the first breath cue as too small to read at 1×. Pass01 is a separate native copy; the pass0 native source and exports remain unchanged.
- Pass01 widens the shirt opening one pixel on both sides through staged rows and extends the jacket shoulder edges by one connected pixel. F2/F4 are partial; F3 is fuller; F5–F8 return to rest body shape. This creates a local chest/shoulder change without moving any cel, face/head, denim or shoes.
- Fresh native exports show 11/24/11 changed composite pixels in F2/F3/F4, zero alpha pixels lost and no changes outside the chest/shoulder motion region and eye masks. The previous 2–3 pixel shirt-fold speck was restored to baseline in pass01.
- The existing blink is unchanged; shoes, denim and face-neck are still pixel-identical across frames. Pass01 awaits user review for 1× readability and contour/overlap. See [`correction-round-1.md`](operations/correction-round-1.md) and [`pass01 metrics`](proof/pass01/frame-metrics.json).
- Sol reviewed pass01 read-only and retained it for user review; the parent also confirmed the final GIF timing and loop. No further art/backend change is pending. User visual approval remains open.
