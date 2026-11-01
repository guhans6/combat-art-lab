# Pass 01 review evidence v2

The original review images are retained. The v2 helper was run from the exact
pass-01 export and the frozen production input:

```sh
scripts/make_review_sheet_v2.sh \
  passes/pass-01.png \
  passes/pass-01-review-v2
```

It emits separate 512x768 RGBA source/candidate previews, identical white and
magenta composites, and side-by-side grayscale alpha masks. `file` and `ffprobe`
confirm the candidate preview source is a 128x192 RGBA PNG before the diagnostic
4x scale. The measured candidate alpha bbox is x32..103/y2..184 (72x183), and
the source alpha bbox is x254..830/y20..1481 (577x1462) before its diagnostic
downscale. However, supervisor review found that the magenta and white comparison
presentations still appear to omit materially different character/source regions.
This discrepancy is unresolved; the sheets are retained as diagnostics only and
must not be used to claim full coverage or visual equivalence.

The candidate export itself remains:

- `passes/pass-01.png`
- SHA-256 `bc7190d2c823539a4499c79ad4f63810fd8a3d1ade098eef624e1d726ea05af4`
- 128x192, RGBA, full canvas, no trim

The new v2 sheets are a retained diagnostic attempt, not a corrected proof; no new
artifact pass was consumed. A future review should rebuild the comparison with an
independently checked flattening/framing path before making a coverage claim.
