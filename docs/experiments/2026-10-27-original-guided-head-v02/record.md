# Original-guided head revision v02

- Status: three bounded drawing passes observed; provisional revision ready for user visual review. Likeness remains unresolved; no user approval inferred.
- Date: 27 October 2026.
- Scope: hair structure and restrained facial expression at fixed framing, after the user said “Okay do it.” No resolution comparison, full character, animation or environment work.
- Authoritative references: `assets/references/approved-2026-10-26/character-scene.png` and `character-closeup.png`, both visually opened in this turn. Cutout is not the drawing authority.
- Baseline: the separate rejected `2026-10-27-reference-drift-audit/head-shoulders-features.aseprite`, not v01-v04. All previous assets/experiments remain untouched.
- Grid/framing: retain 120x112 native canvas, original close-up crop `(380,64)-(860,512)`, one native pixel per four reference-image pixels. This is a head-study grid, not an approved production resolution or a claim about the original's native grid.
- Bounded drawing plan: one structural hair pass, one face/expression pass, and at most one evidence-led refinement if a specific visible discrepancy can be corrected. Save and inspect original/candidate sheets before advancing. Retain rejected passes; stop rather than claim likeness from file correctness.
- Protection: keep the four clothing layers (`02-shoulders-and-hood-back`, `03-shirt`, `09-hood-front`, `10-tote-strap`) byte-equivalent in their pixel data and metadata. Preserve canvas, layer order and frames. Hair/face layers may be reconstructed; neck/ear colors may change for material consistency while their geometry stays fixed.

## Reference observations before drawing

The previous source placed the main crown near original-image y100 although the actual crown is nearer y125-140. The swept side mass, fanned tied locks, fringe openings, near/far lids and mouth need direct reconstruction rather than another global transform. The original near-eye lid rises toward the iris, its far eye is much narrower, the smile is shallow, and the skin is warmer/darker than the rejected study.

`hair-guide.png` and `face-guide.png` show original pixels with coordinate aids, enlarged 2x with nearest-neighbor. Sparse color readings from the approved original inform explicit material ramps; candidate pixels are still authored polygons/lines/clusters, not a resized/quantized raster. No source raster is imported into the native artwork.

## Checkpoint decisions

- Pass 01, `original-vs-pass-01.png`, inspected: corrected crown height and swept clumps; face is still inherited and pale, and the underlying old forehead leaves false gaps. Continue to the planned face reconstruction rather than call this a finished likeness.
- Pass 02, `original-vs-pass-02.png`, inspected: warmer skin and rising near lid, shallow smile, no transparent forehead gap. Remaining visible problems are an oversized upper-left knot, arrow-like tied-hair ends and too-open far eye. Use the one remaining refinement pass for those structural/expression differences. A Lua numeric color-key parse error occurred before any face output was written; its source is retained, fixed by quoting the key, and not counted as a visual pass.
- Pass 03, [direct original review](original-vs-pass-03.png), inspected: reduced upper-left knot, open curled hair ends and a narrower far eye; clothing and framing unchanged. Stop drawing at the declared three-pass bound. This is a provisional improvement over the rejected baseline, not an established faithful match. The crown/front sweep remains too pronounced, tied hair too smooth, central fringe too pointed, far eye too narrow/profile-like and smile too graphic relative to the original.

## Delivered artwork and construction

- [Original / prior / new comparison](original-prior-new.png): original 480x448 crop is unresized; the prior and new 120x112 exports are nearest-neighbor 4x. Same crop framing, no anatomical auto-alignment or quality score.
- [New native source](pass-03-refined.aseprite) and [native 1x export](pass-03-refined.png). Ten meaningful layers, one frame, same 120x112 grid.
- [Hair checkpoint](pass-01-hair.aseprite), [face checkpoint](pass-02-face.aseprite), and all direct comparison images/JSON remain separate. No source or output from an earlier experiment was overwritten.
- [Latest construction script](revise.lua), [pass-01 source snapshot](revise-pass01.lua), [pass-02 source snapshot](revise-pass02.lua), [palette data](palette.lua), [baseline preparation](prepare.lua), and [frozen input hashes](frozen-inputs.json). The syntax-failed source is retained as `revise-face-syntax-rejected.lua`.

The main revision reuses protected clothing from the previous authored native study and reconstructs specified hair/face layers using new original-coordinate polygon/cluster inputs. Its forehead fill is extended behind fringe to prevent transparent holes, and face-feature pixels are clipped beneath the actual fringe. No concept raster, image-generator output or automatically reduced reference is substituted for native construction. Sparse reference color readings are analysis aids for explicit material ramps; they are not a raster-to-master conversion.

## Independent visual review

A separate `gpt-6.1-terra` / high-reasoning read-only agent visually inspected the approved originals, rejected baseline and pass 03. Its advisory finding: the new revision is visibly closer than the baseline and merits presenting as provisional, while still differing materially from the approved original. It identified the pronounced crown sweep/left tip, smoother ponytail, deep central fringe spike, sliver-like far eye, graphic near lid, angular cheek/jaw and more pronounced smile as remaining gaps. This is an agent assessment, not a numerical score, user approval or prediction of gameplay quality.

The immediate next owner is the user for concrete visual direction on the displayed candidate. If continuing, the agent should target head turn/near-far lids/shallow mouth and rounder swept-back crown without changing the fixed clothing. A larger grid is not selected by this result. No full character, environment, animation or engine expansion follows automatically.

## Technical verification

[Independent native checks](native-checks.json), reproduced by [check.py](check.py), use the existing strict RGBA reader without exemptions. All three checkpoints preserve header, palette and non-cel metadata, layer order/flags, frame timing, cel geometry/opacity/z, and all protected clothing-layer pixels. Baseline preparation changes only the declared palette metadata; its visible PNG is exactly the prior rejected input.

To avoid earlier save-time palette churn, the 40-color union of baseline colors and proposed reference-informed ramps is explicitly pinned before freezing the working baseline and after PNG export, before native save. The native palette has a separate transparency entry. This is a reproducibility policy for this run, not an approved color-count limit or a change to any historical source. Fresh reopen exports match each of the three checkpoints exactly, with binary alpha and unchanged native dimensions.

A duplicate-only [tie revision](tie-edit-proof.aseprite), [export](tie-edit-proof.png) and fresh reopened export demonstrate a meaningful localized edit: 16 tie-layer pixels change and all nine other layer images/protected pixels stay equal. The complete strict metadata comparison passes. The lighter-tie proof is not the selected candidate or a newly approved design color.

Actual Aseprite CLI/Lua backend: 1.3.18.6-dev, with existing targeted execution allowance. Five successful CLI invocations cover preparation, three drawing stages and reopen/edit verification; one extra invocation failed to parse the unquoted numeric color key before writing any face candidate. The observed clock interval 07:02:05–07:15:47 UTC (13m42s) covers palette preparation, drawing authoring/rendering, review and initial verification; it excludes initial repository/reference inspection and later reporting. It is not isolated drawing time or a production cost estimate. Aggregate pixel-operation totals, token usage and financial cost remain unknown. No image generation, installation, paid art service, commit, push or publication occurred.

No actual Godot run, projected gameplay scale, animation consistency, attack pose or motion validation is claimed. The native construction and protection checks pass; artistic likeness remains a separate open boundary. [Validation](validation.json) records focused file/link/preservation checks and [artifact manifest](artifact-manifest.json) identifies exact local files.

Official [Palette API](https://www.aseprite.org/api/palette/) and [Sprite API](https://www.aseprite.org/api/sprite/) were consulted on 27 October 2026 for explicit palette creation/assignment. Installed-build behavior is established by this run's native checks, not by documentation alone. Both actual 1x PNG and integer-zoom original/candidate sheets were visually inspected; neither is gameplay evidence.

## Reproduce in a new run directory

Copy `input.aseprite` and `palette.lua` into a new empty run directory. Use the existing Aseprite binary with `--script-param out=/absolute/new/run` and these sources, in order:

1. `prepare.lua` prepares the visually identical baseline and explicit palette.
2. `revise-pass01.lua --script-param stage=hair` creates the original first checkpoint. Generate and visually open an original/candidate sheet using the canonical `tools/pixel-art-director/scripts/reference_review.py` helper and the fixed crop before advancing.
3. `revise-pass02.lua --script-param stage=face` creates the second checkpoint, followed by its direct review.
4. `revise.lua --script-param stage=refine` creates the final checkpoint, followed by direct review. Existing native outputs are refused rather than overwritten.
5. `verify.lua` recreates technical proof files. Run bundled Python/Pillow with `check.py` only after the required files exist. Run `make-review.py` to generate the three-panel diagnostic in a new directory; it refuses existing review output.

These commands reproduce this provisional artwork, not user approval or a later improvement. Keep all snapshots, reference hashes and rejected alternatives. Further art work starts as a separately named bounded continuation.
