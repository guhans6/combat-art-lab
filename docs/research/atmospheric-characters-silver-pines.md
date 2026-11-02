# Silver Pines character-reference study

Researched: **1 November 2026**. Scope: identify directly evidenced character and
atmosphere lessons for the stealth-fighter exploration. This is reference analysis,
not a style approval, production recommendation, or a claim that this project can
replicate *Silver Pines*.

## Evidence boundary

The main source is Wych Elm/Team17's official Steam announcement, ["Behind the Pines Dev Blog 1: Animation and Rotoscoping"](https://steamcommunity.com/games/2333000/announcements/detail/690893589804220611),
published **3 September 2026**. It says that character performances were filmed and
drawn over frame-by-frame; the team made costumes and used team members/friends as
references. It attributes the game-world photo textures to world artist Calle Schytt
Winberg, who modifies and paints them over, and says 2D sprites are rendered in a
3D simulation. The post says the art uses shadows for depth and volume rather than
the flat-colour approach it associates with older rotoscoped games. Those are
creator/publisher statements about *their* pipeline, not observations that establish
our production method.

The supporting source is a [first-person interview with Wych Elm co-founder Linus
Larsson](https://80.lv/articles/how-silver-pines-used-rotoscoping-to-create-its-unsettling-horror)
published by 80 Level on **8 October 2026**. Larsson says their animation practice
uses filmed material and drawing over it, and that some other animation uses bone
rigs plus a manual edit pass or freehand frames. He also says mood takes priority
over realism in lighting while remaining believable, and that lighting/colour changes
do much of the surreal work. This is a directly attributed creator interview, but
80 Level is not the developer or publisher.

No claims here rely on `silverpines.top` or Game Wiki Station.

## What the inspected media supports

The three retained files below are media embedded by the official Steam dev blog. I
visually inspected each file; for GIFs, I also inspected sampled contact sheets.

| Boundary | Directly observed from the official media | Useful design takeaway | Not established |
| --- | --- | --- | --- |
| **Character shape and colour** | Walker reads first as a compact, dark, long-coat silhouette. A pale face plane and, in the walking comparison, a bright flashlight beam are the clearest identity accents. Fine clothing construction is largely lost against the dark scene. | For an atmospheric stealth-fighter study, make the gameplay-scale identity read from one or two deliberate silhouette breaks and a small focal contrast, rather than from lots of armour detail. | Walker's full costume, exact palette, facial details, native sprite resolution, or an appropriate transfer to the fighter. |
| **Performance / animation** | The raw-footage/in-game GIF preserves a forward-leaning, weighted walk. The knockout comparison explicitly shows filmed body reference, simplified drawn frame, then the in-game result. The close character GIF shows a long, restrained body transition rather than a sequence of unrelated pose silhouettes. | If the user later authorizes a motion test, define the performer-like weight shift and the major body arc first; treat rotoscoping as a specific reference method, not as a look that can be copied from one still. | Frame count, timing rules, pose spacing, attack choreography, whether a comparable capture method suits this project, or that the GIF proves a complete combat-animation solution. |
| **Scene lighting / atmosphere** | The samples use an extremely dark, cool field, selective pale highlights, grainy/soft texture, and isolated red/pink environmental accents. In the character close-up, the bright face and floor value are set against a deep foreground silhouette; the official post attributes its depth/volume intent to shadows. | Keep scene atmosphere separate from character construction: test a readable character silhouette under a constrained key/fill/colour-accent scene before deciding what the fighter itself should wear or how it should be shaded. | Shader implementation, fog/film-grain technique, light types, real-time shadow setup, or that an equally dark scene will remain readable in this game's combat. |

The strongest transferable *principle* is not a costume recipe: an individually
readable figure can be sparse and dark when its silhouette, one focal light/face
plane, and the scene's value staging are designed together. That is an inference from
the inspected media plus the creators' stated shadow/lighting intent, not a creator
claim about the stealth fighter.

## Retained first-party media (internal visual-reference use only)

All three assets originate at the official announcement above, role: **first-party
publisher/community announcement carrying Wych Elm's dev blog**. Their exact direct
Steam CDN URLs are recorded below. The files were downloaded only for local research
inspection; no licence granting reuse, redistribution, or incorporation into this
project was found in the announcement. Treat rights as **unresolved / reserved by
the relevant rights holders** rather than as reusable art.

| Local file | What it shows | Direct source / date / observable properties |
| --- | --- | --- |
| [`c1ba084d6e35b5c980b0f6c96be8adcf94733d10.png`](atmospheric-character-references/silver-pines/c1ba084d6e35b5c980b0f6c96be8adcf94733d10.png) | Labeled three-column comparison: “Walker Knock-back” raw footage, edited drawn frames, and in-game. | [Steam CDN PNG](https://clan.fastly.steamstatic.com/images/45060161/c1ba084d6e35b5c980b0f6c96be8adcf94733d10.png), 3 Sep 2026; PNG, 1016 × 347; SHA-256 `7f258a54a0cda3cd8e438f5137cee9d8c06e21c452712c5c239ddf4ba29dd991`. |
| [`f0f6e942d8229181e653fb60a15b0cc9a180c93c.gif`](atmospheric-character-references/silver-pines/f0f6e942d8229181e653fb60a15b0cc9a180c93c.gif) | Split comparison of a filmed walking performance and the in-game Walker walk/flashlight result. | [Steam CDN GIF](https://clan.fastly.steamstatic.com/images/45060161/f0f6e942d8229181e653fb60a15b0cc9a180c93c.gif), 3 Sep 2026; GIF, 479 × 396, 63 frames, 5.04 s reported by `ffprobe`; SHA-256 `d9111e7ccac66a5de0fb430b0ef8c44714d65f802f29c5ee74049eaacb16456c`. |
| [`e120a733f7f7dc8f7cd87bd75dd17dd0b474dcfb.gif`](atmospheric-character-references/silver-pines/e120a733f7f7dc8f7cd87bd75dd17dd0b474dcfb.gif) | Close in-game character motion in a dim interior: a prolonged, restrained change in body posture against a cool, low-key room with pink/red accents. | [Steam CDN GIF](https://clan.fastly.steamstatic.com/images/45060161/e120a733f7f7dc8f7cd87bd75dd17dd0b474dcfb.gif), 3 Sep 2026; GIF, 447 × 512, 207 frames, 20.70 s reported by `ffprobe`; SHA-256 `211dd1df6413d6ba3cf6ec3f035e75ed973fae378a4e55d50877160b90254de6`. |

## Limits and next evidence needed

- **Version limit:** the Steam dev blog predates the 8 October 2026 release; the
  creator interview is launch-day. I did not compare a post-launch build or establish
  whether its images represent every current character/animation revision.
- **Resolution limit:** the retained media are presentation GIFs/PNG, not source
  sprites. They do not reveal native pixel dimensions, drawing resolution, palette,
  layer structure, or export format.
- **Identity limit:** low-key lighting obscures clothing seams, face detail, and
  some limb edges. Do not derive a costume, skin tone, hair treatment, armour shape,
  or facial design from the darkness.
- **Technology limit:** the sources describe a 2D-sprite/3D-simulation result and
  named production approaches; they do not document shaders, exact shadow settings,
  camera values, or a reusable implementation recipe for Godot.
- **Decision still needed:** user visual approval of which *atmospheric principle*
  to borrow—e.g., dark coat-like mass with one bright focal accent, or red/cool
  value staging—before any original concept or native asset work.
