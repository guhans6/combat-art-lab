# Final independent technical verification — material03

Verifier: `proof/verify_final.py` using the repository's read-only Aseprite
decoder. Machine record: [`../proof/final-verification.json`](../proof/final-verification.json).
Selected native sources: `source/tote-clean-material03.aseprite` and
`source/tote-smear-material03.aseprite`. The generic `source/tote-*.aseprite`
files are retained pre-correction candidates. The complete previous package is
preserved in [`final_before-material03`](final_before-material03/). This is a
still/image and file-properties audit only; it does not claim motion viewing,
gameplay validation, artistic approval, or publication.

## Passed evidence

- Both selected material03 sources decode as 19 frames,
  256x208, eight visible normal opaque layers, with the declared timing sequence
  and total **2230 ms**.
- Every decoded native composite equals its individual PNG and its horizontal-sheet
  crop (19/19 for each variant). Both fresh dedicated-MCP material03 reopen sheets also match
  all 19 decoded native composites and their metadata timings.
- Alpha is binary in every native composite. Used non-transparent colours are a
  subset of `inputs/original-neutral.png`'s used colours; no added used colours.
  F1 and F19 exactly equal the original-neutral composited at `(60,8)`.
- Clean versus smear differs only in F9 and only in `01-rear-handle` (91 pixels),
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
- Material03 owner/hide evidence for F4/F5/F6/F8/F9/F14/F15/F16 is copied into
  `final_material03-owners-F*.png` only after exact selected-source hash binding to
  the independently reviewed material03 candidate.

## Alpha-hole screen

Enclosed transparent components were enumerated for every frame in the JSON record.
The nontrivial F9 changes are in the intended tote/handle region: clean largest
component `(143,80)..(152,100)` (112 px), versus smear `(143,80)..(157,105)`
(180 px), plus smear `(162,91)..(167,93)` (11 px). No confident unintended
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

## Exact-palette paired GIFs

The paired F9 composition has 213 colours. The final GIFs use existing palette
colours for the matte/labels and bitmap (non-antialiased) text; decoding each GIF
matches all 19 rendered matted A/B frames at its stated scale. No continuous motion
was viewed by this verifier.

Artifact hashes, input hashes, full per-frame hole coordinates, and all booleans are
in the machine record. Fresh source reopen/local-revision evidence was performed by
the main agent and independently checked here. The completed Godot boundary is
recorded separately in [`../proof/runtime-material03-checks.json`](../proof/runtime-material03-checks.json): zero errors/warnings, three automated A/B loops,
a C probe with 78 contact pixels, and zero RGB mismatches across 38 panels. This
verifier did not perceive continuous motion; user visual approval, production
integration, and publication remain separate.
