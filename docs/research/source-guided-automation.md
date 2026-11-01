# Source-guided pixel art: automation and model routing

Date: 27 October 2026. Status: evidence-backed workflow proposal; model-tier performance and savings are unmeasured. This research changes no art approvals, production grid, runtime assets, or accepted ADR.

## Recommendation

Use source-guided preparation as the default starting point for new studies of this character. Prefer **conversion into a structured seed, an aligned original for guidance, then bounded native cleanup**. Keep trace-only construction available for regions that conversion handles poorly. The local comparison favors conversion plus cleanup for this particular face; it does not establish a universally best method.

Once crop, scale, palette and reviewed masks are fixed, software can create the entire first color pass and assemble its visible parts into native layers. No language-model call is needed to calculate each pixel. Model effort then concentrates on choosing those parameters, correcting exceptions and judging the result. Whether a cheaper model performs those remaining tasks reliably must be measured.

## 1. Evidence from the current workspace

The live repository is newer than the supplied continuation summary. These are existing recorded results, not tests rerun by this research session.

| Evidence | What it establishes | What it does not establish |
| --- | --- | --- |
| [Reference-drift audit](../experiments/2026-10-27-reference-drift-audit/record.md) | Free interpretation of geometry and review against prior drawings allowed face/hair/expression drift; increasing grid size did not isolate or fix the cause. | That the earlier agent never saw originals, or that the smaller grid is intrinsically incapable. |
| [Assisted head comparison](../experiments/2026-10-27-assisted-head-comparison/record.md) | One 480x448 approved close-up crop became a 120x112 seed; nine visible semantic layers exactly reassembled it. Converted/cleaned C01 retained identity/expression better in agent review than traced A02. Native reopen, localized edit and fresh-folder static rebuilds were recorded. | A user-approved final sprite, a fair model-tier comparison, or measured time/cost savings. Equal checkpoint ceilings were not equal measured labor; C01 also used a disclosed mouth rollback. |
| [Preparation source](../experiments/2026-10-27-assisted-head-comparison/prepare.py) and [native builder](../experiments/2026-10-27-assisted-head-comparison/build.lua) | Foreground palette extraction, BOX sampling, alpha coverage, visible-part partitioning, color seeding, layer/cel creation and native saving already have concrete code. | Automatic semantic segmentation. The polygons, feature islands and sample points were authored; crop, grid and coordinates are hard-coded. |
| [Denim repair](../experiments/2026-10-27-denim-alpha-repair/record.md) | Color-based cleanup erased twelve valid fabric pixels; separate moving parts exposed joint seams. Reviewed removal masks and joint backing repaired those defects. | That color thresholds, exterior connectivity, or filling every hole can safely decide transparency. Exterior connectivity alone would have saved only eight of the twelve reported pixels. |
| [Character/shop review](../experiments/2026-10-27-character-shop-quality-review/record.md) | Current character source is standing-alpha-v03; shop source is shop-modular-v02. Scoped native reopen, eight-frame Godot playback, shop assembly and quality checks are recorded. A neck pixel on the wrong semantic layer failed only during motion. | A complete combat/production pipeline, packaged build, full strict binary/header audit, or fresh full-constructor replay of the latest repairs. |

The current 96x216 standing prototype and historical 128x192 drawings are different studies. The 120x112 head crop is another diagnostic grid. None becomes the final production resolution through this proposal.

The approved scene and close-up were visually reopened for this research. The imported package's START_HERE.md, HANDOFF.md, workspace/INTEGRATION.md, workflow/FIRST_EXPERIMENT.md and IMAGE_PROMPTS.md were read. Its resolution_comparison.png and sampling_comparison.png were inspected: they demonstrate changes in sampled detail, not finished pixel art or a winning production grid. The two separately named explanatory diagrams, pixel_art_workflow_visual.png and pixel_mapping_visual.png, were not found inside the imported package; their contents are not assumed. The package remains an immutable historical input.

## 2. How source guidance changes model dependence

An independent redraw asks the model to infer shapes, translate them into coordinates, allocate pixels, choose colors and preserve expression simultaneously. An aligned source and deterministic seed supply much of the geometry and color information directly. Hard masks and validators can also prevent changes to areas outside the task.

That removes mechanical decisions and constrains the search space. It does not remove ambiguity about which details define the person, whether a sampled eyelid still reads correctly, or whether a cleaner hair shape has become a different hairstyle. A weak model can faithfully trace the wrong boundary, remove a meaningful one-pixel feature, or approve an incorrect expression. Giving it an underlay is less constraining than actually transferring source-derived pixels.

The existing comparison illustrates this distinction: trace A retained broad framing yet simplified the face and hair into a different treatment. Converted C retained more of the original, while a seemingly helpful mouth cleanup in B02 removed the shallow smile and needed selective rollback. Therefore preserve a good source-derived region unless a specific visible defect justifies changing it.

**Supported conclusion:** the first-fill workload can move out of model inference. **Testable hypothesis:** cheaper vision/tool-capable models can handle a larger share of bounded cleanup. **Still unknown:** their reliable acceptance rate and total cost after retries, reviewer time and escalation. No percentage of the whole art workload is justified by current measurements.

## 3. Exact division of work

The table distinguishes executing a recipe from choosing a good recipe. Small-model assignments are candidates for testing, not certifications.

| Step | Script/no AI | Small-model-friendly work | Strong visual judgment still needed |
| --- | --- | --- | --- |
| Source inspection | Hashes, dimensions, mode, alpha, bounds, metadata, duplicate detection. | Populate a manifest from measured results. | Establish identity/style authority when references disagree. |
| Crop selection | Apply a stored rectangle; derive bounds plus margin from an already valid subject mask. | Propose a candidate region with explicit uncertainty. | Choose a crop from an opaque busy scene; keep bun, wisps, tote and relevant anatomy. Alpha bounds on an opaque image identify the whole image. |
| Sizing, alignment, scale mapping | Apply one uniform transform, padding and declared anchor; record rounding. | Check measured values against the recipe. | Choose a native detail budget and judge eye/fringe/mouth collisions. No independent width/height stretching. |
| Image simplification | Produce a small named set of resampling/quantization candidates. | Run comparisons and label settings. | Decide which secondary details can merge without redesigning the face or style. |
| Palette extraction and mapping | Sample reviewed foreground; apply one recorded palette and dithering policy. | Check allowed colors/material assignments against explicit instructions. | Preserve skin/hair separation, feature contrast and material/light relationships. A frequent color is not necessarily an important color. |
| Outline suggestions | Extract mask boundaries or image-gradient candidates on a separate guide. | Flag a local contour break for inspection. | Distinguish silhouette from shading/texture; choose selective outline placement and weight. |
| Masks and segmentation | Apply existing masks; rasterize reviewed polygons; label connected regions; check coverage/overlap. | Correct an unambiguous named region under a mask. | Separate hair/skin/coat/strap in ambiguous overlaps; review thin structures and occlusion. Color regions are not semantic parts. |
| First color fill | Transfer sampled pixels or material fills into region images in bulk. | Usually unnecessary; invoke and inspect the result. | Select material roles or override a source defect before freezing the recipe. |
| Tracing preparation | Create aligned crop, underlay, optional guide overlays, masks and layer scaffold. | Routine assembly using explicit names and ordering. | Verify anatomical registration and that the guide preserves useful information. |
| Native assembly | Create layers/cels, apply positions/palette, save and export through the authorized adapter. | Execute a bounded patch or label a known part. | Decide whether part ownership supports the intended revision or motion. Visible masks do not reconstruct hidden surfaces. |
| Local cleanup | Apply exact patches, palette substitutions and rollback; enforce frozen masks. | Small nonidentity edge repairs with precise criteria and review. | Eyes, expression, cheek/jaw, crown/fringe, significant silhouette changes and interpretation of ambiguous noise. |
| Multiple poses | Apply known crops/anchors with shared scale, canvas, palette and explicit root offsets. | Check frame count/order/metadata. | Infer anatomical correspondences, intended travel, volume/identity consistency, new surfaces and contact. |
| Export and checks | Dimensions, alpha coverage, palette/metadata locks, protected pixels/layers, fresh reopen, exact reconstruction where promised. | Summarize observed failures. | Judge identity, style and actual-size readability; inspect motion and engine context. User owns final artistic selection. |

Pillow documents the crop, bounds, resizing and quantization operations [P1]. Aseprite documents layers/cels/native saves and automated exports [A1–A2]. The routing choices above are engineering proposals informed by those capabilities and the repository evidence, not model benchmarks.

## 4. A practical construction sequence

1. **Freeze authority and one recipe.** Use the approved original scene/close-up. Record image hashes, coordinate convention, crop, target grid, source-to-native transform, palette policy, alpha policy and viewing scale. A strong visual pass resolves the few ambiguous choices once; subsequent runs reuse them.
2. **Prepare deterministic candidates.** Crop and resize RGB/RGBA, then map to the recorded palette. Start with the existing BOX route as the replay baseline. Compare another filter separately only for an observed defect. Keep both the unmasked reduction and masked seed. Never choose a different filter/grid midway through a model comparison.
3. **Apply reviewed coverage and ownership.** Separate silhouette coverage from semantic layer ownership. Reuse frozen polygons/masks for the first experiment. Check unassigned samples, overlaps/order and foreground loss. Do not use global color deletion as background removal. Generate uncertain mask proposals for review rather than inventing missing anatomy.
4. **Fill and assemble in bulk.** Build region PNGs, named native layers/cels and an aligned guide using the existing backend. The code writes the first pixels; the drawing agent starts with a populated candidate. Check exact seed reassembly before adding artwork. Treat this initial file as a seeded native candidate until useful revision has been demonstrated.
5. **Review before cleanup.** Show original, raw seed and actual native export at 1x and integer zoom. Record a short defect list and continue/correct/reject decision. Keep an already convincing mouth or eyelid protected instead of rewriting it to prove that drawing occurred.
6. **Route bounded corrections.** Exact coordinate/color operations stay in scripts. A cheaper model may attempt explicit low-risk repairs after its own tool/image preflight. Route ambiguous identity or style changes to stronger visual reasoning. One failed scoped pass may escalate; retain the failed output and include the rescue cost. Never let an automatic lint rule erase all small clusters or fill all holes.
7. **Verify the native result.** Save, reopen and export. Check protected layers and metadata as well as the flattened PNG. Demonstrate a useful local revision on a duplicate. Coverage checks flag defects using reviewed solid regions and intentional-hole exceptions; they do not silently paint corrections.
8. **Extend only the proven boundary.** For a new pose use shared scale and meaningful anchors, preserving intended root movement. Inspect all actual frames and Godot playback when runtime claims are in scope. A static seed does not prove combat motion. The agent owns all painting and correction; the user reviews concrete results.

## 5. Tool boundaries and implementation cautions

**Python/Pillow and existing helpers:** inspection, crops, transforms, palette sampling/mapping, mask rasterization, seed/part images, guide/review sheets and manifests. The kit's helper already implements inspect, seeds and normalize; it expects provided crops/masks/anchors and is not an automatic segmenter. It requires exact crop aspect ratios and new output directories. Its README records no EXIF/profile normalization, unweighted partial-alpha palette sampling and no palette unification in normalize. These are explicit scope gaps, not reasons to install a new service.

**Aseprite through the authorized drawing adapter:** create/import native parts, manage layers/cels/palettes/frames, apply bounded corrections, save/reopen and export. Do not modify an editor-owned file behind its back. A documented CLI or Lua API is not proof that the current MCP exposes it. Discover the current capability; retain a prepared seed and report any actual adapter gap without bypassing access controls.

**Drawing/review models:** choose and review the recipe, semantic masks and simplification; repair local visual defects; evaluate likeness/style/temporal coherence against originals. Route by task ambiguity and failure risk, not just region size: a two-pixel eye change can need more judgment than a large uniform jacket fill.

**Image generation:** obtain a missing pose, occluded view, expression or simpler same-angle production reference only when it addresses a named source limitation. Use the preserved prompt pack and canonical attachments. Review the returned image before conversion; it is supporting material unless the user approves otherwise. No new generation is needed for the proposed first benchmark because its source already exists. A generative edit cannot guarantee exact protection of unrelated native pixels.

Implementation details that matter:

- Resize before converting to palette mode: Pillow forces nearest-neighbor for P/1-mode resizing. RGBA median-cut is unsupported; preserve alpha deliberately through palette mapping [P1]. The existing kit explicitly uses premultiplied coverage for filtered RGBA reduction. Pin actual dependency versions; current web documentation is not an instruction to upgrade the installed environment.
- Retain shared foreground palette values across comparable frames. Fully transparent RGB and background colors must not dominate palette extraction. Thresholding coverage can remove hair/tote strands; threshold and intentional openings need review.
- An edge detector returns candidate edges, not decisions about which outline is artistically appropriate. Connected components label connectivity, not hair/coat identity. These limitations are inferences from the documented algorithm operations [C1–C2]. No OpenCV dependency is needed for the initial experiment.
- Aseprite supports reference layers [A3], but NewLayer(fromFile=true) is documented as opening a file dialog [A4]. Do not promise headless reference-layer import from that option. Use an actually verified adapter, or a hidden ordinary guide layer with explicit export exclusion and a leakage check. Export settings can include hidden layers [A2].
- Normalize poses around measured anatomical anchors with explicit motion offsets. Do not fit every pose to its tight bounding box or force every lowest visible pixel to ground; this changes scale or removes intentional jumps.

## 6. Smallest repository implementation plan

Keep historical experiment/package files unchanged. Begin in the new [automation-routing experiment](../experiments/2026-10-27-automation-routing.md), with new output subdirectories.

| Increment | Reuse | New work | Focused proof |
| --- | --- | --- | --- |
| 1. Frozen preparation recipe | Kit reference_lab.py; existing head prepare.py/traces.json and known B00 seed. | A thin experiment entry point that takes a recipe instead of embedding crop/grid/paths; record input/mask/palette hashes and versions. | Two new output directories produce identical decoded seed/part pixels and invariant recipe fields. Originals unchanged; missing masks fail clearly. |
| 2. Native seed assembly | Existing build.lua arm B at limit 0; current Aseprite adapter. | Parameterize only a new experiment copy/adapter; build layers and an excluded guide without executing old refinement passes. | Native composite equals the frozen seed, useful layer ownership inspected, fresh reopen matches, guide absent from export, one scoped duplicate edit preserves other layers. |
| 3. Bounded tier pilots | Director protections, reference_review.py, pixel_checks.py and applicable native checker. | Identical copied inputs, same task/mask/limits, separate cheap/strong runs and a no-change seed control. | Hard technical compliance plus independent visual decisions; total review/retry cost recorded, unknown telemetry left unknown. |
| 4. Repeat and decide | Same frozen pilots and rubric. | Fresh repeated runs only after tools and tasks work; optional factorial follow-up if causal method effects matter. | Adopt a cheaper tier only for the task class its results support. No production-resolution or full-pipeline claim. |

The existing head builder hard-codes 120x112, its coordinate transform and facial refinement strokes; it is not a general import command. Keep its recorded outputs intact. After the new replay is demonstrated, promote the useful preparation functions to one maintained repository tool instead of building a general art framework now.

Use the current project checker/profile as a regression check for the standing/shop assets if implementation touches them; they are outside this head experiment. Do not apply a body-specific zero-hole policy to hair or reuse the historical v03 head mask for a different canvas. The latest full-character constructors have source-level fixes but no recorded complete rerun; the first new replay must demonstrate its own reproducible boundary.

## 7. Distinct deliverable states

| State | Meaning and required evidence |
| --- | --- |
| Raw converted draft | Sampled/quantized source pixels with a reproducible recipe. Not an approved asset. |
| Tracing underlay | Aligned visual guidance, kept immutable and excluded from runtime export. It may retain detail the native grid cannot represent. |
| Native editable master | Meaningful layers/parts/cels plus construction/patch provenance and an observed useful local revision with protected content and reopen/export checks. Native format alone is insufficient. |
| Approved final asset | The user accepts the specific artifact for its stated use and the applicable technical/runtime evidence exists. Concept approval, agent recommendation and prototype playback do not imply this state. |

## 8. Research and continuation status

This session inspected current repository/package text, constructor sources, approved originals and existing comparison images; checked primary documentation; and prepared a controlled implementation/benchmark plan. No art was generated, no preprocessing or native constructor was executed, no model-tier trial or Godot run was performed, and no performance/cost saving was measured here. Existing record claims remain scoped to their original artifacts.

Next owner: the implementation agent runs the deterministic replay/native-seed checkpoint, then the bounded tier pilot using actually available authorized models. The user selects artistic outcomes; no manual sprite painting is assigned to them. No commit, publication, paid service, new integration or tool-installation decision is implied.

## Primary sources

Accessed 27 October 2026. API capability is distinct from installed-version/adapter validation. Current stable Pillow documentation identifies 13.0.0; the prior head experiment records 12.3.0. Preserve the tested runtime for replay and record the actual version.

- [P1: Pillow Image API](https://pillow.readthedocs.io/en/stable/reference/Image.html) — crop, bounds, resampling, palette-mode behavior, quantization and alpha interfaces.
- [P2: Pillow concepts](https://pillow.readthedocs.io/en/stable/handbook/concepts.html) — filters, transparency, orientation and color modes.
- [A1: Aseprite Sprite API](https://www.aseprite.org/api/sprite) — native layers, cels, palettes, frames and saves.
- [A2: Aseprite CLI](https://www.aseprite.org/docs/cli/) — batch/script/export operations and layer inclusion/exclusion.
- [A3: Aseprite reference layers](https://www.aseprite.org/docs/reference-layer/) — guide-image behavior.
- [A4: Aseprite NewLayer command](https://www.aseprite.org/api/command/NewLayer) — reference and fromFile options, including dialog boundary.
- [C1: OpenCV Canny documentation](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html) — gradient/threshold edge operations.
- [C2: OpenCV shape analysis](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html) — connected-component labeling and statistics.
