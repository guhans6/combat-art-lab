---
name: pixel-art-director
description: Construct, revise or review deliberate pixel art in editable Aseprite sources using a frozen visual brief, scoped operations, visual inspection and deterministic checks. Use for character likeness corrections, pixel-art reconstruction, sprite animation, controlled iteration or cross-model art comparisons. Use trace-guided, conversion-plus-cleanup or hybrid construction when source-derived shapes reduce appearance drift.
---

# Pixel-art director

## Outcome

Deliver an editable native asset and evidence that the requested change improved
its intended appearance without altering protected content. Tool success, file
correctness, visual quality, and user approval are separate outcomes.

This skill is for a selected pixel-art target; it does not choose pixel art for every
supplied reference. For an illustrated, rigged, or other rendering target, first use
the project’s representation-neutral reference intake and the smallest suitable
construction proof, then select an appropriate route. Keep this skill’s existing
pixel-craft, native-protection, and review gates when the pixel route is selected.

## 1. Establish the task

Read the repository's `AGENTS.md` and its required context first. Preserve existing
working changes. Identify authoritative references, any exact baseline source,
allowed region/layers, candidate native canvas, palette policy, and deliverables.
An existing native baseline is required for protected correction; fresh
reconstruction can begin from references and a blank native study.
Record unresolved assumptions rather than treating your earlier critique as fact.
When a receiving project supplies art-production context, apply its experiment
intent, seed review, per-pass identity gate, and selection rules.
For facial construction, correction or deliberate expression/blink changes, read
[face-likeness.md](references/face-likeness.md) before interpreting marks or freezing scope.

Choose one mode:
- **Local correction:** copy the existing native asset; protect everything outside
  the authorized region.
- **New reconstruction:** draw into new named layers from the approved visual brief;
  read [reconstruction.md](references/reconstruction.md) and [craft.md](references/craft.md).
  Test scale and feature feasibility before committing to the full asset; an
  source-derived shapes, colors, masks and converted pixels are permitted inputs.
- **Assisted reconstruction:** compare trace-guided construction, conversion plus
  cleanup, or a hybrid using [assisted-reconstruction.md](references/assisted-reconstruction.md).
  Use this branch when source transfer can preserve identity better than reinvention;
  meaningful native structure and dependable revisions remain the delivery criteria.
- **Animation construction, revision or diagnosis:** read
  [animation.md](references/animation.md) for the task profile, per-part method,
  material continuity and separate pose/playback decisions.

For cross-model comparison, read [benchmark.md](references/benchmark.md). The
bundled `assets/combat-art-lab-v03.json` is a historical optional profile, not a
universal sprite size, current asset choice, or CLI default.

**Complete when:** a task profile names exact inputs, priorities, locks, scope,
output paths, and a bounded pass budget. If native input is missing, do not claim
native-preserving editing from a screenshot; identify the blocked input.

## 2. Verify one drawing backend

This gate applies before native mutation. A read-only audit may use existing native
readers and exports; report unavailable evidence and skip drawing steps 2–4.

Read [setup.md](references/setup.md) on first use or after a tool/version change.
Run `python3 scripts/doctor.py` relative to this skill directory. Its default
Aseprite result is non-launching file inventory only; it does not certify MCP
connectivity. Use `--probe-aseprite-version` only in an execution context where
direct editor launch is permitted. Discover the actual runtime tool schemas and use
the configured MCP preflight for the headless readiness boundary. Use
[adapters.md](references/adapters.md) for backend differences.

Prefer the existing verified backend. For a new multi-agent experiment, the
recommended candidate is Pebbly's Aseprite AI Artist. Diivi's MCP or explicit
Aseprite CLI/Lua are alternatives, not additional servers to start concurrently.
Choose live or headless mode explicitly; do not switch modes to conceal a failed
connection. Do not modify a file on disk while a live editor owns that file.

Run the scratch-document smoke procedure in setup.md, including image delivery,
a one-pixel edit, transparency behavior, save/reopen, and protection checks.

**Complete when:** the selected agent can inspect the returned image AND pixel
coordinates, make the intended scratch edit, and verify the result. A `connected`
status alone is insufficient. Missing installation permissions are a blocker,
not permission to broaden machine access.

## 3. Freeze inputs and observations

Work in a new run directory. Copy references and any native baseline and export;
record hashes and actual tool/model versions. Keep originals unchanged, including
uncommitted ones. For local correction, establish a hard editable mask and allowed
native layers and record pre-edit native structure and pixels. The `prepare_run.py`
profile in [benchmark.md](references/benchmark.md) is specific to the frozen v03
correction, not a requirement or default palette, canvas, or mask for reconstruction.

Visually open the approved original images before drawing; a document describing
them or an old reconstruction is insufficient. Record inspected paths and concrete
visible identity cues in the run observations. If the agent cannot receive the
images, stop construction and identify that capability gap.

View any baseline, then inspect reference crops at native
size and integer nearest-neighbor zoom. For faces, follow
[face-likeness.md](references/face-likeness.md) before assigning a meaning to a
faint mark or freezing its mask. Do not infer exact source pixels from a compressed
or rescaled screenshot. Treat the task's approved identity source as primary when a
generated cutout disagrees. Multiple references may supply expression, pose,
visibility or production simplicity. Generate only a named missing reference with an
available authorized image tool; otherwise deliver a filled editable prompt, exact
attachment paths and expected returned image. Review generated images against the
originals before using them, recording agent use status separately from user
approval. Do not copy compositing halos into the sprite.

For a seed or converted baseline, record its recipe and role, inspect original/seed/
seeded-native export at 1x and integer zoom, and choose whether it is suitable for the
task, suitable only for a named bounded repair, or needs re-preparation. A
reference-supported face correction is permitted within its stated scope; do not treat
a baseline's unreviewed feature loss as an accepted starting point.

**Complete when:** `observations.md` separates visible reference cues, any baseline
differences, uncertain interpretations, and the next construction/change hypothesis.
Preserve the baseline preview when one exists; otherwise retain the first study as
the starting checkpoint for revisions, with the approved originals still authoritative.

## 4. Draw a bounded pass

For reconstruction, resolve silhouette, orientation, proportions and large planes
before identity-bearing accents or secondary detail. For correction, retain good
pixels and patch relevant clusters within the frozen scope. Use explicit layer/frame
targets and scoped operations; read back a patch region before writing. Preserve
the existing palette for a correction unless the task authorizes changing it.

Make one coherent revision per pass. Save a labeled checkpoint and its operations
or Lua source. Use native undo transactions when the backend supports them. Check
erase-versus-skip behavior before sending a text grid back to the editor.
Meaningful one-pixel facial marks are valid; do not run blanket speckle removal.

**Complete when:** the revised native source and PNG exist in the run directory,
the changed region is known, and the agent has inspected the actual export beside
the original, seed where relevant, and best eligible prior at 1x and matched integer
zoom. Save that review image and a visual decision in the pass record before
advancing. At blockout, check framing/head turn/hair mass/proportions; at
feature passes also check eyes/expression/fringe. Correct material drift within
scope or mark the attempt rejected and stop. An older reconstruction alone is not
the reference panel. Read [reconstruction.md](references/reconstruction.md) for the
review-sheet helper and the evidence it can and cannot establish.
A long list of successful drawing calls is not a completed visual pass.

## 5. Evaluate both correctness and appearance

For a meaningful before/candidate revision, apply
[comparison review](references/comparison-review.md): account for changed content,
inspect its connected context, and decide target improvement and regressions separately.

After transparency cleanup or part motion, read [alpha coverage](references/alpha-coverage.md).
Check actual exported frames for unintended fabric/body holes before dependent work.

For the frozen local-correction profile, run `scripts/pixel_checks.py check` against
the export and mask, make and inspect a review sheet with `preview`, and verify
inputs with `prepare_run.py verify-inputs`. For other tasks, use checks suited to
the declared scope and inputs; these helpers do not establish artistic quality.

Also inspect native source: layer order/names/visibility/opacity/blend modes,
frames/timing/cel positions, palette data, and protected layer pixels. Reuse the
repository's existing native checker where applicable. A flattened PNG diff
cannot detect hidden-layer damage. Save, close/reopen a scratch output, and verify
that its fresh export matches the intended output. Never close unsaved user work.

Compare reference and candidate at matched displayed size, native size, integer
zoom, and in representative full-body or scene context. Record the exact reviewed
export/checkpoint and reviewer role. Label reference resampling as preview only,
recording source crop and actual candidate dimensions. Assess
identity, style/aesthetic, proportions/orientation, expression, pixel craft,
secondary detail and atmosphere independently; record observations and uncertainty,
not an automatic art score. Compare against the reference as well as the previous
attempt.

**Complete when:** declared constraints pass appropriate PNG and native checks,
including protected content for corrections, and visual observations state what
improved and what remains uncertain. An identity/expression regression cannot be
offset by technical or craft gains. Name the best retained checkpoint, latest status,
decision/reason and next baseline; if no reviewed candidate meets the task, record no
selected result. If worse, retain the checkpoint for evidence but revert the working
copy to the best prior candidate.

## 6. Stop and hand off

Stop when the bounded evidence budget is reached, gains diminish, the next change
lacks visual evidence, or a required capability is missing. If a required feature
cannot read on the chosen grid, preserve the result and propose a separate scale or
representation variant with its tradeoff. Never expand canvas/palette/scope inside
a frozen benchmark. Do not self-approve final art.

Deliver native source, construction/patch history, transparent PNG, native-size
and zoomed comparisons, exact tool/model identifiers, verification results,
remaining visual gaps, and the unchanged-input check. State what was not tested.
The user selects the artistic result; preserve all tested candidates. Distinguish the
best/selected result from the last attempt, proof-only edits, user preference and user
approval; native technical proof does not select art.

Research and evidence limits: [research.md](references/research.md).
