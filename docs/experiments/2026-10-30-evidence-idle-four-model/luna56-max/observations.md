# Luna56-max independent idle study — observations and plan

Date: 2026-10-30  
Model assignment: `gpt-5.6-luna/max` (fresh-context independent artist)  
Experiment: `2026-10-30-evidence-idle-four-model`  
Status before lease: `prepared_not_executed`; no Aseprite MCP call or native mutation made.

## Frozen inputs and roles

- Native baseline: `../inputs/neutral.aseprite`, SHA-256
  `d76266fa8afcd1de643e6b6421ec4dfe4fa77f8044a1d083205b921eb2f25540`.
- Composite baseline: `../inputs/neutral.png`, SHA-256
  `e7c62ff0e2f3f88b10b17904322f834175e62d33579cc646a9e6396f940b57ad`.
  It is 128x192 RGBA with an observed opaque bounding box `(32,2)-(104,185)`;
  the offline inspection reports 7,844 opaque pixels and 249 visible RGBA values.
- Approved identity/style anchors inspected visually before construction:
  `../inputs/character-scene.png` (full standing figure in the dusk street) and
  `../inputs/character-closeup.png` (face, tied brown hair, olive jacket, pale
  shirt, wide blue denim, cream tote). They are appearance authorities, not
  frame sources.
- `../inputs/blink-source.aseprite` is an optional inherited blink source. I will
  not redesign the eyes or mouth. Blink inclusion remains a separate decision
  after the breathing keys are coherent.
- Native layer names observed from offline strings in the baseline are:
  `guide-source-seed (hidden)`, `00-shoes`, `01-denim`, `02a-jacket-left`,
  `02b-jacket-right`, `03-shirt`, `04-tote`, `05-tote-strap`,
  `06a-left-hand`, `06b-right-hand`, `07-face-and-neck`, and
  `08-hair-tie-and-hair`. This is read-only preparation evidence; native
  ownership and frame/cel metadata must be confirmed through Aseprite MCP after
  the lease is granted.

## Direct reference observations

The approved scene/close-up were opened as actual local images, not inferred from
older prose. The character faces three-quarter right with a shallow smile and
quiet, friendly expression. The tied brown hair is a large rear mass with a small
tie/loop and fringe over the forehead; the face and neck are warm peach against
the olive jacket. The pale shirt is a broad light plane under a dark olive collar;
wide blue jeans and cream tote are large stable masses. Feet are symmetrically
planted and the tote hangs on the character's right side. Fixed-lighting/material
identity is more important than adding motion texture.

The 4x nearest-neighbor offline view of the neutral export shows the same
three-quarter-right figure at the 128x192 study grid. The head, shoulders, jacket
and tote occupy the upper-body motion region; the denim and shoes form a large
stable grounding block. The baseline is an agent-provisional construction, so the
animation test must preserve its identity and palette rather than silently redraw
the face or costume.

## Frozen video evidence used

The pack is the local copy of the user-referenced AgentWatch evidence. Its source
hash is `c946289c8fc1ff74faf4fbc0206c58f2e1c9eebd37e18f595f5418e9b5e93a95` and
the evidence ZIP is recorded in the common brief. The source recording is
instructional evidence only; its exact native project, palette and per-cel timing
are unavailable. I use its motion ideas, not its character art or recording FPS.

Directly opened stills and bounded observations:

| evidence ID / local still | observation used here |
|---|---|
| `chunk-001-frame-021`, 05:00, asset SHA `12ad90029d1759a8971f0df6d897be7485116ec217e348699915a445762a349d` | Aseprite shows two adjacent small full-body cels on a checkerboard. The source demonstrates starting from a pair of breathing poses and a one-pixel-scale difference above the hips, but its character is not reused. |
| `chunk-001-frame-029`, 07:00, asset SHA `edb3b308ae4dd131797293146e536ca65d83e0f04de1d2e013e70bb08c891ff5` | Enlarged head/torso view with a 12-column timeline. Chest and collar pixels are intentionally stepped; the useful lesson is a short transition sequence rather than a rigid whole-sprite warp. |
| `chunk-002-frame-002`, 10:15, asset SHA `4e2f1fdb1c5f62312442c7c1e33932b12414c4f5273901dde3a48e908bf84f04` | Two full-body cels are visible. The hands/arms are distinct forms that can lag the torso slightly; this supports a small secondary delay without moving the planted legs. |
| `chunk-002-frame-011`, 12:15, asset SHA `0bcf1b44e4f2f3002dd9442218294f44bb836983b9117c96cdfbf5e65efe2683` | Enlarged head view shows a deliberately stepped hair mass and a detached curled strand above/right of the crown. |
| `chunk-002-frame-012`, 12:30, asset SHA `734ca07ea94ad449d29976460154fd88e28f6d96c9d28ae238936b1139fba0ab` | A later enlarged hair/head view keeps the large hair mass while exposing the small curl as a useful settling accent. |
| `chunk-002-frame-021`, 14:30, asset SHA `efc22b53263ad9e427876bce10bfea20ef5e5023437a647cd04ee63ab4833d0c` | Enlarged lower-body view shows the source's stated preference for changing leg shadow clusters while retaining the leg silhouette. This will be adapted conservatively to the blue denim, not copied as a redrawn lower body. |
| `chunk-002-frame-028`, 16:00, asset SHA `5e7e2d9726473aad10ea3bcb3a5ea7feb7a9df7844b719aedbb67ae20047e2b8` | The final source setup visibly has a `Breathe` tag and 13 timeline columns. This supports an authored named loop, but not a mandated 13-frame count or timing for this character. |
| `chunk-002-frame-032`, 17:00, asset SHA `9eb0665622a9e557c64895e83d546be3aab6544022f59c5d35d58b703cc661b4` | The reference is removed from the canvas; an isolated sprite remains on transparency with `Idle` and `Breathe` tags. This informs the export/cleanup proof boundary only. |

The evidence review also identifies the bounded source excerpts: `clip-01-core-poses`
(05:04–05:18), `clip-02-chest-subpixel` (06:54–07:20), `clip-03-arms-delay`
(10:14–10:32), `clip-04-hair-settle` (12:07–12:29), `clip-05-leg-shading`
(14:26–14:46), `clip-06-breathe-tag` (15:46–16:10), and
`clip-07-cleanup-and-export` (16:52–17:15). The prepared stills and review text
support the lesson; no exact source durations or editable source pixels are
claimed. Temporal naturalness of these source clips was not inferred from a
single still.

## Independent construction decision

Intent: an end-to-end native animation pilot from the frozen neutral source, not a
pure model ranking and not a copied tutorial reconstruction.

I will use a **six-frame quiet breath loop** with a 1-pixel upper-body travel and
small form-aware cluster edits. The neutral drawing remains frame 1 and the loop
return. The proposed timings are:

| frame | role | duration |
|---:|---|---:|
| 1 | exact neutral rest | 420 ms |
| 2 | early inhale: torso/chest begins, hands/tote mostly hold | 140 ms |
| 3 | inhale crest: upper body 1 px up, shirt/jacket volume accents | 180 ms |
| 4 | quiet crest hold, one delayed hair-curl/tote settle accent | 220 ms |
| 5 | exhale transition, torso returns before the small secondary parts | 180 ms |
| 6 | exact neutral rest / long seam hold | 560 ms |

Total loop: 1,700 ms. These timings are authored for this asset and are not
derived from the video recording FPS. If the native editor exposes the baseline
as a one-frame source, I will duplicate the cel/frame preserving layer order,
palette, hidden guide and exact rest pixels before changing any candidate cel.

### Per-part method and protection intent

- `00-shoes` and `01-denim`: keep silhouette, feet rows and waistband anchor
  fixed. A very small existing denim shadow-cluster adjustment is allowed only on
  frame 4 if the torso transition otherwise reads as a rigid cut; no leg redraw.
- `02a-jacket-left`, `02b-jacket-right`, and `03-shirt`: use explicit local
  contour/plane edits for the chest rise (collar/upper shirt highlight and one
  jacket shoulder step), rather than a blanket row-band warp. The outer jacket
  hem/waist overlap must be read back after every key.
- `06a-left-hand`, `06b-right-hand`: hold at rest through frame 2, follow the
  torso on frame 3/4, and return on frame 5. Preserve hand identity and pocket
  ownership; no facial or hand redesign.
- `04-tote` and `05-tote-strap`: let the tote lag the inhale by one key and settle
  one key after the torso. Keep the cream material ramp and strap path; change
  only the small hanging contour/overlap needed for the delay.
- `07-face-and-neck` and `08-hair-tie-and-hair`: move with the torso at the crest
  only if the native cel offset keeps the neck/collar overlap clean. Keep eyes,
  mouth and expression unchanged. A one-pixel detached-curl settle is preferred
  over a blink for the first pass; the inherited blink remains optional and must
  not become an expression redesign.

This gives one main construction pass. A single self-identified artistic
correction pass is reserved for a visible discontinuity in chest/shoulder/neck,
tote overlap, or hair settle. Technical repairs (alpha/protection/export) are not
artistic budget expansion. If the correction does not improve the named defect,
retain both checkpoints and stop.

## Preparation and proof plan after lease

1. Call Aseprite MCP preflight first; record actual server/client/editor/tool
   versions and selected headless mode. Inspect the exact sprite ID, frame count,
   layer order/visibility, palette, cel positions, timing, and hidden guide.
2. In my folder, run the required scratch capability/revision proof through the
   dedicated MCP: preview delivery, pixel read, one-pixel edit, transparency
   semantics, save/reopen, and protected-layer check. Do not use UI, Code-MCP,
   direct editor CLI/Lua, backend proxy or imagegen.
3. Copy/read the frozen baseline through MCP, duplicate frames using explicit
   sprite/frame/layer IDs, and apply the six-frame plan above. Preserve every
   source reference and the exact neutral frame.
4. Save a labeled native checkpoint and export each transparent frame through MCP.
   Decode exports locally to confirm 128x192, opaque/transparent alpha policy,
   palette membership and neutral-frame equality. Build 1x/3x nearest-neighbor
   GIFs only from the actual exported frames; no quantizing/resizing source art.
5. Inspect a pose/torso contact sheet and the exact neutral/crest/return frames at
   native size and matched integer zoom. Record separate motion/anatomy,
   material/shading, identity/expression, and technical/native decisions. If a
   visual discontinuity is found, spend the one correction pass and retain the
   pre-correction checkpoint.
6. Save, close only my documents, reopen a fresh copy, export again and compare
   all frame PNGs byte/pixel-wise. Make a duplicate-only local revision proof
   that changes one intended pixel/cluster and demonstrates zero changes to the
   protected rest frame/layers/metadata. Record exact paths and hashes in
   `verification.json` and `delivery.json`.

Unobserved boundaries to report: actual temporal naturalness until a real GIF or
editor playback is inspected; Godot integration/gameplay scale; user visual
approval; and final production selection. The video recording's FPS is not used as
animation timing.

## Native execution addendum

The plan was executed with the dedicated headless Aseprite MCP after the parent
granted the editor lease. The source was saved as `luna56-idle.aseprite` with all
12 original layers and 72 full-canvas cels (6 frames × 12 layers). The named
upper-body layers moved by one pixel up on frames 2–4; the tote and strap lagged
on frames 3–5; shoes and denim remained fixed. The neutral source is preserved
exactly on frames 1 and 6. A six-frame `idle-breathe` tag carries the authored
1,700 ms timing.

The filmstrip and exported contact sheet read as a quiet chest rise and settle,
with the tote lag providing a secondary cue. No blanket redraw or added backing
layer was necessary. The final source was saved, closed, freshly reopened, and
re-exported; all six reopened PNGs are pixel-identical to the first exports.
Both native GIF exports retain the intended six-frame timeline and durations and
compare exactly after matte/alpha normalization. A duplicate-only native source
was edited by one pixel on `03-shirt` frame 3 and saved as a separate proof copy;
the final source remains unchanged.

Technical validation uses the evidence available from this session: Aseprite
`sprite_info`, tag/cel lists, `read_pixels`, `look` filmstrip/ascii, native save,
fresh reopen and export comparisons, plus the bundled-Python report. The server's
preflight feature list mentioned `validate`, but no callable validate tool was
exposed, so that boundary is reported rather than claimed as passed. Godot
playback, user approval, publication and integration remain out of scope.

