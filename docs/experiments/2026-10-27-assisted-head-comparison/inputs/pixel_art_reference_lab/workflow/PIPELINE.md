# Working pipeline

## A. Establish the style/identity contract
Open the authoritative references. Record character design, facial identity cues, material colors, outline/shading treatment, atmosphere and allowable simplifications. State which pose/expression is being drawn. Distinguish native resolution from display scale; neither is approved merely because it appeared in an earlier experiment.

**Ready:** a compact visible-feature contract, actual source paths/hashes and a bounded task are recorded.

## B. Decide whether another reference helps
Classify the gap: unclear expression, missing body/view, occluded detail, overly dense texture, insufficient pose information, or ambiguous action phases. First try existing approved assets/crops. When a new image would resolve the gap, use the appropriate prompt in `prompts/`.

If generation exists in the current authorized toolset, attach the actual images and run it. If unavailable, prepare a complete user request with exact attachments, desired result and return location. Neither invent image IDs nor assume that a filename is visible to another model. Preserve every generated source before processing.

**Ready:** the reference need is satisfied and reviewed, or a precise user request explains which later step remains pending.

## C. Review generated references
Check the original face, expression family, crown/fringe/tied-hair structure, proportions, clothing/accessory relationships and cluster/shading language. Allow intended view/pose changes. Reject unrequested redesigns. Register provenance: tool/model if observable, prompt, inputs/hashes, output/hash, changed intent and review status.

Use a generated image as a candidate pose/style aid, not an automatic replacement for original identity. Ask the user for consequential artistic tradeoffs or final selection, not repeated confirmation of routine processing.

**Ready:** each reference has a role and explicit use/reject decision.

## D. Fix one native mapping
Select a crop, aspect-preserving transform, anchor and proposed grid. Measure key landmarks only to guide alignment; do not enforce false precision on rescaled/generated input. Show source and blockout together. Register any intentionally simplified or adjusted shape.

**Ready:** geometry/framing is comparable before the detail pass. A square head crop has no inferred full-character dimensions without an explicit mapping.

## E. Construct through an appropriate route
1. Trace-guided: retain underlay, map meaningful boundaries/planes, draw clean clusters on separate native layers.
2. Converted seed: reduce with declared filter/palette/alpha policy, organize regions, correct important features.
3. Hybrid: retain successful seed regions and trace/redraw the deficient ones; use another accepted reference for genuinely missing information.

Keep masks and transformations reproducible. Reference guides and raw seeds are labeled and excluded from the final art export. A native file full of empty layers is not meaningful structure. Parts can be organized from imported pixels; provenance stays explicit.

**Ready:** an actual native candidate and export exist and have been visually inspected.

## F. Evaluate and correct
Show original, supplementary reference, seed and candidate. Inspect 1×, integer zoom and declared projected game size. Review identity, expression, shape, style and craftsmanship separately. Correct structural drift before eyelashes or seams. Preserve all variants and record why the next change should help.

**Ready:** each pass has evidence and a continue/correct/reject decision, not only successful tool calls.

## G. Prove editability, then motion
Make one localized native edit with meaningful control and verify protected regions. Reopen/export. Once the style is convincing, carry the same pipeline to needed pose references and keyframes using `ANIMATION.md`. Observe real playback before claiming animation or engine readiness.

**Ready:** source, exports, review, edit proof and remaining limits are delivered. The user selects the artistic result. A good still does not establish a complete production pipeline.
