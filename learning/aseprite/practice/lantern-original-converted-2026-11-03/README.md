# Original lantern image — deterministic conversion

Requested 3 November 2026: convert the original image through the existing automation,
with no AI redraw or cleanup, to the current native output size.

- **converted.png**: 88 × 152 transparent canvas; character bounds [6,4,79,148),
  exactly144px high,73px wide. Ground at y148, matching current native placement.
- **preview-3x.png**: integer nearest-neighbor display enlargement only.
- **converted.aseprite**: exact flat converted pixels on Converted original, plus
  blank Corrections layer. This is not a semantic-layer reconstruction.

Pixel generation uses the unchanged `../../automation/convert_image.py` and
`../../automation/lantern-144.json`. No model, image generator, network service,
hand-drawn patch, palette quantization, dithering or anatomy correction is involved.
The original1024 × 1536 source uses its own alpha threshold160, giving bounds
[107,57,852,1518). No custom mask or component deletion was used. That crop is
sampled with nearest-neighbor to73 × 144 and placed at(6,4) on88 × 152.
The2120visible RGB values are sampled from the source; they are not constrained
to the earlier redraw's21color palette. Minor sampled source texture remains.

Script command after [new-machine setup](../../../../docs/new-machine.md), from
repository root (output must be a new directory; Windows uses `.venv/Scripts/python.exe`):

```sh
.venv/bin/python \
  learning/aseprite/automation/convert_image.py \
  --recipe learning/aseprite/automation/lantern-144.json \
  --out /private/tmp/lantern-original-rerun
```

`report.json` records input/recipe/converter digests and dimensions.
`verification.json` passes an independent every-pixel source-sample mapping,
exact native dimensions/binary alpha/144px visible height, identical rerun PNG
bytes, and exact native export after fresh Aseprite reopen. Source and converter
hashes are unchanged. Native assembly used dedicated Aseprite MCP only: rename
paint layer/add blank Corrections/save. An optional duplicate-layer batch failed
and rolled back; the final two-layer assembly and pixel equality were verified.
No pixel drawing operations were used. Final native SHA256:
f3adaa12e813e4e4791e5f14f3263b69c719aafd54615c727943a26c3724a44f.

Original references, hand-authored sprite and current practice board remain
unchanged. User next opens this conversion if preferred; no artistic approval,
animation/Godot test, practice-board replacement, commit or publication is implied.
