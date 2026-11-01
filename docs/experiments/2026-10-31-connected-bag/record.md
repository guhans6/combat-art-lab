# F8–F10 connected-bag workflow trial — 31 October 2026

## Outcome

A separately saved repair of the bag/handles in F8–F10 passed the structural and
final visual checkpoints. [Three poses](review/three-poses.png),
[baseline versus final joins](review/join-comparison.png),
[full-cycle context](review/full-cycle.gif), [native source](source/connected-bag.aseprite).
SHA256 `3a628bd6960903db95e5908182ff1e62899e852a6cf284cb0be273be96650ec9`.
This is a reviewed candidate, not user-approved art or a completed gameplay test.

The bag body, near strap roots and rim now share one local construction rotated
through the three poses. Near straps continue into front fabric; the thinner rear
loop ends behind the rim. The same gathered bundle stays under the existing hands.
Old fork/edge fragments are removed. Cream/tan folds follow the bag axis.

Body/head/legs/hands, other10frames, palette, layer metadata and timing are exact
against the starting full-attack-repair candidate. Only the two bag/tension owners
changed in F8–F10. Three-frame duration420ms; full sequence13frames/1680ms,320×192.

## New workflow exercised before presentation

[Plan](plan.md) and [scope/sites](scope.json) were written before native edits.
Actual reference close-up/neutral and owner-isolated/hidden baseline images were
opened. Required relationships cover both strap ends, near/far rim and fabric,
hand occlusion, bag proportions and neighboring-pose continuity. Character anatomy
uses exact cel protection; no rescaling or layer-bound proxy was used.

The guide hypothesis uses24×26local bag body,17pxgrip-to-mouth drop and common
near/far roots. F8/F9/F10 rotate43°/17°/10° about their existing grip locations.
These are authored geometry inputs, not a physical-volume score. The far roots
are inferred behind the rim; guide sites mark the chosen construction explicitly.

| Checkpoint | Observed result / decision |
| --- | --- |
| Baseline | Owners show incompatible fork-like handle ends and sloped bag surface; repair connected object. |
| Structural pass01 | Simple planes rendered through MCP; primary sees leftover F8 pixels at x217–218 beyond initial replacement region. Reject that cleanup state. |
| Structural pass02 | Scope expanded to contain complete old prop (same authorized bag repair), remnant removed. New source and initial scope/pass preserved. Exact body/other-frame checks pass. |
| Independent structural review | Fresh read-only global_reviewer verifies candidate hash, opens actual owner/neighbor/guide evidence, traces near/far roots and clears proportions, attachment and F8–F10 continuity for detail. |
| Detail | Sparse fabric folds added; zero alpha changes versus cleared structural pass, rear loops identical.66/84/64opaque tote pixels recolored in F8/F9/F10. |
| Independent final review | Same reviewer continues its own task with final evidence; finds no blocking attachment/proportion/angle/style regression. Primary also opens final clean/comparison/owner exports. Candidate may be presented. |

The reviewer received task, locks, images and structural questions before the
producer's success verdict. It did not edit. [Manual review](review/manual-review.json)
binds the actual comparison-packet and native hashes. This trial demonstrates the
new checkpoint used in a real repair, including a caught cleanup defect. It does
not establish a general model accuracy rate or guaranteed future detection.

## Observed checks

- Dedicated MCP Pebbly0.8.2/headless Aseprite1.3.18.6-dev ready; doctor inventory,
  actual native state and ASCII regions inspected. Existing session drawing smoke
  evidence retained from earlier work; no new full two-layer smoke suite claimed.
  Native edits/saves/reopens/exports used dedicated MCP only. Python prepares literal
  grids and packages/reads evidence, never writes native sources.
- [Scope check](review/final-checks.json):6changed cels, all inside named masks,
  all other cels exact; layer/cel inventory, non-cel chunks, timing and palette exact.
- [Verification](review/verification.json): all13native composites equal dedicated
  PNG exports and fresh-MCP reopen sheet; binary alpha, no colors outside base used
  palette. Both GIF timelines match exact native pixels/timing. Initial RGB-to-GIF
  quantization failed exact comparison; replaced by exact shared palette indices
  and reran successfully. This was packaging, not an art edit.
- [Local revision proof](review/local-revision-and-detail.json): duplicate-only
  F9pixel(166,112) changes on tote owner; every other cel/pixel exact; fresh reopen
  PNG matches. Proof never replaces candidate.
- Existing comparison build/verify: complete/fresh mechanical packet; visual/user
  approval fields remain pending as designed. Independent manual decision is separate.
- [Preservation](review/preservation.json):1343pre-existing protected files unchanged.
  Original candidate hash remains5fb9a4f7…; source operations and all rejected attempts
  retained. Literal [final replay inputs](replay-plan.json) retained; a complete fresh
  rebuild was not run. All task-owned native documents closed after proof.
- MCP advertises validate but exposes no callable validate tool; independent actual
  checks above used. No built-in validation success is claimed.

## Limits and next owner

F7/F11 were inspected as unchanged context. F7→F8 is a large catch/rotation and
F10→F11 a regrip/re-shoulder transition. Exact named root correspondence for those
outer poses was not reconstructed; full-animation smoothness is not cleared.
The looping F7–F11 context GIF has an artificial F11→F7 replay seam; use full-cycle
GIF for overall context. Continuous temporal perception and new Godot gameplay
validation were not performed. No production replacement, installation, publication
or commit. Work remains local at HEAD9e35c5c13987a153e942e6f93f49f247fad13c3a.

Changed only this experiment and the handoff. User next reviews this exact repair
for visual acceptance; agent owns further corrections if requested. The original
whole-cycle artistic approval remains pending.
