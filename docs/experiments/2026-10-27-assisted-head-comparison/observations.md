# Direct observations and checkpoint decisions

Canonical scene and close-up were visually opened before construction. Close-up crop
(380,64)-(860,512) shows a rounded swept crown, asymmetrical fringe openings, tied
rear clumps with a pale tie, right-facing unequal eyes, soft cheek and shallow smile.
The source resolves this still; more generation is not needed merely to add inputs.
No full-character scale or gameplay camera is inferred from this 120x112 crop study.

- Technical failed A batch: only jacket rendered because newCel copied an image
  before later draw operations. The initial script also saved multiple checkpoints
  before visual review. Those outputs remain under unreviewed-batch, excluded from
  visual-method comparison. The corrected script flushes completed cel images and
  emits only the requested checkpoint, reviewed before the next artistic pass.
- A00 corrected: gated/a00-review.png inspected. Hair envelope/cowlick, neck and
  shoulder alignment follow the original; broad face/cheek shape is simplified and
  feature-free at this stage. Continue to traced hair-plane refinement, then features.
- B00: b00-review.png inspected. BOX-derived source geometry preserves the actual
  turned face, restrained expression and tied-hair structure markedly better than
  historical redraw. Reduction gives muddy/noisy fine hair/eye accents, and traced
  mask crops some loose hairs. Continue targeted hair cleanup; retain original seed.

The input source, grid, crop and shared 48-color source-derived palette policy are
identical for both arms. Manual trace geometry and source pixels differ by method.
Two refinement checkpoints per arm are the equal ceiling, not measured equal labor.

- A01: gated/a01-review.png inspected before features. Crown/rear-hair plane flow
  follows the source but simplifies it strongly; far fringe is a broad graphic cap.
  Continue to source-positioned features once, then compare. No resolution claim.
- B01: b01-review.png inspected before features. Retains convincing source face
  and shallow smile, with only a small tie/strand cleanup. Hair still has dense
  sampled texture; source palette reduction darkens some highlights. Continue one
  lid/mouth clarity pass, rejecting it if the delicate expression becomes graphic.

- A02: gated/a02-review.png inspected. Source mapping improves layout control, but
  manual plane/feature interpretation still flattens hair, enlarges the soft cheek,
  weakens eyelids and loses the canonical face/style. Reject as final treatment;
  preserve it as trace-method evidence. More detail would not fix the core interpretation.
- B02: b02-review.png inspected. Same person/rightward expression and hair flow
  survive better than A or the historical redraw. Lid boundary is clearer; the mouth
  remains subtle. Provisional choice for this bust study, with dense/muddy hair texture,
  simplified loose hairs and mask-edge/portrait-versus-gameplay questions remaining.
  This is not user art approval or full-character production-scale selection.
- Generated blink sheet: visually inspected returned image. Three open/half/closed
  poses are present on an opaque gray background. Canonical hairstyle/outfit and face
  broadly survive, but bun shape/strand detail, cheek and framing differ slightly;
  half-lidded pose can read sleepy in isolation. Accepted for agent use ONLY as eyelid
  closure guidance, not replacement silhouette, palette, crop or identity authority.
  Native motion will retain the selected bust's pixels and redraw just the eyes.

- Native/display review: native-and-display.png inspected at 1x and diagnostic 2x.
  B reads as the canonical person; A reads as a flatter, less specific face. At 1x
  B's hair texture is dense and eye/mouth marks are subtle; neither establishes a
  full-character/gameplay grid. Blink filmstrip was inspected: open/half/closed/half/
  open states retain head volume/outfit and a stable silhouette; closed lids are
  rather straight, and the temporary half state looks sleepy when paused.
- Scratch verifier initially assumed a trimmed cel when making its allowed mask;
  native inspection showed a full-canvas cel and the Lua intentionally changed
  (0,0). Corrected mask to that actual declared scratch coordinate; the strict native
  checker itself is unchanged and rejects the all-protected negative-control mask.
- Mask preparation initially mixed BOX silhouette coverage with NEAREST ownership,
  leaving unassigned boundary pixels. Requiring nonzero BOX coverage for semantic
  ownership fixed coverage; exact visible reassembly is independently checked.


- Played review: Codex browser progressed through all five actual exports at native
  timing; saved AX events show 1600/1650/1740/1800 ms transitions over repeated loops.
  Paused half/closed poses were opened at 1x/2x. Closure/reopening is readable and
  head/outfit stays registered. Straight closed-lid marks remain a craft limitation.
  No broader animation/attack or Godot claim is made.


- Final mouth-detail-review.png exposed an expression regression that the broad B02
  sheet review underweighted: the sampled cleanup color erased the shallow smile's
  middle into separated marks. B02 mouth is rejected. Optional hybrid C01 keeps its
  clearer eyes but restores exactly B01's native mouth layer. c01-review.png inspected:
  shallow smile returns without other changes. Strict native rollback and duplicate
  tie-edit checks passed. Final blink uses this restored mouth in every frame; earlier
  B02 static/motion and pre-rollback review images remain preserved. Selection is C01.
