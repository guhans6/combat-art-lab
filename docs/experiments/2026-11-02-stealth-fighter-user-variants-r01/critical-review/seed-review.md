# Independent seed review — 2026-11-02

Scope: review-only gate before native assembly. Reviewed the five complete supplied images, original face crops, each unmasked native-size source transfer, `face-review.png`, `source-mask-review-3x.png`, `review-seed.png`, `raw-unquantized.png`, `raw-seed.png`, and `source-spatial-mask-native.png` for U01/U03/U04/U05. The boards include matched 152 px preview and native-size 3× views; gamma-brightened diagnostic board copies in this folder help reveal source/mask boundaries and are not delivery art. Input/source mappings and role distinctions are in `intake.md`.

## Reviewed seed hashes

- U01: `native-work/variant-01/raw-seed.png`: `69a26877207b2a12b2327049a0b04b4bfe815476935cd74f30194a00f2c8c292`
- U03: `native-work/variant-03/raw-seed.png`: `8f247e5f351064a682984107409e7c54737316f1681495ad4fc2f7137add3949`
- U04: `native-work/variant-04/raw-seed.png`: `577228f388bd82ae5be5c07511afb936a7b08698c824780c651e02c01d4d8ac9`
- U05: `native-work/variant-05/raw-seed.png`: `5e10ac0470f28f722f399b26b029086989b8001c11fe52d2582b27a9d4650c5d`

## Source fidelity and positive evidence

All four retain the right-facing profile, separately placed feet, tied hair mass, near shoulder and forearm armor, rolled sleeve, indigo hanging cloth, waist wrap and sword hilt. U01 keeps its quiet face; U03/U05 retain a darker facial mark at native (73–74,27) and their own eye/brow-area treatment; U04 keeps its brighter, coarser light planes and dark face mark. A pixel-grid reduction cannot preserve all fine stubble and detail at 152 px. No artistic preference or user approval is implied by these observations.

An RGBA comparison of the U03/U05 seeds found 154 changed pixels entirely in native `x35..65, y48..64`, matching the shoulder-cap distinction; their spatial masks are identical. The unquantized pair's 178 changed pixels are also confined to `x34..65, y48..65`. Outside that region these paired seeds are pixel-identical. This does not alone establish face or mask quality.

## Source-backed repair needed before seed clearance

The four masks remove some real rear-hair clusters; on a light matte this opens obvious pale slashes through the locks. Coordinates are in the native 128×264 grid:

- U01: e.g. `(42,37..39)` and `(43,36..39)` show warm dark source-hair pixels but are transparent in the seed.
- U03/U05: e.g. `(43,40)` source RGB `#322b29` and `(41,42)` `#2d2425` are hair pixels removed inside the manually declared opening; nearby source background is approximately `#14151b`. Apply the same fix to both because the supplied originals are identical there.
- U04: e.g. `(35..39,39..42)`, `(41..42,38..41)`, and `(40,42..43)` contain source-colored hair in the original transfer but include deleted seed pixels. Inspect the full source within these rectangles; the whole rectangles are not blanket fill instructions.

The source background is also visibly retained as dark outer bands in places. U01 at `y70, x77..80` is opaque in the seed although its RGB is approximately `#111217`–`#121317`, matching source background immediately outside `x81..86`; the blue shirt ends at x74 and source dark edge is nearer x76. U01 at `y220, x79..81`, U03/U05 at `y220, x80..83`, and U04 at `y220, x79..81` similarly include opaque source-background-like pixels. Inspect continuous contours against the unmasked source; do not erase all dark pixels by color. Conversely, U03/U05 at `(75..76,60)` and U04 at `(75,60)` are transparent despite warmer, darker source edge pixels and deserve a local collar-edge check.

Disposition: **U01 hold**, **U03 hold**, **U04 hold**, **U05 hold** until corrected outputs are inspected. Check actual resulting masks on light/dark mattes, ensure intentional hair gaps and sword/hand/boot attachments survive, then repeat the shared U03/U05 outside-shoulder pixel comparison. The requested corrections are bounded alpha/source correspondence fixes, not preferences about style, palette, or design.

## Evidence boundaries

These are prepared raster seeds, not final native masters. No fresh native save/reopen, semantic owner edit, final transparent export, or Godot playback was inspected in this review. The user has not selected a variant. No animated motion was viewed or inferred. The sprite artist owns the source-guided correction; this reviewer will inspect the exact new checkpoint before native assembly clearance.

## Pass01 re-review and assembly gate

The producer retained pass00 and updated the same seed paths. Reopened the revised unmasked-source/mask/seed boards, face comparisons, light/dark mattes and 152 px previews for each variant. Source hair is restored where reviewed slashes cut through locks; U04 retains a visible loose loop. The reported collar samples are restored and broad background-like contour bands are visibly reduced. Profile, brow/eye-area distinctions, source-specific lighting, sword, hand and two boot shapes remain intact in the reviewed views. At 152 px some fine face and hair information is inherently quieter than in the original and the two shoulder options are subtle; these are source/scale comparison limitations, not grounds to exaggerate either design.

Fresh pass01 seed hashes:

- U01 `d215a555877e4eb780286f0a0c381fe8da64064eb18a9ea69ac822f19bea9e59`
- U03 `0220aa72378042619ac5d8641a0c881473c39ef5fbac3eaac7152cd7afa150d7`
- U04 `0a5e54696e0d95e753e21b9c863323ea28eec7e8a66955b1f17ce88db7d8dea4`
- U05 `3a4f3185f55bcbda220ede8ba57e302180bf064e5fc28c55ff90e4ce80b8e253`

The four alpha bounds remain `y13..252` inclusive (240 px). The specific flagged hair/collar points are now opaque and the flagged background samples transparent. U03/U05 masks remain byte-identical as decoded RGBA; their 154 RGBA seed differences are confined to `x35..65, y48..64`, the source shoulder-cap region. No additional concrete source-backed blocking defect was found during this bounded re-review. **U01, U03, U04 and U05 are cleared to proceed to native assembly.** The clearance is not a final visual selection, user approval, native reopen/edit proof, Godot playback, or animation judgment. The final native exports still require inspection against these seeds and originals.

The pass01 recipe SHA-256 values, in U01/U03/U04/U05 order, are `761efc38c370aa2aae04d88009463a0e7e5736dbf91f714432067ed27cce0eb0`, `a2a5e9b905b30ab98656580435aa4bfc17ce07cce3fce91c2af94bf304f404b3`, `a1c88ec24afdea30445a961259bdb46fa09f147b5af650fe301092ded61b5684`, and `1ede888bc289c0b45ef1b1e7da92568c8b4f4ec7885182bb0433f3459384729c`. Their `source-spatial-mask-native.png` SHA-256 values are `1634a7ed99395d4fa7889c64692166fd284b09bfc8311b5302085296c3037755`, `65d15efdf0e50f992c6b469c6494fee2dbd17729ac67c53adb67761186100fe7`, `4090ef986539f1cf5533fad51a8c9bd9f53eb02e5be5cd8b9fd672c4a539df5f`, and `65d15efdf0e50f992c6b469c6494fee2dbd17729ac67c53adb67761186100fe7`. The individual source-mask boards are bound respectively by `808c5ae52c61b908e84a31eb000e58b95a6056b05fe616094aea7a6488877ea1`, `33a12417012111bfb45d4a28634280b6a73c3e7be1829fb48116b4b122d2df01`, `b6e5733198f22c2ed830818d60a6707435e1d0a62e78c5b02e6019649b4f7f16`, and `3919c9efe35b4e959efb1a37882046bcdd85b2b9b2f0256308370c4bf198aabb`. Recipe and seed hashes above cover the pass01 palette and mask work reviewed at this gate; later changes require new review.
