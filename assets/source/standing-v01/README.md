# Standing reconstruction v01

This is an agent-drawn candidate based on the user's finalized original character. It is **not exact** and awaits visual approval. `standing.aseprite` is the main editable file; the tote-color revision is a separate editability test. No animation, rig, or Godot playback has been validated.

The native file contains named hair-back, tote-body, jeans, sneakers, skin-face, tee, jacket, hands, tote-strap, hair-front, face-features, and hidden ground-guide layers. The source uses authored polygons/pixel lines with a named RGB palette, not an imported reference bitmap. Native canvas: 128x192, feet/ground anchor y186; provisional until actual game-scale review.

## Reproduce with the installed app

From the repository root:

```sh
/Applications/Aseprite.app/Contents/MacOS/aseprite --batch \
  --script-param root="$PWD" --script "$PWD/assets/source/standing-v01/draw.lua"

/Applications/Aseprite.app/Contents/MacOS/aseprite --batch \
  --script-param root="$PWD" --script "$PWD/assets/source/standing-v01/verify-and-revise.lua"

/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  assets/source/standing-v01/preview-and-check.py
```

Required output folders already exist in this workspace. On a fresh checkout, create `assets/source/standing-v01`, `assets/export/standing-v01`, `assets/previews/standing-v01/layers`, and `docs/experiments/2026-10-26-standing-reconstruction` before running. The preview script uses Pillow from the existing bundled runtime and a system Arial font; it draws only labels/comparison layouts, not character pixels. Aseprite execution may require the host's normal execution approval. No UI automation is used.

`draw-pass01.lua` and the corresponding `standing-pass01` files preserve the earlier drawing before contrast/neckline refinement. Use `draw.lua` for the current candidate.

Approved references are under `assets/references/approved-2026-10-26`. The unchanged source reference is used only by the preview/analysis script. Any reduction/alpha cleanup there is explicitly for the comparison panels, not asset construction.

See the [experiment record](../../../docs/experiments/2026-10-26-standing-reconstruction/record.md) for checks, sources, artifact hashes and fidelity limits.
