# Course delivery evidence

Date: 31 October 2026. Artifact: `learning/aseprite/` in branch
`work/aseprite-learning`, isolated worktree `.scratch/aseprite-learning`.
Base revision: `9e35c5c`. Course and isolated handoff are local, uncommitted changes.
No separate repository Definition of Done exists; scope follows the user's teaching request.

## Delivered

- Stateful teaching workspace using the requested teach skill: mission, sources,
  teaching notes, three short HTML lessons, shared CSS/JS, printable HTML reference,
  and independent practice inputs with exact provenance.
- Beginner sequence: reversible tote patch; manual resize plus separate trace layer;
  editable source versus transparent PNG, then a documented optional Godot next step.
- No pre-existing learning branch or teaching workspace found in the inspected
  local/remote branch listing and repository files. Existing art branch retained.
- Learner demonstration remains pending, so no learning record or mastery claim.

## Observed checks

- Five HTML pages: all 46 relative resource/navigation references and referenced
  HTML anchors resolved. Each three-option quiz uses two-word answers; correct
  positions vary between lessons.
- Six practice inputs are byte-identical copies. The original files and copies
  were rehashed after construction and still match `practice/provenance.json`.
- Read-only native binary inspection: 128×192, 32-bit RGBA, one frame, 12 layers.
  `04-tote` exists, and `guide-source-seed (hidden)` is hidden and non-editable.
  This is structure inspection, not a fresh native reopen/edit/export trial.
- Browser: all five pages rendered at 1280px and 390px without document overflow;
  all images loaded. Each quiz produced the intended wrong-answer and correct-answer
  feedback. Checkbox persistence survived reload and was reset after the check.
  A lesson disclosure expanded. No page JavaScript errors were observed.
- Visual inspection: desktop course home, narrow-screen home and Lesson 1,
  and print-media desk reference. A final mobile adjustment retained exact 2×
  sprite display; the two affected pages passed overflow/scale checks again.
  Evidence: `output/playwright/browser-checks.log`, `mobile-integer-scale.log`,
  and four PNG captures. Print styling was inspected; physical page pagination
  and a PDF export were not tested.
- `git diff --check` passed. Parent worktree remains on
  `work/e0-deterministic-replay`; no parent files were edited by this task.
- Primary documentation checked for layer creation, Timeline, resize/canvas,
  paste-as-layer, opacity units, reference types, save/export and Godot static textures.
  Exact sources and version caveats are in RESOURCES.md.

## Boundaries and next owner

No Aseprite document was opened or mutated by these checks. No new sprite drawing,
conversion, native export trial, Godot project/run, learner assessment, visual approval,
commit, push, or publication was performed. Existing project art decisions remain intact.

The user next completes Lesson 1 in Aseprite and describes the visible result.
The teacher then records only demonstrated understanding and chooses the next small
exercise. Agents remain responsible for the separate production art pipeline.

## Foundations addition — 31 October 2026

User requested conceptual basics before the three tool lessons. Added
`lessons/0004-pixel-art-before-you-draw.html` as the first pedagogical step
(the file number records authoring order), plus a printable `reference/size-planning.html`,
shared `assets/size-lab.css` / `size-lab.js`, and dated primary-source research.
Course entry, Lesson 1 prerequisite link, desk reference, resources, notes, README
and isolated handoff now point into that sequence. Mission and learning records were
not changed: this is a prerequisite within the existing goal, and proficiency is unproven.

Fresh observed checks for this addition:

- All seven HTML pages: 66 relative resources/navigation references and referenced
  HTML anchors resolve; four quiz groups have equal answer word counts.
- `node --check` passes for the shared feedback script and new simulator script.
- The two new pages plus three changed navigation pages render without document
  overflow at 1280px, 390px and 360px: 15 page/width combinations. Images load.
- Pixel-budget demo: 32/64-wide draft pixel buffers differ from the source; the
  128-wide draft matches the source exactly. No new native artwork was produced.
- Framing demo: all nine combinations of 48/96/192 design-view height and 1×/2×/3×
  output enlargement produce correct displayed heights and invariant view percentages.
- New quiz produces both wrong-answer and correct-answer feedback. Course entry
  opens foundations; its next action opens Lesson 1. No page JavaScript errors observed.
- Visual inspection covers the two interactive diagrams, narrow-screen lesson and
  print-media planning reference. This checks print styling, not physical pagination.
- Six copied practice inputs retain their recorded hashes. A read-only PNG alpha scan
  measured this exact copy's bounds as `[32,2,104,185)` = 72×183 within 128×192.
- `git diff --check` passes. Evidence: `output/playwright/foundations-static-checks.json`,
  `foundations-browser-checks.log`, and five foundation/diagram/print PNG captures.

The 640×360 view, 96px figure and 3× display are teaching hypotheses. Browser
resampling and framing are not Godot runtime validation or a source-art comparison.
No Aseprite/Godot editor operation, production grid selection, art approval, learner
assessment, commit or publication occurred. Next owner: learner writes the four-line
size plan, then continues Lessons 1–3; teacher adapts based on that evidence.

## Two-route workbook setup — 31 October 2026

Delivered Lesson 5 plus a desk card and two primary 128×128 native workbooks:
`practice/two-routes-2026-10-31/hand-trace-first-keys.aseprite` and
`automatic-first-keys.aseprite`. Each has three frames (original source poses 1/4/5)
and demonstration holds 600/350/150ms. Optional six-pose versions, byte-identical
originals, preparation payloads/recipe and previews are retained. Existing earlier
teaching assets and production art are preserved.

Fresh evidence:

- Native construction used the ready, existing Pebbly 0.8.2 / Aseprite 1.3.18.6-dev
  headless backend. Scratch edit/erase/protection/reopen checks passed.
- Independent decoder checks pass: four workbooks' layers, locks, visibility, palette,
  blank art/corrections, frame counts/durations/tags; six source/payload/export identities;
  source hashes; primary-three-key selection; GIF pixels/timing; and isolated two-pixel
  correction proof with native protected content unchanged. Exact artifacts/hashes and
  60 passing check entries are in `practice/two-routes-2026-10-31/evidence/native-checks.json`.
- Fresh MCP reopen/exports were observed for the primary pair and full six-pose pair.
  Art-only manual exports are empty as intended. Six native PNGs match prepared pixels.
- Parent and independent reviewer inspected actual native contact sheet and aligned
  source/seed comparison. Scope-specific suitability is recorded in evidence/visual-review.md.
  Actual native heights are 92–97px; small-face/detail/edge/foot-continuity limits remain.
- Nine course HTML pages: 99 relative resources/navigation links and referenced anchors
  resolve; five quiz groups have equal answer word counts. The added timeline quiz has
  one correct statement and two false distractors.
- New lesson, desk card and changed course home pass layout at 1280/390/360px; images
  load, four native downloads have correct 128×128/3-or-6-frame headers, feedback works,
  checklist persists and is reset, and the optional six-pose section expands. No page
  JavaScript errors observed. The final locked-guide instruction and workbook navigation
  were checked. Evidence is under output/playwright/two-routes-*.
- Visual page checks include desktop lesson, responsive layout, home/workbook sections
  and print-media desk card. Print pagination is not claimed. `git diff --check` passes.

No AI artistic repair is included in the automatic starter; source preparation alone
created its pixels. The proof edit remains separate. No polished attack, in-between
synthesis, semantic rig, Godot run, game scale approval, learner assessment, commit or
publication is claimed. Next owner: learner saves a copy and reports their first
silhouette/correction; teacher adapts the next exercise.

## Redo: original 183px drawing, one pose — 1 November 2026

Current starters: `practice/one-pose-183-2026-11-01/hand-trace.aseprite` and
`automatic-draft.aseprite`, one frame on 128×192, drawing bounds 72×183, original
255-entry palette and 248 used RGB colors. The linked smear chat was inspected;
its standing entry matches the reused reference exactly after (+60,+8) translation.
No resize, quantization or newly authored art. Earlier small workbooks are preserved.

Independent verification passes 27 scoped checks, including reference byte lineage,
exact source/native/PNG/reopened RGBA, manual guide identity and empty art layers,
all twelve original automatic source layers/cels/palette/metadata protected, empty
Corrections, exact 2× display and a separate one-pixel revision/reopen proof. Evidence:
`practice/one-pose-183-2026-11-01/evidence/native-checks.json` and visual-review.md.
Parent observed native inspection, fresh reopen/export and the comparison image.

Lesson 5, entry page, desk card, resources, README and teaching notes now use one
pose and the new files. Nine HTML pages have 87 valid relative references/anchors
and five equal-word-count quiz groups. Three changed pages pass layout at
1280/390/360px; both downloads have one-frame 128×192 Aseprite headers; preview is
256×384 at exact 2×; quiz feedback and checklist persistence/reset pass; no JavaScript
page errors observed. Print styling inspected, physical pagination untested.
`git diff --check` passes. Local browser evidence: output/playwright/one-pose-*.

Next owner is the learner: save a personal copy, then trace only a tote contour or
make a reversible color patch. No new Godot run, completed tracing, animation,
learner proficiency, final art approval, commit or publication is claimed.


## Cleanup — 1 November 2026

User requested safe removal of rejected small starters. Removed generated native
workbooks, frame/preview images, GIFs, smoke/revision copies, reduced pixel payloads
and stale two-route browser captures. Original six input images, source/recipe
records and all current 183px assets remain. Historical validation claims refer to
the original run; removed outputs cannot be inspected or verified in place. See
`learning/aseprite/practice/two-routes-2026-10-31/cleanup-2026-11-01.json` for the deleted-file inventory.


## Full pose library — 1 November 2026

User requested all poses from the earlier smear chat after the one-pose starter.
Added `reference/all-poses.html` and `practice/full-sequence-183-2026-11-01/`: byte-identical
clean/smear material03 layered natives, 19 transparent PNGs each, timing and native/3×
GIF previews (45 copies). Both sequences have eight layers, 19 frames, 2230ms,
256×208 canvas. Standing is still 183px high; canvas is action padding. Frame 19
returns exactly to frame 1; only frame 9 differs clean/smear. Every one of the 38
PNG images matches the independently decoded native composite. Copy hashes match
sources. No native mutation, new art, resize, palette reduction or new runtime test.
The one-pose starters are unchanged; rejected reduced assets were not restored.

The chat reader rejected the oversized turn on this follow-up; lineage was resolved
from the saved chat final-message extract, the earlier experiment record and actual
local files. These records are historical evidence, not instructions. Gallery links
are added to the lesson and course entry. Next owner: learner picks one clean pose
to inspect/trace; source art approval and temporal judgment remain pending.


## No-AI reach preparation — 1 November 2026

User corrected the drift into manual preparation. Branch audit: main,
work/e0-deterministic-replay and work/aseprite-learning share committed9e35c5c;
relevant pipelines live as uncommitted experiment files in the parent worktree.
Found fullbody converter, E0 deterministic replay and source-guided smear recipes.
Added standalone automation/convert_image.py, original PNG/mask, JSON preset and
one-command launcher. Runtime uses installed Pillow13, no model/network or new
installation. Reviewed historical mask/anchors reused; nearest sampling preserves
source RGB, binary alpha,183px upright pose,256×208 canvas. No head/prop redraw.
Separate practice/reach-script-2026-11-01/ output has4490usedRGBcolors; all source
samples. Actual3× preview inspected. This is a flat seed needing user cleanup,
not layered semantic reconstruction or finished pixel craft. Existing native
starters/animation/production sources unchanged; no replacement performed.

Checks: independent rerun PNG bytes equal;183px geometry/binary alpha/source RGB;
clipping fails before output; existing output refused without altering its PNG;
git diff --check. Focused agent review completed. External recipe paths remain
allowed intentionally for a local image CLI, not a service accepting untrusted
recipes. Completion report is written last; a disk-write failure can leave an
incomplete new directory (choose a new destination). Script/Python/Pillow hashes
and versions recorded. No native export/reopen, new Godot run, installation,
commit or publication. Next: learner opens prepared PNG and corrects a duplicate.


## All original poses — script-only conversion, 1 November 2026

User requested the same accepted reach conversion on other original images with
source colors, no AI art. Created separate all-original-poses-2026-11-01 workbook
with6source poses only. Existing19frame animations and previous starters unchanged.
Sharedscale183/1022,256×208; source-derivedRGB,binaryalpha,previous reviewed masks
and anchors. No per-pose183pxfit, head replacement, tote redraw or new in-betweens.
Six flat named pose layers plus blank topCorrections;400ms study holds. All6PNG/
native/export/fresh-reopen exact, rerun bytes equal; frame2 equals accepted reach.
Lossless APNG preview checked frame by frame. Script conversion calls no model or
network. Existing dedicated headless MCP performs native assembly only. Not final
combat timing or new Godot validation; no learner correction/visual approval,
commit or publication. Next owner: learner opens native copy and corrects one pose.
