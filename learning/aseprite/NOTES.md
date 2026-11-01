# Teaching notes

- 1 November 2026: learner finds the 92–97px converted starter odd and prefers the earlier crisp appearance shown in the clean/authored-smear comparison. Read-only audit matched all 70,596 opaque displayed pixels in the supplied screenshot's left panel to `2026-10-31-new-keys-smear/exports/clean-01.png` at 3×. That neutral drawing is 183px tall, 7,844 occupied pixels, 248 visible RGB colors; the new standing draft is 92px, 2,077 occupied pixels, 28 visible colors. Its unquantized 92px sample already loses fine structure; palette reduction adds another change. The two sources/preparation routes differ, so this is not a controlled test isolating resolution, color count or AI quality. Withdraw the approximately-96px recommendation for preserving this learner's preferred detailed look. Recommended next preparation retains approximately 183px character scale and reference color fidelity, while shrinking the exercise to one region/pose. No new native asset or revised workbook was produced by this diagnosis; do not imply that the existing files were upgraded or that the earlier animation has final user approval.

- 31 October 2026: user explicitly requested the teach skill, a branch, and a learning folder. Mission is grounded in the request; no interview needed to establish why.
- User wants optional hands-on correction and tracing after AI preparation. Keep agent-owned production available; this course does not change ADR 0001.
- No learning exercise has been demonstrated yet. Do not create a learning record or claim mastery because these lessons exist or a checkbox is selected.
- After the foundations lesson, begin hands-on work with Lesson 1: change one small tote color patch. Avoid starting with eyes, full-body tracing, animation, or a palette conversion.
- Next session: ask what happened when Corrections was hidden, and whether the learner could reopen their saved file. Use their evidence to choose a next exercise.
- Recall schedule: after a day, repeat the small correction without reading the steps; several days later, distinguish cleanup and tracing stacks from memory.
- Checkboxes are optional browser-local reminders, not assessed progress. They may not persist for local files in every browser. Quiz answers are not saved.
- Current app UI was not operated or changed. Menus are taught from official docs/source; local shortcut customizations may differ. Use menu names and tooltips on macOS.
- Community preference unknown; one optional official community link in RESOURCES.md, with no requirement to join.

- 31 October 2026 follow-up: user explicitly needs conceptual foundations before tool practice, especially choosing size and connecting Aseprite artwork to Godot framing. Start with the new foundations lesson (authored fourth, taught first). Do not assume the learner knows canvas, visible bounds, viewport or display scaling.
- This adds prerequisites within the existing mission, not a mission change. No new learning record: questions reveal needs, not demonstrated mastery.
- Ask for a four-line provisional size plan and what stayed constant in each simulator. Example 640×360/96px/3× numbers are hypotheses, not a game specification. Then return to existing Lessons 1–3 without resizing their practice source.

- 31 October follow-up with six supplied poses: learner reports exposure to sprite concepts but no specific demonstrated skill yet. They request two hands-on routes: full hand tracing/shading and deterministic automatic preparation followed by their own cleanup. Do not infer mastery or create a learning record from this request.
- Current entry is Lesson 5 with two new 128×128 workbooks. Primary versions contain source poses 1/4/5, renumbered timeline 1/2/3; full six-pose versions are optional next material. Approximate visible height 96px; actual six drafts 92–97px. Existing 128×192 practice stays separate.
- Teacher decision: keep the learner's supplied character, simplify the practice scope to a standing pose and then three rough silhouettes, rather than generate another character. Learn two shades per material before copying every fold.
- Automation-only means alpha threshold + fixed common scale/placement + one pooled palette + native assembly. The delivered automatic draft contains no AI artistic repairs. Two-pixel edit proof is isolated under evidence/ and not included in the starter.
- Next feedback: ask which route they chose, whether Guide visibility exposes only their own art, and what changes at 1×. Explain timeline rows/layers, columns/frames, cels and duration using their actual three-key file.

- 1 November 2026 redo authorized: use exactly the earlier 183px standing drawing and keep its colors; start with one pose. Source chat inspected via read_thread, title/id recorded in the new manifest. Its 128×192 original-neutral PNG matches the clean animation's first 256×208 frame at translation(+60,+8), full RGBA exact. New primary folder is practice/one-pose-183-2026-11-01; manual art blank over full-resolution faded guide; automatic preserves all 12 original layers plus blank Corrections. No downscale/quantization; palette255 / used colors248. Older three-key task is superseded, not the next required step. This is an explicit refinement within the existing mission, not demonstrated learner proficiency.
- Sample colors from the original palette or a separate full-opacity reference tab. Eyedropper on a faded guide can pick partial transparency; return to Base colors before painting. Current first win remains one tote contour or reversible color patch on frame1.


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
