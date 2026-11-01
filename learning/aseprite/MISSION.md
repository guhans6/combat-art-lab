# Mission: Make small, confident Aseprite corrections

## Why
I want to turn AI-generated character art into sprites for my Godot combat game and understand enough Aseprite to correct the AI's mistakes myself. I want to try resizing, drawing over a base, and tracing a reference while agents can continue the larger art work.

## Success looks like
- Open a practice copy, identify the drawing layer, and save a separate native master.
- Make one small correction using existing colors, undo it, and compare it at 100% zoom.
- Resize a concept to a declared practice grid while explaining what resizing cannot decide.
- Trace on a separate layer and distinguish a guide from visible final artwork.
- Export a transparent PNG with the intended layers and know the next Godot import step.

## Constraints
- Beginner; use this project's existing female character as the example.
- Short, concrete lessons with visible feedback and official references.
- Preserve active art work and original references. No purchases or new art generation needed.
- 128×192 is a historical practice grid, not an approved final game resolution.

## Out of scope
- Mastering anatomy, building a full animation, and replacing production assets in this first course.
- Making manual drawing a requirement for the project's AI-assisted production workflow.


---

## Preserved learning-branch document (484d4d0)

The following original local document is retained verbatim for historical context. Guidance above reflects the incoming course updates; statements about missing assets below describe the earlier checkout.

# Mission — Aseprite, for the Combat Art Lab director

## Why learn

I want to understand enough Aseprite to inspect an AI-authored pixel sprite, compare it with the approved character reference, and optionally fix small mistakes myself while building a combat-focused 2D Godot game. I do not want to become the required pixel artist. AI/agents continue to own asset production, revisions, and engineering verification.

## Initial starting point

Beginner in sprite editing. Recent practice focus: consistent character proportions and the six poses of a tote-bag swing attack. A higher-resolution character reference and AI-generated pixel-base pose may be available from the ongoing agent workflow; the actual files are not present in this lesson branch.

## Measurable first success

Using an AI-base PNG and reference image, I can:
1. Make a copy of the sprite into a native Aseprite document without overwriting the source.
2. Add a high-resolution reference layer and a safe editable working layer.
3. Correct one visible silhouette/pixel defect deliberately.
4. Save the layered \`.aseprite\`, export transparent PNG, and inspect at 100% / gameplay-like displayed scale.
5. Explain why pixel resampling cannot automatically guarantee good pixel art.

## Next success

Import or arrange six aligned attack poses in a timeline, assess anchor consistency and silhouette readability, and export a provisional sprite sheet for agent review.

## Boundaries

- Production resolution, palette, style and exact animation timing are not approved by this lesson.
- Manual exercise assets are optional learning outputs; the normal art pipeline may remain AI-authored.
- Work on a separate branch/checkout; do not change the ongoing agent's workspace.
- A clean PNG export is not evidence of animation quality or Godot playback.

Date started: 2026-10-31.
