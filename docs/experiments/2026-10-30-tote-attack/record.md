# Experiment: source-guided tote swing and recovery repair

## Superseding user rejection — 31 October 2026

User identified the F9 recovery grip/handle join as disconnected in the delivered
before/after and supplied a close crop. The parent withdraws its earlier visual
claim that the shared grip/continuous handles were adequate. Sol6.1 authored this
repair; parent inspected and incorrectly let it through the visual checkpoint.
The technical/runtime results below remain valid only for their stated boundaries;
they did not test a believable hand wrapping/grasping the handle or sound strap
attachment. V03 is rejected as the recovery repair, preserved as evidence, and must
not be promoted. No replacement has been drawn in this feedback turn. Original
generated pose remains available. Next correction must establish a clear hand/strap
occlusion and continuous strap-to-rim path in an enlarged key proof before cycle
integration. This section supersedes the earlier candidate-selection/visual claims.

- Status: observed prototype; user artistic review pending.
- Dates: 30–31 October 2026.
- Question: Can the supplied attack keys and weak middle recovery become an editable attack without another generated sheet?
- Intent: bounded end-to-end attack prototype, not model comparison or production replacement.
- Reference roles: canonical scene/close-up establish identity; supplied sheets propose poses; existing neutral establishes resting appearance and approximate character scale. Current art-production/style/motion/asset rules apply.
- Frozen inputs: [manifest](inputs/manifest.json). Original sheets and native neutral are unchanged.
- Tools observed: dedicated headless Aseprite MCP, Aseprite1.3.18.6-dev/extension0.8.2; Python/Pillow12.3 for preparation/readback/review; dedicated Godot4.7.2 MCP.
- Authority: research, native repair, exports and isolated engine test. No new purchase, credentials, external installation, commit or publication.

## Delivered artifact

[tote-attack-v03.aseprite](artist/sol-rescue/source/tote-attack-v03.aseprite), SHA256
`1f6d68c6927bbcc594be9913156f74a6b0939aa373a9be9971dcd5be8ab52065`.
13frames/1680ms,320×192 canvas, approximately180px drawn character height. Extra width
contains the full bag arc; it does not enlarge the character or establish a production
grid. First/last frames retain the exact existing neutral at x64. No new imagegen.

[Review page](review/index.html) contains actual-speed [1× GIF](review/attack-1x.gif),
[nearest3× GIF](review/attack-3x.gif), [duration contact](review/contact-1x.png),
[2× contact](review/contact-2x.png), and [recovery before/after](review/recovery-before-after-3x.png).
The diagnostic left side preserves the flawed converted source, including its stray
crop fragment; the final right side removes it. Transparent frames are under
`artist/sol-rescue/frames/v03-frame-0.png` through12.

## Findings and applied motion

[Research](research.md) records five first-party animator/publisher lessons.
The applied chain is support/pelvis → thorax/shoulders → elbows/wrists → shared handle
bundle → flexible bag. The body brakes and elbows fold while the tote remains
downstream briefly, then guides it toward the hip. No blanket one-frame lag or
independent decorative sway was added. Published principles guide a stylized pose
proposal, not cloth physics. Research text and decoded example stills were inspected;
no continuous tutorial/video viewing is claimed. See [visual observations](evidence/source-visual-observations.md).

Equal sheet-cell crops had discarded bag tips crossing cell boundaries. Enlarging
the resulting sprite could not restore those pixels. Rescue uses complete full-sheet
silhouette masks, excludes neighboring fragments and retains shared family scales
(.4333 main/.264 additional), rather than fitting every pose independently. A neutral
head transplant also produced a doubled neck/collar despite passing silhouette
connectivity. Action head/neck/collar now remain together. These construction defects
were demonstrated by the assets; export timing was not their cause.
[Preparation findings](review/preparation-findings.md) retains the evidence.

Seven normal editable layers own legs/shoes, clothing, underarm backing,
head/neck/collar, tote/handles, grip and handle tension. They own visible drawings,
not hidden rig surfaces. Source scripts/masks/palette projection/literal operations
remain under [sol-rescue](artist/sol-rescue/), with [construction record](artist/sol-rescue/record.md).
Native imports/edits/registration/saves/reopens/exports used dedicated Aseprite MCP;
Python did not write native files. A duplicate-only tote-fold edit demonstrates
localized revision without changing other cels or the selected candidate.

## Phase and timing plan

All timing is in native, GIFs and [metadata](artist/delivery.json). Registration is
baked into cels; engine offsets are zero. Ground anchor y185/front sole y184; raised
rear toe pivots are retained. Hair/face/neck stay together in their source action
poses; sleeves and garment folds follow the corresponding body/arm poses. Blinking
is outside this attack scope.

| Frame | ms | Connected pose/action |
| --- | ---: | --- |
| 1 | 60 | Exact neutral, tote supported at shoulder. |
| 2 | 110 | Pickup, hand reaches handle with attached shoulder/neck. |
| 3 | 140 | Shared grip, widening stance. |
| 4 | 210 | Counter-windup left; torso/shoulders turn with arms/load. |
| 5 | 70 | Acceleration right; handle bundle leads tote. |
| 6 | 60 | Committed contact; extended arms/lunge transmit force. Only active key. |
| 7 | 90 | Follow-through; front sole[208,184], bag continues beyond wrists. |
| 8 | 110 | Arrest/redirect; same front sole/lunge, elbows bend, tote outward/downstream. |
| 9 | 140 | Recovery; clasp and continuous handles guide tote inward. |
| 10 | 170 | Tote settles closer to hip; hands support load. |
| 11 | 140 | Re-shoulder; supporting hand raises handle, torso re-centers. |
| 12 | 160 | Transfer/release, bag supported at shoulder. |
| 13 | 220 | Exact original neutral return. |

Proposed contact interval590–650ms. Later stance resets are coarse key-pose steps;
they are not certified as polished continuous footwork. Final/first images are exact.

## Pass and selection ledger

| Checkpoint | Observation / decision |
| --- | --- |
| Luna recovery v01–v03 | Open/doubled neck; rejected before cycle propagation. [Critical review](review/recovery-base-critical-review.md) and [reproduction](evidence/open-neck-reproduction.json). |
| Terra mechanical native | Clipped tote/foreign fragments persisted; preserved, not selected as art. [Handoff](artist/handoff-terra.md). |
| Editable import test | Reported lack of editable PNG import disproven by actual normal RGB paint-layer open/native save/one-pixel edit. [Proof](evidence/png-paint-import-proof.json). |
| Sol rescue v02 | Full silhouette/native recovery repaired. Parent found front-foot registration and two canvas-edge curl pixels. |
| Sol rescue v03 | F7/F8 +18px x holds F6–F8 front sole; two F9/F10 curl pixels moved off row0. Retained for user review. [Delta proof](artist/sol-rescue/review/v03-focused-correction-checks.json). |

The one critical reviewer became the bounded rescue editor after earlier failures;
its earlier review does not approve its own edits. Parent freshly inspected recovery
at1×/3×, final all-frame contact, before/after and Godot contact/idle captures. No
blocking detached neck/arm/handle or clipped bag remains visible in those inspections.
Redrawn cuffs look flatter/blockier at3×; source-key shading/head placement and coarse
stance resets still need actual-speed user judgment. Parent cannot establish motion
naturalness through stills. [Review closure](review/review.md) separates these boundaries.

## Observed checks

| Check | Result / evidence |
| --- | --- |
| Native/export | All13native composites=PNGs=fresh dedicated-MCP reopen; binary alpha, shared palette, transparent margins, exact neutral return. [Parent checks](verification.json). |
| GIF | Both1×/3× timelines/pixels exact,1680ms. [Checks](review/gif-verification.json). |
| Editability | Duplicate changes exactly20visible pixels on F9/tote layer; all other native cels exact; fresh MCP export matches. [Independent audit](preservation-verification.json), [reopen evidence](artist/sol-rescue/review/native-v03-verification.json). |
| Godot |4.7.2, isolated362×304 nearest street target. Three synthetic Space events→three attacks, one F6hit each, three actual idle returns. Durations1673/1667/1666ms vs1680 authored; frame clocks within50ms observation tolerance. [Audit](runtime-verification.json), [raw observation](runtime/godot/evidence/attack-observation.json). |
| Rendered pixels |13/13live frame captures match opaque source pixels; three idle-return captures exact. No paused fallback used. |
| Runtime errors | None in debug or stopped-project final errors. [Debug evidence](evidence/godot-final-debug.json). |
| Regressions | Director35/35, existing character/shop28/28. evidence/director-tests.log and evidence/existing-assets-checks.json. |
| Preservation |3775historical files checked; only four intentional maintained-doc changes. Sixinputs,42Luna/17Terra attempt files unchanged. preservation-verification.json. |

The dummy rectangle was chosen from the contact key; this proves input/active-hit/
return integration, not combat balance or real cloth physics. Physical keyboard use
was not tested. Engine executed actual-speed playback; continuous agent temporal
perception was not performed. Engine stopped and native editor closed.
[Runtime instructions](runtime/README.md) distinguish the fixture from final art.

## Workflow delta and next owner

Small director guidance changes cover complete silhouettes before grid slicing and
actual editable raster-open capability tests. Existing shared-phase/anatomy/visual
key checkpoints remain in force. No new system, numeric art score, portable-bundle
replacement or broad rewrite.

Actual changed files: this experiment tree plus `docs/handoff.md`,
`docs/art/motion-guide.md`, and director `references/animation.md`/`references/adapters.md`.
[Artifact hashes](artifact-manifest.json) identify delivered files. Unrelated dirty
work is preserved; Git remains `9e35c5c13987a153e942e6f93f49f247fad13c3a`.
No commit/publication/production replacement/other-host installation.

**User feedback:** no approval of v03 yet. Next owner: user watches actual-speed GIF
and judges weight/grip/recovery/appearance/pacing; agent owns subsequent bounded
correction. Remaining polish target: stance-transition spacing and recovery cuff
shading if the overall action is accepted. No new source sheet is required by the
demonstrated repair.
