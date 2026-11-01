# Aseprite Resources

Primary documentation checked 31 October 2026. Aseprite pages are current and unversioned; the art repository records Aseprite 1.3.18.6-dev. Exact tooltips/menus can differ with build, language or customized shortcuts. No live editor session was tested for this course.

## Knowledge

- [Aseprite: Layers](https://www.aseprite.org/docs/layers/)
  Ordinary layers, order, visibility, opacity and locking. Use for the first small correction and separating final art from a guide.
- [Aseprite: Drawing](https://www.aseprite.org/docs/drawing/)
  Drawing tools and brush basics. Use for Pencil, Eraser and Eyedropper; prefer clicking tools and reading tooltips over platform-specific shortcut assumptions.
- [Aseprite: Sprite Size](https://www.aseprite.org/docs/sprite-size/) and [Canvas Size](https://www.aseprite.org/docs/canvas/)
  Resampling versus crop/padding. Use before shrinking a concept or changing document bounds.
- [Aseprite: SpriteSize command API](https://www.aseprite.org/api/command/SpriteSize)
  Primary source for nearest, bilinear and RotSprite method names. The teaching exercise uses Nearest Neighbor as a controllable starting point, not a claim of best likeness or equality to the historical conversion recipe.
- [Aseprite: Edit menu](https://www.aseprite.org/docs/edit-menu/)
  Documents Paste Special → Paste as New Layer. Use to bring an aligned, same-sized guide into a drawing document.
- [Aseprite: Reference Layer](https://www.aseprite.org/docs/reference-layer/)
  Special non-editable, high-resolution reference type. Distinguish from an ordinary faded guide; lessons use an ordinary layer and explicitly hide it before export. Current page does not explicitly establish export exclusion, so this course does not rely on it.
- [Aseprite: Save](https://www.aseprite.org/docs/save) and [Exporting](https://www.aseprite.org/docs/exporting)
  Preserve native structure and export runtime images. Use before turning a layered practice file into a PNG.
- [Godot: Sprite2D](https://docs.godotengine.org/en/stable/classes/class_sprite2d.html), [CanvasItem](https://docs.godotengine.org/en/stable/classes/class_canvasitem.html), and [Importing images](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)
  Godot 4 texture assignment, node Texture Filter/Nearest and lossless image import. Use for the optional static-sprite next step; this course does not claim an observed engine run.

- [Aseprite: Preferences](https://www.aseprite.org/docs/preferences/) and [v1.3.3 release notes](https://blog.aseprite.org/2024/02/14/aseprite-v133/)
  Alpha & Opacity can display percentages or 0–255. Use if a beginner sees 255 instead of 100%.

## Foundations: size and visual decisions

- [Godot: Multiple resolutions](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html)
  Base design size versus window presentation, viewport rendering and integer stretch. Read the base-size and pixel-art scenario sections; no engine setup is needed for the first lesson.
- [Godot: Camera2D zoom](https://docs.godotengine.org/en/stable/classes/class_camera2d.html#class-camera2d-property-zoom)
  Separates camera framing from image-file dimensions and whole-window enlargement.
- [Derek Yu: Pixel Art Tutorial: Basics](https://www.derekyu.com/makegames/pixelart.html)
  A practicing artist's primary tutorial: outer form, large color/value areas, refinement and smaller-sprite compromises. Its example sizes and palette are teaching choices, not requirements for this project.
- [Local foundations research](reference/pixel-art-foundations-research.md)
  Dated primary-source findings, assumptions, arithmetic and limits. Browser demonstrations do not establish Godot rendering or choose a production grid.

## Wisdom (Communities)

- [Aseprite Community](https://community.aseprite.org/)
  Official community for specific tool questions and critique. Optional: share a small before/after with intended size, what you changed, and one concrete question. No need to post or join to take these lessons.

## Gaps

- Best production resolution, style fidelity and finished game scale remain project art decisions; a resize tutorial cannot establish them.
- The historical seed used preparation beyond a single Nearest Neighbor resize. Lesson 2 intentionally teaches a separate manual experiment, not an exact reproduction of that seed.
- User proficiency and the installed UI's exact appearance remain untested. Ask for the learner's result before writing learning records.

## Drawing and timing your supplied poses

- [Aseprite: Timeline](https://www.aseprite.org/docs/timeline/) and [Sprite structure](https://www.aseprite.org/docs/sprite/)
  Rows are layers; columns are frames; each frame composites its visible cels. Use with the prepared three-key files.
- [Aseprite: New Frame](https://www.aseprite.org/docs/new-frame/) and [Linked Cels](https://www.aseprite.org/docs/linked-cels/)
  Distinguish empty, copied and linked cel content before extending the starter. The starter does not require new frames yet.
- [Aseprite: Onion Skinning](https://www.aseprite.org/docs/onion-skinning/), [Frame Duration](https://www.aseprite.org/docs/frame-duration/) and [Preview Window](https://www.aseprite.org/docs/preview-window/)
  Ghost guides, timing and rough playback; none creates missing drawings automatically. Checked 31 October 2026 against official, unversioned docs.
- [Two-route preparation manifest](practice/two-routes-2026-10-31/manifest.json)
  Exact source hashes, common transform, binary-alpha policy, pooled palette, frame data and tool versions. This is a source-derived practice seed, not a finished action.

## Current one-pose reference

- [Earlier clean/smear chat](codex://threads/01a19024-f723-7a23-ad2b-74fbda7ff9e6)
  Inspected 1 November 2026. The neutral standing pixels are reused unchanged at 183px drawn height; the animation's wider canvas is placement space.
- [183px reference manifest](practice/one-pose-183-2026-11-01/manifest.json)
  Exact original/native hashes, 128×192 source dimensions, color counts and matched animation-frame translation. This is source reuse, not a newly generated or resized drawing.


---

## Preserved learning-branch document (484d4d0)

The following original local document is retained verbatim for historical context. Guidance above reflects the incoming course updates; statements about missing assets below describe the earlier checkout.

# Resources — Aseprite learning

Last verified against primary Aseprite documentation: **2026-10-31**. Prioritize official docs; community pages are supplemental explanations, not guarantees.

| Question | Source | Why it matters |
| --- | --- | --- |
| Where do I begin? | [Aseprite workflow](https://www.aseprite.org/docs/workflow/) | Open image, pencil, zoom, layers, frames, native save, export |
| What is editable? | [Layers](https://www.aseprite.org/docs/layers/) | Visible/locked layers, transparent layers, copy selection into layer |
| How does a tracing image work? | [Reference layers](https://www.aseprite.org/docs/reference-layer/) | Higher-resolution reference, not directly drawable |
| How do I resize? | [Resize](https://www.aseprite.org/docs/resize/) and [SpriteSize command](https://www.aseprite.org/api/command/SpriteSize) | Sprite > Sprite Size; nearest-neighbor, bilinear, RotSprite options |
| How do frames/layers relate? | [Basics](https://www.aseprite.org/docs/basics/) and [Timeline](https://www.aseprite.org/docs/timeline/) | Each layer/frame intersection is a cel |
| What if I already have separate pose PNGs? | [Opening an image sequence](https://www.aseprite.org/docs/open/) | Numbered PNGs can open as animation |
| What if I have a grid sprite sheet? | [Sprite sheets](https://www.aseprite.org/docs/sprite-sheet/) | Import sheet by frame cell dimensions and offsets |
| How do I compare adjacent poses? | [Onion skinning](https://www.aseprite.org/docs/onion-skinning/) | F3 to view adjacent frames while editing |
| How do I vary timing? | [Frame duration](https://www.aseprite.org/docs/frame-duration/) | Each frame has its own display duration |
| What should I save/export? | [Save](https://www.aseprite.org/docs/save/), [Exporting](https://www.aseprite.org/docs/exporting) | Native .aseprite for editing; PNG/sheet for game |
| Does a reference layer export? | [Aseprite Community reference guide](https://community.aseprite.org/t/how-to-work-with-references/14684) | Community explanation of reference layer behavior; check actual exports |

## Study order

Complete Lesson 01 before reading extensively. Refer to each official source only when the task requires it, then do the edit in Aseprite. Lesson 02 adds animation mechanics.
