# Coherent idle correction — 30 October 2026

Status: constructed and locally verified; **candidate awaiting user visual review**.
No production idle is artistically approved. Existing work and all four original
experiments are preserved. This bounded implementation follows the user's current
seven completion criteria; no separate repository-wide Definition of Done exists.

## Outcome and artifact

Review [the looping comparison](review/index.html), [3x side-by-side GIF](review/comparison-3x.gif)
(original Sol left, coherent v02 right), [native-size actual-speed GIF](exports/idle-1x.gif),
[3x nearest-neighbor GIF](exports/idle-3x.gif), and [duration contact sheet](review/contact-2x.png).
Native: [source/coherent-idle-v02.aseprite](source/coherent-idle-v02.aseprite), SHA256
`b5051489af54beef68b9dd4176d1cddb4fc990dfed4054de278416f06f0e6b40`.
Twelve semantic layers, eight 128x192 native frames, 3380ms, forward looping tag
`idle-coherent`. No new palette, expression, character redesign or animation system.

## Local inspection and diagnosis

The actual local workspace was used; Code-MCP was not used. Read AGENTS/context/
glossary/handoff/domain/checkpoints/ADR0001, art-production/style/motion/asset docs,
the director's setup/animation/alpha procedures and the four-model records/scripts.
The published motion guide preceded the latest four-model work; the handoff and
local files supplied the current baseline. Dirty Git work was present before this
request; none was reset, committed or published. [Frozen plan](plan.md),
[original torso poses](evidence/torso-originals-4x.png), [native pose audit](evidence/pose-audit.json).

- Sol6.1: anatomical-region copy plus lower-boundary overlap reconstruction;
  hand/pocket/feet fixed. F3 holds raised shoulders/collar against a rest-position
  head/neck for120ms. F6 repeats that mismatch for160ms. Two isolated shirt-fold
  pixels fade180ms before structural motion and remain altered240ms after it.
  Its restrained amplitude and3380ms period are useful, but primary attachments
  are deliberately staggered without an articulated intermediate neck pose.
- Luna5.6Max: whole upper-body/hand cel translation, delayed tote/strap, then a
  sideways tote step. More evident connected upper movement is useful direction;
  moving pocketed hands and the1px lateral bag motion are not copied. Its later
  backing repair restores coverage but does not make that motion anatomical.
- Terra5.6: jacket/shirt/hands/face-neck move F3–6, hair (which owns most of the
  skull/face) follows F4–6, strap only F4–5. Its740ms cycle compounds the discrete
  positional changes. Alpha backing repairs vacancies, not timing relationships.
- Luna6Max: mostly shirt-fold changes with fixed anatomy and independent source
  blink. The crease is animated, but that alone is weak evidence of breathing
  volume. It is not the same head/neck disconnection as Sol/Terra.

Existing comparison routines and fresh decoded checks establish faithful native/GIF
pixels and timing; no common export-speed defect explains the four authored recipes.
Ownership crosses layer names, so layer-by-layer animation is not an anatomical plan.
The backend's installed `skills/animate/SKILL.md` suggests shoulders one frame later;
`rules/41-idle-and-breathing.md` suggests head last, delayed contents and lateral drift.
These generic prescriptions are a workflow hazard when applied to attached anatomy;
this does not prove exactly which text each earlier artist read or followed.

## Construction and motion plan

Sol is the initial visual baseline, not a newly approved static source. Both approved
concept originals were opened before drawing. [Reference/Sol/candidate review](review/reference-sol-candidate.png)
retains the costume, tied-hair silhouette, right-facing shallow expression and broad
material relationships. The task is motion coherence, not a fresh likeness study.

[Frame table and motion hierarchy](plan.md#frame-and-timing-plan-native-128x192-zero-root-travel)
cover every requested part. One thorax driver selects rest or Sol's repaired inhale
key: head/neck/collar/shoulders/upper sleeves rise together by at most1px. The lower
sleeve, wrist/pocket, waist and legs remain anchored; this is not identical whole-body
translation. The upper strap takes up slack with its shoulder; lower attachment and
tote body remain fixed. Tied hair follows the skull. No unsupported free hair/bag
oscillation or extra blink was added.

The only secondary response is an existing muted lower-rib crease tip extending1px,
180ms after the core rises, and relaxing before the core returns. It stays connected
to the source fold and retains its material/shadow role. This is an authored cloth
tension cue, not measured physiology. The final/first drawing is exact rest.

All native construction/save/export used dedicated Aseprite MCP, headless,
Aseprite1.3.18.6-dev/Pebbly0.8.2. Agent: primary Codex session, not a new four-model
benchmark. No model-specific artistic performance comparison is claimed.
[source/prepare.py](source/prepare.py) reads the frozen Sol native and emits literal
MCP grids in [operations.json](source/operations.json); it never writes sprite artwork.
Apply those15 per-cel draw patches to a new Sol copy, create the idle-coherent tag,
save and export the horizontal untrimmed sheet. Existing palette is locked.
The initial actual native calls/results are retained in `source/mcp-v01-log.json`;
v02's three repair calls restore source shadow at `(60,55),(61,55)` on F3–5.
Replaying the final operations is checked against every native layer/frame target.
`build_delivery.py` packages actual MCP sheet crops; GIFs use exact palette indices,
original durations and integer nearest-neighbor display without quantization.

## Pass ledger and visual observations

| Artifact | Observation and decision | Native/export boundary |
|---|---|---|
| Preserved Sol baseline | Slow restrained motion preferred by user; primary part phase mismatch remains rejected | Original unchanged |
| `coherent-idle-v01.aseprite` | Primary mismatch corrected; new lifted two-pixel crease tip detached from source fold. Rejected for the new floating mark | Retained source/operations/contact |
| `coherent-idle-v02.aseprite` | Restored two connecting fold pixels on F3–5. Agent retains for user review: coherent primary keys, stable hands/feet, connected crease and familiar materials | Fresh reopen and all eight export matches pass |

Primary agent inspected actual native-size contact/full-body exports, 3x character,
4x original/new torso strips, 8x local crease and original concept comparison. No new
hole is visible at collar, shoulders, pockets or strap. The same facial raster is
registered rigidly at rest/inhale; expression and proportions are preserved. The
pale shirt/olive jacket keep their original shade relationships. Shirt follow-through
is very subtle at1x; torso timing still has a discrete one-pixel step. Motion could
remain too held or mechanical for the user; pose checks cannot resolve that taste.

The tools expose still-image inspection, not continuous temporal vision. The GIFs
were decoded across their complete authored timeline and Godot actually played the
cycle at1x speed; neither is represented as the agent perceiving a video continuously.
**Agent actual-speed temporal naturalness review remains unverified.** User review
of the actual-size normal-speed loops is the remaining artistic checkpoint. No new
attack or broader animation library should depend on approval inferred from this run.

## Observed technical and runtime evidence

[verification.json](verification.json): native targets equal actual MCP exports and
fresh reopened sheet for all8frames; original layer metadata and palette exact;
hidden guide, shoes, denim, tote and both hand layers exact. Lower-body composite
rows90+ remain exact. No new enclosed body holes or partial alpha; inherited source
hole `(63,116)` remains. Source's intentional head/hair openings are outside the
body-hole scope; visual silhouettes are a separate inspection.

Both GIF scales preserve the native visible timeline exactly; identical neighboring
holds may be merged. Final and first frame are exact rest. Phase-contract audit
rejects the original's F3/F6 head/neck mismatch and accepts v02. The localized v01→v02
native change is exactly2pixels ×3frames on03-shirt; other layers/timing preserved.
Scratch image/readback proved the L-shaped warm mark at(2,2), green pair at(8,4), blue
at(9,5), isolated blue at(13,12), skip/erase and protected-layer/native-reopen behavior.
Dedicated `validate` remains unexposed; no result is fabricated for it.

User confirmed the native/export test seams during this task. The focused suite checks
original disconnection, corrected delivery, corrupted foot export, corrupted GIF timing
and finite loop metadata. The finite-loop regression first failed (checker accepted
loop=2), then passed after requiring loop=0; [red log](evidence/tdd-red.log),
[5-test green log](evidence/contract-tests.log). The art correction preceded that
checker extension; this is not a claim that all art construction was test-first.
Existing director suite:35/35; existing character/shop checker:28/28. No numeric art score.

[Isolated Godot project](godot-preview/project.godot) reuses the existing preview,
scene and shop assets, without changing the original project/production textures.
Character at(88,69), ground anchor(68,185), zero root travel,362x304 viewport,128x192
native frames, nearest filtering and2x default window. Godot4.7.2.stable.official.ed1daf0bf,
macOS display, OpenGL/Metal compatibility renderer on Apple M3 Pro. First copy lacked
its imported environment cache and showed background-load errors; the isolated scene
was changed to read existing PNG bytes just as it already did for character/parts.
Final dedicated-MCP run captured all8frames, recorded at least3loops at authored
speed, returned no errors and was stopped cleanly. [Debug/stop evidence](evidence/godot-final-debug.json),
[runtime events](godot-preview/evidence/coherent-runtime.json),
[scene capture](godot-preview/evidence/runtime-startup.png).
This is scoped idle playback, not combat gameplay/controls or production-scale approval.

## Reusable workflow change

`tools/pixel-art-director/references/animation.md` now requires a shared frame/phase
plan, anatomical attachment chain, planted constraints, cause/attachment/release for
secondary motion, conditional backend recipes, and a native-size/actual-speed joint
review checkpoint. Existing motion-guide routing reaches it; the motion guide adds
latest feedback/candidate status. No new motion framework, mandatory amplitudes,
universal per-part lag or automated naturalness score. The discovered local skill
symlink uses this maintained source; old portable ZIPs and external installations are
unchanged. The rule's effect across future independent artists remains untested.

## Acceptance and remaining ownership

| Requested criterion | Observed evidence and boundary |
|---|---|
| Coherent breathing | Shared primary keys; phase mismatch gone. Naturalness awaits user playback review |
| Connected upper body | Registered head/neck plus repaired collar/shoulder pose; native/visual joint checks |
| Restrained secondary motion | Connected two-pixel crease extension; hair/bag stable where justified; user judgment pending |
| No independent jitter/sliding | Phase/anchor checks, all poses reviewed, fixed hands/feet; temporal perception gap disclosed |
| Clean loop | Exact rest at both ends, decoded timings and Godot loops |
| Appearance/editable source | Twelve layers, original palette/identity rasters; source and localized native revision/reopen |
| Reusable improvement | Existing procedure amended and focused regression checks; no cross-artist effectiveness claim |

Next owner: user reviews the exact v02 GIF/comparison for motion, rhythm, clothing and
expression. Agent owns any follow-up correction from concrete feedback. No artistic
approval, production replacement, installation elsewhere, commit, push or publication.

## Final independent review and changed files

[Two-axis review](review/review.md): Standards0 unresolved after the GIF-reader
resource fix; Spec0 material findings. Reviewers did not edit the art. The native
SHA above is unchanged after review. [Final audit](delivery-audit.json) checks3558
pre-existing files: only the three intended maintained documents differ, with no
unexpected historical/art changes. All8opaque runtime character captures equal
the actual native frames, and observed full-cycle interval is3382ms versus3380ms
authored (display scheduling). [Changed files and artifact hashes](changed-files.json).

Maintained files actually changed: `tools/pixel-art-director/references/animation.md`,
`docs/art/motion-guide.md`, and `docs/handoff.md`. All other task additions are in
this experiment folder: frozen source/plan, native candidates and MCP payloads,
packaging/contract/timeline/audit helpers and tests, exports/comparison/contact,
isolated copy of the existing Godot preview, and evidence/review records.
The original art-production and asset-contract files were read, not changed by
this task; their pre-existing uncommitted changes remain preserved.
