# Combat Art Workflow

## Purpose

Find a repeatable way to make the intended visual style and responsive combat animation with AI assistance. The user directs the art, evaluates results, and learns the relevant basics. Agents do the asset construction, revisions, technical setup, and verification.

The first result is a small, inspectable proof of the art pipeline. It is not a commitment to produce a complete game or a large asset library.

## Accepted direction

1. Explore the visual direction with reference analysis and concept images.
2. Convert the selected direction into explicit visual and motion rules.
3. Have AI construct editable assets through the chosen editor, scripts, drawing operations, layers, or a rig.
4. Complete one representative combat attack.
5. Play it in Godot at the intended screen size and gameplay speed.
6. Make a deliberate art revision and a timing revision before expanding production.

The user's inability to draw is a pipeline constraint. Do not make manual repainting of generated PNGs the default handoff. If an agent cannot produce or revise an acceptable result, document that limitation and propose a concrete alternative.

## Decisions still open

Pixel art is not selected merely because Aseprite is available. Camera perspective, character proportions, asset resolution, palette limits, outline treatment, animation method, and tools remain open until references and a small test justify them. Godot is the intended engine.

Aseprite, its scripting API, an MCP integration, specialist generation services, 2D rigs, and 3D-to-sprite rendering are candidate tools or routes. Installing a connector or creating a valid file does not establish that it can achieve the intended art quality.

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

### 2. Write the visual and motion rules

**Work**

- Translate the chosen concept into observable requirements. Record the intended game-view scale before deciding how much detail a sprite needs.
- Define proportions, distinctive features, palette relationships, outline/shading behavior, facing conventions, and which details may simplify in motion.
- Define the motion character: deliberate or snappy, grounded or airborne, restrained or exaggerated, with examples of acceptable poses and timing.
- State what can change between actions and what must stay consistent. Keep character art and attack effects distinguishable during inspection.

**Outputs**

- A compact style guide with an approved character view and annotated examples.
- A motion guide describing one representative attack's anticipation, active/contact phase, follow-through, and recovery.
- A provisional technical specification: camera/view, asset scale, transparency, anchors, and intended import/export format. Mark tentative decisions as tentative.

**Go criterion:** another agent can describe what to construct and how to judge it without inventing major design choices.

**If unresolved:** resolve the specific missing requirement with a visual comparison or a focused question.

### 3. Prove editable asset construction

**Work**

- Select the smallest toolchain capable of the required style. Prefer existing repository capabilities before adding integrations.
- Have the agent construct one representative character pose in the native production format. Depending on the route, preserve useful layers, source scripts or drawing operations, separate body parts, or a rig.
- Inspect the result at native/game size as well as enlarged. Check the actual asset rather than only an attractive presentation image.
- Request a localized revision, such as changing the weapon shape or a costume accent. Reopen the native file and inspect the result.

**Outputs**

- The editable source and any scripts or parameters needed to reproduce it.
- A transparent runtime preview and an image showing the source structure.
- Before/after evidence of the localized revision, including any unintended changes.

**Go criterion:** the asset matches the selected direction closely enough for the test, has meaningful editable structure, and can be revised without losing unrelated approved features.

**If unsuccessful:** identify whether the limitation is the tool interface, the agent's construction quality, the representation, or the style's complexity. Try a targeted correction or compare another route. Do not describe a flattened image imported into an editor as a fully structured asset.

### 4. Build one representative attack

**Work**

- Choose an attack that exposes the important challenge in the desired combat style. An idle loop alone is insufficient evidence for a combat-heavy game.
- Establish readable key poses and timing first. Add drawings, interpolation, deformation, or effects where they improve the intended motion.
- Maintain character identity, weapon dimensions, palette behavior, anchor positions, and facing conventions across the action.
- Keep gameplay timing explicit. Separate the art's frame count from the duration of anticipation, active/contact, and recovery phases.
- Inspect the action both with and without impact effects. Effects may enhance the action but should not be the only evidence that it reads correctly.

**Outputs**

- Editable attack source, a preview animation, and exported runtime assets.
- Timing notes and the expected contact pose or interval.
- A short defect list with fixed, accepted, and unresolved items distinguished.

**Go criterion:** the attack communicates its direction, force, contact, and recovery while preserving the chosen style and character identity.

**If unsuccessful:** revise the key poses or production method before generating additional attacks.

### 5. Evaluate in Godot

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

### 6. Test revision cost, then decide whether to expand

**Work**

- Make one art change that should propagate through the attack, such as a weapon or costume adjustment.
- Make one timing or pose change driven by the Godot test.
- Rebuild the exports and replay the scene. Confirm that approved unrelated features remain intact.
- Record agent work, user intervention, generation/service usage where observable, and recurring defects. Do not invent estimates for missing measurements.

**Outputs**

- Before/after source assets, exports, and playback evidence.
- A short assessment of what was easy, what failed, what remained manual, and whether the process is repeatable.
- A production decision: continue with this method, simplify a specific requirement, test a named alternative, or seek targeted artist assistance.

**Go criterion:** both revisions are achievable with an amount of effort the user accepts, without repeatedly reconstructing unrelated approved work.

**Expansion:** only after this gate, add the next small animation set or a second character. Repeatability across a second asset is the next check; one successful attack does not establish that every asset is solved.

## Acceptance checklist

- [ ] The user approved a visual direction using actual examples.
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

## Evidence and traceability

Keep decisions, sources, assets, and observations connected. For each approved asset, record its source path, relevant style-guide version, creation method and material parameters, exported files, and review evidence. Retain approved versions so regressions can be compared directly.

Label evidence accurately:

- **Documented capability:** an official API or product document describes a feature.
- **External example:** a creator or tool provider demonstrates an output.
- **Local construction evidence:** this repository contains a generated or edited asset.
- **Local playback evidence:** the asset was observed running in the current Godot test.
- **User approval:** the user accepted a specific visual result or tradeoff.

A successful export establishes file validity. It does not establish style quality. A script completing establishes execution. It does not establish correct anatomy or convincing movement. Report what was actually checked, and keep unexecuted recommendations separate from results.

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
