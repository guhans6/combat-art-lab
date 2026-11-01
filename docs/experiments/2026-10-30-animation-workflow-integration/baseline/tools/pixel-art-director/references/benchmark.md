# Cross-model drawing benchmark

## Question

Can another model, using the same native asset, references, skill and tools,
produce a more faithful head without damaging already-correct work?

This is narrower and more useful than "which model makes the best pixel art?"
A separate blank-canvas reconstruction test can follow. An image-generator output
is a third track, not a direct substitute for either native-drawing task.

## Comparison intent

Declare one intent before preparation. For a **model comparison**, freeze identical
references, derived seed pixels, crop/grid/transform, alpha/palette treatment,
masks/ownership, native baseline, task and budget; verify hashes and decoded seed
equality for every contestant. A deliberately imperfect shared seed is allowed when
the named task repairs that defect. For a **method/recipe or source comparison**, name
the variables that differ, retain every arm, and hold the other practical conditions
comparable; conclusions cover the combined recipe when several variables vary. Label
an unavoidable model-plus-host-plus-toolchain pilot as such. Equal original inputs do
not by themselves establish equal seeds, and no historical recipe is a default winner.

## Frozen first task

`assets/combat-art-lab-v03.json` is an optional historical example. It points at the native v03, not a labeled
screenshot, later shoe/background work, or a "latest" file. Confirm all inputs
exist and the profile agrees with the inspected source. The current palette is
measured, not imposed as 45 colors. The head mask and neck notch are fixed.
This is a historical protected-correction profile, not the default profile for a new
reconstruction or a claim about another asset's palette, face mask, or canvas.

Example after setting these to real local paths and the actual selected model:
```bash
SKILL="/absolute/path/to/pixel-art-director"
REPO="/absolute/path/to/your-project"
MODEL="exact-model-id-selected-in-your-client"
python3 "$SKILL/scripts/prepare_run.py" prepare \
  --repo "$REPO" --output-root "$REPO/art-runs" --run-id pilot-01 \
  --model "$MODEL" --host gemini-cli --backend pebbly \
  --profile "$SKILL/assets/combat-art-lab-v03.json"
```
This creates copies and hashes; it does NOT run a model or draw. Inspect the
resulting BRIEF.md and task.json. Fill the actual model identifier, host/tool/editor
versions, skill hash and tool-catalog hash in run.json after runtime discovery.
The initial state is explicitly `prepared_not_executed`.

The input hashes include source originals as well as copies, so preservation can
be verified even when the art has not been committed to Git. The script refuses
an existing run directory rather than overwriting an earlier trial.

## Experimental controls

Start with one pilot per candidate host/model. After setup succeeds, run three
fresh independent trials each, subject to the user's approved usage budget.
Use the same visual brief, baseline hashes, palette, mask, backend version,
editor version, skill version, and maximum three visual revision passes. The
supplied starting budget is 80 tool calls per trial; adjust it before comparing,
not midway through a failing model's run. Record actual calls, time, context,
reasoning setting, manual intervention and available cost data. Unknown values
stay unknown, not estimated as exact.

Keep all attempts, failed artifacts and intermediate candidates. Do not publish
only the best-of-N image. Do not allow private human hints or extra critic models
for one contestant only. Mask model names before human review. Judge in shuffled
order at both native scale and the same nearest-neighbor zoom.

If different clients provide different system instructions, tool filtering,
image handling or retries, call the comparison **model + host + toolchain**, not a
pure model benchmark. A stricter follow-up can use one multi-provider harness and
the same tool schemas/images, after verifying that harness actually supports the
selected models' vision and tool calls. Do not build a large harness before the
first useful pilot.

## Per-pass checks

After exporting the native working candidate without resizing/trimming:
```bash
RUN="$REPO/art-runs/pilot-01"
python3 "$SKILL/scripts/pixel_checks.py" check \
  --before "$RUN/input/baseline.png" --after "$RUN/work/candidate.png" \
  --mask "$RUN/input/editable-mask.png" --out "$RUN/passes/pass-01-checks.json"
python3 "$SKILL/scripts/pixel_checks.py" preview \
  --before "$RUN/input/baseline.png" --after "$RUN/work/candidate.png" \
  --crop 32 0 82 34 --scale 8 --out "$RUN/passes/pass-01-review.png"
python3 "$SKILL/scripts/prepare_run.py" verify-inputs --run "$RUN"
```
Use fresh filenames for subsequent passes. The checker fails on any changed
protected pixel, canvas drift, new visible colors, partial alpha, a blank result,
or a claimed edit that changes nothing. For a justified no-change diagnosis,
record that outcome explicitly rather than claiming a successful correction.
Generic override flags exist for other tasks; do not enable them to pass this
frozen benchmark.

These checks do **not** prove native editability or likeness. Inspect all native
layers and frame metadata; compare protected layers at full canvas coordinates.
For allowed head layers, still compare pixels outside the mask. Ensure layer
order/visibility/opacity/blend modes, frame count/timing, palette entries and cel
positions have not been silently changed. Reuse/adapt the repository's existing
`compare-and-check.py` plus its native source checks. Its historical v02-to-v03
paths must be parameterized for the copied v03-to-candidate comparison: merely
rerunning an old successful report does not validate new work.

Finally save, reopen the output copy and produce a fresh matching PNG. Report
this native check separately. Do not compare entire `.aseprite` file hashes for
equality after a legitimate edit; compare protected native data semantically.
Original/reference hashes, however, must remain unchanged.

Before another art pass, retain the actual native checkpoint/export and review the
original, shared seed, best eligible prior, and new candidate at 1x and identical
integer zoom. Verify comparison-sheet labels, paths, scale, clipping and matte. Record
the visual decision separately from technical status; identity or intended-expression
failure is a veto, not a score tradeoff. A corrective branch can remain in scope but a
failed or unreviewed pass cannot become the working selection.

## Human scorecard (0-4 per axis)

| Axis | What to judge |
|---|---|
| Identity | Does it resemble the approved face rather than a generic attractive character? |
| Geometry | Does eye spacing, near/far size, face angle and cheek/chin shape match? |
| Expression | Does the intended restrained, slightly quirky reaction survive simplification? |
| Hair/ear | Do fringe openings, tied-hair volume, tie and ear overlap match? |
| Pixel reading | Are clusters deliberate and facial features readable at native size? |

0 = unusable/worse; 1 = major mismatch; 2 = partial likeness with clear gaps;
3 = close with minor gaps; 4 = convincing match at this sprite's resolution.
Record the baseline rating and candidate rating, plus concrete reasons. This is
an ordinal human rubric, not a calibrated scientific likeness metric. Keep hard
compliance as a separate pass/fail column; do not average body damage, identity, or
expression failure into a good art score. Report all runs and the median/range, not
just the winner. The user makes final selection. An extra model critic is advisory
unless equally provided to all contestants and separately logged. For facial-expression
critique, apply [face-likeness.md](face-likeness.md) rather than rewarding a smaller edit.

## Deliverables

Native candidate, transparent export, head/full-body comparisons, patch history,
actual environment versions, source hashes, per-pass checks, native reopen/layer
checks, all failed attempts, remaining visual gaps, and human review status.
For every pass, record checkpoint/export identity, defect hypothesis, technical
result, original/seed/best/new evidence, visual decision, and next baseline. State the
best retained/selected candidate and reason separately from the last attempted
candidate; permit “none selected” or “awaiting review.” Proof-only duplicate edits do
not select an artistic candidate. No animation or Godot claim is implied by this
head-only benchmark.
