# Style guide

Updated: 30 October 2026.

## Approved visual target

The user finalized the original character and rendering direction in the [full scene](../../assets/references/approved-2026-10-26/character-scene.png) and [close-up](../../assets/references/approved-2026-10-26/character-closeup.png). The subsequent [isolated character](../../assets/references/approved-2026-10-26/character-cutout.png) is a supporting construction reference. Preserve the scene/close-up when the cutout introduces edge artifacts. Approval covers the design and concept appearance, not the reconstructed sprite or an animation.

The earlier generated male lighting study was rejected for smoothness and style mismatch. Its B lighting was preferred within that comparison only. It does not override the newer finalized references.

## Clarified fidelity and supplementary references

The target is recognizable identity, expression, aesthetic and vibe; pixel-perfect
copying is not required. Simplify secondary detail before changing the face, hair
silhouette, proportions or selective-contour/cluster language. Small differences are
acceptable when the same character/style survives. Traced boundaries, source-derived
colors and converted seeds are allowed with provenance and deliberate finishing.

Separate invariant design (tied brown hair/fringe, face proportions, costume/materials)
from pose-specific expression and scene-specific warm/cool lighting. New expressions
may follow an action while retaining identity. Register additional images by role;
compare them with originals before use. Generated simplifications cannot silently
replace identity/style anchors. Do not read the earlier rejected flat-background
experiment as a universal ban on all reference-assisted methods.

## Animation appearance direction — 30 October 2026

The user prefers the game-suitable appearance of the [earlier Terra-left/Sol-right comparison](../experiments/2026-10-30-natural-idle-sol/proof/terra-left-sol-right-3x.gif),
despite its motion defects; no particular side was selected in this feedback. The
[latest redraw](../experiments/2026-10-30-redrawn-breathing-sol/proof/neutral-3x.gif)
is rejected for apparent clothing color/shading changes. Preserve the earlier pale
shirt, olive jacket and their characteristic shade/texture relationships when
developing new poses. This is appearance direction, not approval of either animation
or a frozen-pixel requirement. The [motion guide](motion-guide.md#animation-procedure)
routes sequence work to the detailed continuity review. No art was revised by this
workflow update.

## Reference feasibility and preservation priorities

The approved concept's appearance remains the target. The rows below are a **proposed translation strategy**, not approval of a new sprite or proof that a grid can support every cue. Use the [concept-to-native research](../research/concept-to-native-pixel-art.md) and [feasibility workflow](../workflow/art-production.md) before a fresh reconstruction.

| Priority | Preserve or test | Permitted study simplification |
| --- | --- | --- |
| Identity and structure | Rightward three-quarter face; unequal near/far eyes and rightward gaze; restrained, slightly uneven smile; soft cheek/jaw; distinctive broken fringe; overlapping tied hair, pale tie and loose silhouette strands | Combine small strand interiors while retaining the fringe openings and tied-hair silhouette. Test eye/eyelid/mouth separation rather than replacing the face with generic symmetric marks. Exact pixel positions remain unapproved. |
| Body and costume identity | Natural tall proportions, relaxed standing pose, olive open hooded jacket framing an off-white shirt, broad blue jeans, pale shoes, cream tote and continuous strap | Reduce fold/seam counts while preserving waist, sleeve/hood overlaps, wide-leg negative space and tote attachment. No chibi redesign or costume replacement. |
| Secondary surface detail | Small hair glints, blush texture, fabric specks, minor sneaker seams | Omit or merge marks that compete with face/hair readability. A deliberate one-pixel pupil or corner remains valid; no blanket noise-removal rule. |
| Atmosphere and scene | Warm urban sunset, warm practical lights against cooler distance, depth and focal contrast | Test large environment color planes and separate lighting/effect layers. Preserve neutral material identity in the sprite; do not bake the full scene's glow, distant texture or grading into every frame. |

**Provisional feature budget:** in each study record the actual face/hair envelope and approximate near-eye, far-eye, fringe, nose and mouth footprints. Mark visible separations that merge at the intended display size. A budget is a tested allocation of space, not a minimum eye size or fixed palette count. Resolve orientation, skull/hair mass, eyeline and cheek/jaw before adding strand or lash pixels. If an identity feature remains unreadable after the declared structural passes, preserve the result and compare a separate grid/rendering variant.

**Native versus display scale:** 128x192 with 184px drawn height remains the existing provisional full-character baseline. 192x288 and 256x384 are study equivalents only. Larger native art must contain newly authored information; enlarging the existing sprite changes display size alone. Record crop/full-character equivalence, visible bounds, projected game height, camera/filter assumptions and any preview resampling. No production grid or gameplay display size is selected here.

**Rendering proposals to test:** hair as overlapping masses with selective fringe openings before isolated strands; face as a coherent turned plane with separate near/far feature clusters; reusable material shadow/base/light roles without a fixed number of shades; selective material-colored contours; deliberate opaque intermediate edge colors only where the brief permits hand anti-aliasing. Automatic smoothing is not a replacement for cluster construction. Preserve existing alpha/palette locks in local corrections.

**Environment consistency:** compare character and background at a common display scale for cluster density, contour strength, value contrast and lighting direction. Background depth may use quieter contrast and broader shapes; consistency need not mean identical detail everywhere. The drawn scene is an available provisional context, not a visually approved production environment. Dynamic light, grading, shader or parallax choices require a later Godot comparison and remain proposed.

The [resolution feasibility record](../experiments/2026-10-27-resolution-feasibility/record.md) owns current study status and results. Use independent review dimensions in the workflow; file validity, agent judgment and user acceptance remain separate.

## Visual rules for the standing reconstruction

| Property | Decision | Evidence |
| --- | --- | --- |
| Rendering | Deliberate visible pixel clusters; avoid smooth image-filter appearance | Approved images and user's explicit correction |
| Design | Brown tied hair with loose fringe/cowlick and pale tie; olive open hooded jacket; off-white tee; high-waisted wide blue jeans; pale sneakers; cream shoulder tote | Approved close-up and full body |
| Proportions | Preserve the long-leg silhouette and reference head/body relationships; no chibi redesign | Full-body reference |
| Pose | Three-quarter front, face turned right, hands in pockets, one leg angled outward | Full body and cutout |
| Colors | Preserve material identity and warm skin; avoid importing environmental glow as a fixed full-body orange tint | Approved originals |
| Outlines | Selective material-colored dark contours, restrained interior seams | Approved images |
| Shading | Large readable planes before small fold/strand accents; no random texture or soft gradients | References and construction study |
| Test canvas | 128x192, drawn bounds x32..103/y2..185, anchor y186; provisional choice by agent, not Until Then's actual native dimensions | Standing v01 export checks |
| Palette | 45 visible opaque RGB colors in v01; prototype palette, not a user-approved color-count restriction | Export checks |
| Camera/gameplay size | Static reference pose for this test. Full gameplay camera remains open; actual Godot scale is untested | Scope boundary |
| Weapon/attack | Not selected; no new weapon or combat costume added | Current request is one standing reconstruction |

## Construction and revision

[Standing v01](../../assets/source/standing-v01/standing.aseprite) is an agent-drawn candidate with 12 named layers and reproducible [Lua drawing instructions](../../assets/source/standing-v01/draw.lua). The reconstruction script reads no reference raster. References were used by the agent for proportions and appearance; reduced reference images exist only in labeled comparison previews.

The [comparison](../../assets/previews/standing-v01/comparison.png) makes fidelity limits visible: face/hair shapes differ and jacket/denim folds are simplified. The generated reference remains authoritative. The tote-color variant is a local-edit proof only; cream remains the approved main design.

## Approval history

- 25 October: Until Then carnival image strongly preferred as general reference. No copying its character designs.
- Later feedback: lighting B preferred; earlier generated rendering rejected as too smooth and unlike Until Then.
- 26 October: user explicitly finalized the new original character and look, supplied close-up/full body and then isolated character; authorized native Aseprite reconstruction.
- Standing v01: user responded “Good!” and requested continued refinement, face first. This is positive feedback, not final sprite/animation acceptance.
- Standing v02: [face-first refinement](../../assets/previews/standing-v02/face-before-after.png) and [full-body comparison](../../assets/previews/standing-v02/full-before-after.png) ready for review. Face/neck corrected first; then hair and selected fabric/shoe details. Main native source is [v02](../../assets/source/standing-v02/standing.aseprite); v01 preserved.

See [experiment evidence](../experiments/2026-10-26-standing-reconstruction/record.md).

Current refinement evidence: [v02 record](../experiments/2026-10-26-standing-refinement/record.md). v02 retains the same grid and anchor, with 51 visible opaque colors; no palette-count rule is imposed.

## Current v03 head-only boundary

The user identified v02's remaining far-eye/profile and hair-identity problems. [v03](../../assets/source/standing-v03/standing.aseprite) uses v02 as the base, bringing pupil positions to x64/x70 with a narrower far eye, subtle uneven brows/smile, rounded cheek/chin contour, partial ear coverage and overlapping rear-hair clumps. [Original / v02 / v03 comparison](../../assets/previews/standing-v03/head-before-after.png) awaits review. No new colors, body/neck edits or resolution changes. Future corrections stay within this boundary unless the user explicitly expands scope. See the [v03 record](../experiments/2026-10-26-head-v03/record.md).

## Current v04 shoe refinement

The user subsequently requested slightly more detailed shoes, authorizing this specific exception to the prior head-only scope. [v04](../../assets/source/standing-v04/standing.aseprite) carries forward v03's head unchanged and adds restrained lace, panel and sole details. Shoe shape, stance and existing palette remain unchanged; all other layer images are identical to v03. [Comparison](../../assets/previews/standing-v04/shoes-before-after.png); review pending.

## Static background context

[Street preview](../../assets/previews/street-preview-v01/street-scene-4x.png) places exact v04 in a cleaned version of the original background. This is a static appearance test, not a new character revision. The 352x264 scene scale is provisional, and the background is a flat generated clean plate with separate character and grounding shadow in the [native scene](../../assets/source/street-preview-v01/street-scene.aseprite). Review pending; no environment-asset or gameplay validation inferred.

## Current environment construction requirement

The user explicitly rejected using the flat cleaned image as the background because it looked inconsistent. Continue from the [Aseprite-drawn scene](../../assets/source/street-drawn-v01/street-scene.aseprite) and its [16-layer background](../../assets/source/street-drawn-v01/background.aseprite). This environment uses the same native grid, large color planes, clustered plants and restrained contours while preserving exact v04. No reference raster is imported. The composition remains a simplified interpretation and awaits visual approval; the earlier plate is only a historical placement experiment. See [drawing evidence](../experiments/2026-10-26-drawn-background/record.md).
