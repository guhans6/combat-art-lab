# Observed validation
Date: 27 October 2026. Environment: Python 3.13.5, Pillow 12.3.0.

| Check | Observed result |
|---|---|
| Offline helper unit tests | 24/24 passed; see `unit_tests.txt`. |
| Real input inspection | Actual supplied concept and sprite inspected; hashes/dimensions/alpha/color counts in `input_inventory.json`. |
| Real conversion command | Three crop seeds generated using the documented CLI; parameters and outputs recorded. |
| Historical pixel reproduction | 56×42, 84×63 and 112×84 decoded RGBA bytes each match the corresponding earlier seed; see `seed_comparison.json`. |
| Real normalization command | Existing sprite placed in two equal-sized frames, with the second retaining its declared (6,-8) offset. This is a translation-only technical smoke test. |
| Source preservation | Three original uploads remain byte-identical in the package. |
| Historical archive preservation | Every expanded member of the previous conversion archive is byte-identical. |
| Script syntax | All packaged Python files compiled successfully. |

Tests cover source preservation, dimensions, aspect-ratio rejection, masks, transparent filtering, optional binary alpha, palette bounds, existing-output refusal, shared-scale behavior, explicit anchors/offsets, clipping, empty/opaque frames, unsafe names and invalid timing/scale.

Remaining packaging checks (JSON/image integrity and internal relative links) are recorded in `package_checks.json`. `manifest.json` at package root inventories packaged bytes, excluding itself. Use `scripts/verify_manifest.py` after extraction.

## Not tested or claimed
No new image-generator output, traced/native-cleaned character, PixelOE/SAM/ControlNet execution, Aseprite integration run, semantic layer authoring, novel pose sequence, animation quality, Godot playback, user artistic acceptance or production speedup. The newest Aseprite outcomes described in the handoff are repository records, not reruns performed here. No remote workspace file was modified.
