# ADR 0001: AI-directed concept exploration and structured asset production

- Date: 25 October 2026
- Status: accepted project direction
- Source: the user's conversation and repository-setup request

## Context

The user wants a stylish combat-heavy 2D game in Godot, is new to development, and cannot currently draw. The goal is to express a personal visual and motion direction while AI performs construction and revisions.

The user clarified that the workflow should explore generated images and then produce actual sprites; importing a PNG for the user to paint over does not satisfy that goal.

## Decision

Use a staged workflow: concept exploration, explicit style/motion rules, AI-authored native asset construction, combat animation, Godot observation, and a deliberate revision test.

Retain meaningful editable masters and any construction sources so the agent can make controlled changes. Let the user direct and approve the artistic result while the agent carries out technical work and explains relevant basics.

## Consequences

Visual direction and motion are evaluated early together. A good concept image does not establish animation quality. The next recommended proof is one character and one representative attack, with an art and timing revision before broad production.

Researched alternatives remain available when an actual test reveals a limitation. No service, editor integration, pixel resolution, palette, camera, or animation method is selected by this ADR.

## Revisit when

The user's references suggest another representation, the first proof cannot preserve the intended style, or revision effort is unacceptable. Record the evidence and user decision before changing the production direction.
