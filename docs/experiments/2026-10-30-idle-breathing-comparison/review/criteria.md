# Independent review criteria and prior-pass reassessment

Reviewer role: Sol, review only. No artwork/editor/backend changes. 30 October 2026.

## Authoritative starting point

The user rejects the prior idle's barely visible breathing and reports a visual impression of removed pixels. This overrides the earlier agent's narrowly positive visual assessment. Native baseline is `../2026-10-30-idle-breath-blink/luna/passes/pass01/luna6-idle-breath-blink-pass01.aseprite`, SHA-256 `d5b9d7675de8bea50a1941361d3e3bed3c187b3ee7e1d7e0585d51f8d37cc8ed`. Both new candidates must continue independently from that same animation, preserving the established face/blink, denim, feet and timing scope.

## Why the earlier technical pass was insufficient

The previous review's “breathing pose construction: pass” overstates what the actual frames show. At 1x the torso is effectively rigid. Enlarged views show most peak differences concentrated on short outer-shoulder tabs and narrow shirt-opening edges; the large chest plane, neckline, folds and jacket mass remain stationary. The additions connect spatially to the body but do not demonstrate coordinated expansion of a continuous form.

Zero alpha loss means baseline opaque samples remained occupied. It says nothing about how an added contour disappears on return, whether a recolored pixel reads as an erased plane, whether contour/fold motion agrees, or whether an observer perceives a breath. In this pass, small additions can read as local edge flicker or pixel popping; cream/olive boundary recoloring can read as subtraction even with opaque backing. A mathematically intact silhouette therefore does not contradict the user's perception.

The prior native/coverage/export checks remain factual evidence about preservation. They must not be reused as evidence that this breathing looks convincing. Retain prior pass as the shared starting artifact and rejected visual evidence, not an approved breathing result.

## Gates for each independent candidate

1. **Visible motion and form:** inspect every actual native-composed frame at 1x full body and 3x torso/full context. The inhale must visibly change a coherent torso/shoulder form rather than isolated contour tabs or moving shade specks. Shoulder, chest opening, relevant material planes and returns should agree. Do not select by changed-pixel count.
2. **Continuity and volume:** compare neutral, intermediate, peak and return. No isolated fragments, one-frame notches, material-line flicker, joint/strap gaps, unbacked holes, or apparent loss of body/fabric mass. Preserve sufficient overlap/backing and protected details. Alpha metrics are supporting evidence, not the verdict.
3. **Protected identity and anchors:** fixed face/head outside the existing blink, same blink states/sequence and seam, fixed denim/shoes/root, protected hands/tote where locked. Verify native layer pixels, not just flattened PNGs.
4. **Native/export facts:** 128x192, eight native frames; inspect layer/order/visibility/opacity/blend, palette, cel metadata, frame durations, alpha coverage and original hashes. Compose each actual native frame independently; compare all PNGs and reported fresh-reopen outputs. Check GIF count, loop and durations against the native timing and actual frames at nearest integer scale.
5. **Evidence limits:** still-frame inspection can establish pose/construction defects and timing metadata. It cannot certify actual-speed rhythm, sufficient perceptual amplitude during playback, Godot behavior or user artistic acceptance. User plays GIF. No watched-playback or gameplay claim.

## Feedback and budget

Issue concise blocking defects to the originating drawer only. No replacement coordinates, recipes or sharing the other drawer's solution. Each drawer owns its own corrections, maximum two rounds per candidate. Sol never changes artwork. Report pass, reject or uncertain separately for technical facts, visual construction and unobserved playback. If the bounded budget does not yield a convincing reviewed form, retain evidence and report no selected result.
