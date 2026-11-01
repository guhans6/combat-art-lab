# Continue in Codex

## Read first

Read root AGENTS.md and CONTEXT.md, then the research and workflow documents they reference.

## User's intended outcome

Use AI to explore images until a personal visual style emerges, formalize that style and its motion rules, then have AI construct and revise actual sprite/animation sources. The user directs and learns; manual PNG repainting is not their required role. Godot is the intended engine.

## Completed preparation

- The delivered archive contains a complete local Git repository on main, including the initial commit and all 19 intended project files.
- Prior research consolidated with primary-source links and evidence boundaries.
- Project instructions, context, glossary, and decision record prepared.
- Style, motion, reference, asset, and experiment documents prepared.
- Matt Pocock project configuration and the exact shared checkpoint protocol prepared.

Consult [setup status](agents/setup.md) for publication and host-enablement boundaries. On 25 October 2026, the archive's 19 tracked files and initial commit `1a07783b2d4dea42383db5d30e553647f6932343` were imported into `/Users/guhan/Guhan/Projects/combat-art-lab`. The existing local documents matched the archive apart from older setup/handoff records and a trailing newline; those versions were backed up outside the repository before reconciliation. Local `.code-mcp` operation records were preserved and excluded from publication.

The private GitHub repository [guhans6/combat-art-lab](https://github.com/guhans6/combat-art-lab) now exists. The initial `main` commit was pushed, GitHub Issues is enabled, and all five canonical triage labels were verified. The setup-status follow-up is recorded in Git history. No art tools ran during publication.

## Next substantive action

The user rejected the raster-background placement as a style mismatch and requested actual Aseprite drawing. [Drawn scene preview](../assets/previews/street-drawn-v01/street-scene-4x.png) and [native source](../assets/source/street-drawn-v01/street-scene.aseprite) now supersede the plate preview for continuing art work. Request concrete visual feedback on the drawn background; do not switch back to a flattened image import as the production method.

Read the [drawn-background record](experiments/2026-10-26-drawn-background/record.md) and [style guide](art/style-guide.md). The native background has 16 meaningful layers; the combined scene has 29. Actual pixel geometry and plant-branch instructions construct the environment; no reference/generated background is imported. Exact PNG rebuild passed in a fresh folder with only v04 native character input. Lamp edit changed 205 light pixels while preserving the other 15 environment layers. Exact v04 cel images/positions and original files are preserved.

This is a simplified native redraw, pending user style approval. Native canvas remains 352x264; character offset is (84,61). No computer use, new MCP, new installation or image generation was used for the drawn background. User acceptance, motion, Godot playback and publication remain separate. All art work remains local/uncommitted.

## First recommended experiment

An AI-constructed native character master, one representative attack, a minimal Godot playback scene, and one visual plus one timing revision. Design it using docs/workflow/art-production.md and record it with docs/experiments/experiment-template.md.

The result must be reviewable at game scale and retain a practical revision source. Expand only after evidence supports the method and the user accepts its look and effort.

## Publication state

The verified remote is `https://github.com/guhans6/combat-art-lab.git`; the intended branch is `main`. Publication used the authenticated local GitHub CLI in the user's authorized Codex environment. No Code-MCP trust or guest-authority settings were changed. Verify the current remote and branch before future publication.

## Remaining boundaries

The reference-study work and standing reconstruction remain uncommitted and unpublished; the published repository remains at the prior setup milestone until publication is authorized. Aseprite is installed and CLI/Lua drawing was exercised. Final user acceptance of standing v04, weapon/attack choice, animation, actual Godot playback and paid-service use remain unperformed.
