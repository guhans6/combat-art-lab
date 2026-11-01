# First experiment: does assisted construction reduce appearance drift?

**Status:** planned, not executed by this kit. Suggested defaults below are proposals, not new user-approved production constraints.

## Question
Can reference tracing or conversion-plus-cleanup yield a closer-feeling face/style than the current independent reconstruction, while remaining practically editable?

## Scope and inputs
Use one head/shoulder study with the approved scene/close-up and the newest relevant native candidate. Preserve all originals and older experiments. Recheck the current workspace before choosing a baseline; do not silently use a v03 benchmark mask for a new study.

First inspect whether the references are sufficient. One new same-angle simplification/close-up may be useful. A different pose is not needed merely to fill a checklist. When obtaining a new image, preserve the original as identity/style authority and record its actual changes.

## Controlled comparison
- **A: trace-guided.** Map the same crop/landmarks and major planes; construct meaningful native layers.
- **B: conversion + cleanup.** Use the same source/crop/grid/palette policy, then organize and correct its pixels.
- **C: hybrid, optional follow-up.** Combine the better regions only after a specific limitation of A/B is visible.

Use the same proposed grid, facing, framing, light direction and bounded effort for A/B. Existing redraws are context, not a fair new arm unless conditions match. Do not change both source and grid and attribute the result to tracing alone. Extra-reference tests are a separate documented branch: original-source baseline versus approved simplified source, holding the conversion/native finishing approach fixed where possible.

A suggested initial limit is two meaningful refinement checkpoints per candidate, then a decision. Generation requests should likewise be bounded. Adjust the budget before a run rather than silently extending only one failing candidate. Record real activity when measurable; leave unobserved cost/time unknown.

## Review questions
Does this look like the same person and art style? Is the intended expression preserved? Do hair masses, face orientation and clothing remain coherent? Are details simplified rather than redesigned? Does it read at the stated size? Is the pixel treatment deliberate? Can one useful revision be made without damaging unrelated work?

Use side-by-side images and a registered overlay to diagnose geometry, not to demand pixel equality. Review at 1× and equal display framing with any resampling labeled. Record technical checks separately from user selection.

## Required deliverables
Native source, transparent export where appropriate, actual reference/seed/candidate sheet, image/provenance manifest, masks/transforms, useful layer organization, localized edit proof, fresh reopen/export check, retained rejected attempts and a concrete recommendation with limits.

## Failure diagnosis
| Failure | Next targeted action |
|---|---|
| Geometry wrong before details | Fix mapping/trace; do not merely increase resolution |
| Source too dense for target style | Request a same-character simplified production reference; preserve identity/style anchors |
| Required feature cannot read on grid | Test a larger grid or a deliberate feature redesign in a separate variant |
| Converted edges/eyes are noisy | Redraw those clusters; optionally compare a feature-preserving algorithm |
| Generated reference changes identity | Regenerate/edit with canonical attachments and a precise correction |
| Layers do not support meaningful edits | Separate the relevant parts and verify an actual edit |
| Tool cannot deliver images to the drawing agent | Fix image inspection before continuing art construction |

## Next boundary
Select a convincing static treatment, then one limited action with supplementary references. Do not build a full pose library before a method has worked on this asset. If neither arm is convincing, retain evidence and request the smallest source/tool/method change that addresses the observed failure.
