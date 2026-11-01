# Static street preview with existing v04 character

- Date: 26 October 2026
- Request: add the background from the original image and stand the reconstructed character in it. This expands the task to a static scene composition; it does not request a new character or full background construction/animation pipeline.
- Base: v04 native/PNG and the newly pasted original scene reference, preserved as [street-scene-user.png](../../../assets/references/approved-2026-10-26/street-scene-user.png).
- Completion criterion: no remaining original figure behind our character; comparable composition/grounding, separate editable character/background/shadow, and proof v04 pixels remain intact.
- Tools: built-in imagegen (one background edit), installed Aseprite 1.3.18.6-dev batch Lua, bundled Python/Pillow for comparison/export checks. No new installation, API key, paid external service or computer interaction.

## Method

1. Imagegen removed the original figure/tote and reconstructed the occluded scenery. [Exact prompt](../../../assets/source/street-preview-v01/background-edit-prompt.txt) and [generated clean plate](../../../assets/source/street-preview-v01/background-clean-generated.png) are saved. The visible setting follows the original shopfront/plants/lamps/dusk street/bridge; generated scenery is not claimed pixel-identical outside the removed figure.
2. Aseprite samples the clean plate to a provisional 352x264 grid with explicit nearest-neighbor sampling. This grid fits the existing 184px-tall figure at comparable screen scale; it is not a finalized game resolution.
3. Copy all 12 character native layers at offset (84,61), without resampling, reposing, relighting or repainting. Feet reach y246; the original scene composition guides placement.
4. Add two small contact shadows and a broader ambient footprint on a separate pixel-art layer beneath the shoes, with no blur filter.
5. Save/reopen native scene, compare each copied cel and position, export character-only isolation and confirm exact placement against v04. Produce a 1408x1056 nearest-neighbor presentation preview.

## Deliverables

- [Scene preview](../../../assets/previews/street-preview-v01/street-scene-4x.png).
- [Native 14-layer Aseprite scene](../../../assets/source/street-preview-v01/street-scene.aseprite).
- [352x264 scene PNG](../../../assets/export/street-preview-v01/street-scene-native.png), [background](../../../assets/export/street-preview-v01/background-native.png), [shadow](../../../assets/export/street-preview-v01/ground-shadow.png), [character-only placement](../../../assets/export/street-preview-v01/character-placement-only.png).
- [Build source](../../../assets/source/street-preview-v01/build-scene.lua), [verification source](../../../assets/source/street-preview-v01/verify-scene.py), [run instructions](../../../assets/source/street-preview-v01/README.md), [check results/hashes](checks.json).

## Observed evidence and boundaries

- Aseprite native source saved/reopened: 352x264, one frame, 14 layers. All 12 copied v04 cel images, translated positions and visibility values checked equal.
- Character-only scene export is exact RGBA v04 placed at the declared offset. v04 native/PNG hashes unchanged.
- Reopened scene export is identical to original scene export. Independent composition matches exactly outside semitransparent shadow; Aseprite/Pillow differ by at most one channel unit inside uncovered shadow due to rounding.
- Visual inspection: original person is removed, reconstructed character reads against the background, shoes lie on the pavement, and the small contact shadow grounds the stance. User acceptance remains pending.
- Background is a generatively cleaned flat raster. This does not prove separately editable plants/buildings or agent-drawn environment construction. Character layers remain meaningfully editable.
- No Godot playback, input, motion, camera, combat contact, commit or publication performed. Scene/camera resolution remains provisional.

Next: user reviews the static character-in-scene appearance/scale. Continue the next approved asset or motion experiment while retaining v04 and this static composition independently.
