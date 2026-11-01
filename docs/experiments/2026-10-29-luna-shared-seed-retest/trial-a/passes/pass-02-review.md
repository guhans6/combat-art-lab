# Pass-02 gate review

## Decision

Pass-02 is the first eligible exported candidate and is released for
defect-only supervisor review. It starts from the verified raw seed, uses one
named face-correction layer, and makes the intended eight-pixel bounded face
change in the actual PNG. Pass-01 remains rejected and is not used as a
baseline.

## Export-path proof

Before the art repair, one pixel at `(64,21)` was applied inside the face mask
and exported as `passes/pass-02-tech-proof.png`. The proof PNG differed from the
raw seed at exactly one decoded pixel, proving that this fresh native/layer route
reaches the export. The remaining seven bounded pixels were then applied in one
batch.

## Candidate evidence

- Native source: `passes/pass-02.aseprite`, saved from the raw baseline and
  reopened through the same MCP route.
- Candidate PNG: `passes/pass-02.png`, 128×192, 8-bit RGBA.
- Candidate PNG SHA-256:
  `fd221d8a2d411b985e257dbdfb327e8c1437b5bb7f23d9b8a9532ef5e5d2cb9f`.
- Candidate decoded RGBA SHA-256:
  `5c6533d48ed388fd44295a70848b02693d74a3f2231cf844c4d14bf6bcce0d97`.
- Exactly eight decoded pixels differ from the shared raw seed; all lie within
  `M-face-expression` (`x=54..83,y=19..48`). No palette snapping or off-palette
  colours were reported.
- Reopen export `passes/pass-02-reopen.png` has the same file SHA-256 and
  decoded RGBA as the candidate export.
- Nearest-neighbor visual evidence: `evidence/pass-02-4x.png` and
  `evidence/pass-02-head-16x.png`; the full-body silhouette, costume, hair/tie,
  tote, shoes and framing remain unchanged by the declared mask.

## Visual boundary

The face change is deliberately minimal: two small eye-value/pupil corrections
and a restrained three-pixel mouth mark, all in the declared face mask. This is
an exported candidate, not user-approved final art. Godot playback, animation,
publication and user visual approval remain unperformed.
