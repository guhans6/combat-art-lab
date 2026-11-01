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

## Assisted-input provenance

For each reference record path/hash, role, origin and review status. Keep user-approved
anchors separate from generated candidates accepted only for agent use. Preserve
prompts and exact canonical attachments for generation; original, intermediate, raw
converted seed and actual candidate export must be available in comparisons where used.

Record crop, source/native/display dimensions, transforms, masks, palette extraction,
traced/source-derived shapes and pixels, and authored cleanup separately. Finished
sources must have parts that support useful revisions; visible-part masks do not prove
hidden-surface reconstruction or a ready rig. Verify a duplicate-only local edit with
protected-native checks and fresh reopen/export. Pixel equality protects originals and
locked content; it is not an artistic similarity target for a fresh reconstruction.

## Runtime deliverables

Record canvas/frame dimensions, scale, transparency, facing, anchor/pivot, animation names, frame order/durations, and export settings appropriate for Godot.

For pixel studies, distinguish native canvas, visible character bounds/height, cropped-study dimensions and equivalent full-character scale. Record projected gameplay height, viewport/camera/filter and integer-scaling assumptions where known; label unknowns and comparison-only resizing. A static matched-size preview does not establish runtime behavior.

Attach a concise visual brief: essential identity/silhouette/expression cues, secondary details that may simplify, palette/edge rules, lighting/effect separation, and protected regions or layers. A new reconstruction may test a separate grid; a local correction preserves its declared locks. Proposed grids and feature budgets remain provisional until supported by actual art and approval.

Keep sources and runtime exports distinguishable. Once assets exist, use an explicit layout such as assets/source, assets/export, and assets/previews; avoid generating placeholder assets merely to fill folders.

## Verification

Use automated checks for declared dimensions, frame counts, palette constraints where relevant, transparency, and export metadata. Inspect visible images and actual playback for identity, anatomy, poses, and timing. Check a fresh export after reopening or reconstructing the master.

Preserve the approved result before revisions. Report unintended changes, cleanup performed by the agent, remaining manual work, and the effort of the revision. Do not infer style approval from passing structural checks.

Use the [workflow review rubric](../workflow/art-production.md#visual-review-rubric) to record technical checks, agent visual observations, subjective artistic assessment and user acceptance independently, naming the exact artifact and review size. Leave animation feasibility and gameplay readability untested until their actual proofs run. Preserve unsuccessful comparison passes as evidence; no aggregate automated quality score establishes acceptance.

## Provenance

Record source URLs or local reference paths and attribution/license notes for reused assets. Keep credentials and service keys outside the repository. Record actual generation/service usage when observable; do not invent usage or cost.

## Reusable environment modules

Retain separate native parts, transparent runtime exports, local anchors and placement offsets. Prove useful removal/movement without obvious leftover fragments and test independent scene instances in Godot. Mark camera-specific crops, unreconstructed occluded surfaces and grouped decoration. Painted illumination, separate emissive pixels and engine lights are distinct deliverables; packaged export needs its own verification. The [first shop experiment](../experiments/2026-10-27-shop-modular-refinement/record.md) demonstrates the current boundary.
