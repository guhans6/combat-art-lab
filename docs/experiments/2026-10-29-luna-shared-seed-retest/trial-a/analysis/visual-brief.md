# Trial A visual brief and locks

## Essential identity and silhouette

Preserve the approved character as a natural tall three-quarter standing figure,
turned and gazing right. The defining face read is unequal near/far eyes, a visible
rightward gaze relationship, soft cheek/jaw, and a restrained slightly uneven smile.
The defining hair read is brown tied hair with a pale tie, loose rear volume and a
broken fringe with a few intentional openings. Preserve the long-leg proportion,
relaxed stance, one leg angled outward, hands-in-pockets pose, tote negative space
and continuous shoulder strap.

## Costume and material roles

- olive open hooded jacket framing an off-white shirt;
- high-waisted broad blue jeans with large readable planes;
- pale shoes with restrained panel/lace clusters;
- cream tote and strap;
- warm skin kept distinct from jacket/denim, without baking the scene's orange glow
  into all materials.

Large material planes and silhouette edges take priority over secondary folds, hair
strands, fabric specks and tiny shoe seams. No new weapon, pose, scene or attack is
introduced.

## Pixel and alpha rules

- fixed 128×192 canvas and fixed common framing;
- fixed ordered 255-entry palette from the copied native baseline;
- palette lock on all native draw/recolor operations;
- binary alpha only (`0` or `255`); no blur, smoothing, dither, quantization,
  resampling, crop or palette replacement;
- deliberate staircase contours, selective material-colored dark contours and
  coherent clusters; no blanket speckle removal;
- inspect at 1× and integer nearest-neighbor zoom, with full-body context and a
  readable head crop.

## Protected regions and correction masks

The copied one-layer seed remains the protected baseline. Corrections should be
authored on named overlay layers where the backend permits, so the raw common seed
remains recoverable. The following are bounding review masks, not permission to
paint every pixel inside them:

| Mask | Native bounds (inclusive) | Allowed purpose |
| --- | --- | --- |
| `M-face-expression` | x=54..83, y=19..48 | near/far eye clusters, gaze, cheek/jaw and restrained smile only |
| `M-fringe-tie` | x=39..89, y=2..43 | repair only merged fringe openings, tied-hair crossing or a directly connected silhouette step |
| `M-head-context` | x=38..91, y=0..52 | review/clearance boundary; no broad redraw or hair-mass expansion without an observed defect |

All pixels outside the active mask and all body/costume pixels are protected until
an export review identifies a directly connected defect. If a pass needs body work,
the pass record must name the observed reference defect before any draw call.

## Lighting and context

The approved scene supplies warm urban sunset against cooler distance, but the sprite
must keep material colors readable and separate from scene grading. The supporting
cutout supplies production geometry only. No environment, glow, shadow, or dynamic
light layer is added in this trial.

## Review gates

Identity/expression is a hard gate. A technically valid or more polished candidate
cannot displace a candidate that better preserves the approved face and silhouette.
Record identity, geometry, expression, pixel craft, style/context, native editability
and technical checks independently. User selection and approval remain pending.
