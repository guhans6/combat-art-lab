# Gameplay view explorations — 2026-11-01

Built-in image generation, two calls. Original returned PNGs copied unchanged. These are concept explorations, not native sprites or gameplay validation. The reference is provisionally accepted for direction, not a final identity lock. Requested size was not specified; actual dimensions are 1024 × 1536 for both.

## Reference

`assets/concepts/stealth-fighter/atmosphere-r01/A/simplified-01.png` — identity, outfit and rendering anchor; SHA-256 `e1dcf18e72ce22b8b6c6031d0f00da91259dcbf4c2bfbb0e0c12c8d1c56b6e1e`; 1024 × 1536 RGB. The second call additionally used `side.png` for companion view, framing and pose.

## side.png

Source: `/Users/guhan/.codex/generated_images/01a197f2-2da0-76c3-8a58-347220b7fb3c/exec-e2f19d16-5ac9-4f3d-a1b7-308149bbfb8b.png`. SHA-256 `4a4ab8abf0cdd252cb7923cdd0e034e274a508969b422bed1cecf648d5346368`. RGBA; alpha 0–254, transparent corners, 25,151 pixels alpha 1–127; alpha-positive bounds (267, 48, 922, 1490), alpha ≥128 bounds (333, 52, 685, 1482), coordinates left/top inclusive, right/bottom exclusive.

Exact prompt (transparent_background=true; reference image 1 as above):

> Use case: stylized-concept. Asset type: transparent full-body gameplay character view exploration. Input image 1 is the provisional identity, costume and rendering anchor; preserve this same character and outfit, not a redesign. Render him in a strict right-facing orthographic side view at eye level, as a side-scrolling game's idle-ready stance: head, torso, hips and feet all aligned in profile, no visible top planes. Full body including all hair and both boots, centered with clear margins. Lean naturally proportioned young adult brown-skinned male, long dark half-tied hair, visible face and light stubble; muted indigo split-hem tunic, charcoal light shoulder armor, worn steel forearm guard, brown waist wrap with small rust buckle, dark trousers and boots, compact sheathed one-handed sword. Preserve the reference's distinctive shapes and material colors. Quiet deliberate pixel clusters and broad shadow masses, restrained warm edge and cool shadow, no environmental glow; stylized game pixel art, not realistic, anime or chibi. Actual transparent alpha background; no floor, scenery, cast shadow, border, lettering or UI.

Self-review: Complete figure and recognizable costume, but strict profile is not met: torso and boot tops retain near-side depth. The posture is more upright portrait than ready stance. A visible semi-transparent warm halo remains despite the prompt, so this is not a clean cutout. Fine face and hair detail remains relatively dense.

## quarter.png

Source: `/Users/guhan/.codex/generated_images/01a197f2-2da0-76c3-8a58-347220b7fb3c/exec-4126fb26-165d-4553-a8d0-6c5711de465e.png`. SHA-256 `c57a91c1fa592d7f752e98978dff7297a238ec4a57b30294a1477856ce17e2e4`. RGBA; alpha 0–254, transparent corners, 34,464 pixels alpha 1–127; alpha-positive bounds (0, 37, 1008, 1536), alpha ≥128 bounds (327, 61, 754, 1465), coordinates left/top inclusive, right/bottom exclusive.

Exact prompt (transparent_background=true; image 1 is the anchor and image 2 is side.png above):

> Use case: stylized-concept. Asset type: transparent full-body gameplay character view exploration. Image 1 is the provisional identity, costume and rendering anchor. Image 2 is the companion side-view study and the reference for pose, framing, figure scale and lighting. Preserve the same character and outfit, not a redesign. Render a shallow near-side right-facing gameplay view at eye level: mostly profile with only a small reveal of the chest, head facing right; idle-ready stance. Full body including all hair and both boots, centered with clear margins, same apparent scale and pose as image 2. Lean naturally proportioned young adult brown-skinned male, long dark half-tied hair, visible face and light stubble; muted indigo split-hem tunic, charcoal light shoulder armor, worn steel forearm guard, brown waist wrap with small rust buckle, dark trousers and boots, compact sheathed one-handed sword. Preserve the reference's distinctive shapes and material colors. Quiet deliberate pixel clusters and broad shadow masses, restrained warm edge and cool shadow, no environmental glow; stylized game pixel art, not realistic, anime or chibi. Actual transparent alpha background; no floor, scenery, cast shadow, border, lettering or UI.

Self-review: Recognizable costume and complete figure; the torso is substantially frontal rather than a small chest reveal, and boot tops are visible. Pose and silhouette differ from side.png, reducing the fairness of a camera-only comparison. A visible semi-transparent warm halo remains; alpha extends to image edges. No clean cutout or gameplay validation is claimed. Figure sizing by alpha bounds is contaminated by the halo and is not an accurate body-size measurement.
