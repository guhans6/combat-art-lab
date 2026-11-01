# Luna pass03 procedure and outcome

Date: 2026-10-30

## Provenance

The work stayed in the headless Aseprite MCP editor. Pass03 was saved as a new native file from the open pass02 working document. For the four deformed clothing layers, the source pixels were read from `inputs/current-idle-source.aseprite`, which is the copied current idle source. Pass01 and pass02 files remain separate and unchanged.

## Operation

Frames 2, 3, and 4 were rebuilt from the copied current idle source for layers `02a-jacket-left`, `02b-jacket-right`, `03-shirt`, and `05-tote-strap`. Each source row was resampled around canvas x=64 with nearest-neighbor sampling. The horizontal scale factors were 1.08 for frame 2, 1.14 for frame 3, and 1.04 for frame 4. The scale tapered smoothly to 1.0 above y=41 and below y=65, with a full-weight band at y=46–56. The same mapping was applied to each listed layer so existing colors, folds, overlap, and surface texture moved together. Frames 1 and 5–8 and the other layers were not edited.

No palette colors were added. The 8-frame timing and `idle` tag were retained.

## Verification

`render_pass03_review.py` recreates the 1×/3× review GIFs, contact sheets, and per-frame pixel/alpha metrics from the native Aseprite exports. The saved source was closed and freshly reopened through Aseprite MCP; a second native frame export matched the first export byte-for-byte for all eight PNGs. The head/face and hair layer crops match the current idle source in all eight frames. Composite pixels below y=76 match the current idle source; pass03 gained opaque pixels in the breathing region and lost none.

## Review result

Sol rejected pass03 as an experiment: although the pale patch was removed and the 1× motion became clearer, the horizontal expansion reads as an accordion stretch. It creates abrupt shoulder proportions where the expansion tapers above the fixed elbows and waist. This is the final authorized attempt and is not approved for production use.
