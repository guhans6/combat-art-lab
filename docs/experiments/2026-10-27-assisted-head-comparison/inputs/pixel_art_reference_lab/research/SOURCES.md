# Primary-source register

Checked on **27 October 2026**. Links below document capabilities or techniques, not a guarantee of results on this character. Explanations in this kit are a synthesis; tutorials and third-party implementation code are not redistributed.

| ID | Primary source | What it supports / boundary |
|---|---|---|
| S01 | [Aseprite reference layers](https://www.aseprite.org/docs/reference-layer/) | Higher-resolution reference underlays distinct from editable artwork. Actual automated placement must be tested locally. |
| S02 | [Aseprite NewLayer command](https://www.aseprite.org/api/command/NewLayer) | Reference-layer and selection-to-layer command options; a GUI file-dialog option is not a headless filename API. |
| S03 | [Aseprite layer API](https://www.aseprite.org/api/layer) and [layers](https://www.aseprite.org/docs/layers/) | Native layer organization, opacity and selection-based separation. No automatic reconstruction of hidden parts. |
| S04 | [Pedro Medeiros: 3D reference](https://saint11.art/blog/3d-ref/) | An artist's reduced-reference then redraw process in Aseprite. Not a claim that AI cleanup is automatic or cheap. |
| S05 | [Pedro Medeiros: consistency](https://saint11.art/blog/consistency/) | Resolution, color and stylistic consistency; separate visual systems may have separate treatment. |
| S06 | [Cure: pixel-art tutorial](https://pixeljoint.com/forum/forum_posts.asp?TID=11299) | Deliberate pixel control, clusters, palette/contour craft and manual anti-aliasing. No universal color-count prescription. |
| S07 | [Pillow resampling concepts](https://pillow.readthedocs.io/en/stable/handbook/concepts.html) | NEAREST, BOX and LANCZOS behavior. Stable documentation may differ from the locally tested version; kit validation records it. |
| S08 | [PixelOE](https://github.com/KohakuBlueleaf/PixelOE) | Contrast-aware outline-expansion pixelization implementation. Researched, not run here. |
| S09 | [Meta SAM 2](https://github.com/facebookresearch/sam2) | Promptable image/video segmentation masks. Researched, not installed; masks are not a completed character rig. |
| S10 | [ControlNet paper, abstract](https://arxiv.org/abs/2302.05543) | Spatial controls including edges, pose, depth and segmentation. Abstract inspected, not a full paper replication or local test. |
| S11 | [Images in ChatGPT](https://help.openai.com/en/articles/11084440-chatgpt-images-faq) | Image creation/editing from references; selection edits can affect neighboring content; exact local tool access still needs inspection. |
| S12 | [OpenAI image generation guide](https://developers.openai.com/api/docs/guides/image-generation) | Image/edit workflows and recurring-character/composition limitations. API capabilities are not identical to web UI controls. |
| S13 | [OpenAI image tool](https://developers.openai.com/api/docs/guides/tools-image-generation) and [edit reference](https://developers.openai.com/api/reference/resources/images/methods/edit) | Reference-image tool/edit capability; exact models/parameters are runtime-specific and are deliberately not pinned by prompts. |
| S14 | [Gemini image generation](https://ai.google.dev/gemini-api/docs/image-generation) | Text-and-image generation/editing and model-dependent output controls. Does not establish what is enabled in the user's web account. |
| S15 | [Aseprite animation](https://www.aseprite.org/docs/animation/) | Frames, cels, tags, onion-skin inspection and per-frame duration. |
| S16 | [Godot 2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html) | Animation from individual images or sprite sheets using documented engine components. Not a local playback result. |

## Local sources

[WORKSPACE_EVIDENCE.md](WORKSPACE_EVIDENCE.md) identifies the live files inspected and their returned identifiers. The original user uploads and SHA-256 values are in `references/manifest.json`. Historical reduction methods and evidence are under `examples/previous_conversion/`.

Installed guidance read: `skills://plugins/game-studio/sprite-pipeline/skill.md`, plus global `handoff` and `writing-for-agents` bodies through Code-MCP. The sprite skill's shared-scale/anchor workflow is useful, but this kit permits both multi-view references and separately generated poses as the user explicitly requested. Its browser-game-specific scripts and the full private skill contents are not bundled.

Current external documentation was read for capabilities only. No new paid account, API request, image generator, segmentation model, ControlNet pipeline, PixelOE installation, Aseprite execution or Godot execution was used to prepare the kit.
