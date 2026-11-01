# Reference generalization and shared-seed retest plan

- Date: 29 October 2026.
- Status: audit complete; small documentation clarification recommended before retest. No drawing or new capability validation performed by this audit.
- Audited local base: `9e35c5c13987a153e942e6f93f49f247fad13c3a`, with substantial pre-existing uncommitted work preserved.
- Delivery authority: current user request and [validated checkpoints](../../agents/validated-checkpoints.md); no separate repository delivery reference or additional Definition of Done is established there.

## Decision

Make a small reference-intake/routing clarification, then run the requested bounded
same-seed comparison. Do not replace the workflow or build a universal art engine.
The long-term objective is to analyze supplied reference artwork with human art
direction, identify its relevant rendering/style properties, and construct usable,
revisable sprites in that chosen direction. The current character is a test case.
This objective is not a claim that every reference style is already supported.

[ADR 0001](../../adr/0001-ai-directed-art-workflow.md) leaves representation and tools
open; the [asset contract](../../art/asset-contract.md) explicitly accommodates pixel
and rig routes; the [workflow](../../workflow/art-production.md) already separates
style selection, construction, revision, motion and Godot evidence. Its seed gates
also explicitly reject a universal filter or palette winner. No new ADR, competing
asset contract, general-purpose skill, new tool installation or research phase is
needed for this increment.

The small gap is operational: feasibility/grid instructions still use this
character's face and 128×192 baseline as unqualified work items, while the experiment
template lacks an explicit representation/target intake. The pixel-art skill is
properly specialized, but its routing boundary can be made explicit. Clarifying
these items prevents the current successful recipe from becoming a default for
unrelated references; it does not establish non-pixel construction capability.

## Minimal maintained changes before the retest

| Target | Small change |
| --- | --- |
| `docs/workflow/art-production.md` | Add one compact reference-intake/representation subsection at the visual-target/feasibility boundary. Record source roles and approved qualities; camera/view; pixel versus illustrated/other edge and shading evidence; silhouette/identity; native/display scale; palette/color relationships; lighting/material separation; motion needs; native editability/revision requirements; uncertainties and smallest test. Select the recipe/backend from this target rather than the existing editor. Label the current facial landmarks and 128×192/192×288/256×384 grids as this-character pixel-study examples, conditional on relevance. |
| `docs/experiments/experiment-template.md` | Add concise intake fields, preferably one target-contract entry/link, for reference authorities, representation evidence, camera/scale, palette/lighting, identity, motion and native revision needs. Reuse existing recipe/seed and pass ledgers; do not create a compulsory second schema. |
| `tools/pixel-art-director/SKILL.md` | Add a brief route boundary: this skill serves selected pixel-art targets; it does not choose pixel art for every supplied reference. A different rendering target first follows the project's representation-neutral intake and a suitable smallest construction proof. Preserve all existing pixel craft, backend, native protection and review gates. Edit this canonical file, retaining `.agents/skills/pixel-art-director` symlink; leave ZIP snapshot unchanged. |
| `CONTEXT.md` and `docs/handoff.md` | Record the broader reference-to-sprite objective, link this plan/matrix, and state that this retest validates only the existing pixel route. Point to central intake instead of duplicating its contract. Leave current approved character/style history intact. |

Do not change the style guide into a universal style guide. It records this
character's direction. Motion guide and asset contract already provide appropriate
generic boundaries. Do not hardcode this character, nearest-neighbor, 253 colors,
fixed eye sizes or a palette count into generic instructions. User art direction
resolves consequential missing visual choices with concrete evidence; agents own
routine analysis, preparation, native construction, correction and verification.
Unknowns outside the current static test need not block it.

Focused verification: inspect the targeted diffs and touched links; confirm the
canonical skill symlink/frontmatter; run patch hygiene and applicable existing helper
regressions once if changed instructions affect their invocation. Reuse the previous
[guardrails verification](../2026-10-29-workflow-guardrails/verification.md) for its
already observed boundary, without claiming it validates new prose or new art.
Check two routing scenarios: a pixel reference can proceed through the director;
an illustrated/rig target is not forced into Aseprite pixel clusters or current grids.

## Retest readiness and frozen inputs

The [prior postmortem](../2026-10-29-luna-independent-trials/postmortem.md) explains
why equal originals did not make the earlier end-to-end pilots a model comparison.
Use the user-preferred sharper preparation as a controlled input for this test,
without attributing its success universally to nearest-neighbor or a large palette.

1. Complete and record the small documentation delta above; freeze the exact skill,
   brief, tool versions/catalog, target, pass/call budgets and controls for both runs.
2. Use the **source-only sharper pre-face-edit seed**, preserving the old experiment.
   Parent preparation measurements report that raw FFmpeg `seed-alpha-clean.png`
   contains 3572 visible RGB colors, while the actual sharper native base was
   palette-snapped. Prefer a deterministic read-only extraction of only the
   `converted-seed` source layer and exact palette from prior A pass-01 native,
   after proving that layer is identical in A pass-02 and contains source-derived
   pixels only. This is preparation provenance, not permission to provide contestants
   prior completed native artwork. Exclude every authored face overlay, correction,
   copied semantic layer, mouth fix and old correction script. Freeze the extracted
   seed/palette in new shared inputs and document the native extraction boundary.
   If raw FFmpeg seed is chosen instead, label it explicitly as a different
   preparation from the actual 253-color native look; do not claim equivalence.
   Raw file SHA-256 observed here is
   `1a02835a48ba3078c792d8047c0e6dc83f9cce2c45bed18fb40b5eba46354d52` at
   `../2026-10-29-luna-independent-trials/trial-a/work/seed-alpha-clean.png`.
3. Freeze the actual common palette bytes/order and decoded seed RGBA, dimensions,
   alpha policy, crop/transform and any ownership/native scaffold before drawing.
   Verify both contestant copies have identical seed, decoded pixels and palette
   hashes. Independently verify extraction/palette measurements; the prior final's
   reported 253 visible colors is not a substitute for the actual shared-seed check.
   If a common
   native baseline is supplied, verify its decoded pixels and native scaffold too.
   Choose one shared ownership/scaffold policy and declare any deliberately variable
   organization as part of the tested task; do not silently mix baseline structures.
4. Preserve source authority: approved scene/close-up own identity/style; the clean
   generated cutout supplies production geometry/pixels and remains supporting.
   Source SHA-256 observed here:
   `12e971cc9e3cbfa7add2a17a62ff53d1f45b3c55197ce23c336a6447bed1f49e`.
   Open originals, seed and seeded native export at 1x and matching integer zoom;
   record suitable, suitable for named repair, or re-prepare before dependent edits.
5. Launch independent fresh contexts for exact `gpt-5.6-luna`/`max` and
   `gpt-6-luna`/`max`, with the same brief and authorized dedicated Aseprite backend.
   No old trial outputs/ledgers, peer artifacts, extra model art advice or hidden
   rescue. Required context may mention history; contestants must not follow its
   links to prohibited artwork. Provide the new shared input rather than instructing
   them to browse old trial directories. Parent orchestrates only; art construction
   and correction remain each contestant's responsibility. Serialize shared editor
   access and retain the current no UI/Code-MCP/raw-Lua/direct-CLI restrictions.
6. Keep every pass, failed evidence and exact operations. Require direct
   original/seed/best/new export review, independent technical status, identity and
   expression veto, explicit next baseline and best-versus-latest selection. A good
   seed may remain the preferred visual candidate; demonstrate required native
   editability on a labelled duplicate rather than inventing a cosmetic improvement.

This retest can establish observed results for one shared pixel recipe and bounded
task per requested model. It cannot establish a general model ranking, rendering
universality, full production readiness, motion quality or Godot behavior.

## Deferred validation matrix

| Future supplied reference | Smallest useful validation | Current boundary |
| --- | --- | --- |
| Current cinematic pixel character | Same sharper seed, independent native cleanup/revision trials | Requested retest; not run by this audit |
| A different pixel subject/style or camera | Fresh intake and identity-rich crop, target-specific grid/palette/edge choices, native local revision | Untested; do not inherit this character or recipe |
| Illustrated or softly shaded 2D reference | Identify edge/rendering rules; compare a suitable layered/rig or other native construction route at intended display size | Deferred and untested; pixel-art director is not automatically applicable |
| A stylized action reference | Shared identity/scale anchors, key poses/contact/timing, actual-speed playback, local art/timing revision, then Godot observation | Deferred; static export and editability cannot prove motion/runtime |

Keep these future tests discoverable through CONTEXT and handoff. They are local
backlog questions rather than implied production commitments. No external issue is
needed for this bounded record: tracker writes require their own authorization and
fresh destination verification even though historical setup records enablement.

## Audit evidence and next owner

Read required context/glossary/handoff, ADR 0001, validated checkpoints, art workflow,
style/motion/asset contract, experiment template, canonical director and assisted /
benchmark / setup references, prior Luna brief/results/postmortem/A recipe and
preparation/pass-02 records, plus guardrails plan/verification. Canonical discovery
symlink resolves to `../../tools/pixel-art-director`; the earlier guardrails record
reports 32 regression tests and eight scenario decisions, with PyYAML validator
unavailable. This audit ran no art tools, model trials or regression suite and claims
no fresh image review, original preservation audit or runtime proof.

Only this new plan file was written. Next owner: parent dispatches the small
documentation integration and checks, prepares/validates the shared frozen inputs,
then dispatches the two independent requested contestants. User retains artistic
selection. Original artwork, existing trial outputs, configuration and publication
remain outside this audit's changes.
