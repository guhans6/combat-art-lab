# Standing v03: head-only correction

Main file: `standing.aseprite`. Base: unchanged v02 native master. v01/v02 are preserved. Only the existing hair-back, skin-face, hair-front and face-feature layers are edited, inside an enforced head mask. The neck notch and all rows from y31 downward remain identical to v02. There are no new palette colors or canvas changes.

From the repository root:

```sh
/Applications/Aseprite.app/Contents/MacOS/aseprite --batch \
  --script-param root="$PWD" --script "$PWD/assets/source/standing-v03/edit-head.lua"

/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  assets/source/standing-v03/compare-and-check.py
```

Output directories under `assets/source/standing-v03`, `assets/export/standing-v03`, `assets/previews/standing-v03/layers` and `docs/experiments/2026-10-26-head-v03` must exist. The comparison/check script uses existing bundled Pillow and a system Arial font; it creates labeled layouts only, not sprite pixels.

The first command opens v02, edits allowed head pixels, saves/reopens v03 and exports each actual native layer. The second verifies original-version hashes, every changed pixel's location, unchanged neck/body, retained palette, separate eye landmarks and exact reopened export. Prior baseline hashes must exist from the recorded first run.

The head comparison uses a 384x256 crop of the original and 48x32 sprite crops at equivalent display sizes. Only previews are enlarged. No blur, smoothing, reference raster transfer, GUI automation or generation service is used.

This version awaits user visual acceptance. [Experiment record](../../../docs/experiments/2026-10-26-head-v03/record.md).
