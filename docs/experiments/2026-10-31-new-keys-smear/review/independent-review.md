# Independent structural review — structural pass 03

Date: 31 October 2026  
Reviewer role: independent read-only structural critic; producer conclusions were not provided.  
Stage reviewed: untextured structural keys only. No detailed-material, authored-speed, engine-playback, or user-approval claim is made here.

## Evidence binding and method

- Candidate native: `source/structural-pass03.aseprite`, SHA-256 `57f0a3c7c3df01ac68b7902875f2a0f08ede6a7ade2b3e83a16bd2ddb61cef98`.
- Evidence packet: `review/structural03-packet.json`, SHA-256 `6a368c39e010281f89480a4310792c6ae7df1200058dc0c52a7b1494c75f5ef0`. I recomputed all 22 listed file hashes; none differed.
- Canonical identity references opened: `assets/references/approved-2026-10-26/character-scene.png` and `character-closeup.png`.
- Pose proposals opened: all six `inputs/01-idle.png` through `inputs/06-recovery.png`, plus `inputs/original-neutral.png` and the actual original native.
- Clean evidence opened: all six `proof/structural03-*.png`, `review/structural03-keys-2x.png`, the current full-canvas `review/original-key-comparison.png`, all six current owner and hidden-owner sheets, and all six current guides.
- A read-only native decoder found a 256x208 document with six 100 ms frames and eight visible, normal, 255-opacity layers. Each decoded composite is pixel-equal to its corresponding `proof/structural03-*.png`. This establishes source/export correspondence for these stills, not artistic validity.
- This was a still-image inspection at native size and integer zoom. I did not perceive continuous motion and make no pacing, arc, or playback claim.

## Blocking finding: the carry-to-windup and recovery-to-carry role transfers are not solved

The shown endpoints do not establish the difficult neighboring-pose relationship required before cycle propagation.

- In key 3, the tote remains on the right shoulder: one hand holds the strap at `G=(143,62)` and the other hand has only just left the pocket.
- Key 4 jumps to a two-hand gathered grip at `G=(96,94)` with the tote left of the body. The current stills do not show which hand maintains the load, when the shoulder loop clears the shoulder/arm, or how the four visible strands are gathered without a release, crossing, or root-role swap.
- Key 6 ends with both hands at `G=(160,79)` and the opened tote down-right. The only return context is the exact neutral, where the tote is narrow and shouldered and the hands are back in pockets. No structural re-shoulder/grip-transfer key or stepped guide demonstrates how the key-6 rear/near routes become the neutral carry route.

These are not requests for smooth in-betweens. They are required changes in hand ownership, occlusion, and rear/near strand role. `plan.md` defers the unshoulder/pass and re-shoulder drawings to later cycle construction, while the connected-form procedure requires the difficult transition to be structurally resolved before expansion. Because the hidden route affects the requested attachment result, prose intent is not enough.

**Decision — neighboring-pose continuity: revise. Overall gate: stop before cycle expansion under the current evidence.** Add a simple unshoulder/gather transition and a simple re-shoulder/settle transition (or marked stepped overlays plus clean keys) that explicitly identify hand retention/release and each rear/near route. Re-run owner/hide and neighbor review on those transitions. The frozen plan already records an initial pass plus two structural corrections (`structural01`–`structural03`), so continuing requires either treating this as a newly evidenced blocking study within authorized scope or explicitly revising the exhausted structural-pass budget; it must not be hidden inside detail or smear work.

## Proportions and connected anatomy

The six endpoints otherwise retain a coherent character scale.

- Clean composite bounds are: neutral `(92,10)..(163,192)`, reach `(94,11)..(163,192)`, free hand `(97,12)..(163,192)`, windup `(65,9)..(186,191)`, extension `(75,15)..(215,192)`, and recovery `(85,11)..(198,192)` in native coordinates.
- Frames 1–3 use the exact same 4,411-pixel combined legs/shoes owner. The changed stances use distinct source-guided lower bodies rather than independently resized copies. Waist/crotch remain near `(123..129,76..104)` while the changed knee and sole positions support the visible bend, lean, and raised rear foot.
- The action heads use the same 42x32 rigid face/hair crop translated on the shared canvas; the original lower neck is not carried into the changed poses. The separately reconstructed shirt/neck owner is visible when the rigid head is hidden and overlaps/adjoins the head and collar owners in every changed key. I found no visible head-neck hole or doubled source neck in the clean composites.
- Windup's lowest opaque shoe pixel is at `y=191`, one row above the original/recovery floor contact at `y=192`, despite the guide's approximate sole observations at `y=192`. This is within the declared +/-3 px landmark uncertainty and does not by itself overturn the pose, but a later grounded neighbor sheet should confirm that it is deliberate rather than a one-pixel float.

**Decision — proportions/anatomy: continue for the shown endpoints.** Residual risk is the one-pixel windup ground registration and the fact that upright rigid-head reuse has only been judged in stills; neither authorizes motion or final identity approval.

## Grip, handles, roots, rim, and tote body

The visible endpoints provide concrete attachment evidence rather than merely touching silhouettes.

- At every current guide site, the claimed coordinates land on or within two Manhattan pixels of the relevant actual owners. Examples:
  - Windup: `G=(96,94)`, `FL=(81,105)`, `FR=(95,113)`, `NL=(78,110)`, `NR=(92,118)`, mouth `M=(87,110)`, bottom `(73,136)`.
  - Extension: `G=(174,68)`, `FL=(182,85)`, `FR=(192,73)`, `NL=(186,89)`, `NR=(197,77)`, `M=(188,80)`, bottom `(211,99)`.
  - Recovery: `G=(160,79)`, `FL=(166,97)`, `FR=(177,86)`, `NL=(170,101)`, `NR=(182,90)`, `M=(172,92)`, bottom `(193,114)`.
- On the three two-hand keys, hands/forearms are above and overlap or directly adjoin both handle owners at `G`. The cuff-to-wrist-to-finger path remains visible in the clean and hand-hidden views.
- `01-rear-handle` sits below `04-tote-body-rim`: its two far branches enter the recorded FL/FR sites and disappear behind the rim/body. `05-near-handles-seams` sits above the body: its NL/NR branches continue into the front face. `06-hands-forearms` sits above both, so the gathered bundle is actually occluded by the fingers.
- The action tote bodies have 789, 774, and 772 opaque pixels for windup, extension, and recovery. Their site vectors rotate coherently: for example, windup `M->bottom=(-14,+26)` becomes extension `(+23,+19)`, while all four M-relative root vectors rotate by about the same amount. This supports one rotating construction rather than three unrelated bags. Pixel counts are supporting observations, not an automatic art score.
- Owner-isolated and owner-hidden views show no second body, abandoned root fork, or old cream source bag left on jacket/sleeves, shirt/neck, hands, or legs when the new bag body/handles are hidden. The owner names are honestly mixed at the requested production granularity: the jacket owner contains both jacket and sleeves, and the lower-body owner contains both denim and shoes; the review relies on the visible pixels rather than those names.
- Neutral/reach/free-hand bags change from a narrow carried view to a somewhat broader/lower face before removal. That can be explained by the hand pulling and rotating flexible cloth, but the missing carry-to-windup transition is where this explanation must become visible rather than remain assumed.

**Decision — attachment for the six shown endpoints: continue.** This does not clear the unresolved transfer between those endpoints, detailed seams/materials, or every future frame.

## Gate summary

| Dimension | Decision | Evidence boundary |
| --- | --- | --- |
| Proportions / anatomy | **continue** | Shared scale, registered landmarks, exact early lower-body reuse, source-guided changed stances, and reconstructed neck/collar joins read coherently in the six stills. |
| Attachment | **continue** | Actual owner order and hide views support fingers -> gathered rear/near handles -> far roots behind rim / near roots into face -> one rotating tote body. |
| Neighbor continuity | **revise** | Carry-to-windup grip/strand transfer and recovery-to-neutral re-shoulder/settle are not drawn or marked; required ownership/occlusion changes remain uncertain. |
| Overall expansion | **stop for now** | Under ADR 0002 and the connected-form procedure, one uncertain required relationship blocks propagation. Do not spend cycle/smear/detail budget until the two transfer studies are reviewed. |

Best eligible checkpoint for endpoint structure: `structural-pass03.aseprite`, retained as a diagnostic structural candidate. It is not selected as an improved animation or ready for art approval. User visual approval, authored-speed motion, material/detail continuity, every exported future frame, alpha coverage, and Godot behavior remain untested by this review.

---

## Continuation review — transfer study 02

This continuation reviews only the missing transfer increment that caused the stop above. It does not re-score the unchanged six keys.

### Evidence binding and source correspondence

- New native: `source/transfer-study02.aseprite`, SHA-256 `2174c9d4166a9ea2cc198feaa56f076f2a94f2df4ae41700a90c6793d506c041`.
- Transfer packet: `review/transfer-packet.json`, SHA-256 `f03755edf0b4e4ab91926f3a8fa3ab12157722f2dd131e668b2dc992b1644647`. I recomputed all seven packet-listed hashes; none differed.
- Actual MCP exports inspected directly: `proof/transfer02-7.png`, SHA-256 `3aa1001d5032043a0e529522c84607c1bf16a693c470431044fa7e49d227a0fd`, and `proof/transfer02-8.png`, SHA-256 `f58b949f6685abf4bee94d58196c02a6f585f8ab4a7db98f7371ea0d4c7552c4`.
- The native contains eight 256x208, 100 ms frames on the same eight normal visible layers. Read-only decoding showed frames 1–6 are layer-for-layer pixel-identical to `structural-pass03.aseprite`; decoded frames 7 and 8 are pixel-equal to the two actual MCP exports above.
- Opened evidence: both clean exports, both current ownership/hide sheets, both site sheets, and the outbound and return neighbor strips. No engine or playback was used.

The two clean proof PNGs are not entries in `transfer-packet.json`; only the derived ownership/site/neighbor sheets and site JSON are packet-bound. The hashes above bind the exact proofs inspected in this review, so this is not a semantic blocker, but the producer should add them to any packet used as the durable machine-verifiable evidence bundle.

### Outbound grip and strand roles

The new key 7 now supplies the previously missing shoulder-clearance state.

- From key 3, the right hand retains the same load and moves the gathered top to `G=(157,43)`. Both rear and near handle owners have actual pixels at G, and the hand/forearm owner covers them there.
- The handle bundle lies outside the right shoulder: its top is around x157 while the shoulder landmark is around x140, and the clean drawing contains no pale span still resting across the shoulder.
- The revised left arm follows shoulder `(112,50)` -> elbow `(126,73)` -> wrist/hand around `(151..156,61..62)`. In the actual composite it reaches across to occlude the lower visible handle strands; those strands remain visible both above/beside and below the catch rather than terminating at the forearm. The earlier stacked-forearm ambiguity is not present in transfer study 02.
- The right arm follows shoulder `(140,49)` -> sleeve/elbow around `(167,67)` -> raised forearm -> retained top grip around `(157,43)`. With hands hidden, the two new jacket sleeves end at their new cuffs; with jacket hidden, the two forearms remain separately legible. I found no surviving source-key-3 free hand, old sleeve end, or doubled arm on the other owners.
- Far roots `FL=(155,74)` and `FR=(165,72)` occur on rear-handle/body pixels; near roots `NL=(156,80)` and `NR=(166,79)` occur on near-handle/body pixels. The far owner remains below the rim/body and the near owner remains above it.

Key 8 then establishes the two-handed gathered state at `G=(134,86)`. Both handle owners and the hand owner occupy G; the two forearms converge from distinct cuffs, cover the bundle, and the strands reappear below before reaching `FL=(128,104)`, `FR=(144,102)`, `NL=(128,110)`, and `NR=(144,108)`. The tote body has 773 opaque pixels, consistent with the already reviewed opened action bodies (789/774/772) rather than a newly scaled prop.

**Transfer attachment decision: continue.** The actual drawing supports right-hand retention, left-hand catch, two-hand gather, the same four roots, and no shoulder span after lift.

### Neighbor and return continuity

The outbound neighbor strip now shows a structurally usable route:

1. Key 3: shoulder supports the tote; right hand retains the strap; left hand is free.
2. Key 7: right hand lifts the bundle wholly off/outside the shoulder; left hand catches the lower strands.
3. Key 8: both hands gather the same bundle at center-front.
4. Key 4: both hands retain that gathered bundle as the tote moves into the left windup.

The return strip supplies the inverse ownership order rather than assuming an unexplained jump:

1. Key 6 -> key 8: both hands retain the bundle while the opened tote comes back to center.
2. Key 8 -> key 7: right hand lifts and remains the primary load owner while the left hand continues to support the lower bundle.
3. Key 7 -> key 3: the loop moves onto the shoulder before the left hand is absent; key 3 shows shoulder support plus the continuing right-hand grip.
4. Key 3 -> key 2 -> key 1: the left hand is already released, the right hand settles the supported strap, and only then does the exact neutral put the right hand back in the pocket.

These are structural endpoints, not evidence that the eventual spacing or timing will read continuously. They do, however, identify the hand retention/release and shoulder-support order that the original six-key packet omitted.

**Neighbor continuity decision: continue.** No required hand/strand-role transition remains uncertain in the supplied structural route.

### Superseding gate decision and residual risk

The transfer increment resolves the blocking finding recorded above. The earlier stop remains the historical decision for `structural-pass03`; it is superseded for the combined eight-key evidence by this result.

| Dimension for transfer increment | Decision | Evidence boundary |
| --- | --- | --- |
| Connected arm anatomy | **continue** | Distinct sleeve/cuff/forearm routes reach the retained top grip and visible lower-strand catch; source-key-3 arm pixels are replaced on their actual owners. |
| Attachment | **continue** | Both handle owners are covered by the hands at G and return to the same far-behind/near-front root ordering. |
| Outbound and return continuity | **continue** | Shoulder clearance, left-hand catch, two-hand gather, shoulder re-support, and release order are now explicit in clean neighboring keys. |
| Cycle-expansion gate | **continue** | The missing structural relationship is resolved enough to construct the planned cycle frames. This is not clearance of those future drawings. |

Best eligible structural checkpoint is now `transfer-study02.aseprite`. It may advance to cycle construction, where every new affected frame and join still needs static review. The flat sleeves/forearms are structural planes only; their material volumes, cuffs, folds, palette clusters, and silhouette polish remain for the material pass. Authored-speed motion, timing, smear benefit, alpha coverage across the completed sequence, return smoothness, Godot behavior, and user artistic approval remain untested. No continuous-motion claim is inferred from the neighbor strips.

---

## Final-cycle review — material 03 corrected candidate

This section reviews the completed 19-frame still sequence and the one focused correction prompted by the first final-cycle inspection. The retained pre-correction natives are diagnostic baselines, not selected appearance results: their custom F4–F6, F8–F9, and F14–F16 arms used visibly flat olive and orange planes, with blunt forearm-to-hand contours that did not carry the source keys' cloth and skin rendering. The pre-correction F9 smear also had a far-left rear-handle branch ending about five Manhattan pixels from the tote fabric. Those were concrete material and attachment defects; the first version was **revise**, despite its otherwise valid structure.

### Corrected evidence binding and source correspondence

- Corrected clean native: `source/tote-clean-material03.aseprite`, SHA-256 `b29bc145f3159044e29857501056cc2194aa11dc022f43d884482bdc469bb77e`.
- Corrected smear native: `source/tote-smear-material03.aseprite`, SHA-256 `c36f806b09e9898401a6ba6dc85ab543c40a0d3c0e519e752b5a516f715ace4f`.
- Focused comparison packet: `review/material03/packet/packet.json`, SHA-256 `6124ea7ffc8938772473cea6b537d6b83723f3930a3191586fb62b417ee83054`. I recomputed all 46 bound source and sheet hashes; none differed. The packet's visual and user-approval fields correctly remain pending.
- Actual MCP proof sheets inspected: `proof/material03-clean-sheet.png`, SHA-256 `28e85f4084275c906e514aecd902be939d4fe2924dd528f7f4858f35fec9d0b6`, and `proof/material03-smear-sheet.png`, SHA-256 `c40c6a8a73ba5698274e0ce3f8f17f5ff93ccc1af705747b7ecd7cc4e279c56a`.
- Read-only native decoding found 19 frames on a 256x208 canvas, eight visible normal opaque layers, the declared timing `[180,100,90,80,100,90,130,50,50,90,70,100,90,100,100,100,110,100,500]`, and total 2,230 ms in both corrected natives. Every decoded composite is pixel-equal to its corresponding proof-sheet crop.
- Compared with the retained baselines (`tote-clean.aseprite` SHA-256 `7ae3ae3a6168a66670d32bf4f95c0a222b73ca042ed8e257f1f2447f7c0f0d41`; `tote-smear.aseprite` SHA-256 `e9645c42f8eb0174525ca0e2aca24271229d70bef2f69bca21b4d4716eb8aa6a`), the clean candidate changes only jacket/sleeve and hand/forearm cels in F4, F5, F6, F8, F9, F14, F15, and F16. The smear candidate changes those same 16 cels plus the F9 rear-handle cel. Timings and all other cels are exact.
- Corrected clean versus corrected smear differs only in F9 and only on the rear-handle, tote-body/rim, and near-handle/seam owners. F9 head, jacket, shirt/neck, hands, and legs remain the clean control. All other frames are exact between variants.
- Across the corrected smear sequence, alpha remains binary and all 248 used RGB colors are members of the canonical `inputs/original-neutral.png` color set. F1 and F19 are pixel-exact copies of that original composited at `(60,8)`.

The durable packet directly binds the corrected smear native and smear sheet but not the corrected clean native/sheet. Their exact hashes are therefore recorded above. This does not make the inspected A/B correspondence uncertain, but a final combined delivery packet should include both variants rather than relying on review prose for the clean half.

### Material and hand-form correction

The focused pass supplies the requested gain without replacing the approved pose construction.

- In `review/material03/material-before-after.png`, the olive sleeves now carry oriented dark seams, fold clusters, and lighter ridges that turn around the authored upper-arm directions. The underlying silhouette and shoulder/elbow routes remain recognizable; the treatment no longer reads as a uniform pasted plane beside the more densely rendered source-key torso.
- The hand/forearm owners now taper from forearm to wrist and use separate palm, thumb, finger-edge, and overlap clusters at the same grips. Their unique visible RGB counts rise from 3–4 before correction to 16–23 after correction on the eight affected frames, while opaque owner area generally decreases because the former blunt tubes were narrowed. These counts only corroborate the visible change; they are not the reason for acceptance.
- The actual owner/hide sheets show jacket-to-skin overlap at every affected pose and hands above both handle owners at the gathered grip. Readback finds 168–295 shared owner pixels between jacket/sleeves and hands/forearms, 11–80 between rear handles and hands, and 15–102 between near handles and hands across the eight affected frames. In the clean composites the cuffs cover the proximal skin, the wrists emerge, fingers cover the gathered strands, and the strands reappear below before reaching the bag. There is no exposed shoulder-to-hand gap or surviving flat source forearm on another owner.
- F4 and F16 retain the high right-hand strap grip and left-hand lower-strand catch; F5/F15 retain the centered two-hand gather; F6/F8/F14 retain two separately approaching wrists; and F9 retains both hands pulling the outbound bundle. The correction changes rendering and modest wrist contours, not hand-role order.
- The corrected custom frames are still somewhat simpler than the densest source keys (for example, the source-guided F7 hands use 45 RGB values while affected corrected hands use 16–23). At native size the new clusters nevertheless read as the same pale skin and olive cloth rather than a material switch. Whether that remaining density change flickers at 50–100 ms is a playback question, not something these stills establish.

**Material/shading decision: continue provisionally.** The correction is a visible improvement over the rejected baseline and I found no new identity, silhouette, grip, or palette-role regression in its allowed region.

### Prop attachment, smear, and neighboring poses

- At corrected smear F9, the new far-left root is `(160,99)`. The actual rear-handle owner has opaque `#DFB39B` there and the tote-body owner above it has opaque `#795246` there; with rear handle below body/rim in native order, the far strand now ends under fabric instead of in open space. The obsolete branch is absent in the isolated owner view.
- The clean F8 -> smear F9 -> clean F10 stills preserve the same two-hand pull. Only the bag and its rear/near straps elongate at F9; head, torso, hands, grip, and both lower-body supports are the clean control. F10 immediately restores the normal tote construction for contact. This is correct authored-smear ownership, but its perceptual benefit over the clean F9 has not been observed at speed here.
- On the return, corrected F14 -> F15 -> F16 visibly carries the tote inward, centers the bundle, then lifts it toward the shoulder while keeping the same rear-behind/near-front ordering and the corrected cuff-to-finger path. The already cleared F16 -> F17 -> F18 -> exact F19 settle route remains pixel-unchanged outside the corrected F16 arms.
- The front/right lower-body owner is pixel-identical through F8–F13, and the rear/left support component is pixel-identical from F13 to F14. That evidence contradicts a whole-body-slide or newly floating-support diagnosis from a global bounding-box row alone. The custom step drawings do lift the intended moving sole, but still images cannot establish the weight transfer's timing.

**Attachment decision: continue. Static-neighbor decision: continue. Smear decision: eligible for playback comparison.** No known still-frame attachment defect remains after the root repair.

### Proportion, identity, and head/neck joins across the cycle

The rigid canonical head, broad denim proportions, pale shirt, olive jacket, and cream tote remain recognizable across all 19 proof-sheet frames and against the approved scene/close-up and source-pose comparison. F1/F19 preserve exact entry/return identity; the action frames change body lean and stance without rescaling the head or expanding the character to fill the larger action canvas. The actual head and shirt/neck owners overlap in F2–F18; at the exact original F1/F19 they directly adjoin at one pixel. I found no exposed neck hole, doubled source neck, or collar discontinuity in the current composites.

The face is deliberately rigid, so this review does not claim expression animation or that every head translation will feel natural at speed. It establishes only that the still-frame identity anchor and neck/collar attachment remain coherent.

**Proportion/identity decision: continue for provisional playback.** No still-frame proportion or join contradiction blocks presentation.

### Final gate and residual evidence risk

| Dimension | Decision | Evidence boundary |
| --- | --- | --- |
| Proportion / identity | **continue** | Exact original entry/return, rigid canonical head, shared 183 px scale, coherent neck/collar joins, and source-guided stances hold in the 19 stills. |
| Grip / prop attachment | **continue** | Corrected cuffs, wrists, fingers, both handle owners, rear-behind/near-front roots, and F9 far-root coverage are visible on actual owners. |
| Static neighboring poses | **continue** | Launch/contact and gather/re-shoulder sequences preserve hand roles and support registration when inspected as still neighbors. |
| Material / shading | **continue provisionally** | The focused pass removes the visible flat-sleeve/flat-forearm regression without changing protected owners; residual transition density must be judged in playback. |
| Smear construction | **playback candidate** | Only F9 prop owners deform and the normal construction returns at F10; stills cannot establish that the smear improves motion. |
| Technical scope / export | **continue** | Native structure, declared cel scope, timing, palette membership, binary alpha, and proof-sheet equality pass read-only checks. |
| Final artistic approval | **pending user** | Independent review does not select final art for the user. |

**Gate: there is no known blocking still-frame defect in `tote-smear-material03.aseprite`; it is eligible to be presented as the provisional playback candidate, with `tote-clean-material03.aseprite` as its A control.** This is not final animation approval.

The corrected material03 sequence itself was not perceived at authored speed in this review, and no continuous-motion judgment is inferred from proof sheets, neighbor panels, decoded durations, or runtime event counts. The existing `review/tote-*.gif`, `review/final_clean-v-smear-*.gif`, individual `exports/*.png`, and prior Godot captures were produced from the pre-correction natives unless separately regenerated and hash-bound; they must not be presented as playback evidence for material03. The next owner should export/reopen the two corrected natives into actual authored-speed A/B playback, run the corrected smear candidate in Godot if gameplay validation is claimed, and then obtain the user's visual selection. Existing pre-correction runtime evidence remains useful only for the older artifact's execution boundary.
