# Pass 01 record

## Artifacts

- Native source: `passes/pass-01.aseprite`
  - SHA-256: `d7ddf39445e9d756254775ccafc865de3b695a0b7247578984d6c4395477dadd`
- Transparent runtime export: `passes/pass-01.png`
  - SHA-256: `bc7190d2c823539a4499c79ad4f63810fd8a3d1ade098eef624e1d726ea05af4`
- Review sheet, source versus candidate on white at 4x:
  `passes/pass-01-review-source-vs-candidate-white-4x.png`
- Review sheet, source versus candidate on magenta at 4x:
  `passes/pass-01-review-source-vs-candidate-magenta-4x.png`
- Corrected evidence set with explicit RGBA inputs and alpha masks:
  `passes/pass-01-review-v2-manifest.md` and the `passes/pass-01-review-v2-*`
  files. These were regenerated from the exact pass-01 PNG without changing it.
- Candidate native/zoom views and source preview are retained beside the review
  sheets with the `pass-01-review-*` prefix.

## Construction

The candidate started from the 1024x1536 production source reduced 8:1 with
nearest-neighbour sampling. Alpha values at or below 16 were removed, leaving a
reviewed opaque silhouette on transparency. The seed was imported into Aseprite,
snapped to its source-derived palette (254 visible colors), and retained as
`converted-seed`. A locked, hidden `reference` layer preserves the source guide.

Native structure includes clipped converted raster regions for `hair-face-raster`,
`jacket-shirt-raster`, `jeans-raster`, and `tote-shoes-raster`, plus authored
semantic overlay layers (`hair-face`, `jacket-shirt`, `jeans`, `tote-shoes`,
`silhouette-coverage`, and `cleanup-accents`). The authored face overlay brightens
the near/far eye whites and replaces an initially overlarge smile test with a
three-pixel restrained warm smile. The overlarge four-pixel test was erased in the
same pass and was not exported as a candidate.

## Technical observations

- Aseprite source reports 128x192 RGB, one frame, 12 layers, 255 palette entries,
  and a hidden non-editable reference layer.
- Export reports 128x192 RGBA, full canvas retained, no trim, one frame.
- The local review export is nearest-neighbour 4x diagnostic only; the runtime
  candidate remains 128x192.
- The v2 comparison includes explicit color and alpha diagnostics, but supervisor
  review found that its magenta and white presentations still appear to omit
  materially different character/source regions. Do not claim that contrasting
  composites prove full coverage; the discrepancy remains unresolved.
- No animation, Godot playback, installation, publication, or user approval is
  claimed by this pass.
- A Pillow-based pixel checker was unavailable in this environment; editor-native
  structure/preview/readback plus `file`/`ffprobe` checks are the observed boundary.

## Appearance observations at 1x and matched 4x

- Identity: recognizable as the supplied woman; tied brown hair, olive jacket,
  cream tote, wide blue jeans, and pale shoes survive the reduction.
- Expression: rightward three-quarter face and rightward gaze read; the small warm
  smile is visible in the 4x head review but remains a native-size risk.
- Proportions/pose: tall long-leg stance, hands-in-pockets pose, jacket opening,
  tote attachment, and outward-angled leg remain coherent.
- Pixel craft: broad source clusters survive and the 128 grid reads crisply at 4x;
  fine hair/eye texture is necessarily compressed and can still be simplified.
- Transparency: contrasting backgrounds show clean outer coverage, intentional hair
  and leg openings, and no enclosed garment holes observed in this static frame.

These are agent observations only. Supervisor/user visual review remains pending.
The supervisor later flagged ambiguity in the first comparison presentation and
expression/craft defects; pass 02 is planned in `pass-02-plan.md`.

## Pass boundary

Pass 01 is retained as the initial artifact. No correction pass has started. The
editor slot is released now so the supervisor can provide defect-only feedback;
any next pass will be selected and authored independently from that observation.
