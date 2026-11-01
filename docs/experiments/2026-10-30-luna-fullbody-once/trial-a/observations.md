# Observations

## Frozen inputs

The actual approved originals were opened visually before drawing:

- `inputs/character-scene.png`: 1448×1086 full scene; the character has a tall relaxed stance, right-facing three-quarter head, tied brown hair with a loose fringe, olive open jacket, light shirt, wide blue jeans, pale shoes and cream tote. Warm shop light contrasts with cooler distance.
- `inputs/character-closeup.png`: 1448×1086 close-up; unequal near/far eyes and rightward gaze are visible, as are the broken fringe, tied bun/loose curls and restrained shallow smile.
- `inputs/source-only-converted-seed.png`: 128×192 source-only converted seed. It preserves the broad character arrangement but has soft/weakly articulated clusters; it is provenance, not a selected asset.
- `inputs/baseline-reopen.png`: 128×192 native baseline export, reviewed at 1× and nearest-neighbor integer zoom. It is the eligible starting point for this bounded finishing task.

The full-body and head comparison sheets show the reference, baseline and actual candidate together:

- `comparisons/fullbody-1x-reference-baseline-candidate.png`
- `comparisons/fullbody-4x-reference-baseline-candidate.png`
- `comparisons/head-1x-reference-baseline-candidate.png`
- `comparisons/head-2x-reference-baseline-candidate.png`

Reference panels are explicitly labeled resized preview crops; baseline/candidate panels are native 1× or nearest-neighbor integer zooms. This is a visual diagnostic, not gameplay-scale proof.

## Technical scope audit

The candidate PNG and its independently reopened export were compared pixel-for-pixel with the frozen baseline. The candidate remains binary-alpha and has the same outer visible bounding box, but that is insufficient protection: there are **43 alpha changes**, all `transparent → opaque`, with no removals. These are internal/edge mask violations, including the explicitly observed hair points `(54,6)`, `(46,7)`, `(51,7)`, `(42,8)`, `(40,23)`, `(38,26)`, and `(41,27)`, plus additional hair, jacket, tote, denim and shoe-edge points listed in `alpha-audit.json`.

Cause is provable from the recorded operations: the pixel batches wrote opaque colors at coordinates whose baseline composite alpha was transparent. No hard baseline alpha/silhouette mask or pre-write alpha check clipped those points. The Aseprite save/reopen path is not the cause; the fresh-reopen PNG is byte-identical to the first candidate export. This makes the candidate a valid preserved experiment artifact but a **failed frozen-scope attempt**, not an eligible cleanup result.

## Visual review

| Region | Observed change | Agent judgment | Selection / approval |
| --- | --- | --- | --- |
| Hair / bun / fringe | More connected crown and bun cluster rhythm is visible, but 11 new opaque pixels were written onto transparent baseline cells | Visual effect observed, but candidate is ineligible for this protected pass; baseline is the best eligible artifact | None selected; user pending; no user approval |
| Jacket | Added hood/lapel and sleeve/hem planes, with 4 alpha additions in the audited region | Visual effect observed, but candidate is ineligible for this protected pass | None selected; user pending; no user approval |
| Shirt | Added a small fold rhythm; no alpha additions in the shirt audit region | Local visual change observed, but whole candidate fails the shared alpha gate | None selected; user pending; no user approval |
| Tote / strap | Added tote edge/fold accents, including 4 new opaque tote-edge pixels | Visual effect observed, but candidate is ineligible for this protected pass | None selected; user pending; no user approval |
| Denim | Added crease clusters, including 4 audited alpha additions in/near the tote/denim region | Visual effect observed, but candidate is ineligible for this protected pass | None selected; user pending; no user approval |
| Shoes | Lace/upper highlights and dark soles read more clearly, but 22 opaque edge additions changed the protected alpha mask | Visual effect observed, but candidate is ineligible for this protected pass | None selected; user pending; no user approval |
| Eyes / face orientation | No direct face-layer edit; existing near/far eye relationship and rightward gaze were preserved | Baseline and candidate remain the same eligible face treatment except nearby hair accents; no new face winner established | None selected for identity; user pending |
| Mouth / expression | Mouth intentionally unchanged to preserve the original shallow smile and avoid the rejected pout/U/dotted treatment | Baseline/candidate tie for mouth; no correction claimed | None selected; explicit user identity veto remains active; user pending |
| Whole character | Candidate has visible changes across several requested material regions, but fails the protected alpha/silhouette constraint and remains simpler than the authoritative concept | Last attempted artifact only; frozen baseline remains best eligible | **None selected**; user visual approval pending |

## Limits

No Godot preview, gameplay-scale test, motion test, attack/contact test, strict binary/header audit, or user visual approval was performed. The candidate is not a production-approved sprite and fails the frozen alpha/silhouette scope gate. The head/face remains the largest unresolved likeness risk, and the user—not this agent—selects the artistic result.

