# Trial B preparation

## Frozen task

- Requested model/effort: `gpt-6-luna` / `max`; host: this Codex Desktop task.
- Method: source-assisted reconstruction, using only the common brief's production cutout and approved scene/close-up references. No generation, other model, subagent, or prior converted asset was used.
- Target: one static 128x192 transparent sprite; full source framing; no background; same pose and outfit.
- Budget: three artifact passes total and at most 120 Aseprite/editor calls. Pass 01 used 58 calls, pass 02 used 22, and pass 03 used 30, for 110 total. Native runtime/Godot work is out of scope.

## Inspected inputs and visual observations

All three allowed image files were opened visually before drawing and copied without modification into `input/`. Hashes, dimensions, alpha coverage, and the white/dark/checkerboard source review are in `intake/input-observations.json` and `intake/source-alpha-mattes.png`.

- Production source: `input/source-cutout.png`, 1024x1536 RGBA. It already has pixel-cluster rendering and the same 2:3 canvas ratio as the target. The figure reads from x=255..830 and y=20..1482 where source alpha is at least 32. Source alpha spans 0..254 and has no fully opaque pixels; very faint material extends beyond the main silhouette. White, dark and checkerboard views show the character itself is intact. Do not use source alpha values as final sprite translucency.
- Approved identity/style anchors: `input/character-scene.png` and `input/character-closeup.png`, both 1448x1086. The scene confirms the relaxed three-quarter standing pose, rightward face turn, tied brown hair and broken fringe, olive open jacket, cream shirt and tote, wide blue jeans and pale shoes. The close-up confirms unequal near/far eye footprints and a shallow, slightly uneven smile. Warm storefront lighting and cool street depth belong to the scene; keep the standalone sprite's material colors without importing that background.
- Target framing: preserve the full production-source canvas with no crop or translation. Its source figure footprint maps to approximately x=32..104 and y=3..185 on the 128x192 target. The prepared seed yields `(32, 3, 104, 185)` and 7,834 visible pixels.

## Preparation recipe

`scripts/prepare_seed.py` checks all frozen input hashes, copies the originals, and recreates `prep/seed-128x192.png`.

1. Threshold the production source alpha at 32 to remove only the faintest cutout fringe.
2. Preserve the full 1024x1536 framing and reduce exactly 8:1 using BOX resampling in premultiplied-alpha space.
3. Turn downsampled area coverage into binary alpha at 128 (half coverage). The seed has only alpha values 0/255.
4. Build an image-adaptive 40-color median-cut palette from visible seed pixels only; use no dithering. The seed currently uses 35 visible colors.
5. Save the native-size seed and a nearest-neighbor 4x view.

The 40-color cap and alpha thresholds are this trial's technical starting choices, not project-wide art-direction decisions. The native palette is small because the target is a 128x192 pixel sprite; no texture dither is added.

## Seed review and initial pass-01 hypothesis

`prep/seed-approved-scene-review.png` and its JSON sidecar compare the prepared seed's visible full-body crop with an approved scene crop at matched height and nearest-neighbor 4x. `prep/seed-approved-head-review.png` and its sidecar compare the seed head with the approved close-up. The candidate retains the overall figure proportions, rightward pose, broad costume blocks, tote, and grounded stance. At 1x the face is too quiet: near/far eyes merge into weak dark marks and the restrained smile is lost. Hair contour and fringe are also softened by the 8:1 area reduction. This is a seed observation, not acceptance of an exported candidate.

The initial pass-01 hypothesis kept the source-derived large planes and silhouette, then added a small number of pixels for eye marks and a mouth. Parent review found that the near/far distinction and restrained smile remained weak; see the retained pass notes and the second-pass result.

## Tool boundary

The local preparation and verification scripts use the bundled Python/Pillow runtime. Aseprite AI Artist MCP preflight reported headless Aseprite 1.3.18.6-dev and extension 0.8.2; no mode switch was made. Pass 01 is native document `#81`; pass 02 is native document `#129`; pass 03 was built as `#211`, closed after save, and reopened from disk as `#302`. All documents were created by this trial. The pass-03 reopen/export is pixel-identical to its saved PNG. A duplicate-local-edit proof is saved separately. No install, config edit, commit, publication, or Godot preview was performed.
