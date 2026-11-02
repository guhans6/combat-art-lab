# Independent final static review — 2026-11-02

## Scope and evidence

Each `native-work/variant-NN/static.png` was opened directly at its 128×264 native canvas, at 3× nearest-neighbor on a light diagnostic matte (`final-light-NN.png` here), and as an approximately 152 px body-height preview (`final-display-NN.png` here). The exact full original, face crop, unmasked native source transfer, and source-mask comparison were inspected for the corresponding variant. Recipe/seed/mask and all seed-review observations are hash-bound in `seed-review.md`. These are held-rest stills, not motion tests or artistic approval.

| Variant | Native SHA-256 | Final export SHA-256 |
| --- | --- | --- |
| U01 | `6edf22ccca5e5ecc53caaa55f577b201d829153ff8430e391a9be13d44b7c002` | `f5ddce534af241fe3e60591ace51a404330a246b22e240a761c67d67d0cc78a5` |
| U03 | `7cf57a3fe73afc2b9531c6c8ec3ead8ae030b664a4dd0f078ef9ba7e03879a26` | `46ed03b35b3a2be0adff758eddedc8fd5f13b78c829bab86aaf43d6165d73df6` |
| U04 | `bbbffc7131e79e7e129375fea984a59f41fb666be42e00e4bd36b7547f6ebf29` | `7061de0b0a11fc26ee0792cf590313874ec47e5ec46d71e465344c4992e8dea2` |
| U05 | `4a361b5f7b994b5a8c58a0df0aa70441bf331a3b27c2d08d4c4dc7a5449343b6` | `a7ca6984874b4ba667ece4d99da2e5c6fec54b4b2760f31ead7625273ed84c6e` |

## Source fidelity, expression and color

- U01: quiet profile, warm tie, long hair, broad gray-brown shoulder plane, dark sleeve folds, indigo sash, sword and two boots read consistently with its original. It is intentionally quieter in the eye area.
- U03: the longer shoulder cap, distinct upper-arm guard, brow/eye-area cluster, warm ear/skin and textured dark hair survive. Some high-resolution stubble and face marks are necessarily subtler at the comparison display size.
- U04: retains the chunkier angular light planes, comparatively brighter skin and face mark, loose-hair loop, sleeve folds and trouser shapes of its own source. Its look remains visibly distinct from U01/U03.
- U05: matches U03 everywhere except the short shoulder cap, consistent with the supplied sources. This difference is subtle at 152 px; enlarged views support the choice without exaggerating the source.

The steel-gray/brown shoulder material does not visually become skin-colored in the final previews. For an additional narrow diagnostic, opaque native-grid shoulder (`x40..64,y52..63`), face (`x67..74,y27..35`), and arm (`x36..44,y96..102`) output pixels were compared to the corresponding unmasked nearest-neighbor source transfer. The mean absolute RGB channel difference was approximately 0.9–1.4 out of 255 across the per-variant regions; e.g. U03's dominant sampled shoulder output `(69,58,54)` remains distinct from its dominant face output `(123,83,61)`. These statistics diagnose this palette-mapping concern only; they do not establish visual quality or faithfully compare every source pixel.

## Alpha, attachments and grounding

On light matte the repaired rear-hair slashes are absent and the U04 hair loop remains. The face edge, near arm and hand, far hand, waist wrap, sword hilt and guard, sash, leg gap, and distinct soles remain present. Previously flagged broad background-colored edge bands are reduced. The 240 px visible body spans native y13..252 inclusive for every static; both shoes share the declared ground line. No further concrete source-backed blocking alpha/attachment defect was found in this bounded inspection. The dark source images make some hair-edge/background distinctions uncertain, so this judgment is limited to the reviewed stills and mattes.

## Technical evidence and boundaries

Independently decoding the final export, producer-provided `reopened.png`, and repaired `raw-seed.png` to RGBA gives identical pixels for each variant. The exported and reopened PNG files are also byte-identical. Each final PNG has binary alpha, 64 visible RGB colors, a 128×264 canvas and a 240 px vertical alpha bound. U03/U05 final PNGs differ in exactly 154 RGBA pixels within native `x35..65,y48..64`, and their spatial masks remain identical. These checks verify exports and recorded reopen outputs, but this reviewer did not independently operate the native editor, inspect hidden native-layer ownership, or execute the producer's separate local-edit proof.

**Disposition:** all four static exports are cleared for the requested human comparison; no final design or aesthetic winner has been selected. Actual Godot scene rendering, project integration, producer local-edit proof and user visual approval are separate evidence boundaries owned by the integrating agent and user. No continuously perceived animation was reviewed or inferred.

## Later U04 coverage finding

After the review above, the producer's focused coverage audit identified two enclosed transparent points in U04 hair and a four-pixel source-background slit at `(64,180..183)`. The latter is already eight-neighbor connected to the leg gap but not four-neighbor connected. Direct source-grid inspection shows adjacent `(63,183)` is source background `#0e0d15`, directly connecting `(64,183)` to the already transparent `(63,184)`; nearby `(64,184)` is source-colored trouser and should remain. Producer is correcting the two hair points and that one background bridge. **The U04 hash and clearance above apply only to the earlier checkpoint and require fresh review of the new U04 export.** The other three variants remain hash-bound as above.

## U04 repaired export re-review

The new actual U04 export was reopened visually at native size, 3× on a light matte, and approximately 152 px body height. Decoded RGBA differs from the earlier U04 checkpoint at **exactly three pixels**: restored hair at `(50,25)` and `(36,50)`, and cleared source background at `(63,183)`. A four-neighbor traversal from `(64,180)` now reaches the exterior, and the nearby source-supported trouser remains opaque. The new PNG has binary alpha and decodes identically to the updated seed and producer reopen export. No visual regression appeared in the bounded source comparison.

The replacement U04 native SHA-256 is `9ea53943404b207b860d1022c0b48ff7bce6e939ed4b591f66017a6001953089`; replacement final/reopened PNG SHA-256 is `341b01e5bdbfb77bd796eb2e022dc49c7636442c3b7d9a144d77afb110e1266b`. Updated seed SHA is `7a695488460dd505b4078f631bbdeb6498a98be58ecbe5236e14cbe33bcc1fb8` and source-spatial mask SHA is `392ec122a5bf67e41e3e3a5482a6dfb1dcdfe2ce1c3285b61025ba03d70c2821`. The original recipe hash did not change; the final recorded construction must include the three point overrides or use the updated mask and native draw operations so it does not imply the earlier polygon alone produced the current mask. **U04 is again cleared for the bounded user comparison on this new exact export**, subject to the same native-edit/engine/user-approval limitations.

## Independent inspection of selected edit-proof exports

For U01, U03 and U05, the producer's duplicate edit proof changes 24 RGBA pixels within native `x40..42,y111..122`, all inside the supplied proof mask, and changes no alpha. The proof PNG exactly matches the producer's reopened proof export after RGBA decoding; the bracer highlight is visible when the proof is viewed. This demonstrates a localized visible composite edit on the duplicate. It is not a direct independent audit of hidden layers or a production appearance request. The U04 proof must correspond to the newly repaired master and remains pending producer completion.

The rebuilt U04 duplicate proof has now also been compared against the repaired U04 master: 24 changes, all within the supplied proof mask, with no alpha changes, and its PNG decodes identically to the reopened proof PNG. The same visible-composite and reopen conclusion thus applies to all four variants; hidden-layer preservation remains a separate producer/native audit.

## Godot scene capture inspection

Inspected the actual scene captures `check-project/evidence/set-1.png` and `set-2.png`, the dedicated `armor-pair.png`, and the crop board `lead-review/five-looks-152.png` on 2026-11-02. The board SHA-256 is `8db855a35445b27094d57f3c5152426d5268c40c768a867718205ed682eb9433`; the armor-pair screenshot SHA-256 is `bb83faba1d3b95e1cf6c7cf0815518d51bba9c8807f2f1e5196e000424e1ba5a`. They show Current A and all four supplied looks in the same dark purple room, with the soles placed on the floor and no conspicuous rectangular source backgrounds. The warm face/hand, armor and indigo cloth remain visible in context; U04's brighter, chunkier planes read most clearly in these still captures. The U03/U05 shoulder difference is small at 152 px, consistent with their small source-only difference. No visual winner is selected, and static captures do not establish animation quality. Runtime measurements, control behavior and error checks are owned by the integrating agent and are not independently certified by this visual inspection.

## Final native ownership and local revision review

The producer subsequently corrected native-only ownership; the output images stayed unchanged. The **native hashes in the table above now refer to the final corrected files**, superseding the earlier pre-ownership hashes described chronologically in the U04 section. I inspected the six isolated native-owner contact panels for all four variants. The shoulder caps now sit with torso/armor instead of the head/hair owner, and the far-hand owners consist of the actual warm skin rather than adjacent indigo hanging cloth. The visible-only owners are useful for localized revision, but have no inferred hidden surfaces and are not presented as a movement-ready rig.

An independent read of the actual final native files with `tools/check_native_pilot.py` reassembled all six disjoint visible layers into the actual final PNGs, which also match the pre-ownership and producer-reopened composites exactly. In the U03/U05 native files all 154 differing pixels are on `torso-cloth-armor`; the other five corresponding native owners are identical. For each final master, independently comparing the protected native layers and frame metadata against its refreshed duplicate edit proof passed: 24 visible bracer pixels changed within the declared mask and layer, with no changes to protected native content, and the proof PNG equals the reopened proof PNG. This independently verifies the native-reader and export evidence, not an independent editor session or moving-part coverage.

The complete machine-readable report is `ownership-audit.json`, SHA-256 `d59f18b26f0d2da18204566ab7a6b972cd9013dccdd88db06b33230e95c81bc6`; it was produced by `check-ownership.py`, SHA-256 `aca1f9ae0b9db576183341b61ded8c5af135d1bc0fc98db76fe368d2ad063865`. This gate clears the inspected native ownership and local-edit scope for the requested still comparison. User visual selection and any animation or final game-art approval remain pending.
