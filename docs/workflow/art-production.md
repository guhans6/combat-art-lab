# Combat Art Workflow

## Purpose

Find a repeatable way to make the intended visual style and responsive combat animation with AI assistance. The user directs the art, evaluates results, and learns the relevant basics. Agents do the asset construction, revisions, technical setup, and verification.

The first result is a small, inspectable proof of the art pipeline. It is not a commitment to produce a complete game or a large asset library.

## Accepted direction

1. Explore the visual direction with reference analysis and concept images.
2. Assess reference feasibility and compare representative native scales where fidelity is uncertain, then write explicit visual and motion rules.
3. Have AI construct editable assets through the chosen editor, scripts, drawing operations, layers, or a rig.
4. Complete one representative combat attack.
5. Play it in Godot at the intended screen size and gameplay speed.
6. Make a deliberate art revision and a timing revision before expanding production.

The user's inability to draw is a pipeline constraint. Do not make manual repainting of generated PNGs the default handoff. If an agent cannot produce or revise an acceptable result, document that limitation and propose a concrete alternative.

## Multi-reference and assisted construction — 27 October clarification

Preserve the approved character's identity, aesthetic, expression and vibe. Small
differences and intentional simplification are acceptable. Reference-guided tracing,
source-derived shapes/colors, conversion followed by cleanup and hybrids are permitted.
Keep raw references, converted seeds and finished native candidates distinguishable;
a flat untouched import alone does not demonstrate practical native editability.

Obtain additional heads, expressions, views, simplified production images, coherent
sheets or individual poses when they solve a named need. Use an available authorized
image tool with canonical originals attached. If unavailable, give a complete prompt
in an editable writing block, exact attachment paths and expected returned image.
The [kit prompt pack](../experiments/2026-10-27-assisted-head-comparison/inputs/pixel_art_reference_lab/prompts/README.md)
supplies request templates. Review generated references for identity/style consistency
and record accepted-for-use, needs-correction or rejected; agent use status is separate
from user visual approval. A reference's role may be identity, style, expression, pose,
visibility, lighting or production simplicity.

For uncertain construction fidelity follow the [bounded comparison plan](../experiments/2026-10-27-assisted-head-comparison/inputs/pixel_art_reference_lab/workflow/FIRST_EXPERIMENT.md):
one identity-rich crop, fixed grid/framing/palette policy, trace-guided versus converted
plus cleaned, comparable bounded effort, then a hybrid only for an observed failure.
Historical redraws are context. Show original, generated intermediate if used, raw seed
and actual exports; inspect 1x and integer zoom and label any projected display size.
Review identity, expression, style, proportions, pixel craft and editability separately.
Keep failed attempts and a localized revision/reopen proof. Motion follows a convincing
static checkpoint and the motion guide; final user selection remains explicit.

## Automation and model routing — proposed next-study default

Use source-guided preparation for the next studies of the approved character.
The [automation analysis](../research/source-guided-automation.md) recommends conversion
into a structured seed, aligned original guidance and bounded native cleanup, informed
by the existing assisted-head comparison. Trace-only drawing remains available for a
specific failed region. This is a testable production proposal, not final asset approval.

Scripts own repeatable crop/scale/palette/mask application, bulk color fills, layer
assembly, export and protection checks once the recipe is frozen. Agents still choose
or review ambiguous crops, semantic ownership, feature budgets and simplification.
Known coordinate/color patches need no model reasoning. For an ambiguous eye, mouth,
or expression, follow the director's detailed [face-likeness procedure](../../tools/pixel-art-director/references/face-likeness.md)
before freezing a mask: register landmarks and confidence, read actual visible native
ownership, then judge morphology/contrast in feature, head, and full-asset context.

For this project, Luna6 Max is the currently tested route for routine drawing;
Terra implements routine workflow/documentation work; Sol6.1 at high reasoning owns
critical final likeness/expression review and a bounded rescue where the task warrants
it. Record actual identifiers and host availability. The user may override this
routing; if a chosen route is unavailable, stop to reselect rather than silently
substituting. These are local workflow choices, not portable model-quality claims.
One automatic Sol/high critic is the maximum per user task. A critic may suggest an
edit or make one scoped rescue within the existing budget, but its edited candidate
needs fresh independent inspection and remains pending user visual selection. Routine
nonfacial pixel work does not require a new Sol review.

Cheaper vision/tool-capable models are candidates for explicit local repairs; strong
visual review remains appropriate for eyes/expression, hair structure, likeness and
cross-pose coherence.
The [new experiment plan](../experiments/2026-10-27-automation-routing.md) tests
tier adequacy on identical seeded inputs; no cost or quality equivalence is established.

Keep raw converted drafts, tracing underlays, meaningful native masters and
user-approved final assets distinct. Exclude guides from exports; review masks and
every affected frame. Color alone is not evidence for deletion, and small clusters
or holes may be intentional. Preserve native protections and the current asset checker.
Count inherited setup, actual retries and reviewer/rescue effort separately when
measuring economy. The user directs and selects results; agents own all sprite edits.

### Experiment intent and seed review

Before preparation, state whether the work is a production/reconstruction study, a
model comparison, a method/recipe or source comparison, or an exploratory
end-to-end pilot. A model comparison freezes identical references, derived seed
pixels, crop/grid/transform, alpha/palette treatment, masks/ownership, native
baseline, task and budget for every contestant; verify hashes and decoded seed
equality before drawing. A method or source study instead declares the variables
that differ and attributes any result to that combined recipe where several differ.
An intentionally weak common seed is valid for a named repair task. Equal originals
alone are not equal starting conditions, and no filter, palette count, model, or
historical profile is the default winner.

Before dependent cleanup, inspect the approved original, raw seed, and seeded native
export where available at 1x and matched integer zoom, including identity-rich crops
and full context. Record recipe/source role and hash, crop/dimensions/transform,
alpha/resampling/palette/dither policy, mask provenance, versions and seed hash.
Choose explicitly: suitable for the named task; suitable only for a stated bounded
repair; or re-prepare/a separately labelled reconstruction study. A seed need not be
perfect: an observed, reference-supported eye, mouth, expression, or structural
defect may be repaired within a stated region, while unrelated defining features stay
protected. Later recipe changes create a new arm rather than preserving a same-seed
claim. The [Luna pilot postmortem](../experiments/2026-10-29-luna-independent-trials/postmortem.md)
is local evidence for these guardrails, not a general model ranking.

## Decisions still open

Pixel art is not selected merely because Aseprite is available. Camera perspective, character proportions, asset resolution, palette limits, outline treatment, animation method, and tools remain open until references and a small test justify them. Godot is the intended engine.

Aseprite, its scripting API, an MCP integration, specialist generation services, 2D rigs, and 3D-to-sprite rendering are candidate tools or routes. Installing a connector or creating a valid file does not establish that it can achieve the intended art quality.

### Reference intake and representation choice

Before selecting a construction route, record the authority and role of each reference;
camera/view; observed pixel, illustrated, or other edge/shading behavior; silhouette and
identity cues; intended native and display scale; palette/color relationships;
lighting/material separation; motion needs; and the required native revision boundary.
Record uncertainties and the smallest useful test. Select the recipe and backend from
that target contract, not from the currently installed editor. The current character's
facial landmarks and 128×192/192×288/256×384 grids are conditional pixel-study
examples, not defaults for another reference or rendering route.

## Milestones and gates

### 1. Establish the visual target

**Work**

- Collect a small, relevant set of references supplied or approved by the user. Include motion references when animation is part of the appeal.
- Describe the qualities to carry forward: silhouette, proportions, shape language, color relationships, contrast, surface detail, lighting, pose exaggeration, and motion rhythm.
- Separate these qualities from recognizable characters, costumes, symbols, or compositions that should not be carried into the original design.
- Produce a few meaningfully different concept candidates. Change one or two important variables per comparison so the user's feedback is actionable.
- Ask what the user likes or dislikes in concrete terms. Update the next candidates accordingly.

**Outputs**

- Reference register with links or file paths, provenance, and notes on what each reference contributes.
- Dated candidate images and a short decision log.
- An approved visual direction, with unresolved questions called out.

**Go criterion:** the user can identify a candidate and explain which qualities to preserve. A pleasing image alone does not prove animation feasibility.

**If unresolved:** continue bounded concept exploration; do not mass-produce assets or select a production tool by habit.

### 2. Assess reference feasibility before drawing

**Work**

- Select **new reconstruction**, **assisted reconstruction**, **local correction**, or **animation** explicitly. For animation construction, revision or diagnosis (including idle and blink), follow the [motion guide's animation procedure](../art/motion-guide.md#animation-procedure). A correction inherits the approved asset's locks; a new reconstruction can test new grids in separate files. The frozen v03 correction benchmark does not define the limits of fresh construction.
- Inspect the approved scene and close-up, with any extracted cutout as supporting evidence. Separate identity features, secondary detail, and atmosphere using the [style guide](../art/style-guide.md).
- Open the actual original images visually before construction and record their paths and concrete observations; a prose summary or prior sprite alone does not complete this step. If image delivery is unavailable, stop drawing and report that gap.
- Record approximate feature footprints on each proposed native grid: face envelope, near/far eye clusters, fringe openings, cheek/jaw, and hair tie. State which cues appear supportable and which collide or disappear. These are design observations, not a calculated likeness score.
- Look for inconsistent apparent pixel sizes, fine texture, smooth or resampled edges, and baked lighting. Record visible evidence and uncertainty; do not assume all generated images have these defects or infer the generating model's internals.
- Propose simplifications in priority order and identify any loss that would change identity, orientation, expression, or proportions. Treat those as study questions rather than silently replacing the design.

**Output:** a concise feasibility brief in the experiment record: exact reference paths, essential cues, secondary details, atmosphere, candidate grids/display sizes, expected simplifications, confidence, risks, and smallest study.

**Go criterion:** the next drawing pass has a specific visual question and an explicit preservation hierarchy. If the head is uncertain, study the head and upper body before rebuilding the environment.

### 3. Compare native resolution and rendering where uncertain

This stage applies to new reconstruction with uncertain fidelity or scale. A local correction inherits its frozen grid, palette policy and protection mask; proceed through its scoped construction/review checks without requiring a multi-grid study. If the correction exposes a grid limitation, finish or stop that run honestly and propose a separate reconstruction variant.

**Work**

- For this character's pixel studies, existing 128x192 standing art is a baseline and 192x288/256x384 equivalent full-character scales are comparison candidates, not selected production sizes. Another target selects and records its own scale evidence. A crop study records its dimensions, full-character equivalence and common framing.
- Construct or transfer source-guided shapes/features at each grid and finish the native candidates deliberately. Record source-derived seeds separately from completed art. Nearest-neighbor enlargement alone adds no detail. Compare methods at one grid before attributing improvement to resolution; a reduced reference may become a seed, with semantic organization, cleanup and revision evidence required for a completed master.
- Hold orientation, design, broad material colors, lighting and framing comparable. Declare any differences in construction effort or detail strategy; one attempt per grid cannot isolate resolution from drawing skill.
- Before detail, map a shared reference crop and approximate hair-top/eyeline/chin/neck/shoulder landmarks into normalized coordinates for each grid. Inspect matched-display silhouette/large-plane blockouts. Correct mismatched head size/position or crop at this checkpoint; matching crop-canvas dimensions alone does not establish comparable anatomy. A budget-exhausted mismatch is an inconclusive attempt, not a resolution test result.
- Save and visually inspect **approved original alongside actual export** at each meaningful blockout/revision, including after coordinate scaling or recomposition. Record the original-image crop, candidate size, display resizing, visible deviations and continue/correct/reject decision before the next drawing stage. Existing reconstruction panels may supplement this sheet; they cannot replace the approved original. The director's [reference-review helper](../../tools/pixel-art-director/references/reconstruction.md#produce-direct-reference-evidence) automates sheet/metadata creation, not likeness judgment.
- Retain native sources, authored operations, all passes and a local edit/reopen proof. Record actual elapsed intervals and observable operations with their boundaries; unknown usage remains unknown.
- Show each candidate at 1x, integer nearest-neighbor zoom, and matched displayed character height. Label any fractional resampling. If game-view scale is not selected, call the display comparison a diagnostic rather than gameplay evidence.

**Output:** a small comparison and independent visual observations using the rubric below. See the [current feasibility study](../experiments/2026-10-27-resolution-feasibility/record.md) and [research](../research/concept-to-native-pixel-art.md).

**Go criterion:** evidence supports a provisional grid/rendering strategy for the next pass, or identifies a precise unresolved feature. No larger grid wins by default. User selection remains separate from the agent's recommendation.

**Reject criterion:** materially wrong facial orientation, eye relationship/expression, hair silhouette, proportions or clothing structure invalidate a fidelity/resolution comparison. Correct within scope and budget or stop as a rejected construction attempt. Passing native-file checks cannot waive this visual decision, and rejection does not prove the reference impossible at that grid.

### 4. Write the production style and motion rules

**Work**

- Translate the chosen concept into observable requirements. Record the intended game-view scale before deciding how much detail a sprite needs.
- Define proportions, distinctive features, palette relationships, outline/shading behavior, facing conventions, and which details may simplify in motion.
- Define the motion character: deliberate or snappy, grounded or airborne, restrained or exaggerated, with examples of acceptable poses and timing.
- State what can change between actions and what must stay consistent. Keep character art and attack effects distinguishable during inspection.
- Record native canvas and visible height, projected display height/filter, feature priorities, hair masses and fringe openings, facial angle/expression, material ramps, outline/anti-aliasing policy, and sprite/background detail relationship. Separate base shading from proposed scene light, grading and effects; mark untested rules provisional.

**Outputs**

- A compact style guide with an approved character view and annotated examples.
- A motion guide describing one representative attack's anticipation, active/contact phase, follow-through, and recovery.
- A provisional technical specification: camera/view, asset scale, transparency, anchors, and intended import/export format. Mark tentative decisions as tentative.

**Go criterion:** another agent can describe what to construct and how to judge it without inventing major design choices.

**If unresolved:** resolve the specific missing requirement with a visual comparison or a focused question.

### 5. Prove editable asset construction

**Work**

- Select the smallest toolchain capable of the required style. Prefer existing repository capabilities before adding integrations.
- Have the agent construct one representative character pose in the native production format. Depending on the route, preserve useful layers, source scripts or drawing operations, separate body parts, or a rig.
- Establish silhouette, proportions and major value planes before texture and accents. Preserve reference identity through intentional simplification rather than attempting every illustrated mark.
- Inspect the result at native/game size as well as enlarged. Check the actual asset rather than only an attractive presentation image.
- Request a localized revision, such as changing the weapon shape or a costume accent. Reopen the native file and inspect the result.

**Outputs**

- The editable source and any scripts or parameters needed to reproduce it.
- A transparent runtime preview and an image showing the source structure.
- Before/after evidence of the localized revision, including any unintended changes.

**Go criterion:** the asset matches the selected direction closely enough for the test, has meaningful editable structure, and can be revised without losing unrelated approved features.

**If unsuccessful:** identify whether the limitation is the tool interface, the agent's construction quality, the representation, or the style's complexity. Try a targeted correction or compare another route. Do not describe a flattened image imported into an editor as a fully structured asset.

### 6. Inspect appearance and revise structure first

Compare the actual export to the approved reference at native size, integer zoom, intended display size, and representative background context. Where the game camera is unknown, record the assumed display size and leave gameplay acceptance pending. A static composite is appearance evidence, not Godot playback.

Carry the direct original/candidate sheets and decisions forward from construction; a final comparison only against earlier reconstructions can hide accumulated drift. Preserve rejected attempts and avoid recommending a grid from a candidate that fails the structural/likeness review. See the [reference-drift audit](../experiments/2026-10-27-reference-drift-audit/record.md) for observed failure evidence and the limits of the remedy.

Use the rubric below to name concrete defects. Correct orientation, skull/hair mass, eyeline, cheek/jaw and body proportions before eyelashes, isolated strands or seam accents. Make one coherent revision per pass and preserve checkpoints. A successful local pixel change is evidence of edit control, not necessarily of improved likeness.

For every actual pass, retain the native checkpoint/export, operations and technical
result. Inspect original, seed, best eligible prior, and new candidate at 1x and the
same integer zoom; use aligned face crops for facial work and full context for
proportions. Verify that comparison sheets name the exact exports and have no clipping,
matte, scale or missing-region defect. Record a visual decision independently of
technical status before advancing. Identity or expression regression is
noncompensable: clean files, lower cost, extra edits, or stronger pixel craft cannot
select that candidate. A failed candidate may support a bounded corrective branch, but
cannot become the baseline for dependent production until the visual gate is met.

Stop micro-editing when the next pass cannot identify a visible, reference-supported improvement, the declared pass budget expires, or an essential feature repeatedly merges on the current grid. Preserve the best candidate and unsuccessful attempts. Start a separately labeled structural/grid/rendering variant where warranted; keep protected correction areas locked until scope changes explicitly permit a new variant.

After each review, name the best retained checkpoint, the latest candidate's status,
the decision/reason, and the next working baseline. Select only a reviewed candidate
that meets the declared visual goal and required technical boundary; otherwise retain
or restore the best eligible prior and matching export. If none qualifies, record no
selected result. Label raw seed, awaiting review, rejected, agent-preferred/selected,
user-preferred direction, user-approved artifact, last attempted, and proof-only
edits accurately. “Final” is not a selection decision merely because it is last.

**Go criterion:** visual observations cover every relevant dimension and technical checks are separate. Under the clarified multi-reference request, an agent-reviewed convincing static study may support a separately labeled bounded motion probe while user selection remains pending. Expanding character/action production still requires user acceptance; no numeric aggregate substitutes for approval.

### 7. Prove one representative attack and runtime playback

#### Native attack

**Work**

- Choose an attack that exposes the important challenge in the desired combat style. An idle loop alone is insufficient evidence for a combat-heavy game.
- Establish readable key poses and timing first. Add drawings, interpolation, deformation, or effects where they improve the intended motion.
- Before detailed keys or cycle expansion, apply the director's [connected-form checkpoint](../../tools/pixel-art-director/references/structure.md): reference anatomy and object sites, actual native ownership, simple structural keys, then composite/owner-hide/neighbor review. Its continuation decision is required; a failed key remains a diagnostic, not an improved animation delivery.
- Maintain character identity, weapon dimensions, palette behavior, anchor positions, and facing conventions across the action.
- Keep gameplay timing explicit. Separate the art's frame count from the duration of anticipation, active/contact, and recovery phases.
- Inspect the action both with and without impact effects. Effects may enhance the action but should not be the only evidence that it reads correctly.

**Outputs**

- Editable attack source, a preview animation, and exported runtime assets.
- Timing notes and the expected contact pose or interval.
- A short defect list with fixed, accepted, and unresolved items distinguished.

**Go criterion:** the attack communicates its direction, force, contact, and recovery while preserving the chosen style and character identity.

**If unsuccessful:** revise the key poses or production method before generating additional attacks.

#### Evaluate in Godot

**Work**

- Build a minimal scene with the character, a target or dummy, and enough background to test contrast and scale.
- Run the attack from player input at its intended gameplay speed. Synchronize the target response with the planned contact interval.
- Check the start, completion, and return to rest. Check facing changes or interruption only if those behaviors belong to the current test.
- Record the running scene at actual game scale. Inspect enlarged frames only as an additional diagnostic.

**Outputs**

- A runnable Godot scene and documented controls.
- A short real playback recording or a reproducible visual review procedure.
- Findings tied to the style and motion rules: readability, consistency, timing, alignment, contrast, and transitions.

**Go criterion:** the action looks intentional and feels appropriate in play, and no unresolved defect prevents evaluating the art pipeline.

**If unsuccessful:** distinguish an asset problem from import settings, anchoring, playback, or gameplay timing. Correct the responsible layer and retest that issue.

### 8. Test revision cost and make a production decision

**Work**

- Make one art change that should propagate through the attack, such as a weapon or costume adjustment.
- Make one timing or pose change driven by the Godot test.
- Rebuild the exports and replay the scene. Confirm that approved unrelated features remain intact.
- Record agent work, user intervention, generation/service usage where observable, and recurring defects. Do not invent estimates for missing measurements.

**Outputs**

- Before/after source assets, exports, and playback evidence.
- A short assessment of what was easy, what failed, what remained manual, and whether the process is repeatable.
- A production decision: continue with this method, simplify a specific requirement, test a named alternative, or seek targeted artist assistance.
- State whether to keep the native grid, compare a higher grid, simplify named features, revise rendering rules, or test another animation/construction method. Attach observed evidence and distinguish agent recommendation from user acceptance. For frame-by-frame work, measure a key-pose revision across the tested frames before estimating a moveset.

**Go criterion:** both revisions are achievable with an amount of effort the user accepts, without repeatedly reconstructing unrelated approved work.

**Expansion:** only after this gate, add the next small animation set or a second character. Repeatability across a second asset is the next check; one successful attack does not establish that every asset is solved.

## Acceptance checklist

- [ ] The user approved a visual direction using actual examples.
- [ ] A feasibility brief separates essential identity, secondary detail, atmosphere and uncertain feature limits.
- [ ] Any grid recommendation names actual comparison evidence or is explicitly untested.
- [ ] Pixel art, perspective, resolution, and tooling choices are explicit rather than assumed.
- [ ] Visual and motion rules are specific enough to guide construction and review.
- [ ] The native source has meaningful editable structure; final PNGs are exports.
- [ ] The agent demonstrated a localized edit without unwanted redesign.
- [ ] One representative attack works, with intentional poses and timing.
- [ ] The character and weapon remain consistent through the action.
- [ ] The attack reads at the intended game scale against a representative background.
- [ ] Godot playback and target contact were actually observed.
- [ ] An art revision and a timing revision were completed and rechecked.
- [ ] Remaining manual work and failures are recorded accurately.
- [ ] The user accepts the result and effort before expanding production.

Apply the checklist to the current scope: this research task can finish without an approved sprite or attack, provided those unperformed boundaries and the next experiment are explicit.

## Visual review rubric

For a meaningful before/candidate revision, use the director's
[comparison review](../../tools/pixel-art-director/references/comparison-review.md).
Account for changed content and record target improvement separately from regressions
in the edited feature, its connections and full context before selecting a result.

Record concrete observations, unresolved gaps, evidence paths and reviewer for each relevant dimension. Use **observed / uncertain / not tested** with reasons; do not sum dimensions into an automated quality score.

| Dimension | Review question | Evidence required |
| --- | --- | --- |
| Character identity | Does it represent this character, including defining hair/outfit/proportions? | Reference/candidate comparison; user selection pending until explicit |
| Silhouette | Do hair, torso, tote and limb negative spaces read without interior detail? | Silhouette and native/display-size view |
| Face | Are rightward orientation, near/far eyes, restrained expression and distinctive fringe preserved? | Comparable head crops plus actual-size reading |
| Pixel craftsmanship | Are contours, clusters, values, ramps and accents deliberate? | Visual inspection at 1x and integer zoom; lint is advisory |
| Style consistency | Do character and environment share coherent density, edges, contrast and lighting? | Representative context, not an enlarged portrait alone |
| Native editability | Can an agent revise the source reliably without unrelated damage? | Layer/cel inspection, local edit, fresh reopen/export |
| Animation feasibility | Can identity/volume/overlaps survive key poses and a revision? | Actual editable attack and revision; a still leaves this untested |
| Gameplay readability | Do scale, silhouette, contrast, anchors and contact read in play? | Actual Godot run with version, target, filter, camera and timing |

Keep four evidence owners distinct: **automated technical checks** (properties/protection), **agent visual observations** (visible differences), **artistic assessment** (taste and likeness judgments with reasons), and **user approval** (specific accepted artifact and scope). Passing a file check proves none of the other three.

Identity and intended expression are gates, not ordinal dimensions to average away.
“Uncertain” or “not reviewed” remains pending rather than a passing review. A user
preference is distinct from approval of a native deliverable; technical reopen/edit
proof is distinct from both.

## Evidence and traceability

Keep decisions, sources, assets, and observations connected. For each approved asset, record its source path, relevant style-guide version, creation method and material parameters, exported files, and review evidence. Retain approved versions so regressions can be compared directly.

Label evidence accurately:

- **Documented capability:** an official API or product document describes a feature.
- **External example:** a creator or tool provider demonstrates an output.
- **Local construction evidence:** this repository contains a generated or edited asset.
- **Local playback evidence:** the asset was observed running in the current Godot test.
- **User approval:** the user accepted a specific visual result or tradeoff.

A successful export establishes file validity. It does not establish style quality. A script completing establishes execution. It does not establish correct anatomy or convincing movement. Report what was actually checked, and keep unexecuted recommendations separate from results.

For candidate work, retain original/seed/best/new comparison evidence, changed-region
or face diffs for identity edits, and the selection/rollback decision. Keep best,
selected, and latest status explicit when they differ; retain rejected and proof-only
variants rather than allowing them to displace a reviewed source.

## Learning alongside the work

At each milestone, explain the small set of concepts needed to direct the next decision. Use the user's own asset as the example: silhouette and scale during concept review; layers and anchors during construction; key poses and timing during attack work; contact and recovery during gameplay review. Let the user make simple optional edits, but do not make drawing proficiency a prerequisite for progress.

Agents should continue routine implementation, exports, fixes, and verification autonomously within the agreed direction. Ask the user when the work requires a meaningful art decision or acceptance of a demonstrated limitation, presenting the concrete result and tradeoff.

## Alternatives to retain

**2D cutout or skeletal animation:** test this if the chosen style benefits from reusable body parts and editable poses. Keep replacement drawings available for difficult angles, hands, faces, or silhouettes. A flattened image is not automatically a complete rig.

**3D rendered into 2D sprites:** test this if many attacks, directions, equipment changes, or repeated revisions make frame construction impractical. The editable source becomes the model, rig, materials, and animation. This route adds setup and learning; it is not presumed easier.

**Targeted artist assistance:** retain this as an optional response to a specific demonstrated quality gap, such as a model sheet, a master attack, or a source-asset cleanup. Do not silently redefine the workflow around the user hand-painting each frame.

## Supporting research

These sources establish relevant capabilities and a production precedent, not a guarantee that AI will deliver the desired style:

- [Godot: 2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html) — image sequences, sprite sheets, and animation playback.
- [Godot: SpriteFrames](https://docs.godotengine.org/en/stable/classes/class_spriteframes.html) — per-frame duration and animation controls.
- [Godot: Cutout animation](https://docs.godotengine.org/en/stable/tutorials/animation/cutout_animation.html) — reusable parts and mixed cutout/cel animation.
- [Godot: 2D skeletons](https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html) — built-in 2D skeletal deformation.
- [Thomas Vasseur: Dead Cells animation pipeline](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-) — a non-AI production account showing why pose, timing, and revision cost matter in a 3D-to-sprite workflow.

## Current asset quality gate

For the standing/shop prototype, run [the project checker](../../tools/check_art_assets.py)
through the authorized MCP execution tool before claiming readiness for another asset.
[The reviewed profile](../../tools/art-quality-profile.json) distinguishes intentional hair/foliage
openings from solid surfaces. Inspect every frame and each isolated/hidden/moved shop part
as well. Current evidence: [character/shop review](../experiments/2026-10-27-character-shop-quality-review/record.md).
