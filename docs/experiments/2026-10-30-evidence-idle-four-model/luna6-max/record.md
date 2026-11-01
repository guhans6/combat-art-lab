# Luna 6 Max — quiet breathing idle candidate

## Result and status

The final candidate is an editable 10-frame, 128×192 RGB Aseprite `idle` cycle,
2,390 ms long, derived from the shared frozen neutral source. Pass01 remains saved
unchanged as `idle-candidate.aseprite`; the selected final is a separate native,
`idle-candidate-corrected.aseprite`, with one bounded shirt-fold correction at the
inhale peak. It retains the neutral rest drawing, planted silhouette, original layers,
palette, hidden guide and inherited 50/80/50 ms blink. This remains a playback
candidate for review, not an approved production asset.

- Final native: `idle-candidate-corrected.aseprite`
- Ordered fresh-reopen exports: `verification/fresh-reopen-corrected/idle-00.png`
  through `idle-09.png`
- Exact-palette 1×/3× GIFs: `exports-corrected/idle-neutral-1x.gif`,
  `exports-corrected/idle-neutral-3x.gif`
- Corrected full-body and torso contacts: `reviews-corrected/`
- Pass01 native, exports, reports, record and original hash manifest remain separately preserved.
- Correction operation: `ops/mcp-correction.json`; pass01 drawing history:
  `ops/mcp-operations.json`; session chronology: `ops/session-log.md`
- Manifest: `delivery.json`; preserved pass01 manifest: `delivery-pass01.json`

## Independent decisions and correction

I used the approved character anchor for the tied brown hair, three-quarter face,
open olive jacket, pale shirt, wide blue jeans, cream tote and pale shoes. The native
source pose is provisional, so the original neutral drawing is retained as frame 1.
The body silhouette, head, jacket contour, hands, tote, strap, legs, shoes and root
remain fixed. No palette color or layer was added.

Pass01 animates a small existing rose-gray fold and pale highlight inside `03-shirt`
through frames 2–6. My full-body review showed the cue was subtle. In the single
allowed correction pass, I lifted the existing two-pixel rose-gray crease by one
pixel at inhale peak F4, exchanging two cells at y=54 for the same two cells at y=53.
The correction uses the existing `#d6b7bb` and `#fde4cc` palette colors. It changes
only four values in F4 on `03-shirt`; no contour, outer silhouette, timing, or rest
pose changed. The proof in `verification/correction-check.json` confirms the bounded
diff and the unchanged pass01 hash.

| Frame | Duration | Pose |
| --- | ---: | --- |
| 1 | 600 ms | Exact neutral rest |
| 2 | 180 ms | First shirt-fold lift |
| 3 | 180 ms | Fold lift extends |
| 4 | 360 ms | Peak hold; upper crease lifted one pixel |
| 5 | 220 ms | Fold settles |
| 6 | 220 ms | Return step |
| 7 | 450 ms | Exact neutral rest |
| 8 | 50 ms | Source blink frame 5 |
| 9 | 80 ms | Source blink frame 6, closed eye |
| 10 | 50 ms | Source blink frame 7 |

The blink source's face/neck layer is pixel-identical to neutral in source frames
5–7. Its 13/26/13 eye changes are carried by `08-hair-tie-and-hair` and match the
source frames exactly. All 12 existing layer definitions and their order/properties
are preserved; `added_layers` is empty.

## Evidence used

- `clip-01-core-poses`, 05:09: two inhale/exhale states informed the independent
  ten-frame timing plan; the tutorial character and pixels were not copied.
- `clip-02-chest-subpixel`, 07:05; transcript `transcript-072`–`074`: easing an
  existing shirt plane across several tones informed the fold movement.
- `clip-03-arms-delay`, 10:26; transcript `transcript-103`–`107`: both hands are in
  pockets, so hands and tote attachment remain fixed.
- `clip-04-hair-settle`, 12:22; transcript `transcript-117`–`118`: no hair motion was
  adopted; only the allowed eye blink is used.
- `clip-05-leg-shading`, 14:40; transcript `transcript-134`–`139`: jeans and shoes
  remain fixed to protect the planted stance.
- `clip-06-breathe-tag`, 16:04; transcript `transcript-146`–`154`: its 13-frame tag
  was not copied; this candidate uses its own ten-frame tag and holds.

I inspected the selected frozen video stills and their filmstrips, not actual-speed
playback. The pack concerns another character, uses re-encoded editor footage and
automatic speech transcription, and lacks the original source project, palette and
exact cel timings. Source hashes and excerpt observations are in
`observations.md` and `prep/video-frames/index.json`.

## Verification

- `verification/native-comparison-corrected.json`: passed. Canvas is 128×192;
  original named layers/order and timing are intact; only the permitted shirt region
  in F2–F6 and source eye pixels in F8–F10 differ from neutral.
- `verification/correction-check.json`: passed. The corrected native differs from
  pass01 in exactly four `03-shirt` pixels at F4. The original pass01 SHA-256 remains
  `a84f1336358155a22831ab539f24c3bf82ff1b190dfd6818eda0db0ea63e54e8`.
- `verification/export-check-corrected.json`: passed. Each pre/post-reopen MCP PNG
  is byte-identical and matches the native composite. Frame 1 exactly matches the
  frozen neutral PNG. Each frame has 16,732 transparent and 7,844 opaque pixels,
  zero partial-alpha pixels and 249 unique RGBA tuples.
- `verification/parent-compatibility-corrected.json`: passed the parent's bounded
  delivery audit on this candidate alone. It confirmed exact native/export and GIF
  timelines, preserved shoes/hidden guide and layer metadata, binary alpha, and no
  new enclosed body holes. One inherited source hole at `(63,116)` remains.
- `verification/gif-check-corrected.json`: passed. The 1× GIF is 128×192 and the 3×
  GIF is 384×576. Both preserve the 2,390 ms visible timeline and exact
  matte-composited pixels across ten frames.
- `verification/local-revision-actual-native.json`: passed. A separate saved copy of
  the final animation native was freshly reopened after exactly one local edit at
  F4, `03-shirt` (x=60, y=53); the delivered native hash stayed unchanged, and the
  fresh PNG matches the revised native composite.
- Pass01 checks and hash manifest remain in `verification/native-comparison.json`,
  `verification/export-check.json`, `verification/gif-check.json` and
  `verification/local-revision.json`.
- Preflight listed a `validate` feature, but the callable MCP inventory exposed no
  validate operation. The focused parser/export reports above do not claim that
  unavailable action.

No Godot import/playback, engine version, game-scale review, actual-speed playback,
user visual selection or production approval is claimed.

The Aseprite tag and its olive user-data color are present. The official
[Aseprite file-format specification](https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md#user-data-chunk-0x2020)
identifies `0x2020` as user data. Fresh `sprite_info` readback reported no slices.

## Next owner

The parent can compare this corrected candidate against the other independent
deliveries. User visual review should decide whether the restrained fold-only breath
reads clearly enough at the intended gameplay size. Godot integration, user selection
and production approval remain out of scope.
