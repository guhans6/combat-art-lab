# Agent instructions

## Start each task

Read [CONTEXT.md](CONTEXT.md), [GLOSSARY.md](GLOSSARY.md), and [docs/handoff.md](docs/handoff.md). Read relevant decisions in [docs/adr/0001-ai-directed-art-workflow.md](docs/adr/0001-ai-directed-art-workflow.md) before changing the workflow. Inspect the current Git state and preserve unrelated work.

This is an art-pipeline research workspace for a stylish 2D combat game in Godot. Existing repositories are separate; work only in the repository selected for the current task.

## User intent

The user is a beginner and directs the art while learning. The intended path is AI-generated concept exploration, explicit style and motion rules, then AI construction and revision of actual native sprite or animation assets.

Agents own drawing operations, scripts, asset corrections, exports, and engine integration. User participation centers on reference selection, feedback, and visual approval. Manual repainting of imported PNGs is not the required workflow.

Keep approved decisions, provisional proposals, and unresolved questions distinct. Pixel art, perspective, resolution, palette, and tool choices remain open until supported by references and a small experiment.

## Art and motion work

Before generating or constructing assets, read [docs/workflow/art-production.md](docs/workflow/art-production.md), the [style guide](docs/art/style-guide.md), [motion guide](docs/art/motion-guide.md), and [asset contract](docs/art/asset-contract.md).

- Preserve an approved candidate and its defining rules before developing dependent assets. Keep variants separate.
- Evaluate the actual gameplay-sized asset and its motion. Concept approval alone does not approve a sprite or animation.
- Preserve native source structure and reproducible drawing or rig inputs. Demonstrate a local revision; file extension alone does not prove editability.
- Establish attack poses, contact, and timing before expanding the moveset. Apply the workflow's proof criteria to the current scope.
- Run an actual Godot preview when claiming gameplay validation. Record the artifact, engine version, target, and observed behavior.
- Use focused automated checks for file properties and visual review for style, poses, consistency, and motion. Report each evidence boundary accurately.

## Research and learning

For tool, API, license, or current capability claims, inspect primary documentation or source and record the source and date. Start with [docs/research/ai-combat-art.md](docs/research/ai-combat-art.md); recheck facts when making an implementation choice. Distinguish published examples from tests performed here.

Explain only the concepts needed for the current decision, using the user's asset as the example. Continue routine implementation and corrections within agreed scope. Ask for a concrete art decision or consequential unresolved tradeoff with candidates or evidence available for review.

## Working records and tools

Keep experiments under docs/experiments using the [record template](docs/experiments/experiment-template.md). Update the handoff after a meaningful milestone or blocker; record the last proven result and smallest next step. Record reusable decisions in an ADR.

Prefer the smallest existing toolchain that can test the hypothesis. Install integrations only when needed for agreed work. Use already authorized services and budgets; new purchases, credentials, paid usage, public release, and broader machine authority require the appropriate user decision.

Use the installed research, grill-with-docs, teach, prototype, to-spec, to-tickets, implement, tdd, diagnosing-bugs, and code-review skills when their task matches. For Git publication, use publish-workflow when available and publish only to the verified destination within the user's authorization.

## Agent skills

### Issue tracker

GitHub Issues is the intended tracker. Read [docs/agents/issue-tracker.md](docs/agents/issue-tracker.md) before issue operations; its enablement status must be verified.

### Triage labels

Use the five canonical labels in [docs/agents/triage-labels.md](docs/agents/triage-labels.md).

### Domain docs

This is a single-context repository. Read [docs/agents/domain.md](docs/agents/domain.md) for glossary and ADR consumer rules.

### Validated checkpoints

For approved implementation with dependent increments or an uncertain integration boundary, read [docs/agents/validated-checkpoints.md](docs/agents/validated-checkpoints.md) and any established repository delivery reference before planning, advancing or reporting completion.

## Completion

Report what changed, the exact revision or artifact, observed checks, unresolved gaps, and the next owner/action. Keep construction, export, engine playback, user visual approval, and publication as distinct claims. This setup does not establish an additional repository-wide Definition of Done.
