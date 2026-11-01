# Trial A observations — shared sharp-seed retest

## Scope and authority

- Trial: independent `gpt-5.6-luna/max` same-seed comparison, 2026-10-29.
- Frozen task: `../BRIEF.md`; scoped context: `../shared/trial-context.md`.
- This record uses only the declared approved scene, approved close-up, supporting
  generated cutout, and the copied common seed/native inputs. Historical trial
  outputs, peer files, correction scripts and provenance sources were not inspected.
- No image generation or preparation change is part of this trial.

## Declared references (copied into `input/references/`)

| Role | Local copy | Source SHA-256 | Observed use |
| --- | --- | --- | --- |
| identity and style | `input/references/character-scene.png` (1448×1086 RGBA) | `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae` | full-body proportions, pose, costume and warm/cool scene context |
| identity and expression | `input/references/character-closeup.png` (1448×1086 RGBA) | `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7` | turned face, unequal eyes/rightward gaze, fringe, cheek and restrained smile |
| supporting production geometry | `input/references/clean-generated-cutout-v1.png` (1024×1536 RGBA) | `12e971cc9e3cbfa7add2a17a62ff53d1f45b3c55197ce23c336a6447bed1f49e` | silhouette and clothing geometry only; not an identity/style authority |

## Seed and native baseline observations

The copied seed is `input/source-only-converted-seed.png`, a fixed 128×192
8-bit RGBA image. Its native companion is `input/shared-source-seed-baseline.aseprite`
with one `shared-source-seed` layer and one frame. The copied ordered palette is
`input/ordered-palette.json`; it is the palette table extracted from the same native
baseline and is not a new palette.

At 1× and nearest-neighbor 4×, the seed retains the useful high-level design:

- tall full-body framing with visible bounds x=32..103, y=2..184;
- three-quarter standing pose, face turned and looking right, hands in pockets and
  one leg relaxed outward;
- tied brown hair with a pale tie, olive open jacket, off-white shirt, broad blue
  jeans, pale shoes and cream shoulder tote;
- crisp opaque clusters and binary transparency rather than a filtered resize.

The seed is not treated as an approved finished asset. At the 8× head crop, the
rightward orientation and smile direction are present, but the near/far eye
relationship is compressed into a small dark/skin cluster and the eye/gaze read is
less explicit than the approved close-up. The fringe openings and tied-hair mass
also merge in places at native size. These are observed, reference-supported
candidate repair targets; they are not permission to redesign the head.

The full-body silhouette, clothing blocks, tote attachment and leg negative space
already read at 1×/4×. They are therefore preservation priorities. No broad body
redraw is justified before reviewing the head correction. A dark warm/cool edge
field is visible around the seed in the preview; it is not assumed to be a defect
without a spatial review because the fixture freezes the seed's pixels and alpha.

## Seed-use decision

**Suitable only for a named bounded repair:** preserve the common seed's fixed crop,
canvas, palette, binary alpha, silhouette, pose and costume; repair only observed
face/gaze/expression and, if the same pass shows a directly connected identity
defect, the smallest adjacent fringe/tie clusters. Re-preparation, recoloring,
cropping, resampling, halo deletion, or a new generated intermediate would create a
different study arm and is out of scope.

## Provisional feature budget (hypothesis, to review on actual export)

- head/hair envelope: approximately x=41..89, y=2..49;
- turned face/cheek/jaw: approximately x=55..82, y=20..47;
- near eye and gaze cluster: approximately 3–5 native pixels wide;
- far eye/eyelid cluster: approximately 2–4 native pixels wide and intentionally
  narrower/partly occluded;
- mouth: approximately 3–6 native pixels, a restrained uneven smile rather than a
  horizontal bar;
- fringe openings: a few deliberate separations, not a field of isolated strands;
- hair tie: a small pale crossing cluster that remains visible without enlarging the
  hair silhouette.

These are inspection hypotheses, not hard thresholds or a likeness score. If a cue
cannot remain legible on this grid after a bounded repair, retain the candidate and
record a separate grid/representation proposal rather than expanding this trial.

## Evidence captured before editor access

- 1× copied seed: `input/source-only-converted-seed.png`.
- nearest-neighbor seed 4×: `evidence/seed-4x.png`.
- nearest-neighbor seed head 8×: `evidence/seed-head-8x.png`.
- copied baseline export: `input/shared-source-seed-baseline.png`.
- copied baseline reopen export: `input/shared-source-seed-baseline-reopen.png`.
- supporting cutout 2× preview: `evidence/cutout-2x.png`.

The baseline export and reopen export are retained as technical evidence; the seed
PNG remains the visual source-of-truth for the common decoded pixels until the
native document is opened through the authorized Aseprite MCP.

## Unresolved until a candidate export exists

- exact face-pixel mask and palette indices after `sprite_info`/pixel reads;
- whether the seed's dark edge field belongs to the frozen character treatment or
  needs a separately labelled study (no removal is planned in this arm);
- actual native layer organization after opening the baseline;
- final visual selection, user approval, animation, Godot playback and production
  readiness (all outside this static trial).
