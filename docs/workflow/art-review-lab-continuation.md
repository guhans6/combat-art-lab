# Art Review Lab: parallel UI continuation

Date: 2 November 2026. This is a product intake and preserved-fixture handoff, not an approved software architecture or a claim that the generic UI exists.

## User outcome

The human likes comparing character variants side by side and singly in the same game environment. Make that a reusable workflow/UI for different characters, backgrounds, display sizes and lighting, with authored animation review later. Preserve the existing study so character decisions can continue independently. The user explicitly chose a separate Git worktree from a committed checkpoint.

The [Art Review Lab skill](../../tools/art-review-lab/SKILL.md) captures the established review procedure. [Research](../research/art-review-lab-2026-11-02.md) explains look development and precedents. This project applies their comparison pattern to 2D Godot; no engine migration is selected.

## Runnable baseline and evidence

- Fixture: [playground r03](../../godot/stealth-fighter-playground-r03/project.godot), with [controls](../../godot/stealth-fighter-playground-r03/README.md). Retain it as a regression fixture; implement the generic tool in a separate directory.
- Five static looks: unchanged Current A REST and supplied images 01/03/04/05. Image 02 contains the exact 03 main-figure crop; it is context, not an extra unique sprite. Only 03/05 isolates the shoulder-cap change. Other candidates change several properties.
- Native/export provenance: [variant manifest](../../assets/export/stealth-fighter/user-variants-r01/variants.json). User source files, six meaningful visible-part native layers and reproducible inputs are preserved. The split is for revision; hidden surfaces or animation rigs are unproved.
- Common displayed body height 152 px, native 128×264 / 240 px visible body; root (64,253). World 1200×480 inside 1280×800 viewport. These are fixture settings, not universal defaults.
- Fixed Quiet Keep background, three equivalent bays, side-by-side/single mode, per-panel appearance selection, sets including shoulder pair, common height slider, guides/reset and three lighting diagnostics. Credits/license are in the project.
- [Experiment record](../experiments/2026-11-02-stealth-fighter-user-variants-r01/record.md) and its godot-evidence folder own the existing proof: Godot 4.7.2 local macOS/OpenGL, 14 focused UI/state cases, five source-color/height/ground checks and final launch with no errors. This handoff does not claim a fresh engine run.
- Accepted Current A idle stays in assets/source/stealth-fighter/idle-r02/idle.aseprite: 700/260/500/340 ms, 1800 ms loop. r03 holds REST for all candidates; it does not implement generic animation playback. Do not replace this idle or animate the new variants as part of UI development.

The current view reads variants.json but its panel count, presets and background remain specialized. The human likes the review process and approximately 152 px presentation; no final appearance among these five, production native grid, lighting design or new animation is selected.

## Next task route and bounded first result

Use ask-matt's multi-session route: grill-with-docs → to-spec → to-tickets → implement. Use the existing running fixture as prototype evidence. Inspect it and settle only consequential open product choices with the human, starting with where the tool should run (Godot-native versus another shell) and how sessions are supplied/saved. Recommend the smallest existing stack supported by that inspection. Create the spec and implementation slices after that agreement; retain the repo's tracker/publication rules.

Suggested first vertical slice, for agreement: load a session description containing candidate asset paths/provenance, anchors/body bounds, environments and lighting profiles; display an arbitrary candidate list in a bounded number of comparison panels or singly; persist enough setup to reopen the same comparison. Demonstrate a second session or additional candidate through data changes without editing rendering code. Reproduce r03's five looks in the first fixture. Give clear validation errors for missing assets/invalid metadata. Keep source-color inspection and credits accessible.

Subsequent slice: authored static/animation assets with exact duration/anchor metadata, play/pause/frame-step and declared clock modes, using the same environment and light setup. Animation construction and visual selection remain separate art work. Keep extensibility grounded in these real use cases rather than a plugin framework.

Completion evidence for software slices should exercise the real renderer, saved-session round trip, single/side-by-side consistency, scale/ground/lighting controls and unchanged fixture assets. Record what was inspected visually versus automated. Use fresh Terra 6.1 Max for critical design/review and Sol 6.1 for normal tasks, per user preference; no silent model substitution.

## Coordination

This character chat owns art feedback and future selected-character animation. The parallel worktree owns the reusable UI, its session contract and tests. Preserve others' changes; avoid editing shared art/history. Work from the checkpoint named by the creating chat, verify HEAD and fixture hashes before depending on it, and report missing dependencies before proceeding. Verify the copied fixture in the destination before claiming runtime continuity. No PR, merge, new purchases, global tool installation or public release is requested.
