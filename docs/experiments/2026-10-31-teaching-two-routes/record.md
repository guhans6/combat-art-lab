# Experiment: two beginner routes from supplied pose references

- Status: observed teaching setup; learner exercise and artistic selection pending.
- Date: 31 October 2026.
- Question: can the learner start either from blank drawing layers over aligned guides,
  or from a deterministic converted raster and make their own corrections?
- References: six user-supplied pose PNGs, archived unchanged under
  `learning/aseprite/practice/two-routes-2026-10-31/inputs/`.
- Scope: practice workbooks and instruction. Existing production art and earlier
  128×192 teaching files are preserved. No finished attack or game integration.
- Tools: Aseprite 1.3.18.6-dev, Pebbly 0.8.2 headless MCP, Python 3.11/Pillow 12.0.0
  for deterministic grid preparation and evidence composition, local browser checks.
- Budget: one frozen preparation pass; no parameter repair required. One isolated
  two-pixel native correction proof; no artistic cleanup of the learner's draft.

## Plan and frozen recipe

Use the supplied character rather than generate a new design. Simplify the first
exercise to one tote silhouette or small correction, followed by three rough keys.
Native canvas 128×128; common transform scale 3/32 and translation (-4,+8) for every
1448×1086 reference. Nearest-center sampling, alpha >=128 becomes opaque, other alpha
becomes transparent. A pooled MEDIANCUT palette gives 31 opaque colors plus transparency;
no hue-based pixel deletion and no independent per-pose fitting.

Retain all six pose drafts. Primary workbooks select source poses 1/4/5 as standing,
windup and swing in frames 1/2/3, with 600/350/150ms demonstration holds. Full-study
timing is 600/250/250/350/150/400ms. These sequences are key-pose reels: missing
transitions and abrupt returns remain, rather than being presented as polished motion.

## Artifacts

All paths below are relative to `learning/aseprite/practice/two-routes-2026-10-31/`:

- `hand-trace-first-keys.aseprite`: three locked faded guides; three blank art layers.
  SHA-256 `1d9ae3423c2bc2c11209b7826d2e69997ed89ae2d3b6421c453b2ecc5e30f4fd`.
- `automatic-first-keys.aseprite`: same three guides hidden, prepared raster visible,
  blank Corrections layer. SHA-256
  `08b51ab3d1ca1742f8da6a52c6b438d0bcb55d97b51265223344489944a7c1eb`.
- `hand-trace.aseprite` and `automatic-draft.aseprite`: optional six-pose workbooks.
- `manifest.json`, `payloads/`, `rebuild/prepare_payloads.py`: copied-input hashes,
  exact grid recipe, shared palette and native bulk-painting inputs.
- `previews/`: native PNG frames, tagged sheet/JSON, three/six-pose GIFs and labeled
  contact sheet. These are practice previews, not approved runtime assets.
- `evidence/`: scratch smoke, MCP receipt, native checks, isolated local-edit proof,
  source/seed comparison and independent scoped visual review.
- Instruction: `learning/aseprite/lessons/0005-two-ways-to-start-your-character.html`
  and `learning/aseprite/reference/two-routes-cheatsheet.html`.

## Observations

| Check | Observed result | Evidence |
| --- | --- | --- |
| Backend smoke | Pattern/image delivery, exact one-pixel change, transparent skip/erase, protected area, native reopen and deliberate out-of-mask rejection passed. | `evidence/smoke-checks.json` |
| Native structure | Six/three frame counts, RGB dimensions, palette, named layers, guide lock/visibility/opacity, blank manual art and blank Corrections passed. | `evidence/native-checks.json` |
| Exact preparation | All six payload/native PNG pixels match; original hashes unchanged. Three-key files match six-pose sources 1/4/5. | `evidence/native-checks.json` |
| Local revision | Only two Corrections pixels in frame 1 change on a proof copy; native protected layers, alpha, palette, timing and reopen export remain intact. Main draft remains uncorrected. | `evidence/local-revision-proof.*`, `evidence/native-checks.json` |
| Size and appearance | Actual visible heights 92–97px; no native clipping. Character/outfit/bag recognizable. Small-face detail, edge residue, dense fabric marks and source foot drift remain cleanup subjects. | `evidence/visual-review.md`, `previews/contact-sheet.png` |
| Preview encoding | GIF frame counts, 384×384 dimensions, holds and 3× visible pixels match the native exports. Filmstrip reviewed; no claim of temporally polished motion. | `evidence/native-checks.json` |
| Teaching pages | Links, equal-length quiz choices, responsive layouts, feedback, optional section and native download headers passed. | `learning/aseprite/output/playwright/two-routes-*` |
| Godot/game scale | Not run. Approximate 96px character is a beginner trial, not a production resolution decision. | Scope boundary |

The tool named `validate` is not exposed in this session. Focused independent native,
PNG, palette, timing and scope checks provide the observed technical evidence instead;
do not claim a successful `validate` tool invocation. The bulk `frames` export did not
produce the intended six named files, so each PNG was exported explicitly and checked.

## Decision and next owner

Continue as learner practice. This clears workbook usability, not a new production
asset, complete animation, rig, user proficiency or visual approval. The user next
saves a personal copy and makes one silhouette or 2–6 pixel correction. The teacher
uses that result before adding frames or detailed shading. No commit, publication,
new paid service, generated character or editor-window modification was performed.


## Cleanup — 1 November 2026

User requested safe removal of rejected small starters. Removed generated native
workbooks, frame/preview images, GIFs, smoke/revision copies, reduced pixel payloads
and stale two-route browser captures. Original six input images, source/recipe
records and all current 183px assets remain. Historical validation claims refer to
the original run; removed outputs cannot be inspected or verified in place. See
`learning/aseprite/practice/two-routes-2026-10-31/cleanup-2026-11-01.json` for the deleted-file inventory.
