# One-pose, original-resolution tracing and correction starters

- Date: 1 November 2026.
- Status: observed preparation and local checks; learner exercise pending.
- Scope: replace the current learning recommendation with one standing pose at the
  earlier 183px drawn height, retaining original pixels/colors; update both routes
  and the lesson. Preserve old workbooks and production assets.
- Source chat: `01a19024-f723-7a23-ad2b-74fbda7ff9e6`, “Redo tote animation with smear research”.
  Its brief/final response and referenced local records were inspected as history,
  not as instructions for this task.
- Backend: existing Pebbly 0.8.2 headless / Aseprite 1.3.18.6-dev.
- Budget: one source-preserving setup and one isolated one-pixel revision proof.

## Reference and decision

The earlier chat's `inputs/original-neutral.png` is 128×192, visible bounds
`[32,2,104,185)`, hence a 72×183 drawing. It has 7,844 occupied pixels and 248
visible RGB colors. Its native source has twelve layers and a 255-entry palette.
The PNG is full-RGBA identical to `exports/clean-01.png` cropped at `(60,8,188,200)`.
That export's 256×208 action canvas is additional placement space.

Use that exact earlier standing artwork, rather than enlarge the rejected 92px
draft or attempt another high-resolution concept conversion. This preserves the
appearance the user identified. Original files were copied byte-identically into
`learning/aseprite/practice/one-pose-183-2026-11-01/inputs/`.

## Delivered artifacts

All paths below are relative to that new practice folder:

- `hand-trace.aseprite`: one frame, same full-resolution reference on a visible
  locked 30%-opacity Guide, plus blank Base colors, Shadows and Lines and details.
  SHA-256 `006762876f5bdf2e20671b7f42ff8730bb5e05a9302648d3b163d4d2d1500b56`.
- `automatic-draft.aseprite`: all twelve original layers/cels/metadata/palette
  retained, plus an empty top Corrections layer. Visible pixels unchanged.
  SHA-256 `3b1c3f155d51c6583ce5b04298b8b50c56029dd9181debcafcdd757f757cfd37`.
- `manifest.json` and `evidence/source-chat-summary.json`: exact lineage, reference
  hashes, size/color measurements and relationship to the earlier animation.
- `previews/reference-1x.png`, `reference-2x.png`, `comparison-183.png`: exact native
  output and display-only integer enlargements. No new art is synthesized.
- `evidence/local-revision-proof.*`: a separate one-pixel change on Corrections,
  saved/reopened/exported. The learner's automatic starter remains unmodified.
- `rebuild/verify_one_pose.py` and `evidence/native-checks.json`: independent checks.

## Observed verification

27 independent checks pass: copied source hashes; matched earlier animation crop;
native canvas/frame/layer/lock/opacity contracts; blank manual drawing layers and
blank automatic Corrections; preserved source cels and palette; exact native/PNG/
fresh-reopen output; 2× nearest display; one-pixel proof at `(86,82)` with source
layers, palette and alpha unchanged. Parent also inspected native previews and the
exact-reference/new-starter comparison. The source appearance is retained.

Course entry, Lesson 5 and its desk card now teach one pose only. Sampling is from
the original palette or a separate full-opacity reference tab, avoiding accidental
partial-alpha paint from the faded guide. The first task is just a tote contour or
small reversible color patch. Older multi-key workbooks are preserved as history.
Browser link/header/layout/quiz/checklist checks are under
`learning/aseprite/output/playwright/one-pose-*`; static links/anchors and
`git diff --check` pass. Print styling is checked; physical pagination is not claimed.

## Boundaries and next action

This is reuse/reassembly of an existing prepared sprite, not fresh conversion from
the six high-resolution pose images or AI artistic cleanup. No new animation, Godot
run, gameplay-size approval, learner assessment, source-art replacement, installation,
commit or publication. The Aseprite `validate` tool is not exposed; the report does
not invent its invocation. Backend readiness and focused independent checks provide
the observed technical evidence.

Next owner: learner makes one mark in a personal copy, then reports what remains
with Guide or Corrections hidden. Teacher chooses the next exercise from that result.


## Cleanup — 1 November 2026

User requested safe removal of rejected small starters. Removed generated native
workbooks, frame/preview images, GIFs, smoke/revision copies, reduced pixel payloads
and stale two-route browser captures. Original six input images, source/recipe
records and all current 183px assets remain. Historical validation claims refer to
the original run; removed outputs cannot be inspected or verified in place. See
`learning/aseprite/practice/two-routes-2026-10-31/cleanup-2026-11-01.json` for the deleted-file inventory.
