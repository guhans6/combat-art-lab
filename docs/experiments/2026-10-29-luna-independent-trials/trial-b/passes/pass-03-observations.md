# Pass 03 observations

## Artifact and requested profile

- Requested configuration: `gpt-6-luna`, maximum effort; host: this Codex Desktop task. Provider compute and cost telemetry were not exposed.
- Native candidate: `pass-03.aseprite`, created in Aseprite document `#211`, 128×192 RGB, one frame; SHA-256 `3bacdd36befa22226383488c548ecf8293708ac7af0734758ededaa17e3cf2ba`.
- PNG export: `pass-03.png`; SHA-256 `f0b5e2831e8a263da134356cf38957f5f08ae756d4d2d2ebd98d125361049df0`.
- Review artifacts: `pass-03-review-sheet.png`, `pass-03-head-review.png`, `pass-03-part-isolation.png`, `pass-03-alpha-holes.png`, and `pass-03-source-hole-grid.png`.
- Earlier pass 01 and pass 02 native sources, exports, observations, and review sheets are retained.

## Art and native structure

Pass 03 keeps the full 128×192 framing, pose, outfit, silhouette and source-derived colors. It revises the small face area with asymmetric lids and right-set pupils, plus a connected, shallow smile above the jaw edge. Review sheets show the full approved reference figure, seed and candidate at native size and 4× nearest-neighbor display; labels fit the panels.

The native file has nine visible editable layers: `Hair`, `Tote and strap`, `Shirt`, `Jacket`, `Jeans`, `Shoes`, `Face, neck, hands`, `Contour details`, and `Facial features`. The recipe in `scripts/prepare_pass03_layers.py` partitions each visible seed pixel once, verifies exact recomposition, then replaces only the documented eye and mouth boxes. `prep/semantic-pass03/draw-grids.json` contains the exact nine grid inputs used to construct Aseprite document `#211`; `pass-03-part-isolation.png` shows the parts individually. Ownership checks report zero olive pixels assigned to the tote, zero denim pixels assigned to jacket or contour, and zero pale-fabric pixels assigned to jeans.

## Technical checks

- Export properties: 128×192, binary alpha, visible bounds `(32, 3, 104, 185)`, 7,834 visible pixels, 35 colors.
- `scripts/verify_export.py` reports an exact match between `pass-03.png` and the local semantic composite, zero alpha changes, and no changed pixels outside the eye and mouth boxes. It records 33 visible color changes from the trial's seed.
- Aseprite reports nine named editable layers and a 35-color palette. Palette analysis finds zero off-palette colors; the source-derived palette still contains 11 near-duplicate pairs.
- Fresh native reopen proof: after saving `pass-03.aseprite`, I closed only document `#211`, reopened that path as `#302`, inspected its 128×192/9-layer/35-color structure, and exported `pass-03-reopened.png`. Its SHA-256 equals the candidate PNG, and canonical RGBA comparison found zero differing pixels.
- Duplicate-local-edit proof: reopened document `#302` was saved separately as `pass-03-local-edit-proof.aseprite` (SHA-256 `8a113219d224ff926aa35d020606d903b6113f11c2863b1fe4f6b3fadf305b29`). A one-pixel warmth adjustment on the `Facial features` layer changed `(68, 28)` from `#aa8378` to `#bf998a`. `scripts/verify_change_mask.py` accepted the proof PNG with exactly that one pixel changed and nothing outside the allowed mask. The original candidate native file and PNG remain unchanged. `scratch-smoke.md` records the checker rejecting a deliberately out-of-mask edit at `(8, 10)`.
- The raw alpha-warning coordinates remain the same 26 as pass 01 and pass 02; the pass-03 alpha is identical to pass 02. Source-block inspection found 0–31 of 64 source samples at alpha ≥32 per warned cell. The retained overlay and source grid place them in hair/face edge openings and the gap between the legs. The warnings remain raw-check failures; this evidence supports unchanged source-derived coverage and does not by itself prove every opening is desirable.
- By-eye review used the Aseprite 4× full-sprite preview and head crop, then inspected the exported matched comparison sheets. No Godot or engine playback was performed.

## Call accounting and limits

Pass 03 used 30 Aseprite/editor MCP calls, including preflight, document creation/inspection, palette and layer setup, nine layer draws, preview and ASCII review, save/export, fresh reopen/export, and duplicate edit/save/export. Pass 03 had no failed calls. The earlier 35-call smoke block, documented in `scratch-smoke.md` and included within pass 01's 58-call accounting, included two failed attempts. Cumulative use is 110 of 120 calls over all three artifact passes. No fourth artistic pass is available within the agreed brief.

## Final supervisor review

The supervisor confirmed the semantic isolation and full-reference framing improvements, and that the smile is visible. The eyes still read more angular or closed than the source. The reopen equality was independently confirmed. No further art round is available after the third pass.

The candidate has not received user visual approval and is not validated in Godot. The 26 raw alpha warnings remain, even though they are unchanged and source-cell reviewed. Runtime behavior, installation and publication were not tested or performed.
