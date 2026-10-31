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
