# Standing idle art lab

Open project.godot in the installed Godot 4.7.2 and run the main scene.
This is an isolated art preview, not a full game.

The full character has eight idle frames: quiet one-pixel breathing and a blink.
The character and scene use exported pixel assets; original concept images are not loaded.
Scene art: 362x272. Viewport including controls: 362x304. Default window: 2x, nearest filtering.

Implemented controls (real keyboard input not yet tested): Space pause/resume, F next frame,
B isolated storefront, 1/2/3 integer window size, Escape quit.

Native sources and source provenance:
docs/experiments/2026-10-27-standing-idle-godot/record.md

Before the user imposed MCP-only operation, the engine observation mode played two cycles,
captured every frame, inspected closed eyes and isolated the first building. Evidence is in
evidence/observation.json, frame-events.json and runtime-*.png. These are actual engine output.

Current agent constraint: dedicated MCP tools only, no computer use, no Code-MCP.
The user authorized workspace-local installation. `godot-art-lab` is configured and
protocol-tested: eight frames, two loops, no errors, run/debug/stop all pass. Direct tools
may require a workspace/chat reload. See tools/godot-mcp/README.md for exact setup identity.
Do not substitute raw Godot CLI/UI operations; the MCP server owns engine invocation.
