# Rebuild this candidate in the existing repository

Use the existing dedicated Aseprite MCP; all native/source writes stay in Aseprite.
`prepare.py` reads `../baseline/sol-original.aseprite` and the repository's existing
read-only native decoder. It only generates literal draw payloads, not sprite files.
The bundle Python used here is
`/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
(Pillow12.3.0). No new dependency was installed.

1. Run `prepare.py` to regenerate `operations.json`.
2. MCP preflight(headless); open the preserved Sol native, call sprite_info; save_as
   a fresh output. Do not overwrite the baseline or a document open elsewhere.
3. For each `calls` entry, call dedicated Aseprite `draw` with the fresh sprite ID,
   explicit layer/frame and the payload's palette-locked grid. Apply in array order.
4. Create forward tag `idle-coherent` from1 through8, repeats0. Durations already
   match the original plan. Save. Export an untrimmed horizontal spritesheet with
   zero padding and JSON; close/reopen and export again to a fresh path.
5. For a reproduction in a new folder, compare decoded frame/layer pixels with
   `states()` from prepare.py and fresh exports. File byte hashes may differ due
   to Aseprite serialization; compare native structure/pixels/timing too.

The delivered v02 is an actual native MCP construction, not merely prepared input.
Its all-layer/all-frame equality to the final recipe and fresh reopened exports is
recorded in `../verification.json`. The initial v01 native/operations/calls are
retained separately. v01's disconnected crease tip was repaired on F3–5 by restoring
`#d6b7bb` at `(60,55),(61,55)` through MCP; v02's recipe includes that repair directly.

Packaging/checks from the repo root, using that existing bundled Python:

- `docs/experiments/2026-10-30-coherent-idle/build_delivery.py`
- `docs/experiments/2026-10-30-coherent-idle/verify_contract.py --sheet docs/experiments/2026-10-30-coherent-idle/reopen/sheet.png --gif docs/experiments/2026-10-30-coherent-idle/exports/idle-1x.gif`
- `-m unittest discover -s docs/experiments/2026-10-30-coherent-idle/tests -v`
- `docs/experiments/2026-10-30-coherent-idle/audit_delivery.py`

`build_delivery.py` crops actual MCP sheets and encodes faithful GIFs; it does not
redraw native art. `verify_contract.py` is scoped to this character and these two
reviewed primary keys; it is not a universal anatomy or naturalness detector.
`prepare_godot.py` creates a fresh isolated copy of the existing preview and refuses
to overwrite an existing directory. Dedicated Godot run/debug/stop produced the
runtime evidence. The project already exists in this delivery, so rerunning its
preparation is unnecessary unless a separate new output is chosen.
