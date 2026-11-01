# Reconstruction feasibility and review

Use this for a new native reconstruction from an approved concept. The agent draws
and revises the asset; the user directs the visual decisions. The concept provides
a target, not a pixel grid or proof that every feature survives at game scale.

## Decide what must survive

Record the reference hierarchy and intended display size if known. Separate
identity-bearing features (such as head shape, gaze, hair masses and costume
silhouette), secondary details (folds, seams, small accessories), and atmosphere
(lighting and color relationships). Identify conflicts between views and label
uncertain interpretations. Prioritize identity and structural readability when
small details compete for space; preserve atmosphere without baking scene lighting
into every material by assumption.

## Source-assisted construction

Reference-guided traces, sampled colors, converted seeds and hybrids are permitted.
Use [assisted-reconstruction.md](assisted-reconstruction.md) when transferring source
geometry/pixels; retain raw inputs and meaningful native parts plus a local revision.
The same character/style is the target; exact raster duplication is optional. Additional
views and simpler generated references may resolve named gaps without replacing the
canonical identity/style anchors.

## Test scale before full construction

For each meaningful blockout or revision, inspect a sheet with the **approved
original** and **actual candidate export** before the next drawing stage. Keep
crop coordinates, source hashes, native dimensions and display scaling attached.
An old sprite plus new sprites is a reconstruction comparison, not a direct
original-reference review. Record visible deviations and a decision: continue,
correct structure, reject/stop, or request a specific unresolved art choice.

Freeze comparable framing before detail: record a shared reference crop, its
full-character equivalence, and approximate hair-top, eyeline, chin, neck junction
and shoulder landmarks in normalized crop coordinates. Derive design proportions
from the approved reference; use any existing sprite as a labeled baseline, not
an authority for a mismatched face. Map this layout onto each candidate grid and
inspect a silhouette/large-plane checkpoint at matched displayed size. Record
rounding and intentional differences. If head size, position, pose or crop differs
materially, correct the layout before spending the detail pass; matching canvas
dimensions alone does not make anatomy comparable. When budget ends first, label
the result an uncontrolled construction attempt and leave resolution unresolved.

Scaling or translating an agent's own polygon coordinates can be a legitimate
revision, but does not realign likeness to the original automatically. Recheck
the face turn, near/far eyes, cheek/jaw, fringe openings, tied-hair silhouette and
neck/shoulder relationship directly after any such transformation. If materially
wrong, correct or stop before detail or resolution conclusions. For a protected
correction, keep its locks; a required out-of-scope structural fix is a separate
proposal, not permission to enlarge the mask.

Make small, editable head or upper-body studies at a few plausible native scales,
using a provisional feature budget: estimate the pixels available for the eyes,
mouth, hair shapes and their spacing, then test whether those features actually
read. These estimates are hypotheses, not mandatory dimensions, color counts, or
quality thresholds. Compare studies at matched displayed size as well as native
size and integer zoom; show their full-body or scene context where available.
Label any reference resampling as comparison-only. Choose a provisional grid based
on visible tradeoffs and intended gameplay scale; where gameplay scale is unknown,
state the assumption and avoid claiming runtime readability.

Build from silhouette and large planes into anatomy, orientation and overlaps,
then identity accents and secondary detail. A structural mismatch calls for a
structural correction before repeated one-pixel polishing. Keep named layers and
construction operations so the agent can make a localized revision and verify it.

## Evaluate and stop

Review identity, geometry and orientation, expression, silhouette, pixel clusters,
secondary detail, atmosphere and context as independent observations. Note what is
visible at each scale and what remains uncertain; avoid a computed art score.
Compare with the approved reference as well as prior candidates. Record actual
checks, user approval and any playback separately.

Set a bounded pass or effort budget before testing. Stop when the next pass no
longer produces an observable improvement, evidence for a change is weak, or the
budget is exhausted. If the grid cannot represent a required feature, preserve
the best study and propose a separate larger-grid, simplification or representation
variant, with consequences for display size and animation cost. The six-pixel v03
local-correction pilot is evidence for a tightly protected edit only; it is not a
maximum fidelity result for a reconstruction.

The 27 October combat-art-lab studies exposed this specific failure: native files
and edit proofs passed while framing/proportions differed, so neither study could
establish a resolution advantage. The layout checkpoint above addresses that
observed failure; it has not yet been validated by a controlled redraw.

## Produce direct reference evidence

Use the helper from this skill directory (Pillow is already a toolkit dependency):

```sh
python3 scripts/reference_review.py \
  --reference /path/to/approved-original.png \
  --reference-crop 380 64 860 512 \
  --candidate /path/to/actual-candidate-export.png \
  --candidate-zoom 4 --out /path/to/new-pass-original-review.png
```

Those crop numbers are only an example from this character; choose and record
the relevant original-image crop for the task. The tool includes both images,
keeps their aspect ratios, labels nearest-neighbor display resampling, records
hashes/crops in JSON, and refuses overwriting evidence. Matching crop heights does
not match anatomy. It cannot authenticate an approved reference, prove the agent
looked at a sheet, judge likeness, or approve resolution: the agent must verify
the authoritative source, open the resulting image and record a reasoned decision.
Keep the native 1x PNG separately; the sheet is a diagnostic, never a native master.
