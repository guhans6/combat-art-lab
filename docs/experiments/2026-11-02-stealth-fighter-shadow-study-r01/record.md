# Current A:152px and shadow/readability investigation

Date:2November2026. User likes the playground, prefers152px between B128andC160, and questions excessive painted shadow/missing detail and future lighting/animation readability. Scope: investigate actual references and source behavior, set152px as working display size and provide an isolated lighting demonstration. No native refinement was requested or performed in this investigation.

## Inputs, roles and routing

Current A appearance source assets/concepts/stealth-fighter/game-specific-r01/silver-pines/corrected.png, SHA256a3cc3ab1d658ac3d2d464ef4781ed966e815c7eedeefcf5801d81ca93924ab9c. Accepted main idle native assets/source/stealth-fighter/idle-r02/idle.aseprite SHA256f4cb8fff0a460cde6845fb15bc0c5e3271259d9d38d5f3efa051e4970b2e6127;128×264canvas/240pxrestbody/nine semantic layers/four1800ms entries. Exact runtime PNGs retained. Original quiet sparse design and idle motion remain; the amount of darkness is explicitly reopened by latest feedback.152px is a preferred display test, not a native-grid or final lighting approval.

Research skill applied with a fresh-context GPT-6.1TerraMAX agent, per explicit user model request. Lead normal implementation/review is GPT-6.1Sol. No 5.6/Astra assignments or image generation. Dedicated GodotMCP used for all engine starts/output/stops. No direct editor CLI, computer use, native writes, new integration/purchases, commit or publication. Existing pixel-art-director research/comparison evidence boundaries retained; actual native art untouched, so no native mutation/repair gate invoked.

## Research and observed diagnosis

Full cited findings: docs/research/stealth-fighter-shadow-readability-2026-11-02/findings.md; exact primary image URLs, crops and hashes in provenance.json. Selected visual references: Silver Pines actual in-game/drawn/filmed dev-blog frames; Blasphemous combat screenshot; Hyper Light Drifter campfire screenshot. Lead independently opened all3selected views plus our actual152px lighting captures. These are still observations, not continuously perceived playback or inferred shader implementations. Game screenshots are limited research references only; no production reuse or redistribution license was established, and they are not playground assets. Unselected research downloads/contact sheets excluded from delivery.

The existing Current A correction intentionally merged arm/torso shadows and trouser boundaries and omitted eye marks. Root's original playground used exact PNG colors without lights, CanvasModulate, tint or shaders. Terra independently read/composited all4native frames and confirmed exactRGBAexports. At152px the face, hand, shoulder and outer silhouette survive, while the near arm/vest boundary and upper-leg separation are weak. Source darkness predates runtime lighting.

Silver Pines provides a direct contrast: a mid-brown coat and readable planes in the drawn character are subdued in its dim actual scene. This demonstrates distinct drawing/presentation contributions without establishing that game's shader settings. The selected Blasphemous still uses light armor/helmet and a pale slash against dark brown staging; effect obscures bodies, so it proves no anticipation/timing. HLD's red/pink focal character against dark-violet areas is another contrast strategy, not a requested new saturated palette or anatomy reference.

## New playground study

New saved project godot/stealth-fighter-playground-r02, preserving r01. Default Single/B152px/source colors. Comparison defaults128/152/160px. Same fixed1200×480world inside1280×800viewport, groundline558, shared4entry[700,260,500,340]ms clock. Existing view/selection/slider/pause/frame/speed/guides/reset/fullscreen controls retained.

Light button / L cycles exact source colors (ambientwhite and no point lights), dim room (0.35ambient), and dim room plus3equal warm PointLight2D fills (energy1.8, procedural512radialGradientTexture2D, scale0.9). World CanvasLayer-1 isolated from interface Canvas0. Actual 2D runtime lighting, no normals/specular maps, cast-shadow occluders or altered character pixels. Strong fill is diagnostic, not a proposed final lighting design: face/skin can become over-bright while the vest and legs remain broad dark shapes. Ordinary lights can change existing colors/spatial illumination but cannot recover a specific material/fold/shape that was never drawn. Extra surface maps require authored information and are not the recommended next action.

Godot official4.7 docs checked via Context7 and primary pages: https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html ; classes/class_canvasmodulate.html ; classes/class_gradienttexture2d.html ; classes/class_light2d.html ; classes/class_pointlight2d.html. No image-derived technique guesses.

## Focused fresh verification

Dedicated Godot4.7.2.stable.official.ed1daf0bf/localmacOS/OpenGLCompatibility/AppleM3Pro test copy:19mouse/key/state checks pass;>=3authored loops; finalerrors[]. Covers defaultSingle152, mouse/keyboard lighting modes and return, comparison/single, selection/height slider, pause/step/resume, speed/guides, reset152/lightneutral. Actual neutral four native-scale captures have0opaqueRGBmismatches. All4at152px unambiguous nearest samples match source exactly. Measured128/152/160bodyheights and common bottom row557pass. Exact mathematical texel-boundary samples are excluded only from fractional-projection color oracles: CPUdouble/GPUfloat nearest tie resolution differs at19/30scale. Native1xchecks remain strict; no added color-error tolerance. This is a sampling diagnostic limit, not an art change.

Runtime light effects confirmed in screenshots and sampled actor luma: unlit38.15,dim12.97,fill65.36meanY8 over the same unambiguous actor pixels. Counts are diagnostics, not art scores. All interface pixels outside the lighting control remain identical across modes, confirming world/UI separation. Native/PNG file hashes remain exact. Actual cropped scene comparison is lighting-comparison-2x.png, crop[560,350,720,582], nearest2×, no art repaint/grade. Root inspected clean source/lamp wholeviews and this3modecrop. Screenshots are static render evidence; user temporal evaluation remains separate. Test instance stopped. Saved final project launch/status recorded separately.

## Decision and next boundary

152px retained as working display preference. Dark sparse rendering was intentional, but excessive merging is not a required style rule. Recommendation, not performed: one separate restrained value-separation pass for near arm/vest and front/rear upper legs, checking belt/indigo only as needed. Preserve silhouette, no-eye face, hair/beard, outfit, color families, native grid, weapon and accepted idle timing. Compare all4frames at152px under the same neutral and lamp conditions. Keep quiet broad planes; do not restore fine noisy detail or treat a uniform exposure lift as a shape redesign.

This study does not prove future attack readability, intent/telegraph timing, full moveset consistency or final dynamic-lighting performance. Attack windup/contact/recovery should later be judged effects-off and at actual speed. Next owner: user reviews the explained examples and current152px light toggle; agent owns a separately authorized native readability refinement. No character source was replaced, no public release or executable export performed.

Final saved r02 project launched through dedicated GodotMCP: SHADOW_STUDY_READY observed, errors[]. Script/config bytes equal the tested copy; no RUN_CHECKS marker. Left open at Single152 / Sprite colors. See evidence/live-launch.json.
