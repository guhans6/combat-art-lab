# Generated-seed cleanup

This is a separate native cleanup candidate for the generated-cutout conversion seed
at 128×192. The approved originals and earlier candidates are unchanged. The full
head/hair block `(19,7)-(78,82)` is locked, and a stronger pixel check rejects every
change outside the declared interior-denim coordinates. Face, expression, ears, hair,
pose, silhouette and all alpha values remain unchanged.

The retained candidate makes 14 existing-palette interior denim changes: two near the
fly and two short fold clusters on each leg. It is an editable one-layer Aseprite
source because the conversion input was flat; it does not claim semantic full-body
layers or animation readiness. Save, reopen and export preserve decoded RGBA pixels.

At 4× the folds group more clearly. At actual size the change is subtle, so this is
not an art promotion. The generated source's eye, smile, hair and shading changes are
inherited from image generation and were not altered by this cleanup.

[Before/after](evidence/before-after-cleanup.png) shows the source, actual-size
baseline/candidate, 4× views and the change mask. The exact old/new pixels are in
[change-ledger.json](evidence/change-ledger.json); rejected attempts are retained in
[rejected-pass-summary.json](evidence/rejected-pass-summary.json). Run
`uv run --with pillow python scripts/verify.py` here for read-only verification.

No motion, Godot playback, source-layer reconstruction, user approval, commit, push,
or publication was performed.
