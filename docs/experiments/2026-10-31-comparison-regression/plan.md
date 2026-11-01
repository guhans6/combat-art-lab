# Plan: review the repair and its regressions

31 October 2026. Separate planning pass after [research](research.md); parent
implements. Approved scope and acceptance are in [request.md](request.md).
Use `implement` with TDD at the three already agreed comparison-tool seams, then
independent standards/spec review. No further clarification is needed. This changes
the workflow and evidence preparation, not artwork or artistic approval.

## Decision and observed baseline

Keep `pixel-art-director` as the entry. Add one small batch comparison-packet helper
that imports the existing `pixel_checks.py` canonical pixels, mask/check functions,
difference rendering and review sheet. Add one authoritative disclosed comparison
procedure. This is justified because the current helpers cannot account for every
changed pixel across named close-review regions or verify a packet's freshness.
Keep the new helper near 200–300 lines if practical; avoid a review engine, numerical
art score, automatic alignment, inferred edit scope or new dependency/service.

The existing mask/protected-pixel checks already work; new tests should prove their
integration at this public packet boundary rather than count them as new detection.
`reference_review.py` remains the original-versus-export helper. A baseline diff
complements it; neither replaces approved-reference inspection or native protection.

I opened the actual 320×192 `artist/sol-rescue/preparation/frame-09-base.png`,
`artist/sol-rescue/frames/v03-frame-8.png` and frozen user rejection crop. They show
changed forearms, cuffs, hands, handles and bag placement on shared coordinates.
The candidate's hand/strap junction remains visually ambiguous; this interpretation
agrees with the user rejection and is not a new independent discovery.

Provenance: `prepare.py` constructs registered 320×192 additional-2;
`build_native_inputs.py` uses it for zero-based frames 8/9 and saves the recomposed
base as `frame-09-base.png`. `artist/delivery.json` binds final zero-based frame 8 to
v03. A read-only probe using the existing bundled Python/Pillow and canonical helper
found 2,680 changed pixels, bounds `[145,0,217,157)`. Crop `[140,55,225,150)` misses
30 changes, including four curl-tip pixels at `(161,0),(162,0),(161,1),(162,1)`.
This gives a real coverage failure without altering art. The historical 256×192
`recovery-source-v00.png` comparison is unregistered and unsuitable for exact diff.

## Public packet boundary

Add `scripts/comparison_review.py` with callable build/verify functions and:

```text
comparison_review.py build --spec comparison.json --out NEW_PACKET_DIRECTORY
comparison_review.py verify --packet NEW_PACKET_DIRECTORY/packet.json
```

Use one documented JSON spec, paths relative to the spec file:

```json
{
  "baseline_role": "rejected diagnostic pre-repair; not approved art",
  "registration": "same native grid; describe provenance here",
  "required_frame_ids": ["F9"],
  "evidence": [
    {"role": "candidate native", "path": "candidate.aseprite"},
    {"role": "native/export verification", "path": "existing-checks.json"}
  ],
  "frames": [{
    "id": "F9", "before": "before.png", "after": "after.png",
    "mask": "explicit-scope.png",
    "regions": [{"name": "forearm-hand-handle-rim", "crop": [140,55,225,160]}]
  }],
  "zoom": 4
}
```

Required frame IDs are the task's declared affected-frame inventory; reject missing,
extra or duplicate entries. They do not prove that the declaration covers the native
timeline: the existing native/export audit and reviewer own that boundary. Optional
evidence entries bind originals, neighboring frames and playback when relevant.
Hashing a native/check report binds identity; it does not parse or certify the
report's native-to-PNG correspondence. Record that limitation explicitly.

For every frame, require equal dimensions and a stated same-grid registration
basis. Matching dimensions alone do not establish anatomical registration. Refuse
size mismatch with a clear error and retain the separate reference-view route;
never fit, rescale or translate inputs automatically. Validate named nonempty crop
bounds and integer zoom. Reuse the existing explicit binary edit-mask semantics.
Keep all inputs and earlier output directories unchanged.

Build the canonical changed set D; report existing scope result D−M and new
close-review coverage D−R, with count, bounds and coordinate examples. R is the
union of explicitly named close crops; the automatic whole-asset overview is
excluded. A covered change is merely available for inspection. Inside-mask damage
is still possible. Generate each named clean baseline/candidate/difference sheet
with the existing 1x overview and matched integer crop. Make `review_sheet`'s label
part-neutral (default “Review crop”; optional region label if useful), preserving
existing callers. No connected-component subsystem is necessary for this increment.

Write a packet with spec/input/evidence hashes, source dimensions, exact half-open
crops, zoom/matte/resampling, every generated sheet's hash, per-frame checks and
aggregate `mechanical_passed`. Include explicit `visual_acceptance: pending` and
user approval pending. A successful build or verify never changes these to pass.
Noop packets honestly report zero visible changes, using the existing allow-noop
behavior; they do not imply improvement. Scope/coverage failure still emits the
diagnostic packet and exits 1; invalid inputs exit 2. Verify recomputes hashes of
the spec, all bound sources and sheets, reports missing/stale files and exits
nonzero; freshness success says only that the recorded packet is unchanged.

Keep the eventual visual review in a short separate record naming the packet JSON
hash and exact candidate/native hashes. Before relying on that review, compare its
packet hash and run verify. This is enough stale-review protection; avoid a prose
validator, machine-generated art verdict or mutable clearance lifecycle.

## One disclosed procedure

Create `references/comparison-review.md`; add concise triggers in SKILL steps 4/5,
the animation review section and project workflow stage 6. Condition: a meaningful
revision/correction with a before/candidate baseline, including animation frame
repairs. Keep expression/anatomical registration rules and animation material rules
in their existing references. Do not replicate this procedure in those pointers.

The procedure must require the reviewing agent to:

1. Freeze baseline role, target improvement, exact candidate/native/export binding,
   allowed scope, important attachment chains and affected-frame inventory. Open
   actual images. For unregistered reference comparisons state that limit and use
   the existing reference helper instead of inventing exact-diff evidence.
2. Build the packet; resolve scope failures and uncovered changes before clearance.
   Add explicit close crops for legitimate peripheral changes, retaining the first
   failed packet. For a diagnostic replay, label retrospective masks as diagnostic,
   not prior authorization. Enlarging a mask does not repair an unauthorized edit.
3. Inspect clean images and differences: target feature; all changed regions,
   including changes inside the allowed mask; connected unchanged surroundings;
   whole-asset silhouette/proportions/expression/materials at 1x and integer zoom.
   For sequences inspect adjacent keys/transitions and loop return when affected,
   plus authored-speed playback where perceptually available. Record still-only
   evidence honestly. Generation of crops alone is not completed visual review.
4. Record separate target-improvement and regression observations. For each named
   region/important join give concrete relation, frame/crop/scale, viewed path and
   pass/reject/uncertain. Ask “which edge covers which, where does it reappear, and
   what supports the load?” For this tote follow cuff→wrist→fingers→each handle→rim;
   “connected” alone is insufficient. Ask what became worse even if the target
   improved. A disputed structural join remains rejected/pending and cannot be
   offset by mechanical success. Preserve best eligible prior or no selected result.
5. At the existing independent critic boundary, provide task/locks/exact packet
   without prior praise or the producer's success conclusion. Critic first describes
   visible relations and seeks regressions, then gives a decision with uncertainty.
   This reduces anchoring opportunity without claiming reliable debiasing. A critic
   edit requires fresh inspection by another reviewer. Keep existing bounded review
   routing; ordinary work does not acquire an unconditional new Sol review.
6. Bind review to the packet hash, run freshness verification before advancement,
   and retain separate user approval and playback/engine decisions. Any source edit
   requires a new packet and affected visual review.

## TDD and checkpoint sequence

Use bundled Python already documented at
`/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
No installation needed. Keep new tests in `tests/test_comparison_review.py` at
build/verify/CLI behavior. One failing test → minimal passing implementation per slice:

1. **Scope and coverage:** small literal RGBA fixture includes one permitted target
   edit and one remote edit. A narrow mask fails outside scope; with a deliberately
   broader mask the narrow crop still fails coverage. Adding its named crop clears
   bookkeeping, while visual acceptance remains pending. This distinguishes the
   existing scope detector from the new regression-attention behavior.
2. **Exact identity:** build a complete packet, then alter a source PNG byte/pixel
   and verify fails; restore and alter one generated sheet, then verify fails.
   Include native/evidence/spec freshness using the same public behavior. File-hash
   changes beneath zero alpha are stale evidence even when canonical D is empty.
3. **Honest status:** complete in-scope covered edit passes mechanical checks yet
   remains visually pending; identical inputs report noop rather than improvement.
4. **Batch/invalid boundary:** missing required frame, canvas mismatch and invalid
   crop fail clearly. Existing/input output collision preserves bytes. Add only
   cases justified by actual validation paths; do not unit-test internal plumbing.

Capture meaningful red/green outcomes in the experiment record. Run the complete
existing director suite after these slices, then the real replay and instruction
review. Tests prove preparation, identity and status separation, not anatomy.

## Real replay and final verification

Parent owns the replay under this experiment, without native writes:

- Historical 256×192→320×192 pair: demonstrate exact-edit refusal; label old sheet
  a nonregistered reference view. Do not claim a valid old-grid diff.
- Registered F9 pair: build target-only crop and explicit narrow diagnostic mask;
  show outside-scope and uncovered changes, including curl-tip movement. Build a
  second separately labeled diagnostic packet with explicit allowed diagnostic
  regions covering actual body/bag changes and curl tip. Retain the failed packet.
  Complete close crops can pass mechanically while the known user grip rejection
  remains rejected. No retrospectively approved scope or automatic anatomy detection.
- Include final neighboring F8/F10 context as bound evidence and inspect it; label
  this F9 diagnostic, not a new whole-animation clearance. Reuse existing source/
  export verification or fresh read-only native audit; state exactly which ran.
- Write concrete target/regression observations using actual images. Disclose that
  the replay's defect is already known. It tests exposure and honest disposition,
  not independent blind defect-detection accuracy.

Before completion, independent standards/spec reviewers inspect the task-start
snapshot delta, this request/plan and resulting artifacts. Include instruction
scenarios: inside-mask regression; peripheral uncovered edit; stale candidate;
unregistered reference; omitted frame; still-only animation; critic edits own work;
mechanical pass with rejected grip. Resolve actionable findings and rerun affected
checks. Keep standards/spec reports separate.

Use task-start preservation hashes to verify art, native masters and unrelated dirty
work remain intact, excluding only explicitly owned workflow/test/experiment/handoff
files. Update one experiment record and handoff with checks, artifact hashes and
remaining boundary. Source workflow and local symlink enablement may be verified;
portable archive refresh and another-host installation remain unperformed unless
separately requested. No Godot run, art generation, commit or publication is needed.
Completion is the bounded source change, fresh tests/replay/review and preservation
evidence; the user still owns visual approval of art, and this task delivers no repair.
