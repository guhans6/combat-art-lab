# Project context

## Current direction — 1 November 2026

The user has set the tote character aside to try a new design. Start at
[the next-asset guide](docs/new-asset.md). Earlier character choices and artifact
pointers below are historical case-study context, not constraints for the new design.
The existing workflow, deterministic conversion option, native asset requirements,
and tool permissions are unchanged. No new character, size or palette selected.


Updated: 27 October 2026.

## Goal

Develop a repeatable, AI-assisted way to turn the user's imagined visual style into an original character, usable sprite assets, and convincing combat animation for a 2D Godot game.

The user is new to game development, cannot currently draw, and wants to direct and monitor AI while learning relevant fundamentals.

## Settled direction

- Godot is the intended game engine.
- Visual style and combat animation should be investigated early together.
- Start with generated concept images and iterate until the user selects the desired direction.
- Translate approved examples into explicit visual and motion rules.
- Have AI construct and revise the actual native asset sources through suitable tools, code, layers, frames, or rigs.
- Preserve an AI-friendly revision process; the intended workflow does not depend on the user repainting PNGs.
- Capture research and rules in this repository so work can continue in Codex.

[ADR 0001](docs/adr/0001-ai-directed-art-workflow.md) records this direction.

## Current workflow research — automation boundaries, 27 October 2026

[Source-guided automation analysis](docs/research/source-guided-automation.md) builds on
the already observed assisted bust and later standing/shop work. For the next studies,
the proposed default is deterministic conversion/region seeding plus aligned original
guidance and targeted native cleanup. Scripts can compute the first fill after crop,
scale, palette and masks are fixed; choosing/reviewing those inputs still needs judgment.

[The next experiment](docs/experiments/2026-10-27-automation-routing.md) first
replays the existing 120x112 nine-part head seed in new outputs, then compares cheaper
and stronger models on identical bounded tasks. It is planned, not run. No model-tier
equivalence, savings, final production resolution or new art approval is established.
This research creates no replacement asset: standing-alpha-v03 and shop-modular-v02
remain the current sources described below; their recorded scoped Godot evidence
supersedes the older continuation summary's absence of runtime proof.

## Reference-to-sprite scope clarification — 29 October 2026

The broader objective is to analyze user-supplied reference art with human direction,
identify its relevant rendering properties, and construct revisable sprites in the
chosen direction. The current cinematic-pixel character is one test case, not a
universal recipe. The [intake and representation boundary](docs/workflow/art-production.md#reference-intake-and-representation-choice), [shared-seed retest plan](docs/experiments/2026-10-29-luna-shared-seed-retest/generalization-plan.md), and its future-validation matrix record the next bounded work. The requested retest validates only the existing pixel route; illustrated/rigged and action references remain untested.

## Current quality review

All eight character frames and sixteen shop parts reviewed. Current native sources: standing-alpha-v03 and shop-modular-v02. Small neck-ownership/hidden-backing/pot fixes pass native reopen/protection, all28 project checks and32 director tests, plus fresh Godot playback. Future agents run [the project checker](tools/check_art_assets.py) through the authorized MCP path, following [the reviewed profile](tools/art-quality-profile.json). See [review record](docs/experiments/2026-10-27-character-shop-quality-review/record.md).

## Prior character repair

The user reported transparent denim gaps. Current source is [standing-alpha-v02](assets/source/standing-alpha-v02/standing-idle.aseprite): twelve fabric pixels restored per frame and a joint backing for inhale. All eight body exports pass coverage; thirteen protected layers and palette/timing are unchanged. Godot startup now rejects the original damaged frames and plays corrected frames. See [diagnosis](docs/experiments/2026-10-27-denim-alpha-repair/record.md).

## Current shop milestone

The user liked the standing idle scene and authorized first-shop refinement. A separate sixteen-part native facade and reusable Godot scene now pass scoped part assembly, native reopen, isolated light edit and two-instance/visibility/move checks. See [shop record](docs/experiments/2026-10-27-shop-modular-refinement/record.md). User reviews the new pots/board and simpler hidden glazing; dynamic lighting and packaged export remain untested. Original character/shop sources are preserved.

## Next proof boundary

Review the [full standing idle scene](docs/experiments/2026-10-27-standing-idle-godot/scene-idle-preview-mcp.gif).
The character has fourteen semantic layers and eight native idle frames at 96x216, with
one-pixel breathing/blink and fixed feet. First shop has six editable visible-part layers.
Actual Godot playback has now also been verified through the dedicated Godot MCP protocol:
all eight rendered frames, two loops, no runtime errors, successful stop.
See the [art record](docs/experiments/2026-10-27-standing-idle-godot/record.md) and
[installation proof](docs/experiments/2026-10-27-standing-idle-godot/godot-mcp-install/mcp-smoke.json).

User constraint: use dedicated MCP tools; no computer use; **do not use Code-MCP**.
The user authorized needed MCP installations for this workspace. Godot MCP 0.1.1 is installed
and configured in project `.codex/config.toml` as `godot-art-lab`; existing Aseprite is preserved.
After the workspace restart, all six dedicated Godot tools appeared directly in the chat.
Native MCP version/project inspection and scene launch passed; runtime captured all eight
frames and completed at least two loops with no reported errors. The engine startup capture
was visually inspected. No global configuration change or new paid service.
The independent strict binary/header and full-hash audits remain unrun; do not claim them passed.
User next reviews likeness, scale and idle restraint before further building production.

## Open choices

| Choice | Current state |
| --- | --- |
| Visual references and target style | Original scene/close-up remain authoritative; recent resolution studies explicitly rejected by user; v01-v04, drawn street and v03 pilot preserved; final native likeness/style acceptance pending |
| Pixel art versus illustrated/other 2D rendering | Cinematic pixel art is the preferred reference direction; native rendering rules remain provisional |
| Camera and facing directions | Open |
| Character design, weapon, and attack | Female design finalized (tied brown hair, olive jacket, wide blue jeans, cream tote); weapon and attack open |
| Native resolution and on-screen scale | Provisional 128x192 standing canvas / 184px drawn height; actual Godot scale untested |
| Palette, outlines, shading, and texture | Open |
| Frame-by-frame, cutout/rig, or 3D-to-sprite method | Open |
| Aseprite, MCP bridge, generator, and paid-service budget | Existing Aseprite 1.3.18.6-dev and Pebbly 0.8.2 headless used; normal MCP preflight ready on 27 October. No new integration, purchase or paid art service authorized by this research task |
| Final game scope and asset volume | Deferred until the first proof |

Aseprite is a candidate because it exposes drawing and animation operations. Its availability does not decide the art style. PixelLab, editable pixel grids, cutout rigs, and rendered 3D remain researched options.

## Initial research/setup evidence (historical)

Research inspected official documentation, public implementations, creator reports, a research paper, and a published simple attack. No new art generation, installed Aseprite integration, or Godot playback was performed for this repository setup.

The existence of an API or a successful external demo establishes a possible method. The user's references must be tested before claiming the intended style is achievable with acceptable revision effort.

## Initial setup scope (historical)

Create the repository, preserve research, configure the requested engineering workflow, and leave a concrete handoff. Do not silently start full game development or select the user's style during setup.

## Reference-study milestone — 25 October 2026

Two user-supplied Until Then screenshots are preserved in assets/references. [Lighting study v01](assets/concepts/2026-10-25/lighting-study-v01.png) is a generated original concept comparison, awaiting feedback; it is not a production sprite. See the [reference study record](docs/experiments/2026-10-25-reference-study/record.md) for findings and evidence.

The user's existing compiled Aseprite 1.3.18.6-dev was copied from Gadot Sample/ForestDuel to `/Applications/Aseprite.app` at their request. A two-layer swatch test proved native save/reopen, localized revision, and PNG export. No character asset or Godot playback was produced. No new MCP or skill was installed.

## Standing reconstruction milestone — 26 October 2026

The user finalized both an original female character design and its concept rendering, then authorized an Aseprite reconstruction with internet drawing research and no computer use. See [approved references](assets/references/approved-2026-10-26/character-scene.png), the [style guide](docs/art/style-guide.md), and [standing proof](docs/experiments/2026-10-26-standing-reconstruction/record.md).

The agent constructed one pose through authored pixel/polygon instructions in Aseprite Lua. Native source has 12 named layers; export is 128x192 with 45 visible colors. Save/reopen, exact export rebuild and isolated tote-color revision passed. The likeness is recognizable but not exact, particularly face/hair and fabric folds. User approval, animation and Godot playback remain pending. No computer use or new integration installation was performed.

## Face-first refinement — 26 October 2026

The user liked v01 and requested iteration, mainly face first. v02 adjusts eyes, jaw, cheeks/neck, then hair, denim/sleeve highlights and shoe accents. [Face comparison](assets/previews/standing-v02/face-before-after.png) and [full-body comparison](assets/previews/standing-v02/full-before-after.png) preserve reference/v01/v02 side by side. See [refinement evidence](docs/experiments/2026-10-26-standing-refinement/record.md). Same canvas/anchor/layer structure; independent rebuild and native reopen checks passed. Final visual acceptance and all motion/engine boundaries remain pending.

## Head-only v03 — 26 October 2026

The user supplied specific identity corrections for eyes, expression, cheek/jaw, ear and hair, and explicitly locked neck/body. v03 edits v02's native head layers with a hard mask. [Head comparison](assets/previews/standing-v03/head-before-after.png) and [record](docs/experiments/2026-10-26-head-v03/record.md) show the result. Both eyes have separate clusters and rightward pupils; hair is rearticulated. 369 visible pixels changed, none outside the head mask; neck/body and v01/v02 were independently checked unchanged. Same grid and palette, native save/reopen passed. No visual approval, animation or publication inferred.

## Shoe detail v04 — 26 October 2026

The user requested a small increase in shoe detail. [v04](assets/source/standing-v04/standing.aseprite) adds lace/eyelet contrast, panel seams and sole accents on existing shoe pixels only. [Before/after](assets/previews/standing-v04/shoes-before-after.png). 89 changed pixels; 11 other layers, head/face, alpha silhouette, stance, canvas and palette unchanged. Native save/reopen passed; see the [record](docs/experiments/2026-10-26-shoe-detail/record.md). Earlier versions remain preserved; work is local/uncommitted.

## Static street placement — 26 October 2026

The user requested the original scene background with reconstructed v04 standing in it. [Street preview](assets/previews/street-preview-v01/street-scene-4x.png) and [14-layer native scene](assets/source/street-preview-v01/street-scene.aseprite) are ready for review. The original figure was removed by one built-in imagegen background edit; the clean plate is a flat imported raster. Character layers remain exact v04, translated at native size into a provisional 352x264 scene, with a separate grounding shadow. Native reopen and exact character-placement checks passed. See [evidence](docs/experiments/2026-10-26-street-preview/record.md). No Godot or motion validation is implied; work is local/uncommitted.

## Aseprite-drawn background — 26 October 2026

The user rejected the raster-plate placement as a style mismatch and explicitly requested drawing the background in Aseprite. [Drawn scene](assets/previews/street-drawn-v01/street-scene-4x.png) now has 16 environment layers and exact v04, plus separate shadow (29 scene layers). [Source](assets/source/street-drawn-v01/draw-background.lua) draws geometry, planes and plant branches without any background/reference raster import. Native save/reopen, local lamp edit and exact fresh-folder PNG rebuild passed; see [evidence](docs/experiments/2026-10-26-drawn-background/record.md). This is a simplified interpretation of the original scene, pending user visual review; no engine/motion or publication claim.

## Feasibility research and workflow refinement — 27 October 2026

[Current research](docs/research/concept-to-native-pixel-art.md) separates pixel craft, generated-concept interpretation, native/display scale, cinematic lighting and animation routes. The strongest supported explanation for the reference mismatch is insufficiently controlled feature prioritization and structural interpretation, with a possible pixel-budget contribution still unisolated. Neither the existing 128x192 drawing nor the six-pixel protected correction establishes a maximum achievable likeness.

The workflow now adds reference-feasibility review, scale studies and independent review dimensions before detailed reconstruction. The director selects new reconstruction versus protected correction explicitly; existing mask/native protection checks remain intact. Style/feature budgets and lighting separation are proposed rendering rules, not newly approved art direction. ADR 0001 remains unchanged.

Two fresh native crop studies, each with two passes, were produced at 192x288/256x384 full-character equivalents. [Evidence](docs/experiments/2026-10-27-resolution-feasibility/record.md) retains all sources and previews. They are **inconclusive**: anatomy, head position, crop and detail differ, so no resolution winner is justified. Seven-layer native save/reopen/export and local edits passed. Initial strict native checks exposed palette/header changes during save; stable normalized scratch baselines then passed the unchanged strict protection checker. All prior artwork and experiments remain preserved.

Next agent action: align one head-only reference crop and normalized hair-top/eyeline/chin/neck/shoulder blockout before detailed redraw. Include a fresh 128-equivalent interpretation before attributing any improvement to a larger grid. The new layout checkpoint addresses this observed failure but awaits a controlled redraw. User owns artistic selection; agent owns construction and verification. Final production scale, animation effort and actual Godot readability remain untested. No commit, push, publication, new integration or paid art service was performed by this task.

## Follow-up: reference drift audit — 27 October 2026

The user explicitly rejected the recent studies as unlike the original and asked whether inadequate reference use or enlargement caused the failure. [Source audit and visual findings](docs/experiments/2026-10-27-reference-drift-audit/record.md) confirm fresh polygon construction, then a 0.76 transform of earlier head coordinates with three extra hair shapes. The main comparison omitted approved-original panels. This supports drift during construction/review, but does not prove the agent never inspected originals or enlarged a PNG. The normalized-layout rule was added after that failed experiment; its later presence is not evidence of earlier violation.

The director/workflow now require visually opening originals before drawing and saving/inspecting an original-versus-actual-export sheet with a reasoned decision at every meaningful blockout/revision. A small tested helper records crops, hashes and display scaling without judging likeness. One 120x112 head/shoulder study mapped to a fixed close-up crop exercised the review: a blank technical export and wrong hair-mass blockout were caught and preserved; a feature checkpoint still changed expression/hair too much, so it was rejected and art iteration stopped. This is evidence of detection and honest stopping, not accepted art or a successful resolution comparison.

Next agent action: resolve crown/fringe/tied-hair structure and near/far lid/shallow-smile expression directly against the originals, in a bounded same-layout study. Do not promote these rejected results or infer a production grid. Native sources retain ten layers and a duplicate-only 15-pixel tie revision; strict palette/header preservation failed and remains disclosed. All prior artwork/experiments are preserved; no install, paid art service, commit, push, publication or Godot run occurred.

## Original-guided head revision — 27 October 2026

The user authorized the next focused study. [Record and native source](docs/experiments/2026-10-27-original-guided-head-v02/record.md) preserve three passes: crown/tied-hair reconstruction, face/skin/expression, then a bounded knot/curl/far-eye refinement. All retain the same 120x112 canvas and `(380,64)-(860,512)` approved close-up crop. The four clothing layers are unchanged. The original is shown directly with each actual candidate export; no new resolution comparison or full-character grid is inferred.

Agent review finds it closer than the rejected input, but crown sweep, central fringe, far-eye visibility and smile still differ materially. User visual selection is pending; no replacement of v01-v04 or accepted new design is claimed. A separately assigned read-only visual review agreed it merits showing as provisional, not a faithful match.

Native reopen/export, layer/pixel protection and full strict metadata checks pass for all three checkpoints and a duplicate-only 16-pixel tie-color edit. A reference-informed palette was explicitly pinned before freezing the working baseline, preventing previous save-time palette churn without weakening the checker. Earlier source files and failed evidence remain intact. Next owner: user reviews the displayed comparison; any further agent pass should focus on head turn/lids/shallow smile and rounder swept-back crown while protecting clothing. No install, paid art service, commit, push, publication or Godot run.


## Multi-reference assisted comparison — 27 October 2026

Current user goal: usable assets retaining the approved identity, aesthetic, expression
and vibe; intentional simplification is acceptable. Additional generated references are
permitted for named needs, with canonical originals retained and new inputs reviewed.
The approved original scene/close-up remain identity/style authority.

[Assisted bust v01](assets/source/assisted-bust-v01/bust.aseprite) is the agent's provisional
conversion-plus-cleanup choice (C01 retains clearer eyes and restores the B01 smile) from one controlled crop/grid comparison, not a user-approved
full sprite. The trace arm and all prior art/failures remain preserved. A single generated
blink reference supplied only eyelid guidance; a five-frame native expression probe retained
eight other layers and was played in the browser. No Godot, attack/contact or full-body
production-scale proof. Native reopen, strict duplicate edits and fresh-folder static
rebuilds passed. No install, new paid service, commit, push or publication. User next selects
the concrete bust treatment; agent owns subsequent full-body construction/cleanup.
