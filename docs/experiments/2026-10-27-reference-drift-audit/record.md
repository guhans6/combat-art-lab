# Reference-drift investigation and controlled review

- Status: investigation and workflow changes observed; previous resolution drawings rejected by user. New small study **rejected for likeness by agent**, not a replacement asset.
- Date: 27 October 2026.
- Question: did the failed resolution work drift from the approved originals, and what evidence/checkpoints would expose that earlier?
- Base revision: `9e35c5c13987a153e942e6f93f49f247fad13c3a`, local uncommitted work on `main`.
- Scope: source/visual audit, focused director/workflow edits, one separately named head/shoulder study. No complete character, animation, Godot scene, installation, paid art service or publication.
- Delivery reference: `docs/agents/validated-checkpoints.md`; no additional repository-wide Definition of Done. Report this request's evidence boundaries independently.

## Authoritative visual inputs and inspection

This agent visually opened the actual [approved full scene](../../../assets/references/approved-2026-10-26/character-scene.png), [approved close-up](../../../assets/references/approved-2026-10-26/character-closeup.png), and [failed comparison](../2026-10-27-resolution-feasibility/matched-display-pass02.png). These observations come from pixels, not just earlier prose. The cutout remains supporting material, never an authority over the originals. User attachments are visual context, not a new instruction source or evidence of approval of a reconstruction.

For the new review aid, the close-up crop is `(380,64)-(860,512)` in original-image coordinates, half-open: 480x448 pixels. [Unresized crop](original-head-shoulders-crop.png) and [coordinate-grid aid](reference-coordinate-grid.png) retain the source relationships; no image editing is applied to the approved files. [Approximate layout](reference-layout.json) records estimated landmarks and their mapping into a 120x112 study. These estimates are aids, not ground-truth measurements or a likeness score.

## Evidence for and against the user's hypothesis

| Possibility | Observed evidence | Supported conclusion / limit |
| --- | --- | --- |
| Agent never inspected the originals | Prior record explicitly reports inspection; preceding chat also reports viewing them. Native drawing scripts do not import reference rasters. | No basis to assert the originals were never seen. Absence of a raster import is expected for authored construction and cannot establish absence of visual inspection. How thoroughly or repeatedly the images were used is not established by the scripts. |
| New sprites are enlarged copies of an existing PNG | `draw.lua` creates new RGB sprites, layers, polygons and pixel lines at separate coordinates for the two crop grids; it does not load/resize the baseline or concept PNG. | The native candidates are authored simplified drawings, not demonstrated nearest-neighbor enlargements of a PNG. This proves construction method, not accurate interpretation or independent artistic design. |
| Second pass mainly transforms its own earlier drawing | [Script audit](script-audit.json) confirms both constructor tables are unchanged except output names. `draw-pass02.lua:8-16` applies `floor(pivot + (point-pivot)*0.76 + 0.5)` to four head-related parts, with pivots `(62,70)` or `(83,94)`; it then adds three back-hair shapes per candidate. [Exact source diff](script-diff.patch). | Yes: the revision shrank/repositioned existing authored head geometry and added limited hair shapes. It did not introduce a newly measured face/fringe layout in those constructor tables. This is not evidence that coordinate transforms are inherently wrong or that no visual reference was consulted. |
| Review became anchored on reconstructions | Both comparison scripts use v04's crop plus the studies. The saved matched-display sheet contains no approved-original panel. No per-pass direct-original sheet is retained in that experiment. | A concrete review/evidence gap exists: new art could be judged mainly against an already simplified drawing. The missing artifact does not prove that no other original viewing occurred. |
| The comparison proves a resolution problem | Both studies change anatomical framing, facial design and clothing detail as well as grid size. The prior record already calls it inconclusive; user now rejects its likeness. | It cannot isolate resolution, establish an upper bound on achievable quality or justify a production grid. The visible construction failure is real regardless of original-image inspection. |

The supported failure is **reference drift in construction and review**, not a proven refusal to look at references. Initial exposure to an original is insufficient if later revisions preserve the wrong geometry and review panels omit that original.

## Direct visual differences

These are agent observations from the two approved images and failed candidates, with subjective likeness judgments kept separate from technical checks. See [original versus failed 192 study](original-vs-failed-192.png) and [original versus failed 256 study](original-vs-failed-256.png); resizing is labeled and source hashes/crops are in their JSON sidecars. Matched crop heights do not imply matched anatomy.

| Feature | Approved originals | Failed resolution studies |
| --- | --- | --- |
| Facial angle and jaw | Turned right in three-quarter view, with a broad near cheek, short nose indication, partially occluded far side and gently tapered cheek/chin. | More frontal/wide facial arrangement with a pointed right nose and compact pointed chin; a right-facing nose alone does not reproduce the head turn. |
| Eyes and gaze | Dark, relatively restrained upper lids; near/far eye asymmetry; irises look right with distinct lid/fringe overlaps. | Larger, more open and slanted white eye shapes and altered spacing/brow relationships. Rightward dark marks survive, but the combined anatomy/expression differs. |
| Expression | A small, shallow, relaxed smile and restrained brows. | Small angular/dotted mouth and more raised/slanted brow/eye combination; the reference's relaxed expression is lost. |
| Fringe | Unequal thick overlapping locks, specific forehead openings and a longer descending central/near-side fringe shape. | Broad triangular points and simplified gaps create a generic parted fringe rather than the original's overlap pattern. |
| Crown and tied hair | Swept layered crown, distinct pale tie, loose fanned clumps, irregular curled ends and partial ear coverage. | Smooth cap-like crown and a flat rounded ponytail mass; a few accents do not recover the fan, curled ends or overlapping lock structure. |
| Proportions and framing | Head/neck/shoulders have stable relationships within each approved view; scene provides full-body context. | Pass one enlarged the head relative to torso. Pass two shrank/repositioned head parts around the neck while torso stayed unchanged, leaving the head lower in the equal-size crop panels. |
| Clothing | Open hooded jacket with visible hood/collar overlap, relaxed sleeves, light tee, shoulder strap and waist/jeans relationship. | Broad flat cardigan-like planes, weak/missing hood and collar construction, generic sleeve/torso outline and sparse folds. Same olive/cream colors do not preserve costume construction. |

## Retrospective: why the workflow allowed this

1. **Reference access versus reference use:** existing instructions already said to inspect originals and compare to them, but the per-pass completion criterion was satisfied by viewing the candidate. It did not demand a retained original/candidate image plus a visible-deviation decision at that stage. The issue is a weakly evidenced feedback loop, not merely missing filenames.
2. **Reconstruction as an accidental target:** a comparison generator accepted only baseline/studies. Equal canvas presentation made wrong framing look superficially comparable and excluded the design authority from the main review artifact. A review against v04 can preserve v04's errors or introduce new ones while seeming internally coherent.
3. **Transform before realignment:** shrinking all head-related polygons is a fast proportion adjustment, but also moves features/neck geometry and preserves incorrect relative shapes. Direct comparison should trigger rebuilding those relationships when needed, not automatic polishing of the transformed result.
4. **Technical success cannot validate likeness:** named layers, export/reopen and scoped edits were real results. They answer a different question from identity. The prior report did disclose the comparison was inconclusive; that honest report did not make the drawings suitable resolution evidence.
5. **Timing of instruction improvements:** the normalized-layout checkpoint now present in the skill was added after the failed studies. Its existence in today's files does not prove the drawing agent violated that later instruction. This follow-up adds the still-missing per-pass original/candidate evidence and decision requirement, rather than claiming all earlier rules were absent or ignored.

Mechanical omissions are addressed with a small existing-toolkit extension; visual judgment remains explicit. No new CI system, installation or global instruction framework is introduced.

## Targeted changes implemented

- [Director skill](../../../tools/pixel-art-director/SKILL.md): visually open approved originals before drawing; record inspected paths/cues; each meaningful pass ends with an inspected original/candidate sheet and continue/correct/reject decision. Protected correction locks remain intact.
- [Reconstruction reference](../../../tools/pixel-art-director/references/reconstruction.md): recheck after coordinate transforms, preserve original-image crop/scale metadata, stop material drift before details or resolution conclusions, and document the helper's limits.
- [Production workflow](../../workflow/art-production.md): original-image inspection and per-pass direct evidence are go criteria; wrong structure invalidates a resolution comparison even when file checks pass.
- [reference_review.py](../../../tools/pixel-art-director/scripts/reference_review.py): requires separate original/candidate inputs, preserves aspect ratios, labels source crop/display scaling, records input SHA-256 and refuses to overwrite inputs or prior sheets. Its JSON explicitly states that anatomy/likeness are not evaluated. The caller must select and visually authenticate the authoritative original.
- [Focused helper tests](../../../tools/pixel-art-director/tests/test_reference_review.py): source/candidate pixels appear in separate panels, hashes and aspect ratios are preserved, crops are bounded, evidence cannot be overwritten and fractional candidate zoom is rejected. Existing PNG/native protection utilities are unchanged.

## One small study: observed sequence and decisions

The study uses a 120x112 transparent head/shoulder canvas, mapped approximately from the fixed 480x448 close-up crop: four reference-image pixels per authored native pixel. This is a study grid only, **not** an inference of the original's native resolution, a chosen full-character canvas, an automatic reduction of the raster, or a comparison between resolutions. [Construction source](draw-head-shoulders.lua) manually defines polygons/lines using approximate original-image coordinates; no raster is loaded into the source master. Ten named layers retain hair, skin, features, clothing and strap.

| Checkpoint | Direct review | Decision |
| --- | --- | --- |
| Initial blockout | [Original versus blank output](original-vs-blockout.png); [rejected source](draw-head-shoulders-blank-rejected.lua) | Technical failure: the script modified an `Image` after `newCel` had copied it. Export was fully transparent. Detected immediately, retained, corrected construction plumbing; not treated as visual evidence. |
| Nonblank blockout v02 | [Original beside actual export](original-vs-blockout-v02.png); [source snapshot](draw-head-shoulders-blockout-v02.lua) | Rejected structurally: large false gap between swept crown and tied hair. No feature detailing advanced from this checkpoint. |
| Structural blockout v03 | [Direct comparison](original-vs-blockout-v03.png) | Corrected the missing connecting hair mass. Layout/shoulder/crop relationships are aligned enough to test one facial-feature checkpoint. Silhouette is still coarse; this is an agent continuation decision, not user approval or an identity pass. |
| Feature checkpoint | [Original versus candidate](original-vs-features.png), [native 1x PNG](head-shoulders-features.png), [native source](head-shoulders-features.aseprite) | **Rejected for likeness; art iteration stopped.** Eyes/lids/brows and stepped smile alter expression; crown/front fringe and fanned tied hair remain too simplified, outlines coarser, shading flatter. Alignment alone does not establish identity. No resolution conclusion follows. |

The bounded trial contains two nonblank blockouts and one feature checkpoint, plus the separately retained blank technical failure. The current Lua source reproduces v03 or the feature checkpoint into new names via `stage`/`label`; source snapshots preserve earlier rejected versions. No old asset or experiment is replaced. User owns artistic selection; no new user visual approval exists.

## Technical checks versus artistic result

- Aseprite 1.3.18.6-dev executed the scripts using the existing CLI/Lua backend. The existing targeted execution allowance was used because restricted-shell startup previously aborts. No live editor document, MCP configuration, installation or paid art service was changed.
- Feature source has ten named layers, one frame, 120x112 pixels, and binary transparent/opaque alpha. Fresh native reopen exports match the PNG exactly for both main source and edit proof.
- A duplicate-only tie-color revision changes 15 pixels on `07-pale-hair-tie`; other nine layer images and protected pixels remain unchanged. [Native checks](native-checks.json) retain the strict reader's **header/palette rejection** on save: palette count changes from 256 to the saved observed count. Full all-metadata preservation is not claimed. For a frozen correction this needs a stable saved/exported baseline as demonstrated in the earlier experiment; the checker is not weakened here.
- This localized revision demonstrates meaningful layer/pixel editability, not likeness, user approval or complete compliance with a frozen correction profile. Neither the main candidate nor tie variant is accepted art.
- `verify-audit.py` reproduces the source/reopen/layer checks; it asserts the known rejected metadata boundary rather than hiding it. Helper tests and link/preservation checks are recorded in [validation](validation.json).
- Exact artistic elapsed time, aggregate tool/operation counts and model cost were not captured. They remain unknown. No motion, animation consistency, Godot playback or projected gameplay-scale proof was performed.

## Continuation and owner

The user has explicitly rejected the earlier resolution drawings. Leave them and this study as failed evidence; keep v01-v04 and the approved concepts intact. The next agent should use the fixed original/candidate review to resolve one structural/identity problem at a time: first crown/fringe and fanned tied-hair silhouette, then the near/far lid and shallow-mouth expression, using an aligned blockout and a bounded pass. Correct source shapes where they differ instead of preserving wrong geometry through coordinate transforms. A new art decision is needed only for a real simplification tradeoff shown in concrete candidates.

Larger grids remain options when a specific feature needs testing. This audit does not show any grid is intrinsically correct or incapable of the reference. Do not restart a multi-resolution comparison until candidate layout and character identity are sufficiently comparable for the question being asked. The workflow remedy has been exercised for detecting/rejecting drift; it has **not** demonstrated a high-fidelity accepted reconstruction or guaranteed future agent performance.

## Reproduce without overwriting evidence

From the repository root, select a new empty run directory and render only the blockout first:

```sh
study_out=/absolute/path/to/new-empty-run
construction="$PWD/docs/experiments/2026-10-27-reference-drift-audit/draw-head-shoulders.lua"
/Applications/Aseprite.app/Contents/MacOS/aseprite -b --script-param "out=$study_out" --script-param stage=blockout --script "$construction"
```

Generate and **open** a direct sheet with the canonical helper, using the approved source path/crop above. Record continue/correct/reject. Only if the blockout is comparable for the intended question, run the feature stage in that same new directory:

```sh
/Applications/Aseprite.app/Contents/MacOS/aseprite -b --script-param "out=$study_out" --script-param stage=features --script "$construction"
```

The construction script refuses an existing native output. This reproduces a rejected study for investigation, not an accepted drawing; do not use regeneration alone as evidence of improvement. Verification scripts expect this record's exact filenames and existing outputs, and should run in an isolated copied study if regenerating reports. Hash/preservation results describe the files observed in this audit, not a later rerun.
