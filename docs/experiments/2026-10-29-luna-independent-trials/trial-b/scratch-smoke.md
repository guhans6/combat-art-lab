# Trial B backend smoke

## Runtime

- Backend: dedicated Aseprite AI Artist MCP, Pebbly extension 0.8.2.
- Mode: headless; no mode switch requested or performed.
- Aseprite: 1.3.18.6-dev.
- Preflight: ready, no sprite open. The only documents used were created by this trial: `#3`, its saved/reopened copy `#42`, and the out-of-mask duplicate `#62`. No preexisting document was opened, edited, or closed.
- Total Aseprite/editor MCP calls through this smoke: 35, including failed attempts. No calls to other art services or code MCP.

## Evidence

- Created a new 16x16 RGB sprite, renamed its two layers `Smoke Pattern` and `Protected Swatch`, and drew an asymmetric three-color mark with a separate teal pixel. The `look` preview delivered the image; `look ascii` and structured `read_pixels` exposed exact coordinates/colors.
- On `Smoke Pattern`, changed `(5,4)` from `#ffd166` to `#118ab2`. Before/after structured pixel reads found exactly one composite pixel changed and zero changes on `Protected Swatch`.
- Tested grid transparency: `transparent: "skip"` left an existing `#ff5a5f` pixel intact (0 pixels changed); the default transparent cell erased that exact pixel (1 pixel changed, then fully transparent).
- Saved `scratch/asset-pipeline-smoke.aseprite`, reopened it as `#42`, and exported both before and after. `scratch/smoke-before-reopen.png` and `scratch/smoke-after-reopen.png` are 16x16 and decoded-RGBA-identical. Reopened metadata reports two named layers and a 5-color palette; alpha values are only 0 and 255.
- Opened a duplicate as `#62`, changed protected swatch pixel `(8,10)` to green, and exported `scratch/smoke-out-of-mask.png`. `scripts/verify_change_mask.py` compared it to the known baseline while allowing only `(5,4)` and rejected the out-of-mask change at `(8,10)` with exit status 2. The rejected duplicate is preserved as `scratch/out-of-mask-violation.aseprite`.
- The erase/skip variant is preserved as `scratch/erase-skip-state.aseprite`. The canonical smoke source remains `scratch/asset-pipeline-smoke.aseprite`.

## Call accounting and failed attempts

The first drawing call used `op` where the backend schema requires `kind`; validation rejected it before changing pixels. The corrected `kind: "grid"` call succeeded. Closing reopened document `#42` initially failed because the backend marked it modified; it was saved, then closed successfully. Both failures are included in the 35-call count. All three trial-created documents were closed after saving their needed states.

## Capability boundary

This proves local headless MCP image delivery, exact pixel reads, grid editing, transparent skip/erase behavior, a protected layer check, save/reopen/export equality, and a simple out-of-mask checker rejection for this agent/session. It does not prove art quality or user visual approval.
