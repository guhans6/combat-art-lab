# Standing refinement: face first, then hair and fabric

- Date: 26 October 2026
- Status: v02 constructed and locally checked; visual review pending
- User direction: “Good! Can you iterate and fix the issues mainly the face first and others after that?” This is positive feedback on v01 and authorization to refine the standing candidate, not final acceptance of its likeness or permission to expand into animation.
- Baseline: [v01 master](../../../assets/source/standing-v01/standing.aseprite), [v01 export](../../../assets/export/standing-v01/standing.png), finalized concept references and the current style guide. Prior source and artifacts preserved.
- Scope: prioritize facial likeness, then refine existing hair/clothes/shoes without redesigning outfit, stance, bag or canvas. No computer use; no new dependencies or paid services; no commit/push.
- Tools: existing Aseprite 1.3.18.6-dev batch Lua and bundled Python/Pillow for file analysis and preview layout. Same drawing method and previously inspected API/research as the first reconstruction.

## Checkpoints

1. **Face core.** Compare eye locations, foreground fringe, jaw and neck against the finalized cutout/close-up. Move near-eye cluster left, reposition and reduce the far-eye cluster, open the near-eye area by adjusting the fringe, shorten the chin, simplify cheek/neck shading, and replace the bright chin accent. Keep the skin color changes local to the face layer rather than recoloring hands.
2. **Face proof.** Preserve the [native checkpoint](../../../assets/source/standing-v02/standing-face-checkpoint.aseprite), [PNG](../../../assets/export/standing-v02/standing-face-checkpoint.png), and drawing-source snapshot. Exactly 292 composite pixels changed from v01, all within the x53..78 / y13..42 face/neck region. No clothing, feet, tote, hands, body or anchor changes at this checkpoint.
3. **Secondary refinement.** Warm hair colors, narrow/rearticulate the tied mass and curls, split broad crown highlights, reduce broad trouser light patches, narrow a dark denim side band, and refine a sleeve highlight and shoe sole pixels. Keep the tote, tee, hands, strap and ground-guide layer images byte-identical to v01.
4. **Proof.** Reopen native source, inspect/export layers, run the separate local tote-edit check, and reconstruct v02 in a fresh ignored folder. Compare full-body, face and actual-size previews. Preserve v01 and every completed checkpoint.

## Review artifacts

- [Reference / v01 / v02 face](../../../assets/previews/standing-v02/face-before-after.png).
- [Reference / v01 / v02 full body](../../../assets/previews/standing-v02/full-before-after.png).
- [Actual-size comparison](../../../assets/previews/standing-v02/at-size.png).
- [Native v02 master](../../../assets/source/standing-v02/standing.aseprite), [transparent PNG](../../../assets/export/standing-v02/standing.png), [drawing source](../../../assets/source/standing-v02/draw.lua), and [run instructions](../../../assets/source/standing-v02/README.md).
- [Native source checks](source-checks.json), [export checks and hashes](export-checks.json), [exact change-scope checks](change-checks.json).

The reduced reference is explicitly labeled and used only for comparison. Sprite pixels are authored by Lua geometry/pixel instructions; no reference image is loaded by the construction script.

## Observed results

| Check | Result |
| --- | --- |
| Face-first scope | 292 changed pixels confined to face/neck at saved checkpoint |
| Previous candidate | v01 PNG SHA-256 remains `7dbf8ea70416d61f7e6c19662c72fa50935c891d034ba39502f5004e1e8a27d7` |
| Final native source | Reopened with 12 named layers, one frame and standing tag; 128x192 canvas |
| Main export | Reopened native export is identical; binary alpha; 51 visible opaque colors; original bounds/feet anchor retained |
| Fresh construction | Exact PNG bytes reproduced in `.scratch/reconstruction/v02-rebuild` from final v02 drawing source |
| Preserved layers | Tote body, tee, hands, tote strap and hidden ground-guide decoded images identical to v01 |
| Local edit test | 223 source tote pixels recolored in a separate file; 171 visible composite pixels changed, all in the tote layer; all other layer images unchanged |
| Visual inspection | Face has more frontal eye separation, a shorter jaw and less angular chin/neck shading. Hair and folds remain stylized/simplified relative to the reference; no exact-likeness or user-approval claim |
| Engine / animation | Not performed; static PNG review only |

## Next action and ownership

Present v02 for the user's likeness review, with face first. Continue focused standing corrections based on concrete feedback. Keep finalized design and prior candidates intact. User approval of the current asset, attack selection, animation and real Godot playback remain separate boundaries. Work remains local and uncommitted.
