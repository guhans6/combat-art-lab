# E1 — bounded pixel-craft candidate

**Status:** Candidate B is technically valid and retained as evidence, but **rejected
for promotion**. Control A remains the E1 baseline.

## Scope and frozen control

Control A is the unchanged E0 B00 native source and export copied into inputs.
The source crop, E0 recipe, and E0 manifest hashes are frozen in freeze.json.
The grid remains 120x112, with the same crop/masks/palette and nine semantic layers.
No image generation, new reference, pose, resolution, alpha, silhouette, frame,
layer, or palette change was made.

The first pass is warnings-only-lint.json. Its 1,835 RGB-isolation observations
are explicitly non-actionable diagnostic candidates, not defects and not an
automatic deletion list.

## Visual hypothesis and pass

source-control-shoulder-hypothesis.png compares the approved source and Control A.
It disproved an initial proposed right-shoulder brightening: the source supports the
existing midtone there, so that edit was not made.

The one pass instead uses four already-opaque 01-jacket pixels:
(29,91), (30,91), (31,92), (32,92). They are a two-row stepped cluster,
not a solid square. Existing frozen colour #5f4a34 replaces the broken
dark-to-mid transition to test a compact left shoulder-plane cluster. Face, eyes,
mouth, fringe, rear hair, tie, shirt, neck/ear, all jacket pixels outside those
four coordinates, alpha, and all other native structure are protected.

Candidate B was built through the dedicated headless Aseprite MCP, saved as
outputs/candidate-b.aseprite, exported, closed/reopened, and exported again.
No Lua, CLI fallback, UI, or Code-MCP was used. The observed tool sequence consumed
well below the 80-call maximum; two rejected draw-schema calls changed no pixels.

## Checks

scripts/verify_e1.py is read-only and passes: frozen E0 inputs still hash-match,
exactly four opaque jacket pixels differ, Candidate B's fresh reopened export matches,
and the normalized strict checker passes. The raw strict check is retained in
raw-strict-check.json: it reports only header/frame serialization drift, matching
the known E0 palette normalization behavior. normalized-strict-check.json passes
with four allowed 01-jacket changes and zero protected changes.

The direct review sheet is source-control-candidate-comparison.png: approved source,
Control A, and Candidate B appear at actual 1x plus 4x nearest-neighbour, with
magnified changed-region callouts.

## Honest visual assessment

At actual 1x, the candidate is not a clearly perceptible improvement. At 4x, the
callout shows a more regular local shoulder cluster, but it reads as subtle edge
lightening rather than meaningful cleanup. This narrow hand-chosen four-pixel patch
does not establish a general pixel-craft-aware first-fill algorithm, a numerical
lint improvement, or user art approval. Review therefore rejects promotion and
retains Control A; Candidate B remains available as a failed-but-preserved trial.
No repair pass was justified by the observed evidence.

## Unperformed boundaries

No Godot/runtime playback, motion, production-scale decision, cost measurement,
commit, push, publication, or E2 work was performed.
