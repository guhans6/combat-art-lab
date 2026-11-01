# Trial B readiness record

Date: 2026-10-29  
Assigned output: `trial-b/`  
Trial intent: controlled same-seed model trial; frozen 128×192 source-guided pixel-art cleanup.  
Requested configuration: gpt-6-luna / max (retain host configuration).  
Aseprite editor calls so far: 0 / 120. No Aseprite MCP call, preflight, or editor-mode operation has been made.

## Frozen inputs and verification

Inputs were copied into `input/` from the declared fixture paths. The copies are read-only baselines; all construction will be under `passes/` and proof work under `proof/`.

| Input | SHA-256 | Role |
| --- | --- | --- |
| `input/seed.png` | `074168d9bfc5b2a2f2751810152bb0c31a71e7027a5368c0b393e17449fb84eb` | Common converted seed |
| `input/seed-baseline.aseprite` | `b1d91f6f87f650cbd2cae3edb69704d195bbdcf8d6b679b287d01e8a7283cc19` | One-layer native baseline |
| `input/seed-baseline.png` | `7353611071482ea1e879ab9c247fb1d92c7bd90050b8eb99cbec4cdbdf612d12` | Baseline export |
| `input/references/character-scene.png` | `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae` | Approved identity, style, full-body pose |
| `input/references/character-closeup.png` | `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7` | Approved identity and expression |
| `input/references/clean-generated-cutout-v1.png` | `12e971cc9e3cbfa7add2a17a62ff53d1f45b3c55197ce23c336a6447bed1f49e` | Supporting production geometry only |

`input/input-verification.json` records independent checks. The copied baseline parses as a 128×192, 32-bit, one-frame native document with the `shared-source-seed` layer. I decompressed its cel directly and verified that its RGBA bytes equal both copied PNGs: SHA-256 `8839680f1bc70c1c99653a28c76c6f8ea41f401d2755c93146d765523cb5806c`. The seed has binary alpha `[0,255]`, 7,844 visible pixels, and 254 visible RGB colors. The embedded 255-entry palette payload SHA-256 is `f2d4907a7493af8e6557f933e3c2c40d73f733658fc8250d925f79678ffb5b81`; exact payload and ordered RGBA entries are in `input/palette-chunk.bin` and `input/ordered-palette.json`. No input was requantized, reframed, or edited.

The project image runtime used for these checks is Python 3.12.14 / Pillow 12.3.0. The verification code is `verify_inputs.py`.

## Reference observations

I inspected the exact three declared references and the copied seed. Approved-source crops for direct inspection are retained in `reviews/`; they are review-only crops and do not change the common seed framing.

- **Scene:** full-height, relaxed three-quarter standing pose with hands in jacket pockets and one leg angled outward. The body reads long and natural, not chibi. Brown tied-back hair with a loose flyaway and broken bangs; olive open hooded jacket over a light shirt; broad blue jeans; pale shoes; cream tote and strap. Face turns and looks toward image-right. Background light is warm against a cooler dusk distance; that grading belongs to the scene, not as a full-body tint.
- **Close-up:** establishes an open, unequal near/far eye relationship and a rightward gaze; the nearer eye has more width, while the far eye is narrower under the fringe. The smile is small and slightly uneven, with a soft cheek/jaw. Hair reads as overlapping masses with deliberate fringe openings and a pale tie. Selective dark contours and shaped clusters remain visible; no blur is part of the requested finishing.
- **Supporting cutout:** confirms broad body, hair, tote and clothing geometry only. It differs in lighting, texture and edge treatment. Its feathered alpha and glow are not to be copied into the seed.
- **Seed at 1×, 4× and a 12× head review:** retains the full pose, costume, large hair silhouette and rightward head turn on the fixed canvas. The opaque silhouette bounds are x=32..103, y=2..184. Pixel alpha is already binary, and the baseline export is byte-identical at the decoded RGBA level. At high integer zoom the far eye reads much less openly than the approved close-up, and the restrained smile is difficult to separate from nearby skin pixels. These are the only facial changes presently proposed; exact patch scope will be confirmed from the actual pixel read after editor access. Some surface shading is finely varied, but I have no evidence to repaint the body or reduce detail wholesale, so it stays unchanged unless a later review identifies a concrete defect.

## Seed-use fitness decision

**Suitable only for bounded finishing of this named static-sprite task.** The seed already satisfies the fixed crop, canvas, full-body composition, pose, costume identity, large silhouette, binary-alpha policy, and palette control. Re-preparation or a different representation would invalidate the comparison and is not justified. The approved scene/close-up remain the identity and style authorities; the cutout is not allowed to override their face or expression.

The proposed repair scope is the compact face area only: preserve the three-quarter turn and gaze direction while making the far eye read open and keeping the slight smile legible at 1×. Preserve the larger near eye, hair silhouette/fringe openings, and all non-face pixels unless a specific reference-supported defect is observed. No blanket speckle cleanup, smoothing, partial alpha, palette editing, resampling, crop adjustment, background glow, or unrelated costume redraw.

## Frozen visual brief

- **Canvas and framing:** 128×192, one static frame. Keep original placement and visible bounds unless a proven defect requires no frame/crop change; the current plan does not.
- **Identity and expression:** same young woman; right-facing three-quarter face, unequal open eyes, rightward gaze, restrained uneven smile, soft cheek/jaw, brown tied hair and recognizable fringe/cowlick.
- **Silhouette and costume:** retain the existing relaxed full-body pose, proportions, jacket, shirt, wide jeans, tote/strap and shoes.
- **Pixel treatment:** deliberate opaque clusters, crisp nearest-neighbor edges, selective material contours, no blur or automatic smoothing. Existing ordered palette remains fixed; no palette entry RGB/alpha changes, added colors, or alpha policy changes.
- **Lighting:** keep reference identity/material colors; do not bake the scene's sunset glow or the generated cutout's halo into the sprite.
- **Native organization:** preserve an exact source backup and make the final layer structure useful for localized review/editing. The tentative plan is a seed-preservation layer plus semantically named authored layers for the facial treatment and any other independently revised part; choose final layer boundaries only after native/tool inspection. Do not claim full-body separation unless composite equality and layer coverage prove it.

## Pass and selection plan

Maximum three artistic exports, 120 total editor calls including discovery/smoke/proofs/failures. All calls will be counted in `call-log.md` with arguments, results and purpose. No calls have been spent yet.

1. **Pass 1 — face finish plus first editable organization.** Start from a copy of the common baseline. Read the relevant native pixels, define the smallest face mask from those observations, and make one coherent face correction. Keep all unrelated composite pixels exact. Save the native file, export PNG, operation record, layer inventory, pixel diff and direct reference/seed/candidate review at 1× and a matched integer zoom. The visual gate is identity/expression first; technical or craft gains cannot offset a face regression.
2. **Checkpoint.** Send the exact native/export/review to the supervisor and release the editor slot. Wait for defect-only feedback. Review it independently; perform another pass only when a visible, reference-supported defect remains.
3. **Pass 2 and optional Pass 3.** Each must repair a named defect in one coherent change, start from the best eligible prior, retain the rejected candidate, and repeat all reviews/checks. A newer pass is not presumed better. Stop early if the face gate is met and no justified improvement remains.
4. **Selection.** State best eligible, last attempted, decision, next baseline and reason independently. If no candidate meets the visual and technical gate, explicitly select none and retain the best prior.
5. **Native proof after selection.** Fresh reopen/export must match the selected PNG. Make a useful one-pixel/cluster edit on a labeled duplicate, then verify the selected file remains unchanged, the duplicate edit is localized, and protected composite/native data is intact. Proof does not alter the artistic selection and consumes editor calls.

## Technical checks and evidence boundaries

For each export: verify 128×192 RGBA dimensions, one frame, binary alpha, frozen palette payload/entries, exact native/export RGBA provenance, visible bounds, and changed-pixel locations. Check native frame/cel/layer names, visibility and positions; no partial-alpha or outside-mask change is permitted. Retain native source, PNG, exact editor operations and count, and direct original/seed/best/candidate sheets. Reopen the final candidate through the authorized MCP and compare a fresh export. Verify the localized edit only on its duplicate.

Visual assessment remains separate: identity, silhouette, face/expression, pixel craft, style and native editability use observed/uncertain/not-tested with reasons. A technical pass is not artistic acceptance. User approval, animation, Godot/runtime playback, gameplay scale, production readiness and publication remain unperformed in this trial.

## Current state / next action

Preparation is complete and no Aseprite/editor calls have been made. Await the supervisor's explicit editor-slot grant before tool discovery/preflight or any native operation. Once granted, record the actual server/editor/model identifiers and run the isolated scratch smoke checks within the shared call limit.

## Editor smoke outcome — blocked before art

On 2026-10-29 the supervisor granted the editor slot. `preflight({})` returned ready in the already-active headless mode, Aseprite `1.3.18.6-dev`, extension `0.8.2`, `switched:false`. Read-only `sprite_info`, `layer list`, and `look preview` worked. On the owned 16×16 scratch document, layer batch/rename/create and both a grid draw and filled-rectangle draw returned `aseprite_error: function: 0x…`. A subsequent preview was blank and `sprite_info` reported `modified:false`; no pixels were changed. The blank scratch was closed without force. No mode switch, CLI, UI, or shared-file operation was used.

The required construction smoke therefore did not pass. The issue is a local write-path failure of this MCP session, while preflight and read paths are available; the evidence does not yet distinguish the exact internal cause. Per the MCP-only contract, construction stops here. There is no artistic pass, candidate export, layer organization, localized-edit proof, eligible selection, or user approval. Conservative Aseprite-service call count is 28/120, including documentation reads, failures, and scratch setup; art exports remain 0/3. The supervisor has the editor-slot status and call log. The next action owner is the supervisor: decide whether to diagnose the authorized MCP write path and grant another slot. No further editor call is authorized in this slot.

## Scratch smoke retry — PASS

After the supervisor re-granted an exclusive editor slot, the same API operations succeeded on a fresh owned scratch document (`#19`). The layer batch created `protected-pattern` and `editable-layer`; a red/green/blue asymmetric mark rendered and matched its exact `look ascii` grid. A one-pixel white addition at (6,6) produced exactly one composite change and zero protected-layer changes. Default transparent `.` erased that pixel; `transparent:"skip"` left it intact. The source saved/reopened through the MCP with the same two layers and pixel maps; three PNG exports are byte-identical and RGBA-identical (`proof/scratch-smoke-verification.json`). A separate saved duplicate changed only (15,15); the local independent mask checker rejected that out-of-mask change (`proof/check_out_of_mask.py`). The original smoke file reopened unmodified. Aseprite remained `1.3.18.6-dev`, extension `0.8.2`, headless; no mode or configuration changes were made.

The earlier first-slot blocker remains preserved in `blocker-evidence.json`. This retry shows the current session write path is working, but does not identify why the first session's write calls returned function-pointer errors. Conservative total editor/service calls: 70 / 120; artistic exports remain 0 / 3. The trial is now entering pass 1.

## Pass 1 checkpoint — 2026-10-29

The owned baseline was reviewed at 1× and integer zoom. Both eyes are open in the unequal, fringe-partly-occluded arrangement; a pale sliver is present in the far eye. The seed's lower-face pixels did not read as a restrained smile at the review scale, while the close-up reference shows a short, curved smile. Pass 1 therefore adds only three #744433 pixels at (68,28), (70,28), and (69,29), preserving the original pose, silhouette, costume, eyes, palette, and alpha.

The corrected native and exported PNG are `pass-01/character-pass-01.aseprite` and `pass-01/character-pass-01.png`. The visual gate is provisionally met for identity, expression, silhouette, and pixel treatment; the first and only eligible candidate so far is pass 1. The output retains one editable full-sprite layer, appropriate for the requested static frame. It is not an animation rig.

Local binary/Pillow verification in `verify_pass01.py` passes: native cel equals the exported PNG; only the three recorded pixels changed; the frozen palette chunk hash is unchanged; alpha stays binary; dimensions, visible-pixel count, and visible bounds are unchanged. Direct comparisons are under `reviews/pass-01/`. The original baseline and copied inputs remain unchanged.

**Attempt evidence:** The first pass-01 layer-order construction placed its 3-pixel `face-smile` layer beneath the opaque base. The first export was byte/RGBA-identical to baseline and the composite readback showed no change. This was caught before checkpoint and corrected by drawing the same three pixels into the source layer. The failed export bytes are preserved as `pass-01/attempt-00/export-mismatch.png`, with diagnostic state in `pass-01/attempt-00/evidence.json`. The first native attempt was saved to the same pass-01 path and inadvertently overwritten during correction; its binary is not preserved. The call log records the exact observed layer state and reads. This is disclosed, not treated as a candidate.

Conservative editor/service count: 111/120; completed artistic passes: 1/3. The final candidate document was closed after save/export. **Next action:** await the supervisor's defect-only review; if no supported defect remains, select pass 1 and finish native reopen/duplicate-edit proof within the remaining call budget. No user approval, animation, gameplay-scale review, Godot playback, or publication has occurred.

## Supervisor defect review — 2026-10-29

The supervisor's review rejected the pass-1 mouth as a deep/puckered U or open-mouth mark. I independently repaired the scale mismatch in the review presentation: the approved source face is cropped to 180×140 and nearest-neighbour reduced by 5 to the same 36×28 footprint as seed/pass 1, then shown at 1× and 16×. The matched artifact is under `reviews/pass-01/matched-face-*`. This confirms the source's smile is shallower; the pass-1 mark does not pass the expression gate. Eyes/hair remain preserved.

Decision: pass 1 is rejected for selection. The exact seed remains the best prior available, but its smile is still uncertain at the target scale; selection is **none**. The next baseline, if work resumes, is the exact shared seed. At 111/120 editor calls only nine remain, insufficient for another art pass plus visual review and required fresh-reopen/duplicate-edit proof. The editor is paused for the other contestant, so this trial stops without requesting another slot. Fresh-reopen and selected-candidate proof remain unperformed; scratch smoke proof remains separate setup evidence only.
