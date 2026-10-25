# Project context

Updated: 25 October 2026.

## Goal

Develop a repeatable, AI-assisted way to turn the user's imagined visual style into an original character, usable sprite assets, and convincing combat animation for a 2D Godot game.

The user is new to game development, cannot currently draw, and wants to direct and monitor AI while learning relevant fundamentals.

## Settled direction

- Godot is the intended game engine.
- Visual style and combat animation should be investigated early together.
- Start with generated concept images and iterate until the user selects the desired direction.
- Translate approved examples into explicit visual and motion rules.
- Have AI construct and revise the actual native asset sources through suitable tools, code, layers, frames, or rigs.
- Preserve an AI-friendly revision process; the intended workflow does not depend on the user repainting PNGs.
- Capture research and rules in this repository so work can continue in Codex.

[ADR 0001](docs/adr/0001-ai-directed-art-workflow.md) records this direction.

## Proposed first proof

One character, one representative attack, a minimal Godot scene, and one successful art revision plus one timing revision. This is the recommended next experiment, not a completed result or fixed production scope.

## Open choices

| Choice | Current state |
| --- | --- |
| Visual references and target style | Awaiting user references |
| Pixel art versus illustrated/other 2D rendering | Open |
| Camera and facing directions | Open |
| Character design, weapon, and attack | Open |
| Native resolution and on-screen scale | Open |
| Palette, outlines, shading, and texture | Open |
| Frame-by-frame, cutout/rig, or 3D-to-sprite method | Open |
| Aseprite, MCP bridge, generator, and paid-service budget | Candidates only |
| Final game scope and asset volume | Deferred until the first proof |

Aseprite is a candidate because it exposes drawing and animation operations. Its availability does not decide the art style. PixelLab, editable pixel grids, cutout rigs, and rendered 3D remain researched options.

## Evidence today

Research inspected official documentation, public implementations, creator reports, a research paper, and a published simple attack. No new art generation, installed Aseprite integration, or Godot playback was performed for this repository setup.

The existence of an API or a successful external demo establishes a possible method. The user's references must be tested before claiming the intended style is achievable with acceptable revision effort.

## Scope of this setup

Create the repository, preserve research, configure the requested engineering workflow, and leave a concrete handoff. Do not silently start full game development or select the user's style during setup.
