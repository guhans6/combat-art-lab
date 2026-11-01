# Denim alpha repair — 27 October 2026

## Request and red loop
User reported missing leg pixels in a Godot screenshot and requested diagnosis, repair and skill/tool prevention. Dedicated MCP only; no Code-MCP/computer use. Screenshot retained as user-report.png.
repro.py checks transparent connected components in the actual PNG. Two original runtime-frame probes failed consistently: twelve interior leg pixels. Minimal real 3x3 cuff crop fails at (1,1); fixture retained in the existing director test suite.
One reproducible invocation, run through Node MCP: bundled Python + repro.py + before-frame-00.png + 100 + 205. Red output is in red-reproduction.json. The same invocation on repaired frame-00 returns zero missing pixels (original-repro-green.json).

## Ranked predictions and observed cause
1. Cleanup deletes source material: confirmed.
2. Disjoint moving parts expose seams: separately confirmed at waist/hands/tote in inhale poses.
3. Export/Godot alpha changes: ruled out for these pixels; native and export share the damage.
4. Intentional holes in reference: ruled out for reported fabric gaps; source samples are opaque.

clean-static.lua's old predicate used b <= r+4 OR g <= r+1 over every denim sample in rows 114..191. The gray-blue (90,90,108) fabric satisfies the second clause. All twelve reported interior pixels were opaque in seed and absent after cleanup. stage-probe.json retains RGBA values. An exterior-connectivity-only proposal would preserve just eight of these twelve, so it was insufficient. It was not used as the repair.

## Native repair and construction
Current master: assets/source/standing-alpha-v02/standing-idle.aseprite, 96x216, eight frames, unchanged 65-entry palette/timing/tag.
Restore twelve original seed-color samples on 01-denim in all eight frames. Add one bottom 00-joint-underpaint layer with forty-seven reviewed rest-pose color pixels on inhale frames 2..6. These close gaps exposed by disjoint part motion; other layers retain exact original pixels. A first backing pass left one newly enclosed pixel at (59,115), caught by the same loop; the final patch closes it.
Original native and PNG attempts remain preserved. New exports and GIF are under assets/export/standing-alpha-v02 and assets/previews/standing-alpha-v02. Native drawing, save/reopen and export used Aseprite MCP 1.3.18.6-dev/Pebbly 0.8.2.
denim-repair-pixels.json and motion-repair-pixels.json are complete final patch inputs. The original constructor now uses 479 explicit edge removals, preserving the twelve fabric samples. animate.lua receives the same explicit joint backing and refreshes exports after applying it. Lua edits were not executed through the current MCP catalog (no general Lua execution tool exposed); data-level patch replay equals all eight native PNG exports. Actual final native operations were independently executed and validated through MCP.

## Prevention
Existing pixel_checks.py now has alpha coverage checks, native-canvas connectivity before ROI filtering, exact intentional-hole exceptions and reviewed solid-mask coverage for edge-connected loss. It flags rather than fills. Eight new tests include the actual cuff fixture, intentional leg gap, ROI connectivity and solid-mask edge loss. All 32 director tests pass.
Canonical tools/pixel-art-director skill and assisted reconstruction reference point to references/alpha-coverage.md. Color alone is insufficient evidence for deletion; inspect every actual exported frame and use backing at moving joints.
The Godot preview now checks body coverage [0,55,96,205] before playback, loading actual PNG bytes. Real MCP run with old exports failed at frame 0 with ART_LAB_ALPHA_FAIL. With repaired exports it reports ART_LAB_ALPHA_OK frames=8, plays and captures all eight frames, repeats loops and has empty final runtime errors. Head/hair openings lie outside this body gate and are unchanged. A different costume/pose needs a reviewed ROI/cutout policy; this is not a universal zero-transparency rule.
PNG buffer loading uses Godot 4.7 Image.load_png_from_buffer and FileAccess.get_file_as_bytes; official documentation checked through Context7: https://github.com/godotengine/godot-docs/blob/4.7/classes/class_image.rst. This also avoids stale imported texture contents. Packaging still needs raw PNG inclusion or normal Texture2D imports.

## Evidence and limits
alpha-before.json fails all eight old leg frames; full-body probe also exposes inhale seams. final-delivery-alpha.json passes all eight corrected body frames with zero enclosed gaps. Native save/reopen exports match all eight outputs. Thirteen protected original layers are pixel-identical on every frame; dimensions, palette, timing and tags unchanged. Native denim has exactly twelve changes per frame; only the declared new backing layer is added.
Engine-pixel-checks.json compares 331 repaired-point samples from actual engine captures against the corrected source, with zero RGB differences. Engine 4.7.2, OpenGL/Metal Apple M3 Pro, viewport362x304, root108,48, nearest rendering. godot-red.json and godot-green.json preserve runtime rejection/pass. No OS input interaction was performed.
Old character/static native and shop master hashes unchanged. Runtime loader/layout, project part PNG loader, helper, skill references and constructor inputs are intentionally updated. Strict native binary/header and full-tree hash audits were not run. Dedicated Aseprite validate tool remains unavailable.
Bundled Python skill validator cannot import PyYAML; no dependency installed. Existing frontmatter parses with bundled Node YAML, unchanged name/description preserved, new reference links checked. Runtime and pixel tests passed; no automatic artistic approval claimed.
The original/before/after and magenta-background leg comparisons are under assets/previews/standing-alpha-v02; magenta is diagnostic display only. Actual Godot feet capture is godot-feet.png.
No [DEBUG-] instrumentation added. Reproduction/failed attempts are retained as clearly scoped evidence. Permanent ART_LAB_ALPHA startup guard remains deliberately enabled.

## Next action
User reruns the existing Godot project using Run Project to load corrected frames; preview is also running through MCP. Agent next handles a selected visual correction. No new service, installation, generation, commit or publication.
