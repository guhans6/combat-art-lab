# First correction review — suitable for user playback review

Reviewed native SHA-256 `d5b9d7675de8bea50a1941361d3e3bed3c187b3ee7e1d7e0585d51f8d37cc8ed`, `luna/passes/pass01/luna6-idle-breath-blink-pass01.aseprite`; all eight original/reopened PNG exports and the actual timed 4× GIF. Independent native compositions were visually inspected at 1× full body, 8× head and 4× torso, plus a 10× torso diagnostic and changed-pixel map. The actual-speed perceptual boundary remains unobserved on this still-image surface.

## Defect-only feedback

No further blocking defect established by the reviewed native frames and exports. Do not spend the remaining correction round solely to increase changed-pixel count.

The first review's shirt-speck defect is addressed: the chest opening and both jacket shoulder contours now expand together, then return through the same intermediate state. This is spatially coherent lateral torso expansion, with a still head and planted lower body. It is a very restrained cue at native size; this review does not certify that its amplitude/rhythm feels sufficient in playback. The 1× strip can support consistency and lack of broad bobbing, not a claim that a played breath was watched.

## Gate status and evidence

- **Native/export: pass.** Same 128×192 canvas, 12 layer metadata records and exact palette chunk as neutral. All eight recomposed native frames equal original PNGs and fresh-reopen PNGs. Actual GIF's eight frames equal exact nearest-neighbor 4× native output, including uniform pixel blocks, and retain native durations `600/350/550/600/50/80/50/250 ms` (2530 ms, infinite loop).
- **Breathing pose construction: pass, narrowly.** Breath frames 2/3/4 have 11/24/11 changed composite pixels, involving both outer jacket contours and internal shirt opening. Expansion is one native pixel at the affected contours, then restores; no whole-character translation. No fragmented/disconnected contour addition or newly opened joint/strap gap was observed. First/last frames still equal neutral.
- **Identity, anchors and introduced coverage: pass.** All head/face/neck pixels during breathing equal neutral. Blink frames are exactly the initial reviewed blink. Shoes, denim, hands, tote/strap and lower body remain fixed. Every frame stays binary alpha; no opaque pixel is removed. Breath adds 4/9/4 boundary pixels, with the exact baseline enclosed-hole list unchanged in every frame. This does not repair or approve inherited still-image holes. Neutral native/PNG hashes remain unchanged.
- **Blink construction: pass.** Same brief 50/80/50 ms partial/closed sequence; 92.9% of loop fully open. No new eye/expression/head-volume defect observed across actual native frames.
- **Perceived motion at actual speed: uncertain.** User must view the delivered GIF to judge whether the extremely subtle breathing and blink cadence feel natural. Reviewer did not watch timed playback or run Godot, and no runtime/gameplay or final artistic approval is claimed. No independent local-edit proof was executed by this read-only reviewer.

Decision: pass01 is the best reviewed motion-study candidate for user playback review. Initial attempt remains rejected evidence. No second corrective pass is required by current defects; one round remains if user-visible playback reveals a concrete problem within scope. Parent owns delivery/evidence wording; user owns artistic acceptance. Reviewer modified only review artifacts and scripts, with no artwork/native/backend/config changes.
