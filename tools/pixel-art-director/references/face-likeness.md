# Face likeness and expression correction

Use this procedure when eyes, mouth, expression, or other small facial marks are
ambiguous. It applies to the task's authoritative references and declared native
scope; it does not prescribe a face grid, palette, or anatomy ratio.

## Register before interpreting

Open the original references and actual baseline export. State each source's role
(identity, expression, pose, simplification, or support) and record any pose, crop,
or scale disagreement. Register approximate eye centers and extents, nose, chin,
and existing mouth/feature clusters with confidence. Preserve aspect ratio; matching
panel dimensions or raw distances across unrelated crops does not align features.

Inspect the baseline at three scales: the tiny feature crop, the whole head, and
the native full asset or intended display context. Separate observations (for
example, “two low-contrast pixels curve down”) from interpretations (“mouth”,
“nose”, or “skin shadow”). Record an observation → confidence → small test → expected
visible result. If source pose prevents a confident registration, retain the source
as authority, label the uncertainty, and stop rather than inventing exact pixels.

## Establish the editable owner and scope

Read the actual visible native owner, frame, cel, and pixels for the feature before
editing. A nominally named face layer may not own the composite mark. Freeze the
mask/layer/frame scope after registration and preserve it in the pass record.

For a correction, retain the approved good clusters and change only the declared
scope. Test economical alternatives as separate checkpoints. Evaluate a proposed
curve by placement, relative contrast, and reading in context—not by lowest changed
pixel count. A feature that improves only at extreme zoom is not a sufficient pass.

## Review and hand off

Inspect each actual export against original, baseline, and best eligible prior at
native size, useful integer zoom, and whole-asset context. Record whether the
candidate improves expression and likeness, remains uncertain, or is rejected;
technical scope success cannot choose the art.

An independent critic may suggest a correction or perform one bounded rescue within
the declared remaining pass budget. A critic-edited output is a new checkpoint: log
the editor, operations, exact export, and hash, then obtain fresh independent
inspection before it can be selected. User visual approval remains separate.

## Historical v03 protection profile (optional)

The bundled `combat-art-lab-v03.json` records one 128×192 protected correction:
editable x34..79 and y2..30 inclusive, excluding neck notch x57..65 at y29..30;
allowed layers `01-hair-back`, `05-skin-face`, `10-hair-front`, and
`11-face-features`. It is a historical example only. Re-verify it against that
source before use; it is not a default for another asset.
