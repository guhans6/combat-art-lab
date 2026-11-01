# Aseprite/editor call log

Budget: 120 calls total; count all Aseprite MCP service operations and documentation-resource calls conservatively.  
Used before scratch setup: 15. Artistic exports: 0 / 3.

1. `preflight({})` — ready; headless mode already active; `switched:false`; Aseprite 1.3.18.6-dev; extension 0.8.2; no document open.
2. MCP resource catalog — discovered rules and workflows (documentation only; counted conservatively).
3. `rules://index` — read.
4. `skill://fix` — read.
5. `rules://11-clusters-and-noise` — read.
6. `rules://32-heads-and-faces` — read.
7. `rules://33-eyes-and-expressions` — read.
8. `rules://35-hair-and-clothing` — read.
9. `rules://06-layers-and-rigging` — read.
10. `rules://07-review-checklist` — read.
11. `skill://new` — read.
12. `skill://draw` — read.
13. `skill://review` — read.
14. `rules://00-core-principles` — read.
15. `rules://01-palette-and-color` — read.

For each subsequent call, append its number, exact tool/operation, explicit document ID, concise arguments, purpose, and returned status. Failed calls and smoke/proof calls count. Do not reset the count between passes.
16. `sprite_manage new` — created owned scratch `#3`, 16×16 RGB, one default layer.
17. `sprite_info` on explicit `#3` — confirmed 16×16 RGB, one frame, default `Layer 1`, 256-entry all-black RGB table.
18. `sprite_manage new` — accidentally created a second owned blank scratch `#7`; no edits or files. Will close it without force and continue on `#3`.
19. `sprite_manage close` on explicit `#7` — closed the unintended extra blank scratch; no force/discard used.
20. `layer batch` on scratch `#3` (`Layer 1` rename + create) — failed with `aseprite_error: function: 0xb0cd78be0`.
21. `layer rename` on scratch `#3` — failed with `aseprite_error: function: 0xb0cd78aa0`.
22. `layer list` on scratch `#3` — succeeded; confirms the single default layer remains `Layer 1`.
23. `layer create` on scratch `#3` — failed with `aseprite_error: function: 0xb0cd78960`. No source or fixture was touched.
24. `draw` grid on scratch `#3`, `Layer 1` — failed with `aseprite_error: function: 0xb0cd70700`.
25. `look preview` on scratch `#3` — read succeeds; displayed a blank 16×16 canvas after failed draw.
26. `sprite_info` on scratch `#3` — confirms `modified:false`, one layer, no edit landed.
27. `draw` filled rect on scratch `#3`, `Layer 1` — failed with `aseprite_error: function: 0xb0cd701c0`.

Current conservative total: 27 / 120; artistic exports: 0 / 3. The required scratch write smoke test has not passed. The editor remains in headless mode and no mode switch was requested or attempted.
28. `sprite_manage close` on explicit scratch `#3` — closed blank, unmodified scratch without force; editor slot released.

Current conservative total: 28 / 120; artistic exports: 0 / 3. First artistic pass is not produced. No candidate was selected.

## Retry after exclusive editor slot was re-granted

29. `preflight({})` — ready; headless remains active; `switched:false`; Aseprite 1.3.18.6-dev, extension 0.8.2; no sprite open.
30. `sprite_manage new` — created owned scratch `#19`, 16×16 RGB.
31. `sprite_info` on explicit `#19` — confirms 16×16 RGB, 1 frame, default `Layer 1`.
32. `layer batch` on explicit `#19` — rename `Layer 1` → `protected-pattern`, then create `editable-layer`; both operations applied successfully.
33. `draw rect` on explicit `#19`, layer `protected-pattern` — filled rect at x=2,y=2,w=3,h=3, palette lock off for RGB smoke; succeeded, reported 21 pixels changed, bounds 3×3. Inspect before interpreting that count.
34. `look preview` on `#19` — successful image delivery; rendered the 3×3 red rectangle at 64×.
35. `look ascii` on `#19`, region (0,0,8,8) — read exact rectangle cells; no mutation.
36. `draw grid` on `#19/protected-pattern` — asymmetric R/G shape plus isolated B, explicit x=1,y=1, 8×8 grid; succeeded.
37. `look preview` on `#19` — successful image delivery; asymmetric red shape, green protrusion, isolated blue mark visible.
38. `look ascii` on `#19`, region (0,0,12,12) — exact rows and legend confirm B at (8,8), green at (3,2), red at (1..2,1..3).
39. `read_pixels` protected layer before edit, 12×12 — four returned colors including transparent; exact grid recorded in tool result.
40. `read_pixels` composite before edit, 12×12 — identical to protected layer.
41. `cel create` on `#19/editable-layer`, frame 1 — succeeded.
42. `draw grid` on `#19/editable-layer` — added only white pixel at (6,6), with `transparent:"skip"`; tool reports 1 changed pixel.
43–44. `read_pixels` composite and `protected-pattern` after edit — independent comparison finds exactly one composite difference, (6,6) transparent→white; protected layer differences: 0.
45. `draw grid` on `#19/editable-layer` — default transparent `.` at (6,6); tool reports one erase.
46–47. `read_pixels` composite and `protected-pattern` — (6,6) is transparent again; pattern pixels unchanged; protected-layer differences: 0.
48. `draw grid` on `#19/editable-layer` — restored one white pixel at (6,6), `transparent:"skip"`; tool reports 1 changed pixel.
49. `draw grid` on `#19/editable-layer` — `.` at (6,6), `transparent:"skip"`; reports 0 changes.
50–51. `read_pixels` composite and `protected-pattern` — white pixel remains at (6,6), protected layer remains unchanged.
52. `sprite_manage save_as` on `#19` — saved `proof/scratch-smoke.aseprite` through MCP.
53. `export png` on `#19`, frame 1 — wrote `proof/scratch-smoke.png` through MCP (16×16).
54. `sprite_manage close` on `#19` — closed saved scratch without force.
55. `sprite_manage open` on own `proof/scratch-smoke.aseprite` — reopened as explicit ID `#78`.
56. `sprite_info` on `#78` — one frame, 16×16 RGB, two named layers with cels, `modified:false`, five palette entries.
57. `look preview` on `#78` — reopened preview matches the same red/green/blue pattern and white pixel.
58–59. `read_pixels` on reopened `protected-pattern` and `editable-layer` — both grids match expected; protected layer has only the authored 3-colour pattern, editable layer only white (6,6).
60. `export png` on `#78` — wrote `proof/scratch-smoke-reopen.png` through MCP.
Local Pillow verification is in `proof/scratch-smoke-verification.json`: both exports have identical PNG SHA-256 `8913f8d305b0ffe557357b78dd75632b193cb736963b61152c0c268217bf0715` and identical RGBA SHA-256 `f16c60a0daf1c7a5d7b51734cb2c6def0e59ed5ee5aadf4400130c7b6206ad2f`; alpha is binary. The only white pixel is (6,6).
61. `sprite_manage save_as` on `#78` — duplicated the reopened smoke document through MCP to `proof/scratch-out-of-mask.aseprite`; original smoke file remains on disk.
62. `draw grid` on `#78/editable-layer` — controlled single white pixel at (15,15), outside the allowed localized edit mask {(6,6)}; succeeded on the duplicate.
63. `sprite_manage save` on `#78` — saved the duplicate-only out-of-mask edit.
64. `sprite_info` on `#78` — duplicate has two visible named layers and `modified:false` after save.
65–66. `read_pixels` composite and editable layer at (12,12,4,4) — white pixel is exactly at local (3,3) = sprite (15,15); no protected layer targeted.
67. `export png` on `#78` — wrote `proof/scratch-out-of-mask.png` through MCP.
68. `sprite_manage open` on own `proof/scratch-smoke.aseprite` — opened preserved original again as `#117` while the duplicate remained separate.
69. `sprite_info` on explicit `#117` — confirms the original smoke file is unmodified, 16×16, one frame, and retains both named layers.
70. `export png` on `#117` — wrote `proof/scratch-smoke-original-reopen.png` through MCP.
Local comparison confirms all three exports (`scratch-smoke.png`, first reopen, original reopen) are byte-identical and RGBA-identical; only one white pixel at (6,6), binary alpha. The duplicate has one extra pixel at (15,15), and `proof/check_out_of_mask.py` rejects it as expected. Scratch reopen, layer-readback and protection checks passed. This setup proof does not count as an artistic pass.
71. `sprite_manage close` on explicit duplicate `#78` — closed saved proof document without force.
72. `sprite_manage close` on explicit original `#117` — closed unmodified proof document without force.

## Owned-baseline review (retry slot)

73. `sprite_manage open` on own copied `input/seed-baseline.aseprite` — opened as explicit `#129`; shared fixture untouched.
74. `sprite_info` on `#129` — confirms 128×192 RGB, one frame, one editable layer `shared-source-seed`, 255 palette entries.
75–76. `look preview` on `#129` at 1× and 4× — full-body placement and silhouette read; unchanged baseline.
77. `look preview` head crop, 8× — face/upper-body inspection.
78. `look ascii` head region — exact pixel positions and palette glyphs.
79–80. `look preview` face crops at 16× and 24× — eye and expression inspection.
81. `look ascii` face crop — exact palette and pixel map.
82–83. `read_pixels` face regions — verified visible eye colors and nearby contours.
84. `read_pixels` far-eye detail — confirmed a pale open-eye sliver plus dark pupil/contour; retained as reference-supported asymmetric open eye.
85–86. `look preview` and `look ascii` lower-face crop — inspected the tiny warm-brown facial mark and mouth area.
87. `look ascii` on `#129`, region `{x:60,y:17,width:20,height:18}` — exact face map; eyes are open; far eye is smaller/partly under fringe; most of lower cheek has no distinct smile arc.
88. `read_pixels` on `#129`, composite region `{x:66,y:25,width:9,height:7}` — recorded existing warm skin, nose/face contours, and exact palette colors; basis for a 3-pixel smile correction limited to the lower cheek.

Current conservative total: 88 / 120; artistic candidate exports: 0 / 3. No source or fixture pixels have been edited. First-pass edit will be made only on a `save_as` copy.

## Pass 1 creation, export mismatch diagnosis, and correction

89. `sprite_manage save_as` on own baseline `#129` — created `pass-01/character-pass-01.aseprite`; the copied baseline remains unchanged.
90. `layer batch` on `#129` — renamed `shared-source-seed` to `character-pixels`.
91. `layer batch` on `#129` — created visible `face-smile` at requested index 1. Later stack review showed this layer was below the opaque character layer.
92. `draw grid` on `#129/face-smile`, frame 1, origin (67,28), rows `[".m.m","..m."]`, `m=#744433`, transparent skip — 3 pixels changed at (68,28), (70,28), (69,29); this first attempt was occluded by the source layer.
93–94. `look preview` on `#129` — face crop 16× and full 1×; the initial output looked like the unchanged seed.
95. `sprite_info` — two visible layers, face-smile active, 128×192 RGB, one frame, 255-color palette.
96. `sprite_manage save` — saved the two-layer first-attempt native file.
97. `export png` — first attempt at `pass-01/character-pass-01.png`. Local hash and pixel comparison showed this output was byte/RGBA-identical to baseline. This mismatch was caught before checkpoint.
98. `sprite_info` — confirms the two-layer file was saved and unmodified after save.
99. `read_pixels` composite region (67,28,4,2) — returned only baseline skin colors; overlay not in composite.
100. `read_pixels` with `layer:"face-smile"` but default composite — repeated the composite result; no conclusion drawn about isolated layer.
101. `read_pixels` with `composite:false, layer:"face-smile"` — confirms exactly the three #744433 overlay pixels.
102. `layer list` — reports stack top-to-bottom as `character-pixels, face-smile`; diagnosis: the new face layer was below the opaque base.
103. `draw grid` on `#129/character-pixels` with the same 3-pixel rows/color — 3 pixels changed in the base cel.
104. `layer delete` on `#129/face-smile` — removed the redundant occluded layer; final source is a single editable `character-pixels` layer.
105. `read_pixels` composite region (67,28,4,2) — now includes #744433 at the planned 3 pixels.
106. `look preview` on `#129`, face crop at 16× — confirms the smile pixels render in the composite.
107. `sprite_info` — final in-memory document is 128×192 RGB, 1 frame, 1 visible editable layer, 255-color palette.
108. `sprite_manage save` — saved corrected pass 1.
109. `export png` — overwrote the candidate PNG with the corrected Aseprite composite; the earlier mismatch is separately documented in `pass-01/attempt-00/`.
110. `look preview` on `#129`, full sprite at 1× — final composition visually inspected after the correction.
111. `sprite_manage close` on explicit candidate `#129` — closed the saved native document; editor slot released.

**Checkpoint count:** 111 / 120 conservative Aseprite/editor service calls (including setup, documentation, scratch proof, failures, and diagnostic reads). One artistic pass has produced an eligible candidate export. The occluded first layer-order output is a failed export attempt, recorded separately; it is not counted as a completed artistic pass. No more Aseprite calls are made while awaiting defect-only review.
