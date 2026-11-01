# Reproduce the retained candidate

The canonical rebuild inputs are the literal MCP drawing batches in
[operations/replay-plan.json](operations/replay-plan.json), not a re-run of the
historical preparation heuristics. The preparation scripts are frozen to prevent
accidental regeneration over these exact inputs. Their formulas/masks remain
readable construction history. A new recipe experiment requires a separate copy.

A fresh dedicated-MCP replay was executed on31October2026:110draw calls, one layer
reorder and one animation tag. It produced a byte-identical native file, SHA256
`5fb9a4f776ea46df1ee86c3eb5e10c8be32b094aa265004e908e832b7f4518ea`.
See [actual invocation results](review/mcp-replay-log.json) and
[replay equality](review/replay-verification.json).

1. Resolve `path_base` relative to the replay-plan.json directory (`..` means this
   experiment root). Resolve `base` and every batch `path` from that root. Verify
   the base native SHA and every operation-file SHA against replay-plan.json.
   Never apply an individual batch to an unrelated or newer asset.
2. Use Aseprite AI Artist `preflight(mode="headless")`; the tested backend is
   Pebbly0.8.2 / Aseprite1.3.18.6-dev. Stop if not ready.
3. `sprite_manage(open)` the base path in the plan; `sprite_info` it. Immediately
   `save_as` to a NEW derived native path before any mutation.
4. Apply each listed JSON file in order. Each array entry is one `draw` call with
   explicit frame/layer/operations, plus the new document ID. Palette lock stays on.
   After `finish-f12.json`, execute the exact `layer` reorder in the plan. After
   all batches execute its exact `tag` creation. Check each tool response.
5. `look` at the filmstrip and key crops; `save`. Close only this saved document,
   freshly reopen it, then export transparent frames, horizontal sheet,1x/3xGIFs.
6. Compare native bytes, cels, palette, durations and exports to the retained result.
   The delivered fresh replay matches all of them, including the complete file SHA.

Native mutations must use the dedicated MCP. No editor CLI, raw Lua, generic
computer use or Python native-file writer is part of this recipe. Python packages
editor-produced exports and reads native structures; it does not write native art.

The whole actor in F2–F12 is authorized for correction; F1/F13 remain exact neutral.
The broad comparison mask reflects that scope. Per-frame color additions in the
comparison helper are allowed because neutral colors are reused in action frames;
package_review.py independently rejects any opaque pixel outside the unchanged
native255-entry palette. This does not authorize a new palette or new art scope.

For validation use the existing Python/Pillow runtime named in record.md:
`package_review.py`, then comparison_review.py build/verify in a NEW packet folder.
The package script is preparation plus focused checks; it does not itself invoke
comparison build/verify or claim visual approval. Hole counts are diagnostic only.

For scoped runtime reproduction use the dedicated Godot MCP `run_project` on
`runtime/godot`, then `get_debug_output`, `verify_runtime.py`, and `stop_project`.
The copied scene injects three synthetic Space events, captures all13frames and
returns, and writes evidence. Use a fresh copy/evidence folder to retain prior runs.
Physical keyboard behavior, game-feel approval and production integration are separate.
