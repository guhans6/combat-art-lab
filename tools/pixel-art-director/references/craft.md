# Pixel construction and drawing passes

These are practical rules for this workflow, not a universal definition of good
pixel art. The approved art direction overrides generic retro-sprite defaults.
Research links and evidence status are in research.md.

## Start from the intended picture, not a filter

Use the approved silhouette, proportions, camera angle and material colors as the
brief. Establish the actual native grid and on-screen size independently of the
resolution of an AI-generated reference. A 1448-pixel illustration does not prove
a 1448-pixel native sprite, and a screenshot's display pixels do not identify the
game's native resolution. Never claim that our 128x192 experiment is Until Then's
native size. For new work, use the head/upper-body feasibility studies in
[reconstruction.md](reconstruction.md) before committing to a grid.

## Ordered construction

1. Block the silhouette and negative spaces on named layers. Compare at 1x.
2. Separate large material planes using the chosen palette. Check that hair,
   face, shirt, jacket and background are distinguishable without texture.
3. Place major shadow shapes consistent with the approved light direction. Do
   not change the light or color grading during a likeness correction.
4. Refine contour steps and overlaps: ear behind fringe, hair tie crossing hair,
   face against collar. Avoid mechanically repeated outlines of equal strength.
5. Place identity-bearing accents: eyes, mouth, a few fringe notches and clumps.
   For ambiguous facial marks, use [face-likeness.md](face-likeness.md): inspect
   morphology, contrast, and feature/head/full-asset context before editing.
6. Remove accidental clutter only after viewing the actual composition. Export,
   inspect at native size, and compare to the reference after each major pass.

The ordering is an authoring strategy; no step has a universal fixed color or
frame count. Correct structural relationships before polishing individual pixels.
A local correction usually starts at step 4 or 5 rather than rebuilding the silhouette.

## Clusters and edges

A cluster is a group of related pixels that reads as a plane or feature. Favor
readable shapes over randomly scattered texture. Use deliberate staircase rhythms
for curves; investigate an abrupt step that breaks the contour. Parallel shade
bands hugging an outline can flatten a form. Examine the actual shape before
changing it. Automated banding or isolated-pixel flags are suggestions, not orders.
An eye corner, nostril, tooth gap, hair glint or pupil may legitimately be one pixel.

Use selective dark, material-related contours where separation is needed. Keep
interior marks economical. Hair should read as a few overlapping masses before
strands; fabric should read as broad planes before seam/fold accents. Handmade
asymmetry means purposeful unequal shapes, not random noise or damaged anatomy.

Manual anti-aliasing is a recognized pixel-art technique, not the same as blur.
For a protected character correction, preserve the baseline edge language and alpha:
no new smoothing/filter/partial-alpha pass. A different art brief may allow
hand-placed intermediate opaque colors, but it must say so explicitly.

## Palette and scale

Preserve a local correction's existing color choices unless palette editing is
part of its scope. Do not assume 16, 32 or 45 is the correct total. The project
style guide records 45 visible colors for v01 and 51 for v02; inventory the frozen
v03 rather than inheriting either number as a hard-coded rule.

For a new asset, establish a compact palette of reusable material ramps, then
add colors only when they solve a specific readability problem. Warm highlights
and cool shadows are options, not a mandatory hue rotation. Keep the reference's
neutral material colors when environmental warmth is already strong.

Use integer nearest-neighbor enlargement for evidence. Enlarged crop comparisons
should use the same displayed head height, with any reference resampling labeled
as a preview only. Do not repeatedly resize the production source. Inspect 1x
and a plausible gameplay scale; attractive 16x detail may disappear at runtime.

## Animation branch (separate task)

For animation construction, revision or diagnosis, read [animation.md](animation.md).
Static construction and correction do not require that branch.

## Source basis

Cure's PixelJoint tutorial supports deliberate single-pixel control, cluster
thinking, and the distinction between manual anti-aliasing and automatic blur:
https://pixeljoint.com/forum/forum_posts.asp?TID=11299

Pedro Medeiros discusses resolution/color/style consistency and integer scaling:
https://saint11.art/blog/consistency/
His short tutorial archive includes work originally made for Twitter:
https://saint11.art/blog/pixel-art-tutorials/

The construction order and this character's constraints are our workflow design,
not claims that these artists endorse this AI pipeline.
