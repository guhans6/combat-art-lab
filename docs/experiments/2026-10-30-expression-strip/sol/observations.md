# Independent Sol expression review preflight

30 October 2026. Reviewer/editor: requested Sol6.1/high. Local correction/review experiment, not a model benchmark. Authority: approved `assets/references/approved-2026-10-26/character-scene.png` (identity/pose/full context) and `character-closeup.png` (identity/expression detail). Baseline: `docs/experiments/2026-10-30-luna-fullbody-once/trial-b/passes/luna6-fullbody-cleanup.{aseprite,png}`. These actual reference images and the exact baseline export were opened independently before reviewing Luna's expression outputs. Preflight hashes are in `inputs/preflight-input-hashes.json`. No prior Sol smile is approved or automatically inherited.

## Observed reference and registration

The original shows a rightward three-quarter head, larger near eye, narrower far eye, rightward gaze, broken brown fringe and a fine closed smile. The mouth is a shallow, slightly unequal curve, with dark small corner accents and a lighter center; the smile does not form a dark broad U. The original scene presents the same quiet friendly character in whole-body context. Hair/body/costume identity are protected in this task.

Approximate close-up landmarks independently checked against direct original crops: near eye center around (655,289), far eye around (720,278), faint nose cue around (719,309), smile corners around (675,336)/(707,336), low center around (690,342), chin around y374. Confidence is high on the visible mouth curve, medium on approximate eye/chin centers, and lower on the faint nose cue. These are approximate anatomical landmarks, not exact corresponding native pixels or a rigid source transform.

Baseline at native full-body size and a 16x nearest-neighbor head crop: near eye around (64,22), far eye around (71,21.5), higher warm cue around (71,24), lower warm pair at (68,27)/(69,27), chin around y30 and underjaw shadow around y31. Eye-to-chin registration places the lower pair at mouth height. It likely represents an inherited mouth simplification (medium confidence), rather than a blank face requiring an additional mark. The different source/cutout head proportions leave residual alignment uncertainty. No reference panel may be warped to make the result appear faithful.

Reference direct face crop is (520,170)-(820,470), sprite head crop (50,10)-(80,40). Approximate 10:1 reference-to-sprite review mapping puts the near eye near (63.5,21.9), far eye near (70,20.8), mouth near (67.1,27.2), and chin y30.4. A small mismatch remains, especially at the far eye; canonical original pixels remain available alongside any reduced preview. `reviews/original-face-direct.png` and `original-mouth-direct-6x.png` preserve the direct original; `baseline-head-16x.png` preserves actual native pixels.

## Review criteria frozen before Luna inspection

- Neutral: relaxed resting closed mouth, no obvious smiling or frowning corners, baseline identity and quiet open-eye relationship retained.
- Subtle smile: one low-contrast closed friendly curve at the registered mouth site; no second floating stroke, broad U, pursed lip, conspicuous grin or dark disconnected diagonal. Read the full body at 1x before zoom can imply success.
- Surprise: an unmistakably open compact mouth plus coherent eye/brow response within facial interiors, while keeping rightward gaze, unequal eye relationship, head turn and the same character. Do not credit an intended 'surprise' label if the visible result only reads worried or decorated.

Actual Luna outputs remain unread until parent confirms completion. No Aseprite MCP call until parent grants exclusive editor lease. For any necessary rescue: inspect actual owning layer/frame/cel/readback, freeze mask after registration, edit new copies only, preserve palette/alpha/outline/hair/pose and all other native content, and log exact operations. One initial rescue plus at most one parent-defect correction round. An edited checkpoint requires fresh parent visual inspection before selection; user approval remains separate.

No standalone scratch smoke or backend invocation performed in this preflight. The skill doctor inventory found Python3.12.14/Pillow12.3.0 and the editor binary but its `--version` check exited -6 without output; that inventory does not establish backend health. Existing MCP evidence may be supplemented after editor lease. No native art has been edited.
