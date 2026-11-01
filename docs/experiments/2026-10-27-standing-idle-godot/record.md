# Full standing idle and first Godot scene

- Date: 27 October 2026. Status: prototype implemented; agent visual review, user art approval pending.
- Base revision: `9e35c5c13987a153e942e6f93f49f247fad13c3a`; local/uncommitted.
- User request: full standing character, quiet idle and a simple scene; try buildings separately.
- Later user constraint: use MCP tools, no computer use; report missing capabilities.
- No repository-wide Definition of Done exists. This record applies to the bounded scene experiment.

## Subsequent workspace MCP installation

The user then authorized installation of needed MCPs for this workspace and prohibited
Code-MCP. A pinned dedicated Godot MCP is now installed/configured project-locally.
Real stdio MCP calls verified version, project inspection, run/debug/stop, eight rendered
frames, two actual idle loops and no runtime errors. See [MCP smoke evidence](godot-mcp-install/mcp-smoke.json)
and [setup guide](../../../tools/godot-mcp/README.md). No Code-MCP or computer-use tool was
used for this installation. The active chat catalog has not exposed the new server yet;
workspace/chat reload may be needed. Earlier unavailable-capability statements below
record the preceding state and are superseded only by this observed protocol boundary.
Independent strict binary/header/full-hash audits are still unrun.

## Outcome and evidence

A separate source-assisted full standing character now has fourteen meaningful visible-part layers
and eight native animation frames. It retains the original pose/outfit and uses a one-pixel upper-body
inhale plus blink, with the lower body planted. One scene and the first shop's visible parts exist.
Actual Godot runtime playback was observed before the user imposed MCP-only operation. Native-file
inspection, pixel checks and review-scene construction/exports then continued through MCP only.

| Deliverable | Artifact |
| --- | --- |
| Full character native master | [standing-idle.aseprite](standing-idle.aseprite), 96x216, fourteen layers, eight frames |
| Static seed and cleanup | [standing-seed.aseprite](standing-seed.aseprite), [standing-cleaned.aseprite](standing-cleaned.aseprite) |
| Original/actual review | [static-seed-review.png](static-seed-review.png), [static-cleaned-review.png](static-cleaned-review.png) |
| Idle at 2x | [idle-filmstrip.png](idle-filmstrip.png); [MCP-exported GIF](idle-preview-mcp.gif) |
| Runtime strip/atlas | [idle-sheet-mcp.png](idle-sheet-mcp.png), [metadata](idle-sheet-mcp.json) |
| Review-scene native master | [standing-scene-idle-mcp.aseprite](standing-scene-idle-mcp.aseprite) |
| Review-scene animation | [scene-idle-preview-mcp.gif](scene-idle-preview-mcp.gif), exported through Aseprite MCP |
| Environment visible parts | [environment-parts.aseprite](environment-parts.aseprite), thirteen layers |
| First shop | [shop-visible-parts.aseprite](shop-visible-parts.aseprite), six visible-part layers; [MCP preview](shop-preview-mcp.png) |
| Local building revision | [shop-lamp-edit.aseprite](shop-lamp-edit.aseprite), 54 lamp pixels changed; other five layers protected |
| Runnable Godot project | [project.godot](../../../godot/standing-idle-lab/project.godot), [GDScript](../../../godot/standing-idle-lab/preview.gd) |
| Actual Godot observation | [observation.json](../../../godot/standing-idle-lab/evidence/observation.json), [frame events](../../../godot/standing-idle-lab/evidence/frame-events.json) |
| Actual rendered scene | [runtime-final-scene.png](../../../godot/standing-idle-lab/evidence/runtime-final-scene.png) |
| Actual closed-eye pose | [runtime-idle-closed-inspection.png](../../../godot/standing-idle-lab/evidence/runtime-idle-closed-inspection.png) |
| Actual isolated building | [runtime-shop-only.png](../../../godot/standing-idle-lab/evidence/runtime-shop-only.png) |

## Inputs, native scale and provenance

Approved scene and close-up remain identity/style anchors. The earlier cutout was inspected but its
pixels were not used because its edges/face differ. The existing generated clean plate is supporting
scenery material for this separate experiment. Its earlier rejection remains historical; neither that
plate nor this new converted environment has new user visual approval. Older drawn scenery is untouched.

Character source crop: (448,208)-(800,1040), 352x832 source pixels. BOX reduction at 4:1 yields
88x208, placed with four-pixel padding in a fixed 96x216 native canvas. The complete scene art region
is 362x272. Character origin is (108,48), matching the original composition; camera/facing is this
standing three-quarter view only. This grid is provisional, not a final full-game resolution.

A 64-color source-derived character palette and 96-color environment palette are experiment choices,
not new project caps. Character/environment share the spatial reduction. Native scene composition
uses their union (161 entries including transparency) without repainting either source's pixels.
The runtime consumes its own exported pixels. It does not load or require the original reference image.

Source-coordinate silhouette/ownership masks and processing are retained in [prepare.py](prepare.py),
[construction-data.json](construction-data.json), prepared/, [data.lua](data.lua) and [build-static.lua](build-static.lua).
Visible-part separation does not infer hidden surfaces. [clean-static.lua](clean-static.lua) removes
491 warm background-contaminated samples from the denim layer in its declared lower-body band;
it does not apply a blanket speckle or smoothing pass. The actual before/after exports were inspected.

## Motion

[animate.lua](animate.lua) constructs eight native frames on the same grid and palette. Durations:
700/650/50/100/70/600/500/330 ms, a 3000 ms loop. The inhale lifts head, upper clothing, hands,
strap and tote by one native pixel; the jacket transitions back at the waist. Denim and both shoe
layers remain pixel-identical across all frames. There is zero root travel or per-frame bounding-box fit.
Existing reviewed generated blink reference from the previous bust study supplies eyelid guidance only.
No newly generated pixels or large portrait head were pasted onto the full-body asset.

Frames: rest, inhale, half blink, closed, half blink, inhale, exhale, rest.
The filmstrip and actual engine captures were visually inspected. The pose/outfit/volume remain
recognizable and shoes remain on the pavement. At this smaller face scale, expression is softer
than the portrait study. Breathing currently uses two pixel positions, so the transition is visibly
stepped when magnified. This is a quiet prototype, not full cloth/hair physics or combat validation.

## Buildings

The environment master has thirteen visible-region layers. The first shop has six native parts:
wall, glass, awning, posts, steps and lamp. A duplicate-only lamp-color revision changes 54 native
pixels while the other five layer images, exposed layer metadata, palette and frame durations stay equal.
This is an editable first-building view, not six architectural models. Plants/other visible occluders
remain in some samples. Hidden walls, reversed views, seamlessly movable/parallax cutouts and the rest
of the buildings remain unfinished. Work on one complete building can follow user selection of this scene.

## Documentation used

Current Godot 4.7 documentation was queried through Context7 on 27 October 2026:
[SpriteFrames frame durations](https://github.com/godotengine/godot-docs/blob/4.7/classes/class_spriteframes.rst),
[Viewport capture](https://github.com/godotengine/godot-docs/blob/4.7/classes/class_viewport.rst), and
[integer resolution scaling](https://github.com/godotengine/godot-docs/blob/4.7/tutorials/rendering/multiple_resolutions.rst).
These document mechanisms; local playback evidence is reported separately below.

## Actual Godot boundary

Installed Godot 4.7.2.stable.official.ed1daf0bf ran with the OpenGL/Metal compatibility renderer on
Apple M3 Pro. Static runtime was inspected before adding motion. Final art region remains 362x272;
viewport is 362x304 with a separate 32-pixel controls area, nearest filtering and integer stretch,
default 724x608 window. Two idle cycles, all eight frames, the paused closed pose and isolated shop
were captured by the running engine; root stayed at (108,48). Runtime finished with exit code 0.

This engine work used the existing CLI before the later MCP-only constraint. It is not Godot MCP proof.
Native CUA access was not approved; no native UI inspection or real keyboard/button input is claimed.
Controls are implemented but OS-input behavior is not verified. Initial headless editor import had
a shutdown cleanup crash; the later idle import and graphical runtime completed. Logs are retained.
No engine installation or global permissions/configuration was changed.

The scene is a scale/appearance/idle experiment. It has no collisions, player movement, attack, combat
contact or exported game build. No game production-readiness claim follows from two idle loops.

## MCP-only continuation and checks

- Aseprite MCP preflight READY, headless; Aseprite 1.3.18.6-dev, Pebbly 0.8.2.
- Native inspection confirms 96x216, fourteen layers, eight durations and idle-standing tag.
- [mcp-pixel-checks.json](mcp-pixel-checks.json): binary alpha; fixed feet region; exact return to rest;
  all eight native denim/shoe/far-shoe cels pixel-equal; blink changes only the declared eye regions.
- [mcp-shop-edit-checks.json](mcp-shop-edit-checks.json): 54 lamp pixels changed, zero changes in the
  other five native layer images; exposed palette/layer/frame metadata equal.
- [mcp-scene-checks.json](mcp-scene-checks.json): scene saved/closed/reopened through MCP; every placed
  character frame matches the native source exactly, zero pixel differences at the fixed origin.
- Scene review master keeps thirteen background layers and one runtime-composited character layer.
  The fourteen-part character master remains separate; the preview master is not claimed to retain
  fourteen semantic character layers internally. Background cels are intentionally shared across frames.
- MCP GIF/strip/atlas and scene GIF exports succeeded; actual MCP preview images were inspected.

Missing capabilities: no Godot MCP tool is exposed; no dedicated Aseprite validate tool is exposed
despite its preflight feature advertisement. Code-MCP execution discovery refused this workspace because
it has no supported package metadata for its deterministic Node/Cargo/Python/Gradle/Maven adapters.
Therefore the independent binary header/strict preservation checker and fresh full hash audit were not
rerun after the MCP-only instruction. Do not report those checks as passing. Do not add fake project
metadata, broaden permissions, install integrations or substitute CLI/CUA to bypass these limits.

Pre-task source hashes are in [preserved-inputs.json](preserved-inputs.json); no earlier artwork was
intentionally written. Full source-byte audit remains pending. Construction scripts and old attempts
are retained; native reopen exports were generated before restriction, and MCP reopen/pixel checks
provide the fresh observed boundary above. No commit, push, publication or new paid service.

## Decision and next owner

This bounded standing-scene/idle prototype is available for user review. User selects likeness,
scene density, scale and motion restraint. Agent then improves the selected full-body face/edges or
finishes the first shop's masks/hidden areas before producing another building. Camera, combat and
final production scale remain open. Continue with MCP tools only and report unsupported capabilities.
The dedicated Godot MCP is now installed/protocol-tested; direct chat tools await catalog refresh.
Continue with dedicated MCP tools, no computer use and no Code-MCP. Further needed MCP installation
is authorized only for this workspace; no paid service/global authority change is implied.
