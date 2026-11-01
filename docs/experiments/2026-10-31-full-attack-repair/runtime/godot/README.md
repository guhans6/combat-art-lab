# Isolated tote-attack repair preview

Source: `../../source/attack-repaired.aseprite`, SHA256
`5fb9a4f776ea46df1ee86c3eb5e10c8be32b094aa265004e908e832b7f4518ea`.
This is a copied experiment fixture, not a production game replacement.

Use the dedicated Godot MCP `run_project` with this directory's absolute path.
It runs three synthetic Space-triggered attacks, registers one bounds-based F6
contact per attack, captures all13frames, and returns to exact neutral. Inspect
`get_debug_output` and `evidence/attack-observation.json`, run the experiment's
`verify_runtime.py`, then call `stop_project`.

Observed final run: Godot4.7.2, macOS/OpenGL Compatibility, viewport362x304,
nearest filtering,2xwindow.13/13live captures match the source opaque pixels;
three contacts/returns; elapsed1666/1681/1661ms versus1680ms authored.
No physical-keyboard test or continuous agent perception is claimed.

Space/Esc are the fixture's controls. Runtime event/capture checks establish scoped
playback, not accepted animation quality, combat range, collision tuning or release.
