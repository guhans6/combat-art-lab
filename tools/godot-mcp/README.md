# Workspace Godot MCP

The user authorized workspace-only MCP installation on 27 October 2026 and explicitly
prohibited Code-MCP. Do not use Code-MCP or computer use for this art workspace.
Use dedicated Aseprite/Godot MCP tools. Setup commands are only for installing/configuring
those tools; engine/art operations must pass through their MCP interfaces.

## Installed identity

- Package: `@coding-solo/godot-mcp@0.1.1` under `.art-tools/godot-mcp`.
- Upstream: https://github.com/Coding-Solo/godot-mcp (MIT).
- Server reports protocol serverInfo version 0.1.0; the package identity is 0.1.1.
- Existing Godot: `/Applications/Godot.app/Contents/MacOS/Godot`, 4.7.2.
- Existing Node: `/Users/guhan/.local/bin/node`.
- Configuration: `.codex/config.toml`, server `godot-art-lab`, project-local only.
- Enabled tools: get_godot_version, list_projects, get_project_info, run_project,
  get_debug_output, stop_project. Scene-editing/editor tools are not enabled yet.
- Existing Aseprite configuration is preserved. No global config or client modified.

This is project-scoped configuration and usage, not an upstream filesystem sandbox.
Use project paths only within combat-art-lab. No network service, credentials, purchase
or new editor plugin is required. Lifecycle scripts were disabled on npm install.
Dependencies and exact registry integrity are recorded in the install experiment.

## Observed boundary

Actual stdio MCP initialization, tool discovery, version/project inspection, run/debug/stop
passed. The standing scene produced all eight rendered frame captures, two loops and no
runtime errors. This used MCP requests through the reviewed server; the test client did
not call Godot directly. The current chat's native MCP catalog has not refreshed, so a
workspace/chat reload may be needed before `godot-art-lab` appears as direct tools.
Do not claim the native catalog was observed merely because the protocol test passed.

Evidence: `docs/experiments/2026-10-27-standing-idle-godot/godot-mcp-install/`.
The first smoke attempt sampled before loop two and is retained; the corrected test
waits for the actual loop marker with a 15-second bound.

## Reproduce installation / test

The package manifest/lock are retained in the experiment. Restore them to
`.art-tools/godot-mcp`, then install with the existing npm, a workspace-local cache,
`--ignore-scripts --no-audit --no-fund`. Do not resolve an unpinned latest release.

`node tools/godot-mcp/test-client.mjs` runs the real stdio MCP smoke test against only
`godot/standing-idle-lab` and stops the process it launched. It needs the normal Godot
runtime's cache access. This is a setup verification client, not a replacement tool
framework or permission to fall back to raw CLI Godot operations.

Project MCP settings were checked against official documentation on 27 October 2026:
https://developers.openai.com/codex/mcp
