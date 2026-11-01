# Luna6 expression strip — frozen task profile

- Date: 30 October 2026.
- Intent: one static expression-strip construction pass on three copies of the same full-body source: neutral, subtle friendly closed smile, and restrained surprise.
- Assigned drawing route: Luna6 Max (`gpt-6-luna`, maximum reasoning effort), per the user-approved project route.
- Backend: dedicated Aseprite AI Artist MCP 0.8.2 in headless mode; Aseprite 1.3.18.6-dev.
- Exact baseline: `inputs/baseline.aseprite`, copied from `docs/experiments/2026-10-30-luna-fullbody-once/trial-b/passes/luna6-fullbody-cleanup.aseprite` before any mouth edits. Its paired PNG and both approved references are frozen under `inputs/`.
- Canvas/native profile: 128×192 RGB, one 100 ms frame per variant, 12 layers (one hidden locked guide), existing 255-entry palette.
- Authority: approved close-up is primary for face, hair and expression; approved scene is identity/body/costume and full-context reference. The baseline is a construction starting point, not user-approved artwork. The rejected Luna6 mouth correction and pending Sol smile are not inherited.
- Scope: edit only declared mouth and, for surprise, brow/eye interior pixels on the observed native owner `08-hair-tie-and-hair`. Preserve the face outline, nose cue, hair silhouette/fringe, every other face/body pixel, all unrelated layers, alpha, palette, canvas, framing and timing.
- Construction budget: one first artistic strip pass with one variant per expression. There is no pixel-count quota. Variants are independent copies of the same baseline; they are not animation frames and their shared pose is not motion proof.
- Review target: actual MCP export against approved source, unchanged baseline and all three variants, at full-body 1×/3× and head 8×. Review at the intended 1× size before judging magnified clusters.
- Acceptance boundary: technical native/export protection can pass while expression remains uncertain. The user owns visual selection. This folder records Luna construction only; parent/Sol owns the later independent review/rescue and the cross-arm result.

## Frozen inputs

| Input | Role | SHA-256 |
| --- | --- | --- |
| `inputs/baseline.aseprite` | Exact pre-mouth native baseline | `dbdf2f693872d2b3c5f102cea01bc1e2441d2452d790770b7b68effd6c563348` |
| `inputs/baseline.png` | Exact baseline export | `c162e373a9b0ed72e2e82f91a6fe6608952444ed3ef9151534fcd29843b65def` |
| `inputs/character-closeup.png` | Approved face/expression/hair reference | `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7` |
| `inputs/character-scene.png` | Approved identity/pose/costume/full-body reference | `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae` |

No generation, install, external service, UI automation, CLI/Lua, Code-MCP, commit, publication, animation, or Godot playback is in this pass.
