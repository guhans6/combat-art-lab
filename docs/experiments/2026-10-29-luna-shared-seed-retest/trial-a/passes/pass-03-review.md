# Pass-03 final-pass review

## Decision

Pass-03 is the best available authored local-correction candidate and is
released for user visual approval. It is not claimed as a completed multi-part
production master. It keeps pass-02 as the prior candidate, adds only a
coherent three-pixel extension to the mouth cluster, and preserves the raw seed
layer, pose, hair/tie, costume, palette, binary alpha and framing.

## Candidate evidence

- Native: `passes/pass-03.aseprite`.
- Export: `passes/pass-03.png`, 128×192 RGBA.
- PNG SHA-256:
  `c6de338361498495d2e634f4c377d3f7e281dee9050371f94c2d1d4f36c91aee`.
- Decoded RGBA SHA-256:
  `cb5864a4f0862d132d0ef51c9f9dcb38e24649abab9e7ff58ee4c909db94d52e`.
- Exactly 11 pixels differ from the raw seed; exactly 3 differ from pass-02.
  All changes are inside `M-face-expression`.
- New smile layer pixels use existing palette colour `#542a1e` at `(67,30)`,
  `(70,30)`, `(71,29)`. The resulting short shallow arc is visible in the
  native-scale face crop and remains deliberately restrained.
- Matched visual comparison:
  `evidence/matched-head-comparison.png`, with panel order documented in
  `evidence/matched-head-comparison.md` as approved reference, raw seed, best
  pass-02 and new pass-03.
- Direct fresh reopen proof: after closing the editing document, the saved
  native was reopened as a new MCP document and exported to
  `passes/pass-03-reopen.png`. It matches `passes/pass-03.png` byte-for-byte
  and by decoded RGBA.

## Required duplicate proof

`passes/pass-03-proof-duplicate.aseprite` and
`passes/pass-03-proof-duplicate.png` are retained separately. The duplicate
received one useful localized smile extension at `(66,30)` and its PNG differs
from the selected pass-03 export at exactly one pixel. The selected master PNG
remained hash-stable, and a protected `shared-source-seed` readback on the
duplicate remained unchanged. The duplicate was closed and is not a candidate.

## Selected-vs-last ledger

| Role | Artifact | Status |
| --- | --- | --- |
| raw fallback | `input/shared-source-seed-baseline.aseprite` / `input/source-only-converted-seed.png` | preserved; no user approval |
| best prior | `passes/pass-02.aseprite` / `passes/pass-02.png` | superseded by pass-03 for mouth readability |
| selected authored candidate | `passes/pass-03.aseprite` / `passes/pass-03.png` | best available local correction; awaiting user visual approval |
| last technical attempt | `passes/pass-03-proof-duplicate.aseprite` / `passes/pass-03-proof-duplicate.png` | duplicate-only one-pixel proof; not selected |

Editor calls ended at `97/120`; all three allowed art passes were used. The
selected candidate and its fresh reopen export agree exactly. No further art
pass is authorized in this trial.

## Remaining boundaries

No Godot preview, animation playback, user visual approval or publication was
performed. The candidate is released for review, not claimed as final approved
game art.
