# Luna 6 Max full-body cleanup trial

- Status: observed; one artistic pass and native fresh-reopen proof complete; user visual selection pending
- Date: 30 October 2026
- Trial: B, independently assigned Luna 6 Max arm
- Intent: single-attempt cross-model reconstruction cleanup on a shared native baseline
- Model assignment: `gpt-6-luna`, maximum reasoning effort (task label: Luna 6 Max). The comparison is model plus host/toolchain evidence; no additional art critic or image generator was used.
- Pass budget: one coherent artistic finishing pass. Mechanical save/reopen/protection repair does not authorize another artistic pass.
- Visual/style guide: `docs/art/style-guide.md` (27 October 2026); motion guide read, but this is a static still task.
- Delivery convention: `docs/agents/validated-checkpoints.md`; no separate project delivery reference/Definition of Done exists.

## Frozen task profile

### Target and inputs

The goal is one intentional, visible whole-character cleanup of the common structured still. Make broad clusters and edges more deliberate across hair, clothing, shoes and tote where the reference supports it. The result must read as a coherent finish, not a few isolated changed pixels. No pixel-count quota is imposed.

The approved full scene is the primary identity, pose and costume authority. The approved close-up is the face, expression and hair authority. Both originals were visually opened for this trial. The converted seed is a provenance/control input only; the native candidate-B export is the actual baseline.

| Input | Role | SHA-256 |
| --- | --- | --- |
| `inputs/candidate-b-baseline.aseprite` | Frozen native source, 128×192, 12 layers (11 visible plus hidden, locked guide), existing 255-entry palette | `b096b209d41790f81acdb61a0ba908b37b31596bb73d03f9c4d5ec3ac88a062d` |
| `inputs/candidate-b-baseline.png` | Fresh-reopen baseline export; 7,844 visible pixels | `b3ad887bf2acff2e71404c78d6fc7260784f51f842e6f19d3bd4986777bbf34a` |
| `inputs/source-only-converted-seed.png` | Source-only seed; unchanged task input | `074168d9bfc5b2a2f2751810152bb0c31a71e7027a5368c0b393e17449fb84eb` |
| `inputs/character-scene.png` | Approved identity, pose, silhouette and outfit reference | `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae` |
| `inputs/character-closeup.png` | Approved face, expression and hair reference | `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7` |

Source originals are at `assets/references/approved-2026-10-26/character-scene.png` and `character-closeup.png`. The duplicate inputs above match their recorded hashes. Supporting cutout and historical art candidates are excluded from construction and review.

### Reference observations before drawing

- **Hair:** large swept brown crown/fringe masses, overlapping rear tied volume, pale tie and a few loose silhouette strands. Prefer coherent clumps and intentional openings over many noisy single-pixel edges.
- **Face/expression:** rightward turned face with visibly unequal near/far eyes and rightward gaze; the original has a shallow, restrained smile. Expression is an identity gate. Do not add a pout, U-shaped mouth or separated dotted marks. Leave the baseline mouth unchanged if a correction is not confident.
- **Body/costume:** relaxed three-quarter standing pose, olive open jacket framing an off-white tee, high-waisted wide blue jeans, pale shoes, cream shoulder tote and continuous strap. Retain the long-leg silhouette and distinct garment overlaps.
- **Rendering:** deliberate opaque pixel clusters, selective dark material contours, broad readable material planes, restrained seams/folds, no smooth filter appearance and no baked scene glow in the sprite.
- **Uncertainty:** the original is a resampled painted scene, not a native sprite pixel map. Simplify deliberately; exact pixel correspondence is neither expected nor an objective.

### Locks and scope

- Keep 128×192 canvas, palette entries/palette count, binary alpha silhouette, pose, framing, body proportions and both eyes fixed.
- Preserve the shallow source smile; no mouth edit unless direct comparison makes the existing correction unambiguous. Any expression/identity regression vetoes the art selection.
- One coherent artistic pass over the full character, with meaningful cleanup supported by the originals. Do not spend the pass budget on an isolated proof edit.
- Ownership defects are known: the hair part owns much of the face; tote ownership includes 52 jacket pixels. Layer ownership may be corrected only in the new copy and only with zero composite change; describe any uncorrected limitation.
- No other model, image generator, UI automation, Lua, direct Aseprite CLI, or Code-MCP. Use the dedicated Aseprite MCP in headless mode only, after the parent grants the editor lease.
- If the candidate needs a technical save/reopen repair, preserve the failure and do not perform another artistic pass.

## Plan and decision gate

1. Inspect exact native layer/palette/cel state and backend versions; confirm the copied input and image/pixel delivery. **Complete.**
2. Ownership repair was not needed for the chosen material-color cleanup; the original layer ownership quirks remain disclosed. **Complete.**
3. Perform one deliberate full-body cleanup pass against the frozen references, using existing palette colors and semantic parts. Read back all changed regions and keep a machine-readable operations log. **Complete: seven layer-batched calls, 924 target layer pixels.**
4. Save a new native source and PNG. Independently close/reopen through the dedicated MCP, export fresh PNG, and verify canvas, layer structure, palette, alpha/pose/eye locks, visible-pixel change map and reference hashes. **Complete.**
5. Produce full-body and head review sheets at native 1× and nearest-neighbor 4×. Compare approved reference, raw seed, baseline and final candidate at matching display height. Record one judgment per region and the whole-art decision. **Complete; user choice remains pending.**

The baseline is the current best retained artifact until the candidate is visually judged. Set **best** to the new candidate only if it improves the intended cleanup while preserving identity/expression and locked content. Otherwise keep the baseline as best and mark the candidate not selected. User visual selection/approval remains pending either way.

## Artifacts

| Artifact | Path | Status |
| --- | --- | --- |
| Frozen inputs | `inputs/` | copied and hash-verified |
| Native candidate | `passes/luna6-fullbody-cleanup.aseprite` | saved and fresh-reopened; SHA-256 `dbdf2f693872d2b3c5f102cea01bc1e2441d2452d790770b7b68effd6c563348` |
| First PNG export | `passes/luna6-fullbody-cleanup.png` | 128×192; SHA-256 `c162e373a9b0ed72e2e82f91a6fe6608952444ed3ef9151534fcd29843b65def` |
| Fresh reopen export | `proof/luna6-fullbody-cleanup-reopen.png` | byte-identical to first PNG; same SHA-256 |
| Operations log | `passes/operations.json` | exact native layer coordinates and from/to palette colors for all 924 requested pixels |
| Full-body comparisons | `reviews/final-fullbody-1x.png`, `reviews/final-fullbody-4x.png` | inspected; reference, seed, baseline and final candidate |
| Head comparisons | `reviews/final-head-1x.png`, `reviews/final-head-4x.png` | inspected; reference, seed, baseline and final candidate |
| PNG check detail | `proof/png-checks.json` | canvas/alpha/color/face-lock and per-region changed-pixel evidence |
| Original native palette | `inputs/native-palette.json` | read from baseline and fresh-reopened MCP metadata; exactly identical |

## Technical and visual observations

| Check/region | Method and target | Result | Evidence |
| --- | --- | --- | --- |
| Input identities | SHA-256 on source and owned copies | Pass; all five hashes match | `inputs/` and task notes above |
| Original visual inspection | Direct open of approved scene and close-up | Observed before drawing; cues and uncertainty recorded above | `inputs/character-scene.png`, `inputs/character-closeup.png` |
| Baseline display review | Original, seed and baseline at native 1× and nearest-neighbor 4×; whole-body context and head crop | Pass; inspected before drawing | `reviews/baseline-fullbody-1x.png`, `baseline-fullbody-4x.png`, `baseline-head-1x.png`, `baseline-head-4x.png` |
| Native structure and palette | Dedicated MCP `sprite_info` before edit and after fresh reopen | Pass; 128×192 RGB, one frame, 12 layers, 11 visible, hidden locked guide; full palette and layer metadata identical | `passes/operations.json` and `inputs/native-palette.json` |
| Face/expression | Original/baseline/candidate head at 1×/4×; native composite ROI compare | Identity and smile pixels unchanged in `[53,16,75,38)`; shallow smile remains restrained; still underarticulated at this grid | `reviews/final-head-1x.png`, `reviews/final-head-4x.png`, `proof/png-checks.json` |
| Hair | Original/baseline/candidate at 1×/4× | Cleaner crown/rear-mass clusters; silhouette and remaining reference-shape mismatch persist | `reviews/final-fullbody-1x.png`, `reviews/final-fullbody-4x.png` |
| Jacket and shirt | Full-body comparison plus semantic-layer PNG changes | Fewer near-duplicate cloth tones; broad clothing planes read cleaner; no structural fold redraw | `proof/png-checks.json` |
| Denim | Full-body comparison plus semantic-layer PNG changes | Reduced color noise across both legs; long crease directions remain | `proof/png-checks.json` |
| Shoes | Full-body comparison plus semantic-layer PNG changes | Cleaner color clusters around small shoe details; actual-size shoe detail remains tiny | `proof/png-checks.json` |
| Tote/strap | Full-body comparison plus semantic-layer pixel compare | Bag material is smoother; visible tote/strap silhouette retained; strap native layer is unchanged | `proof/png-checks.json` |
| Silhouette/pose | Full-canvas alpha and matched full-body review | Alpha changed at 0 pixels; visible count remains 7,844; pose/anchor visually unchanged | `proof/png-checks.json`, final comparisons |
| Unchanged content | Full native-layer `read_pixels` comparisons | Hidden guide, tote strap, both hand layers and face/neck layer all changed at 0 pixels; expression ROI changed at 0 | `passes/operations.json` |
| Native reopen/export | Close saved candidate, reopen by path, export new PNG | Pass; reopened PNG byte-identical to first export | `proof/luna6-fullbody-cleanup-reopen.png` |
| Palette/alpha | Native palette comparison and reopened PNG check | Pass; palette identical, 0 new/off-palette visible colors, 0 alpha changes, 0 partial alpha | `inputs/native-palette.json`, `proof/png-checks.json` |
| Aseprite `validate` | Tool availability in this headless session | Not run; no `validate` function was exposed in the connected tool list | MCP inventory |
| User artistic selection | User review of exact final artifact | Pending | — |
| Godot, gameplay scale, animation | Out of scope | Not tested | — |

## Baseline visual notes before drawing

The full-body 1× and 4× sheets show that the structured native baseline preserves the seed's broad stance, outfit and tote silhouette. The figure reads at 1×. The close-up confirms that the sprite's small face does not carry the source's eye/cheek detail as clearly. Hair has a noisy fine-grain perimeter; the jacket and shirt have many small accents; denim creases form a strong busy diagonal; shoe lace/sole clusters are crowded. These are cleanup hypotheses, not evidence that every mark should be removed. The shallow smile appears restrained at this comparison scale, so it is locked for this attempt.

Full-body original crop source rectangle: `(390, 210)-(830, 1020)` in the 1448×1086 scene, resampled proportionally to 192px high for comparison only. Head original crop source rectangle: `(360, 95)-(782, 530)` in the close-up, resampled to 66×68 for comparison only. Candidate/seed head rectangle: `(25, 0)-(91, 68)` in the native 128×192 canvas. Review sheets use neutral matte behind transparent sprite pixels. The 4× sheet enlarges the 1× matched panels with nearest-neighbor interpolation; this creates no art/detail.

## Tool inventory note

The skill's doctor inventory ran on the host. It reported Python 3.14.7, no system Pillow, Node 26.9.0 and uv 0.12.17. Its Aseprite executable probe returned `-6` with no version output; MCP connection, image delivery and native-edit smoke were explicitly not tested by that script. A bundled Python 3.14/Pillow 12.3.0 runtime was used only for deterministic comparison sheets and PNG checks. The dedicated headless MCP later passed preflight and returned version data.

## Single artistic pass and regional judgment

The complete material-color consolidation was the only artistic pass. It used seven batched `draw(kind="pixels")` calls on the named hair, jacket-left, jacket-right, shirt, tote, denim and shoe layers. All 924 requested point entries map to colors already present in the unchanged 255-entry palette; palette lock stayed enabled and no colors snapped. The two hair-region boxes overlap at 11 coordinates, leaving 913 unique native-layer coordinates and 913 changed composite pixels. No alpha, new color, canvas, pose, framing, eye or mouth change is part of this pass.

| Region | Agent judgment against reference and baseline | Candidate status |
| --- | --- | --- |
| Hair | The crown/rear mass reads with less color speckle and a steadier surface. Hair flow and tied-volume silhouette remain simpler and rounder than the original. | Improved for cleanup; likeness still limited |
| Face/expression | The face remains underarticulated at 128×192, but the shallow smile and eye relationship are unchanged. No pout, U-shaped mouth or dotted-mouth regression. | Protected and unchanged; user identity review pending |
| Jacket | Near-duplicate olive tones merge into fewer clear planes. The open jacket shape is stable; sleeve folds are still broad/simplified. | Improved for cleanup |
| Shirt | Cream and pink-grey values form fewer, clearer patches. Shirt shape and neckline remain unchanged. | Improved for cleanup |
| Denim | Color noise is reduced while both wide-leg forms remain. The strong diagonal creases are still present and remain a style gap. | Improved modestly; folds unresolved |
| Tote/strap | Tote fabric reads smoother with its existing soft light/shadow pattern. Its visible contour and strap placement are unchanged. | Improved for cleanup; flatness remains a limitation |
| Shoes | Lace/toe color variations are less busy and the sole/stance remain. Shoe details remain small at native size. | Improved for cleanup; gameplay readability untested |
| Silhouette/pose | Same visible alpha mask, foot positions and standing pose; no pose redraw. | Preserved exactly at composite alpha |

At native 1× the candidate remains recognizable and visually cleaner than the seed-identical baseline. At 4× the larger material clusters are easier to read. This is a modest finishing improvement, not a new likeness reconstruction. Candidate B remains the best retained baseline if the user values its original fine detail more; otherwise the Luna 6 candidate is the agent-preferred cleanup. User review decides between them.

## Selection and handoff

- Best retained: Luna 6 candidate is agent-preferred for the scoped whole-body cleanup; candidate B remains preserved as the untouched baseline.
- Last attempted: same Luna 6 one-pass candidate; no art correction round.
- Selected/user-approved result: none; user visual approval is pending.
- Last proven state: output native reopens, its PNG is exact, palette/layers are retained, and all protected checks pass.
- Smallest next action/owner: parent compares both model arms and presents the exact candidates for user visual selection; no additional art pass is authorized by this trial.
