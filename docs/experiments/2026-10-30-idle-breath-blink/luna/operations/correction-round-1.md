# Correction round 1 — chest/shoulder breath deformation

## Review trigger and scope

- Trigger: Sol rejected pass 0's breath gate because its 2–3-pixel shirt-fold highlight was only a shading speck at 1×.
- Scope: create a separate corrective native checkpoint while preserving the pass 0 source and exports. Keep the existing blink exactly, feet/denim/face/head fixed, no whole-cel movement, and no new pose or outfit. The revised motion uses local chest/shoulder garment deformation.
- Pass 0 native SHA-256: `79c4ebc3df6f2d0c6d621d4c68329e075a10a8def7a9649463b312105d55221e`.

## Construction

- Opened pass 0 through the dedicated headless Aseprite AI Artist MCP, verified its 8 frames/12 layers, then saved a new copy at `passes/pass01/luna6-idle-breath-blink-pass01.aseprite` before edits. Pass 0 remains untouched.
- Removed the previous F2/F3 shirt-highlight speck by restoring those exact `03-shirt` source pixels from frame 1. This leaves only the new body motion on F2–F4.
- Added a connected 1px outward chest-width expansion by copying the existing edge colors of the shirt onto the next pixel on both sides of `03-shirt`. F2/F4 are the partial state over rows y51–54; F3 is the fuller state over rows y48–56. F4 returns to the partial state, then F5 returns to rest during the blink.
- Added matching outer shoulder contour pixels to the jacket layers so the chest change reads as upper-body expansion, not only an interior color shift.
  - F2/F4, `02a-jacket-left`: `(40,44) #393628`, `(40,45) #3b351c`.
  - F2/F4, `02b-jacket-right`: `(86,44) #2a2416`, `(87,45) #48432d`.
  - F3, left: `(41,43) #5a5437`, `(40,44) #393628`, `(40,45) #3b351c`, `(39,46) #48432d`.
  - F3, right: `(85,42) #242116`, `(86,43) #48432d`, `(86,44) #2a2416`, `(87,45) #48432d`, `(87,46) #2d291d`.
- The expansion is additive/overpainting on existing garment layers; no cel origin moved. The full alpha coverage comparison found zero opaque-to-transparent pixels lost.
- Blink drawing was not changed in this round.

## Final native/export evidence

- Native source SHA-256: `d5b9d7675de8bea50a1941361d3e3bed3c187b3ee7e1d7e0585d51f8d37cc8ed`.
- Native Aseprite GIF SHA-256: `b2bf854e2ed5476ba468c6376b7bd2f3cea67c0701ae69979e26734c1ea40398`.
- Final source was saved, closed, freshly reopened as MCP document `#3807`, verified as 128×192 RGB with 8 frames, 12 original layers and `idle` tag, then all final flattened and protected-layer exports were produced. The document was closed before Sol review.
- F2/F3/F4 composite changes from F1 are 11/24/11 pixels; bounds are x40–87/y44–54, x39–87/y42–56 and x40–87/y44–54. All changes are inside the registered chest/shoulder motion mask x39–88/y42–56.
- Mechanical results in `proof/pass01/frame-metrics.json`: zero alpha pixels lost; zero composite changes outside the body and eye masks; shoes, denim and face-neck layer exports are pixel-identical across all frames; all head-layer changes remain inside registered eye masks; fresh-reopen frame exports match the primary PNG exports pixel-for-pixel; native GIF retains exact `[600,350,550,600,50,80,50,250]` ms timing and infinite loop.
- Visual evidence: `proof/pass01/contact-sheet-neutral-3x.png`, `exports/pass01/idle-neutral-3x-preview.gif`, and the MCP torso crop/filmstrip were inspected. The corrected candidate is submitted for defects-only Sol review; read clarity at 1× remains open.
- Not run: Godot playback and user visual approval.
