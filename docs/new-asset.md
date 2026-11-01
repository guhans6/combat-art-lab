# Start the next character

The tote character is on hold. The production workflow is unchanged.

1. Place new design references under `assets/incoming/`, in their own named folder.
2. Record which image is authoritative, choose the native scale/canvas and palette
   policy for that design, and check one pose before expanding it. Old183px values
   are the tote experiment’s settings, not a requirement for the new design.
3. Use deterministic conversion when desired: `learning/aseprite/automation/convert_image.py`
   reads a JSON recipe (source, optional mask, height OR shared scale, canvas,
   source_anchor, target_anchor), writes transparent PNG and provenance to a new
   destination, and refuses clipping or overwriting. Requires Python/Pillow13+.
4. Open the draft in Aseprite and save an independent native source. Keep the
   converted base; use corrections or a duplicate for erasing. Manual practice and
   agent-driven native revisions remain available as previously agreed.
5. Apply the existing art-production, animation and Godot verification boundaries.

Example from the repo root, with a recipe for the new design:

```sh
python3 learning/aseprite/automation/convert_image.py --recipe assets/incoming/NEW-DESIGN/recipe.json --out assets/source/NEW-DESIGN/draft-01
```

This command does no AI inference, redraw or cleanup. It preserves sampled source
RGB with nearest sampling and applies binary alpha. The optional mask/anchors must
fit the input; arbitrary-image automatic anatomy/segmentation is not established.
The six-pose batch tool and reach launcher are tote-specific examples, not generic
new-character presets. No models, services, licenses or tool settings changed.

See [production workflow](workflow/art-production.md), [asset contract](art/asset-contract.md),
[old-character catalog](../assets/CHARACTER-ARCHIVE.md), and [lessons](../learning/aseprite/index.html).
