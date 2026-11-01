# Integrate image-to-sprite review guardrails

- Status: planned; implementation and verification remain to be performed.
- Date: 29 October 2026.
- Scope: improve the existing agent-agnostic art workflow after the Luna pilot. No artwork, native master, trial export, engine scene, global configuration, purchase, installation or publication changes.
- Completion criterion: the maintained workflow, discoverable director skill and experiment record agree on seed review, preservation, per-pass decisions and candidate selection; focused checks exercise both rejection and legitimate exceptions. This means ready for another bounded test run, not proven art quality.
- Delivery authority: current user request and `docs/agents/validated-checkpoints.md`; that document records no separate repository delivery reference or additional Definition of Done. The user has already authorized planning and integration; routine implementation needs no new approval gate.

## Evidence and failure boundary

Read the trial [brief](../2026-10-29-luna-independent-trials/BRIEF.md), [results](../2026-10-29-luna-independent-trials/RESULTS.md), [postmortem](../2026-10-29-luna-independent-trials/postmortem.md), A's recipe/pass-02 plan/record, and B's preparation/pass-02/pass-03 records. The approved scene/close-up remain identity authority. The generated production cutout has a different role. No new visual judgment or artwork manipulation is needed to integrate these already recorded findings.

- The user prefers A's sharper hair and open-eye treatment, and rejects B's final eye treatment. This is a visual preference with remaining defects, not approval of a production replacement.
- A used nearest-neighbor reduction and a large source-derived palette; B used BOX plus a much smaller quantized palette. The records report 253 versus 35 visible final colors. Hair differences predate face-only later edits. These are recipe confounds, not evidence for a generally superior model or a universally correct filter/color count.
- A's correction principally removed its own bright eye additions and retained underlying source clusters. B's last pass replaced eye/mouth regions; angular/closed eyes remained an observed defect. Native ownership and reopen successes do not compensate for that expression failure.
- Existing workflow and director instructions already require direct original/export review, separate evidence dimensions, preservation and rollback. They need stronger completion conditions and an explicit selection record, rather than another parallel workflow.

The prior [source-guided automation research](../../research/source-guided-automation.md) already separates selecting a recipe from executing it, and supports retaining a good source-derived region unless an observed defect justifies a change. Reuse that distinction. Its historical BOX replay baseline is not a universal production recipe. ADR 0001 continues to permit multiple tools and representations; no ADR amendment or architecture rewrite is needed.

## Minimal maintained changes

Edit these six files. Preserve all pre-existing dirty work and historical experiment artifacts. Prefer replacing or tightening existing prose over appending duplicate instructions.

| File | Exact change area and responsibility |
| --- | --- |
| `docs/workflow/art-production.md` | Central source of truth. Add one compact, anchored section beside **Automation and model routing** for experiment intent and seed review. Tighten **6. Inspect appearance and revise structure first**, **Visual review rubric**, and **Evidence and traceability** to implement per-pass identity veto, explicit best-candidate selection and honest labels. Link the postmortem as local evidence. |
| `tools/pixel-art-director/SKILL.md` | In **1. Establish the task**, **3. Freeze inputs and observations**, and steps **4–6**, add concise operational completion conditions and a conditional pointer to the central project gates. Preserve standalone usefulness, all four modes and existing backend/native protections. Fix only any touched pointer whose resolved target is wrong. |
| `tools/pixel-art-director/references/benchmark.md` | Before **Frozen first task**, require declaration of comparison intent. Add same-seed control for a model comparison and explicit recipe/source variables for other comparison types; keep the v03 task as a named historical correction profile. Update per-pass/scorecard/deliverable interpretation so ordinal axes cannot average away identity/expression failure and the last pass is not implicitly selected. |
| `tools/pixel-art-director/references/assisted-reconstruction.md` | Tighten steps 1, 3 and 4: review the recipe/seed before dependent construction, state its use decision and scoped repair if any, then follow the central review/selection gate. Keep trace-guided, conversion-plus-cleanup, hybrids, supplementary references and intentional reconstruction available. Avoid copying the complete central contract. |
| `docs/experiments/experiment-template.md` | Add compact optional-for-relevance intake fields and a pass/selection ledger described below. This is the existing record format, not a new parallel schema or mandatory migration of old records. |
| `docs/handoff.md` | Add one current dated entry linking this plan, changed workflow and actual verification record. Report exact local artifact/revision, evidence, remaining run/approval boundaries and next owner. Do not rewrite previous trial results. |

No change is needed to the style guide, motion guide, asset contract, `AGENTS.md`, ADR, frozen v03 profile, native checkers, drawing scripts, historical research or archived kit inputs. The asset contract already routes review to the central rubric and requires provenance. The reconstruction and face-likeness references already support direct review and observed-defect diagnosis; change them only if implementation exposes a concrete conflicting instruction, and document that small delta.

### Project-local skill ownership and packaging

`tools/pixel-art-director` is the canonical installed project skill. `.agents/skills/pixel-art-director` is a symlink to `../../tools/pixel-art-director`; `ls -ld` and `diff -qr` confirmed this during planning. Edit the canonical files under `tools`, which are in the writable workspace. Preserve the discovery symlink and verify its real path after editing. There are not two editable mirrors to synchronize, and there is no reason to edit the protected `.agents` tree or global skills/configuration.

`tools/pixel-art-director.zip` is a retained package snapshot, not the live discovery target. Leave it unchanged and state that this task updates the installed project copy only. Do not claim the archive was refreshed or distributed. If a real independent mirror is discovered, stop treating it as a symlink: establish its owner/source, update only explicitly maintained copies and verify byte equality. Do not invent a second source of truth.

## Central gate behavior

### 1. Declare what the experiment can answer

Record one primary intent before preparation:

- **Production/reconstruction:** choose a method suitable for the named visual target; preserve recipe decisions and evidence, without pretending it is a model benchmark.
- **Model comparison:** freeze identical input references, derived seed pixels, crop/grid/transform, alpha and palette treatment, reviewed masks/ownership scaffold, baseline native state when applicable, tool/skill versions, task and budgets. Verify hashes and decoded seed equality across contestants before drawing. A deliberately imperfect common seed is valid when repairing that named defect is the task.
- **Method/recipe or source comparison:** declare which variables differ, hold the other practical conditions comparable, and preserve all arms. If several preparation variables differ, conclusions cover the combined recipe, not a causal claim about one filter. For source effects hold preparation equal; for model effects hold source/preparation equal. An exploratory end-to-end model-plus-recipe pilot is allowed when labelled accordingly, with its confounds stated.

An unspecified intent or mismatched supposedly shared seeds is a preparation defect. Correct it before dependent comparison work, or relabel the experiment and narrow its conclusions. Equal original inputs alone do not establish equal derived starting conditions. No model, filter, palette size or historical profile is the default winner.

### 2. Review and freeze the recipe/seed for its intended use

Before expensive native cleanup or a comparison rollout, record exact source authority/role/hash, crop, source/native dimensions and transform, alpha/resampling/palette/dither policies, mask provenance, dependency versions and seed hash. Reuse the experiment's existing recipe rather than introduce a compulsory new file format.

Inspect original, raw seed and actual seeded native export when available at true 1x and matched integer zoom, including the identity-rich crop and full-asset context. Record whether defining identity/expression, hair detail, proportions, silhouette and material relationships survive. A seed is a draft, so its use decision is one of:

- suitable for the next named task;
- suitable for a specifically scoped repair, with the deficient cue, expected result and repair boundary stated;
- needs re-preparation or a separately labelled reconstruction study before dependent work.

Seed review is an agent checkpoint, separate from user approval. A lost feature may be deliberately reconstructed when the task and scope support it. The gate prevents unexamined information loss from silently becoming an assumed-good baseline; it does not require perfect seeds or ban face reconstruction. Recipe changes after freeze create a new arm/checkpoint and invalidate any affected same-seed claim until equality is restored.

### 3. Protect defining features with scoped exceptions

Translate identity priorities into visible properties, not just “keep the face”: for this character, near/far eye relationship and gaze, intended lid openness/expression, shallow smile, fringe openings and tied-hair silhouette. Record the relevant properties for another asset rather than hardcode this example universally.

Preserve good source/best-candidate regions unless a direct comparison supports a named defect. Before changing an identity feature, record **observed defect → reference evidence/confidence → proposed bounded change → expected visible improvement**, plus unchanged features and allowed layers/region. A legitimate requested eye, mouth, expression or structural correction is a scoped exception. Retain a reversible candidate and compare it directly. Local corrections still obey their exact pixel/native locks; a needed change outside those locks requires a separate authorized variant, not a silently expanded mask. Fresh reconstruction uses its declared study scope rather than inheriting an unrelated historical face mask.

### 4. Review each actual candidate before advancing

Retain each native checkpoint, export, operations and technical results. Open the native file/structure and actual export. Save and inspect original/seed/best-prior/new-candidate comparisons at native 1x and identical integer zoom; use aligned head crops for facial work and full-asset context to catch proportion/pose effects. Existing pairwise `reference_review.py` sheets plus direct PNGs can supply these panels; a new montage framework is unnecessary.

Check sheet provenance against the exact export paths/hashes and inspect labels, clipping, scale, matte/alpha behavior and missing regions. A broken sheet is an evidence defect to repair before using it for selection. Retain failed evidence. For an identity edit, include a changed-region/face diff so preservation, rollback and replacement are observable. Existing scoped pixel checks or experiment diffs can supply it; a diff does not judge expression.

Record a visual decision and independent technical status before another art pass. **Identity/expression is a noncompensable gate:** a material failure or regression cannot be outweighed by cleaner parts, fewer colors, tool success, more edits, documentation or reopen equality. “Uncertain/not reviewed” is pending, not a pass. A bounded corrective branch may continue within scope/budget from a failed candidate, but it remains failed/pending and cannot become a selected result or the baseline for dependent production. Separate the defect-driven correction decision from selection.

### 5. Select the best candidate explicitly

After every review, name the best retained checkpoint, new candidate status, decision/reason and next working baseline. Promote only a reviewed candidate that satisfies the declared visual goal and required technical boundary; otherwise retain/restore the best eligible prior native source and its matching export. Preserve the rejected latest pass and all proof-only duplicates separately. If no candidate satisfies the gate, record **no selected result**; the best available failed study can still be shown with its limits.

Use labels such as raw seed, candidate awaiting review, rejected candidate, preferred/selected by agent for this scope, user-preferred direction, user-approved artifact, last attempted, and proof-only edit accurately. These are not all mandatory file names. The final report/display leads with the actual preferred/selected checkpoint and its reason; it names the last attempt separately when different. “Final” needs explicit scope and must not imply that the numerically last pass won. User approval always names the exact artifact and accepted scope. A visual preference with incomplete native proof remains a preference, not a completed native deliverable.

## Compact record additions

Extend the existing experiment template with fields rather than a new document family:

- Intent, controlled/changed variables and limits on attribution.
- Recipe/seed path and hash; seed review image and reviewer; use decision/scoped repair.
- Defining feature priorities and exact correction locks/scoped exceptions where applicable.
- Pass ledger columns: checkpoint/native/export identity; observed defect/change hypothesis; technical result; original/seed/best/new evidence and visual decision; selected baseline/reason. Reuse separate per-pass records when a row would become unwieldy.
- Selection summary: best/preferred artifact and reason; last attempted artifact/status; user preference/approval scope; remaining defects and next owner. Allow “none selected” and “not reviewed.”

Use existing budget fields to distinguish preparation/smoke, artistic edits, proof/reopen work, failed calls/retries and review/rescue where measured. Preserve unknown telemetry. Extra accounting must not become a proxy for art quality.

## Implementation sequence and focused verification

1. Snapshot current Git status and hashes of the six intended files; read their current text before editing. The tree contains substantial unrelated uncommitted work. Make targeted patches and preserve the established rules, backend restrictions and historical evidence.
2. Implement the central contract and record fields, then update the concise skill/branch pointers. Finish the handoff only after verification. Do not run art tools or modify artwork for this documentation integration.
3. Verify the local skill symlink resolves to the canonical directory, all touched relative links resolve, frontmatter remains valid and the diff contains only intended edits. Run `git diff --check`; inspect diffs explicitly because much of the skill directory is currently untracked.
4. Run `python3 -m unittest discover -s tools/pixel-art-director/tests -v` using the existing working Python/Pillow environment. Existing suites cover input freezing/protection, alpha coverage and review-image provenance/overwrite handling. They are regression checks for the reused tools, not proof that prose improves artistic judgment. Do not add dependencies or claim a successful test run from a historical record.
5. Run the skill creator's `quick_validate.py` against `tools/pixel-art-director` if its existing runtime supports it. A missing PyYAML dependency is recorded as unperformed, not silently installed. Use an already available YAML parser for frontmatter checking if available and label that narrower check accurately. Do not change invocation settings or global skills.
6. Have the parent's planned independent read-only reviewer apply the integrated instructions to the scenarios below. Save actual decisions/reasons in one `verification.md` beside this plan. Check the maintained texts for contradictions and excessive duplication. No second art trial or repeated broad code review is needed to verify this increment.

### Behavioral cases the reviewer must resolve

| Input situation | Required observable decision |
| --- | --- |
| Two model contestants inherit NN/large-palette and BOX/small-palette seeds while claiming a controlled model comparison. | Hold/reprepare for equal seeds, or explicitly relabel as end-to-end workflows and restrict attribution. Neither a filter nor a model is declared generally better. |
| A method study deliberately varies resampling/quantization; source, framing and effort are recorded. | Permit the study; attribute a multi-variable change to the combined recipe. Same-seed identity is not incorrectly imposed on method arms. |
| A technically passing latest candidate has squinted eyes while the best prior has the required expression. | Reject latest for selection, retain/restore the best eligible prior, show both exact artifacts with distinct labels. Technical gains cannot override the veto. |
| Every attempted candidate fails identity, or latest is unreviewed. | Report no selected result or pending review; never infer selection from the last pass number. |
| An authorized face correction has a reference-supported defect and a bounded eye/mouth exception. | Allow correction/reconstruction inside scope, preserve unrelated features, compare original/best/new and require actual review. No blanket face freeze. |
| A weak shared seed is intentionally used to test repair of its lost smile. | Permit the named repair task after seed review; apply the same seed/brief to contestants. A perfect seed is not required. |
| A convincing seed needs no artistic change, while native editability still needs proof. | Preserve it as the visual candidate/control, perform any required localized edit on a labelled duplicate, and keep that proof separate from selection. |
| Sheet labels/clipping/matte panels do not reliably represent the named PNGs. | Repair and inspect evidence before selection; do not infer a new art defect from a broken presentation or treat file equality as visual approval. |

No new validator is proposed for this increment. A schema checker could prove that a self-reported “pass” field exists while reproducing the exact visual-selection failure. The useful automated invariants already have tested helpers. Add a state-transition validator only if a later repeated failure shows missing records/invalid promotion is the problem; it must never compute likeness or replace the visual reviewer. Do not add tests that merely search for mandated words or headings.

## Acceptance and handoff

Integration is complete when all six maintained targets agree, the canonical skill is discoverable, touched links/frontmatter and focused regression checks have observed results, the independent scenarios exercise the intended decisions and legitimate exceptions, and the verification record identifies the exact local files/base revision and any unrun check. No unresolved consequential art choice is needed to implement these gates.

Report **workflow implemented and locally checked, ready for another bounded test run** only after those proofs. Leave actual effectiveness in a new image-to-sprite run, artistic quality, final sprite selection, user approval, motion, Godot playback, packaging and publication explicitly unperformed. Next owner is the parent orchestrator for implementation/review dispatch, then the next drawing agent for a separately scoped run using these gates. The user retains artistic selection; no manual repainting is assigned to them.
