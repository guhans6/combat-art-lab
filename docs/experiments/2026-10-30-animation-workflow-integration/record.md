# Animation appearance diagnosis and workflow integration

30 October 2026. Scope: diagnosis and maintained guidance only. No art revision.

## Evidence-backed starting issues

- The supplied earlier comparison contains Terra on the left and earlier Sol on the
  right. The user's appearance preference covers this comparison; it selects neither
  side and approves neither whole animation. The latest redraw's movement direction
  is preferred, while its clothing appearance is rejected for game use.
- Equal-matte actual exports show changed shirt shadow contours and jacket fold
  patterns in the latest poses. This is a source-appearance lead, independently
  visible in the supplied handoff's torso contacts, not an automatic artistic score.
- Earlier Sol's `proof/prepare.py` copies neighboring colors with a coherent vertical
  sampling field. Terra's `proof/prepare_ops.py` copies local regions with outward
  shoulder displacement. Latest `construction-recipe.json` and
  `final-operations.json` explicitly author shirt/jacket/waist grids, including
  different phase-specific shadow marks. These methods explain different continuity
  risks; neither reuse nor redraw alone establishes acceptable animation.
- Prior records explicitly limit review to stills/decoded timing. Positive judgments
  about connected forms did not catch the user's later motion/material objections.
  This is a review error despite honest playback disclaimers.

## Assumptions and gaps before implementation

The user's supplied playback feedback is authoritative direction. Still-image review
here cannot establish actual-speed naturalness or the perceived magnitude of color
change. Palette/new-RGB checks, raw pixel changes and fixed-region histograms cannot
decide material stability. Native composites and GIF decoding will test export
quantization; shared mattes will test the background confound. No evidence yet shows
a new lighting model, intentional relighting, global palette change or material
misclassification. Native layer names are known to mix semantic owners.

## Compact integration plan

1. Read native files offline, compare every export/GIF frame and timing, and retain
   independently generated same-matte torso evidence in this new experiment only.
2. Add one disclosed animation reference to the existing portable animation branch;
   move that branch's detailed craft instructions there. Route animation audits and
   facial work accurately without making static edits load motion guidance.
3. Point the project motion branch to that procedure and record this project's
   current preference/status. Leave existing unrelated contracts and art untouched.
4. Validate source helpers, links/frontmatter, realistic branch decisions and a new
   standalone extracted bundle. Preserve previous archives and record remaining
   evidence boundaries.

No separate repository delivery Definition of Done exists; acceptance is the
requested diagnosis, maintained conditional integration and fresh local/package
verification. Installation elsewhere, art approval, engine playback and publication
remain separate.

## Independently observed result

Reproduce from repository root with `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.` and the
bundled Python runtime, running this folder's `audit.py`. [audit.json](audit.json)
identifies all three exact native hashes, both supplied GIF hashes, all durations
and comparison results. [Independent torso contact](independent-torso-contact.png)
uses the actual composites, equal matte and equal nearest-neighbor scale. Columns
are labelled native poses, not synchronized instants. Source pixels were inspected
alongside the handoff's independently generated contacts.

| Observation | Evidence | Meaning and limit |
| --- | --- | --- |
| All three rest composites are exactly equal; all 28 native composites equal their PNG exports | Offline normal-blend, full-opacity layer composition, fail-closed against unsupported structures | This isolates divergence to changing poses, rather than different starting costumes. Not a full native integrity audit. |
| Both supplied GIFs equal intended native composites on every decoded frame, at exact 3x, with native durations | A: 8 frames/2530ms, SHA `41e884b763c7073b7338f417311b723812607bb929ff34ed2ef2fd54cc09b7ff`; B: 12 frames/3950ms, SHA `a8a40b65c25460a8533e28350014f9fa51db667deb53558b11ff24a5b9e1e501` | Quantization is ruled out for these files. A's matte is RGB48/50/57; B's is RGB221/221/221. Shared-matte crops still show changed source folds, so the background is not the sole explanation. |
| No frame introduces a visible RGB absent from its own rest | Every native composite, not only the GIF palette | The failure can occur by redistributing existing shades. This does not prove every material uses the right shade or that palette chunks are unchanged. |
| Both earlier sides retain more recognizable source fold patterns; Terra also widens shoulders, earlier Sol lifts garment rows with a fixed head | A-left F2–4, A-right F2–4; actual construction recipes named above | Source-region reuse preserves local color/texture relationships more directly, while the user's motion objections remain. Neither side is selected or motion-approved here. |
| Latest shirt shadow changes branching/notches and cream interruptions, with jacket/waist fold marks also changing | B F3–7 versus F1; authored `initial.patches` and `phaseGrids` | This is consistent with the user's apparent color/shading complaint. Not every changing fold is wrong; the problem is the rejected combined appearance, not a threshold of changed pixels. |

A concrete source witness: latest `final-operations.json` → `phaseGrids`, frame5,
layer `03-shirt`, explicitly writes `[60,57,"sCCss"]`, with `s=#d6b7bb` and
`C=#fde4cc`. Final visible samples at x60..64/y57 are `ssCss` on F4, `sCCss` on
F5 and `Cssss` on F6. The central lavender area gains and loses cream interruptions.
This is authored surface-pattern change, not a new RGB or GIF remap. These frames
share the raised head position (independently exact under 1px registration above
y30), but that registration does **not** establish cloth correspondence or prove
these individual samples invalid. The surrounding shirt/collar/waist sequence and
user rejection supply the artistic context; the witness only establishes provenance.

## Diagnosis, competing explanations and uncertainty

The best-supported local explanation is insufficient continuity of material shade
clusters while constructing new poses: the shirt's pale base/lavender fold pattern
and jacket fold texture were rearticulated by phase, so the surface can read as
being repainted. Better connected motion and unchanged colors did not preserve the
earlier appearance. This is not evidence that redraw is inherently worse or that
translation is generally suitable for deforming cloth.

- **Export remapping:** contradicted by every decoded GIF frame matching native.
- **Preview background alone:** insufficient; equal-matte native comparisons retain
  the pattern changes. It may still influence the perceived strength of the effect.
- **Palette expansion or new RGB:** contradicted for visible frame colors. A
  fixed palette is compatible with the observed problem.
- **Intentional relighting or wrong material classification:** not established.
  No relighting is declared, and the inspected shirt legend assigns its expected
  cream/lavender roles. Nominal layers mix neighboring materials, so ownership must
  still be inspected; this audit found no specific accidental mapping proving that
  classification caused the complaint.
- **Too much independently repainted detail:** plausible contributor supported by
  the authored phase grids and changing topology; no controlled repaired sequence
  was made, so its causal/perceptual magnitude remains unisolated.

No actual-speed playback was watched in this task. User feedback supplies the
temporal complaint and preference. Stills establish pose/pattern differences and
technical decoding establishes pixels/timing; neither establishes natural breathing,
anatomical correctness, smoothness, game readiness or a new approved candidate.

## Instruction audit and review failures

| Classification | Finding |
| --- | --- |
| Existing preservation requirement, unmet artistic outcome | The workflow already required preserving identity/aesthetic, material colors and chosen style. The latest user feedback rejects B's combined appearance. That supersedes its earlier retained-for-review status; it cannot advance as an accepted game asset. |
| No demonstrated palette/protection violation | Fresh checks establish unchanged visible RGB set, not a native palette-chunk claim. Historical native checks are recorded separately. It would be incorrect to call the complaint a proven palette-lock violation. |
| Redraw instruction honored in inspected construction | B has literal authored garment grids and legitimate rigid head reuse. Requesting redraw did not authorize restyling; it also did not require every unchanged pixel to be repainted. |
| Earlier method mismatch, chronology matters | Prior easing used broad row-band displacement. The installed animate guide recommends rigid cel motion **and** explicitly allows redraw where form changes. It never required torso row warps. The explicit redraw request followed that rejection; do not retrospectively call the earlier attempt a violation of a later instruction. |
| Missing operational guidance | The previous portable animation section covered anchors, palette, head volume and played motion, but did not operationalize material/shading correspondence through poses, or choosing reuse/redraw per region. Static material-ramp guidance did not provide that temporal review. |
| Review error | Prior reviewers caught alpha gaps and neckline changes yet retained a cycle with subsequently rejected material behavior. Technical passes and body contacts supported overly positive visual judgments. Records disclosed the lack of actual-speed viewing; that disclosure was accurate but did not cure weak pose/material review. |
| Unsupported assumptions | “Same palette means stable clothing,” “redraw means improved art,” and “a static strip proves natural motion” are invalid inferences. These are risks exposed by the outcome, not claims about an agent's unobservable thoughts. There is no proof that an agent failed to open the references. |

The external animate source also describes a filmstrip as the way to “see the
motion.” Here it provides static pose evidence; the local procedure explicitly
separates temporal perception. External dependency files were not modified.

## Maintained integration

- `tools/pixel-art-director/SKILL.md`: discover animation construction, revision and
  diagnosis; disclose its procedure; reach facial guidance across modes; limit
  backend/drawing gates to mutation so read-only diagnosis can use offline evidence.
- `tools/pixel-art-director/references/animation.md`: canonical task-specific motion,
  appearance, scope and evidence profile; per-part method; corresponding-form shade
  review; independent decisions and playback limits. Generic, with no project model,
  asset, grid or palette defaults.
- `tools/pixel-art-director/references/craft.md`: replace the old detailed animation
  block with a pointer. `assets/AGENTS.snippet.md`: include animation/review in the
  optional consumer discovery trigger. The existing face procedure remains canonical.
- `tools/pixel-art-director/references/alpha-coverage.md`: following independent
  branch testing, separate scoped native coverage completion from engine delivery.
  Every-frame/native/reopen checks remain; runtime claims still need actual engine
  inspection. This resolves an inherited scope ambiguity reached by the new route.
- `docs/workflow/art-production.md`: existing mode selection routes animation to
  the motion guide. `docs/art/motion-guide.md`: conditional procedure pointer and
  current movement/rejection status; supersede historical absence of a motion clip.
- `docs/art/style-guide.md`: current appearance preference with neither earlier side
  selected. `docs/handoff.md`: append this milestone and next boundary.

AGENTS, CONTEXT, asset contract, template, helper implementations, external editor
guidance and project model choices did not need additional rules. All detailed new
animation guidance is disclosed by the animation branch; ordinary still corrections
do not acquire its checklist.

## Verification, delivery and next owner

[Fresh verification](verification.md) records source35/35 and standalone extracted
35/35 helper tests, links/schema/discovery, the official validator's missing-PyYAML
limit, all2,751 preserved input hashes, and the exact portable ZIP/hash. The separate
[independent forward pass](forward-review.md) exercised all eight requests in
[scenarios.json](scenarios.json): unchanged-palette clothing complaint, legitimate
moving cast shadow, rigid prop, deforming cloth, still-only review, static mouth,
static shoe and unrelated CSV work. It independently inspected scenario1's raw art;
the others were instruction decisions against supplied fixtures, not new drawings
or playback. Its one inherited alpha-scope ambiguity was fixed and rechecked, with
no outstanding branch issue. This validates discovery/decisions, not art quality.

The maintained source and existing local discovery symlink are updated. The new
portable bundle is validated for extraction, not installed or enabled elsewhere.
No art, native editor operation, Godot run, global config, commit or publication
was performed. Exact maintained changes versus the dirty starting state are in
[maintained-changes.patch](maintained-changes.patch).

No whole animation is selected by this task. **Next art owner: agent, under a
separate authorized art request**, to make a bounded rest/extreme/transition proof
from the shared neutral source, retaining the earlier appearance relationships and
the latest preferred movement direction. Review corresponding shirt/jacket forms
before extending a cycle; reuse rigid/unchanged parts where valid. **User** then
judges the exact timed candidate's appearance and motion independently. Actual
gameplay validation remains a later, explicit engine boundary. No manual repainting
is assigned to the user.
