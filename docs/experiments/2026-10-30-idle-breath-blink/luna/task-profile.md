# Luna6 idle breath and blink — frozen profile

- Date: 30 October 2026.
- Intent: one short, quiet, review-only idle loop. It is not production approval.
- Construction route: Luna6 Max through the dedicated Aseprite AI Artist MCP in headless mode.
- Aseprite: 1.3.18.6-dev; Aseprite AI Artist 0.8.2.
- Exact native baseline: [`luna6-neutral.aseprite`](../../../2026-10-30-expression-strip/luna/passes/luna6-neutral.aseprite), SHA-256 `d76266fa8afcd1de643e6b6421ec4dfe4fa77f8044a1d083205b921eb2f25540`.
- Baseline PNG: [`luna6-neutral.png`](../../../2026-10-30-expression-strip/luna/passes/luna6-neutral.png), SHA-256 `e7c62ff0e2f3f88b10b17904322f834175e62d33579cc646a9e6396f940b57ad`.
- Approved full-body identity/style reference: [`character-scene.png`](../../../2026-10-30-expression-strip/luna/inputs/character-scene.png), SHA-256 `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae`.
- Approved close-up face, hair and expression reference: [`character-closeup.png`](../../../2026-10-30-expression-strip/luna/inputs/character-closeup.png), SHA-256 `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7`.

## Frozen construction brief

- Preserve the exact 128×192 RGB canvas, 255-entry palette, 12 existing layer names/order/visibility, character volume, hairstyle/fringe, outfit, tote and original stance.
- No new poses, weapons, facial expression change or root translation. Keep both feet/shoes and the entire denim layer pixel-identical on every frame. Keep the face/head cel fixed except for the blink.
- Keep both feet/shoes, the full denim layer, the face/head position and all cels fixed. A whole-cel 1px torso translation was tested, produced garment/neck coverage holes, and was fully reverted. The native tool also rejected moving the full-canvas `07-face-and-neck` cel because it would shift the face; that action was not retried or bypassed. The first loop uses only a tiny shirt-fold highlight shift as a provisional breath cue, with no body or head translation. Its readability is unresolved pending Sol review.
- Blink is restricted to the existing near-eye pixels within `[62,20,67,24)` and far-eye pixels within `[70,20,73,22)` on layer `08-hair-tie-and-hair`. Preserve brow/fringe, nose, mouth, jaw, gaze direction, hair contour and all pixels outside those eye masks. Do not alter any face marks on another layer.
- Eight-frame sequence: rest/open, inhale/open, inhale hold/open, return/open, half-lid, closed lid, half-lid, open/rest. Timing `[600,350,550,600,50,80,50,250]` ms = 2,530 ms total. Eyes remain open for 2,350 ms (92.9%). The final 250 ms open pose plus first 600 ms rest is kept under one second across the loop seam.
- Initial drawing pass only; at most two bounded correction rounds after independent Sol critique. Retain every checkpoint and exact drawing-operation log.

## First-pass evidence

- Native source: [`luna6-idle-breath-blink.aseprite`](passes/luna6-idle-breath-blink.aseprite), SHA-256 `79c4ebc3df6f2d0c6d621d4c68329e075a10a8def7a9649463b312105d55221e`.
- Native Aseprite GIF: [`luna6-idle-breath-blink.gif`](exports/luna6-idle-breath-blink.gif), SHA-256 `4f84de55ec798d3ebea2e282c771d790c382e5184ea8e145ef9046958dfad554`.
- Eight transparent native frame exports are `exports/frame-0.png` through `frame-7.png`; the horizontal RGBA layout is [`idle-transparent-strip.png`](exports/idle-transparent-strip.png). The 3× neutral-matte loop preview is [`idle-neutral-3x-preview.gif`](exports/idle-neutral-3x-preview.gif); the contact sheet is [`contact-sheet-neutral-3x.png`](proof/contact-sheet-neutral-3x.png).
- Final native source was saved, closed, freshly reopened in Aseprite MCP, inspected as 128×192 RGB with 12 original layers and an infinite `idle` tag, re-exported, and closed. Reopened flattened frame exports are pixel-identical to the first exports. Exact durations are `[600,350,550,600,50,80,50,250]` ms (2,530 ms); the exported native GIF has the same durations and loop=0.
- Pillow comparisons of the reopened native exports confirm shoes, denim and face-neck layers are pixel-identical across all frames. Head-layer changes are confined to the registered eye masks; changed-pixel counts in frames 5–7 are 13/26/13. Composite changes from frame 1 are 2/3 pixels for the two breath-cue frames, 13/26/13 for the blink frames, and zero for the other frames. Details are in [`frame-metrics.json`](proof/frame-metrics.json) and [`first-pass-log.md`](operations/first-pass-log.md).
- The Aseprite MCP build did not expose the advertised `validate` operation; native metadata, previews/filmstrip, exported frame comparisons and GIF timing were used instead. No Godot playback or production approval is claimed. This is a review candidate; user visual approval is separate.
