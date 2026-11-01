# Luna 5.6 Max full-body one-shot trial

- Status: observed; rejected for the frozen scope; user selection pending
- Date: 2026-10-30
- Intent: bounded model comparison / one native finishing pass
- Baseline: frozen `docs/experiments/2026-10-30-fullbody-automated-reconstruction/passes/candidate-b-structured.aseprite`
- Trial directory: `docs/experiments/2026-10-30-luna-fullbody-once/trial-a/`
- Candidate native master: `outputs/luna56-fullbody-cleanup.aseprite`
- Candidate runtime export: `outputs/luna56-fullbody-cleanup.png`
- Fresh-reopen export: `outputs/luna56-fullbody-cleanup-reopen.png`

## Acceptance against this trial's scope

| Criterion | Evidence | Result |
| --- | --- | --- |
| One bounded artistic attempt | `operations.md`; eight batched layer calls; no mouth call | Pass — one art pass |
| Meaningful visible whole-character cleanup | 282 composite pixel changes across hair, jacket, shirt, tote/strap, denim and shoes; comparison sheets | Visual change observed, but **scope fail** because 43 writes added opaque pixels where the frozen baseline was transparent; no eligible cleanup selection |
| Preserve canvas/palette/alpha/pose/eyes/mouth | fresh-export alpha diff in `alpha-audit.json`; mouth left unchanged | **Fail** — alpha is binary but the protected baseline alpha mask was not preserved |
| Native editable source | reopened 12-layer Aseprite source | Pass |
| Native PNG export | `outputs/luna56-fullbody-cleanup.png` | Pass |
| Independent fresh reopen/export | `outputs/luna56-fullbody-cleanup-reopen.png` equals first export | Pass |
| Original/reference unchanged | frozen-copy hashes equal authoritative originals; see `verification.json` | Pass |
| Gameplay/Godot validation | none in this trial | Not tested |

## Pass and selection ledger

| Checkpoint | Change hypothesis | Technical result | Visual decision |
| --- | --- | --- | --- |
| Frozen baseline `candidate-b-structured` | Finish whole-character material clusters while protecting restrained face expression | 128×192, 12 layers, 1 frame, 255 palette, binary alpha | Eligible baseline; not user-approved |
| `luna56-fullbody-cleanup` | Hair/clothing/tote/shoes cleanup in one bounded pass | 282 composite pixels changed; fresh reopen is exact; **43 alpha additions, 0 removals** versus frozen baseline | Rejected for the frozen scope. Retain as the last attempted artifact only; it is not an eligible cleanup candidate |
| Reopened `luna56-fullbody-cleanup` | Verify save/export durability | Reopened native source exports byte-identically to first candidate PNG | Technical proof only; not another art pass |

## Per-region decision

The candidate shows visible cluster changes in hair, jacket/shirt, tote/strap, denim and shoes, but it is not eligible for selection because the pass added opaque pixels outside the frozen baseline alpha mask. The frozen baseline is the best eligible artifact for this scope. Baseline/candidate tie for mouth; no face winner is claimed. No artifact is marked user-approved.

## Next owner/action

Parent agent should present the comparison sheets as a **failed bounded attempt**, with the baseline retained as the best eligible artifact. Do not perform an automatic correction round under this one-shot budget. A future separately authorized pass must apply a hard baseline alpha/silhouette mask before drawing, then re-run the alpha audit before any visual selection. Godot preview remains a later boundary.

