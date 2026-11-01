# Luna 5.6 Max — one full-body finishing pass

- Trial: `trial-a`
- Model assignment: Luna 5.6 Max (single attempt; no art retry)
- Date: 2026-10-30
- Intent: bounded model comparison / native finishing pass
- Baseline native: `inputs/baseline.aseprite` (frozen `candidate-b-structured.aseprite`)
- Baseline export: `inputs/baseline-reopen.png`
- Source-only seed: `inputs/source-only-converted-seed.png`; inspected as provenance only and not edited
- Authoritative references: `inputs/character-scene.png` and `inputs/character-closeup.png`
- Native canvas: 128×192 RGB, 255-entry palette, binary alpha, one frame, 12 layers
- Visible structure: 11 visible editable art layers plus one hidden/locked guide layer
- Protected: canvas, palette, alpha/silhouette, pose, eyes, mouth identity, layer names/order/visibility, guide layer, frame count/timing
- Scope: one coherent finishing pass across hair, jacket/shirt, jeans, tote/strap and shoes; no canvas, palette, or pose change
- Mouth rule: preserve the original restrained shallow smile. No pout, U-shape, dotted mouth, or uncertain mouth correction. The mouth was left unchanged.
- Review rule: candidate may be agent-preferred only provisionally; user selection/approval remains pending. A clean native file is not an artistic approval.
- Backend: dedicated Aseprite AI Artist MCP, headless only; Aseprite 1.3.18.6-dev; extension 0.8.2
- Pass budget: one actual art pass. Subsequent save/reopen work was technical proof only, not a second artistic pass.

The authoritative scene and close-up were visually inspected before drawing. The scene shows the complete long-legged three-quarter character with tied brown hair, olive jacket, wide blue jeans, cream tote, pale shoes and warm/cool cinematic lighting. The close-up confirms the broken fringe, tied hair/bun, unequal near/far eyes, rightward gaze and shallow original smile. The candidate's face remains under-articulated relative to the close-up; the eye and mouth identity gate is therefore not claimed as solved.

