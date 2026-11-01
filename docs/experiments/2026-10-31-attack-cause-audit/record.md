# Attack proportions and F9 bag attachment: cause audit

31 October 2026. Requested through `ask-matt`; routed to retrospective, using the
retro and writing-for-agents procedures. Investigation only: no artwork repair,
workflow rewrite, installation, commit or publication. Existing dirty work retained.

## Finding

The strongest supported cause is incorrect construction decisions followed by
insufficient visual rejection. Generated poses supplied inconsistent anatomy and
prop drawings; agents preserved too much of that geometry and repaired connections
as pixel joins. The written workflow already required proportion and attachment
review. Its execution failed, and its mechanical evidence could not judge those
qualities. Model visual reasoning contributed: several reviews confidently accepted
relationships that the user subsequently rejected. This is not evidence of an
Aseprite/Godot rendering fault or a controlled ranking of model capability.

User clarified the current defect: **handles joining the bag in F9**. The latest
candidate's prior positive attachment assessment is withdrawn for that junction.
This is a static, inspectable defect; lack of continuous playback perception does
not excuse missing it.

## Evidence and causal chain

### 1. Generated pose geometry became the construction baseline

The original [plan](../2026-10-30-tote-attack/plan.md) and
[artist profile](../2026-10-30-tote-attack/artist/phase-plan.md) correctly called
the sheets pose proposals, required anatomical landmarks against neutral, and
kept the .4333/.264 family scales provisional pending that review.

Actual [initial assembly](../2026-10-30-tote-attack/artist/build_attack_seed.py)
resized equal sheet panels. Bags crossing panel edges were cut; unrelated fragments
survived. The [rescue preparation](../2026-10-30-tote-attack/artist/sol-rescue/prepare.py)
recovered complete silhouettes but retained the same family scales and source
anatomy. A common scale within a sheet preserves its inconsistencies relative to
the neutral character. Ground registration fixes placement, not body proportions.

The preserved [full-cycle diagnosis](../2026-10-31-full-attack-repair/record.md)
records visible denim starting near y68 in neutral and y80 in old pickup, with
broader source heads/upper bodies. Those are composite landmarks, not layer bounds.
Fresh inspection of both source sheets and current full-cycle contacts confirms
the inherited body/prop differences. Source inputs were suggestions; responsibility
for reconciling them remained with the constructing and reviewing agents.

### 2. The native parts were not anatomically isolated

[Native assembly](../2026-10-30-tote-attack/artist/sol-rescue/build_native_inputs.py)
used spatial polygons for the tote, horizontal head cuts around y42/49, and a lower
body cut at y105. Thus a layer named torso includes upper jeans, and a tote owner
can contain sleeves/hands/denim. Editable layers were proven; anatomical ownership
was not. Treating these labels as anatomy misled both edits and later measurements.

The first head transplant had already produced a doubled neck; the rescue retained
the source head/neck to solve that local issue but retained identity/scale drift.
The latest [repair pass01](../2026-10-31-full-attack-repair/build_pass01.py) then
applied a fixed piecewise body transform to all owners, stretching a hanging bag
with the leg region. This was caught and rejected. Later
[pass03](../2026-10-31-full-attack-repair/build_pass03.py) separated bag scaling from
body scaling, reused neutral head/pants where selected, and patched exposed areas.
That improved proportions but still inherited the old bag's form and used manually
specified local joins. These are construction decisions, not unintended tool output.

### 3. Exact current F9 failure: joined lines without a convincing fabric attachment

Current native: `../2026-10-31-full-attack-repair/source/attack-repaired.aseprite`.
SHA256: `5fb9a4f776ea46df1ee86c3eb5e10c8be32b094aa265004e908e832b7f4518ea`.

In [finish_pass03.py](../2026-10-31-full-attack-repair/finish_pass03.py), line23
chooses F9 endpoints (153,96) and (173,90). Lines39–45 erase old bag/handle pixels
above a straight line through those points. Lines47–51 draw four converging strap
paths and a straight rim segment. The final native places the entire handle/rim
owner **behind** the bag owner, with hands above both.

[Fresh native inspection](f9-inspection.json) confirms both endpoint positions
are opaque on the bag owner, covering the corresponding handle pixels. The
[8× decomposition](f9-ownership-8x.png) shows the retained bag top and triangular
handle drawing separately. In the composite, the left branch has a projecting,
hook-like end, the other meets the sloped top, and front/back rim and strap
attachment relationships remain poorly expressed. Visual diagnosis: this reads
as a loop stuck onto a pouch, rather than straps continuing into the bag fabric.
There is no requirement that every real tote expose four attachment points; the
missing piece here is a convincing chosen arrangement and overlap, not a point count.

Opaque contact is therefore true but insufficient. Merely moving the whole strap
layer above the bag would not establish the correct front/back relationship either.
The attachment, rim, and nearby fabric need to be designed together. This audit
does not supply or claim a repaired pose.

### 4. Review accepted a weaker property than the requested result

The [old closure](../2026-10-30-tote-attack/review/review.md) explicitly withdraws
its positive grip assessment after user rejection. The subsequent
[comparison probe](../2026-10-31-comparison-regression/visual-probe.md) also records
a fresh critic falsely clearing a known defect and citing incorrect coordinates.
Its [comparison helper](../2026-10-31-comparison-regression/record.md) deliberately
checks scope, coverage and freshness; it does not judge anatomy or grip.

The latest [review](../2026-10-31-full-attack-repair/record.md) again described
F9/F10 as continuous loops at the rim. That statement was too favorable about the
attachment. Detailed attention to hands, F8 separation, alpha scraps and reproducible
delivery did not resolve the F9 bag junction. A correct crop or successful native
rebuild makes a bad drawing inspectable and repeatable; it cannot make it convincing.
The primary agent owns that failed review, including the latest delivered candidate.

## Attribution and uncertainty

| Factor | Supported conclusion |
| --- | --- |
| Source/reference quality | Inconsistent generated body/prop geometry was a contributing input, not an instruction to preserve defects. |
| Construction method | Direct cause: scale/registration substituted for anatomical reconciliation; rectangle/polygon partitions mixed anatomy; local strap paths were patched onto inherited bag geometry. |
| Workflow execution | Major cause: planned anatomical/attachment checkpoints did not reject demonstrably weak keys before full-cycle assembly and delivery work. |
| Written workflow | Already contains the relevant requirements. Comparison improvements address evidence quality, but semantic judgment remains an unreliable gate. More generic instructions would not demonstrate a solution. |
| Art-lab tools | No observed renderer/export corruption explains these defects. Current F9 native and exported visible RGBA match. Historical rebuild also reproduced the exact authored file. This supports a construction/review failure, not a general claim that the tools are bug-free. |
| Model capability | Repeated false visual clearance and incorrect ownership/coordinate interpretations demonstrate task-specific limitations. A stronger-model retry alone has not solved the process. Different prompts, tasks, inherited sources and correction stages prevent a fair model ranking or a claim that no model can do it. |
| Context pressure / review budget | Plausible contributors; artifacts do not isolate their causal effect. No claim about hidden reasoning, actual served primary model ID, or a measured context-degradation threshold. |

## Recommended next experiment, in priority order

1. Resolve F9's bag construction as one visual unit: bag mouth, front/back fabric,
   strap roots, overlap and hand tension. Use the existing original reference to
   establish which bag is being represented. Review a simple structural drawing
   before restoring detailed shading. This is a proposed next task, not executed.
2. Check that same bag construction in F8/F9/F10 at a common scale, then the carried
   neutral. Explain deliberate squash, rotation and occlusion. A constant 2D bounding
   box or opaque area is not a valid physical-volume rule.
3. Preserve anatomy using a small visible landmark sheet: head, shoulder, pelvis,
   knees/soles, with limb proportions and intentional pose changes. Validate actual
   composite forms and actual part ownership before transforms. Existing written
   rules cover this; make the evidence concrete at the key checkpoint.
4. Keep the existing export/freshness/coverage checks, but let visual uncertainty
   about the exact requested relationship fail the agent's checkpoint. Reopen the
   clean composite without producer praise and require the reviewer to trace the
   chosen strap roots/overlaps. Another model's confident verdict is not proof.
5. If comparing models is desired, use identical frozen inputs and a bounded F9
   construction task, the same tool/budget conditions, and blind user comparison.
   Current sequential rescues are not that experiment. Do not promise a winner.

## Verification and delivery boundary

Ran `inspect_f9.py` using the existing bundled Python. It independently reads the
current native, verifies F9 visible RGBA equals candidate-8.png, records layer order
and endpoint pixels, and generates labeled nearest-neighbor diagnostic crops.
Native hash matches the delivered candidate. Source drawings and operations were
read; historical mechanical/runtime proofs were inspected, not rerun. No engine
run is needed to establish this native still-image defect. No broad tests claimed.

Changed only this audit directory, a status correction in the prior repair record,
and the handoff. All art stays unchanged. Investigation complete; F9 attachment
remains unresolved. Next owner: agent, on a separately requested repair, using the
bounded structural experiment above. User remains art director, not manual painter.
