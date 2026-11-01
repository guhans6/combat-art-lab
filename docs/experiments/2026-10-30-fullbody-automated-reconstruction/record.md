# Full-body automated reconstruction

- Status: observed; awaiting user visual selection
- Date: 30 October 2026
- Question: can a deterministic whole-character initialization be organized into
  meaningful editable visible parts, then reviewed and corrected without changing
  the frozen seed recipe?
- Intent: assisted reconstruction method experiment; not a production replacement.
- Control: 128×192 frozen source-only seed, binary alpha, existing 255-entry palette.
- Pass budget: automatic initialization, initial whole-character finish, then at
  most two corrective passes after defect-only review.

## Frozen inputs and roles

| Input | Role | SHA-256 |
| --- | --- | --- |
| `inputs/source-only-converted-seed.png` | Control A / automatic sample source | `074168d9bfc5b2a2f2751810152bb0c31a71e7027a5368c0b393e17449fb84eb` |
| `inputs/source-seed-baseline.aseprite` | Frozen native palette/source fixture | `b1d91f6f87f650cbd2cae3edb69704d195bbdcf8d6b679b287d01e8a7283cc19` |
| `inputs/character-scene.png` | Authoritative identity, silhouette, outfit | `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae` |
| `inputs/character-closeup.png` | Authoritative face/expression/hair | `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7` |
| `inputs/clean-generated-cutout-v1.png` | Supporting geometry only | `12e971cc9e3cbfa7add2a17a62ff53d1f45b3c55197ce23c336a6447bed1f49e` |

## Initial visual audit

The fullbody control retains the tied brown hair, right-facing open-eyed expression,
olive open jacket, cream tee/tote, loose blue denim and pale shoes. The clearest
review targets are the fine, noisy hair fringe/pony-tail edges, the facial eye/mouth
clusters, jacket sleeve planes, denim fold density, shoe structure and tote/strap
silhouette. These observations do not yet establish a needed change; the canonical
scene and closeup remain the authorities.

## Current checkpoint

No original or prior experiment artifact was modified. The first ownership recipe was
rejected: it used a misread Y origin and assigned the tote only 20 visible pixels.
`automatic-fullbody-structured-v2.*` remains diagnostic evidence only. The corrected
recipe uses a coordinate-overlay review and has no residual/guide layer: 11 visible
semantic parts cover all 7,844 visible pixels, with 581 declared nearest-owner
boundary completions. The largest ownership counts are denim 3,703, hair 1,030,
shoes 708, shirt 593, jacket-left 514, tote 384 and jacket-right 287.

## Checkpoints and selection

| Checkpoint | Result | Decision |
| --- | --- | --- |
| `passes/automatic-fullbody-structured-v2.*` | Visible composite exact, but ownership review failed; tote had 20 pixels and upper-body parts were materially crossed. | Rejected structural control; preserved. |
| `passes/pass-01-fullbody-finish.*` | Broad face/hair/jacket/denim/tote/shoe edits were exported. Review sheet shows the tote edge and denim stripe became too assertive and the mouth read as separated dark marks. | Rejected artistic pass; preserved. |
| `passes/candidate-b-structured.aseprite` / `.png` | Fresh deterministic rebuild with corrected ownership. Full native reopen retains 12 layers and its reopen PNG is byte-identical to the original export. | Best retained native candidate; it is a structured full-character still, not a claimed likeness improvement. |

**Selection summary:** candidate B is preferred for its whole-character visible-part
organization and technical evidence. The seed remains visually unchanged by candidate
B; no artistic improvement is claimed. User approval is pending.

## Native and rebuild evidence

- `rebuild/prepare_parts.py` is the frozen deterministic ownership/reassembly input;
  `masks/ownership-manifest.json` records precedence, polygons, coverage and inferred
  boundary counts. `masks/ownership-review-4x.png` and the individual part PNGs are
  the isolated-part review evidence.
- Each part was bulk-painted through the authorized headless Aseprite MCP into a
  fresh 128×192 RGB document with the fixture's 255-colour palette. The hidden,
  locked `guide-source-seed (hidden)` is excluded from the visible composite.
- Candidate B native SHA-256: `b096b209d41790f81acdb61a0ba908b37b31596bb73d03f9c4d5ec3ac88a062d`.
  Its first and freshly reopened PNGs have SHA-256
  `b3ad887bf2acff2e71404c78d6fc7260784f51f842e6f19d3bd4986777bbf34a`.
- The seed/candidate alpha differs at zero pixels and visible RGBA differs at zero
  pixels. 13,352 fully transparent hidden-RGB values normalize on Aseprite export;
  this is explicitly not visible/composite drift.
- A two-layer 16×16 scratch `proof/scratch-two-layer.aseprite` save/reopen passed.
  Saving an already-saved mutated headless document instead persisted a one-layer
  source; saving *after construction* to a new target was the proven workaround.

## Localized edit and diagnostic isolation

`proof/candidate-b-tote-accent-edit.aseprite` is the duplicate-only useful-feature
proof source. It changes exactly eight visible composite pixels at `(86,82)`,
`(87,82)`, `(88,83)`, `(89,83)`, `(87,84)`, `(88,84)`, `(89,85)`, and `(90,85)` on
`04-tote`, forming one small existing-palette tote highlight plane; the source
candidate's native SHA is unchanged. The proof reopens with 12 layers, and its
first/reopen PNGs are byte-identical. Hiding `04-tote` in a throwaway reopened candidate visibly exposes the bag
void and lower strap/hand overlap; that diagnostic is expected because the source
has no hidden-surface information. It is labelled evidence of a still's visible-part
organization, not rig/animation readiness.

## Per-region visual review

| Region | Observation against originals | Candidate B status |
| --- | --- | --- |
| Face/expression | Seed retains right-facing gaze but underarticulates lid and shallow friendly smile. | Unchanged; user review required. |
| Hair/tie | Tied silhouette survives; crown/fringe remain noisy versus broad swept reference masses. | Unchanged; pass-01 cleanup rejected. |
| Jacket/tee | Olive/cream material planes and open-jacket silhouette read; fine accents remain busy. | Structured left/right/tee parts; no accepted redraw. |
| Denim | Wide-leg silhouette and blue material are clear; folds remain dense. | Structured; strong added crease rejected. |
| Shoes | Shape and pale contrast read, but laces are noisy. | Structured; no accepted cleanup. |
| Tote/strap | Cream tote, strap, and hand overlap are readable in separate visible parts. | Structured; flatness remains a visual limitation. |
| Silhouette | Stance, tote side and tied-hair mass remain stable. | Preserved exactly from control. |

## Evidence boundary and next owner

`reviews/fullbody-1x-seed-automatic-finish.png`,
`reviews/fullbody-4x-all-candidates.png`, `reviews/head-1x-seed-automatic-finish.png`,
and `reviews/head-16x-all-candidates.png` retain actual exports. The two authoritative
preview crops are comparison-only because framing differs. No animation, hidden
surfaces, Godot preview, gameplay-scale validation, production readiness, publication
or user visual approval was tested/claimed. Next owner: user to select/reject the
retained still; a later artist may use the named visual limitations for a separately
approved reconstruction pass.
