# New keys tote swing: drawn-smear research and bounded implementation choice

- **Status:** research only; no native art, export, Godot scene, or animation timing was changed by this note.
- **Recorded:** 31 October 2026
- **Question:** For this pixel-art tote swing, should the fast swing use a deliberately drawn Aseprite smear, a Godot trail/blur, or a small hybrid—and where is the smallest safe interval to compare it?
- **Scope boundary:** This is guidance for the new-key reconstruction, not approval of any supplied pose, existing attack, gameplay contact, or final visual direction.

## Terms used consistently

| Term | What it is in this experiment | What it is **not** |
| --- | --- | --- |
| **Drawn smear frame** | One deliberately authored, short-lived in-between drawing. It distorts or compresses selected moving forms along the actual travel arc to bridge two readable keys. It can use stretch, tightly controlled multiples, or an abstracted prop/body segment. | A normal pose held too long, a filter, a second copy of the entire character, or permission to hide a broken grip/scale change. |
| **Motion trail / runtime ghost** | A separate render effect that leaves particles, copies, or a path behind an object over time. Godot's `GPUParticles2D` trail is this kind of render mechanism. | The character's authored intermediate anatomy or an evidentiary substitute for a connected tote/hand/handle drawing. |
| **Afterimage / multiples** | Ambiguous term. In a *drawn smear*, multiple partial positions may be composed into one hand-authored frame; in a runtime effect, an afterimage normally means separate old copies persisting across frames. These must be named separately in files and review. | Evidence that the object was structurally connected at the displayed moment. |
| **Generic blur** | Pixel/color averaging or a Gaussian-like post-process. It softens samples; it does not know the character's limbs, grips, tote rim, or collision interval. | An authored pixel-art smear. This experiment's binary-alpha, palette-controlled sprite should not use it on the actor. |

The practical test is therefore not “does blur look fast?” It is whether one **drawn
transition** makes the outbound bag swing easier to follow at game scale without
weakening the readable normal keys. A visual trail is a separate optional effect
question.

## Sources inspected — 31 October 2026

The pages below were inspected as their rendered HTML/text and API/documentation text
on the date shown. I did **not** play videos, scrub animation clips, download or
decode embedded media, or treat still-image captions/search snippets as motion
observation. The cited animation claims are therefore the authors' written guidance,
not a claim that this research watched a demonstrated clip.

| Source | Kind and exact material inspected | Relevant written finding | Practical, bounded implication |
| --- | --- | --- | --- |
| Raymond Schlitter, [*Pixelblog 9: Melee Attacks*](https://www.slynyrd.com/blog/2018/9/8/pixelblog-9-melee-attacks) (accessed 2026-10-31) | Creator-authored pixel-art tutorial; HTML text at lines 45–58. | It calls a smear a non-keyframe for motion/expression, says one can be enough, advises a natural stance-to-follow-through path, and says smears should be few and fast. It separately discusses overshoot and gameplay pacing. | Use no more than one outbound tote-smear drawing in the first comparison; keep the action keys and recovery readable before any effect is considered. |
| Raymond Schlitter, [*Pixelblog 56: Top Down Character Attack Animation*](https://www.slynyrd.com/blog/2025/5/23/pixelblog-56-top-down-character-attack-animation) (accessed 2026-10-31) | Creator-authored pixel-art attack tutorial; HTML text at lines 34–41 and 45–48. | Its phase model puts the smear on the largest wind-up-to-strike leap and explicitly recommends no smear on the recovery leap because it distracts from forward striking motion. The visible follow-through is a clean, held key. | Place the test only between the final counter-wind-up/early-swing key and the committed extension/contact key. Do **not** smear the tote's arrest, recovery, or re-shoulder in this first test. |
| Jesse Bray, [*Art College Crash Course, Lesson 19: Smear Frames*](https://anarchy.mrbray.com/animation-anarchy/2025/3/19/animation-anarchy-the-art-college-crash-course-lesson-19) (accessed 2026-10-31) | Animator/educator-authored lesson; HTML text, including author bio at lines 64–68 and smear guidance at lines 12–53. | It defines a smear as a single stretched/distorted/duplicated drawing for fast motion; it recommends keeping a prop smear to one frame and following the motion arc. | The tote is the moving prop/load; its smear may be deliberately off-model for one frame, but its direction must come from the registered hand-to-rim arc, not from an arbitrary horizontal blur. |
| Canmom, [*Motion blur & smears*](https://canmom.art/animation/smears) (accessed 2026-10-31) | First-party author analysis; HTML text at lines 60–63, 90–101, 103–123, 139–188. | It distinguishes sharp drawn smears from photographic blur, describes stretched in-betweens, overlap/multiple-drawing approaches, and warns that all-frame smearing becomes messy. It also explicitly distinguishes a line-like afterimage example from more form-preserving smear approaches. | Preserve a sharp, opaque pixel drawing with stepped clusters. Do not apply a Gaussian filter or reuse translucent full-character ghosts. If multiples are tested, they are partial bag/handle/arm evidence within one native drawing, never lingering runtime copies. |
| Godot Engine, [AnimatedSprite2D 4.7](https://docs.godotengine.org/en/4.7/classes/class_animatedsprite2d.html) and [SpriteFrames 4.7](https://docs.godotengine.org/en/4.7/classes/class_spriteframes.html) (accessed 2026-10-31) | Official Godot 4.7 API documentation. | `AnimatedSprite2D` plays multiple texture frames through a `SpriteFrames` resource. `SpriteFrames` supports a texture and relative duration per frame, and `AnimatedSprite2D` exposes frame-change/finish signals. The 4.7 page also warns that centered pixel-art textures can deform when positioned between pixels and points to pixel snapping / non-centered placement. | Godot can faithfully **present and compare** a native authored smear at an explicit duration. Register all frames to the same integer root/pivot; do not use the engine to interpolate the character between incompatible keys. |
| Godot Engine, [GPUParticles2D 4.7](https://docs.godotengine.org/en/4.7/classes/class_gpuparticles2d.html) and [CanvasItem shaders 4.7](https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/canvas_item_shader.html) (accessed 2026-10-31) | Official Godot 4.7 API/shader documentation. | `GPUParticles2D` is an emitter; its optional trail is a mesh-skinned particle trail with lifetime/section controls. A CanvasItem shader can draw 2D nodes and has texture/screen samplers and vertex manipulation. These are rendering tools, not character-semantic animation tools. | A Godot trail or shader can be trialed as a separate accent, but it cannot establish grip, tote volume, rim attachment, or a designed pixel silhouette. Do not select it as the principal smear mechanism. Avoid screen/post-process blur on this pixel-art actor. |
| Igara Studio, [Aseprite Animation](https://www.aseprite.org/docs/animation/), [Sprite structure](https://www.aseprite.org/docs/sprite/), [Cels](https://www.aseprite.org/docs/cel/), [Files](https://www.aseprite.org/docs/files/), and [Sprite sheets](https://www.aseprite.org/docs/sprite-sheet/) (accessed 2026-10-31) | Official current Aseprite documentation; HTML text. | Aseprite's timeline controls frames/layers/cels, each frame has a millisecond duration, and a cel is a layer image at a frame and canvas coordinate. `.aseprite` preserves layers, frames, palette, tags, and slices; sprite-sheet export can select visible layers and tag-based frames. | Aseprite is the appropriate source of record for a hand-authored smear cel: it preserves the deliberate drawing, duration, layer ownership, tag, and later local revision. Export transparent frames/sheet only after native review. |

### Software/version boundary

- The Godot facts above are specifically documented for **Godot 4.7**, which is the
  version named in the experiment brief. They do not claim that the currently running
  project or installed editor has been inspected in this research step.
- Aseprite's official documentation is current as accessed on 2026-10-31 but is not
  labelled with a single product version on those pages. It supports the documented
  file/timeline model; this note does not claim availability of any particular MCP
  method or installed build.
- Neither engine documentation nor the animator tutorials proves that this character's
  supplied poses, tote proportions, timing, or final game-scale readability work. That
  remains the required bounded art/runtime test.

## Choice for the first reconstruction test

**Working recommendation: author the character smear in Aseprite, then play the exact
same transparent native exports in Godot.** Treat Godot as the runtime comparison and
optional accent host—not as the generator of the character's deformation.

Why this fits the evidence and the local contract:

1. A drawn smear needs the animator to decide which form remains readable and how the
   motion spans the arc. Here that means the shared hands, two handles, tote rim, and
   bag mass—not a generic texture displacement.
2. The present project requires meaningful native layers/cels and a demonstrated local
   revision. Aseprite's cel/frame structure retains that evidence; a Godot trail does
   not reconstruct hidden joins or make the source revisable.
3. The tote's existing failure mode is structural attachment/proportion drift. A
   runtime effect could make the transition feel faster while concealing exactly the
   thing that must remain inspectable. It must be disabled for structure review.
4. Godot still has a useful role: verify the exact authored timing at intended scale,
   integer placement, playback completion, and whether an optional separate accent is
   helpful or merely noise.

This is a hypothesis to test, **not** a claim that Aseprite-only has already won.

## Bounded authored-smear interval

Use only this first interval:

```text
last normal counter-wind-up key
        -> [one 50 ms native drawn-smear cel]
        -> normal committed extension / contact key
```

- The 50 ms exposure is a proposed test duration, not an approved final frame rate.
  It is short enough to be a single rapid transit beat and must be recorded in the
  animation metadata. If actual played output shows it reads as a held melted pose,
  reduce it once to 33 ms for the same drawing; do not add new smear intervals before
  comparing the result.
- Keep the strike/contact and follow-through as normal, readable keys; keep recovery
  clean. This follows the current Slynyrd attack guidance and confines off-model
  deformation to the action's maximum forward leap.
- The smear must not change the registered root, planted-foot contacts, global head
  scale, torso/pelvis volume, or the approved canvas/pivot. It is an exception only
  for the fast-moving forearm/wrist → handle → tote-rim/body chain.

### What to draw in that cel

1. Keep head, torso/pelvis mass, planted legs/feet, and the near shoulder readable
   from the normal key interpolation. Do not stretch the whole character.
2. Draw the two gripping hands at their continuous shared-bundle position, or retain
   the more readable hand as a fixed anchor if both cannot be read at this speed.
   There must be no empty gap from hand to handle bundle.
3. Draw both handles as a connected, tapering/stepped bridge to the tote rim. Their
   visible curve may flatten under speed, but they may not fork, telescope, or stop at
   an unrelated bag edge.
4. Compress/elongate only the tote's *moving* rim/body silhouette along the measured
   hand-to-bag arc. Use the existing opaque palette and crisp stepped clusters; no
   semi-transparent blur, filter gradient, or soft halo. Preserve enough tote body to
   distinguish a flexible bag from a sword-like streak.
5. If a partial multiple is needed, use at most two decreasing rim/body marks within
   the **same cel**, both connected to the intended direction. Do not duplicate the
   head, torso, legs, or full bag as a trailing ghost.
6. The next normal contact key must immediately restore the tote's normal volume,
   handle length, and anatomy. It is the proof that the smear is intentional
   deformation rather than unresolved scale drift.

## Controlled comparison proposal

All variants use the same normal keys, phase duration, palette, canvas, root/pivot,
collision/contact event, and Godot camera/filter. The A/C control uses an on-model
50 ms conventional in-between so that the comparison tests *deformation*, not merely
the addition of a frame. Only the indicated transition/render choice varies. Keep the
entire comparison in one native candidate lineage and label the exports unambiguously.

| Variant | Native drawing change | Godot change | Purpose / decision rule |
| --- | --- | --- | --- |
| **A — no-smear control** | One 50 ms, anatomically on-model conventional in-between; no stretch, multiple, or abstracted form. | No particles, ghost, shader blur, shake, or speed-line effect. | Baseline: does the new pose sequence already read? It prevents crediting an effect or simply one more exposure for a repaired key drawing. |
| **B — authored-smear candidate** | Insert the single 50 ms Aseprite smear cel specified above. | Play exactly those exports through `AnimatedSprite2D`/`SpriteFrames`; no extra effect. | Preferred first candidate. Select only if it improves the outbound path at game scale while every normal key and attachment remains clear when paused. |
| **C — runtime-trail probe** | Same source as A; no native smear. | One deterministic, very short Godot particle/trail or equivalent ghost accent, confined to the tote path and disabled outside the outbound transition. No blur. | Tests the user's Godot preference without conflating it with a hand-drawn deformation. Reject if it reads as a detached duplicate/afterimage or obscures the bag-to-hand evidence. It is an effect comparison, not a replacement native source. |
| **D — hybrid probe (only if B and C each have a distinct benefit)** | Same authored smear as B. | Add C's minimum accent, still separately toggleable. | Keep only if B supplies coherent form and the effect adds a measurable reading benefit at game scale without visual noise. Otherwise retain B or A, never the accumulated combination by default. |

For each variant, export both authored-speed playback and identical isolated Godot
capture with the same start/end markers. Review at native size, integer enlargement,
and intended gameplay scale. The comparison sheet must include the previous normal key,
the transition, and the following normal key; an isolated attractive smear does not
pass.

### Pass/fail questions

- Does the viewer identify one tote moving from the shared grip toward contact—not a
  detached blurred bag or two whole bags?
- Are root, feet, head size, torso width, arm length, handle roots/rim, and tote volume
  unchanged across the surrounding normal keys?
- Does the single transit clarify the arc at gameplay scale without becoming a readable
  malformed held pose when paused?
- Does the no-effect view remain structurally credible? If not, repair the keys rather
  than tuning a trail or blur.
- Does C or D add information rather than just brightness/noise? If not, remove the
  runtime effect and preserve the native candidate.

## Required evidence when this is executed

1. A native Aseprite inspection listing the actual smear cel owners, duration, tag,
   canvas and integer root/pivot; include owner-isolated, hidden, marked handle-root,
   and neighboring-frame views under the connected-form procedure.
2. A corresponding no-smear export and an authored-smear export, with the same frame
   order/timing metadata except for the inserted smear frame.
3. A Godot 4.7 playback/capture of A and B; C/D only if the optional runtime effect
   is actually implemented. Record whether filtering/pixel snapping and the sprite's
   placement preserved crisp pixels.
4. Visual decisions separated into structural readability, motion/timing, material
   treatment, technical export/reopen, runtime execution, and user artistic approval.

## Unresolved uncertainty

- The six new pose images have not been visually inspected by this research note, so
  it does not assert their true order, exact strike arc, or that the nominated
  counter-wind-up-to-contact transition exists unchanged after structural conversion.
  The construction owner must map the actual registered keys first. If the largest
  forward leap is elsewhere, relocate this **single** trial to that measured outbound
  interval rather than forcing it into a label-derived stage.
- The intended tote load, contact timing/hitbox, final action duration, camera scale,
  and user preference between crisp deformation and an added effect remain open.
- The term “afterimage” remains overloaded across animation practice. This experiment
  resolves it operationally through explicit variant labels and frame evidence rather
  than claiming a universal terminology standard.
- No source here certifies a universal 50 ms exposure, a particle configuration, or a
  visual result for this character. Those are deliberately bounded hypotheses for the
  with/without playback review.

## Next owner/action

The construction owner should first register the new keys and prove the tote/hand/handle
chain in normal keys. Then build variants A and B; only build C and D if the runtime
preference comparison remains useful after that honest no-effect check. Preserve all
variants and report the exact reviewed exports, engine version actually observed, and
the user's visual decision separately from technical playback.
