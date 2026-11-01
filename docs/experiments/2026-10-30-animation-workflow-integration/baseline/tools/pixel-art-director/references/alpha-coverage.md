# Alpha coverage after cleanup or part motion

Color is evidence for a cleanup candidate, not proof that a pixel is background.
Use a reviewed spatial removal mask. Preserve warm/neutral material highlights and
inspect the changed alpha against the original source. Color-key deletion across
an entire garment can silently perforate fabric.

After cleanup and after relative part movement, run the existing checker on every
actual exported frame, not only the first pose:

python scripts/pixel_checks.py alpha --images FRAME_FILES --region X0 Y0 X1 Y1 --out NEW_REPORT.json

Coordinates are half-open in the native canvas. Connectivity is measured over the
whole canvas; the region filters review findings. A transparent gap to the canvas
edge is not an enclosed hole. For known solid coverage including silhouette edges,
provide a same-size binary --solid-mask. Review intentional enclosed cutouts with
an explicit --allow-holes JSON list of XY coordinates. Avoid blanket filling or
blanket ignoring small components; hair openings and leg gaps can be intentional.

Inspect the export on contrasting light/dark or saturated backgrounds and in the
actual scene. Read the native target layer to distinguish absent alpha from a
painted highlight. For moving disjoint parts, provide occlusion backing/overlap at
joints so movement does not expose unpainted pixels. Preserve intentional root travel.

Complete when all affected frames pass the declared coverage checks, save/reopen
matches, protected native layers/palette/timing are verified, and actual engine
output has been inspected. Pixel equality and successful playback alone can preserve
the same defective holes. Generic automatic flags support visual judgment.

combat-art-lab's Godot preview also checks body coverage before playing its frames.
Its full-character policy has explicit reviewed hair cutouts; revise the policy when
poses or costume change. Dedicated MCP remains the required execution path when the user
has selected it.

For combat-art-lab, run the consolidated project check through the authorized MCP execution tool:

python tools/check_art_assets.py --out NEW_REPORT.json

It checks all eight character frames, declared hair openings, sixteen shop parts, solid pot
regions, atlas dimensions/offsets and exact part assembly using tools/art-quality-profile.json.
Foliage holes and disconnected leaf clusters require visual review; solid wall/glass/light
housings should retain backing when props or emitters are hidden. Inspect isolated parts
and their hidden/moved states. Relative part motion also needs correct ownership: a head
pixel left in a stationary clothing layer can open a gap even when every frame exports
correctly. Compare JSON coordinates numerically in Godot; parsed coordinates may be floats.
