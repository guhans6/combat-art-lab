# Whole-character finishing review and correction

- Date: 30 October 2026. Status: pass02 is the agent-preferred review candidate; user selection pending.
- Intent: bounded assisted finishing of the same source-derived whole character, plus evidence-based diagnosis of the earlier cleanup. This is not a controlled model-ranking experiment.
- Scope: one 128×192 standing still. Existing 255-entry native palette, pose, canvas, binary alpha and outer silhouette fixed. Hair, fabric, shoes, tote and a reference-supported facial expression correction permitted. No new generation or service.
- Budget: initial finishing pass plus at most two corrective checkpoints. Used initial pass01 and one corrective pass02. Stopped after reviewed improvement; no third pass needed.
- Backend: dedicated headless Aseprite AI Artist 0.8.2, Aseprite 1.3.18.6-dev. Drawing model is the assigned Sol agent; parent supplied defect-only visual feedback. No other drawing agents, UI, Code-MCP, generic Lua or editor CLI.

## Inputs and starting decision

`inputs/hashes.json` freezes the exact paths and SHA-256 values of the previous experiment's originals, supporting generated cutout, converted seed, rejected finish and retained native/export. Authoritative scene and close-up were visually inspected before drawing; the generated cutout is supporting geometry, not the expression authority. Original scene: `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae`; close-up: `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7`.

Baseline native: previous `candidate-b-structured.aseprite`, SHA-256 `b096b209d41790f81acdb61a0ba908b37b31596bb73d03f9c4d5ec3ac88a062d`. It has 11 visible parts plus a hidden locked source guide, one 100 ms frame, and 7,844 visible pixels. Its visible appearance equals the converted seed; organizing it into parts did not improve its appearance.

Seed-use decision: suitable for a bounded whole-character finish. It retains the rightward three-quarter gaze, tied brown hair/pale tie, olive jacket/cream shirt, broad denim, pale sneakers, tote and relaxed stance. It still has generated simplification and expression differences from the originals. The eye clusters and pose are retained; tiny glints/fabric conversion shades may merge. The facial envelope is roughly x54–73/y17–31, near eye x61–66/y20–24, far eye x70–72/y19–22, nose around x68/y27. Approximate feature ownership was checked on actual native images rather than inferred from layer names.

## Why the earlier cleanup failed

The native and visible diffs are retained in `proof/prior-native-diff.json` and `proof/prior-visible-diff.json`. There are 93 changed native pixels, but only **83 visible changed pixels**. These are sparse accents, not a rebuilt whole-character finish. The visual problem is their location and contrast, not the number alone.

- The extra bag line is exactly **14 newly opaque #b8785a pixels outside the original silhouette**: x93/y78–79, x94/y80–81, x95/y82–91. In the actual export it forms a detached/parallel brown contour. It is not an existing bag fold exposed by transparency. `reviews/prior-bag-line-evidence-8x.png` highlights the added alpha in magenta.
- Denim was changed to #2e4672 along x64/y82–95 and x65/y96–100. That straight high-contrast stripe cuts across the softer hanging-fabric shading. Another 11-pixel lower fold was darkened.
- Jacket changes were mostly thin accents; four shoe pixels became dark marks. They did not resolve larger material planes.
- All ten earlier face-layer edits were hidden by the opaque top hair layer, which actually owned the visible face pixels. Therefore the earlier record's mouth critique cannot be treated as evidence that these ten face edits visibly produced a dotted mouth. The actual composite has **no visible changed face-layer pixels**. The wrong ownership meant successful facial drawing calls could have no visible effect.
- The earlier `operations/` directory is empty. The native before/after and exported pixel coordinates prove these effects; the earlier call shape and intended rationale cannot be recovered. No intent or general model-capability ranking is inferred.

This exposed a native ownership weakness as well as an artistic one: coarse hair-first masks swallowed visible facial content, and the tote part included jacket fabric. Passing exact composite reassembly did not prove correct semantic boundaries.

## Passes and visual decisions

| Checkpoint | Observation | Decision |
| --- | --- | --- |
| pass01 | Broad material work was actually applied and freshly reopened. Shoes quieter; some jacket planes clearer. But crown/ponytail became broad flat patches, tee became a geometric arrow, tote acquired a rigid internal stripe, and smile too far right near the nose read as a pout. | Rejected; preserved native, actual PNGs, authored plan and review sheets. |
| pass02 | Restored inherited curved hair/fabric topology while retaining quieter nearby shade groups; softened tote specks; retained clearer shoe panels/laces and denim work; moved the warm shallow smile left of the nose. Eyes remain exact. | Agent-preferred review candidate; parent defect review found the pout and conspicuous geometric shapes resolved. User approval pending. |
| face-edit proof | Two smile pixels shaded independently on the corrected face layer, in a fresh duplicate. | Proof-only, not the selected art. |

Pass02 changes **1,907 visible pixels**, mostly nearby shade consolidation rather than a large redraw. Specifically denim accounts for 1,401 changes; shirt 241; jacket 143; hair 62; shoes 46; tote 9; smile 5. The number does not measure quality. The final visual gain is modest: quieter material transitions and sneakers, a readable closed smile, and no added external bag contour.

| Region | Decision and remaining limitation |
| --- | --- |
| Face/expression | Five warm pixels make a restrained closed smile; original open-eyed clusters are preserved exactly. Smile is more conspicuous/broader than the original's very shallow expression, so exact expression fidelity remains uncertain. |
| Hair/tie | Preserved crown/fringe/tied silhouette and the native eye openings. Reduced near-shade chatter and used a few connected low-contrast sweep accents. Still differs from the original's broader swept strand volumes; some streaks remain a stylistic difference. |
| Jacket | Reused the original curved fold shapes with consolidated olive ramps; rejected new hard chevrons. Not a full reference-matched fabric redraw. |
| Tee | Restored original crease topology; merged neighboring fabric colors. Existing diagonal fold remains more graphic than the reference. |
| Denim | Joined nearby blue shades and adjusted selected broad hanging folds. Stance and leg opening unchanged. Most changed pixels are small color differences; silhouette and major folds are inherited. |
| Tote/strap | Nine central speck colors softened; original side shadows and alpha retained. No external line or rigid new panel. Strap unchanged. |
| Shoes | Pale vamps and short lace bars are quieter, with original dark soles and stance retained. |
| Overall | Same character/outfit/pose retained. Agent prefers pass02 to seed for this limited finishing task; it does not establish final style matching, user acceptance, animation or gameplay readiness. |

## Native ownership and meaningful edit proof

Pass02 transfers 169 visible face/eye samples from hair to `07-face-and-neck`, and 52 olive jacket samples from tote to `02b-jacket-right`. `proof/ownership-transfer-check.json` verifies the repartition alone changes zero composite pixels. These are visible samples, not reconstructed hidden surfaces. Ownership remains a still-specific interpretation with some boundary/overlap limitations; it is not a ready rig.

The duplicate-only proof darkens `(65,29)` and `(66,29)` from #da784b to existing #c7744e on `07-face-and-neck`. Independent native checks show exactly those two visible pixels change, all other layers and native metadata remain unchanged, and the fresh reopen export is byte-identical. The all-zero negative mask correctly rejects it. `reviews/face-edit-proof-8x.png` shows the effect. Main candidate was reopened afterward and remains unchanged on disk.

## Observed verification

See `proof/final-checks.json`, produced by `rebuild/verify.py` using the existing independent native reader.

- Native SHA-256: **0709390aad9a61bfeb32029f6076530e87155523ff32d3a21082744af0a72e37**.
- Actual transparent PNG SHA-256: **27523c0569a318ff514bd2fc8de1d75b99276f37f9d254536602432a1127bf05**.
- Actual fresh native reopen: 128×192 RGB, 12 layers, one 100 ms frame. Header, all frame non-cel chunks (including palette), layer metadata, cel geometry and protected guide/strap/hands unchanged.
- Actual native visible composite equals actual exported PNG. First and fresh-reopen PNGs byte-identical. Actual export equals authored intended result.
- Alpha differs at zero pixels; 7,844 opaque pixels; no new fabric holes or external contour. Visible ownership disjoint and exhaustive. Eye patch x61–72/y19–24 unchanged.
- Original inputs and all previous experiment files listed in the input manifest retain their original hashes.
- Two-layer scratch verified the asymmetric protected cluster, transparent erase, replacement pixel and native reopen. The system-default Python lacks Pillow; the existing bundled runtime/Pillow was used without installation. The doctor’s direct editor-version probe returned -6; the authorized MCP preflight and actual operations succeeded. This is not an editor CLI validation claim.
- This MCP inventory exposes no `validate` tool. The independent actual-native/PNG checks above were run instead; no unavailable tool is claimed as passed.

## Artifacts and reproduction boundary

- Main native: `passes/pass-02.aseprite`. Transparent actual export: `passes/pass-02-reopen.png`.
- Main sheets: `reviews/final-fullbody-1x.png`, `reviews/final-fullbody-4x.png`, `reviews/final-head-1x.png`, `reviews/final-head-8x.png`.
- Reference previews preserve aspect and are comparison-only: fullbody crop `(464,228)-(769,1023)` resampled once to 72×184 inside a 128×192 panel; close-up crop `(389,99)-(792,399)` to 46×34 inside 53×34. Native source/candidate remain 128×192. All subsequent zoom uses nearest neighbor on a neutral #34363a matte. These are diagnostic display sizes, not established game scale.
- Initial and corrective drawing input JSON lives under `operations/`. `rebuild/prepare_finish.py` and `prepare_correction.py` preserve explicit authored shapes, shade maps, clipping and ownership transfers. Their PNGs under proof are intended-result checks, not substitutes for the actual Aseprite exports. Replay operations through the dedicated MCP against the matching checkpoint; document IDs are session-specific. No native file was written with Python.
- Semantic part PNGs are extracted from the actual native source for diagnostic inspection. They do not reconstruct occluded anatomy.

## Completion boundary and next owner

Construction, native editability, transparency, saved-file reopening, exact export and original protection are locally observed. The scoped request has a genuine new review candidate and an evidence-based explanation of the previous failure. No installation, animation, Godot run, gameplay validation, production enablement, user visual approval, commit, push or publication was performed. Best retained new candidate and latest art attempt are both pass02; proof-only face edit is not selected. Next owner: user to accept/reject this still's visual direction. Broader production remains pending that decision.
