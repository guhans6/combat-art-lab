# Main character scale playground — r01

Date:2November2026. Status: implemented and locally validated; final live launch recorded separately. User says the main idle looks good and asks for an actual themed playground with different sizes, side-by-side or single views. This accepts main idle-r02 as the motion baseline for this placement study; production grid, final display size and world art remain open.

## Scope and baseline

Approved main native assets/source/stealth-fighter/idle-r02/idle.aseprite, SHA256 f4cb8fff0a460cde6845fb15bc0c5e3271259d9d38d5f3efa051e4970b2e6127. Exact4PNG exports,128×264canvas/240pxrestbody, [700,260,500,340]ms timeline, shared1800ms phase. No character edit, new pose, recolor, generation or native-source mutation. Existing studies, main sources and prior environments preserved.

New project godot/stealth-fighter-playground-r01/project.godot. Temporary theme: The Quiet Keep, a ruined stone cloister using Luis Zuno's public-domain GothicVania Church artwork. Verified artist's primary OpenGameArt listing and archive public-license.txt; original license, download URL/hash and exact used texture hashes retained. Only unchanged background/tileset textures used; runtime crops repeat the same stone window bay and floor blocks at integer2×. No audio, enemy/player sprites or pack game code. Primary URLs in CREDITS.md; retrieval2026-11-02. Existing modern street assets were available but did not fit the current character setting. Cold Corridors investigated but not used. No new purchases or services.

## Playground behavior

One1200×480world inside1280×800viewport. Three actors default96/128/160scene pixels tall, synchronized on one clock, identical repeated architecture and ground. Side-by-side displays all three; Single hides other actors and centers the selected one without changing the world, camera or character scale. A/B/C selection and a64–240height slider allow changing one candidate while retaining the others. Pause/play, frame step,0.5×/1×/2×speed, measurement guides and reset. Mouse controls plus M/1/2/3/Space/comma/period/R/G/F11 shortcuts. Resizing/fullscreen uniformly changes display magnification, not the in-world ratios. No walking/combat/playable-game claim.

## Focused proof

Current Godot4.7 documentation checked through Context7: draw_texture_rect_region, SubViewport sizing (considered, not used), input event injection and RenderingServer.frame_post_draw screenshot capture. Primary documentation sources: github.com/godotengine/godot-docs/blob/4.7/classes/class_canvasitem.rst ; tutorials/inputs/inputevent.rst ; classes/class_viewport.rst. Actual runtime through dedicated GodotMCP only, Godot4.7.2.stable.official.ed1daf0bf, localmacOS/OpenGLCompatibility/AppleM3Pro. No direct editor CLI or computer use.

Separate test project ran15 focused checks through actual injected mouse/keyboard events and state observations: >=3authored loops, Single button, A selection, slider change, keyboard B, pause hold, next/previous frame, resume and time advance,2×speed, guides, keyboard comparison and both reset paths. All pass. Initial run had two local parameter-shadowing warnings; renamed those parameters and reran the same focused suite, final errors/warnings[]. Test instance stopped. Main project has no RUN_CHECKS marker, so no automatic test manipulations occur for the user.

Independent pixel audit of actual Godot captures: all4native-scale source poses have0opaqueRGB mismatches. At all3default scales, independently calculated nearest samples match exact source colors (1584/2825/4419opaque pixels tested), drawn heights exactly96/128/160, common bottom opaque row557/groundline558. No camera change between modes. Original artwork has no tint/filter blur. Source PNGs equal approved exports. Compare and Single screenshots visually inspected: joint/feet registration retained, labels/controls clear and no clipping; this is still pose/UI evidence, not continuous model temporal perception or user approval of background/scale.

## Completion and handoff

Implementation and focused local input/render checks pass. Native source unchanged; public release, export to a packaged executable, combat integration and final art/size selection are not performed. The agent launches the saved Godot project for direct user interaction and leaves that final instance running. Next owner: user compares sizes and gives a preference; agent owns any preview corrections. The128px middle option is a comparison baseline, not a chosen production size. Existing source/PNG protection hashes and delivered file manifest accompany this record.

Final saved project launched through dedicated GodotMCP from godot/stealth-fighter-playground-r01. PLAYGROUND_READY observed, errors[]. Same script/config bytes as tested copy, RUN_CHECKS absent. Final instance left running for the user, unlike the stopped test instance. See evidence/live-launch.json and live-project-debug.json.
