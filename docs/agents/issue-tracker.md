# Issue tracker: GitHub

GitHub Issues is the intended tracker for this repository.

- Intended owner/repository: guhans6/combat-art-lab.
- Enablement status: private repository and GitHub Issues verified on 25 October 2026; see [setup status](setup.md).
- Before any tracker write, verify the repository identity and actual remote. Do not redirect issues to another project.

Use the authenticated GitHub connector, bounded Code-MCP issue actions, or the gh CLI when available and authorized. For multiline issue bodies, use a structured body argument or a text file with --body-file.

## Operations

Read the relevant issue, comments, and labels before work. Create an issue only when issue publication is requested or part of the approved workflow. Use the label mapping in [triage-labels.md](triage-labels.md). Reference verified issue numbers in commits; use closing keywords only when closure is intended.

When a skill says publish to the issue tracker, create a GitHub issue in the verified repository. When it says fetch the relevant ticket, read that issue and its discussion.

## Pull requests as a triage surface

**PRs as a request surface: no.**

## Wayfinding

Use a map issue and linked child tickets if a large plan needs wayfinding. Prefer GitHub's native sub-issues and blocking dependencies when available. If unavailable, explicitly use a parent task list and Blocked by references; report the fallback. Claim only authorized work, and update the map with evidence when resolving a child.

## Publication evidence

The repository and issue tracker are enabled. No issues were created during publication. Continue to verify repository identity before tracker writes and distinguish local proposals from published issues.
