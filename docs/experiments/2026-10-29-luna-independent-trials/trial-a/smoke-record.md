# Dedicated Aseprite smoke record

The supervisor granted the editor slot before this record was run. The selected
backend was the existing Pebbly Aseprite AI Artist headless session.

| Item | Observed result |
| --- | --- |
| Aseprite | 1.3.18.6-dev |
| Extension | 0.8.2 |
| Mode | headless, `switched: false` |
| Preflight | READY; bridge/plugin connected; no sprite open |
| Scratch document | 16x16 RGB, two named layers `protected` and `pattern-base` |
| Pattern delivery | asymmetric red/green/blue blocks plus yellow isolated pixel and white protected pixel visible in `look` preview |
| Exact readback | `look ascii` matched the intended orientation and legend; `read_pixels` returned exact layer matrices |
| Save/reopen | saved to `work/smoke.aseprite`, closed, reopened as a fresh document id, and `sprite_info` retained both layers and the six-color palette |
| Local edit | exactly one `pattern-base` pixel changed from red to blue after reopen; `read_pixels` showed the protected layer unchanged |
| Scope guard | a `selectionOnly` draw outside a 5x5 selection returned `pixelsChanged: 0` |
| Export | `work/smoke.png` and `work/smoke-edited.png` written at 16x16 |
| Technical failure retained | one invalid `op` field and one invalid `pixels` field were rejected before mutation; the corrected calls succeeded |

The smoke used 27 observable Aseprite/editor calls including the initial
preflight and one failed close/save retry. It did not consume an artifact pass.
