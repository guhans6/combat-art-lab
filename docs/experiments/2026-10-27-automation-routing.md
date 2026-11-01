# Experiment: deterministic preparation and bounded model routing

- Status: **planned, not executed**. Repository/package audit and proposal completed on 27 October 2026; no new image, native asset or tier trial is claimed.
- Question: can a script prepare a repeatable, meaningfully layered seed, and can a cheaper model perform specified revisions from that seed with acceptable quality and less total effort?
- Relevant guidance: current AGENTS.md, ADR 0001, [art workflow](../workflow/art-production.md), [style guide](../art/style-guide.md), [asset contract](../art/asset-contract.md), [automation research](../research/source-guided-automation.md), and existing pixel-art-director protections.
- Baseline: the observed [assisted-head comparison](2026-10-27-assisted-head-comparison/record.md), especially prepared/converted-seed.png and b00-separated-seed.aseprite. Final C01 and newer standing-alpha-v03/shop-modular-v02 remain evidence/current assets, not files to replace.
- Scope: one existing head/shoulder crop, deterministic replay, then a four-run feasibility pilot. No new pose, generation, production grid, attack, environment or engine work.
- Completion criterion: replayable seed/native assembly plus separate technical and visual evidence for the two candidate model tiers on two defined task classes. Results may justify only a narrow routing choice.
- Authority/budget: documentation and planning are authorized in this session. This record does not launch model calls or authorize new paid usage, credentials, installation, publication or broader machine access. Implementation should use the current authorized tool path and available exact model assignments; report missing capability without substituting a model silently.

## Plan

### Checkpoint 0: freeze the baseline and task definitions

Read current repository instructions and Git state again. Create a new run directory; refuse an existing output directory. Copy/freeze exact reference and baseline inputs and record SHA-256 values. Do not modify the historical package or earlier experiment scripts.

Initial replay settings are inherited controls, not production recommendations:

| Parameter | Initial control |
| --- | --- |
| Identity/style authority | assets/references/approved-2026-10-26/character-scene.png and character-closeup.png; cutout supporting only |
| Source crop | Close-up (380,64)-(860,512), zero-based half-open edges; 480x448 source pixels |
| Native grid | 120x112, fixed 4:1 mapping; no full-character scale claim |
| Sampling/palette | Existing BOX route, source-foreground 48-color policy, no dithering; freeze actual palette values/order before trials |
| Coverage and ownership | Existing reviewed source polygons/feature islands and resulting masks, copied with provenance; nine visible semantic parts |
| Native start | Fresh reproduction of B00 separated seed, without later hard-coded hair/lid/mouth refinement passes |
| Display review | 1x and 4x nearest-neighbor; optional 2x labeled diagnostic display, not gameplay proof |

Record original model-authored/agent-reviewed crop and mask choices as inherited setup. A script-only replay means **no additional model inference to compute the seed**; it does not mean the recipe had no earlier judgment cost.

Before launching either model, inspect the actual B00/native exports against the originals and freeze two task cards. Each card names a visible defect, a permitted region/layer set, a requested improvement and concrete acceptance criteria. The following are task classes, not invented findings that must be painted:

| Task | Selection rule | Required protection |
| --- | --- | --- |
| E: nonidentity edge cleanup | Pick one confirmed contamination/contour defect outside eyes, mouth, identity-bearing fringe and important hair silhouette. If none exists, use a separately labeled fixture derived from this seed or report the task absent. | All pixels/layers outside the frozen mask, face/expression, palette, canvas, frame metadata. Alpha may change inside the mask only as the stated edge repair requires; reviewed solid coverage must remain. |
| F: identity-sensitive correction | Pick one confirmed loss of lid/gaze or expression from original to seed. Do not demand a gratuitous redraw of an already convincing smile. | Non-target layers/pixels and metadata; explicitly declare whether alpha may change. Use a distinct feature mask. No new palette/grid/pose or broad head redesign. |

Freeze task definitions before seeing model results. If initial independent review finds no defect, record no-change-needed or choose a new task version before trials. Later rubric/scope edits invalidate comparison with earlier versions.

### Checkpoint 1: deterministic preparation and native assembly

Use the existing kit's inspection/seed functions and the existing head preparation logic through a thin new experiment entry point. Its recipe records source/mask hashes, crop/grid, transform and rounding, alpha/palette policy, region ownership/order, protected areas, actual tool versions and output identities. Preserve the old scripts; parameterize a new copy/adapter rather than pretending they already accept arbitrary recipes.

Produce two independent new output directories. Save the source crop, unmasked conversion, masked seed, semantic part images/masks, optional outline suggestions, aligned tracing guide and processing manifest. Compare decoded RGBA pixels, masks, palette values and invariant manifest fields; timestamps/run paths may differ. When claiming exact reproduction of B00, compare against its recorded pixels as well. A mismatch must be explained or fixed before model runs.

Assemble those visible parts into native Aseprite layers using the actually available authorized backend. Preserve an original outside the artwork as guidance; any in-document guide must be immutable and explicitly excluded from export. Use native reference-layer import only if the current adapter proves it. No generic Lua capability or UI workaround is assumed from historical CLI evidence.

Required focused proof:

- Input hashes unchanged; outputs refused when the destination exists.
- Correct crop/grid/aspect/registration and recorded palette/alpha policy.
- Every seed foreground sample has declared ownership; no accidental foreground loss or duplicate composite coverage.
- Layer composite matches the frozen seed; inspect semantic ownership visually. Correct alpha alone would not have caught the historical neck pixel assigned to denim.
- Fresh native save/reopen/export matches; guide pixels do not enter output.
- One useful duplicate-only part edit preserves other native layers and protected metadata, using the applicable existing checker.

If native assembly is blocked, report the precise adapter gap and retain the validated seed/masks. Do not count a PNG or a merely flattened .aseprite import as completion.

### Checkpoint 2: four matched pilot runs

Select one available cheaper and one available stronger vision/tool-capable model only after actual model/capability discovery. Record exact model, reasoning configuration, host/system instructions, image delivery, backend/editor versions and tool schema. Use separate clean copies of the same native seed for every run.

| Pilot | Start | Task |
| --- | --- | --- |
| E-small | Frozen B00 copy | Exact E task card |
| E-strong | Identical B00 copy | Same E task card |
| F-small | Separate frozen B00 copy | Exact F task card |
| F-strong | Identical B00 copy | Same F task card |

Retain unchanged B00 as the **no-additional-revision control**. Known coordinate/color patches should be executed by scripts instead of being credited as AI reasoning. The small-model task must contain a genuine bounded judgment if it is to measure judgment.

Proposed ceiling: two visual revision passes and 80 total tool calls per pilot, declared before launch. This reuses the director benchmark's call ceiling but is an adjustable experimental budget, not a quality requirement. Equal ceilings are not equal compute or labor. Count failed calls/retries, batch operation sizes, active work, elapsed time, available usage, reviewer effort and rescue work separately. If a selected tier/vision/tool path is unavailable, mark that cell not run.

Use identical original/seed/reference information and task-specific masks per matched pair. Do not supply private extra hints or a stronger critic to only one contestant. Freeze/scoring-only review happens after each run; any experimental feedback must be standardized and equally available. Preserve every attempt, including technical failures and worse visual outputs.

If different clients/tool adapters are unavoidable, report a model-plus-host-plus-toolchain comparison, not a pure model comparison. Do not build a multi-provider harness merely for this pilot.

### Checkpoint 3: evaluate and route

First run the hard checks: allowed changes, protected native layers/metadata, palette policy, alpha coverage appropriate to the task, nonblank export and fresh reopen. For genuine edge repairs do not accidentally require unchanged alpha inside the allowed mask. Keep this technical result separate from visual evaluation.

Then shuffle anonymized actual exports. Review original, unchanged seed and candidate at fixed sizes. Record these independently with concrete reasons:

1. Was the named defect resolved?
2. Were identity, intended expression and style preserved?
3. Were new contour, cluster, alpha or other artifacts introduced?

A failed identity/protection criterion cannot be averaged away by a clean file or lower cost. A strong model critic is advisory; user approval of a final asset remains separate. Include reviewer/rescue effort in any production-cost comparison. Unknown usage remains unknown. Separate inherited one-time crop/mask setup from per-run preparation and cleanup effort; report when reuse would be needed to amortize setup rather than inventing savings.

Use the four-run pilot to validate tasks and tools. If unchanged, a follow-up can use **three fresh independent runs per model/task cell: twelve additional runs, sixteen total including the pilot**. That is a proposed follow-up, conditional on available authorized usage; it is not launched by this record. Preserve all runs and report failures/ranges, not just best-of-N. These are small operational samples, not statistical proof of universal equivalence.

Promote a cheaper model only for the task class that meets the same visual and technical conditions at lower observed total effort. If neither model improves a good seed, preserve it. If the cheap model fails, narrow its role to mechanical orchestration or escalate the documented visual task. A failed branch must not overwrite a good source.

This design tests **tier adequacy given the same seed**. It does not causally measure how much tracing reduced dependence relative to free redraw. A later method-by-tier comparison would need matched source/grid/task conditions and fresh runs; earlier redraws are historical evidence, not its control arm.

## Artifacts

Planned run root: docs/experiments/2026-10-27-automation-routing/. The record is a sibling Markdown file; all paths below that run root are planned and do not yet exist unless explicitly recorded later:

- recipe.json, task-e.json, task-f.json and frozen-inputs.json.
- replay-01/ and replay-02/: source crop, raw seed, masks, region images, underlay and preparation/native checks.
- runs/e-small/, runs/e-strong/, runs/f-small/, runs/f-strong/: native candidates, exports, operations, per-pass original/seed/candidate comparisons and checks.
- review/: randomized review mapping, observations, technical outcomes and complete effort accounting.

Do not reuse or mutate art-runs' historical v03 profile for this 120x112 crop. Reuse checker implementations with a correct new task profile. Do not rerun a historical successful report and present it as new evidence.

## Observations

| Check | Method and target | Observed result | Evidence |
| --- | --- | --- | --- |
| Existing evidence/source audit | Current repository/package text and constructor inspection; existing original/comparison images | Completed for workflow proposal | ../research/source-guided-automation.md |
| Deterministic replay | Two new preparation outputs; comparison with B00 | Not run | None |
| Native structure and guide exclusion | New seed native and fresh export | Not run | None |
| Scoped edit/protection | Duplicate-only useful edit | Not run | None |
| Cheaper/stronger model pilots | Four independent matched runs | Not run | None |
| Visual defect/identity review | Anonymized original/control/candidate comparisons | Not run | None |
| Cost and intervention comparison | Actual setup, inference, review/rework telemetry | Not measured | None |
| Contact/timing/Godot | Outside this static study | Not run here | Existing idle evidence does not validate this future experiment |

## User feedback

The current request favors constrained, automatable preparation and AI-owned revisions while retaining approved identity/style. No acceptance of a new candidate, model tier, production grid or budget-consuming benchmark run is inferred. The user is not required to paint sprites.

## Decision and continuation

- Continue with the deterministic replay/native-seed checkpoint before model trials.
- Last proven art state remains the existing assisted-head and later standing/shop records, with their stated limits. This record contains no new art proof.
- Benchmark usage consumed: zero trials and zero image generations in this research session. Proposed limits are stated above; no actual model cost was measured.
- Next owner: implementation agent, using exact available authorized model/tool assignments. First action is source/hash/task freeze and one deterministic preparation/native replay.
- If a required capability or budget is unavailable, complete independent preparation, preserve evidence and state the exact missing boundary. Do not silently substitute tools/models or broaden access.
- No commit, push, publication or replacement of existing assets is authorized by this experiment plan.
