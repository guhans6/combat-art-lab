# Coherent idle correction v01 — frozen plan, 30 October 2026

Bounded derived-candidate study, not a new model benchmark. Exact baseline is the
preserved Sol6.1 native `baseline/sol-original.aseprite`, SHA256
e93d058a373ef5329ee862523a966e6db225ee0f5ba6fafd294a574b34b6c6c5.
Approved concept anchors remain `assets/references/approved-2026-10-26/character-scene.png`
and `character-closeup.png`. They were visually opened; tied brown hair/pale tie,
right-facing three-quarter eyes, shallow smile, olive jacket/pale shirt, broad jeans,
cream tote and hands in pockets remain the identity contract. No new expression.
Sol is user-preferred direction, not artistically approved. Luna56 supplies useful
connected upper-body lift; its hand displacement and lateral bag swing are not copied.

## Diagnosis and evidence

Local files inspected: all four final native masters, artist records/operations,
Sol prepare_operations.py, comparison builder/check_deliveries.py, native/reopen
and GIF evidence, prior rejected redraw/row-band studies in the handoff. Native
pose audit and original torso contacts are under `evidence/`.

Ranked hypotheses: (1) independently staggered primary anatomy, (2) native ownership/
seams, (3) isolated fold/shade changes masquerading as volume, (4) export/timing error.
Sol has a 120ms raised-shoulder/rest-head pose on inhale and a 160ms one on release;
its fold-tip fades 180ms before structural motion and remains 240ms after it.
Luna56 shifts upper-body/hand cels, then the tote with a 1px lateral swing; earlier
alpha repair restores coverage but cannot fix a moving pocket-hand relationship.
Terra moves face/neck before the hair layer (which owns most of the face/skull),
with a very short 740ms cycle. Luna6 mostly animates shirt-fold shades; anatomy is
still, so it is weak structural breathing evidence, not disconnected head motion.
The four recipes differ; there is no evidence of one universal export fault.

Existing export checks plus a fresh read-only timeline check distinguish authored
poses from playback. Existing binary alpha passes do not establish anatomical
connection; old repairs only address vacancies. At 4x, Sol's chest/neck pose steps
are visible with maintained materials; phase mismatch is an authored cause, not an
unproven claim about model reasoning. Naturalness remains a visual judgment.

## Motion hierarchy

One primary thorax driver selects rest or the existing connected inhale pose.
Head + neck + collar + shoulders + upper sleeves follow the same pose selection.
Head/hair are reused rigidly for identity, maximum rise 1 native pixel; neck/collar
coverage comes from Sol's repaired inhale key. No independent head lag/oscillation.
The upper sleeve contour responds, but elbows taper into fixed cuffs/wrists/pockets;
waist, denim and both feet remain planted. Not every part translates by the same
amount. This is reuse of reviewed Sol poses, not whole-body/row-band warping.

Cloth secondary response is only an existing two-pixel muted lower-rib crease tip
advancing up 1px, 180ms after structural rise. It relaxes while the torso is still
raised, then the core returns together. Its footprint/color role is retained; no
new shade, glitter mark, shoulder shrug amplitude or relighting is introduced.
Tied hair follows skull; no loose-hair flutter without evidence. Upper strap follows
its shoulder, lower attachment/tote remain fixed; this small lift takes up slack.
No unsupported tote swing or arbitrary delayed whole-bag movement. Blink omitted,
as in Sol baseline; future blink may use an independent eye-only clock.

## Frame and timing plan (native 128x192; zero root travel)

| F | ms | Thorax/shoulders | Neck/head | Arms | Shirt/clothing | Hair | Tote/strap |
|---|---:|---|---|---|---|---|---|
| 1 | 1100 | Rest | Rest | Fixed pockets | Rest | Rest | Rest |
| 2 | 180 | Inhale rise 1px | Follow core 1px | Upper sleeve follows; wrists fixed | Collar follows; lower fold retains rest | With skull | Upper strap follows; bag fixed |
| 3 | 120 | Inhale | Hold connected rise | Same | Lower-rib crease takes tension | With skull | Same |
| 4 | 360 | Inhale apex | Same | Same | Crease held | Same | Same |
| 5 | 220 | Apex/release onset | Same | Same | Crease held | Same | Same |
| 6 | 160 | Exhale preparation | Same | Same | Crease relaxes | Same | Same |
| 7 | 240 | Exhale to rest | Return with core | Rest, pockets fixed | Rest | With skull | Rest |
| 8 | 1000 | Rest | Rest | Rest | Rest | Rest | Rest |

Total 3380ms, matching Sol's original period for direct comparison. Integer-pixel
art retains a visible one-pixel primary step; no claim of continuous subpixel motion.
Final and first drawing are exact rest. Shared phases constrain primary attachments;
only explicitly justified cloth follow-through gets a delay. All-body identical
translation is not the method.

## Scope, checkpoints and bounded effort

One candidate construction plus one focused repair if inspection identifies a concrete
defect. Preserve all originals/checkpoints. Existing twelve layers/order/palette,
hidden guide, denim/shoes/hands/tote body and rest frames protected. Actual owner
inspection precedes each patch; lower-shirt four pixels are the only new drawing.
No independent canvas fitting, new rig, image generation, installs or publication.

1. Establish native/reopen/export baseline and a reproducible phase audit.
2. Apply patches through dedicated Aseprite MCP, inspect key and transition exports
against Sol/original concept at 1x/integer zoom; then retain/reject for user review.
3. Export exact-speed GIFs, comparison and durations contact. Fresh native reopen,
protected pixels, binary alpha/new-body-hole/timing and loop checks. Existing director
suite. Godot: adapt an isolated copy of the existing preview rather than replacing
current production textures. Record actual engine target/version and observations.
4. Add the smallest shared-phase/anatomical review rule to the existing instructions,
review this task's patch against its frozen starting copies and current user brief.

Agent owns construction/verification; user owns appearance/motion approval. Local
proof, actual temporal perception and Godot playback remain distinct claims. Proposed
new tests await the seam question; existing verification can proceed independently.

## Final bounded repair

Pass01 moved the crease tip and made a detached mark; rejected. Pass02 instead
extends the same tip while preserving its two connecting source pixels, so only
two extra muted fold pixels appear at y54 on F3–5. Native v01, its recipe/exports
and the localized repair evidence are retained. No further art pass. User confirmed
the proposed native/export test seams; five focused regression cases now pass.
