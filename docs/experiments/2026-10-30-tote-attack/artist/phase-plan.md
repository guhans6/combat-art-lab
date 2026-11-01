# Tote attack phase and timing plan — 30 October 2026

## Frozen artist profile

- New 256×192 RGB native sequence; target visible character height ≈180 px. Keep neutral source pixels at original scale, translated +64 px in x.
- One shared palette and the neutral's material/shadow/light roles for every drawing. Keep the approved face, hair silhouette, olive jacket, shirt, denim, shoes, cream tote and continuous straps recognizable. Effects stay out of this art pass.
- Preserve generated sheets as pose evidence. The six-key family candidate scale is 0.4333; the three-key family candidate scale is 0.264. Both remain provisional until the scaled head width/eyeline, pelvis and leg proportions are reviewed against neutral. Register by body/root and foot landmarks. Never fit each pose independently to its outer silhouette or force every lowest pixel to ground.
- Repair the supplied upright middle-recovery drawing in native pixels. Add one preceding arrest-and-redirect drawing that retains the lunge's braking foot, folds both elbows, keeps both hands around one handle bundle, and leaves the flexible tote downstream/low before its return toward the carry-side hip.
- Start and end on the same native neutral idle. Return through re-shoulder and a brief hand-release/settle. This is a playback candidate, not approved final art.
- Main pass plus at most two concrete correction rounds. Every retained pose is native, layered, exported and reviewed at 1× and integer zoom.

## Ordered drawings and provisional durations

Durations are milliseconds. Timing is intentionally quicker through the accelerating strike and longer through anticipation and loaded recovery; playback may motivate one focused timing correction.

| Frame | Phase | Source / construction | Duration |
|---:|---|---|---:|
| 1 | ready idle | Exact neutral source, translated +64 px | 220 |
| 2 | pickup | Six-key draw-to-grip pose; native arm/strap cleanup | 110 |
| 3 | shared grip | Refined two-hand handle bundle, bag pulled clear of shoulder | 140 |
| 4 | counter-wind-up | Additional-sheet leftward wind-up; feet set before drive | 210 |
| 5 | acceleration | Short native transition toward screen-right; pelvis/thorax lead arms | 70 |
| 6 | committed contact | Six-key rightward extension; one contact drawing | 60 |
| 7 | follow-through | Six-key longer extension; planted/lunging base absorbs motion | 90 |
| 8 | arrest and redirect | New key before the supplied weak recovery; bent elbows, continuous grip/handles, tote still downstream and slightly low | 110 |
| 9 | controlled recovery | Repair the supplied upright recovery; torso begins re-centering, hands still control the handles and bag | 140 |
| 10 | tote settle | Shortening curved path toward the carry-side hip; cloth mass lags the hands | 170 |
| 11 | re-shoulder | Supplied final carry pose refined in the shared native palette | 140 |
| 12 | release and settle | Hand returns toward the original pocket/rest pose, with strap supported | 160 |
| 13 | ready idle return | Exact frame-1 neutral drawing | 220 |

Total provisional playback: 1,840 ms. Contact proposal is frame 6 only; parent owns the explicit active interval used by the Godot dummy. `delivery.json` will supply actual coordinates and source frame order after native export. All durations are multiples of 10 ms for exact GIF timing.

## Attachment chain and anchors

`ground/root → pelvis → thorax/shoulders → elbows → wrists/hands → one handle bundle → rim → flexible tote body`.
Hair/jacket hem have small, independently justified follow-through only. Foot contacts and root offsets are measured from each exported pose. Tote bounds, grip point(s), and foot-contact coordinates use the canvas's top-left origin and half-open `xyxy` bounds, with pixel-center points for grip/feet.
