# Final independent technical verification

Verifier: `proof/verify_final.py` using the repository's read-only Aseprite
decoder. Machine record: [`../proof/final-verification.json`](../proof/final-verification.json).
This is a still/image and file-properties audit only; it does not claim motion
viewing, gameplay validation, artistic approval, or publication.

## Passed evidence

- Both `tote-clean.aseprite` and `tote-smear.aseprite` decode as 19 frames,
  256x208, eight visible normal opaque layers, with the declared timing sequence
  and total **2230 ms**.
- Every decoded native composite equals its individual PNG and its horizontal-sheet
  crop (19/19 for each variant). Both fresh dedicated-MCP reopen sheets also match
  all 19 decoded native composites and their metadata timings.
- Alpha is binary in every native composite. Used non-transparent colours are a
  subset of `inputs/original-neutral.png`'s used colours; no added used colours.
  F1 and F19 exactly equal the original-neutral composited at `(60,8)`.
- Clean versus smear differs only in F9 and only in `01-rear-handle` (52 pixels),
  `04-tote-body-rim` (1,637), and `05-near-handles-seams` (264). Head, jacket/body,
  legs/shoes, shirt/neck, and hands/forearms are exact at F9; all other frames and
  layers are exact.
- Existing dedicated-MCP clean/smear GIFs at 1x and 3x each contain 19 frames,
  carry the declared timing, and decode pixel-exactly to their native frames at
  their stated scale.
- The duplicate-only local revision passes: its only delta is F10,
  `04-tote-body-rim`, pixel `(205,93)`, `#FCD8B6` to `#DFB39B`. Canvas, duration,
  layers, non-cel chunks/palette data, and every other cel are exact. Fresh MCP
  reopen PNG equals the read-only revised F10 composite.

## Alpha-hole screen

Enclosed transparent components were enumerated for every frame in the JSON record.
The nontrivial F9 changes are in the intended tote/handle region: clean largest
component `(144,82)..(152,100)` (100 px), versus smear `(144,82)..(157,105)`
(150 px), plus smear `(162,91)..(167,93)` (11 px). No confident unintended
body/denim hole was found. Handle windows, limb gaps, and small face/hair negative
spaces were not blanket-filled.

## Review artifacts

- [`final_clean-v-smear-1x.gif`](final_clean-v-smear-1x.gif) and
  [`final_clean-v-smear-3x.gif`](final_clean-v-smear-3x.gif): labeled A/B,
  matched authored timeline.
- [`final_all-frames.png`](final_all-frames.png): 19-frame smear filmstrip, 2x.
- [`final_smear-neighbors.png`](final_smear-neighbors.png): clean/smear F8–F10
  controls at 3x.
- [`final_pose-comparison.png`](final_pose-comparison.png): source `.18x`, raw
  conversion `.18x`, and final native F1/F2/F3/F7/F10/F12 full-canvas panels.

## Technical gap

The paired A/B F9 composition has 261 colours including its matte/labels, exceeding
GIF's 256-colour index limit. Therefore the two `final_clean-v-smear` GIFs use a
deterministic no-dither 256-colour reduction for that delivery frame and are **not
exact-palette proofs**. The original per-variant MCP GIFs above are pixel-exact.
No continuous motion was viewed by this verifier.

Artifact hashes, input hashes, full per-frame hole coordinates, and all booleans are
in the machine record. Fresh source reopen/local-revision evidence has been checked;
Godot execution and user visual selection remain separate owner/evidence boundaries.
