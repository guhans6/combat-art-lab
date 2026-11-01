# Aseprite-drawn street background

This environment is drawn from authored pixel geometry and structured plant branches in `draw-background.lua`. The original street image was a visual reference only. No background raster, image-generation output, reference pixels, blur filter or external asset is loaded by the drawing source. The only image-bearing input is the existing v04 native character, which is copied unchanged.

- `background.aseprite`: 16 independently editable environment layers.
- `street-scene.aseprite`: those layers, a separate ground shadow, and all 12 unchanged v04 character layers (29 layers total).
- `background-lamp-edit-test.aseprite`: separate local-edit proof; main scene keeps its original warm lighting.
- `background-pass01.aseprite`: earlier drawn pass retained for comparison.

The 352x264 grid and character offset (84,61) match the previous placement preview. Exports are under `assets/export/street-drawn-v01`; previews are 4x nearest-neighbor. This is a simplified drawn interpretation, not an exact reconstruction of every reference detail. User visual acceptance is pending.

From the repository root:

```sh
/Applications/Aseprite.app/Contents/MacOS/aseprite --batch \
  --script-param root="$PWD" --script "$PWD/assets/source/street-drawn-v01/draw-background.lua"

/Applications/Aseprite.app/Contents/MacOS/aseprite --batch \
  --script-param root="$PWD" --script "$PWD/assets/source/street-drawn-v01/inspect-and-revise.lua"

/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  assets/source/street-drawn-v01/verify-and-preview.py
```

Output directories under `assets/source/street-drawn-v01`, `assets/export/street-drawn-v01`, `assets/previews/street-drawn-v01/layers` and `docs/experiments/2026-10-26-drawn-background` must exist. The Python command uses the existing bundled Pillow runtime for image checks and presentation layouts only; all environment pixels are drawn by the Aseprite Lua source.

Fresh rebuild was additionally tested in an isolated ignored folder containing only the native character input. Background and combined-scene PNG bytes matched exactly. No Godot playback, motion, public release or installation is implied. [Evidence record](../../../docs/experiments/2026-10-26-drawn-background/record.md).
