# Aseprite learning workspace

Open [the course](index.html) in a browser. For the current one-pose exercise, jump to [Two ways to begin](lessons/0005-two-ways-to-start-your-character.html). Start with [Pixel art before you draw](lessons/0004-pixel-art-before-you-draw.html): distinguish drawing size from game-view size and write a provisional size plan. Then continue through the original Lessons 1–3. The foundations file is numbered 0004 because it was authored fourth; it is first in the learning sequence.

This directory is the teaching workspace: MISSION.md, RESOURCES.md, NOTES.md, lessons/, reference/, assets/, practice/, and learning-records/ all resolve here. Shared styling and feedback code are in assets/. No learning record exists until the learner demonstrates understanding.

## Current: one standing pose, earlier 183-pixel drawing

Use `practice/one-pose-183-2026-11-01/hand-trace.aseprite` or
`automatic-draft.aseprite`. Both are one-frame 128×192 files. Visible artwork is
72×183 with 248 used RGB colors and the original 255-entry palette. There is no
resizing, color reduction or new artistic correction. The source is the exact
original-neutral drawing used in the linked clean/smear chat, verified against
its first animation frame after removing the (+60,+8) placement offset.

- Hand tracing: full-resolution locked Guide at ~30%; three blank drawing layers.
- Automatic: all 12 earlier layers preserved (11 drawing layers plus the hidden
  old guide), with an empty top Corrections layer.
- Inputs, manifest, native reopen/local-revision evidence and previews stay beside
  the files. Save a personal copy, then work on just the tote contour or a tiny
  color patch. Animation comes later.

The rejected 92–97px workbooks, generated frames, previews and test copies were
removed at the user’s request on 1 November 2026. Original reference inputs and
preparation records remain in `practice/two-routes-2026-10-31/`. Its historical
verification reports describe the earlier run; generated outputs are no longer
available. The current reference is not an enlargement of that reduced draft.

## Earlier files to use

- `practice/character-practice.aseprite`: byte-identical copy of a historical one-frame, 128×192, 12-layer structured candidate; practice material, not a new approved asset.
- `assets/converted-seed.png`: historical flat converted draft. Useful if you want a simpler starting point.
- `assets/concept-cutout.png`: high-resolution generated support image for the resize exercise; it differs from the authoritative design in small features.
- `assets/identity-scene.png` and `assets/identity-closeup.png`: authoritative original identity references.
- `practice/provenance.json`: original repository paths and exact SHA-256 hashes.

Save your work as `practice/my-first-correction.aseprite`; export to `practice/my-first-correction.png`. The copies are independent of active production.

## Branch and isolation

Branch: `work/aseprite-learning`, created from `9e35c5c` in a separate worktree at `.scratch/aseprite-learning` inside the original art-lab checkout. The parent checkout remains on `work/e0-deterministic-replay`; its unfinished work was not moved or staged. Only `main` and the active art branch existed locally, and only `origin/main` was listed remotely when inspected. No prior learning branch or teaching folder was found in this checkout.

The worktree's inherited project documents describe the committed historical baseline. Current art status remains in the original checkout; the dated learning handoff and copied-input provenance describe this course. No production guide or reference was changed. Nothing committed or pushed by this task.

## Verification and next owner

See `VALIDATION.md` for observed checks and boundaries. User next chooses the hand-tracing or automatic starter, saves their own copy, and reports a first silhouette or small correction; the teacher adapts the next session. HTML checkboxes and quiz answers alone do not establish Aseprite proficiency.


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
