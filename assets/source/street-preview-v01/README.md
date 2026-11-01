# Static street placement preview

`street-scene.aseprite` contains a flat clean-background layer, separate ground shadow, and all 12 v04 character layers. Character pixels and layer structure are preserved, translated by (84,61) into a 352x264 scene. The hidden character guide remains hidden. Native exported scene and 4x nearest-neighbor preview are separate files.

The background was cleaned from the user's original scene with one built-in imagegen edit. Original figure/occluded scenery removal is generative; background pixels are not claimed identical to the reference. `background-clean-generated.png` and the exact edit prompt are preserved. This is an imported raster plate, not a hand-constructed layered environment. No generation or repainting touched v04.

From the repository root:

```sh
/Applications/Aseprite.app/Contents/MacOS/aseprite --batch \
  --script-param root="$PWD" --script "$PWD/assets/source/street-preview-v01/build-scene.lua"

/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  assets/source/street-preview-v01/verify-scene.py
```

Output directories under `assets/source/street-preview-v01`, `assets/export/street-preview-v01`, `assets/previews/street-preview-v01` and `docs/experiments/2026-10-26-street-preview` must exist. Rebuild is deterministic from the saved plate and native v04 source; the original image-generation result itself is not claimed reproducible byte-for-byte.

No Godot scene, camera, movement or animation was run. This is a static appearance/placement preview, pending user review. [Evidence record](../../../docs/experiments/2026-10-26-street-preview/record.md).
