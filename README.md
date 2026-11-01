# Combat Art Lab

A research and production workspace for discovering an original visual style and building AI-authored sprite assets and combat animation for a 2D Godot game.

## Start here

1. Read [AGENTS.md](AGENTS.md) for agent instructions.
2. Read [CONTEXT.md](CONTEXT.md) for the current goal, settled decisions, and open choices.
3. Read the [Codex handoff](docs/handoff.md) for the next action.
4. Consult the [research](docs/research/ai-combat-art.md) and [production workflow](docs/workflow/art-production.md) when choosing or testing the pipeline.

## Intended process

Explore concepts with AI, select a visual direction, record its rules, have AI construct meaningful native sprite sources, animate one representative attack, test it in Godot, and prove that the result can be revised.

The user directs and evaluates the work while learning relevant basics. Agents own asset construction, corrections, scripts, and technical verification.

## Current state

Ready for a new character on local branch `work/new-character-ready`. The art
pipeline and learning workspace are consolidated in this checkout. Start with
[the next-asset guide](docs/new-asset.md); place new references in `assets/incoming/`.
The previous character is [cataloged separately](assets/CHARACTER-ARCHIVE.md).

Reusable deterministic preparation is in `learning/aseprite/automation/`; the
[course](learning/aseprite/index.html) remains available. Existing native art and
Godot evidence are retained with their original scope. New-design validation and
artistic approval have not happened. Workflow and tool choices are unchanged.

## Working documents

| Document | Purpose |
| --- | --- |
| [Research](docs/research/ai-combat-art.md) | Primary sources, published examples, limitations, and optional methods |
| [Production workflow](docs/workflow/art-production.md) | Small milestones and evidence required before expanding |
| [Style guide](docs/art/style-guide.md) | Fill only after visual decisions are made |
| [Motion guide](docs/art/motion-guide.md) | Key poses, timing, contact, recovery, and effects |
| [Asset contract](docs/art/asset-contract.md) | Native masters, reproducible construction, exports, and review |
| [Reference log](docs/art/reference-log.md) | Reference provenance and selected visual qualities |
| [Experiment record](docs/experiments/experiment-template.md) | Hypothesis, artifacts, observations, decisions, and next step |
| [Glossary](GLOSSARY.md) | Shared terminology |
| [Decision record](docs/adr/0001-ai-directed-art-workflow.md) | Accepted project direction and unresolved implementation choices |
| [Skill setup](docs/agents/setup.md) | Setup provenance and current enablement status |

## Engineering workflow

The Matt Pocock setup uses one domain context, GitHub Issues as the intended tracker, the five standard triage roles, and the checked-in validated-checkpoint protocol. Project configuration is in [docs/agents](docs/agents/setup.md). These documents configure installed skills; they do not install an art generator or guarantee that a new host has every skill loaded.

## Scope

The initial proof is one character, one representative attack, one target, enough background to judge readability, and a successful art and timing revision. A larger moveset, additional characters, or a complete game follows evidence and user direction.

External demos are linked as research. No third-party art is vendored as production content.
