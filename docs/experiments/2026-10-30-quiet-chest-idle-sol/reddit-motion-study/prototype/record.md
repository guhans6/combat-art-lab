# Coordinated upper-body idle — pass01

30 October 2026. **Retained for user playback review.** User clarified that subtle shoulder motion belongs within whole-upper-body breathing. The absolute head-position lock from earlier passes is therefore released; original head/face/hair drawing and blink remain protected after spatial registration. Original static expression is preserved; the reference clip's open mouth is not copied.

## Native construction

Input: `../../pass01.aseprite` SHA256 `82a4a7f309feae726b3e26134f114a21433a494a0eb2192bb7be82d2ca779b79`. Original character scene/closeup remain identity authorities; the [actual Reddit clip study](../record.md) supplies motion/process observations only. No from-scratch redraw, scaling or palette change. Existing neutral F1 garment pixels replace the rejected independent fold movement on F2/F3/F4.

F2/F3 use the same1px upward field for head, neck, collar, shoulders, chest, upper sleeves and attached strap. This keeps their relative registration. The field stops earlier toward the forearms and later at the central chest; pelvis, pocketed hands and tote remain fixed. Central chest motion reaches y62 in F2 and y66 in F3. F4 returns to the original neutral pose. No sideways expansion or separately moving shirt highlight/fold. Two head heights remain a visible quantization limit; this is a coordinated mass hypothesis, not biomechanical proof.

Backend: dedicated Aseprite AI Artist0.8.2 headless, Aseprite1.3.18.6-dev. Native preflight/info passed. [Preparation](proof/prepare.py) computes explicit sampling/masks; [operations](proof/operations.json) and [native call results](proof/native-results.json) preserve the actual editor drawing path. Python only reads native sources or prepares analysis/previews; it does not author the native sprite. No Aseprite CLI/Lua/UI/Code-MCP, image generation, install, nested agent or commit.

One initial motion pass plus one focused coverage correction. Actual native inspection found garment pixels fragmented into fixed hand layers: peak motion exposed8pixels near pocket joints. [Precoverage source](proof/pass01-precoverage.aseprite) remains preserved. [Cleanup operations](proof/coverage-cleanup-operations.json) add exact neutral composite samples as jacket backing at `(47..49,66)` and `(70..74,65)`, preserving the fixed native hand layers. No new colors. Initial coverage comparison also flagged translated intentional hair openings; those are checked at their registered head positions instead of filled. Final native was saved, closed, freshly reopened, inspected, all8PNGs exported again, checked and closed. No unsaved editor document remains.

## Artifact and observed checks

[pass01.aseprite](pass01.aseprite), SHA256 `06cfc2df7adb0846cdb98ee21dd473bf3265f30b1eb4c391d9dad1c9be48361d`. Actual transparent exports `frame-0.png` through `frame-7.png`; [native GIF](pass01.gif).

- [Exact1x GIF](proof/neutral-1x.gif), [3x GIF](proof/neutral-3x.gif), [previous cloth left / new coordinated right](proof/cloth-left-coordinated-right-3x.gif).
- [All poses1x](proof/contact-1x.png), [3x](proof/contact-3x.png), [upper-body6x](proof/upper-contact-6x.png), [transparent sheet](proof/transparent-sheet.png).
- [Independent verification](proof/verification.json), [reader/check recipe](proof/verify.py), [fresh reopen frames](proof/reopen/), [GIF checks](proof/gif-checks.json), [original hashes](proof/input-hashes.json).

PASS:128x192,twelve layers,96cels,eight frames; original255-entry palette, header/layer metadata/non-cel chunks including palette/tags/timing and cel geometry/opacity/z exact. Only declared layers/frames/mask changed. Native shoes/denim/tote/hands exact every frame; all composite pixels y69+ exact. Head/neck/hair native images and head composite exactly match the original after1px upward registration on F2/F3, and at original coordinates on every other frame. Complete blink-frame composites F5/F6/F7 exact;50/80/50ms blink unchanged. Original cycle600/350/550/600/50/80/50/250ms,2530ms total unchanged. No new enclosed alpha holes after registering intentional head cutouts. Every PNG equals independent native recomposition and all8fresh-reopen exports. Native transparent GIF visible pixels/timing exact. Matte/comparison GIFs use an explicit shared palette and decode exactly, including all8durations and infinite loop. All input/native/reference hashes unchanged.

## Visual decision and next owner

Constructor inspected actual native preview and decoded full-body/upper-body contact sheets. Parent independently inspected the initial8poses: correlated head/collar/shoulder rise removes the old relative shrug and isolated wind-fold cue; no obvious seam or foot shift. Final correction changes only the eight backed joint pixels; their fresh native preview was inspected. Retain this candidate for the user's playback decision, with no extra aesthetic pass.

The two-height1px movement can still look stepped or like a body bob, and retained timing may need judgment. Neither model watched real-time playback; convincing natural breathing is not established. No Godot run/gameplay validation, user approval, install, commit, push or publication. Parent owns final presentation/handoff; user owns acceptance of perceived motion.
