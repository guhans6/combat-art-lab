# Aseprite lease plan

This was the pre-lease sequencing checklist. The serialized lease was completed;
actual calls, observed deviations and tool limitations are recorded in
`session-log.md` and `mcp-operations.json`.

## 1. Capability and isolated smoke proof

1. Call `preflight` in explicit headless mode first; stop if not ready.
2. Discover the live tool declarations. Call `sprite_info` before the first edit.
3. In a scratch-only document inside this folder, verify a 16×16 asymmetric pattern
   across two named layers, exact pixel coordinates, one-pixel change, transparent
   erase/skip behavior, save, close/reopen and fresh PNG export. Keep one layer
   protected and compare the intended one-pixel change. Do not use the production
   candidate as the smoke-test document.
4. Record any missing capability (including tool-side `validate` if absent); do not
   claim a pass for a call the server does not expose.

## 2. Candidate setup and native drawing

1. Open the frozen neutral input, record its explicit returned sprite ID, `sprite_info`,
   layer/cel metadata and palette. Save a separate working copy through MCP before
   the first production mutation.
2. Preserve input frame/rest pixels, canvas, palette, 12 layer definitions and hidden
   guide. Use explicit sprite IDs, frame numbers and layer names on every edit call.
3. Duplicate complete native cels into each planned frame. Keep unchanged layers
   copied/static. Copy only the permitted blink-source `07-face-and-neck` cel drawings
   for candidate frames 8–10 after inspecting both native owners and alignment.
4. Use MCP pixel readback for torso owner boundaries. Author local contour/cloth-plane
   changes on `03-shirt` and the relevant jacket owner(s), respecting the bounded chest
   region and seam/strap/hands. Do not translate a whole frame, warp row bands, or add
   a new color. Batch deliberate drawing ops per target cel. Read/preview every key
   before extending the in-betweens.
5. Log actual tool/model/editor versions, sprite ID, tool call counts, operations,
   frame order and durations in this folder. Keep every saved checkpoint under the
   allowed pass budget.

## 3. Export and proof

1. Save the working native source through MCP and export every actual composite frame
   to `frames/` through MCP. Export transparent native-size frames; save durations in
   the same order. Make 1× and nearest-neighbor 3× contact sheets for full body and
   the shirt/jacket torso, with a neutral matte and source pose labels.
2. Build 1× and 3× neutral-matte GIFs from the exported PNG frames without adding
   colors. Use source-native frame durations. Decode them and compare each displayed
   frame against the intended flattened composite to expose palette/timing drift.
3. Inspect the chest keys, adjacent transitions, the blink, the loop seam, fixed feet,
   frame-by-frame material roles and alpha coverage. Record motion/material/expression/
   scope/technical decisions separately. If actual-speed playback cannot be observed,
   leave temporal naturalness unverified.
4. Close only this saved document, reopen the saved native candidate through MCP,
   export every frame fresh, and compare decoded pixels/timings against the prior
   intended exports. Verify layer definitions, palette, hidden guide, original rest,
   static/native protected layers, alpha and input hashes. Make one duplicate-only
   local revision on a separate copy, save/reopen/export it, and demonstrate the
   candidate changes while protected source data stays intact.
5. Only after the post-reopen proof, close this document and report
   `LEASE_RELEASED` with the `delivery.json` paths. Do not close any document not
   opened by this assignment.
