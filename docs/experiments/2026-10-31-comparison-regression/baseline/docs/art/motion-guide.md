# Motion guide

## Current idle direction — 30 October 2026

Latest feedback: Sol6.1's restraint/slow cycle was initially preferred in the
[four-model study](../experiments/2026-10-30-evidence-idle-four-model/README.md),
but disconnected movement remains rejected. The [derived coherence candidate](../experiments/2026-10-30-coherent-idle/record.md)
uses a shared breathing phase, connected upper-body pose, planted pocket/foot
anchors and only justified cloth follow-through. It awaits user visual approval.
Use the director's [connected-motion checkpoint](../../tools/pixel-art-director/references/animation.md#plan-connected-motion-before-extending-the-keys)
for new sequences. Earlier partial preferences below are historical direction.

The user prefers the movement direction of the [latest redraw](../experiments/2026-10-30-redrawn-breathing-sol/proof/neutral-3x.gif)
but rejects its clothing appearance for game use. The earlier two-panel comparison's
appearance preference is recorded in the [style guide](style-guide.md#animation-appearance-direction--30-october-2026).
Neither whole animation nor either earlier side is newly approved. The latest redraw
is rejected as a combined game candidate; preserve its partial motion preference as
direction only. See the [diagnosis and evidence boundaries](../experiments/2026-10-30-animation-workflow-integration/record.md).

## Tote attack prototype — 31 October 2026

The user chose a two-handed tote swing as the next bounded combat test.
[Native v03 and evidence](../experiments/2026-10-30-tote-attack/record.md) use13frames
over1680ms: pickup/shared grip, counter-windup, strike, follow-through, bent-elbow
arrest, inward settle, re-shoulder and exact neutral return. Torso/shoulders/arms
form one load chain; continuous handles connect the bag as it stays downstream
briefly during braking. F6 is the proposed contact interval590–650ms. F6–F8 front
sole is held; later stance resets remain coarse key steps. Godot4.7.2 verified
three contacts/returns. User artistic approval, final pacing/range and polished
footwork remain open. Earlier blank attack fields remain production choices.

## Animation procedure

For animation construction, revision or diagnosis, use the director's
[animation procedure](../../tools/pixel-art-director/references/animation.md).
Its task-specific profile and separate motion/material/expression/technical decisions
apply before extending keys and again to the exported cycle. Static facial edits use
the existing [face procedure](../../tools/pixel-art-director/references/face-likeness.md).

## Current standing idle experiment — 27 October 2026

The user authorized a quiet full-body standing/idle scene. [Observed prototype](../experiments/2026-10-27-standing-idle-godot/record.md):
eight native frames over 3000 ms, one-pixel upper-body inhale and blink, fixed denim/shoes and root.
Shared 96x216 character grid; no independent frame fitting. Actual Godot playback ran two loops
before the user's later MCP-only restriction. This is agent-provisional appearance/motion;
user selection, secondary hair/cloth motion, attacks and gameplay contact remain open.
Earlier status and representative-attack fields below are historical/unresolved.


Historical status on 25 October 2026: two visual stills received; no motion clip or representative attack selected. The later [decoded motion-reference study](../experiments/2026-10-30-quiet-chest-idle-sol/reddit-motion-study/record.md) supersedes the absence of a clip. Desired combat speed, weapon and camera remain open; idle evidence does not choose them.

## Motion target

- Reference clip and useful timestamps:
- Desired movement qualities:
- Character, weapon, camera, and facing:
- Intended gameplay behavior:

## Representative attack

| Phase | Pose/trajectory | Duration or interval | Gameplay relationship |
| --- | --- | --- | --- |
| Anticipation | Open | Open | Preparation/input behavior |
| Strike/contact | Open | Open | Active damage interval |
| Follow-through | Open | Open | Continuation beyond contact |
| Recovery | Open | Open | Return to allowed next action |

Frame count, frame duration, and simulation rate are separate values. Decide each from the action and chosen representation.

## Effects and transitions

Record trails, impact cues, sound, camera behavior, and any pause only when chosen. Inspect the underlying action with effects disabled. Define facing changes, interruptions, and looping only when in the current test scope.

## Review

Compare actual-speed playback and key poses against the intended motion. Record body/weapon consistency, silhouette readability, ground alignment, contact, recovery, and unresolved defects. User approval must name the reviewed version.

## Supplementary motion references and normalization

After a convincing static checkpoint, obtain a short coherent key-pose sheet or
individual poses using canonical identity/style references and the selected native
base. Both routes are allowed. Review each pose for head volume, face/expression,
hair/outfit/tote continuity, proportions and material palette before native finishing.
Measure returned pose count, crops and transparency; prompt wording is not evidence.

Use shared native scale, palette, slots, pivots and explicit anchors for the sequence.
Do not fit each pose independently to its bounds or align every lowest pixel to ground;
preserve intended jumps/root travel in declared per-frame offsets or an engine track.
Keep pose-expression changes intentional. Store durations, order, contact and timing
separately from drawings. Helpers can apply known mappings; they cannot infer anatomy.
Review actual-speed played output plus frame strips, then run Godot before claiming
runtime readiness. A short hair/head movement is a technical motion probe, not a combat
proof. Weapon, attack and permanent camera choices remain unresolved.
