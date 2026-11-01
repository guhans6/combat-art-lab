# Reference-guided pixel-art feasibility: diagnostic image reductions

Date: 27 October 2026

## What was actually tested

A fixed 420 x 315 crop of the user's uploaded 1448 x 1086 reference was processed with Pillow. No generative model was used. No agent redrew the anatomy. No Aseprite session or Godot preview ran. The user's workspace was inspected but not modified.

`resolution_comparison.png` shows the reference and three native crop grids: 56 x 42, 84 x 63, and 112 x 84. Each reduced image uses BOX area averaging, followed by mapping to one shared 32-color median-cut palette extracted from the original crop. Dithering is disabled. The three candidates are displayed at integer 6x, 4x and 3x respectively. The original is resized solely to fit its display panel.

`sampling_comparison.png` holds the target grid at 56 x 42 and compares nearest-neighbor, BOX, BOX plus 32 colors, and Lanczos plus 32 colors.

The native-size PNGs are included separately. Run `python reproduce_seeds.py` to recreate them from the included crop. The script requires Pillow and writes only into a new `reproduced` subdirectory. PNG encoding can differ by software version; compare decoded pixels when checking reproduction.

## Observations and limits

Broad geometry is carried over by these deterministic reductions. Thin eyelids and the shallow mouth lose clarity at the smallest grid. Palette reduction changes the shading and is not a fidelity-neutral operation.

These are conversion seeds, not finished sprites or approved pixel art. The tests do not include background removal, semantic layer separation, deliberate cluster cleanup, alpha handling, full-character scale selection, animation or runtime validation. Crop dimensions must not be presented as full-character canvas recommendations. The choice of 32 colors is illustrative, not a required style rule. There is no numerical likeness score or user approval.

## Recommended next experiment

Use one authoritative crop, one fixed placement transform and one target grid. Compare an existing independent redraw, reference-guided tracing on named layers, and deterministic conversion followed by scoped pixel cleanup. Keep all attempts. Measure geometry drift, expression, pixel craftsmanship and local editability separately. Only vary resolution after controlling layout and construction method.

Tracing guides and converted pixels are legitimate inputs when their provenance is disclosed. Importing an image alone does not recover semantic layers, hidden surfaces or new poses. Conversely, manually rewriting identical pixels does not make them more editable. Require meaningful structure and a successful localized revision, not a prohibition on all raster-assisted construction.

## Primary resources inspected

- Aseprite reference-layer command: https://www.aseprite.org/api/command/NewLayer/
- Aseprite layer model and selections-to-layers: https://www.aseprite.org/docs/layers/
- Aseprite RGB/indexed modes: https://www.aseprite.org/docs/color-mode/
- Pedro Medeiros, reference-assisted Aseprite construction: https://saint11.art/blog/3d-ref/
- Pillow resampling definitions: https://pillow.readthedocs.io/en/stable/handbook/concepts.html
- Kopf, Shamir and Peers, Content-Adaptive Image Downscaling: https://johanneskopf.de/publications/downscaling/
- PixelOE algorithm and implementation: https://github.com/KohakuBlueleaf/PixelOE
- Meta SAM 2 segmentation: https://github.com/facebookresearch/sam2
- ControlNet paper: https://arxiv.org/abs/2302.05543
- ChatGPT Images web-interface documentation: https://help.openai.com/en/articles/11084440-images-in-chatgpt
- OpenAI API image-generation controls and limitations: https://developers.openai.com/api/docs/guides/image-generation
- Gemini Apps image generation: https://support.google.com/gemini/answer/14286560
- Gemini API image-generation controls: https://ai.google.dev/gemini-api/docs/image-generation

PixelOE, SAM 2 and ControlNet were researched, not installed or tested on this character. API documentation does not establish which controls are available in a user's web account. Published size controls do not establish exact low-resolution pixel-grid or palette compliance.
