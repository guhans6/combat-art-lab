# Generated-seed mouth readability pass

## Purpose

Make the mouth of the generated-cutout 128×192 conversion visible without
redrawing its face or disturbing the preceding 14-pixel denim cleanup.

## Frozen inputs

- Baseline: `inputs/baseline-denim-cleaned.png` (SHA-256 in `evidence/checks.json`).
- Supporting visual source: `inputs/generated-clean-source.png`.
- The baseline already includes the separate denim cleanup. This pass does not
  change any of those pixels.

## Scoped construction

The sole editable rectangle was x=68..71, y=26..29. Everything outside it is
pixel-locked: eyes, brows, nose, jaw/cheeks, hair/tie, silhouette, body,
denim, canvas, and alpha. The final shallow smile retains the existing warm
pixel at (68,27) and adds a two-pixel darker lower stroke at (69,28) and
(70,28). Exact old/new RGBA values are in `evidence/change-ledger.json`.

The result is intentionally a small shallow curve rather than a grin or a
feature redesign. It becomes visible in the 1× panel and is legible in the
nearest-neighbour face crop.

## Native/editability and checks

`outputs/candidate-mouth.aseprite` is a native, one-layer, 128×192 RGB
Aseprite document saved from the 14-denim baseline. It was reopened in a fresh
headless Aseprite document and exported again. `evidence/checks.json` records
the source hashes, three actual changed pixels, zero alpha changes, zero
out-of-scope changes, and RGBA equality between the candidate and reopened
export.

## Review artifact

See `evidence/before-after-mouth.png`: baseline/candidate at actual 1× and
nearest 4×, tight face crops, and the isolated three-pixel change mask.

## Boundary

This is an editable local candidate, not a promoted gameplay asset or motion
test. The generated source's identity drift remains inherited context and was
not addressed by this narrow mouth pass.
