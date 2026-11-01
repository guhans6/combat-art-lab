# MCP session log

## Tool and model

- Assigned model: `gpt-6-luna`, reasoning `max` (exact assignment; no substitution).
- Native editor: dedicated headless Aseprite MCP, Aseprite `1.3.18.6-dev`,
  extension `0.8.2`.
- Tool IDs used: `mcp__aseprite_ai_artist__preflight`,
  `mcp__aseprite_ai_artist__sprite_manage`,
  `mcp__aseprite_ai_artist__sprite_info`, `mcp__aseprite_ai_artist__layer`,
  `mcp__aseprite_ai_artist__draw`, `mcp__aseprite_ai_artist__look`,
  `mcp__aseprite_ai_artist__read_pixels`, `mcp__aseprite_ai_artist__frame`,
  `mcp__aseprite_ai_artist__tag`, `mcp__aseprite_ai_artist__export`.
- The live tool inventory did not expose a `validate` action. No plugin validation
  result is claimed.
- The system Python/Pillow used for read-only checks and packaging was
  `/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`,
  Pillow `12.3.0`. Python did not write or modify an Aseprite source.

## Scratch capability and revision check

1. Headless preflight returned ready. The isolated 16×16 RGB scratch document was
   `#3`; it had named `editable` and `protected` layers. A four-color asymmetric
   pattern was painted, the protected layer was locked, one pixel on the editable
   layer was changed, transparently erased with a grid edit, and restored.
2. It was saved through MCP as `prep/smoke-base.aseprite`. A fresh second open
   (`#56`) was changed only at editable-layer pixel `(12,3)` and saved as
   `prep/smoke-revision.aseprite`.
3. The revision was closed and reopened as `#69`; MCP exported
   `prep/smoke-revision-fresh.png`. Read-only native parsing confirmed exactly one
   changed pixel in `editable`, zero in `protected`, and exact fresh PNG/native
   composite equality. See `verification/local-revision.json`. This is a capability
   proof only, not a character-art deliverable.

## Production native calls

- Opened frozen `inputs/neutral.aseprite` as `#82`; `sprite_info` confirmed
  128×192 RGB, one frame, 12 layers, palette and hidden guide. Opened
  `inputs/blink-source.aseprite` as `#108`; its 8 frame
  durations and layer metadata matched the brief.
- Saved the neutral document as `idle-candidate.aseprite` through MCP, then
  duplicated frame 1 nine times with independent cels. The 12 original named layers,
  order, visibility, opacity and blend modes were retained.
- MCP readback found the source blink in `08-hair-tie-and-hair`: source frames 5/6/7
  differed from neutral by 13/26/13 pixels only in the eye region
  `[62,20,73,24]`. The corresponding `07-face-and-neck` pixels were identical.
  Frames 8/9/10 copied the permitted source frames 5/6/7 at 50/80/50 ms.
- The main art pass moved the existing `#D6B7BB` / `#E7D5C7` fold patch on
  `03-shirt` upward one pixel in nested regions. Target frame changes relative to
  rest were 15/20/26/20/15 pixels for frames 2–6, with all changed coordinates in
  `[57,54,64,65]`. Shirt/jacket contour, shoulders, face except blink, hands, tote,
  strap, jeans, shoes, root position, palette and hidden guide were not changed.
  Exact grid payloads are retained in `mcp-operations.json`.
- Set durations to `[600,180,180,360,220,220,450,50,80,50]` ms; created looping
  `idle` tag for frames 1–10 in olive `#6A613C`; saved through MCP.
- The MCP `frames` export expanded `idle_{frame}.png` to zero-based
  `idle_0.png`…`idle_9.png`, although its result listed the pattern path. Those ten
  files were confirmed byte-identical to the retained explicit per-frame exports
  `idle-00.png`…`idle-09.png`; the redundant underscore-named files were removed.
- Closed the production and blink documents; the MCP list returned empty. Reopened the
  saved candidate as `#952`, confirmed `modified=false`, 12 original layers, 10
  durations and the idle tag, then exported all ten frames to
  `verification/fresh-export/`. Closed that document; the MCP list again returned
  empty and the parent received `LEASE_RELEASED`.

## Native metadata note

Aseprite added one tag chunk `0x2018` and one associated tag user-data chunk
`0x2020` for the colored idle tag. The official Aseprite file-format specification
defines `0x2020` as User Data; `sprite_info(includeSlices=true)` returned no slices.
The first-frame header speed changed from 100 to 600 ms in step with the authored
first-frame hold. These intended metadata changes are recorded in
`verification/native-comparison.json`.

## Single artistic correction and actual-native revision proof

- After the separate correction lease, headless preflight returned ready. Opened the
  saved pass01 candidate as `#1156`; `sprite_info` showed the 10-frame, 12-layer
  `idle` animation and existing palette. Saved a separate MCP copy as
  `idle-candidate-corrected.aseprite`.
- Read F4's `03-shirt` region `[57,53,65,57]` through `read_pixels`. A single
  grid edit moved the two existing rose-gray pixels at `(60,54)` and `(61,54)` up
  to `(60,53)` and `(61,53)`, restoring the cells below to the existing pale-shirt
  color. The first malformed call used `op` instead of the required `kind`; it was
  rejected before drawing. The successful `kind:"grid"` call reported 32 touched
  pixels because it reapplied the 8×4 readback region; native comparison confirms
  exactly four changed RGBA values, no other art changes.
- Reviewed F4 with `look preview`, the 10-frame `look filmstrip`, and the F3→F4
  `03-shirt` diff. The diff showed exactly the four intended value changes. Saved via
  MCP, closed, freshly reopened as `#1566`; `sprite_info` returned `modified=false`
  and preserved 10 frames, tag, canvas, 12 layers and slice state. Re-exported all
  `idle` frames into `verification/fresh-reopen-corrected/` via MCP.
- Saved the freshly reopened final animation as
  `verification/actual-native-revision/idle-revision-copy.aseprite` via MCP.
  Read F4 `03-shirt` pixel `(60,53)` as `#d6b7bb`, then changed only that duplicate
  pixel to existing `#fde4cc`, saved, closed and reopened the copy as `#1947`.
  Fresh `sprite_info` returned `modified=false`; MCP exported frame 4 to
  `verification/actual-native-revision/revision-fresh-reopen.png`.
- Closed the duplicate and confirmed `sprite_manage list` returned `sprites: []`.
  Sent `LEASE_RELEASED` before continuing offline checks/package work. Exact operation
  payloads and IDs are in `ops/mcp-correction.json`.

The preflight feature list mentioned `validate`, but the callable MCP inventory did
not expose a `validate` tool or operation. No plugin validation result is claimed.

