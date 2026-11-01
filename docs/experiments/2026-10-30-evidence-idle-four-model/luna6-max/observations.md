# Luna 6 Max — independent idle preparation

Status: candidate construction and evidence packaging are complete. The serialized
Aseprite lease has been released; all output remains in this folder.

## Task profile

- **Intent:** independent end-to-end construction recipe using the shared neutral
  baseline and frozen video evidence pack. This is not a model-only score.
- **Exact assignment:** `gpt-6-luna`, reasoning `max`; no model substitution.
- **Motion target:** quiet, grounded breathing with connected chest/shoulder/head
  relationships. Root travel is zero; feet remain planted. Avoid horizontal
  translation and row-band movement. Prefer local shape redraws where volume changes.
- **Appearance target:** the user's approved tied-brown-haired woman, olive jacket,
  pale shirt, wide blue jeans, cream tote, and retained neutral face. Keep the pale
  shirt and olive jacket shade/texture roles readable through the cycle. The user
  prefers the movement direction of the latest redraw but rejected its clothing
  shading; this does not approve a whole earlier or later cycle.
- **Expression:** no redesign. If the supplied blink is used, reuse only its F5/F6/F7
  head drawings at their 50/80/50 ms source durations.
- **Target scale:** shared 128×192 canvas, transparent, provisional full-body scale;
  review at 1× and integer 3×. Gameplay display size remains unknown.
- **Output scope:** new native candidate derived from the frozen neutral input,
  retaining the one-frame rest drawing, canvas, palette and all 12 layer definitions
  including the hidden guide. No source/reference files are modified.
- **Pass budget:** one construction pass; at most one self-identified artistic
  correction. Keep failed/changed checkpoints and label technical repairs separately.

## Frozen inputs and hashes

| Input | Role | SHA-256 |
| --- | --- | --- |
| `inputs/neutral.aseprite` | One-frame native rest baseline | `d76266fa8afcd1de643e6b6421ec4dfe4fa77f8044a1d083205b921eb2f25540` |
| `inputs/neutral.png` | Composite export of neutral baseline | `e7c62ff0e2f3f88b10b17904322f834175e62d33579cc646a9e6396f940b57ad` |
| `inputs/character-scene.png` | Approved identity/style, full-body context | `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae` |
| `inputs/character-closeup.png` | Approved face/hair/costume detail | `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7` |
| `inputs/blink-source.aseprite` | Optional inherited F5/F6/F7 blink only | `25ae8dc1952cf5ef62d081735f52a56cb4cd726c08423d639b3c510b2d6f6f42` |
| `inputs/evidence-pack.zip` | Frozen reference-evidence pack | `d1b8998eb2eace9e74062a7afb3c5bc0e8711a6666ef95c8c723ac134eb65457` |
| Pack-declared source video | Tutorial evidence provenance | `c946289c8fc1ff74faf4fbc0206c58f2e1c9eebd37e18f595f5418e9b5e93a95` |

The pack and frozen input files are read-only. `prep/native-structure.json` is a
read-only standard-library header/chunk inventory, not a substitute for the required
MCP preflight and `sprite_info` after lease grant.

## Direct visual observations

### Approved character anchors

I visually inspected `inputs/character-scene.png` and `inputs/character-closeup.png`
at their original displayed size before drawing. The full-body anchor has a tall,
relaxed silhouette, right-turned three-quarter face, tied brown hair and flyaways,
open olive jacket, pale shirt, high-waisted wide blue jeans, cream shoulder tote and
pale sneakers. The close-up confirms the off-center fringe/eye relationship, pale
hair tie, warm skin, quiet smile, shirt neckline, jacket opening and tote strap.
Warm storefront light and cooler street light belong to the scene context; they are
not a reason to cycle orange lighting across the neutral sprite.

### Baseline

`inputs/neutral.png` was visually inspected at native 128×192 and as a separate
nearest-neighbor 3× preview at `prep/neutral-3x.png`. It is a single transparent
standing pose with hands in pockets, tote on the character's right side, broad jeans,
and planted shoes. The face/hair and clothing are provisional construction pixels,
not the approved art anchors. I will preserve this neutral pose as the rest drawing.
The standard-library decoder measured 249 distinct RGBA tuples, zero partial-alpha
pixels, and 16,732 fully transparent pixels; it also confirmed the 3× preview is an
exact nearest-neighbor enlargement. A read-only native-cel recomposition matched the
supplied composite PNG pixel-for-pixel. This is preparation evidence, not the required
post-edit MCP reopen/export check.

I also inspected `prep/torso-neutral-5x.png`, a nearest-neighbor crop of the actual
baseline. The torso is framed by separate olive jacket panels and a pale shirt, with
the cream strap crossing the right side; hands meet the lower corners and the shirt/
jacket meet the waistband. The pale shirt has muted rose-gray fold clusters, while
the jacket uses olive base planes and dark olive-brown folds. These are the specific
material relationships to watch during motion. The exact editing boundaries will
still be read back through the MCP.

The read-only parser reports 32-bpp RGBA, one 100 ms frame and these 12 layers in
order: `guide-source-seed (hidden)`, `00-shoes`, `01-denim`, `02a-jacket-left`,
`02b-jacket-right`, `03-shirt`, `04-tote`, `05-tote-strap`, `06a-left-hand`,
`06b-right-hand`, `07-face-and-neck`, and `08-hair-tie-and-hair`. Visible-layer flags,
frame and cel metadata must be confirmed again through the dedicated MCP before edits.
The optional blink source has the same 128×192 canvas and layer definitions; its eight
durations are 600/350/550/600/50/80/50/250 ms. The specified F5–F7 50/80/50 ms
frames are structurally available in the same `07-face-and-neck` owner; alignment and
actual pixels were inspected through the MCP before reuse. The eye closure is carried
by `08-hair-tie-and-hair`; the face/neck layer is pixel-identical to neutral.

### Tutorial excerpts — workflow evidence, not an art recipe

I inspected one frame from each selected MP4 excerpt; stills and hashes are indexed
in `prep/video-frames/index.json`. The exact video-frame samples and transcript lines
below are bounded evidence. I did not claim to have watched actual-speed playback.

| Evidence ID and source time | Direct still observation | What I take from it / what I will not copy |
| --- | --- | --- |
| `clip-01-core-poses`, 05:09 (`local 5s`) | A different character is shown in Aseprite on a two-column timeline. | Supports the tutorial's two-state starting point. Transcript `transcript-052`–`054` says exhale/inhale poses, shifting above-hip material, and a 10-frame plan. I will not transfer its character, pixel shapes, or blanket one-pixel shift. |
| `clip-02-chest-subpixel`, 07:05 (`local 11s`) | The tutorial character is framed around chest/shoulders; the timeline visibly has 12 columns. | Transcript `transcript-072`–`074` describes feathering a highlight across three tones/frames to soften the transition. I will inspect corresponding shirt/jacket forms while retaining the user's material roles; source palette and per-cel durations are unavailable. |
| `clip-03-arms-delay`, 10:26 (`local 12s`) | A small arm/hand region is selected in a 24-column timeline. | Transcript `transcript-103`–`107` discusses delaying/outward secondary arm motion. This pose has both hands in pockets, so I will keep hands and tote attachment static. |
| `clip-04-hair-settle`, 12:22 (`local 15s`) | The tutorial's separate hair strand is visible above the head on the zoomed canvas; the timeline has many columns. | Transcript `transcript-117`–`118` mentions hair flare/settle. Hair motion is outside this quiet test's construction scope; keep hair and identity fixed. |
| `clip-05-leg-shading`, 14:40 (`local 14s`) | The tutorial's lower body is enlarged, with the 24-column timeline visible. | Transcript `transcript-134`–`139` discusses shifting a leg shadow while retaining its silhouette. Our baseline's denim/shoes stay fixed to protect grounding and clothing appearance. |
| `clip-06-breathe-tag`, 16:04 (`local 18s`) | A `Breathe` tag spans 13 visible columns; two small character views appear on the canvas. | Transcript `transcript-146`–`154` explains a 13-frame Breathe tag and a separate held Idle frame. I will choose independent timing for this single idle candidate; the tutorial timing cannot be recovered from the 30 fps screen recording. |

The pack records that source project, palette, export script and exact cel durations
are unavailable. The tutorial concerns another character. Its clips contain editor UI
and creator overlays; the MP4 excerpts are H.264/AAC re-encodes. Transcript content is
automatic STT. I use this evidence for process and transition ideas only, never for
recreating the tutorial sprite.

## Initial construction plan

After the lease grant, I will run headless MCP preflight first, inspect the document
through `sprite_info`, and complete the required isolated scratch edit/reopen/export
smoke procedure in this folder. Then I will make a separate copy of the neutral
native document through MCP operations and inspect exact owners/pixel regions before
constructing frames.

Planned loop: ten frames and an initial total duration of 2,390 ms. The timing plan
is `[600, 180, 180, 360, 220, 220, 450, 50, 80, 50]` ms: neutral hold; two gentle
inhale steps; a short peak hold; two easing exhale steps; return/rest; inherited blink
beginning, closed hold and reopening. The last three frames use only the approved
blink-source face drawing at its 50/80/50 ms durations. The one-frame neutral drawing
remains the unchanged rest state and closes the loop.

The art hypothesis is a restrained chest-volume change built by direct local contour
and cloth-plane edits on actual shirt/jacket owners, not translating the canvas, not
warping row bands, and not painting an unexplained pale patch. Shoulder silhouette,
head/hair, hands, tote/strap, jeans, shoes and root remain fixed unless the actual
owner inspection reveals a specific small overlap that must be redrawn for continuity.
Any such scope expansion must stay within the same construction/correction budget and
be recorded. Palette, material identity, layer definitions and hidden guide stay
unchanged. Exact regions/operations will be frozen only after MCP owner/pixel readback.

The timing is a deliberate choice, not copied from the tutorial. I inspected the
native filmstrip and 1×/3× exports, but did not observe actual-speed playback, so
temporal naturalness remains unverified. There is no Godot/runtime validation, user art
approval, production-grid selection, or publication in this trial.

## Construction outcome

The pass01 candidate keeps the planned ten frames and 2,390 ms timing. Frame 1 is the
exact neutral rest image. Frames 2–6 shift a small existing three-value shirt fold
upward in steps and settle it back down; the affected `03-shirt` pixel counts relative
to rest are 15/20/26/20/15, inside `[57,54,64,65]`. This is a restrained cloth-plane
breath with no jacket contour, shoulder, hand, tote, leg, shoe, or root translation.
By full-body contact sheet the movement is subtle; actual-speed playback was not
observed, so temporal naturalness remains unproven.

Frames 8–10 copy only the eye region from blink-source `08-hair-tie-and-hair` frames
5–7, preserving its 50/80/50 ms durations. MCP readback showed `07-face-and-neck`
identical to neutral in those source frames; all 13/26/13 changed eye pixels belong to
the hair layer. No color was added. The original hidden guide and other ten original
layers remain unchanged, with no added layers.

The final status is in `record.md`; literal MCP grid payloads are in
`ops/mcp-operations.json`. Native layer/duration checks pass in
`verification/native-comparison.json`; fresh reopen PNGs and native cel composites
match in `verification/export-check.json`; the 1×/3× GIF timeline and visible palette
checks pass in `verification/gif-check.json`. The Aseprite tool inventory exposed no
`validate` operation, so no plugin validation pass is claimed. No Godot playback,
engine integration, or user visual approval is claimed.

## Correction outcome

Pass01 remains preserved as `idle-candidate.aseprite` with its original frame exports,
GIFs, checks, record and hash. On the separate corrected copy, one self-identified
review correction lifts the existing two-pixel rose-gray shirt crease by one pixel at
inhale peak F4. It uses the existing `#d6b7bb` and `#fde4cc` colors and changes only
four values in `03-shirt`; it does not move the jacket contour or alter the rest pose.
The corrected native, fresh-reopen frame exports, GIFs, contacts and checks are listed
in `delivery.json` and `record.md`. The duplicate-only local revision proof targets a
saved copy of that corrected animation native. Actual-speed playback, Godot integration
and user approval remain unverified.
