# Updated-workflow, shared sharp-seed retest

## Result and selection

The exact requested fresh-context selectors were `gpt-5.6-luna` / `max` (trial-a)
and `gpt-6-luna` / `max` (trial-b). Parent supervision supplied observed defects
and editor scheduling only. No other model drew or corrected contestant artwork.
Shared infrastructure preparation and non-art tool diagnostics were separate.

| Result | Luna 5.6 Max | Luna 6 Max |
| --- | --- | --- |
| Final reported editor calls | 97/120 | 111/120 |
| Artistic checkpoints | Three, including rejected unchanged pass 01 | One delivered checkpoint; earlier unchanged export attempt disclosed |
| Best available authored result | pass-03 local face correction, pending user visual approval | None selected; pass-01 expression rejected |
| Visible difference from common seed | 11 facial pixels | Three mouth pixels |
| Native/technical boundary | Matching final reopen/export, protected source layer, separate duplicate-edit proof | Native/export correspondence and palette checks pass; final reopen/duplicate proof unperformed |
| Supervisor visual judgment | Shallower, more readable mouth than pass 02; eyes/hair remain recognizably sharp. Exact gaze/likeness remains user review | Mouth reads puckered/deep rather than the reference's restrained shallow smile; reject expression change |

These are bounded facial corrections from a common converted seed, not completed
multi-part production masters. Neither result implies animation readiness, runtime
quality, general model superiority or user approval. The shared seed is a fallback
working baseline, not a newly approved production asset. The comparison labels the
authored candidate and rejected attempt distinctly rather than calling both final.

## Controls and preserved inputs

The one-frame, one-layer native fixture contains only the source-derived seed,
not earlier authored eye/mouth overlays. Extraction proved the named source layer
identical between the prior native checkpoints. Both contestants received the same
128x192 decoded RGBA, binary alpha, 254 visible source colors, 255 ordered palette
entries, references, brief, workflow version, budget and native scaffold. Independent
copy verification preceded editor access. The supplied scoped context replaced
historical narrative that could expose old correction coordinates or outcomes.
No peer access or external art advice was supplied.

The supervisor independently verified unchanged reference/workflow/brief hashes,
both final ordered palettes, alpha equality, the exact 11/3 changed-pixel sets,
trial A's preserved base cel and reopened PNG equality, and trial B's native cel
correspondence. See [verification](supervisor-verification.json),
[fixture](shared/fixture.json), and [comparison](supervisor-comparison.png).

## Attempts, feedback and limitations

Trial B initially failed scratch writes with `aseprite_error: function: ...` while
reads succeeded. A separate non-art differential probe successfully exercised new
and opened scratch documents. The proposed blank-activation root cause was not
reproduced, and no backend/config/mode/extension repair was applied. Trial B's fresh
scratch retry passed. Those failures and substantial smoke overhead consumed its
budget and limit how much artistic opportunity this run compares. Counts are
contestant-reported, not provider billing/compute telemetry.

Both trials encountered face-layer edits not appearing in exported PNGs. Trial A
retained its unchanged pass 01 as rejected; after defect-only feedback, pass 02
exported eight intended face changes. Supervisor found the mouth still insufficiently
clear and reference evidence incomplete. Its third pass added three mouth-cluster
pixels, provided reference/seed/prior/new comparison and a separate local-edit
duplicate, then directly reopened/exported pass 03. No fourth art pass occurred.

Trial B diagnosed its own under-seed overlay and changed its construction route.
It did overwrite the first failed native binary before retaining a separate copy;
the later baseline-byte PNG is explicitly reconstructed evidence, not the lost
original native. Its corrected export contained three actual mouth changes. Parent
review rejected the expression and mismatched presentation scale. Trial B repaired
the presentation locally, agreed with the matched-view finding, retained the seed
as best prior and selected none. It stopped with nine calls unused rather than
claiming an accepted sprite or completed technical proof.

The updated gates demonstrably prevented promoting unchanged/failed-expression
exports in these checkpoints. This does not prove reliable future art quality.
Preparation confounds from the previous trial were removed; transient write errors,
unequal setup overhead and different amounts of completed proof still prevent a
broad intelligence or cost ranking. No token, price or active-time metric is known.

## Broader reference-to-sprite objective

GPT-6.1 Sol audited the existing workflow and recommended a small generic intake
clarification, implemented before freezing this test. Central intake now derives
representation, camera, scale, color/lighting relationships, subject-specific
identity cues, motion and native revision needs from supplied references and human
direction. Current female-face/grid examples are conditional. The pixel director
applies when pixel art is the chosen target; illustrated/rigged routes are not
forced through this recipe. Generic routing was independently checked for both a
softly painted nonhuman reference and an explicit low-resolution pixel reference.
The 32 existing director tests passed with the bundled runtime.

The [generalization plan and deferred matrix](generalization-plan.md) are linked
from CONTEXT and handoff. Different pixel styles/cameras, illustrated/rigged sprites
and action/motion remain deferred validation work. This is documented local backlog,
not an assertion that arbitrary art styles have already been recreated successfully.
No external issue was created. No artwork other than the isolated contestant copies
was changed; no installation, engine run, commit, push or publication occurred.

Next owner: user reviews the local-correction candidate and rejected attempt. Future
tests should follow the named intake/backlog cases and state their own acceptance
criteria rather than inherit this character's recipe as a default.
