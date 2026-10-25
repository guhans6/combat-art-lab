# Engineering-skill setup

Configured: 25 October 2026.

## Project configuration

- Instruction entry point: root AGENTS.md, explicitly requested by the user.
- Issue tracker: GitHub Issues, intended destination guhans6/combat-art-lab.
- Triage: the five default role names; triage was observed in the installed global registry.
- Domain layout: one GLOSSARY.md and docs/adr; CONTEXT.md carries project state.
- Checkpoints: [validated-checkpoints.md](validated-checkpoints.md), copied without body changes and linked once from AGENTS.md.
- No separate delivery-workflow setup or repository-wide Definition of Done was created.

The current request authorizes creating this repository, adding its research/rules, and running setup. Default configuration choices are used for this new empty project; no existing project instructions or local adaptations were replaced.

## Source provenance

The machine's installed setup-matt-pocock-skills body was read through Code-MCP. Its content exactly matched the source at:

- Repository: [guhans6/agent-workbench](https://github.com/guhans6/agent-workbench).
- Source revision: 46b2e9493d75c07ea357cf5ac24ec104afb55500.
- Skill path: shared/skills/setup-matt-pocock-skills/SKILL.md.
- Installed skill SHA-256: 3bb6e45fad2b1148f21c51a41d8a5e8a8299668a9a353b6bbd1f710ef4b59149.
- Protocol path: shared/workflows/validated-checkpoints.md.
- Protocol SHA-256: 40d2c19b90c6cfc28a6c1cb375398b84433810d8e067d4fb27428ba0cc4de969.

The GitHub tracker, triage, domain, and checkpoint-adoption seeds were read from that same revision. Project-specific wording preserves their conventions. The checkpoint body's exact bytes and provenance footer are retained.

## Skill availability

The global registry advertised the relevant setup, research, grill-with-docs, teach, prototype, to-spec, to-tickets, implement, tdd, diagnosing-bugs, code-review, and triage skills. This task configures their project references. It does not install duplicate global skill packages or prove that a future Codex session has loaded them.

Global guidance referenced publish-workflow, but Code-MCP's compact skill registry did not expose its body. The existing source was located and read at platforms/codex/skills/publish-workflow/SKILL.md in the same agent-workbench revision. No global routing or skill files were modified.

Use writing-for-agents for future instruction-file edits. Read the relevant installed skill when invoked; these project pointers do not replace skill bodies.

## Complete local deliverable

The delivered combat-art-lab.zip contains the complete combat-art-lab directory, including its Git metadata and initial commit on main. The commit records the 19 intended project files. No remote or credentials are configured in this repository.

This archive is the concrete local deliverable. It can be extracted and opened in Codex without relying on the unverified macOS write attempts below. The project configuration is portable; availability of the referenced global skills must still be checked in the session that uses it.

## Current external enablement

Verified on 25 October 2026 using local Git and the authenticated GitHub CLI:

- Local repository: `/Users/guhan/Guhan/Projects/combat-art-lab`, on `main`, preserving initial commit `1a07783b2d4dea42383db5d30e553647f6932343` and its 19 tracked project files from the supplied archive.
- GitHub repository: [guhans6/combat-art-lab](https://github.com/guhans6/combat-art-lab), verified private with GitHub Issues enabled.
- Remote: `origin`, `https://github.com/guhans6/combat-art-lab.git`; initial `main` commit pushed successfully with upstream tracking.
- Remote labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix` verified present. Only the four missing labels were created; existing labels were preserved.
- No issues existed when checked; this publication has no originating issue reference.
- Local `.code-mcp` operation records are preserved and ignored, outside the published project files.
- Earlier Code-MCP failures are historical. Publication used the user's authorized local Codex execution environment; no Code-MCP authority settings were changed.
- Aseprite integration, image service, and Godot playback remain unperformed by this setup.

The setup-status follow-up commit records the reconciliation and publication evidence. Publication does not establish art-pipeline validation or user visual approval. The next substantive action remains review of the user's style and motion references.

## Reconciliation checks

Before the publication-status commit, focused checks passed: all 19 tracked files were present, relative Markdown file links resolved, `git diff --check` and `git fsck --full` reported no errors, and a credential-pattern check found no matching tokens or private keys in tracked files. The checkpoint protocol body SHA-256 matched its recorded digest `40d2c19b90c6cfc28a6c1cb375398b84433810d8e067d4fb27428ba0cc4de969`. Separate standards and request-scope reviews found no remaining issue once this follow-up is committed. These checks cover repository integrity and publication records, not the accuracy of every external research claim.
