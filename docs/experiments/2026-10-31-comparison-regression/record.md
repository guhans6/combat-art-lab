# Experiment: comparison regression checkpoint

- Status: implemented and locally verified; artistic defect detection remains fallible.
- Date:31October2026.
- Question: How should before/after review catch damage caused while fixing another feature?
- Intent: reusable workflow/tool correction; no sprite repair or new art selection.
- Baseline: task-start dirty snapshots/hashes of4351files under baseline/; prior
  tote v03 recovery is user-rejected, not an approved appearance baseline.
- Scope/acceptance: [user request and agreed test boundaries](request.md).
- Tools: two distinct explicitly requested gpt-6.1-sol/high agents for research
  then plan; parent implementation; independent global_worker Standards/Spec reviews
  and a separate visual probe. Python3.12.14/Pillow12.3 from existing bundled runtime.
  No installation, generator, native editor, Code-MCP, CUA, Godot, commit or publication.

## Diagnosis and plan

The prior comparison was generated and inspected; it still failed as a review gate.
Fixing forearms/grip/handle position did not establish convincing hand/strap
occlusion, and parent mistakenly cleared the result. Existing technical checks
proved native/export/playback consistency only. The old256×192/320×192 panels also
had no recorded shared-coordinate registration. Another ordinary comparison sheet
or a stronger “check carefully” instruction would not resolve the demonstrated gap.

[Sol High research](research.md) inspects six primary sources and existing helpers;
[a different Sol High plan](plan.md) chooses a small reusable wrapper over existing
canonical pixel/mask checks. The planner verified a genuine same-grid320×192 F9
pre-repair source-part composite. It is diagnostic pre-repair material, not user
approved art. Native action file and every original image remain unchanged.

## Changes

The source director now provides
[comparison_review.py](../../../tools/pixel-art-director/scripts/comparison_review.py)
and one authoritative [comparison procedure](../../../tools/pixel-art-director/references/comparison-review.md).
It records exact spec/source/evidence/sheet hashes and reports both edits outside
allowed scope and changed pixels omitted from named close crops. The full overview
is not silently counted as close review. Inputs must share dimensions and a declared
registration basis; there is no automatic fitting. Required frame inventory is checked
against the supplied batch, not inferred from the native timeline. Hidden-owner/native
protection and actual export correspondence still require the existing native audit.

Build outputs mechanical results while leaving visual acceptance/user approval
pending. Verify checks freshness only; it does not turn a mechanically failed packet
into a pass, interpret review prose, judge grip or grant approval. Manual review must
name the packet hash and separate requested improvement from newly introduced
regressions in edited regions, their connections, full context and affected neighbors.
Important coordinate claims need actual native crop/pixel readback. A disputed
structural relationship prevents selecting an improved candidate. Independent
critics receive images/task/locks without prior praise; edits by a critic need fresh
inspection. These are aids, not guaranteed semantic detection.

Existing SKILL/animation/project-workflow/template pointers reach that procedure.
The old head-specific preview label is now part-neutral. Handoff/motion status
preserve the user's tote rejection. No palette/grid/rendering rules changed.

## Observed evidence

| Check | Actual result | Evidence |
| --- | --- | --- |
| Agreed TDD seams | Public build/verify tests for scope/coverage and freshness began red before implementation. A fixture path-normalization mismatch and fixture palette error were corrected; failed runs retained. | tdd-01-*, tdd-02-*, tests*.log |
| Director regression suite |35baseline tests; final42/42 including7new public-boundary tests. CLI exercises incomplete build exit1, fresh-but-incomplete verify exit0 with mechanical false, invalid spec exit2. | baseline-tests.log, tests-final.log |
| Portable source copy | All42tests pass from standalone copied skill directory. This is not another-host installation or refreshed ZIP. | standalone-tests.log |
| Skill metadata | Official validator could not run because existing Python environments lack PyYAML; Ruby YAML frontmatter parse passes. No dependency installed. | skill-validation.log, frontmatter-check.log |
| Actual F9 difference |2680canonical changed pixels. Narrow diagnostic mask/crop misses30, including curl-tip and bag-bottom pixels. | replay-results.json; replay/target-only/packet.json |
| Complete diagnostic coverage | Mechanical pass, visual/user approval still pending. Known user grip rejection retained manually, not auto-discovered by pixel checks. Masks/palette exception are retrospective diagnostic scope, not prior permission. | replay/complete/packet.json |
| Historical mismatch | Exact mode refuses256×192→320×192; no invented registered diff. | replay-results.json |
| Native/export correspondence | Fresh read-only decoding of real v03F9 equals candidate PNG; native unchanged. | replay/native-readback.json |
| Optimized replay | Mandatory evidence checks use explicit exceptions after standards finding; full real replay passes under Python -O in a new directory. | replay-verified/results.json, replay-optimized.log |
| Fresh critic | Initially falsely cleared the known grip and cited incorrect coordinates. Readback withdrew those claims; critic retained a broad pass but marked essential hand/strap ownership uncertain, which prevents clearance under the procedure. No detection-success claim. | [visual probe](visual-probe.md) |
| Independent code/instruction review | Standards1actionable resolved; Spec0; final actionable0/0. Includes instruction scenario review. | [two-axis review](review.md) |
| Preservation/discovery | Exact baseline audit and local canonical symlink/readable new helper; all native/art bytes unchanged. Folder metadata drift recorded separately. | verification.json, artifact-manifest.json |

## What automation does and does not establish

Exact diffs reliably expose changed pixels. Mask checks detect unauthorized locations;
crop coverage prevents silently omitting remote changes. Source freshness catches
stale inputs or sheets; required-frame checks catch omissions from the declared batch.
These are testable deterministic checks. A covered, in-scope edit can still be ugly,
anatomically wrong or visually disconnected. The real complete packet demonstrates
that false-negative boundary. The fresh critic's initial false clearance also shows
that another AI review alone cannot be called a dependable grip detector. No quality
score, success percentage or general prevention claim is made.

Parent inspected the actual new native-size/4× same-coordinate packet. The grip is
still visually ambiguous, and the user's rejection remains authoritative. This task
improves comparison preparation, accountable review and honest disposition; it does
not repair or approve tote v03. No actual-speed/engine art validation was performed.

## Delivery and next owner

Changed existing files: director SKILL.md, references/animation.md,
scripts/pixel_checks.py; docs/workflow/art-production.md,
docs/experiments/experiment-template.md, docs/art/motion-guide.md, docs/handoff.md.
New reusable files: comparison_review.py, comparison-review.md and
tests/test_comparison_review.py; remaining new files are this experiment's research,
plan, frozen evidence, replay and verification. Exact hashes/delta in verification.json
and artifact-manifest.json. Git revision remains9e35c5c13987a153e942e6f93f49f247fad13c3a.

Local .agents/skills/pixel-art-director symlink resolves to the updated canonical
source. Historical portable archives remain unchanged; new archive publication,
another-host installation and broad production rollout are unperformed.

User artistic approval: none. Next art work remains a separately scoped recovery
repair, starting with one convincing hand/strap key and this revised regression
checkpoint before rebuilding the cycle. Workflow improvement is implemented; an
automatic semantic quality judge has not been established.
