/handoff

# Continue: multi-reference, style-faithful pixel-art production

**Workspace:** `/Users/guhan/Guhan/Projects/combat-art-lab`  
**Companion package:** this `pixel_art_reference_lab` folder  
**Task:** integrate the clarified direction, then test whether reference-assisted construction produces a convincing editable game asset with less appearance drift.

## 1. The user's intent is authoritative

The user wants the aesthetic, vibe, character identity, expressions and rendering of the approved original concept to carry into a usable game asset. They do **not** require pixel-perfect copying. Small differences and deliberate low-resolution simplifications are acceptable when the result still feels like the same character in the same art style.

This is **not a single-image reconstruction constraint**. You may use or obtain additional heads, expressions, poses, alternate views, simpler production references, key poses and animation sheets. Generate these with an available authorized image tool, or give the user an exact prompt and list of attachments to use in ChatGPT/Gemini. The user is willing to supply these images. Do not treat missing views as an unavoidable dead end.

The user uses ChatGPT and Codex. Discover image-generation/editing capabilities in the actual session rather than assuming their presence or absence. Use existing authorized access. New paid API usage, credentials, integrations or expanded machine permissions require the corresponding authorization. A user-side image-generation request is a normal workflow branch, not a failure.

AI agents own native construction and cleanup; the user is not required to repaint PNGs. Tracing, image-derived shapes, sampled colors, reduced-image seeds and hybrids are legitimate inputs when disclosed. An untouched image import alone is not a completed structured asset, but independently redrawing every pixel is not a requirement either.

## 2. Begin with the current repository

Read `AGENTS.md`, its required context, `GLOSSARY.md`, `docs/handoff.md`, ADR 0001, art-production workflow, style/motion guides and asset contract. Inspect the working tree and preserve unrelated local work. Read the actual project `pixel-art-director` skill and relevant references before using it.

Read this kit's `workspace/INTEGRATION.md` and `research/WORKSPACE_EVIDENCE.md`. They record observed paths, not a frozen copy of the whole repository. Recheck the current files; another session may have advanced them.

The latest handoff inspected for this package includes `docs/experiments/2026-10-27-original-guided-head-v02/`: three passes at a fixed 120×112 crop study, technically verified but still only a provisional likeness improvement awaiting user selection. Preserve this work, v01–v04, drawn street scenes and earlier failed studies. A crop-study size is not a full-character resolution recommendation.

## 3. Resolve reference authority without restricting reference supply

Open the approved original scene and close-up. Register their actual paths and hashes. Use the cutout as support only when it does not contradict the originals. Treat included conversation exports and old reconstruction panels according to their documented roles.

Create a compact style contract from visible evidence: distinctive tied brown hair/fringe, face shape and expression, proportions, material-color relationships, selective contours, shading clusters and the desired atmosphere. Separate invariant character design from pose-specific expression and scene-specific lighting. Simplification must remove secondary detail before it redesigns the face or silhouette.

Give every supplementary reference a role: identity, style, pose, expression, visibility/occlusion, lighting, or production simplicity. Generated candidates do not automatically override approved identity or style. Compare each with the originals and any selected native sprite. Record accepted-for-use, needs-correction or rejected, without inventing human approval.

Generate only the references needed for the immediate test. Attach the canonical references to new requests, not only a chain of previous generations. Prompt templates are in `prompts/`; fill unresolved variables before sending them. When no image tool is available, produce the user request in an editable writing block, naming exact attachments and expected outputs. Continue any independent setup that does not need the missing image.

## 4. Update the workflow narrowly

Merge this direction into the existing workflow and `pixel-art-director` rather than installing a competing skill. Use `workspace/assisted-reconstruction.md` as a proposed companion reference, not an automatic replacement of the core skill.

Add an assisted-reconstruction branch with three candidate methods:
- **Trace-guided construction:** aligned reference underlay plus transferred silhouette, major color planes and identity-bearing boundaries; redraw useful clusters on named layers.
- **Conversion plus cleanup:** source-derived reduction/optional palette mapping, followed by semantic organization and targeted native corrections.
- **Hybrid:** preserve stable shapes/colors from the source while redrawing features that fail at the target grid. Obtain a better production/pose reference when the source itself is the bottleneck.

Keep protected local corrections as their own mode. Exact pixel/hash checks remain useful for originals and locked areas; they are not an artistic similarity target for a fresh reconstruction. Record imported pixels, generated references, authored marks and cleanup separately.

Remove the earlier blanket prohibition on tracing/downsampling. Preserve the prohibition on passing off an untouched flat import as complete structured construction. Keep existing native structure and protected-pixel checks; do not weaken them to make a failed experiment pass.

## 5. Run the smallest informative test

Follow `workflow/FIRST_EXPERIMENT.md`. Select one identity-rich head/shoulder crop and one explicit target grid. Inspect current references for sufficiency first; generate/request a matched simpler reference or missing view only if it solves a named problem.

Compare a trace-guided candidate and a converted-plus-cleaned candidate using the same authoritative reference, framing, palette policy and equal bounded effort. The current independent redraw is a labeled historical baseline, not a new controlled arm unless its conditions match. Use a hybrid follow-up only when a specific failure points to it.

Review original, any generated intermediate, raw seed and actual native export together. Inspect native-size, integer zoom and a stated projected display size. Judge identity, expression, proportions, pixel craftsmanship and stylistic fit separately. Shape-overlap scores are diagnostics, not a likeness percentage. Do not force exact source pixels, universal color limits or needless photorealistic detail.

A suggestion, not a universal budget: two revision checkpoints per initial candidate; up to two targeted supplementary-reference requests before reassessing the approach. Record actual time, operations and interventions when possible, unknown otherwise. Preserve rejected results. Stop a branch when the next change lacks evidence; switch route or request a better reference instead of repeatedly polishing the wrong anatomy.

Deliver native sources with meaningful layers, construction/patch provenance, PNGs, comparisons and one isolated edit proof. Reopen/export and inspect actual images. Choose a provisional method only from the displayed evidence. Final artistic selection belongs to the user; routine technical fixes need not become repeated permission gates.

## 6. Extend to motion with more references

After a convincing static style checkpoint, test a short motion sample, then the already-planned representative combat action when its attack/camera choices are resolved. Do not invent a permanent weapon or redesign the tote/outfit to make animation easier.

Use a coherent generated key-pose sheet/short strip or separately generated poses tied to the same canonical references. Both are allowed. One sheet is not automatically correct; separate images need especially careful consistency checks. Treat either as source/reference until its timing and frames are validated.

Follow `workflow/ANIMATION.md`: shared native scale and palette, explicit slots and pivots, no independent bounding-box fitting per frame, preservation of intentional root movement, and review for head-volume, clothing, facial identity and contact drift. The helper can normalize known crops and anchors; it cannot infer them or repair anatomy.

Validate an actual played preview and then Godot before claiming runtime readiness. Request a missing in-between, reverse view or expression when needed. A generated sheet's count, transparency and layout must be measured; prompt wording is not proof.

## 7. Research and evidence boundaries

Start with `research/FINDINGS.md` and `research/SOURCES.md`; research further only for a real unresolved decision. Official image-generation capabilities and API controls are distinct from what the current web/agent session exposes. Document actual tool, version, prompts and attachments. This package deliberately avoids hard-coded image-model names.

PixelOE, segmentation and ControlNet are optional researched alternatives, not dependencies or locally proven solutions. The included historical tests are simple deterministic reductions, not completed tracing/hybrid or animation tests. The new offline utilities are preparation tools, not automatic artists.

## 8. Report and leave the workspace usable

Update the relevant existing research, art workflow, style guide, asset contract and director reference; summarize the new state in `CONTEXT.md` and `docs/handoff.md`. Do not rewrite historical records or claim an untested rendering choice is approved. Record a decision when it is actually selected, with provisional technical choices distinguished from user art approval.

Report exact changed paths, candidate artifacts, actual checks, visual differences, unresolved gaps and the next smallest action. Keep native construction, export, human selection, animation and Godot playback as separate statuses. No commit, push, new purchases or publication is implied.

## Suggested skills

Use `handoff` for continuity, `research` for genuine source gaps, `writing-for-agents` when editing instructions, and the project `pixel-art-director` for native work. Use an actually available image-generation skill/tool for new references. Consult installed `sprite-pipeline` guidance for scale/anchor consistency; its seed-frame preference must not override the user's permission to obtain multiple views and individual pose references. Preserve the project's native Aseprite and Godot requirements rather than adopting a browser-game workflow wholesale.

**Success:** demonstrate a small, editable asset that preserves the approved look and expression through an evidence-backed assisted method, then identify the viable next animation test. If neither candidate works, leave concrete failure evidence and a better-targeted reference or technique request—not another unsupported promise of exact likeness.
