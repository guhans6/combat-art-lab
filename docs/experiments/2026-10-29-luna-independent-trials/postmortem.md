# Luna independent-trial postmortem

## Result

The user preferred Luna 5.6's sharper hair and more open/readable eyes. Luna 6's
final eyes read as angular, squint-like marks. The four comparison panels are
correctly labelled: they were checked against the saved export hashes; see
[head recheck](supervisor-head-recheck.png).

This does **not** show that Luna 5.6 is generally better than Luna 6. It is one
pilot of two independently selected end-to-end workflows, not a controlled
same-seed model comparison. It does show where this run diverged.

## Evidence timeline

| Stage | Luna 5.6 (A) | Luna 6 (B) | Consequence |
| --- | --- | --- | --- |
| Inputs | Same source/references and 128x192 target ([brief](BRIEF.md)). | Same. | Inputs were equal; derived seeds were not. |
| Seed | 8:1 nearest-neighbour, alpha <=16 removed, source-derived large palette ([recipe](trial-a/recipe.md), [script](trial-a/scripts/prepare_seed.sh)); 253 visible colors in final. | Alpha >=32, premultiplied-alpha 8:1 BOX, coverage threshold, then 40-color median-cut/no dither ([preparation](trial-b/preparation.md), [script](trial-b/scripts/prepare_seed.py)); 35 visible colors in final. B's seed review already says hair/fringe soften and eye marks merge. | The preferred hair detail was inherited from preparation. First-to-final diffs are face-only: A 9 pixels, B 35 pixels. The pilot cannot isolate BOX vs alpha/palette choices, nor attribute this solely to a model. |
| Early face work | Pass 01 added bright eye whites and a smile. | Pass 01 added 8 face pixels to its low-color seed; its expression remained weak ([pass 01](trial-b/passes/pass-01-observations.md)). | B needed to reconstruct facial information that A's seed retained. |
| Correction | A pass 02 removes its *own* white-eye additions and diagonal smile, preserving underlying unequal source eye clusters ([plan](trial-a/pass-02-plan.md), [record](trial-a/passes/pass-02-record.md)). | After pass 02, review already says eyes are angular and mouth marks jaw-like ([pass 02](trial-b/passes/pass-02-observations.md)). | A's final is principally a revert/preservation choice; B's visual warning existed before its last pass. |
| Final | Stopped after 2 passes; final remains technically valid but contour/review defects remain. | Pass 03 clears existing `Facial features` pixels in eye/mouth boxes to face-base, then paints explicit replacement `new_marks` ([script](trial-b/scripts/prepare_pass03_layers.py)). Its own final review still reports angular/closed eyes ([pass 03](trial-b/passes/pass-03-observations.md)). | The rejected B eye read is traceable to face-feature replacement, not to semantic-layer ownership itself. Code proves what changed, not private reasoning. |

## Cause assessment

| Finding | Confidence | Limit |
| --- | --- | --- |
| B's softer hair predates later cleanup. | High: B's seed notes, visual first/final, and face-only diffs agree. | No controlled ablation identifies the exact preparation variable. |
| B's final eye regression is in its replacement feature treatment. | High: pass-03 implementation and head crops agree. | This is not evidence of intent or a general model limitation. |
| A's preferred eyes came partly from preserving/reverting to source clusters. | High: A's plan/record explicitly remove its added whites. | A did not thereby pass every visual/technical criterion. |
| Review/selection overvalued workflow evidence over expression. | High: angular eyes were known after B pass 02, yet the final outcome lacked an identity/expression veto. | B's semantic parts and reopen/local-edit proof are still real, separate wins. |
| Call totals caused the visual outcome. | Unsupported: A 116 vs B 110 calls; B's total includes 35 smoke calls/two smoke errors. | Calls are not provider compute/cost telemetry or causal quality proof. |
| Luna 6 is generally worse. | Unsupported. | One confounded pilot cannot justify a tier claim. |

## Future controls

1. Freeze one deterministic seed, palette/alpha treatment and review sheet for a
   model comparison. Test seed recipes separately.
2. Before native construction, gate the raw seed face at 1x and matched enlarged
   scale against the approved close-up: unequal eye footprints, gaze, and shallow
   smile must be readable.
3. Treat identity/expression as a veto, not an average with semantic ownership or
   reopen success. Compare each pass to the best prior head crop and retain that
   prior candidate when a new pass regresses.
4. Include a face-only diff and source/seed/candidate head strip per pass, so
   preservation versus replacement is visible before consuming the final pass.
5. Score native proof separately from visual art, and account for smoke/setup
   calls separately from art-correction calls.
6. Repeat the exact same-seed task before making a model-tier conclusion.

## Status

Read-only analysis of retained outputs and scripts. No candidate artwork, native
source, recipe, or export was modified.
