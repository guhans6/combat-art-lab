# Luna 6 Max — quiet breathing idle candidate

## Result and status

Constructed an editable native Aseprite candidate from the common frozen neutral input.
The animation is a 10-frame, 128×192 RGB `idle` cycle, total 2,390 ms. It uses a
restrained upward-and-return shift of the shirt's existing fold plane, with the
permitted inherited blink in its final three frames. The movement is subtle at full
body scale; it has not been observed at actual playback speed. This is a playback
candidate for user review, not an approved production asset.

- Native source: `idle-candidate.aseprite`
- Ordered transparent MCP exports: `frames/idle-00.png` through `frames/idle-09.png`
- 1×/3× neutral-matte GIFs: `exports/idle-neutral-1x.gif`,
  `exports/idle-neutral-3x.gif`
- Full-body and torso contacts: `reviews/full-contact-1x.png`,
  `reviews/full-contact-3x.png`, `reviews/torso-contact-1x.png`,
  `reviews/torso-contact-3x.png`
- Native operations/grids: `ops/mcp-operations.json`; sequencing and observed calls:
  `ops/session-log.md`
- Manifest: `delivery.json`

## Independent decisions

I used the character anchor to keep tied brown hair, three-quarter face, open olive
jacket, pale shirt, wide blue jeans, cream tote and pale shoes. The native source pose
is provisional, so I preserved its exact neutral rest drawing as frame 1 and kept
outer silhouette, head, shoulders, hands, tote, strap, legs, shoes and root fixed.
There is no new shading or palette color.

The one construction pass lifts the existing rose-gray fold and pale highlight inside
the shirt by one pixel, in nested groups through frames 2–4, then lets them settle
through 5–6. This is a small cloth-plane breathing cue; it does not translate the
character or move the outer torso contour. The actual native diff bounds remain in
`verification/native-comparison.json`:

| Frame | Duration | Pose |
| --- | ---: | --- |
| 1 | 600 ms | Exact neutral rest |
| 2 | 180 ms | First shirt-fold lift |
| 3 | 180 ms | Fold lift extends |
| 4 | 360 ms | Peak hold |
| 5 | 220 ms | Fold settles |
| 6 | 220 ms | Return step |
| 7 | 450 ms | Exact neutral rest |
| 8 | 50 ms | Source blink frame 5 |
| 9 | 80 ms | Source blink frame 6, closed eye |
| 10 | 50 ms | Source blink frame 7 |

The blink source's face/neck layer is pixel-identical to neutral in frames 5–7. The
eye changes are on `08-hair-tie-and-hair`, so only that region was transferred.
The 13/26/13 changed eye pixels match source frames 5/6/7 exactly. Original named
layer order/properties and hidden guide remain intact. No layer was added.

## Evidence used

- `clip-01-core-poses`, 05:09: the two-state inhale/exhale and ten-frame process
  informed the independent timing choice. The tutorial character and pixels were not
  copied.
- `clip-02-chest-subpixel`, 07:05; transcript `transcript-072`–`074`: the idea
  of easing an existing shirt plane across several tones informed the fold-lift pass.
  Its palette and exact timing are unavailable.
- `clip-03-arms-delay`, 10:26; transcript `transcript-103`–`107`: both hands are
  in pockets here, so the hands and tote attachment remain fixed.
- `clip-04-hair-settle`, 12:22; transcript `transcript-117`–`118`: no hair-settle
  motion was adopted; only the allowed eye blink is used.
- `clip-05-leg-shading`, 14:40; transcript `transcript-134`–`139`: jeans and
  shoes stay fixed to protect the planted stance.
- `clip-06-breathe-tag`, 16:04; transcript `transcript-146`–`154`: the source's
  13-frame tag was not copied; this candidate has its own ten-frame tag and holds.

I inspected the referenced stills and filmstrips, not the video at actual speed. The
source pack concerns another character, uses re-encoded editor footage and automatic
speech transcription, and does not supply the source project, palette, or exact cel
timings. Those limits are recorded with source hashes in `observations.md` and
`prep/video-frames/index.json`.

## Verification

- `verification/native-comparison.json`: passed. The candidate has the same 128×192
  canvas and 12 named layer definitions/order; the hidden guide is preserved; frame 1
  matches baseline cels; only the shirt fold in frames 2–6 and eye pixels in frames
  8–10 differ. Timing, tag and tag user-data chunks are recorded there.
- `verification/export-check.json`: passed. All ten fresh-reopen PNGs match both the
  pre-reopen MCP exports and native cel composites. Frame 1 is pixel-identical to
  frozen `inputs/neutral.png`. Every frame has 16,732 transparent pixels, 7,844
  opaque pixels, zero partial-alpha pixels and 249 unique RGBA tuples.
- `verification/gif-check.json`: passed. The 1× GIF is 128×192 and the 3× GIF is
  384×576. Each has ten frames and preserves the 2,390 ms timing after hold
  coalescing. Decoded visible pixels and the 249-color matte-composited palette are
  exact; no GIF quantization drift was found.
- `verification/local-revision.json`: passed. In a separate scratch-native proof,
  reopening a saved revision changed exactly editable pixel (12,3), left the
  protected layer unchanged and produced a fresh PNG equal to the native composite.
  It is not part of the character art.
- The tool inventory had no `validate` action. These focused parser/export checks do
  not substitute for the plugin's unavailable validator.
- No Godot import/playback, engine version, game-scale review, actual-speed playback,
  user visual selection, or production approval is claimed.

Aseprite added the idle animation tag and its olive user-data color. The official
[Aseprite file-format specification](https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md#user-data-chunk-0x2020)
identifies chunk `0x2020` as user data. `sprite_info(includeSlices=true)` reported
no slices. The first-frame header speed follows the new 600 ms hold; source timings
are separately listed for every frame.

## Next owner

The parent can include this candidate in the independent four-way comparison. User
visual review should decide whether the deliberately small fold-only breath cue reads
clearly enough at the intended gameplay size. Godot integration, user selection and
production approval remain out of scope.

