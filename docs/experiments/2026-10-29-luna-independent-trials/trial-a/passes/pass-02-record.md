# Pass 02 record

## Artifacts

- Native corrected source: `passes/pass-02.aseprite`
  - SHA-256: `be50bfa634c6acceb671b4a7e8d60280d5ccad4d4a83334ccac675156e770bef`
- Transparent corrected export: `passes/pass-02.png`
  - SHA-256: `d06e147c21cc3fc09b04d9ca2fe56c7510c287ef01e00e63a719a7bf448f5a30`
- Fresh reopen export: `passes/pass-02-reopen.png`
  - SHA-256: `d06e147c21cc3fc09b04d9ca2fe56c7510c287ef01e00e63a719a7bf448f5a30`
- Corrected source/candidate v2 review sheets:
  `passes/pass-02-review-v2-source-vs-candidate-white-4x.png`,
  `passes/pass-02-review-v2-source-vs-candidate-magenta-4x.png`, and
  `passes/pass-02-review-v2-source-vs-candidate-alpha-4x.png`.

## Correction

Pass 02 preserves pass 01's framing, pose, costume and broad material palette. On
the authored `hair-face` overlay it removes the two added bright eye-white pixels,
erases the diagonal cheek-like three-pixel smile, mutes the near-eye highlight,
and redraws a shorter shallow warm three-pixel smile inside the face plane. The
result is less blocky and no longer reads as a diagonal cheek mark at 8x review.
No body, tote, leg gap, shoe, or hair-tie silhouette was redrawn.

## Reopen/export proof

The saved native source was closed and reopened as a fresh document. Its export is
byte-identical to the pass-02 export (`cmp` exit 0 and matching SHA-256). The
reopened source reports 128x192 RGB, one frame, 12 layers, 255 palette entries,
and the hidden locked `reference` layer.

## Duplicate localized-edit proof

Pass 02 was opened as a separate document. A two-pixel pale tote accent was added
only on the empty `tote-shoes` overlay, with the backend snapping the requested
`#f9d5b5` to the existing `#fcd8b6` palette entry (DeltaE 1.41). The duplicate was
saved and exported without overwriting pass 02:

- `passes/pass-02-local-edit.aseprite`
  - SHA-256: `337d7b022a77311c49900cd1de49b0ddbd5d668e218a9fcadb77f23bf699ae4b`
- `passes/pass-02-local-edit.png`
  - SHA-256: `ed8074605074ef4f5d2c7a1a62134fe21c73f0902d7378e96017b8c99b60796b`

Structured `read_pixels` comparisons between the untouched pass-02 document and
the duplicate found equality for every converted raster layer: `converted-seed`,
`hair-face-raster`, `jacket-shirt-raster`, `jeans-raster`, and
`tote-shoes-raster` (128x192, zero differences each). The changed overlay is
isolated to `tote-shoes`. This proves a useful local edit and protected raster
preservation, not full animation-rig readiness.

## Appearance observations

- The smile now reads as a restrained short line rather than a diagonal cheek mark.
- Near/far eye whites are less artificially bright; the unequal clusters and
  rightward face turn remain visible at 4x, with native-size readability still
  subject to supervisor/user judgment.
- Pose, costume, long-leg proportions, tote attachment, intentional leg gap, and
  shoe grounding are unchanged from pass 01.
- Hair and garment contours remain source-derived and stepped; some irregular
  sampled clusters remain an honest limitation for a possible later craft pass.
- The v2 alpha bbox is measured and retained, but supervisor review found that the
  magenta and white comparison presentations still appear to omit materially
  different character/source regions. Full coverage is therefore unproven and is
  recorded as an unresolved evidence defect. No Godot/runtime/user-approval claim
  is made.

## Technical note

One export call initially used an incorrect sibling `passes/` path; the resulting
file was immediately moved into this assigned `trial-a/passes/` directory and the
correct hash/equality checks were rerun. No peer or shared artifact was read or
modified.

## Boundary

Pass 02 and its proof artifacts are retained. Supervisor-tracked editor usage is
116/120, leaving four calls; the slot is released now for defect-only review.
