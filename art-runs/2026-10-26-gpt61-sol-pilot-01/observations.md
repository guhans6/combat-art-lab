# Pre-edit observations

Viewed both complete primary references, the complete native 128x192 baseline, MCP head preview at 12x, and primary head crops. The cutout is supporting only. Measurements below are approximate reference landmarks, not source pixel ground truth.

## Landmarks and interpretation

Close-up crop origin (385,105), extent 415x305. Hair top approximately (170,25), rear extent (10,130), chin approximately (300,270), near eye center (267,180), far eye center (335,160), mouth center (305,234), ear center (188,210). Confidence medium: generated image edges and lighting complicate single-pixel placement. Scene broadly corroborates the orientation/expression but has a more pronounced smile and different fringe accents.

Native baseline: hair spans approximately x35..78/y2..30; face x56..73/y16..30. Historical pupils (64,21) and (70,21) confirmed by native/source inspection; eye centers are retained, not assumed optimal. Mouth occupies x67..69/y26..27. Ear around x55/y23..25. Neck notch x57..65/y29..30 is protected.

- Face orientation: both references show a rightward three-quarter head with a tapered cheek and near/far eye difference. Baseline broadly supports this; medium confidence. No evidence warrants moving the eyes closer or rotating the entire head. Keep geometry initially.
- Expression: reference has a shallow, quiet smile with a wider horizontal span; baseline's three diagonal orange marks read as a tiny pursed/comma mouth. High confidence. Small test: reshape the mouth into a shallow five-pixel smile with restrained existing skin-contour colors. Expected: closer restrained, mildly amused expression without changing nose or jaw.
- Eyes: baseline pupils lose vertical continuity and the far eye has a pale block below it. Reference has tall dark irises and clear upper lids. Medium-high confidence. Small test in the same expression pass: retain eye centers and whites, extend near/far iris columns down one pixel using existing dark brown/ink. Expected: more coherent rightward gaze without enlarging whites or frontalizing the face.
- Hair: baseline ponytail/bun reads as a broad rounded disk, with many bright zigzag bands across the crown. References show more overlapping clumps, less uniformly bright striping, and hanging wisps. High confidence on broad masses, medium on exact small strand mapping. Defer until expression pass inspection; no whole-head redraw.
- Cheek/chin: baseline is somewhat pointed; close-up chin is flatter. Medium confidence because its neck joins a different crop/scale. Defer changes near neck; scope must not expand.

## First change hypothesis

A very small expression patch, preserving eye centers and all hair/face silhouette, can reduce the startled/pursed reading. Read exact feature-layer grid (MCP 038) before writing. Use selection x60..71/y19..28, frame 1, layer 11-face-features only. All coordinates are inside profile mask. Do not alter neck or body.

Budget remains maximum 3 visual passes / 80 trial MCP calls. Setup calls 001..033 are separate. Trial begins at 034. No extra critic, subagent, image generator or human drawing intervention.

## Pass review and stop decision

Pass 01: MCP 040..046. Viewed full native-size sprite and 12x head. Six visible pixels changed on the feature layer; the mouth is a wider shallow smile, far iris has a continuous dark column. The near-iris point (64,23) was already the requested brown and produced no change. Centers and head geometry remain fixed. Existing dark corner color makes the smile rather square at 12x; this is a remaining simplification, not exact reference likeness. Palette lock reported a snap for the RGB part of a fully transparent pixel; read_pixels 049 and native parsing confirm its alpha stayed zero. Prefer tested grid/clear erasure in future instead of an RGBA pixels point for clarity.

Pass 02: MCP 047..056. Read exact back-hair grid, then removed a small outer/underside cluster and restored its dark contour. 26 native hair pixels changed; total 32 composite pixels from baseline, 16 silhouette pixels removed. Both independent checks pass. Viewed native size and 12x. The round rear mass is slightly reduced, but its lower opening reads as an angular bite and the left contour now projects a horizontal ledge. This is not convincing enough against the reference's curled clumps. Retain as a rejected alternative; select pass 01 for the delivered working candidate. No hidden third attempt.

Stop after 2/3 visual passes. A more substantial hair/cheek redesign needs better landmark mapping at this grid and could compromise the existing recognizable design; no further confident small patch is justified in this pilot. Remaining discrepancies: round rear hair, bright crown bands, pointed chin, simplified near-eye shape, and square smile corners. Human likeness review is pending. No human score assigned by the model.
