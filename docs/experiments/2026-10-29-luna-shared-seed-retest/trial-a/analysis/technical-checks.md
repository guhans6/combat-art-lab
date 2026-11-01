# Trial A technical checks and call ledger

## Input verification (completed before editor access)

| Item | Observed result |
| --- | --- |
| native baseline copy | SHA-256 `b1d91f6f87f650cbd2cae3edb69704d195bbdcf8d6b679b287d01e8a7283cc19` |
| seed PNG copy | SHA-256 `074168d9bfc5b2a2f2751810152bb0c31a71e7027a5368c0b393e17449fb84eb` |
| seed/native decoded RGBA | both `8839680f1bc70c1c99653a28c76c6f8ea41f401d2755c93146d765523cb5806c`; exact equality observed |
| canvas | 128×192 |
| native baseline | one frame, layer `shared-source-seed` |
| native palette | 255 entries; palette chunk SHA-256 `f2d4907a7493af8e6557f933e3c2c40d73f733658fc8250d925f79678ffb5b81` |
| seed alpha | `[0, 255]` only; binary alpha observed |
| visible pixels | 7,844 |
| visible RGB colors | 254 |
| visible bounds | x=32..103, y=2..184 (half-open review tools should use x=32..104, y=2..185) |
| baseline export | SHA-256 `7353611071482ea1e879ab9c247fb1d92c7bd90050b8eb99cbec4cdbdf612d12` |
| baseline reopen export | same SHA-256 `7353611071482ea1e879ab9c247fb1d92c7bd90050b8eb99cbec4cdbdf612d12` |
| copied ordered palette | JSON copy SHA-256 `daf9add836b6282ef3d3ce92485834ed5c6a006f5cebb1ad69646a78a5e60e81`; normalized ordered entries match the native palette |

The verifier used only read-only parsing of the copied native/PNG files and the
declared shared helper. The shared fixture and shared check report were not changed.

## Checks required for each artistic pass

- editor call sequence and return status logged with a monotonically increasing
  `editor_calls` count (limit 120);
- native canvas, frame count, layer names/order, cel geometry, visibility, opacity,
  blend mode, palette entry count/order and target document ID recorded;
- exported PNG is 128×192 RGBA with alpha values only 0/255 and no unexpected
  dimensions, matte, crop or filter;
- visible bounds and coverage inspected against the fixed framing; no accidental
  holes in face, shirt, jacket, jeans, tote or shoes;
- changed pixel bounding region matches the declared mask; pixels outside the mask
  and the preserved raw seed layer are unchanged;
- approved original, raw seed, best eligible prior and new candidate compared at 1×,
  integer zoom, head crop and full-body context;
- identity/face/silhouette/pixel craft/style observations recorded separately from
  automated results; no numeric aggregate or technical pass selects the art;
- source saved, reopened through the same MCP, re-exported and compared by decoded
  RGBA equality;
- one labelled proof duplicate receives one useful localized edit; the selected
  candidate and protected data remain unchanged.

## Call ledger

Before editor grant: `editor_calls=0`; local file/hash/preview work is not counted
as Aseprite/editor calls. Append one row per Aseprite MCP call after the slot is
granted; include failures and proof work.

| # | Pass/role | Tool operation | Document ID | Result | Notes |
| ---: | --- | --- | --- | --- | --- |
| 1 | smoke/setup | `preflight(mode=headless)` | — | pass | Aseprite `1.3.18.6-dev`; extension `0.8.2`; ready; features advertised: draw_batch/recolor/validate/tileset/reference/filmstrip |
| 2 | setup | `sprite_manage(open)` | `#3` | pass | Opened copied native baseline |
| 3 | setup | `sprite_info` | `#3` | pass | 128×192; one frame; one `shared-source-seed` layer; 255-colour palette |
| 4 | smoke | `sprite_manage(new)` | `#7` | pass | 16×16 RGB scratch |
| 5 | smoke | `sprite_info` | `#7` | pass | Scratch pre-edit readback |
| 6 | smoke | `layer(batch)` | `#7` | pass | Renamed base and created `smoke-edit` |
| 7 | smoke | `palette(set)` | `#7` | pass | Four-entry smoke palette |
| 8 | smoke | `draw` | `#7` | fail | Schema error: `kind` required; intentionally retained failure |
| 9 | smoke | `draw` | `#7` | fail | Schema error: `points` required; intentionally retained failure |
| 10 | smoke | `draw(pixels)` | `#7` | pass | Asymmetric three-colour pattern; palette locked |
| 11 | smoke | `look(preview)` | `#7` | pass | Scratch visual readback |
| 12 | smoke | `look(ascii)` | `#7` | pass | Scratch exact-pixel readback |
| 13 | smoke | `draw(pixels)` | `#7` | pass | Single localized edit |
| 14 | smoke | `read_pixels` | `#7` | pass | Default/composite readback |
| 15 | smoke | `read_pixels` | `#7` | pass | Default/base readback |
| 16 | smoke | `read_pixels(composite=false)` | `#7` | pass | Edit-layer readback |
| 17 | smoke | `read_pixels(composite=false)` | `#7` | pass | Protected-base readback |
| 18 | smoke | `draw(pixels)` | `#7` | pass with warning | Transparent colour palette-locked to blue; exact receipt retained |
| 19 | smoke | `draw(clear)` | `#7` | pass with warning | Clear operation cleared whole layer; exact receipt retained |
| 20 | smoke | `draw(grid)` | `#7` | pass | Restored scratch grid |
| 21 | smoke | `draw(grid)` | `#7` | pass with warning | `.` erased cells rather than skipping; exact behavior retained |
| 22 | smoke | `look(ascii)` | `#7` | pass | Grid transparency readback |
| 23 | smoke | `draw(grid)` | `#7` | fail | Schema error: legend/rows required; intentionally retained failure |
| 24 | smoke | `sprite_manage(save_as)` | `#7` | pass | Saved `analysis/scratch-smoke.aseprite` |
| 25 | smoke | `export(png)` | `#7` | pass | Exported `analysis/scratch-smoke.png` |
| 26 | smoke | `sprite_manage(close)` | `#7` | pass | Closed scratch |
| 27 | smoke | `sprite_manage(open)` | `#53` | pass | Reopened scratch through same MCP route |
| 28 | smoke | `sprite_info` | `#53` | pass | Reopened structure readback |
| 29 | smoke | `look(ascii)` | `#53` | pass | Reopened pixels read back |
| 30 | smoke | `export(png)` | `#53` | pass | Reopen export completed |
| 31 | setup | `sprite_manage(activate)` | `#3` | pass | Returned to production document |
| 32 | pass-01 | `look(preview)` | `#3` | pass | Baseline full-body 4× review |
| 33 | pass-01 | `look(ascii)` | `#3` | pass | Baseline head region readback |
| 34 | pass-01 | `read_pixels` | `#3` | pass | Baseline face region readback |
| 35 | pass-01 | `look(ascii)` | `#3` | pass | Baseline face region readback |
| 36 | pass-01 | `read_pixels` | `#3` | pass | Baseline face colours/coordinates readback |
| 37 | pass-01 | `look(preview)` | `#3` | pass | Baseline head crop review |
| 38 | pass-01 | `sprite_manage(save_as)` | `#3` | pass | Saved `passes/pass-01.aseprite` before correction |
| 39 | pass-01 | `layer(batch)` | `#3` | pass | Created face/fringe correction layers above protected base |
| 40 | pass-01 | `draw(pixels)` | `#3` | pass | Eight face-layer pixels; no palette snapping; bounded mask |
| 41 | pass-01 | `look(preview)` | `#3` | pass | Composite full-body readback requested |
| 42 | pass-01 | `look(preview,layer=face)` | `#3` | pass | Face-layer-only readback |
| 43 | pass-01 | `look(preview)` | `#3` | pass | Composite head-crop readback |
| 44 | pass-01 | `look(ascii)` | `#3` | pass | Composite face ASCII readback |
| 45 | pass-01 | `sprite_manage(save)` | `#3` | pass | Saved edited native source |
| 46 | pass-01 | `export(png)` | `#3` | pass | Wrote `passes/pass-01.png` |
| 47 | pass-01 | `sprite_info` | `#3` | pass | Three layers; face cel present; native modified=false after save |
| 48 | pass-01 | `palette(analyze)` | `#3` | pass with warning | 255 colours; 87 near duplicates; no off-palette colours |
| 49 | pass-01 | `read_pixels(composite=false)` | `#3` | pass | Protected base readback after export |
| 50 | pass-01 | `read_pixels(composite=false)` | `#3` | pass | Face overlay readback: eight visible pixels |
| 51 | pass-01 | `read_pixels(composite=true)` | `#3` | pass with defect | Composite readback remained equal to base at overlay coordinates |
| 52 | pass-02 | `sprite_info` | `#3` | pass | Confirmed pass-01 diagnostic state before opening raw baseline |
| 53 | pass-02 | `sprite_manage(open)` | `#140` | pass | Opened copied raw native baseline |
| 54 | pass-02 | `sprite_info` | `#140` | pass | One protected base layer; 128×192; 255-colour palette |
| 55 | pass-02 | `sprite_manage(save_as)` | `#140` | pass | Saved `passes/pass-02.aseprite` |
| 56 | pass-02 | `layer(create)` | `#140` | pass | Created `pass-02-face-correction`; protected base retained |
| 57 | pass-02 | `draw(pixels)` | `#140` | pass | One-pixel export-path proof inside face mask |
| 58 | pass-02 | `look(ascii)` | `#140` | pass | Composite readback visibly contained proof pixel |
| 59 | pass-02 | `sprite_manage(save)` | `#140` | pass | Saved proof state |
| 60 | pass-02 | `export(png)` | `#140` | pass | Wrote `passes/pass-02-tech-proof.png` |
| 61 | pass-02 | `draw(pixels)` | `#140` | pass | Seven additional face-expression pixels; palette locked |
| 62 | pass-02 | `look(preview)` | `#140` | pass | Head crop visual review |
| 63 | pass-02 | `look(ascii)` | `#140` | pass | Composite face exact-pixel review |
| 64 | pass-02 | `sprite_manage(save)` | `#140` | pass | Saved pass-02 native |
| 65 | pass-02 | `export(png)` | `#140` | pass | Wrote `passes/pass-02.png` |
| 66 | pass-02 | `sprite_info` | `#140` | pass | Two layers; correction cel present; native modified=false |
| 67 | pass-02 | `palette(analyze)` | `#140` | pass with warning | 255 colours; no off-palette colours |
| 68 | pass-02 | `sprite_manage(close)` | `#140` | pass | Closed saved native before reopen proof |
| 69 | pass-02 | `sprite_manage(open)` | `#181` | pass | Reopened `passes/pass-02.aseprite` through same MCP route |
| 70 | pass-02 | `sprite_info` | `#181` | pass | Reopened native retains two layers and correction cel |
| 71 | pass-02 | `export(png)` | `#181` | pass | Wrote `passes/pass-02-reopen.png`; decoded equality with pass-02 confirmed locally |
| 72 | pass-03 | `sprite_manage(save_as)` | `#181` | pass | Copied eligible pass-02 native to `passes/pass-03.aseprite`; pass-02 PNG retained separately |
| 73 | pass-03 | `sprite_info` | `#181` | pass | Confirmed 2-layer pass-02 baseline before final smile layer |
| 74 | pass-03 | `look(ascii)` | `#181` | pass | Reviewed existing mouth cluster at native pixels |
| 75 | pass-03 | `look(preview)` | `#181` | pass | Reviewed pass-02 head crop before final bounded correction |
| 76 | pass-03 | `read_pixels(composite=true)` | `#181` | pass | Read mouth neighborhood to choose own bounded extension |
| 77 | pass-03 | `layer(create)` | `#181` | pass | Created `pass-03-smile-correction` above prior layers |
| 78 | pass-03 | `draw(pixels)` | `#181` | pass | Three additional smile pixels; palette locked; bounded face mask |
| 79 | pass-03 | `look(ascii)` | `#181` | pass | Composite smile neighborhood readback |
| 80 | pass-03 | `look(preview)` | `#181` | pass | Composite head-crop visual readback |
| 81 | pass-03 | `sprite_manage(save)` | `#181` | pass | Saved final native candidate |
| 82 | pass-03 | `export(png)` | `#181` | pass | Wrote `passes/pass-03.png` |
| — | pass-03 | local decoded checks | — | pass | Not an editor call: 11 changed pixels vs seed; 3 changed pixels vs pass-02; all inside face mask |
| 83 | proof | `sprite_manage(open)` | `#234` | pass | Opened saved pass-03 for duplicate proof |
| 84 | proof | `sprite_manage(save_as)` | `#234` | pass | Saved `passes/pass-03-proof-duplicate.aseprite` |
| 85 | proof | `sprite_info` | `#234` | pass | Duplicate retained protected base and pass-03 correction layers |
| 86 | proof | `layer(create)` | `#234` | pass | Created `proof-duplicate-local-edit` |
| 87 | proof | `draw(pixels)` | `#234` | pass | One useful localized smile extension at `(66,30)` on duplicate only |
| 88 | proof | `look(ascii)` | `#234` | pass | Duplicate localized edit visible in composite readback |
| 89 | proof | `sprite_manage(save)` | `#234` | pass | Saved duplicate proof source |
| 90 | proof | `export(png)` | `#234` | pass | Wrote `passes/pass-03-proof-duplicate.png` |
| 91 | proof | `read_pixels(composite=false)` | `#234` | pass | Protected `shared-source-seed` region read back after duplicate edit |
| 92 | proof | `sprite_manage(close)` | `#234` | pass | Closed duplicate; selected master preserved |
| 93 | pass-03 | `sprite_info` | `#181` | pass | Selected master remains 3 layers, visible and saved, no duplicate edit |
| 94 | pass-03 | `sprite_manage(close)` | `#181` | pass | Closed original pass-03 document before direct fresh reopen proof |
| 95 | pass-03 | `sprite_manage(open)` | `#265` | pass | Freshly reopened saved `passes/pass-03.aseprite` |
| 96 | pass-03 | `sprite_info` | `#265` | pass | Reopened native retains 3 visible layers, one frame, 255-colour palette |
| 97 | pass-03 | `export(png)` | `#265` | pass | Wrote `passes/pass-03-reopen.png`; local file and decoded RGBA equality confirmed |

Actual dispatched Aseprite/editor calls: `editor_calls=97` of 120. The local
decoded comparisons are explicitly excluded from this count.

## Per-pass status

| Pass | Native source | PNG export | Technical status | Visual status | Decision |
| --- | --- | --- | --- | --- | --- |
| raw seed | `input/shared-source-seed-baseline.aseprite` | `input/source-only-converted-seed.png` | pre-editor checks pass | bounded-repair baseline; not finished art | preserve as fallback |
| pass-01 | `passes/pass-01.aseprite` | `passes/pass-01.png` | native overlay exists, but exported PNG decoded RGBA equals raw seed | unchanged seed at exported-artifact boundary; artistic goal not demonstrated | reject candidate; retain raw seed as best eligible baseline |
| pass-02 | `passes/pass-02.aseprite` | `passes/pass-02.png` | proof and candidate exports differ from seed at exactly 8 intended pixels; reopen export equals candidate | bounded face-expression change is present in actual PNG; full-body silhouette/costume unchanged by declared mask | eligible checkpoint; release for defect-only supervisor review |
| pass-03 | `passes/pass-03.aseprite` | `passes/pass-03.png` | exported PNG differs from seed at 11 pixels and from pass-02 at 3 pixels; native saved, fresh reopen/export equality and duplicate proof completed | reviewer found the shallower mouth closer to intended expression; open-eye/hair/sharpness preserved; exact gaze/likeness remains user review | best available authored local-correction candidate; awaiting user visual approval; not a completed production master |

## Pass-01 export discrepancy

The saved native contains an eight-visible-pixel `pass-01-face-correction` cel
(`cel_raw_sha256=cf0ab95ae966916f12314201cf41c27178e1c577c9c4d62e24dad500a3613997`)
above the protected `shared-source-seed` cel. The native base remains the exact
shared RGBA (`8839680f...cb5806c`). However, `passes/pass-01.png` has file SHA-256
`7353611071482ea1e879ab9c247fb1d92c7bd90050b8eb99cbec4cdbdf612d12` and decoded
RGBA SHA-256 `8839680f...cb5806c`, exactly matching the raw seed export. A local
read-only source-over calculation predicts decoded SHA-256
`5c6533d48ed388fd44295a70848b02693d74a3f2231cf844c4d14bf6bcce0d97` for the
eight opaque overlay pixels, but the exported file does not contain those
changes. Therefore the face-layer readback is not accepted as an exported-artifact
proof. The next pass must use the raw seed/export as its baseline and first prove
that a localized native edit reaches the PNG before making any artistic claim.

## Pass-02 export proof

The fresh raw-baseline document accepted a one-pixel proof: `pass-02-tech-proof.png`
decoded to exactly one changed pixel versus the shared seed. The seven additional
bounded face pixels were then applied and exported as `pass-02.png`; its decoded
RGBA SHA-256 is `5c6533d48ed388fd44295a70848b02693d74a3f2231cf844c4d14bf6bcce0d97`
with exactly eight changed pixels, all inside `M-face-expression`. After saving,
closing and reopening the native source through the same MCP route, the
`pass-02-reopen.png` file SHA-256 matched `pass-02.png` exactly
(`fd221d8a2d411b985e257dbdfb327e8c1437b5bb7f23d9b8a9532ef5e5d2cb9f`). This is
the first eligible exported candidate; pass-01 remains rejected and is never
used as the next baseline.

## Pass-03 final-pass proof and selection evidence

Pass-03 copied the eligible pass-02 native and added only three pixels on the
named `pass-03-smile-correction` layer: `(67,30)`, `(70,30)`, `(71,29)`, all
inside `M-face-expression`, using existing palette colour `#542a1e`. The saved
candidate PNG has file SHA-256
`c6de338361498495d2e634f4c377d3f7e281dee9050371f94c2d1d4f36c91aee` and decoded
RGBA SHA-256
`cb5864a4f0862d132d0ef51c9f9dcb38e24649abab9e7ff58ee4c909db94d52e`. It differs
from the raw seed at exactly 11 pixels and from pass-02 at exactly 3 pixels, all
in the face mask. Matched visual evidence is
`evidence/matched-head-comparison.png` with its companion Markdown panel legend;
the strip is explicitly ordered approved reference, raw seed, best pass-02, new
pass-03.

The required duplicate proof is retained separately. The duplicate adds one
localized pixel at `(66,30)`, producing exactly one decoded pixel difference
from pass-03, while the selected master's PNG remains hash-stable and the
duplicate's protected `shared-source-seed` region readback remains unchanged.
The duplicate is closed after proof; it is not a candidate.

The selected pass-03 native was then closed and freshly reopened as document
`#265`. Its `pass-03-reopen.png` export has the exact same file SHA-256 as
`pass-03.png` (`c6de338361498495d2e634f4c377d3f7e281dee9050371f94c2d1d4f36c91aee`)
and decoded RGBA SHA-256 (`cb5864a4f0862d132d0ef51c9f9dcb38e24649abab9e7ff58ee4c909db94d52e`).

## Evidence boundary

Preflight, native edits, proof export, candidate export, direct fresh source
reopen/re-export equality, duplicate proof and read-only file checks occurred.
Godot preview,
animation playback, user visual approval and publication remain unperformed. The requested
`validate` operation was advertised by preflight but no standalone validate tool
was exposed in this MCP surface; no substitute is claimed.
