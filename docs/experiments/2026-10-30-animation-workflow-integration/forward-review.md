# Independent animation instruction forward pass

Date: 30 October 2026. Read-only validation of eight requests in `docs/experiments/2026-10-30-animation-workflow-integration/scenarios.json`. No repository edits, art mutation, installation, editor launch, UI, Code-MCP, publication, or network access. The only written artifact is this report. Scenarios 2–8 use their supplied evidence as fixtures; they do not describe work completed here.

## Result

All eight requests reached an appropriate branch. The instructions permit rigid-part reuse, require changed cloth forms to be constructed deliberately, allow justified moving cast shadows, preserve partial preferences without selecting a whole animation, and keep playback judgment separate from still-pose evidence. Static mouth and shoe edits remain static; unrelated CSV work does not enter the art workflow. No blocking instruction regression observed. One inherited scope ambiguity was found and resolved during this pass, as documented below.

## What I actually consulted

- Required context: root AGENTS.md, CONTEXT.md, GLOSSARY.md, docs/handoff.md, ADR 0001, docs/agents/domain.md and docs/agents/validated-checkpoints.md. Some first combined command output was truncated; I reread relevant workflow/guide sections individually. The checkpoint document explicitly states that no separate delivery reference is established.
- Evaluation authority: `/Users/guhan/.codex/skills/.system/skill-creator/SKILL.md`, especially independent forward testing.
- Entrypoint: `tools/pixel-art-director/SKILL.md`; its actual animation link led to `references/animation.md`. The face link led to `references/face-likeness.md`; the part-motion/coverage link led to `references/alpha-coverage.md`. Also consulted `references/research.md` for evidence boundaries, without following its external links.
- Project-facing discovery: `docs/workflow/art-production.md` selects animation at milestone 2 and links to `docs/art/motion-guide.md#animation-procedure`, which links to the same animation reference. Also read the style guide and asset contract. The style and motion guides preserve appearance/motion preferences separately.
- Read the diagnosing-bugs skill because scenario 1 asks for investigation. Its software feedback-loop requirements do not supply a machine verdict for subjective material appearance. I therefore used repeatable native/export diagnostics and actual pose inspection, and make no claim to a deterministic test of perceived naturalness or the user's exact subjective symptom.
- Raw first-scenario provenance: `2026-10-30-natural-idle-sol/proof/input-hashes.json` identified the Terra native path. Read `tools/check_native_pilot.py` as the offline native-reader implementation, then imported it with bytecode writing disabled.
- Inspected only permitted raw native/GIF/frame inputs for scenario 1. Did not read the integration record.md, audit.json, snapshots/baseline content, BRIEF.md, or prior forward-review conclusions. A file-name inventory listed some such paths but their content was not opened.

## 1. shirt-in-idle

**Request:** investigate clothing appearance in the preferred-motion idle; compare both earlier GIF characters; draw nothing.

**Discovery and branch:** SKILL.md → animation.md; project style guide → earlier comparison and latest redraw; motion guide → animation procedure. This is a read-only animation/material diagnostic. SKILL §2 explicitly permits existing native readers/exports and skipping drawing steps 2–4. No doctor, smoke document, backend preflight, or drawing work is needed.

**Minimal profile:** earlier Terra and Sol are appearance evidence with neither selected; latest redraw supplies partial preferred movement and rejected clothing appearance. Compare each source's rest, extremes, transitions and return on a common matte, using collar, shirt folds, waist and jacket opening correspondence. Keep material, pose/anatomy, identity, export and unobserved playback decisions separate. Budget: one offline diagnostic, zero edits. No source becomes a production baseline through this review.

**Actually observed:**

- Earlier comparison GIF SHA-256 `41e884b763c7073b7338f417311b723812607bb929ff34ed2ef2fd54cc09b7ff`: 768×576, 8 decoded frames, durations [600,350,550,600,50,80,50,250] ms, 2530 ms total.
- Latest redraw GIF SHA-256 `a8a40b65c25460a8533e28350014f9fa51db667deb53558b11ff24a5b9e1e501`: 384×576, 12 decoded frames, durations [650,240,240,500,350,300,190,500,50,80,50,800] ms, 3950 ms total.
- Read all three `pass01.aseprite` sources: Terra in `2026-10-30-idle-breathing-comparison/terra`, earlier Sol in `2026-10-30-natural-idle-sol`, and latest redraw in `2026-10-30-redrawn-breathing-sol`. They are 128×192, 12-layer sources with normal-blend, full-opacity layers/cels in the inspected structures. The existing reader decoded all frames. Independently compositing visible cels matched every corresponding PNG exactly: 8/8, 8/8 and 12/12. This is an offline existing-file comparison, not a fresh editor reopen/export.
- Decoded earlier GIF matched the exact Terra-left and earlier-Sol-right PNGs at 3× nearest neighbor over its [48,50,57] matte in all 8 frames. Latest GIF matched its PNGs over its [221,221,221] matte in all 12 frames. No export discrepancy appeared in this comparison. Different mattes are a presentation variable, so the diagnostic also placed source frames on a shared neutral grey matte.
- All three rest PNGs are byte-identical as decoded RGBA. Every subsequent frame uses only RGBs already present in its own rest. This independently confirms the fixture's color-set statement; it does not certify stable perceived material.
- Visually inspected all 28 full source-frame poses in an in-memory common-matte strip, plus 6× nearest-neighbor torso crops for all eight old frames and the first nine redraw frames. The latest shirt's central mauve fold cluster changes from the rest's small angular accent to a broader diagonal/branching shape around frames 3–5, then changes through release. The waist edge and jacket opening also reshape. The two earlier sources preserve more of the rest cluster's arrangement while moving/deforming it. These are concrete form/cluster observations, not an automatic artistic score.

**Decision/evidence limit:** unchanged RGBs do not rule out the reported appearance change. Redistribution/topology of pale base and mauve fold/shadow pixels is a supported candidate mechanism; matte difference is controlled for in the pose comparison. Exact GIF/native agreement makes an export-color error unsupported by these inputs. The available stills cannot establish temporal naturalness or how the effect reads at speed. Preserve the user's clothing rejection and movement preference separately; no selected animation, no side selection, no redraw, no assertion that every changed fold is illegitimate. The next authorized construction task would need corresponding-form explanations and a bounded key-pose material correction; that task is not performed here.

**Construction/backend:** inappropriate for the current request. No new art, generation, tool installation or Godot work.

## 2. arm-cast-shadow

**Discovery and branch:** SKILL.md → animation.md, especially material roles and per-part method. Alpha coverage is relevant at the changing arm/shirt overlap. This is an in-between plan from user-selected keys.

**Minimal next action/profile:** retain the reviewed rest and raised key as endpoints; record the fixed overhead light, arm trajectory/occlusion, garment seam correspondence, existing palette, protected design and a bounded in-between pass. Determine how the arm and shirt surfaces connect at the middle pose. Permit the cast-shadow boundary to travel across the shirt with arm occlusion. Track its value role and edge language rather than holding exact shaded pixels constant. Do not invent a new light direction or costume texture.

**Fixture versus evidence:** matching seams/light/shadow attachment and key selection are supplied facts, not new observations. A changed shirt shadow is expected under these facts; palette equality alone neither approves nor rejects it. Review the actual intermediate against both keys for anatomy/volume, shadow continuity and identity, then eventually inspect playback. No temporal/runtime claim yet.

**Construction/backend:** plan now; native mutation would be appropriate only when carrying out the authorized construction scope with exact files, native ownership and the normal backend gate. No need to redraw every rigid/unchanged part. No work performed here.

## 3. rigid-prop

**Discovery and branch:** SKILL.md → animation.md → per-part method. The fixture's isolated verified owner, no rotation/deformation and retained front-facing shape make cel translation/copied pixels the suitable method.

**Minimal next action/profile:** separate output; sign-only native owner; preserve lettering, painted highlights, palette, canvas and character; declared six-pixel horizontal travel. Choose the short pose/hold sequence and timing consistent with the request, record offsets rather than independently fitting each frame. Translate the rigid sign and repair/check newly exposed overlaps if relevant; verify decoded sign pixels in registered sign coordinates and protected native content.

**Decision/evidence limit:** no torso-style redraw requirement applies. Fixed painted highlights may move intact with the front-facing rigid prop. Native/protected export/reopen and actual playback remain checks to perform, not completed evidence. The fixture does not specify timing or an exact source path, so I do not invent them.

**Construction/backend:** appropriate in the separately authorized output after backend readiness; evaluation restrictions prevent execution. No backend was launched.

## 4. cloth-expansion

**Discovery and branch:** SKILL.md → animation.md → actual ownership, changed forms, material correspondence; alpha coverage for joints/overlaps.

**Minimal next action/profile:** user-selected static source as appearance baseline; quiet chest expansion/release, connected shoulders, pocketed hands and planted feet; fixed light, existing material roles, protected appearance and source; scope only the new animation output. Read actual native cels/pixels and identify neighboring ownership before freezing masks. A layer name is insufficient evidence for moving its contents.

Establish rest/extreme/release keys before in-betweens. Construct changed chest/jacket contours and cloth planes; preserve volume and connected shoulder/neck/waist contacts. Reuse valid rigid or unchanged regions. Avoid treating row-band shifts or whole-layer translations as a model of deforming cloth. Track characteristic seams/folds/shade hierarchy with local form correspondence, not a head offset applied to the shirt. Review keys separately for motion/anatomy, material continuity, identity and technical protection before assembling a cycle.

**Decision/evidence limit:** fixed lighting does not require identical shaded pixels across poses. Shape changes may legitimately move folds and highlights, but do not authorize relighting or new texture. The source selection and neighboring pixel ownership are fixture facts; no ownership inspection or successful redraw was performed here.

**Construction/backend:** appropriate once the plan is executed in the separate scoped output with ownership confirmed and backend readiness. No universal redraw and no project-specific grid/frame/model default.

## 5. stills-review

**Discovery and branch:** SKILL.md → animation.md → separate review decisions and still/playback boundary. Read-only review skips drawing/backend setup.

**Minimal next action/profile:** inspect all 12 actual poses, transitions/seam, full character and material correspondence using supplied native/export/timing evidence; label exactly which dimensions stills can support. Record the timing design without claiming temporal perception. Retain an eligible playback candidate only if the available pose/material/identity checks actually support it.

**Delivery verdict:** no verified smooth/natural animation verdict is possible from these tools. The fixture says static/source/export evidence exists, not that appearance is good; I cannot infer an artistic pass from export equality. Delivery can honestly report completed static review findings and an unresolved playback judgment. User approval, engine/gameplay readiness and actual-speed naturalness remain unverified. A disclaimer must not replace the still review that is feasible.

**Construction/backend:** neither necessary nor authorized by a review request. No launch to conceal missing playback capability, no fabricated observation.

## 6. static-mouth

**Discovery and branch:** SKILL.md §1 → face-likeness.md. Animation.md explicitly says static expression edits use the face procedure; no animation branch is needed.

**Minimal next action/profile:** authoritative close-up plus exact native/export of this one still; register eye/nose/chin/existing feature landmarks with confidence, inspect feature/head/full-asset contexts, distinguish faint visible mark from its interpretation, and read actual visible native ownership before freezing the mouth mask/layer/frame. Protect the rest and preserve palette. Then make an economical separate checkpoint within a declared bounded pass budget, comparing quieter smile morphology/contrast at native size and useful integer zoom.

**Decision/evidence limit:** do not assume the mark is the mouth or that the nominal face layer owns it. Do not add another competing stroke before locating it. No blanket noise removal or project-v03 coordinates. The fixture supplies existence, not observed anatomy; no facial diagnosis or improvement was completed here. User visual selection remains separate from technical protection. If a critic edits, fresh independent inspection applies; no automatic extra critic is required by this simulated review.

**Construction/backend:** appropriate after reference/owner/scope establishment and normal backend readiness. No frame/timing work, no blink, no animation expansion.

## 7. static-shoe

**Discovery and branch:** SKILL.md local correction. No animation or face reference is needed. Supplied owner/mask/export/native are already verified fixture inputs.

**Minimal next action/profile:** duplicate native source into scoped output; exact single frame, verified shoe owner and supplied mask, same palette; two lace accents only; protect all other native content. Read the patch, make the bounded accent edit, inspect actual export against baseline/reference at native/integer zoom, verify protected pixels/native structure and fresh reopen/export equality.

**Decision/evidence limit:** no new scale study, anatomy/face interpretation, animation task profile, blanket redraw or Sol critic is implied. No actual two-pixel/accent result or completed verification is claimed. The exact pixel locations and source path remain supplied inputs to the execution task.

**Construction/backend:** authorized protected correction, so appropriate after normal backend readiness; not performed in this read-only evaluation.

## 8. unrelated

**Discovery and branch:** skill description and selected-pixel-target boundary exclude this request. Do not load animation references or art gates for CSV sorting. Previously loaded art context does not make it relevant to this independent scenario.

**Minimal next action:** use the CSV/spreadsheet route; inspect header/date format and sort rows by invoice date while preserving columns and cell values. Retain correct row associations and verify ordering/column preservation. The fixture contains no actual CSV bytes/path, so no sort is claimed here.

**Construction/backend:** no art construction, Aseprite doctor, source-copy ritual, image review, model routing or Godot task.

## Instruction issue found and resolved

**Low severity, inherited scope ambiguity:** `references/alpha-coverage.md` says completion requires that “actual engine output has been inspected.” Following the animation link for the rigid-prop or cloth-expansion branch reaches this unconditional clause, even when the requested deliverable is a local native asset or key-pose plan and engine playback is explicitly outside scope. The main animation procedure correctly treats engine/gameplay playback as a separate evidence boundary. I followed that task-specific boundary and did not expand these requests into Godot work.

Suggested narrow correction: qualify the alpha completion clause with “where engine validation is in the agreed scope; otherwise mark it untested.” Keep every-frame alpha/overlap/native/reopen checks. This avoids turning an inherited project proof into a universal backend requirement. It is not a new animation-rule regression and did not block the eight decisions.

Follow-up validation: the parent narrowed alpha-coverage.md and asked me to inspect it. I reread the actual current file. It now conditions actual-scene inspection on runtime delivery being in scope and completes native coverage separately; engine delivery still requires actual engine inspection, while native-only output explicitly leaves that boundary untested. Applying this wording to rigid-prop and cloth-expansion removes the unintended Godot requirement without weakening native/alpha checks. The identified ambiguity is resolved; no outstanding correction is required from this pass.

No additional actionable branch failures found. The important counterexamples all worked: moving cast shadows remain legitimate; rigid signs may translate without redrawing; cloth can deform without restyling; unchanged RGBs are not a material pass; stills do not establish temporal naturalness; static facial and shoe tasks remain scoped; CSV work exits the skill.

## Evaluated revision and limits

SHA-256:

- SKILL.md: `1c4de83b2c057f93fa339d4617266b2a39e129ecce45be50b271078bdbeef2d5`
- animation.md: `bd0c5b6b7bcca2404c4255a6163cb52e20892b4e4f750fa82a2e7cc2c2ffbb53`
- face-likeness.md: `9df29483b56a23a4dc8c44ab2eade29bc1e26be11f0113288b33c7a6f6ee8932`
- alpha-coverage.md initially evaluated: `5616037c1c173224eae2ef9d15e90d674b0be3e804c70b298f979e0d961e9e79`
- alpha-coverage.md follow-up resolution verified: `072ee4b87758d95ca12d62bf93a006f54178a27b1021ff814c394542a4535ec8`
- scenarios.json: `6b27410b7e174fb0b7720ee09efe75c19933f884e45601fc6d13c51c185eefde`

Observed verification is limited to forward instruction decisions and offline existing native/PNG/GIF comparisons. System Python initially lacked Pillow; the already bundled workspace Python supplied it without installation. All comparison sheets were generated in memory and shown through the tool; no extra files were written. No fresh native edit/reopen, art selection, editor/backend readiness, real-time playback, Godot, installation elsewhere, commit or publication is established. Parent owns any narrow instruction correction and integration delivery; user remains the artistic selection owner.
