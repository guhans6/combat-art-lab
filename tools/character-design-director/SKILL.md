---
name: character-design-director
description: Interview the human director, research reference qualities, and iteratively develop an original character through controlled AI concept variants before handing an approved design to native asset production.
---

# Character-design director

## Purpose and boundary

Use this skill for a NEW character or a fundamental redesign, before image generation, pixel conversion, reconstruction, or animation production. The human directs concept, personality, visual taste, and approval; the agent discovers facts, prepares visual options, generates/organizes concepts with an authorized image tool, and tracks decisions. Do not require the human to draw or manually repair PNGs.

Read the repository's AGENTS.md, CONTEXT.md, docs/handoff.md, docs/new-asset.md, GLOSSARY.md, relevant ADRs and the art-production contract. Earlier approved character files, sizes, palettes, tools and outfit are historical examples, NOT defaults for this new character. A previous character must never become an identity anchor unless the human explicitly selects it.

This is the upstream counterpart to tools/pixel-art-director/SKILL.md. Do not rewrite or bypass its native/editability, likeness, motion, or Godot proof rules. Pixel-art-director begins only after a canonical character appearance and specific production task are approved. If the selected representation is not pixel art, route through the representation-neutral workflow instead.

## 1. Interview: extract decisions rather than invent them

Use the installed /grill-me (grilling) or /grill-with-docs workflow when available. Follow the [interview decision tree](references/interview.md). In rounds, ask all currently unblocked decision questions, each with an explicitly identified recommended YES answer; wait for the human's response before asking dependent questions. Research facts and examples yourself rather than asking the human to find them. User decisions are not delegated.

Record every answer as **human-stated**, **agent interpretation pending confirmation**, **open**, or **human-approved**. "No preference" and "show me alternatives" are valid answers; do not silently turn them into permanent style decisions. Distinguish a proposed direction from an accepted brief. Do not produce purported final character images or production frames until the human authorizes a defined exploration scope and comparison axes. No fixed number of questions is required.

Discuss: gameplay role and personality; desired contrasts; age/shape cues if relevant; character silhouette and body proportions; clothing, hair, props and combat identity; camera/facing, likely displayed height and animation needs; rendering approach (pixel, illustrated, cutout, other); color/emotional direction; influences and things to avoid; image-generation use; and reference approval. Ask downstream questions only after their dependencies are settled. Treat uncertain game scale and unknown camera as open, not guessed values.

## 2. Build an annotated reference board

Bring concrete examples from real games, developer art breakdowns, anatomy/pose sources and visual examples when available. Invite the human's own images and links. For every reference record: source URL/path, author/game, intended role (silhouette, anatomy, palette, lighting, expression, costume, pose, animation, rendering), useful property, prohibited copied elements, and human acceptance status.

Borrow principles, not recognizable characters, costumes, trademarks, or traced frames. Preserve provenance and license notes. Existing docs/research/character-design-foundations.md is the starting reference library, not a compulsory art style. Show alternatives visually when possible; a written game name alone is not a meaningful visual comparison.

## 3. Agree to a bounded concept experiment

Create a character-specific brief from docs/art/character-brief-template.md. The human confirms the brief's purpose and comparison variables before image generation.

Use deliberate passes, not random batches:
- **Silhouette / proportion pass:** 3–5 meaningfully different, described design directions; vary body/head proportion, shape language, recognizable masses, stance or outfit volume. Start with clean readable full-body shapes.
- **Rendering/style pass:** compare the same identity and pose in a few rendering approaches ONLY when style is still open. Keep silhouette/proportions stable within this pass.
- **Color pass:** preserve the selected geometry, material assignments and lighting; alter palettes deliberately rather than regenerating a new person.
- **Identity/pose pass:** after the human selects a canonical full-body reference, create only named missing views/expressions or 2–3 key poses to test animation feasibility. Do not mass-generate in-betweens by default.

**Fair comparison:** within a pass, use a shared camera/view, framing, orientation, full-body visible height, feet/ground alignment, background and image canvas as far as the image tool permits. Record requested dimensions and actual measured output; a prompt is not proof of matching scale. Equal *comparison size* does NOT select final native pixel resolution. Proportions can vary in the proportions pass but the figures must still be displayed at comparable overall height. Don't resize individual poses independently to hide proportion drift.

Generate and save each image separately, retaining original outputs and prompt/attachment manifests. Never mix several major variables in one comparison and claim the effect of a single variable. A generation tool may fail to respect dimensions, identity, transparency or pose constraints; inspect the returned pixels and report these failures.

## 4. Compare, revise, and lock only what the human selects

Show labeled contact sheets with the actual outputs at matched display size plus individual details. Ask the human what to keep, reject and change. Record: candidate ID, key differences, strengths, problems, what is approved, what remains open, and next variation. Preserve rejects and prior accepted versions. Limit each next round to 1–2 named changes where possible.

Progressive gates:
1. **Brief/exploration authorized:** user accepts the goal and controlled variant axes; no accepted appearance yet.
2. **Direction selected:** user names preferred visual qualities, proportions and rendering candidates.
3. **Canonical identity approved:** exact full-body image/ID, silhouette, anatomy, costume/material colors, face/hair cues and expression constraints recorded. Freeze as the identity anchor.
4. **Pose feasibility reviewed:** key poses preserve identity, connected body/prop structure, ground/anchors and intended motion; approval status recorded independently.
5. **Native production handoff:** approved original references and all declared unknowns go to the appropriate production route.

A concept image cannot prove sprite editability, real runtime readability or animation quality. A selection for the agent's next experiment is not user approval. Do not self-approve art.

## 5. Handoff to production, without rewriting the existing pipeline

Recommended per-character records (create these when a character is actually named):
- docs/characters/<slug>/brief.md — decisions and open questions.
- docs/characters/<slug>/references.md — source-role register and license notes.
- docs/characters/<slug>/decisions.md — round-by-round candidate comparisons and approvals.
- assets/concepts/<slug>/ — raw labeled generations and comparison sheets.
- assets/incoming/<slug>/ — the exact selected image inputs/pose guides, when approved.

Handoff includes canonical image paths and hashes, exact approved cues, exceptions/negative constraints, requested and observed concept dimensions, camera/stance, colors/materials, declared native-scale assumptions, locks, pose/reference roles, prompt/attachment history, user approval statement and unresolved questions.

For pixel art, hand off to [pixel-art-director](../pixel-art-director/SKILL.md) and the existing [next-asset guide](../../docs/new-asset.md): then test scale, make a native structured source, prove one local revision, animate and observe in Godot. If the production candidate drifts from the approved concept, return to the appropriate review gate instead of redefining identity silently.

## Stop conditions

Stop concept production when the human has not approved a bounded exploration, generated identity keeps drifting, comparisons are not actually fair, the reference cannot be displayed, budget/permissions are missing, or the requested character remains ambiguous. Report the exact stage, evidence, best retained candidate and next human decision. No new paid service, credential or installation is authorized by this skill.
