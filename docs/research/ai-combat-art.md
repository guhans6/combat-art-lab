# Research: AI-directed art for a stylish 2D combat game

Last researched: **25 October 2026**. This document preserves the evidence and open choices for continuing in Codex. It is research, not a claim that this project's asset pipeline has been built or validated.

## Intent and current decisions

- The user is a beginner making a stylish, combat-heavy **2D game in Godot**, with AI doing implementation and the user directing, monitoring, and learning.
- The desired direction is **iterate AI-generated concept images until the style is right, then have AI construct actual editable sprite assets and animations from the approved design**.
- The workflow must not depend on the user painting over imported PNGs or becoming the primary pixel artist. AI-assisted construction, correction, and revision are the intended work. The user approves appearance and motion.
- The precise style, references, camera perspective, sprite resolution, palette, animation method, and required animation set are **not yet selected**.
- Aseprite automation is a candidate implementation route. Pixel art itself is not a settled requirement merely because Aseprite supports automation.

## What the evidence establishes

**AI can generate sprite imagery and can also draw editable pixel data through code or editor tools.** Public examples exist for both. None of the sources establishes that an agent will reliably reproduce this user's unspecified style through a full combat animation library.

| Evidence level | Meaning in this research |
|---|---|
| Official capability documentation | The tool or engine documents the operation; this project has not exercised it. |
| Source inspection | Research inspected implementation that creates or edits real document structure. |
| Published asset inspection | Research examined an author's existing output; no new model generation was run. |
| Creator report or demonstration | The creator reports a workflow or result; it is not an independent quality benchmark. |
| Research paper | The authors describe experiments and limitations within a particular setup. |
| Proposed workflow | A recommendation to test, not an established project decision or measured result. |

No Aseprite MCP server, PixelLab workflow, or complete Godot art pipeline was installed and executed during this research. Published examples and documentation are evidence of feasibility, not project validation.

## 1. Editable assets: what Aseprite and automation provide

Aseprite supports layers, frames, cels, animation tags, frame durations, palettes, previews, and onion skinning. Its native `.aseprite` format retains editing structure. PNG sheets and GIF previews are useful exports but do not replace that source document. Sources: [animation documentation](https://www.aseprite.org/docs/animation/) and [file formats](https://www.aseprite.org/docs/files/).

Its supported Lua API can create sprites, layers, frames, cels, and palettes and save native documents. Its command-line interface can run scripts and export sprite sheets and JSON metadata. An AI coding agent can author these instructions; an MCP server is one possible connection between the agent and those operations. It is not an image model and does not itself establish artistic quality. Sources: [scripting](https://www.aseprite.org/docs/scripting/), [Sprite API](https://aseprite.org/api/sprite), and [CLI](https://www.aseprite.org/docs/cli/).

**License correction:** current Aseprite is source-available under its own EULA, rather than the earlier GPL license. The official FAQ permits compiling/modifying it for one's own purposes and making commercial artwork while restricting redistribution of compiled Aseprite. This does not prevent supported scripting. Source: [Aseprite FAQ](https://www.aseprite.org/faq/).

### Two different AI routes

| Route | What AI produces | What remains editable |
|---|---|---|
| Generative imagery | A concept image, sprite image, or sequence of raster frames | Visible pixels; additional structure must be authored or reconstructed. |
| Tool/code drawing | Pixel placements, shapes, palette definitions, layers, cels, and frame operations | The native document plus any scripts or structured drawing source retained. |

A sprite is still an image. The useful distinction is whether the **source retains meaningful structure**. Saving a flattened PNG as `.aseprite` does not recover separate limbs, a weapon layer, hidden body parts, or a skeletal rig. Reconstructing those is additional work that the agent must perform and demonstrate. This follows from the documented file and API model above.

## 2. Concrete tool-drawing and pixel-grid examples

### Aseprite MCP: swordsman and attack animation

[`diivi/aseprite-mcp`](https://github.com/diivi/aseprite-mcp) documents pixel/shape drawing, layers, palettes, frames/cels, timing and tweening, previews, frame comparison, and exports. Source inspection of [`canvas.py`](https://raw.githubusercontent.com/diivi/aseprite-mcp/main/aseprite_mcp/tools/canvas.py) confirmed that it creates an Aseprite `Sprite`, adds native layers/frames, and saves the file. Its batch-mode execution should not be confused with editing an arbitrary unsaved GUI document.

Research also inspected the published [static swordsman](https://raw.githubusercontent.com/diivi/aseprite-mcp/main/examples/swordsman/opus_redraw.png) and [eight-frame slash](https://raw.githubusercontent.com/diivi/aseprite-mcp/main/examples/swordsman/opus_redraw_slash.gif). The compact blue-clad character remains recognizable while raising the sword, slashing, and following through. That is evidence of a simple working example, not the user's unknown aesthetic or an entire combat moveset.

[LJ V. Miranda's July 2025 experiment](https://ljvmiranda921.github.io/notebook/2025/07/20/draw-me-a-swordsman/) provides prompts, outputs, criteria, and linked code for tool-calling models drawing a swordsman and slash sequence. It reports mixed results across the tested models. Treat it as a small historical experiment, not a benchmark of every current model.

[`willibrandon/pixel-mcp`](https://github.com/willibrandon/pixel-mcp) is another documented bridge: canvas/layer creation, drawing, palettes, frame duration/tags, pixel reads, image import, and native saves. Its README establishes a potential integration route; this research did not execute it.

### sprite-gen: editable text grids and generated motion

[`aldegad/sprite-gen`](https://github.com/aldegad/sprite-gen) publishes attack-loop examples and documents image-to-atlas and video-to-transparent-animation workflows. Its author warns that requested facing direction is not guaranteed and locomotion requires motion review.

Its experimental [`pixel-draw` workflow](https://github.com/aldegad/sprite-gen/blob/main/docs/pixel-draw.md) has a language model write a palette and text grid of pixel-color keys. Code validates and renders the grid; editing the grid and rendering again does not require image regeneration. The creator reports small-sprite experiments at 16–48 pixels and admits that walk-cycle legs can fail to alternate convincingly. Those reported quality judgments are not independent benchmarks.

**Export caveat:** [`export-aseprite`](https://raw.githubusercontent.com/aldegad/sprite-gen/main/docs/engine-export.md) creates Aseprite-compatible **JSON atlas metadata**, not an editable `.aseprite` source file. Do not accept an atlas/JSON pair as proof that a layered source deliverable exists.

### Dungeon Sookuma: a public game-development example

[Dungeon Sookuma's Steam disclosure](https://store.steampowered.com/app/5045950/) states that AI coding/writing agents placed the in-game pixel art under developer direction. Selected enemy designs used generated concept references; larger illustrations and title animation used image/video generation separately. The listing was **Coming soon, with a demo** when inspected. This is a relevant first-party production report, not proof of a released action game or sophisticated combat-animation fidelity.

## 3. Generative alternatives worth retaining

These methods remain available if a style test shows they help. They are not substitutes for the user's preferred structured-asset goal without an explicit decision.

### PixelLab

PixelLab documents [style-reference generation](https://www.pixellab.ai/docs/tools/consistent-style), an [Aseprite extension](https://www.pixellab.ai/docs/installation), and [reference-image animation](https://www.pixellab.ai/docs/tools/animate-with-text-new). The newer animation tool preserves the input as its first frame and supports 4–16 even-numbered frames, with limits depending on image size. Its action examples include attacks.

Its [skeleton workflow](https://www.pixellab.ai/docs/tools/animate-with-skeleton) supports pose estimation, correction, templates, reuse, and saved pose material. Its [older animation tutorial](https://www.pixellab.ai/docs/tools/animation) explicitly includes selecting/reordering outputs, fixes, and inpainting. These are documented workflows, not evidence that every output meets the user's style or combat requirements. Within this project, required corrective work would be assigned to the agent or another approved production method; it is not a mandatory user painting task.

The tool's creators also posted an [early attack-animation demonstration](https://discussions.unity.com/t/ai-tool-for-generating-map-tiles-and-character-animations/924355). This is a creator demo, not independent validation. Use Aseprite's own FAQ for licensing; PixelLab's installation page describes that issue imprecisely.

### Sprite Sheet Diffusion

The [paper](https://arxiv.org/html/2412.03685v2) and [code](https://github.com/chenganhsieh/Sprite-Sheet-Diffusion) explore generating sprite sequences from an appearance reference and pose sequence. The authors provide comparisons and discuss a failure in which a character's gun disappears. Pose adherence and appearance preservation are separate challenges.

This is research evidence rather than a ready-made beginner pipeline. The [project page](https://chenganhsieh.github.io/spritesheet-diffusion/) had an unfinished Results section when inspected; the paper contains the substantive experiments.

### A small independent developer example

[Sr. Jr. Games' pigeon-animation devlog](https://srjrgames.com/blog/how-we-generate-consistent-animation-sprites-with-ai/) shows reference-conditioned flight poses and reports subsequent background removal, assembly, and timing work. This supports a limited practical use case. It does not establish precise control from numerical pose wording, arbitrary-style reproduction, or combat quality.

## 4. Animation methods beyond drawing every frame

| Option to evaluate | Editable source | Relevant tradeoff |
|---|---|---|
| Frame-by-frame raster animation | Layers, cels, frames, palette, durations | Supports changing silhouettes; every pose must retain design and scale. |
| 2D cutout or skeletal animation | Separate part images, pivots/bones, animation keys | Reuses parts; hidden surfaces, extreme turns, and foreshortening may need replacement drawings. |
| Rigged 3D rendered into 2D sprites | Model, rig, materials, animation curves, render setup | Enables reusable motions and viewpoints; adds modeling/rigging/rendering work. |

These suitability judgments are proposals, not measured comparisons. Choose after examining the user's references at the intended game size and in motion.

Godot documents [cutout animation](https://docs.godotengine.org/en/stable/tutorials/animation/cutout_animation.html), including mixing cutout and cel animation, and [2D skeletons](https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html). A generated picture is not automatically a clean rig with all required parts.

As a **non-AI production precedent**, Dead Cells artist Thomas Vasseur describes a 2D model sheet → simple rigged 3D model → small rendered PNG frames pipeline. He discusses easier motion/equipment revision alongside flickering-pixel and detail tradeoffs. His combat process starts from key poses and timing and revises animations alongside gameplay. Source: [first-person production account, January 2018](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-). This remains an optional method, not a recommendation to make the beginner learn 3D immediately.

## 5. Proposed proof of the intended workflow

This is the next experiment to design, not completed work or a commitment to a specific resolution, frame count, or service.

1. **Define the style from references.** Record silhouette, proportions, shape language, outline/shading, palette, camera, material treatment, and motion character. Separate admired qualities from a particular character's identity.
2. **Iterate concept images with user approval.** Converge on an original character and overall look. Also inspect a representation at intended gameplay scale; approval of a large concept does not validate a tiny sprite.
3. **Have the agent build an editable master.** Construct meaningful layers/parts, palette, consistent canvas and anchor, and an approved base pose. Retain the actual native file and any drawing scripts or structured source used. A flattened import alone does not satisfy this stage.
4. **Animate one representative attack.** Establish anticipation, contact/active motion, and recovery. The agent creates and corrects poses and timing. Keep gameplay hit timing explicit rather than assuming generated motion supplies it.
5. **Perform a local revision.** For example, change the weapon length or improve the contact pose while preserving the remaining design. This tests practical editability, not only whether a source file can be opened.
6. **Review the attack in Godot.** Use a small scene and target/dummy at intended camera scale. Judge readability, identity, weapon trajectory, ground contact, and timing. Expand the moveset only when the pipeline is acceptable.

Godot supports separate frames or sheets through `AnimatedSprite2D`, and frame/property animation through `AnimationPlayer`: [sprite-animation tutorial](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html). `SpriteFrames` supports per-frame duration in addition to animation FPS: [class reference](https://docs.godotengine.org/en/stable/classes/class_spriteframes.html). More frames are not, by themselves, evidence of better combat motion.

### Proposed proof deliverables

- Approved concept/reference and a short style specification.
- Editable native master with meaningful structure; retained scripts or pixel-grid source when used.
- Transparent frames or sheet plus frame/timing metadata appropriate for Godot.
- A motion preview and a minimal playable validation scene.
- A recorded local revision, known defects, and a clear statement of what was actually run and visually inspected.

Automated checks can verify dimensions, transparency, filenames, frame counts, palette constraints, and export consistency. Style fidelity, convincing motion, and gameplay readability still require visual review. The user should be able to direct the result without being required to draw it; how much agent correction is necessary remains to be measured with the actual chosen style.
