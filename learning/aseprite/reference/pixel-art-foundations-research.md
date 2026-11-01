# Pixel-art foundations research — framing before the grid

**Scope:** source notes for a short beginner Aseprite/Godot lesson, not a change to
the project art direction or a claim that the learner has used either application.
Researched **31 October 2026**. No editor or engine session was run.

## The lesson in one minute

Choose the gameplay picture first: how much of the screen is world, character, UI,
and motion. Then choose a native drawing grid that can express that picture. A bigger
displayed sprite is still the same drawing unless someone deliberately adds or changes
pixels.

For a first pass, block the silhouette and large light/dark masses, then make clean
pixel clusters. Texture comes last. Keep every animation frame on a stable canvas and
put the feet at the same declared ground point; this makes a moving character read as
movement rather than a document that jumps around.

Those last two sentences are **teaching recommendations**, informed by the sources
below, not Godot or Aseprite requirements.

## Terms that must not be conflated

| Term | Meaning in this lesson | Documented basis / limit |
| --- | --- | --- |
| **Native sprite grid** | The width × height of the editable Aseprite document or individual source image, e.g. a 128×192 document that contains a 96 px-tall visible character. | An Aseprite sprite has a pixel width and height; its layers, frames, and cels are separate structure. [Aseprite: Sprite structure](https://www.aseprite.org/docs/sprite/) |
| **Canvas** | The document's rectangular visible area. It can include transparent safety/motion margin around the drawing. | Aseprite calls canvas the sprite's visible area; Canvas Size changes that area, and Trim can remove transparent borders. [Aseprite: Canvas Size](https://www.aseprite.org/docs/canvas/) |
| **Visible artwork bounds** | The smallest rectangle containing the non-transparent character drawing. This is a useful review measurement, not a Godot setting and not necessarily the canvas size. | Inference from the canvas/trim behavior above. Measure it; do not mistake transparent padding for character height. |
| **Base viewport / design size** | The logical game picture the scene is composed for, e.g. 640×360. | Godot calls the configured base size the “design size”; it does not switch the monitor to it. [Godot: Multiple resolutions](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html#base-size) |
| **Window / display resolution** | The space supplied by the OS to the game, e.g. 1920×1080. It may differ from the base viewport. | Godot distinguishes the system-allotted window from the root viewport. [Godot: Multiple resolutions](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html#base-size) |
| **Camera and node scale** | Additional transforms that can change the on-screen size of the drawing. | `Camera2D.zoom` defaults to `(1, 1)`; a `Sprite2D` is a texture-displaying `Node2D`. [Camera2D](https://docs.godotengine.org/en/stable/classes/class_camera2d.html) · [Sprite2D](https://docs.godotengine.org/en/stable/classes/class_sprite2d.html) |

## One hypothetical, with the assumptions exposed

This is arithmetic for teaching, **not a project specification or observed render**.

- Base viewport: **640×360**.
- Intended visible character height: **96 base pixels**.
- Character's intended vertical share: `96 / 360 = 0.2667`, or **26.7%**.
- At a 1920×1080 16:9 window, `1920 / 640 = 3` and `1080 / 360 = 3`.
  With a 3× integer viewport scale, the character occupies `96 × 3 =`
  **288 displayed pixels** high, still 26.7% of the displayed 1080-pixel height.

That 288-pixel result assumes all of the following: the visible 96-pixel artwork maps
one-for-one to base viewport pixels (no `Sprite2D`, parent, or CanvasItem scaling),
the active `Camera2D` is at `(1, 1)`, the game content area is exactly 1920×1080,
the aspect ratio is preserved, and OS/HiDPI/compositor behavior introduces no extra
scale. Change any of those and measure in the running game instead. Godot notes that
its base size is a design size and provides separate stretch modes/scales; it also
documents HiDPI caveats. [Multiple resolutions](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html)

For pixel art, Godot's current stable guide names 640×360 as a useful baseline because
it maps at an integer scale to 720p, 1080p, 1440p, and 4K. Its suggested starting
combination is base size = intended viewport, stretch mode `viewport`, aspect `keep`
(or `expand` for more aspect ratios), and integer scale mode. This is a **Godot
recommendation**, not a mandate for this game's first lesson. [Godot: pixel-art
scenario](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html#desktop-game)

`viewport` first renders at the base size then stretches the result; `canvas_items`
renders 2D directly at target resolution and can lose a 1:1 sprite-to-screen-pixel
relationship. Integer scaling rounds the automatic scale down and can add black bars;
it avoids uneven pixel widths. `viewport` also trades away sub-pixel movement/rotation
compared with `canvas_items`. [Stretch modes and scale modes](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html#stretch-mode) · [pixel-art caveat](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html#desktop-game)

Nearest filtering and pixel snapping solve different problems. Nearest samples one
texel rather than blending neighbors. Transform/vertex snapping can make 2D crisper,
but Godot explicitly says it can make movement less smooth; `Sprite2D.centered` can
also place a texture between pixels. Treat these as later render tests, not advanced
setup for the first lesson. [CanvasItem filtering](https://docs.godotengine.org/en/stable/classes/class_canvasitem.html) · [Viewport snapping](https://docs.godotengine.org/en/stable/classes/class_viewport.html) · [Sprite2D centering note](https://docs.godotengine.org/en/stable/classes/class_sprite2d.html#class-sprite2d-property-centered)

## What size does *not* decide

- **No universal native size.** Aseprite lets a new sprite have a width and height and
  lets Sprite Size resize it; Godot's general-purpose `Sprite2D` displays a 2D texture
  and can also show an atlas region or sprite-sheet frame. Neither cited page gives
  ordinary `Sprite2D` a power-of-two, tile-size, or actor-size rule. A tile grid may be
  a level-design convention, but it is not a requirement that an actor be one tile.
  [Aseprite: Sprite Size](https://www.aseprite.org/docs/sprite-size/) · [Godot:
  Sprite2D](https://docs.godotengine.org/en/stable/classes/class_sprite2d.html)
- **Enlarging does not invent authored detail.** Aseprite's resize operation changes
  sprite/cel dimensions and offers resampling methods (including Nearest Neighbor).
  It cannot know the intended eyelid, fold, or silhouette correction that was absent
  from the source; that is a teaching inference, not an Aseprite promise. Use resizing
  to initialize a working size, then inspect and deliberately construct/revise pixels.
  [Aseprite: Resize](https://www.aseprite.org/docs/resize/) · [SpriteSize method
  options](https://www.aseprite.org/api/command/SpriteSize)
- **A large canvas is not a large character.** The canvas may include transparent
  margin. Review the visible artwork bounds and the intended foot anchor, not only the
  file's dimensions.

## Craft order for the beginner exercise

**Teaching recommendation:** first make a readable outer contour, then group the
largest light/dark shapes, then refine deliberate clusters; add texture only when it
supports those forms. This keeps the first correction reversible and readable at game
scale. For animated frames, retain a common canvas and record one foot/ground anchor;
avoid changing canvas size merely to chase a pose. Aseprite documents frames, cels,
and per-frame duration, but it does **not** prescribe this anchor convention.
[Aseprite: Animation](https://www.aseprite.org/docs/animation/) · [Sprite
structure](https://www.aseprite.org/docs/sprite/)

The primary artist source behind that order is Derek Yu's own beginner tutorial. It
starts at 96×96 only because it is easier to demonstrate techniques, calls that large
for many retro games, advises reading a form as large light/dark clusters before
details, and describes smaller sprites as a set of deliberate compromises. It supports
the lesson's craft guidance; it does not set this project's style or production size.
[Derek Yu, *Pixel Art Tutorial: Basics*](https://www.derekyu.com/makegames/pixelart.html)

## Version limits and unresolved uncertainty

- **Godot:** all engine facts above are from the live `/en/stable/` official docs
  retrieved 31 October 2026, not pinned to a numbered manual or tested against this
  course's project. The wider repository has historical evidence of Godot 4.7.2, but
  this research neither opens it nor asserts the exact current editor menus.
- **Aseprite:** official help pages are unversioned and retrieved 31 October 2026. The
  wider repository records Aseprite `1.3.18.6-dev`; this note did not inspect that
  build, so labels, commands, and behavior should be checked in the learner's UI.
- **Rendering:** no import, window, camera, OS/HiDPI, monitor, filtering, snapping, or
  gameplay-sized visual test occurred. The 640×360/96/3× calculation is an example
  only; camera framing, final style, native grid, palette, and production scale remain
  open project decisions.
- **Art advice:** Derek Yu's tutorial is a working pixel artist's first-party teaching,
  not an engine specification or a universal aesthetic rule. Its 2019–2020 date is
  visible on the page; the source was retrieved 31 October 2026.


## Local practice-image measurement

Parent agent independently decoded the copied `assets/practice-preview.png` with a
read-only PNG scan: canvas 128×192 RGBA; nonzero-alpha bounds `[32,2,104,185)`
(right/bottom exclusive), hence visible bounds 72×183. This measurement belongs to
that exact practice copy, not every earlier character version. Browser framing demos
rescale this crop as a stand-in and are not newly authored source sprites.
