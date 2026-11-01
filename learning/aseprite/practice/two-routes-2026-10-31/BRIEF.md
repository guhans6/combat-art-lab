# Six-pose automatic draft preparation

These are byte-identical copies of the user's six supplied pose PNGs.  The rebuild
recipe makes a fixed 128×128, shared-palette draft grid for later bulk painting in a
native Aseprite document.  It applies one common transform and alpha threshold; it
does not fit poses individually or delete pixels by RGB hue.

This is preparation for the simplified beginner route, not a drawing correction.
The automatic draft may retain colored opaque edge artifacts.  The native art layer
starts blank and the user may clean it up later; the payload grid is a separate
automatic draft/reference layer.

Scope: six pose-study keys (`neutral`, `straplift`, `grip`, `windup`, `swing`,
`recovery`) with the durations in `manifest.json`.  This is not a complete attack,
does not provide inbetweens, and is not game or visual approval.

Study budget: one preparation pass and, only if the fixed parameters prove wrong,
one parameter repair.  Re-run `rebuild/prepare_payloads.py` from this directory to
recreate JSON payloads.  The recipe deliberately emits no PNG, GIF, sprite, or
native Aseprite file.  A parent/native-export check can rebuild RGBA bytes from a
painted export and compare its SHA-256 against each frame's
`draft_pixel_hash_canonical_rgba_sha256` in `manifest.json`.
