# Offline tools and their limits

Python 3.10+ and Pillow are required. The kit was tested with the version in `requirements.txt`; an existing compatible environment may suffice. These programs make no network calls and do not install dependencies, generate artwork, or modify Aseprite/workspace files.

## Inspect
```sh
python scripts/reference_lab.py inspect references/approved_concept_upload.png references/supplied_sprite.png
```
Reports file hashes, dimensions, alpha bounds, visible RGB colors and alpha counts. These are file properties, not scores for art or identity. Stored-image coordinates are used; EXIF orientation and color-profile conversion are not applied.

## Seed conversion
```sh
python scripts/reference_lab.py seeds references/approved_concept_upload.png \
  --crop 380 100 800 415 --sizes 56x42 84x63 112x84 \
  --method BOX --colors 32 --out /tmp/new-seed-study
```

Crops use zero-based, half-open `[left, top, right, bottom]` coordinates. All target sizes must have the crop's exact aspect ratio, so the tool cannot silently stretch a head. Crop or pad explicitly when necessary. The default filter is BOX, not a claim that it is optimal; compare NEAREST/LANCZOS as needed.

`--colors N` derives one palette from visible crop pixels and reuses it across sizes, without dithering. It is optional. It is not an established material palette; review it before using it in animation. Partial-alpha RGB participates in palette sampling without perceptual weighting.

`--mask path.png` expects a full-source-sized grayscale coverage mask: white keeps pixels, black removes them. It uses grayscale values, **not the mask file's alpha channel**, and multiplies the original image alpha. It does not create the mask or remove a background automatically. Review mask edges/hair/straps before use.

Filtered RGBA reduction uses premultiplied alpha. `--alpha-threshold 128` is an optional example that forces binary alpha after reduction. It can remove thin details; it is not the default. Without it, coverage alpha is preserved. Hidden RGB at fully transparent pixels is not an identity constraint.

Outputs: the masked crop, native-size seed PNGs and `processing.json` containing provenance, parameters and stats. A converted seed is not a meaningful layered native master. The diagnostic sizes here are head crops, not recommended full-character canvases.

## Normalize explicit animation frames
```sh
python scripts/reference_lab.py normalize /absolute/path/to/completed-layout.json \
  --out /tmp/new-normalized-frames
```

Use `templates/animation_layout.example.json` as a schema example; replace its input paths and coordinates first. Input paths resolve relative to the JSON file. All inputs must already have a coherent source scale. The tool applies one common scale; it does not decide how large a differently framed head ought to be.

`source_anchor` is measured in the **full source image's edge-coordinate system** before its optional crop. `target_anchor` is in output-frame coordinates. `motion_offset` is an explicit displacement in **output pixels**; use it to retain intentional root travel. For a jump, do not anchor the lowest visible pixel to the idle ground line with a zero offset. Position the actual root appropriately or provide the intended displacement.

Placement is:
`translation = round(target_anchor + motion_offset - scaled_local_source_anchor)`.

Integer resized dimensions can cause slight x/y rounding differences; `effective_xy_scale` and `realized_anchor` disclose them. No independent bounding-box fitting occurs. Visible clipping, empty inputs, duplicate/unsafe frame names and missing durations cause an error before writing output. Fully transparent margins may extend beyond the output without losing visible content.

`require_transparent` checks for some fully transparent pixels, not correct segmentation. A stray transparent pixel does not certify a clean cutout. Inspect every frame. Background removal, palette unification, anatomy, in-betweens, timing quality and native-layer construction are outside the helper.

Outputs are equal-sized frames, a packed sheet (up to eight columns), supplied durations and processing records. A sheet is not a GIF/playback or an artistic approval. Use Aseprite/Godot for actual motion validation.

## Safety and verification
All output directories must be new. Source bytes are never written. Keep raw references unchanged. Files named in a layout are read as images; no commands are executed from the configuration. `verify_manifest.py` checks packaged-file SHA-256 values (excluding the manifest itself); it is an integrity inventory, not a cryptographic author signature and it does not reject extra user-added files.
