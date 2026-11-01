# Sol mouth-only repair

30 October 2026. User-requested diagnosis and native correction, not a model benchmark. Exact baseline is the Luna6 full-body cleanup before mouth edits. User-approved original scene/close-up remain authoritative. Original native, PNG and references were frozen/copied and hashes verified unchanged. Existing dirty work was preserved. All work is in this new experiment directory.

## Result

Retain **pass02** as the quieter review candidate; no user artistic approval inferred. [Native](passes/pass-02.aseprite), [transparent fresh export](passes/pass-02-reopen.png), [head 1x](reviews/final-head-1x.png), [head 8x](reviews/final-head-8x.png), [fullbody 1x](reviews/pass-02-fullbody-1x.png), [fullbody 4x](reviews/pass-02-fullbody-4x.png). Pass01's stronger symmetric raised corners were rejected in parent defect review; both attempts are preserved. Two passes used, no third pass spent.

Actual export shows one warm closed curve instead of competing facial marks. Pass02 lowers the corner weight and unevenly softens the far transition. At 1x the expression is very subtle; at 8x it is less squared than pass01. Parent independently inspected both exports, direct reference mouth, head and fullbody and retained pass02 for user review. This is not exact reference matching: native staircase remains and inherited face geometry still differs from source. No universally better model, proven grid limit, or guaranteed user preference follows.

## Diagnosis and evidence boundaries

- **Observed:** the baseline contains two warm lower-face pixels at (68,27)/(69,27); earlier edits added another dark mark below/left or against the face edge. The field was not blank. **Inference:** the inherited pair is a simplified ambiguous mouth, supported by eye/nose/chin registration; generator intent cannot be recovered. Calling it a nose or asserting a blank mouth without registration was unsupported.
- **Observed:** approved mouth is a fine shallow closed curve with slightly unequal corners, approximately x675–707, y336–343 in the close-up. The faint nose cue is higher, around (719,309). Approximate normalized eye-to-chin mapping places mouth around x67–68/y27–28, within the cheek. Exact landmark centers have uncertainty; direct rulers and coordinates are retained in observations.md and reviews.
- **Observed:** old right-edge patch looked pout-like; moved three-pixel patch looked like a floating diagonal under the inherited pair. A uniform #744c40 stroke omitted the source's lighter center/corner weighting. Pixel count minimization did not preserve the expression's cluster grammar.
- **Observed:** earlier reference comparison crops matched panel dimensions without matching eye-to-chin span. The first sheet in this run had that defect too. It was corrected in the final reviews using an aspect-preserved wider source crop (520,170)-(820,470); native sprite pixels never rescaled fractionally. Original ruler crops remain available to avoid judging only a reduced preview.
- **Observed:** parent positive reviews were later contradicted by user rejection; parent withdrew them. **Inference:** expectation/confirmation bias contributed to accepting intended smiles instead of judging the marks actually visible. Technical protection/reopen passes were valid but did not support expression success.
- **Observed:** the face pixels are owned by the inherited hair layer, while the nominal face layer is transparent in this patch. This explains why earlier nominal face-layer changes could be hidden. Repair edits the actual owner without transferring unrelated pixels or changing native structure. That ownership remains an inherited limitation.

The diagnosis is local and evidence-based. The current references suffice; no generation was needed. Repeated failure does not establish that the small grid cannot carry a smile.

## Construction and protection

Registration preceded frozen mask `[66,27,71,29)` in zero-based half-open coordinates. Native owner: `08-hair-tie-and-hair`, frame1. Pass01 restored the inherited two-pixel mark to surrounding skin and authored five curve pixels. Pass02 changed four of those lip shades only. All native drawing used dedicated headless Aseprite MCP; JSON batches in operations retain exact reproducible edits. Python only prepared evidence and independently read/checked native pixels.

Aseprite 1.3.18.6-dev; Aseprite AI Artist MCP 0.8.2; headless. Save-as to a new path followed every mutation. Actual final native was freshly reopened as a separate document and exported again. Current MCP inventory does not expose validate, so no backend validate result is claimed. The preflight advertises that feature, which is not the same as an available tool. No fresh standalone scratch smoke was performed in this run; the same backend had existing saved scratch proof, and this actual local edit/reopen was independently verified.

[Independent checks](proof/pass-02-checks.json) pass:

- Exactly seven composite/native pixel changes, all within the ten-cell mask; zero protected changes.
- All other eleven native layers, including hidden guide, and every owner-layer pixel outside the mask are unchanged.
- Canvas 128x192, one 100ms frame, 12 layers, 255-entry palette; header, all non-cel chunks, layer metadata and cel geometry/opacity/z unchanged.
- Every alpha unchanged; 7,844 opaque pixels; binary alpha retained. Thus silhouette, eyes/brows, nose cue, cheek/jaw contour, body and prior body cleanup are unchanged.
- Independent native composite equals fresh reopened PNG; first/fresh reopened PNG files byte-identical.
- Input originals' SHA-256 values unchanged. Negative scope test correctly rejects this patch when the entire native canvas is protected.

Final native SHA-256: `34bce2011f0c0ab1434d5c7eb624c3379459e2ef37ae9dcfe3ad96cf524b824f`. Final PNG SHA-256: `39e55fc167ea1aa3e90090dfdab6fca447e7417d53169b62eb550d80602a84e0`. The verification script reruns the complete native/PNG/input comparison; review scripts rebuild diagnostic sheets. Native art can be replayed by opening inputs/baseline.aseprite with MCP, reading sprite_info, applying operations/pass-01.json then operations/pass-02.json to the named layer/frame, saving to a new path and freshly reopening/exporting.

## Remaining boundary

Local construction/export and scope protection are proven. User visual selection is pending; parent owns handoff/result selection. No animation, Godot/gameplay validation, new generation, install, paid service, commit, push, publication or asset promotion performed. No broader pipeline/skill changes made.
