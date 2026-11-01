# Initial review — breathing gate rejected

Reviewed native SHA-256 `79c4ebc3df6f2d0c6d621d4c68329e075a10a8def7a9649463b312105d55221e`, `luna/passes/luna6-idle-breath-blink.aseprite`; actual original/reopened frame exports; actual 4× transparent timed GIF. All eight independently recomposed native frames were inspected at 1× full body, 8× head and 4× torso on light matte; eyelid states also inspected at 20×. The rubric's original/neutral views were retained. GIF was decoded frame by frame; actual-speed playback was not watched on this still-image surface.

## Defect-only feedback

- **P1 — Requested breathing is absent as readable body motion.** The only breath-state differences are two or three pixels in one shirt highlight while torso contour, shoulders, neckline, head and jacket stay entirely frozen. At native/full-body scale this does not establish an inhale/exhale; enlarged, it reads as a traveling shading speck. The requested loop is breathing plus blinking, so this candidate fails the breathing gate. Correct with a visibly coherent, still restrained breath while retaining planted feet, identity and continuous overlaps. This is a motion defect, not a request to redesign the still or add broad bobbing.

## Independent evidence and limits

- Native/export boundary **passes**: 128×192, 12 layer metadata records identical to neutral; unchanged palette chunk; all eight independently recomposed native frames match their PNG and fresh-reopen PNG. Stored native and GIF durations match `600/350/550/600/50/80/50/250 ms`, total 2530 ms, GIF infinite loop. GIF decodes as exact nearest-neighbor 4× native pixels after ignoring irrelevant RGB under alpha zero.
- Protection/coverage **passes for introduced changes**: first/last frames equal neutral; zero loop-seam pixel difference; denim, shoes and lower body unchanged; every frame's entire alpha channel equals baseline and stays binary. Original neutral native/PNG hashes remain unchanged. The baseline already contains enclosed transparent samples, including a one-pixel inner-denim sample; this review establishes no newly exposed hole, not that the inherited still has no holes at all.
- Blink frame construction **passes**: open neutral face occupies 2350/2530 ms (92.9%); partial/closed states last 50/80/50 ms. Eye closure is readable at 1×, with no observed mouth, eyebrow, fringe, head-volume or gaze drift outside the intended eye change. The near/far lids are simple/graphic but no additional material defect is established by these stills.
- Perceived blink rhythm and breathing rhythm **uncertain** pending actual-speed user playback. Save/reopen pixel proof is observed; no independent native local-edit test was performed by this review-only agent. No Godot/runtime/gameplay claim or user visual approval.

Decision: no selected breathing/blink result yet; retain exact neutral as baseline and the reviewed candidate as rejected initial evidence. Next owner: Luna, first correction round; parent orchestrates. Two correction reviews remain. Reviewer made only review evidence/scripts and no artwork/native/config/backend changes.
