# Quiet chest idle — Sol pass01

30 October 2026. **Retained for user playback review only; natural breathing is not established.** User rejected the previous shoulder lift as a shrug and earlier sideways torso inflation. This candidate removes those motions and proposes a smaller chest/cloth response beneath stationary shoulders. Parent independently inspected actual full-body3x and torso6x exports: shoulder/sleeve outlines remain steady, changed chest seam/folds remain connected, no former side ledges or shrug. Parent requested no further art pass. At1x the motion is very quiet. Neither agent watched actual-speed playback through these still-image tools; the user owns that judgment.

## Scope and construction

Input: `../2026-10-30-natural-idle-sol/pass01.aseprite`, SHA256 `25ae8dc1952cf5ef62d081735f52a56cb4cd726c08423d639b3c510b2d6f6f42`. Original scene/closeup were visually opened; identity cues and the newly supplied Reddit reference/access limit are recorded in [SOURCES](references/SOURCES.md). Read required context, glossary, handoff, ADR0001, art-production/style/motion/asset contract, validated checkpoints and canonical pixel-art-director/setup/craft/alpha guidance. No separate repository Definition of Done exists.

One bounded artist pass, with one possible parent defect correction; none requested or needed. Only this new experiment directory is artist-owned. All original/rejected candidates remain intact. Parent owns handoff and delivery report.

Native ownership is fragmented: jacket, shirt and strap cels include neighboring garment pixels. F2/F3/F4 garment owners were reset to the existing neutral F1 pixels to remove inherited shoulder/strap hoist. Then one connected front chest/open-jacket field bows forward by at most1px, with an associated1px lift of the existing lower shirt fold as cloth tension changes. Its discrete masks taper by limiting which height/width bands move at approach/peak/release. This is a volume/cloth hypothesis, not anatomical proof; no new highlight spot or moving oval was painted. Collar, shoulder tops, outer sleeves, strap, head/hair/face, hands, tote and lower body remain fixed. No new silhouette alpha is introduced.

New motion relative to neutral is entirely inside `[46,44,73,67)`. The 79/162/88 changed composite pixels in F2/F3/F4 include existing shirt/jacket boundary and broad fold clusters; the rest of the garment matches neutral exactly. The larger diff against rejected baseline also includes undoing its hoist. Construction and exact native call payload: [prepare.py](proof/prepare.py), [operations.json](proof/operations.json), [native call results](proof/native-results.json). Preparation computes source samples/masks; only dedicated Aseprite MCP writes native art.

Backend: Aseprite AI Artist0.8.2 headless, Aseprite1.3.18.6-dev. Nonlaunching doctor inventoried the installation; MCP preflight ready. Abbreviated scratch delivery/erase/save/reopen proof found exactly one erased pixel `(9,7)` and retained the red L. It did not repeat the complete two-layer setup smoke. No UI, Code-MCP, Lua, editor CLI, image generation, installation, nested agent, commit or publication.

The first explicit save_as to the new path was incorrectly rejected by automatic review as overwriting the baseline. A read-only check proved the destination absent and original hash unchanged; the same direct save_as then succeeded. No workaround or baseline save occurred.

## Artifact and observed verification

Native [pass01.aseprite](pass01.aseprite), SHA256 `82a4a7f309feae726b3e26134f114a21433a494a0eb2192bb7be82d2ca779b79`. Transparent actual native exports `frame-0.png` through `frame-7.png`; native MCP [GIF](pass01.gif). Main file saved, closed, freshly reopened as a new editor document, inspected, all eight PNGs freshly exported and compared exactly, then closed. No unsaved document remains under this lease.

- [1x neutral animation](proof/neutral-1x.gif), [3x neutral animation](proof/neutral-3x.gif).
- [Rejected shrug left / quiet chest right](proof/shrug-left-quiet-right-3x.gif), synchronized to original timing.
- [Actual all-frame1x](proof/contact-1x.png), [3x](proof/contact-3x.png), [torso6x](proof/torso-contact-6x.png), [transparent sheet](proof/transparent-sheet.png).
- [Original / rejected / new F3 comparison](proof/reference-baseline-candidate-3x.png). Original crop `[450,220,790,1040)` resampled only for preview; native panels nearest-neighbor3x.
- [Independent native verification](proof/verification.json), [reproducible reader/checks](proof/verify.py), [fresh reopen PNGs](proof/reopen/), [original input hashes](proof/input-hashes.json). Parent's additional checks are in `proof/supervisor-checks.json`.

Observed PASS: 128x192; twelve layers,96 cels,eight frames; original 255-entry palette; exact header/layer metadata/non-cel chunks/timing and cel geometry/opacity/z. Protected native layer pixels exact on all frames; all new garment motion confined to declared chest box relative to neutral. Original per-frame head/hair/face and complete blink frames F5/F6/F7 remain exact. Blink timings50/80/50ms and complete cycle600/350/550/600/50/80/50/250ms (2530ms) unchanged. Neutral shoulder/sleeve/strap/waist/lower-body regions and entire alpha silhouette exact every frame; no new enclosed alpha holes. Every PNG equals independent native recomposition and fresh reopen export. Original input hashes unchanged. Shared249-color explicit-index GIF previews decode to exact intended matte pixels/timing and infinite loop; no quantization drift. No separate validate tool is exposed, so scoped native/export checks are the actual validation boundary.

## Remaining boundary and next owner

Construction, native revision, export and preservation are proven locally. The shoulders no longer shrug in the inspected poses. The quiet chest cue may still read as small cloth motion rather than convincing breathing at played speed; do not describe it as approved or biomechanically proven. User next plays the exact GIF and accepts/rejects the motion. No Godot run, gameplay validation, installation, publication or user visual approval occurred. No dependent asset work is authorized by this technical result.
