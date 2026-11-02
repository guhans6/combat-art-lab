# Animal Well — atmospheric character-reference study

**Researched:** 1 November 2026. **Scope:** character/creature presentation and
animation evidence for the working `stealth-fighter` brief—not an approved style,
an authorization to generate art, or a proposal to copy *Animal Well* characters.
No game asset, native source, export, or Godot playback was made in this study.

## Evidence and actual inspected material

The strongest process source is [Chris Kerr's 2022 interview with Billy
Basso](https://www.gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well).
It is a publisher-hosted secondary page, but the quoted answers are Basso's direct
statements. The two PlayStation posts below are first-party posts by Basso/Shared
Memory; the press page is the official publisher/developer press kit. All were
opened and checked on 1 November 2026.

| Local inspected artifact | Public original and provenance | Observable file data | What it actually shows |
| --- | --- | --- | --- |
| `atmospheric-character-references/animal-well/aw1-creature-motion.gif` | [Game Developer interview asset, `AW1.gif`](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/blt97a50b88d541cec5/663cd5de241e906fcb59b91c/AW1.gif) | GIF, 540 × 540; SHA-256 `2de83a2bae0bbca373631518071643b6fbd3fd87cad56a5de8da06e710f72388` | An Aseprite screen capture: a deliberately tiny quadruped in the preview and a timeline with named creature/player rows. This is direct visual evidence of an animation workspace and a small silhouette/pose workflow, not a released sprite sheet or a specification of every game asset. |
| `atmospheric-character-references/animal-well/aw3-ghost-cat-dog-motion.gif` | [Game Developer interview asset, `AW3.gif`](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/bltecc775b1a742837b/663cd616c07ad3e04b1f25be/AW3.gif) | GIF, 500 × 281; SHA-256 `b140c4f78e9b6ed4909e0530827088751fc437acc4729a1ea4ce1b70bef5efd3` | The oversized blue ghost creature faces the very small player at the right edge. Its readable face is a few large dark eye/mouth regions with blue value planes and a white/cyan rim; scale, dark void, and the creature's motion carry the threat more than detailed anatomy. |
| `atmospheric-character-references/animal-well/official-screen-ghost.png` | [Official Shared Memory press-kit image, `screen_ghost.png`](https://www.animalwell.net/press/build/Animal%20Well/images/screen_ghost.png) | PNG, 3840 × 2160; SHA-256 `1baaca5487fbda98dcab002e7e40a096a584dd914b1f57bf8ee04828a13c6b1f` | An official gameplay still: a minute player and tall ghost/creature forms are isolated by black negative space, sparse cyan/blue/purple light, and a few high-value practical lights. The staged depth and selective illumination—not a human portrait treatment—make the scene atmospheric. |

The files above were downloaded unchanged only as bounded research references from
publicly viewable sources. The press-kit page does **not** state a reusable
production-asset licence. Retain their provenance and treat them as third-party
research references, not project art or confirmed licensable/redistributable
production assets. This note makes no legal conclusion about any particular use.

## What Basso's material supports

- In the 2022 interview, Basso describes starting with one giant sprite sheet and
  manually entered UV coordinates, then adding Aseprite-data ingestion for
  traditional 2D animation. He says a character animation can combine authored
  animation, particles, and procedurally drawn geometry. That is a creator account
  of a hybrid process, not evidence that an Aseprite file alone produces the final
  look. [Interview](https://www.gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well)
- The same interview gives the Ghost Cat-Dog as a concrete character example:
  independently code-driven limbs/body segments follow slightly different paths,
  producing its unnatural stretch/bend. Its enemy pass begins with behavior and
  states, a rough Aseprite art/animation pass, then a state machine, play-testing,
  particles, eye tracking, and iteration. The visible `AW1` and `AW3` files above
  substantiate that this discussion is about creature animation rather than only
  environmental effects. [Interview](https://www.gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well)
- Basso explicitly says he was avoiding familiar excitement shortcuts such as
  squash-and-stretch and screen shake in this project. This is an **Animal Well
  aesthetic choice**, not a general rule for a sword strike. [Interview](https://www.gamedeveloper.com/art/creature-feature-the-surreal-pixel-art-and-animation-of-animal-well)
- In Basso's [PlayStation technical post (20 July
  2022)](https://blog.playstation.com/2022/07/20/how-animal-well-taps-into-ps5-hardware-to-elevate-2d-pixel-art-platforming/),
  he says he used a modified Aseprite that outputs a custom binary animation format
  and that the running custom engine instantly reloads it. The same post attributes
  parts of the scene result to manually drawn normal maps, dynamic lighting, fluid
  effects, and raymarched background geometry. Those are named creator techniques,
  not an instruction to adopt a custom engine or an assertion that Godot supplies
  identical output.
- The official [Shared Memory press kit](https://www.animalwell.net/press/build/Animal%20Well/index.html)
  is the source of the retained `screen_ghost.png`, lists separate GIF links, and
  describes the game as a custom-engine/renderer pixel-art project. The retained
  `AW1.gif` and `AW3.gif` instead come from the Game Developer interview, as their
  provenance table records. The [PlayStation
  announcement](https://blog.playstation.com/2022/02/10/the-secrets-of-animal-well-coming-to-ps5/)
  similarly frames the project as simple-looking pixel art paired with lighting and
  effects. That supports an atmosphere-through-layering reading; it does not prove
  that any individual on-screen glow is a particular shader.

## Bounded application to the stealth fighter

**Useful, originalizable principles to test later:** keep the fighter silhouette
legible before light/FX; let a narrow, deliberately placed light hierarchy select
the face, sword, and enemy-facing plane; use darkness as space rather than texture
everywhere; and design threat/weight from clear state changes and a held contrast
of scale. For a combat move, assess the naked pose/read first, then separately test
light, particles, or an optional restrained procedural secondary motion.

**Do not transfer:** *Animal Well*'s protagonist and antagonists are deliberately
tiny, abstract animal/creature forms. Their few-pixel eyes, extreme player-to-enemy
scale contrast, nonhuman segmented deformation, and ambiguity cannot answer how to
render this project's visible-faced, long-haired adult human, light armor, hands,
or compact sword. Atmosphere/lighting and creature animation are therefore **not**
a human-face, hair, armor, or sword-animation recipe. Keep the existing user
requirements in [`brief.md`](../characters/stealth-fighter/brief.md) ahead of this
reference.

## Version limits and unresolved uncertainty

- The direct interview and PlayStation technical article are from **2022**, while
  the official press assets describe the released 2024 game. They document Basso's
  reported development approach at those dates; no released source project, native
  sprite sheets, Aseprite files, shader source, or frame-data format was inspected.
- Basso stated a **320 × 180** low-resolution render target in the 2022 interview.
  It is a cited *Animal Well* example, not a measured current build specification,
  a size for the downloaded media, or a recommended/native size for this project.
  No project canvas, palette count, scaling rule, or shader/engine choice follows
  from it.
- The local GIFs visibly demonstrate an Aseprite UI and released-looking motion,
  but do not expose their source layers, timing tables, palette, procedural code,
  or the complete player/enemy state machine. The official press page provides no
  explicit reuse licence. These gaps remain intentionally unfilled rather than
  guessed.
- No direct developer material was found here that turns the desired “Silver Pines”
  vibe into a shared asset pipeline with *Animal Well*. That reference needs its
  own character-focused, rights-aware study before combining rules.

**Smallest next human decision:** choose whether the desired contribution is (A)
low-key cyan/purple light hierarchy and negative space, (B) unsettling restrained
secondary motion, or (C) both. Then gather/approve human-character references for
face, long hair, armor, and sword contact before any new concept pass; do not use
these creature examples to fill those unanswered design questions.
