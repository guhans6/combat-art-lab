# Original-pose correction workbook

Open `original-poses-correction.aseprite`: six frames,256×208 RGB,400ms study holds.
Order: idle,reach,strap grip,windup,swing,recovery. This is a separate six-key study,
not a replacement of the previous19-frame authored animation. No new in-betweens,
head substitutions, tote reconstruction, palette reduction or AI cleanup.

Select a frame column and the top Corrections row to paint. To erase/change the
converted base, duplicate that frame’s named converted layer, hide its original,
and edit the duplicate. Each pose is a flat image on its own named layer, not
semantic body-part layers. Save a personal native copy first.

`all-poses-2x.png` is a static contact sheet. `study-playback.png` is lossless animated
PNG,6frames/2400ms. `pose-01..06/converted.png` are the actual transparent drafts.
`inputs/`, `recipes/`, `manifest.json` retain originals, previously reviewed masks,
anchors, source hashes and measured conversion reports. All six share183/1022
source scale (taken from accepted reach), not individual183px bounding-box fits.
The face/body/tote come from their own original images. All visible RGB colors are
source samples. Masking produces binary alpha; pixel noise/contours/transitions
remain for the learner to judge and correct. Not final gameplay art.

Rebuild conversion using Python with Pillow13+ (new destination only):

```sh
python3 ../../automation/convert_original_poses.py --source-root /Users/guhan/Guhan/Projects/combat-art-lab/docs/experiments/2026-10-31-new-keys-smear --out /private/tmp/new-original-pose-drafts
```

Conversion is deterministic and calls no model or network service. The original
PNGs and masks are historical inputs; their prior generation/review is not rerun.
Native assembly used the existing headless Aseprite MCP, not AI drawing operations.
PNG processing is scripted; native sources are saved only by Aseprite.

Checks: all6composites match source-derivedPNG, exported sheet and fresh-reopen
sheet; repeat runs produce identicalPNGbytes; reach identical to accepted draft;
blank Corrections; native frame durations400ms; APNG decoded frames exact. Existing
animation files preserved. Built-in validate is advertised but not exposed; scoped
native/pixel checks used. No new Godot run, artistic approval, commit or publication.

Reliability limit: disk/copy/write failure can leave an incomplete new output directory.
Choose a new output destination before retrying; manifest.json is written only after
all six conversions succeed. The converter does not overwrite an existing folder.
