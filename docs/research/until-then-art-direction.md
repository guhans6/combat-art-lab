# Reference study: cinematic pixel-art direction

**Date:** 25 October 2026  
**Purpose:** turn the user's *Until Then* screenshots into original, testable visual constraints for the first combat-art experiment. This is reference analysis, not permission to copy its characters, locations, costume designs, logos, or compositions.

## Evidence level

### Confirmed externally

- *Until Then* is an adventure game by Polychroma Games, released on 25 June 2024. Its official Steam page identifies it as pixel graphics and a side-scroller; this establishes the reference work and genre presentation, not its internal production pipeline. [Steam store page](https://store.steampowered.com/app/1574820/Until_Then/) (accessed 2026-10-25)
- In a 2025 interview, director Mickole Klein Nulud describes anime and pixel-art communities as visual inspirations, naming *The Last Night* and *Tails Noir*; he says the team wanted to add its own flair. This is a direct creator statement reported by an industry magazine, but it does not specify a source-editor, sprite resolution, palette, or animation workflow. [MCV/DEVELOP interview, p. 41](https://www.gamesmags.com/download/MCV-1004-August-September-2025-digital-issue.pdf) (accessed 2026-10-25)
- Aseprite preserves a native sprite as a grid of layers, frames, and editable cels, supports per-frame duration, animation tags, onion skinning, indexed colour, PNG sequences, and PNG/JSON sprite-sheet export. Those are sufficient features for the first construction and revision proof. [Aseprite basics](https://www.aseprite.org/docs/basics/), [animation](https://www.aseprite.org/docs/animation/), [colour modes](https://www.aseprite.org/docs/color-mode/) (accessed 2026-10-25)

### Observed in the supplied screenshots

These are observations from the two user-provided screenshots, not claims about *Until Then*'s internal assets.

- Human figures use relatively natural, tall proportions and readable faces, with selective single-pixel accents instead of uniformly chunky, low-detail sprites.
- Edges are often dark but are not a universal black outline. Local value contrast and coloured outlines separate clothes, hair, props, and the background.
- The carnival image is organized in depth: a dark, low-contrast distant fairground; a saturated illuminated stall; foreground people; then stronger shadow beneath the stall. The warm stall light is the focal contrast.
- The scene uses a broad palette, clustered shading, small texture marks, and saturated practical lights. It is cinematic pixel art, rather than a restricted retro-console palette.
- Character silhouettes remain simple at gameplay scale: head/hair mass, torso, separated legs, and one or two distinctive colour blocks. This is the aspect to carry into combat first.

## Original direction to test

Use the reference for **cinematic contemporary pixel-art principles**, not an imitation:

1. Design an original combat character with a distinct silhouette, outfit and weapon. Start with a neutral street-and-neon setting rather than a fairground, school, or any reference character/location.
2. Work at a provisional native canvas that supports hands, face direction and weapon contact. Do not select final resolution until the first sprite is viewed in Godot at the intended game scale.
3. Use named transparent Aseprite layers: `body`, `hair`, `outfit`, `weapon`, `fx`, and a locked `guide-ground`. Keep the character separate from any scene lighting/effects layer.
4. Build the first attack around four readable key poses: anticipation, contact, follow-through, recovery. Check the silhouette with effects hidden before adding a coloured impact flash or trail.
5. Use a small role-based palette rather than copying sampled colours: deep cool shadow, neutral midtone, warm key light, one saturated character accent, and one impact accent. Move to Indexed mode only after a palette size is consciously selected; it makes global palette edits possible because each pixel references a palette entry.

## Recommended smallest proof

Create an original full-body side-view fighter in one standing key pose, then make a short weapon strike. Preserve `.aseprite` source, an export, and a short preview. Request two deliberate changes after the first pass: one costume/weapon accent and one contact-timing change. This directly tests editability, visual readability, and motion without assuming that a scene background or a complete game is already solved.

## Useful, recognized learning material

- Aseprite's own [drawing tutorial index](https://www.aseprite.org/docs/tutorial/) and [pixel-perfect stroke documentation](https://www.aseprite.org/docs/drawing/) are the primary tool references for clusters, pencil workflow, palette operations and export.
- Use Aseprite's [onion-skinning guide](https://www.aseprite.org/docs/onion-skinning/) and [animation guide](https://www.aseprite.org/docs/animation/) for the first attack; they are appropriate for checking spacing between the four key poses.
- Use Godot's [2D sprite animation documentation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html) only when the native asset is ready to preview; it documents the engine integration boundary and does not dictate the art style.

## Unknowns to resolve by experiment

- The game-view camera, native resolution, final palette count, final outline rule, desired combat genre and representative attack remain undecided.
- No public primary source found here confirms *Until Then*'s exact asset format, authoring software, resolutions, or character-animation technique. Do not infer them from the screenshots.
- The compiled Aseprite build was subsequently copied to `/Applications/Aseprite.app` and verified for version, batch scripting, layered native save/reopen/revision and PNG export. The GUI and production character workflow were not visually validated. See the reference-study record.

## Additional artist resources and comparable assets

Checked 25 October 2026. These are study resources, not installed dependencies or a selected asset pack.

- [Pedro Medeiros / Saint11's articles](https://saint11.art/pixel_art_articles/) cover cluster sketching, shading, anti-aliasing/banding, color theory, and a basic Aseprite animation. Use them to reduce noisy isolated pixels and preserve readable forms, rather than merely adding a pixel filter. The artist's [tutorial repository](https://github.com/saint11/Saint11Tutorials) also provides compact illustrated lessons.
- [Ansimuz's Warped City](https://ansimuz.itch.io/warped-city) is a useful contrasting urban combat asset example: parallax background, character animations and a Godot project. Its more compact platformer treatment is not an exact Until Then match. The creator currently labels the base asset CC0; verify the exact downloaded package and any addon terms before reuse. Nothing was downloaded, purchased or adopted.
- Aseprite's [official CLI](https://www.aseprite.org/docs/cli/), [Sprite API](https://www.aseprite.org/api/sprite/) and [Image API](https://www.aseprite.org/api/image/) support the locally verified scripting approach. A dedicated third-party MCP has not been shown necessary.
