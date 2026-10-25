# Asset contract

Use this contract for production experiments. Adapt representation-specific fields after choosing the method; it does not assume pixel art.

## Source deliverables

Every approved test asset retains:
- Its approved appearance reference and style-guide version.
- A meaningful native master, with named layers/frames or parts/bones as appropriate.
- Construction scripts, editable pixel grids, or rig parameters when used.
- A record of tool versions and material generation/settings information that can be observed.
- A demonstrated localized revision with before/after evidence.

An imported flattened image alone does not demonstrate the structured construction requested by the user. A filename ending in .aseprite is not sufficient evidence. Aseprite-compatible JSON is atlas metadata unless a native source is also supplied.

For an Aseprite route, inspect actual layers, frames, cels, durations, palette, and tags. For a rig route, inspect parts, pivots/bones, key poses, and replacement drawings. Scripts need not recreate stochastic generations byte-for-byte; preserve accepted inputs and outputs and state the reproducible boundary.

## Runtime deliverables

Record canvas/frame dimensions, scale, transparency, facing, anchor/pivot, animation names, frame order/durations, and export settings appropriate for Godot.

Keep sources and runtime exports distinguishable. Once assets exist, use an explicit layout such as assets/source, assets/export, and assets/previews; avoid generating placeholder assets merely to fill folders.

## Verification

Use automated checks for declared dimensions, frame counts, palette constraints where relevant, transparency, and export metadata. Inspect visible images and actual playback for identity, anatomy, poses, and timing. Check a fresh export after reopening or reconstructing the master.

Preserve the approved result before revisions. Report unintended changes, cleanup performed by the agent, remaining manual work, and the effort of the revision. Do not infer style approval from passing structural checks.

## Provenance

Record source URLs or local reference paths and attribution/license notes for reused assets. Keep credentials and service keys outside the repository. Record actual generation/service usage when observable; do not invent usage or cost.
