# Recovery grip: isolated pose proof

- Status: pose candidate for user inspection; no artistic approval or propagation.
- Date:31October2026.
- Request: Sol High repairs recovery grip using the updated workflow, showing the
  corrected pose and before/after before updating the full animation.
- Artist: explicitly requested gpt-6.1-sol/high, fresh context; parent independently
  inspected clean exports and verified protection. No other artist/model rescue.
- Baseline: rejected tote v03 F9/index8. [Frozen inputs](inputs/manifest.json),
  [scope and checkpoint plan](plan.md), [artist observations](artist/observations.md).
- Tools observed: dedicated headless Aseprite MCP/Pebbly0.8.2,
  Aseprite1.3.18.6-dev; existing Python3.12.14/Pillow12.3 for preparation/readback
  and review packaging. No new generation, installation, CLI/Lua editor invocation,
  Code-MCP, CUA, runtime playback, commit or publication.

## Candidate and artifacts

[Native candidate](artist/source/recovery-grip-pass02.aseprite), SHA256
`b2508d390693adaacc8f6db9ed9f3f129828a6071d20a1c4f9b6779c78009f38`.
It is a separate13-frame native working copy with only F9 locally revised, retained
to prove protection. It has not replaced the attack source or been integrated into
a new animation export. Other12poses/timing remain exact. Editable operations and
earlier checkpoints remain under artist/.

- [Corrected pose,3×](review/corrected-pose-3x.png), [native PNG](review/corrected-pose-native.png).
- [Clean before/after](review/before-after.png): rejected F9 left, candidate right;
  full native views above, identical6×hand/handle crops below.
- [Source-bound comparison packet](review/packet/packet.json) with differences,
  exact crops, scope coverage, input/evidence hashes and pending visual status.
- [Independent checks](verification.json), [raw native/readback checks](review-checks/parent-raw-scope-and-readback.json).

## Pass ledger and review provenance

| Pass | Observation | Decision |
| --- | --- | --- |
| Pass01 | More compact hand contour, but old tote-owner handle strokes remained beside the new paths. Parent independently observed the extra branches at1×/8×. | Not cleared; specific correction requested on actual owner. |
| Pass02 | Old upper handle fan removed, far length routed into retained rim; stepped finger/thumb edge crosses the bundle. | Retained for user pose inspection, no cycle propagation. |

Frozen pre-edit owner/mask contract: artist/scope.json and proof/allowed-mask.png;
parent captured both hashes before production edits in baseline/artist-pre-edit-scope.json.
Only F9 tote/grip/tension owners4/5/6 changed; backing owner2 was permitted but not
changed. Main pass plus one concrete correction; remaining round was not spent on
unsupported cosmetic edits. All artist-owned native documents saved/closed.

Parent reviewed actual clean pass01/pass02 full poses at1×, matched8×crops, final3×
pose and6×comparison. The producer supplied artifact paths before its own verdict.
Final manual observations bind packet SHA256
`f50021292f4bff8a01bbd88fcd6b7779adb666781938e295e1e32e81d090bc40`:

| Area and evidence | Target improvement | Regression/uncertainty |
| --- | --- | --- |
| F9 grip, crop[140,60,205,130),1×/6×/8× | Compact stepped skin edge replaces broad terminal block; exposed cream is covered by skin and reappears beneath it. Parent native pixel readback confirms cream175,83, skin174..176,84 and reappearance171..172/175..176,90. | Back hand overlaps front hand and is less explicit; a hidden strap route remains inferred. This does not prove two separately delineated grips. |
| Upper handles/rim, same crop | Unrelated upper fan remnants removed on their native owner; main branches now trace one visible loop/shared bundle to retained rim. | The far strap is thinner; two independently visible tote loops are not claimed. User must judge cloth weight/readability. |
| Handle opening | Larger negative space is visibly between handles and rim. |86newly enclosed transparent pixels are intentional loop opening, reviewed as background space, not blindly filled as a cloth hole. |
| Whole character, final native/3× | Face/head, pose, outfit, feet and bag mass retained. | No new visible change outside local scope; exact protection checked separately. Static evidence does not establish temporal recovery quality. |

Selection: pass02 is a candidate for the user's requested pose gate, not an approved
improved animation. Remaining overlapping-hand uncertainty prevents production
clearance; technical passes do not override it. Original v03 rejection stands until
the user accepts a specific replacement. No neighboring frame or full-cycle review
was performed in this bounded pose task.

## Technical proof

Parent independently decoded the native and checked all actual cels:3changed,
56remaining native cels exact, all outside-mask raw/visible RGBA changes zero;
all other12composited poses exact.422visible composite pixels change only in
[159,80,191,110). Layer/cel metadata, palette, non-cel chunks and durations unchanged;
no new visible RGBs, binary alpha, all changes covered by the named comparison crop.

Native and exported visible RGBA match after canonicalizing fully transparent RGB.
Ten fully transparent exported pixels contain different invisible RGB from the
read-only decoder; this is disclosed, not described as raw-RGBA equality. Fresh
dedicated-MCP reopen PNG equals the exported PNG in decoded RGBA. Comparison build
and freshness verify pass while visual/user acceptance remain pending. The exposed
MCP inventory lacked the advertised validate method; independent actual checks were
used rather than claiming an unavailable invocation. See artist scratch/proof records.

Preservation/delivery identity is recorded in preservation.json and artifact-manifest.json.
Original source/exports/full GIFs/runtime and earlier experiment files are unchanged;
only handoff is intentionally updated outside this new experiment. No broader test
suite rerun was needed: no reusable helper changed, and checks ran against actual
native/export artifacts. No Godot/full-animation validation is claimed.

Next owner: user reviews this exact pose and clean before/after. Full animation work
waits for that feedback; no approval is inferred and no propagation was performed.
