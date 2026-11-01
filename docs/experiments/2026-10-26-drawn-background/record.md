# Native drawn street background

- Date: 26 October 2026
- Request: “Please use Aseprite to draw those background too so the style would be same now it looks odd.” User rejected the previous flat background placement as a style mismatch and requested native drawing. Preserve character v04 and earlier experiments.
- Baseline: v04 plus static raster-plate placement preview. Actual editable environment construction was not previously proven.
- Completion criterion: draw a recognizable shop/dusk street in Aseprite at the same pixel grid as the character, preserve v04, retain meaningful native background layers and reproducible drawing source, inspect appearance and prove a local environment edit. User approval remains separate.
- Tools: existing Aseprite 1.3.18.6-dev batch Lua; existing bundled Python/Pillow for checking and preview layout. No computer use, image-generation call, new MCP, new installation, paid service or reference-raster transfer in this increment.

## Construction principles and plan

The original scene guides the warm storefront, cool evening street, plants, railing, lamps/wires and distant bridge. Rechecked artist-authored [cluster sketching](https://saint11.art/pixel_art_articles/article2/) and [shading](https://saint11.art/pixel_art_articles/article4/) on 26 October 2026. Applied large masses before details, plane-based material shading, quiet distant values, connected foliage shapes and selective highlights. The source's fern leaves follow explicit branch trajectories; wall foliage uses controlled overlapping clumps rather than per-pixel noise.

1. Draw the sky/clouds, skyline, street facades, bridge and ground planes with authored pixel polygons/lines.
2. Draw shop shell, interior, frame/steps/curb and overhang. Add native plant branches/clusters, railings, lamp fixtures and light clusters, and a small sign.
3. Inspect a first pass, preserve it, then refine repetitive foliage and sparse architectural details. The final environment is intentionally simpler than the reference; exact fidelity is not claimed.
4. Save background source before composition. Copy all v04 cel images and layer visibility at native size with offset (84,61), and add a separate grounding shadow. No character relighting, resampling or repainting.
5. Save/reopen native sources, export actual environment layers, demonstrate an isolated lamp-core edit, and reproduce the background/scene in a fresh folder with no background/reference image inputs.

## Artifacts

- [Drawn scene preview](../../../assets/previews/street-drawn-v01/street-scene-4x.png) and [background-only preview](../../../assets/previews/street-drawn-v01/background-4x.png).
- [Native background](../../../assets/source/street-drawn-v01/background.aseprite), [native combined scene](../../../assets/source/street-drawn-v01/street-scene.aseprite).
- [16 actual environment layers](../../../assets/previews/street-drawn-v01/environment-layers.png).
- [Native drawing source](../../../assets/source/street-drawn-v01/draw-background.lua), [layer inspection/local-edit source](../../../assets/source/street-drawn-v01/inspect-and-revise.lua), [verification/preview source](../../../assets/source/street-drawn-v01/verify-and-preview.py), [run instructions](../../../assets/source/street-drawn-v01/README.md).
- [Background export](../../../assets/export/street-drawn-v01/background-native.png), [scene export](../../../assets/export/street-drawn-v01/street-scene-native.png), [exact character placement](../../../assets/export/street-drawn-v01/character-placement-only.png).
- [Separate lamp edit source](../../../assets/source/street-drawn-v01/background-lamp-edit-test.aseprite) and [before/after proof](../../../assets/previews/street-drawn-v01/local-edit-proof.png).
- [Native structure](source-checks.json), [editability checks](editability-checks.json), [export/rebuild checks with artifact hashes](checks.json).

## Observed results

| Boundary | Observed evidence |
| --- | --- |
| Native environment | 16 populated, named layers actually saved/reopened/exported; no imported background layer |
| Native scene | 29 layers, 352x264 grid, one static frame; background, ground shadow and character remain separable |
| Character preservation | All 12 original v04 cel images/positions/visibility checked after native reopen. Character-only scene PNG exactly equals v04 at offset; original native/PNG hashes unchanged |
| Reopened export | Both background and scene exports match their reopened native files exactly |
| Reproducible drawing | Fresh `.scratch/drawn-background-rebuild` contained only v04 native character input plus output directories. With no reference/background images present, final background and scene PNG bytes reproduced exactly |
| Local revision | Lamp-core test recolored 205 pixels on `bg/15-lamp-light-pixels`; all other 15 environment layer images/positions remained identical after save/reopen. Main lighting is preserved in the main source |
| Visual review | Shop/street layout recognizable, shared pixel grid, restrained palette/plane treatment and foreground character readability inspected. Wall foliage was revised from repetitive clusters; environment remains simplified, with some geometric shapes and procedural-looking vegetation |
| Approval/engine | User visual review pending; no Godot, animation, contact/timing, collision or camera validation |

The background is an actual native drawing, not the previous generated clean plate imported under another name. Shared grid and working shading rules do not by themselves establish the user's approval of the visual match.

## Continuation

The last proven state is this drawn environment plus exact v04. User reviews appearance and chooses any concrete background correction; agent performs routine local edits within that direction. Keep the raster placement and earlier character versions as historical experiments. Do not describe the previous plate as a constructed environment, or this static scene as a played Godot scene. All work remains local/uncommitted/unpublished.
