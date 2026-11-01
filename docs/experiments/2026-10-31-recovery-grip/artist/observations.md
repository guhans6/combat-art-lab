# Isolated recovery-grip pose candidate

Artist: requested Sol / High assignment. Backend: dedicated Pebbly0.8.2 headless MCP,
Aseprite1.3.18.6-dev. Python3.12.14/Pillow12.3.0 used only for preparation,
read-only native decoding and checks/review images. No CLI/Lua/native-file writer,
image generation, installation, animation export or Godot run.

## Before drawing

Inspected original canonical `2026-10-30-tote-attack/inputs/character-scene.png` and
`character-closeup.png`, generated `additional-keys.png` and `six-keys.png`,
`artist/sol-rescue/preparation/frame-09-base.png`, rejected `v03-frame-8.png`,
and `2026-10-31-comparison-regression/inputs/user-rejected-grip.png`.
Original identity cues are tied brown hair, turned restrained face, olive jacket,
wide blue jeans and warm cream tote. This task protects their native pixels.
Generated middle pose supplies the recovery arrangement, not an approved grip.

Rejected F9 has large block-shaped skin masses; the broad fan of handle pixels
from the top layer meets a relatively flat hand underside. Native ownership
inspection also found old handles on tote layer4 behind the newer layer5 hand/
backing and layer6 handle fan. Patching the top composite alone would leave those
old paths exposed when narrowing the new handles.

Frozen pre-edit contract is `scope.json` plus `proof/allowed-mask.png`; parent
recorded their hashes before edits. These remain unchanged. Full13-frame native
copy; only F9/index8 local cels may change. Artifacts are isolated pose studies,
not an integrated or approved animation.

## Pass01 and specific correction

`source/recovery-grip-pass01.aseprite` / `proof/recovery-grip-pass01.png` preserve
main pass and `operations/pass01.json` records dedicated-MCP inputs. Front terminal
hand was reduced with stepped pads and skin-shadow detail; exposed handle lengths
narrowed. My inspection found inherited layer4 strokes beside the new branches.
Parent's clean review independently found the same tangled remnant/rim region and
requested correction round1.

`source/recovery-grip-pass02.aseprite` / `proof/recovery-grip-pass02.png` preserve
that correction. `operations/pass02.json` removes inherited upper handles on their
actual tote owner, routes the far length into the far rim and gives the front hand
an opposing thumb and descending pads. One allowed correction round remains unused;
no unsupported cosmetic pass was made.

## Actual visible relationships, pass02

Coordinates below refer to the native320x192 export and are bound to the pixel/
owner readback in `proof/attachment-readback.json`.

The small cream fold at(175,83), brown edge(176,83), is beside the back palm.
The warm skin edge on the next row covers it: light(174,84), shadow(175,84),
outline(176,84). The front thumb/finger edge descends diagonally left: light/
shadow/outline at x173/174/175,y85; x172/173/174,y86; x171/172/173,y87;
and x170/171/172,y88. The pads have unequal stepped ends, replacing a flat rectangle.
Cream reappears beneath the hand at(171..172,90) and(175..176,90), with a shared
brown fold at(173..174,90). Olive at(174,91) separates the two descending lengths.
The left length reaches cream(162..163,109); the far length reaches cream
(187..188,99) at the retained rim corner.

This is one visible handle-loop silhouette with two descending lengths. It does
not establish two independently delineated tote loops. The second hand overlaps
the front hand: the right-side wrist leads to a back palm around(172..175,81..83),
and the foreground thumb/fingers cover its lower side. Separation of the two
hands is less explicit than the two forearms. A through-palm hidden strap is
inferred from exposed portions; the source does not draw a complete concealed
strap beneath each finger. These are uncertainties for approval, not proven anatomy.

## Gains and regressions are separate

Observed at native1x, integer8x detail and full-body context through actual MCP
previews: compact front terminal, a stepped skin edge, narrower cream lengths,
and removal of the extra fan. Parent independently observed the two main branches
now read as one grip-to-rim loop. This supports showing the pose proof.

Uncertain: whether the front hand reads as an enclosing grip without explanation,
and whether the overlapped second hand is sufficiently distinct. The new loop
opening is larger (86 newly enclosed transparent pixels), intentional space between
handle and rim rather than garment coverage. It remains a visual decision. Face,
legs and torso outside the local connections remain pixel-identical. Narrow far
strap is less broad than the former rendering; user may prefer a heavier fabric
read. No independent loops or complete hidden-hand anatomy are claimed.

Latest checkpoint is pass02, awaiting user inspection; no artist self-approval,
production selection or propagation. Parent owns the clean comparison packet and
independent final checks. No authored-speed playback or neighbor-frame integration
was reviewed because only this still was authorized for the current gate.

## Mechanical evidence

`proof/pass02-checks.json`: only native F9 layers4/5/6 changed; all other cels,
layer metadata, palette/noncel frame chunks, durations and cel geometry/type/
opacity/z remain exact. 422 composite pixels changed in[159,80,191,110); zero
outside the frozen mask, no new visible colors, binary alpha. Invisible RGB in10
transparent exported pixels differs from the decoder's canonical zero; native
visible/alpha pixels match. The fresh dedicated-MCP reopen PNG matches the prior
MCP PNG byte-for-byte in decoded RGBA (`proof/reopen-check.json`). Originals retained.

The available tool inventory advertises a validate feature but exposes no validate
method. Therefore no native `validate` invocation is claimed. Independent native,
palette, alpha, PNG and mask checks were run instead; this limitation is explicit.
Scratch proof records image delivery, oriented pattern, exact color edit,
transparent-skip, erase behavior, protected-layer preservation and save/reopen.
All artist-owned MCP documents were saved and closed before releasing the lease.
