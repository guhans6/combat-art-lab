# Luna 6 mouth-only correction

- Status: rejected by user on visual expression; no mouth candidate selected.
- Date: 30 October 2026.
- Question: can a tiny, bounded native edit restore the approved reference's quiet closed smile to the Luna 6 cleanup without changing the eyes or other content?
- Baseline: `inputs/luna6-fullbody-cleanup-baseline.aseprite` and `.png`, copied from the parent Luna 6 cleanup; hashes are recorded in `passes/operations.json`.
- Scope: mouth only, one initial pass plus at most one correction if the parent flags expression failure. That condition occurred; the single correction is complete and no further artistic pass is authorized.
- Authorities: the approved close-up and scene in `inputs/`; the Luna 6 candidate is the comparison baseline. The original references were opened directly; crop and resampling details are recorded in `observations.md`.
- Native tool: dedicated Aseprite AI Artist MCP, headless; Aseprite 1.3.18.6-dev, extension 0.8.2. Python/Pillow 3.14/12.3 was used only for deterministic crop/review preparation and pixel checks.

## Artifacts

- Frozen first candidate (parent rejected expression placement): `passes/luna6-mouth-correction.aseprite` and `passes/luna6-mouth-correction.png`.
- Final native candidate: `passes/luna6-mouth-correction-final.aseprite`, SHA-256 `2d2cd512b82396276dbe4b96e69234bf7044e12bff181dc2a4adcaf575b3d09a`.
- Final PNG: `passes/luna6-mouth-correction-final.png`, SHA-256 `ffbda8af18b9e6c59f949876f520a577f66d9918ed82e3d3279eec100bcbc761`.
- Fresh reopen export: `proof/luna6-mouth-correction-final-reopen.png`; byte-identical to the final PNG.
- Frozen first mask and correction mask: `mouth-mask.json`, `correction-mask.json`; the second mask was recorded before the authorized correction.
- Exact native operations: `passes/operations.json`.
- Technical evidence: `proof/png-checks.json`, `proof/native-layer-checks.json`.
- Inspected matched comparisons: `reviews/reference-baseline-final-head-1x.png`, `reviews/reference-baseline-final-head-8x.png`, `reviews/reference-baseline-final-fullbody-1x.png`, and `reviews/reference-baseline-final-fullbody-8x.png`.

## Outcome and evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Expression | First location rejected by parent as far-edge lip/pout. After the single correction, parent reports a closed slight smile and accepts it for user review. User likeness approval remains pending. | Three-panel head comparisons at 1×/8× |
| Scope | Final PNG differs from baseline at 3 pixels, all within `[65,28,71,30)`. Eyes, face outline and body are unchanged. | `proof/png-checks.json` |
| Alpha/visible coverage | 0 alpha changes; 7,844 visible pixels before and after. | `proof/png-checks.json` |
| Native structure | 128×192 RGB, one frame, 12 layers, 11 visible plus the hidden locked guide; palette and all layer metadata match the baseline exactly. Only the owning hair layer changes, at the three mouth pixels. | `proof/native-layer-checks.json` |
| Palette | Existing 255-entry palette is byte-for-byte identical; the mouth color `#744c40` is already in the palette and palette lock reported no color snaps. | `proof/native-layer-checks.json`, `passes/operations.json` |
| Reopen/export | Saved native reopened in the MCP and exported to PNG; fresh export is byte-identical to the saved final PNG. | `proof/luna6-mouth-correction-final-reopen.png`, `proof/png-checks.json` |
| Aseprite validate | Not run: no `validate` function was exposed in the connected MCP tool inventory, although preflight listed it among backend features. | Tool inventory at run time |
| Full-body/gaming evidence | Full-body comparison inspected; no change outside the mouth. Gameplay scale, Godot playback and animation were out of scope. | `reviews/` |

## Automation boundary and selection

Reference crop, seed and palette preparation were scripted; agents selected semantic masks and bulk-filled the earlier candidate. This mouth correction was visually directed by the agent and applied through native Aseprite MCP pixel batches. Hashes, pixel diffs and comparison sheets were automated. Visual expression judgment came from the parent/model and remains subject to user review. The imported/converted seed plus local refinements do not amount to a full redraw.

- Last attempted and best eligible artifact: `passes/luna6-mouth-correction-final.aseprite` / `.png`, accepted by parent for user review only.
- Rejected prior expression placement is preserved in `passes/luna6-mouth-correction.aseprite` / `.png`.
- Selected/user-approved: none yet; the user must judge the exact final candidate.
- Remaining work: parent presents the final candidate and comparison sheets for user visual review. No additional art pass is authorized in this follow-up.

## User rejection and supervisor correction

The user rejected the final mark as a stray-looking pixel near the mouth. Supervisor re-opened the actual comparison and agrees: the added mark does not convincingly convey the restrained original smile. The earlier supervisor slight-smile assessment was incorrect. Technical checks still establish edit scope, not artistic success. Both mouth attempts are rejected; best retained baseline is the unchanged pre-mouth Luna6 full-body cleanup. Preserve all attempted artifacts as evidence; no new art pass performed.
