# Assisted reconstruction

Use for new assets when source geometry/colors can reduce likeness drift. Protected
corrections retain their original masks, palette and metadata checks.

1. Open canonical originals. Record roles/hashes for each identity, style, pose,
   expression, lighting or simplification reference. The target is the same character,
   expression and aesthetic with intentional simplification, not pixel equality.
   Declare whether this is production/reconstruction, a model comparison, a
   method/recipe/source comparison, or a labelled end-to-end pilot. For a model
   comparison, freeze and verify the same derived seed and task; for another
   comparison, declare the recipe/source variables that differ.
   For ambiguous facial expression, use [face-likeness.md](face-likeness.md) to
   register landmarks, inspect visible ownership, and freeze the scope after that
   registration. **Ready:** exact inputs, grid/crop, display assumption, pass budget and comparison
   intent are frozen.
2. Identify missing evidence. Generate a focused image with available authorized tools
   and canonical attachments, or give the user a filled editable prompt, exact files
   to attach and expected image to return. Use the project's prompt pack linked from
   its art workflow; a standalone use can write the same explicit request directly.
   Review every generated candidate against originals before assigning agent use
   status; accepted-for-use does not mean user-approved.
   **Ready:** sources suffice for the next test, or dependent work is explicitly pending.
3. Select trace-guided drawing, converted seed plus cleanup, or a hybrid. Retain raw
   references, seeds and finished candidates separately. Record crop/scale, sampled
   palette, masks, traced boundaries, imported pixels and authored cleanup. An unchanged
   flat import is a seed; organize semantic parts needed for real revisions, without
   claiming that visible-part separation reconstructs hidden surfaces or an animation rig.
   For transparency cleanup, apply the [alpha coverage checks](alpha-coverage.md)
   to the actual exports before using them as animation inputs.
   Review original, raw seed and seeded native export at 1x and matched integer zoom.
   State whether the seed suits the named task, only a bounded repair, or needs
   re-preparation/a separately labelled reconstruction. A reference-supported identity
   correction may proceed inside a declared scope; retain unaffected cues and a
   reversible candidate.
   **Ready:** seed/blockout and actual native export have a direct original comparison
   and a recorded use decision.
4. For a method comparison, hold source/crop/grid/palette policy and bounded effort
   comparable. Use two checkpoints per initial arm unless another budget is declared
   beforehand. Historical redraws are context unless their conditions match. Review
   each actual export at 1x, integer zoom and declared display size; state continue,
   correct or reject with reasons across identity, expression, style, proportions and
   pixel craft. Include original, seed, best prior and new candidate; record technical
   status separately. Identity/expression failure cannot be offset by technical success
   or other rubric dimensions. Name the selected/best eligible checkpoint and reason,
   or no selection, separately from the last attempted pass. Shape overlap is diagnostic
   only. If a critic is used for a controlled comparison, provide equal assistance
   to every arm and log it apart from drawing effort. Follow the receiving project's
   review gate when one exists.
   **Ready:** retained candidates and separate visual observations support a recommendation.
5. Demonstrate a useful localized edit on a duplicate. Reopen/export and verify
   protected native layers, pixels, metadata and palette with existing checks. Report
   limits honestly, including cost/time unknowns. Stop weak branches; acquire a better
   reference only for a concrete source limitation.
   **Done:** native masters, provenance, all attempts, comparisons, edit evidence and
   checks are delivered, with user approval and motion/runtime status kept separate.

For motion use sheets or individual poses with shared scale/palette, declared slots,
pivots and root travel. No independent per-frame bounding-box fitting or accidental
removal of jumps. Inspect actual played motion before animation claims, and run Godot
before engine-readiness claims.
