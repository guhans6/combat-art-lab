# Natural idle study — Sol pass01

30 October 2026. User requested research of actual existing idle animations and a more natural continuation of the preferred Terra6.1 candidate. **Retained for user playback review; artistic acceptance pending.** Parent independently inspected all actual frame poses and requested no additional art pass. No actual-speed playback was watched by the agents; still-image tools exposed decoded poses and exact timing only.

## Inputs and acceptance boundary

Original identity authority: `assets/references/approved-2026-10-26/character-scene.png` and `character-closeup.png`, both visually opened before drawing. They show relaxed rightward gaze, tied brown hair, olive open jacket, pale shirt, wide jeans, cream tote and hands in pockets. They are appearance references, not motion clips. Terra preferred baseline: `../2026-10-30-idle-breathing-comparison/terra/pass01.aseprite`, SHA-256 `3ea95ac7cd738e3920bac50d22641b8d296ed28a61234f65898d43f4737964ee`. Preference does not approve its motion; the user found the torso stretching unsuccessful.

Task scope: new separate native candidate; preserve head/identity and original blink exactly on every frame, fixed denim/shoes/hands/tote, original eight frames/durations, canvas/palette/native metadata; construct a coordinated quiet torso/shoulder change without former horizontal widening. Budget: initial artist pass plus one parent-requested defect correction; only initial pass with focused technical cleanup used. No global/workflow/handoff edits or publication.

Read project context/glossary/handoff, ADR0001, art-production/style/motion/asset contract and validated-checkpoints; canonical discovered pixel-art-director skill plus setup/craft/face/alpha references. No separate repository Definition of Done exists. Acceptance here is the requested bounded motion candidate with construction/export/protection evidence; Godot, gameplay and user approval remain separate.

## Research actually performed

See [source and license record](references/SOURCES.md) and [download hashes](references/SHA256.json). Downloaded creator-published CC0 assets: Danilo Mattos's Sora idle PNG strips, thekingphoenix's original fourteen-frame idle GIF, and Doodle's urban sheet. Inspected actual extracted frame images; no artwork was imported or copied into our character.

Sora's side idle shifts the head/upper garment vertically over fixed foot placement; source PNG timing is unknown. Thekingphoenix GIF has six identical 100ms frames, one arm transition, six held lowered upper-body frames, then the return arm transition. This shows how holds and motion overlap can make a small cycle intentional; its armed pose and head motion are not a direct anatomical model for this character. Urban's sheet provided clothing context but no reliable timing labels. These are observations from these examples, not universal animation rules. An asset with an explicit no-AI restriction was excluded from download/study.

Motion plan: preserve feet/pocketed hands and head; let the upper jacket/shirt/strap rise 1px, reach 2px, then settle through the 1px pose. Use a common vertical field across actual garment owners, tapering to stationary lower sleeves/waist. No horizontal displacement or widening. Existing pose durations remain `600/350/550/600/50/80/50/250 ms` (2530ms total). Retaining this timing is a first controlled comparison, not a finding that it is ideal. Head motion seen in references was omitted because the exact head/blink is protected.

## Native construction and local correction evidence

Backend: Aseprite AI Artist0.8.2 headless, Aseprite1.3.18.6-dev. Nonlaunching doctor inventoried the installed executable; native MCP preflight reported ready. All native drawing/save/export/reopen operations used dedicated MCP. Python read native files, calculated explicit patches/masks, composed analysis/proof images and made faithful GIF previews; it did not author a sprite file or replace the editor drawing path. No UI, Code-MCP, Lua, CLI editor launch, new service, install or paid generation.

Actual native inspection found fragmented ownership: shirt and strap contain adjacent jacket pixels; face/neck layer owns some collar neighbors. Whole-cel translation would move unrelated content. `proof/prepare.py`, `allowed-mask.png`, `operations.json` and `native-call-operations.json` retain the precise coordinate/native-owner preparation and drawing payload. Only native layers `02a-jacket-left`, `02b-jacket-right`, `03-shirt`, `05-tote-strap` on F2/F3/F4 changed, in x31–95/y34–68 with the explicit cloth/owner mask. Palette unchanged.

Initial drawing calls used array coordinate pairs; MCP schema rejected them without mutation. Converted to `{x,y}` points and applied successfully. Palette-lock snapping gave erased alpha-zero samples nonzero hidden RGB; a transparent-only follow-up with paletteLock false normalized these to RGBA zero without changing the palette. The MCP frames-pattern export wrote one literal filename; explicit per-frame PNG exports replaced it and the ambiguous file was removed.

Coverage/protection cleanup preserved at `proof/pass01-precoverage.aseprite`: strict mask caught two resets outside the cloth mask, restored to exact baseline; coverage found one new transparent joint pixel at (70,40) beside fixed collar pixels, filled with existing olive on the actual shirt owner across F2/F3/F4. `coverage-cleanup-operations.json` records these nine native pixel changes. This is a demonstrated localized native revision, not a second aesthetic experiment. Final PNGs all match independent native recomposition; the main file was saved, closed, freshly reopened, inspected and all eight PNGs exported again exactly. No unsaved document remains open under this lease.

## Delivered artifact and evidence

Main native: [pass01.aseprite](pass01.aseprite), SHA-256 `25ae8dc1952cf5ef62d081735f52a56cb4cd726c08423d639b3c510b2d6f6f42`. Transparent frames: `frame-0.png` through `frame-7.png`. Native MCP GIF: [pass01.gif](pass01.gif).

- [Exact 1x neutral preview](proof/neutral-1x.gif), [3x neutral preview](proof/neutral-3x.gif).
- [Synchronized comparison](proof/terra-left-sol-right-3x.gif): Terra left, Sol right, 3x, no headings added to the frame.
- [All frames 1x](proof/contact-1x.png), [all frames 3x](proof/contact-3x.png), [collar/strap/waist continuity6x](proof/torso-continuity-6x-light.png).
- [Original/baseline/candidate comparison](proof/reference-baseline-candidate-3x.png). Original scene crop `[450,220,790,1040)` is resized only for this preview, preserving aspect ratio; native character panels are nearest-neighbor3x.
- [Independent native/export/protection checks](proof/verification.json), reproducible reader/check recipe `proof/verify.py`, and fresh exports under `proof/reopen/`.

Observed: 128x192,12 layers,96 cels,eight frames; equal header, layer metadata, cel geometry/opacity/z and all non-cel chunks including palette/timing. Exact protected native head/neck/hair/denim/shoes/hands/tote and original blink composite on F5/F6/F7. All pixels below y69 unchanged; every source hash recorded before editing remains exact. No new enclosed alpha holes; eight PNGs equal independent native composition and all fresh-reopen PNGs. Native GIF and explicit-index matte/comparison GIF frames equal intended pixels, original durations, infinite loop. Explicit shared 249-color palette avoids Pillow quantization changes. The tool surface exposes no separate validate tool, so these scoped independent checks are the observed validation boundary.

## Visual assessment and remaining work

Constructor inspected actual full-body1x/3x frames, native torso preview, original/baseline/new comparison and all collar/strap/waist crops. Upper silhouette rises and returns as connected garment forms, without the former sideways bulge. Face/neck expression is unchanged, pale shirt/olive coat/cream strap remain coherent; no independent bright patch or broken collar overlap is apparent. Parent's independent frame review likewise retained pass01 as a playback candidate, without requesting a second artist pass.

Whether the modest lift looks like natural breathing at actual speed remains the user's judgment. The fixed head limits natural upper-body coupling; do not describe the motion as biomechanically proven. The inherited timing may still feel held/stepped. No Godot run, gameplay validation, user approval, installation, commit, push or publication occurred. Parent presents the exact GIF; user selects/rejects the perceived motion before any dependent asset work.
