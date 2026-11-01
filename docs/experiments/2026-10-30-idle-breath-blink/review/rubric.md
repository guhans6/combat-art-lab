# Independent idle review criteria

Reviewer: Sol, review only. User instruction overrides the older workflow's critic-rescue allowance: the reviewer makes no artwork, native-source, construction, or configuration changes. Initial review plus at most two correction reviews; Luna owns corrections. User approval remains pending.

## Frozen inputs and observations

Identity/style authority: `assets/references/approved-2026-10-26/character-scene.png` and `character-closeup.png`, opened directly. The originals show a rightward three-quarter face with unequal near/far eyes, warm skin, broken brown fringe/tied hair, restrained expression, relaxed pocketed hands, olive jacket, wide blue jeans, cream tote/continuous strap and pale planted shoes. Their static poses do not prescribe exact blink timing.

Motion baseline: `docs/experiments/2026-10-30-expression-strip/luna/passes/luna6-neutral.aseprite` and matching PNG, opened directly at 1x and nearest-neighbor 3x full body / 12x head. This is the task-selected neutral source, not a new claim of user approval. The sprite is quieter-mouthed than the concept and must retain that neutral expression during this idle.

Independent native decode matches its PNG exactly: 128×192, 12 layers, 7,844 opaque pixels, visible alpha bounds `[32,2,104,185)`. Exact metadata and hashes are in `baseline-native.json`. The existing native reader rejects linked cels; a candidate using them needs a documented read-only decoder extension rather than a guessed pass. Nominal layer names are not semantic proof: existing hair ownership includes facial marks, so review actual visible pixels and relative overlaps.

## Gates

1. **Motion and timing:** review the delivered timed loop and all actual frames. Breath is gentle, with coherent torso/shoulder/neck relationships, rather than rigid whole-character translation. Feet/root stay planted. The open neutral state occupies most of the loop; closure is brief and intentional. Timing, repeats and loop seam are checked from actual native durations and GIF delays, not labels or declared intent.
2. **Identity/expression:** eye direction, near/far relationship, brow/mouth, fringe, head volume and facial angle remain stable except intended eyelid closure. Blink reads as a blink, not a glance, new emotion, face shrink or sliding pupil. Review feature crops, whole heads and full body at native size and integer zoom.
3. **Body/coverage:** no unpainted gaps at neck/collar, jacket/tee, waistband, hands or tote strap after part motion. No limb/body volume snapping, unrelated-pixel travel, contour tears, isolated edge sparkle or silhouette wobble. Distinguish existing intentional hair openings and leg negative space from newly exposed interior alpha.
4. **Native/export correctness:** inspect actual canvas, layer order/names/flags/opacity/blend, cels and positions, frame order/durations, palette and tags. Recompose each native frame independently and compare actual exports; inspect all frames, coverage, ground area and protected content. Evaluate save/reopen and local-edit proof separately when supplied. Original input hashes stay unchanged.
5. **Evidence boundary:** technical checks, visual observation, artistic judgment and user approval are separate. Static sheets establish pose/cluster consistency; decoded timing establishes stored duration/order. If the available viewer exposes only the first GIF frame, do not claim actual-speed motion was watched. Record that limitation unless a permitted local playback surface is available. No Godot or gameplay claim without an actual engine run.

## Feedback and disposition

Report only concrete prioritized defects to Luna, without replacement pixels, patch scripts or spoon-fed drawing instructions. Each review names exact candidate paths/hashes, pass/reject/uncertain per native and visual boundary, best retained checkpoint and next owner. At budget exhaustion, preserve evidence and report unresolved gaps; the reviewer does not repair the artwork.

Read workflow references: root AGENTS/context/glossary/handoff; ADR 0001; art-production workflow including current role rules and review rubric; style, motion and asset guides; validated-checkpoints delivery reference (no separate Definition of Done); pixel-art-director skill and craft animation, face-likeness, alpha-coverage and setup references. No editor backend operation or version probe was performed by this reviewer.
