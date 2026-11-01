# Pass 02 plan

Pass 02 responds to the supervisor's observed defects while preserving the good
pose, costume, framing, and broad material relationships. It is one coherent
expression-and-craft correction, not a redesign.

## Planned corrections

1. Remove the face overlay's two bright eye-white additions so the source's
   unequal near/far eye clusters carry the gaze without blocky highlights.
2. Erase the current three-pixel diagonal cheek-like smile and redraw a shallower,
   source-positioned warm smile using a shorter horizontal/curved cluster. The
   mark will sit inside the face plane rather than reading as a cheek slash.
3. Inspect the native 4x head and full-body views after the expression correction.
   If a contour still reads as a stray isolated step, make only a small, reviewed
   cleanup on the relevant semantic overlay; preserve the tied-hair silhouette,
   fringe openings, jacket outline, tote attachment, leg gap, and shoe grounding.
   No blanket smoothing, color-key deletion, or coordinate changes to the pose.
4. Save as `passes/pass-02.aseprite` and export `passes/pass-02.png`; retain pass 01.

## Proof work (not an additional art pass)

- Close/reopen pass 02 in the dedicated editor and export
  `passes/pass-02-reopen.png`; compare its pixel hash to `pass-02.png`.
- Open pass 02 as a separate duplicate document, add one useful localized tote or
  zipper accent only on a dedicated overlay layer, save as
  `passes/pass-02-local-edit.aseprite`, and export its PNG.
- Read back the untouched converted/raster layers in both documents and report
  equality/protection separately from the changed overlay layer. Do not overwrite
  pass 02.

## Evidence repair

The first comparison was visually ambiguous because it did not expose alpha and
framing independently. `scripts/make_review_sheet_v2.sh` emits explicit RGBA
source/candidate files, identical white and magenta composites, and side-by-side
alpha masks. Every sheet is generated from the exact candidate PNG path and its
hash is recorded alongside dimensions. The v2 evidence still received a supervisor
finding of materially different omitted regions between white and magenta views;
that presentation defect remains unresolved and is not treated as coverage proof.
The actual re-open/export hash comparison is independent and passed.

## Call budget

The supervisor-tracked budget at pass 01 release was 85/120, leaving 35 calls.
The correction and proof sequence is bounded to fit within that remainder; failed
technical calls remain in the ledger and no editor-mode switch is permitted.
