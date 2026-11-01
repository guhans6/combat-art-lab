# Research: comparing a repair without overlooking regressions

Research/access date: 31 October 2026. Scope: read-only repository inspection,
actual image inspection and a bounded primary-source search; recommendations for
the separate planner. No artwork/native edits, editor launch, installation,
engine run or publication. The working tree already contains substantial changes;
they were preserved. Repository delivery guidance establishes no additional DoD.

## Finding

Add a small, source-bound comparison packet to the existing director helpers,
then require separate observations for the intended improvement and regressions
throughout the changed content and its connected context. Exact pixel detection
can make omissions visible and fail incomplete evidence. It cannot decide whether
a hand convincingly grasps a strap. A fresh critic can still miss that judgment.

The tote failure is an observed false clearance, not a missing native/export test.
[The superseding rejection](../2026-10-30-tote-attack/record.md) and
[withdrawn review](../2026-10-30-tote-attack/review/review.md) identify native v03,
SHA256 `1f6d68c6927bbcc594be9913156f74a6b0939aa373a9be9971dcd5be8ab52065`,
as rejected for recovery grip/handle readability. Earlier source/export/Godot
results remain evidence only for their stated technical boundaries.

I visually opened the actual
[recovery comparison](../2026-10-30-tote-attack/review/recovery-before-after-3x.png)
and the supplied user crop, subsequently frozen as
[inputs/user-rejected-grip.png](inputs/user-rejected-grip.png).
The candidate changes both forearm contours, cuffs, hand mass and strap paths;
the junction reads as an ambiguous angular meeting rather than clearly wrapping
fingers around supported handles. This is a visual interpretation consistent with
the rejection, not a semantic fact established by pixel connectivity. The full
before/after already exposes these changes: another ordinary side-by-side alone
would repeat a demonstrated insufficient review. An enlarged relevant crop helps
attention; its existence would not guarantee a correct verdict.

## Existing capabilities and actual gap

- [pixel_checks.py](../../../tools/pixel-art-director/scripts/pixel_checks.py)
  already canonicalizes RGB under zero alpha, detects every visible RGBA change,
  checks an editable mask, reports changed bounds/examples, and makes a baseline /
  candidate / difference sheet with a full 1x row and an integer-zoom crop. Its
  crop label is currently hardcoded to “Head crop”. It neither proves crop coverage
  of all changes nor binds a completed visual decision to that evidence.
- [reference_review.py](../../../tools/pixel-art-director/scripts/reference_review.py)
  already records source hashes, crops, dimensions and resampling, refuses evidence
  overwrite, and warns that matched crop heights do not establish anatomical
  alignment. It compares an original to an export, rather than tracking all
  baseline-to-candidate regressions.
- Existing alpha coverage deliberately tests transparent gaps, with optional solid
  masks. It does not understand hands, straps, overlap order or grip.
- [build_review.py](../2026-10-30-tote-attack/build_review.py) constructs the known-bad
  comparison from `artist/checkpoints/recovery-source-v00.png` and the actual
  recovery frame selected through `artist/delivery.json` (F9, zero-based 8).
  It supplies faithful full views but no difference map, coverage audit or explicit
  regression observations. **The historical pair is not registered:** the seed is
  256×192 and the final is 320×192, freshly confirmed with `file`; the builder places
  both at their panel origin without anatomical registration. It is a pose/reference
  comparison, not an exact same-coordinate edit comparison. Native v02/v03 have
  nearly the same F9 repair; the
  [v03 focused check](../2026-10-30-tote-attack/artist/sol-rescue/review/v03-focused-correction-checks.json)
  mainly verifies later foot registration/canvas-edge corrections. Comparing only
  v02 to v03 would omit the original grip redraw that the user rejected.
- The existing native/reopen readers and delivery manifest can establish export
  identity. Flattened PNG comparison still cannot reveal hidden layer damage.

The integration should reuse these capabilities. The failure supports stronger
execution and evidence accounting of the existing visual gate, not a claim that
the project had no visual review rules or that reviewers never opened the image.

## What the primary sources support

Six primary sources were inspected; all accessed 31 October 2026. These sources
document mechanisms or specific research results, not validation on this sprite.

| Source and date/version | Supported result | Application and limit |
| --- | --- | --- |
| [Pillow ImageChops documentation](https://pillow.readthedocs.io/en/stable/reference/ImageChops.html), served 13.0.0; publication date unstated | `difference` computes absolute per-pixel channel differences. | Exact difference maps are practical with the existing dependency. Difference magnitude does not distinguish an intended improvement from damage. |
| [Pillow Image documentation](https://pillow.readthedocs.io/en/stable/reference/Image.html), served 13.0.0; publication date unstated | `getbbox` defaults to alpha-only behavior for images with alpha; nearest-neighbor resizing must be selected explicitly because common resize paths default to bicubic. | Avoid testing RGBA difference emptiness through alpha alone: opaque color edits can have zero alpha difference. Reuse the repo's canonical tuple comparison and single-channel binary difference mask. Use explicit nearest-neighbor integer zoom; do not change production pixels to align a review. Local installed compatibility remains separately testable. |
| [GitHub image-diff documentation](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files#viewing-differences), undated current docs | GitHub supplies 2-up, swipe and onion-skin views; onion skin helps expose small positional shifts. | Shared-coordinate views and an optional toggle/overlay are established inspection tools. They do not guarantee detection or semantic correctness. A simple PNG packet is sufficient for the first integration. |
| [scikit-image `label` documentation](https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.label), served 0.26.0; publication date unstated | Components join equal-valued neighboring pixels under a declared connectivity; 2D connectivity can include or exclude diagonals. | Component bounds can enumerate disconnected change regions. Geometric adjacency has no representation of skin, strap, depth or load. No new scikit-image dependency is needed: a small existing-style flood fill suffices if components are useful. |
| [Hwang et al., *Fooling the LVLM Judges*](https://aclanthology.org/2025.emnlp-main.1182/), EMNLP November 2025 | The authors report image-induced bias in all tested judges on their T2I benchmark; pairwise evaluations and prompt mitigations remain vulnerable. | Independent vision critique is fallible evidence. This inspected abstract does not measure current Sol sprite anatomy accuracy or prove the cause of this failure. The full PDF could not be fetched by the web tool, so finer results are not relied on. |
| [Rensink, *The Need for Attention to See Change*](https://www2.psych.ubc.ca/~rensink/flicker/), author-hosted account last updated 20 November 2011, linking the 1997 primary experiment | Its interrupted flicker paradigm demonstrates substantial human difficulty noticing changes without attention to the relevant object. | Supports directing review to enumerated changes rather than relying on memory. Human flicker findings are not proof of LLM anchoring, nor evidence that flickering GIFs improve model inspection. |

No benchmark found in this bounded search establishes reliable automatic judgment
of pixel-art hand/strap occlusion. Earlier positive review prose may have anchored
the parent, or attention may have stayed on neck/crop repairs; these remain
hypotheses. The records prove the mistaken clearance, not its internal cause.

## Smallest reusable integration to plan

1. **Bind the exact pair and scope.** Use an explicit baseline with its role
   (approved / retained / rejected diagnostic), candidate export, frame number,
   editable mask and named review regions. Record file hashes, dimensions, crop
   coordinates, common matte and display zoom. Keep the approved reference separate
   when pose/style judgment needs it; an unapproved seed is not an approved outcome.
   Record the candidate native hash and the export/readback verification used to
   connect it to this PNG. Hashes alone establish file identity, not native-to-PNG
   correspondence. A later artifact change invalidates this packet's clearance.
2. **Detect changes on the original shared grid.** Let `D` be the canonical RGBA
   changed-pixel set. Reuse the exact checker; do not use perceptual tolerances,
   antialias suppression or a percentage-of-image allowance for protected pixels.
   Refuse unexplained size/registration mismatch rather than automatically fitting
   bounds. Keep a raw comparison even if a labeled translated diagnostic is needed.
   Check all affected frames, including hidden-owner/native protection separately.
3. **Account for every change, then inspect context.** Distinguish allowed edit mask
   `M` from the union `R` of close-review regions. Report `D − M` (scope violation)
   and `D − R` (uncovered close-review changes), with counts/bounds/examples. Crops
   must use the same source coordinates on both sides. An automatically added
   uncovered-region crop is acceptable if its subsequent inspection is recorded;
   automatic generation alone does not complete review. A whole-image overview
   must not silently count as close-review coverage. Inspect broader connected
   context even when unchanged: cuff → wrist → fingers → handle → bag rim here.
   A regression inside `M` can pass every scope/coverage check and still require
   rejection by visual judgment. Exact coverage is bookkeeping, never an art score.
4. **Make one packet easy to inspect.** Retain full baseline/candidate/difference
   at 1x, matched integer zoom, and explicit named contextual crops with the changed
   pixels highlighted in separate panels. Keep clean views alongside highlights;
   marks can obscure the junction being judged. For animation add corresponding
   neighboring keys and authored-speed playback; still inspections prove no
   continuous motion perception. Reuse native/export sources rather than screenshots.
5. **Require two distinct decisions against the packet.** State whether the target
   improved and what changed around it. For each changed region and its important
   joins, record concrete observation and pass / reject / uncertain, with coordinates,
   frame, scale and reviewer role. Example question: “Which hand edge covers which
   handle, where does each visible handle reappear, and does it reach the rim?”
   Do not answer merely “connected”. Include a full-asset scan for silhouette,
   proportions, expression and material changes. A disputed/uncertain structural
   join means no eligible improved result; preserve the candidate and last baseline.
6. **Keep the critic independent and bounded.** A fresh critic receives exact
   artifacts, task and locks, without prior praise or artist rationale as the
   premise. Ask it to describe visible relations and actively find regressions
   before seeing the producer's conclusion. It must cite viewed files/regions and
   uncertainty. This is a mitigation proposal, not proven debiasing. An edited
   critic output needs fresh inspection; avoid critic/editor self-clearance and
   repeated reviews until one says pass. User visual approval remains separate.

The reusable path should be still/frame based and part-neutral. A narrow animation
adapter can supply frames/timing; it should not force idle-specific or tote-specific
rules onto unrelated artwork. Prefer one helper extension plus one comparison
reference/procedure linked from the existing skill/workflow. Avoid another scoring
system, a new backend, or a broad workflow rewrite.

## Known-bad replay: useful proof and honest boundaries

The planner should run the **real** registered pre-repair F9 preparation → v03 F9
pair in a new experiment directory. Parent identified
`../2026-10-30-tote-attack/artist/sol-rescue/preparation/frame-09-base.png` as the
320×192 baseline in the same native coordinates; implementation must verify its
provenance before using exact changes. This is a diagnostic pre-repair baseline,
not user-approved art or necessarily the last native revision. Preserve the old
256×192 comparison separately as a labeled nonregistered reference view. Record
both actual input hashes and frame binding. This tests whether the packet exposes
the real forearm / hand / handle differences rather than only a synthetic fixture.

| Replay | Expected observable evidence | Cannot establish |
| --- | --- | --- |
| Old 256×192 seed → 320×192 final | Exact-edit mode refuses canvas mismatch; a reference view explicitly records noncomparable registration. | An independently fitted pixel drift mask is valid. |
| Target-only grip or neck crop on the registered real pair | Any changes outside that crop are explicitly uncovered; the gate blocks incomplete close-review evidence or adds separately inspected crops. Parent reports a curl-tip correction outside the grip ROI, a useful coverage challenge. | That uncovered changes are artistically bad. Scope is not reconstructed retrospectively as if approved. |
| Complete relevant crops and real v03 F9 | Packet includes forearms, hands, handles and rim; coverage can pass while the visual decision retains the already documented user rejection. Fresh critique, if actually performed, records its own judgment separately. | A detector independently discovered the semantic defect. A rejection copied from the known label is not an independent recovery-rate result. |
| Intentionally broken review provenance/coverage fixtures | Altered candidate hash, omitted affected frame, invalid crop, or missing coverage causes a clear mechanical failure. An identical image can produce an honest no-change packet rather than invented improvement. | General artistic quality or runtime behavior. Fixtures supplement rather than replace the real pair. |
| Future new bounded repair, only if separately requested | Exact checks plus observed improved grasp/occlusion and surrounding/global regression review on the new source-bound packet. | Production/user approval merely from a mechanically complete packet. |

Research did not execute the replay. The parent separately inspected the registered
pre-repair pair; its observations are inputs to the planner, not tests run here.
A read-only numerical probe failed because the
default `python3` lacks Pillow; no installation was attempted. Existing repo
records cite a Pillow-enabled environment, which the implementation owner should
locate/reuse before adding dependencies. This does not affect the actual image
inspection or the source-code findings above.

Next owner: separate planner to choose the bounded helper/procedure changes and
acceptance evidence; implementation follows that plan. No replacement sprite or
new artistic clearance is delivered by this research.
