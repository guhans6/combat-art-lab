# Luna6 idle first-pass operation log

## Inputs and tool state

- Date: 2026-10-30.
- Dedicated Aseprite AI Artist MCP, headless; Aseprite 1.3.18.6-dev; extension 0.8.2.
- Baseline native source: `docs/experiments/2026-10-30-expression-strip/luna/passes/luna6-neutral.aseprite`, SHA-256 `d76266fa8afcd1de643e6b6421ec4dfe4fa77f8044a1d083205b921eb2f25540`.
- Baseline flattened PNG: `docs/experiments/2026-10-30-expression-strip/luna/passes/luna6-neutral.png`, SHA-256 `e7c62ff0e2f3f88b10b17904322f834175e62d33579cc646a9e6396f940b57ad`.
- Approved scene reference SHA-256 `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae`; approved close-up reference SHA-256 `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7`.
- Baseline source was directly opened, inspected and freshly exported before construction. It remained untouched. Candidate was saved to a new native path.

## Native construction

1. Duplicated the neutral frame seven times; set durations to 600, 350, 550, 600, 50, 80, 50 and 250 ms. Created an infinite forward `idle` tag over frames 1–8.
2. Tested a 1px upward whole-cel torso motion on frames 2–3 using the existing jacket, shirt, tote, strap and hand layers. The actual composite exposed transparent/garment coverage gaps, so each successful translation was reversed. The saved candidate has no moved cels.
3. The native action to move the full-canvas `07-face-and-neck` cel on frame 2 was explicitly rejected by auto-review because it would shift face/head content and violate the no-face-bob constraint. A frame-3 request returned no structured success; it was not retried after the explicit rejection. No indirect operation moved or edited that layer.
4. Added a restrained cloth-fold cue to `03-shirt` with palette-locked native drawing: F2 steps the highlight at `(60,60)` to `(60,59)` and restores the displaced shirt shades; F3 steps it to `(60,58)`; F4 returns to the untouched rest frame. The flattened diff from F1 is 2 pixels on F2 and 3 on F3 because one layer pixel is occluded in the composite. No palette entry was added and the tool reported no color snaps. This is provisional and may read too weakly as breath.
5. Drew the half/closed/half blink only on the registered owner `08-hair-tie-and-hair`, using existing palette colors `#fda977` (skin) and `#35150a` (lid ink).
   - F5/F7 half-lid: skin base over near-eye x62–66/y20 and far-eye x70–72/y20; short lid lines at near-eye x63–65/y21 and far-eye x71–72/y20; the existing lower-eye pixels remain open.
   - F6 closed: skin base over near-eye x62–66/y20–23 and far-eye x70–72/y20–21; lid lines at x62–66/y22 and x70–72/y21.
   - A first F6 pass also overwrote three pixels at far-eye y22, outside the registered mask. Readback showed their original values were `#f6a26e`, `#874c33`, `#c7744e`; all three were restored before saving. Final frame comparisons show zero head-layer changes outside the registered masks `[62,20,67,24)` and `[70,20,73,22)`.
6. Looked at the altered eyes, shirt-fold region, overall character and 8-frame MCP filmstrip. Shoes, denim, face-neck, stance and all cels outside the recorded pixel edits remain fixed.

## Saved artifact and proof

- Final native source: `passes/luna6-idle-breath-blink.aseprite`, SHA-256 `79c4ebc3df6f2d0c6d621d4c68329e075a10a8def7a9649463b312105d55221e`.
- Final Aseprite GIF: `exports/luna6-idle-breath-blink.gif`, SHA-256 `4f84de55ec798d3ebea2e282c771d790c382e5184ea8e145ef9046958dfad554`.
- Exported all eight transparent PNGs from the native document. A final save → close → fresh reopen as MCP document `#1583` → `sprite_info` → export confirmed 128×192 RGB, 8 frames, the `idle` tag, all 12 original layers and exact durations. The fresh-reopen flattened PNGs are pixel-identical to the earlier exports.
- Pillow was used only to compare native exports and arrange proof: `operations/render_proof.py` builds `exports/idle-transparent-strip.png`, `proof/contact-sheet-neutral-3x.png` and the 3× neutral-matte `exports/idle-neutral-3x-preview.gif`. It does not draw or modify source pixels.
- `proof/frame-metrics.json` records full-frame diffs and per-layer checks. Shoes, denim and face-neck layer exports are pixel-identical across frames; head differences are within the two blink masks. Native GIF timing was read back as 600/350/550/600/50/80/50/250 ms with infinite looping.
- The advertised `validate` action was absent from the active MCP tools, so it was not run. No Godot playback, user visual approval or production integration is claimed.
- MCP document `#1583` was closed after final export, releasing the editor lease before independent Sol review. Candidate files are stable for review. This is a review-only first pass.
