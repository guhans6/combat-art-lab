# E0 — deterministic B00 replay

**Status:** technically passed; E1 is proposed only, not run.  
**Question:** can the existing 120×112 nine-part B00 seed be replayed without new visual inference?

## Frozen recipe

- Authority: `assets/references/approved-2026-10-26/character-closeup.png`.
- Crop: `[380,64,860,512)`, 480×448 source pixels.
- Conversion: BOX reduction to 120×112, no dithering, source-foreground 48-colour policy.
- Ownership: nine reviewed semantic masks, with nonzero BOX coverage used for ownership.
- Construction: the pinned headless Aseprite MCP (Aseprite 1.3.18.6-dev) opened each prepared part PNG and duplicated its sole layer into a fresh RGB sprite. No Lua, UI, Code-MCP, image-generation/model-tier trial, or historical B01/B02 correction was used.

The source hash, crop, palette, masks, role samples, and visible-part polygons are frozen in each run's `traces.json`; the complete immutable file digest inventory is [e0-manifest.json](e0-manifest.json), while [recipe.json](recipe.json) identifies the source, deterministic parameters, tool versions, and output roles. `run-a/replay-2` and `run-b/replay-2` are the manifests/outputs. The inherited crop and masks were earlier human/agent-reviewed choices. E0 added no image generation, model-tier trial, or new visual inference.

## Outputs and checks

`run-a/replay-2` and `run-b/replay-2` are independent fresh preparation/assembly runs. Their B00 exports, their fresh-reopen exports, and historical B00 are decoded-RGBA identical (PNG SHA-256 `0341156ff730ebc22514cb267d758bc81968596faff20b06fdd5264e0ae8b55d`). Both native sources have one 120×112 frame and the ordered layers `01-jacket` through `09-mouth`. All foreground pixels have exactly one declared owner; no overlap, unowned foreground, or part-outside-seed pixels were observed.

Prepared converted seeds retain RGB values beneath transparent pixels. Native export normalizes those values: alpha and visible RGBA match the preparation, while full decoded RGBA differs at 5,907 transparent pixels. This is recorded separately from the full-RGBA B00 export equality.

The first direct duplicate-only edit is retained as `b00-separated-seed-tie-edit.*`. It changed one allowed tie pixel and reopened with identical RGBA, but the unchanged strict checker rejected it: Aseprite serialization changed the header file-size bytes, palette count from 256 to 48, and old palette chunk `0x0004` to `0x2019`. The machine-readable rejection is [strict-raw-edit-check.json](strict-raw-edit-check.json).

The normalized technical baseline `b00-normalized.*` was then created by reopen/save/export and shown pixel-identical to B00. Editing only tie pixel `(26,38)` in `07-hair-tie` produced `b00-normalized-tie-edit.*`. The unchanged strict checker passes: one permitted pixel changed; all other layers, header, frame data, layer data, and cel geometry remain identical. The edited source was freshly reopened and exported again.

## Retained failures and reproduction

The empty initial output directories document an adapter path-depth error before inputs were read. An initial in-memory MCP assembly used the wrong imported PNG layer name (`Layer 1` rather than `Layer`), yielding only a placeholder target; it was discarded in memory and rebuilt before any file save. The ordinary sandboxed Aseprite CLI aborts during macOS application registration, while the dedicated headless MCP preflight was ready. The raw `b00-separated-seed-tie-edit.*` pair retains the first strict-metadata rejection; it was not relabelled as a passing proof.

With the workspace Python runtime, run `scripts/prepare.py --out <new-output>` from `scripts/`; it refuses an existing destination. Native assembly is the recorded dedicated-MCP sequence of opening each `prepared/01-jacket.png` through `09-mouth.png`, duplicating its `Layer` into a fresh 120×112 RGB target, naming/order-setting the nine semantic layers, saving, exporting, reopening, and exporting again. Freeze with one reopen/save/export before the strict local-edit comparison. Run `scripts/verify_e0.py` from this experiment root for the fail-closed, read-only final replay/reopen/strict-edit check; its persisted strict result is [strict-normalized-edit-check.json](strict-normalized-edit-check.json), and [checks.json](checks.json) is a concise summary rather than the sole proof.

No price, token/call total, active-work duration, or model cost was observed. The headless MCP operation count is also not captured as a complete benchmark metric.

## Evidence boundaries

This establishes deterministic preparation, native semantic-layer assembly, fresh reopen/export, and one protected local revision. It does not establish user approval, better visual quality, production resolution, motion, Godot playback, cost, or model-tier routing.

## E1 readiness

E1 is ready to propose, not execute: retain unchanged B00 as Control A; first run warnings-only lint against the frozen crop/grid/masks; then construct one separate role-palette/contour-cluster candidate B. Protect eyes, mouth, and identity-bearing hair, and compare exports at 1×/4× before user review. User visual review remains required before any artistic promotion.
