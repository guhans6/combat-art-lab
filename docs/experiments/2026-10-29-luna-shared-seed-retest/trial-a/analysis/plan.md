# Trial A bounded plan

## Trial profile

- Mode: same-seed model comparison / bounded native repair.
- Model/effort: `gpt-5.6-luna/max` (requested exact configuration).
- Backend: only the existing dedicated Aseprite AI Artist MCP, after an explicit
  supervisor editor-slot grant; no UI automation, Code-MCP, generic Lua, direct
  Aseprite CLI, new image generation or mode switching.
- Inputs: copied common baseline, seed PNG, ordered palette and the three declared
  references under `input/`.
- Budget: at most three artistic exports (initial plus two corrections), at most
  120 total Aseprite/editor calls including preflight, smoke/proof calls, failures,
  look/validate/export/save/reopen work. Actual calls will be logged in
  `technical-checks.md`; unknown provider compute/cost stays unknown.

## Preparation complete before editor slot

1. Copy the common native baseline, decoded seed PNG, baseline exports, palette
   extraction and declared references into the isolated trial directory.
2. Verify copied file hashes, native decoded RGBA, PNG decoded RGBA, dimensions,
   binary alpha, visible count/color count and exact ordered palette. Results are
   recorded in `technical-checks.md`.
3. Review original references, seed at 1×, seed at nearest-neighbor 4× and the
   head at nearest-neighbor 8×. Record the seed-use decision as bounded repair.
4. Wait. Do not call Aseprite, including preflight, until the parent grants the
   editor slot.

## Editor sequence and call accounting

Once granted, use one dedicated Aseprite session and only trial-a document IDs:

1. `preflight` (the first editor call), then the required scratch smoke/proof
   procedure from the pixel-art-director setup reference. If the backend is not
   ready, stop and report the capability boundary; do not switch backends.
2. Open/import the copied native baseline. Call `sprite_info` before any edit and
   record the actual layers, frame/cel, palette and editor/client versions.
3. Inspect the native baseline with a preview and pixel/ascii reads of the head and
   full body. Confirm the target layer and copy/save it as `pass-01` without
   touching shared files.
4. Add named correction layer(s) above the preserved `shared-source-seed` layer.
   Use one batched, palette-locked draw transaction for the smallest observed
   face/gaze/smile/fringe repair. Read back the edited patch, preview the full
   sprite and head, and export `pass-01.png` plus `pass-01.aseprite`.
5. Verify that every claimed native change reaches the exported PNG by decoded
   RGBA comparison and a localized changed-pixel report. A layer-only readback
   is insufficient. If the export is byte-for-byte the raw seed, classify the
   pass as unchanged/failed and retain the raw seed as the only eligible
   baseline before any further artistic work.
6. Run technical checks and make a direct comparison of approved reference, raw
   seed, best prior and `pass-01` at 1× and equal integer zoom. Record a visual
   decision before advancing. If identity regresses or no justified improvement is
   visible, retain the seed/raw baseline as best and mark pass-01 rejected.
7. Send the checkpoint to the supervisor and release the editor slot. Wait for
   defect-only feedback. Do not start a later pass while feedback is pending.

## Pass budget

### Pass 1 — initial bounded cleanup

Target only `M-face-expression` and, if directly connected, `M-fringe-tie`.
Preserve the full-body seed. Aim for clearer unequal eye widths, explicit rightward
gaze and a small restrained smile while retaining cheek/jaw, hair tie, silhouette,
pose and palette. This is the first artistic export.

### Pass 2 — one defect-only correction

Run only after the supervisor's defect-only feedback. Choose one observable defect
from the reviewed pass, such as merged far-eye/gaze cluster or a fringe/tie step that
weakens the face turn. Keep the mask and palette fixed, perform one coherent native
transaction, export and re-review. Do not polish unrelated clothing pixels.

### Pass 3 — final bounded correction or no-op stop

Run only if a second reviewed defect remains and the change has a concrete,
reference-supported hypothesis. It may refine one face/hair cluster or a directly
connected contour step. If the prior candidate is already the best eligible result,
stop without spending a speculative pass. A newer export is not automatically better.

## Proof and handoff sequence

After the best eligible candidate is named (and before any final claim):

- save the native master and reopen it through the same MCP route;
- export again and verify decoded pixel equality against the selected export;
- create a labelled duplicate, make one useful localized edit on the duplicate,
  verify the duplicate changed only in the intended region, and verify the selected
  master/protected raw layer stayed unchanged;
- retain every pass, failed candidate, proof duplicate and operation record;
- send the selected/latest checkpoint and release the slot; wait for defect-only
  feedback. User approval, Godot playback, animation, publication and production
  readiness remain unperformed.

## Stop rules

Stop at 120 calls, three exports, a missing backend capability, repeated visual
regression, or when no next change has an observed reference-supported improvement.
If no candidate passes the identity gate, deliver no selected result while retaining
the raw seed and attempted passes separately.
