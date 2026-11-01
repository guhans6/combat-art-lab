# Full-character transparent-source conversion comparison

## Question

Does a generated clean transparent cutout produce a different 128×192 source-derived
seed than the earlier extracted cutout when every conversion setting is held fixed?

## Inputs

- Rough supporting cutout: `assets/references/approved-2026-10-26/character-cutout.png`
  (`4dd54a80…280b8`). It contains partial-alpha edge contamination in its original
  extraction.
- Generated candidate: `../inputs/clean-generated-cutout-v1.png`
  (`12e971cc…f49e`). It was visually reviewed on white, checkerboard, and dark-gray
  mattes as a clean transparent cutout. It is still a generated candidate, not a
  replacement authority for the approved scene/close-up.
- Current standing context: `assets/export/standing-alpha-v03/frame-0.png`
  (`0ebd67bc…857f5`). Its pose, grid, construction and animation role differ from
  this source-conversion test and it is not a matched control.

## Frozen recipe

Both full-character sources are exactly 1024×1536 and kept at that registration.
Each is reduced to 128×192 using BOX sampling, no dithering, and a common 48-colour
palette extracted from near-opaque (`alpha >= 250`) interior pixels of the rough
source. Alpha is BOX-resampled and retained rather than thresholded, so these are
conversion seeds, not clean game-ready alpha exports.

The generated source changes visible face/hair/shading detail slightly despite
retaining the broad pose, costume and tote. Those source differences remain visible
in the generated seed. They must not be credited to the conversion method.

## Result

[The comparison sheet](fullbody-source-conversion-comparison.png) shows source images
on white and their matched seeds at 3× nearest-neighbour, with the current standing
frame separately labeled. The generated seed has a cleaner outer edge because its
source is cleaner, but it also carries generated reinterpretation of identity-bearing
details. The test therefore demonstrates a source-quality tradeoff, not that the
generated cutout is better art or a production replacement.

`verify_conversion.py` is read-only and confirms the frozen input hashes, identity
registration, conversion recipe and seed dimensions. No native Aseprite source,
semantic separation, local cleanup, motion test, Godot playback, user approval,
commit or publication was performed in this comparison.
