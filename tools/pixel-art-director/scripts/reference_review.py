#!/usr/bin/env python3
"""Show an approved-original crop beside an actual export; never score likeness."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


def checked_crop(image: Image.Image, box):
    box = tuple(box) if box is not None else (0, 0, *image.size)
    x0, y0, x1, y1 = box
    if not (0 <= x0 < x1 <= image.width and 0 <= y0 < y1 <= image.height):
        raise ValueError("Crop must be nonempty and within the source image.")
    return image.crop(box), box


def create_review(reference, candidate, out, reference_crop=None,
                  candidate_crop=None, candidate_zoom=4):
    reference, candidate, out = map(lambda p: Path(p).resolve(), (reference, candidate, out))
    sidecar = out.with_suffix(".json")
    if out.suffix.lower() != ".png":
        raise ValueError("Review output must be a PNG with a separate JSON sidecar.")
    if reference == candidate:
        raise ValueError("Provide separate approved-original and candidate files.")
    if any(p.exists() or p in (reference, candidate) for p in (out, sidecar)):
        raise FileExistsError("Keep previous evidence and inputs; choose a new output path.")
    if not isinstance(candidate_zoom, int) or not 1 <= candidate_zoom <= 16:
        raise ValueError("Candidate zoom must be an integer from 1 through 16.")
    with Image.open(reference) as image:
        ref_native = image.convert("RGBA")
    with Image.open(candidate) as image:
        candidate_native = image.convert("RGBA")
    ref, ref_box = checked_crop(ref_native, reference_crop)
    cand, cand_box = checked_crop(candidate_native, candidate_crop)
    height = cand.height * candidate_zoom
    ref_width = max(1, round(ref.width * height / ref.height))
    cand_width = cand.width * candidate_zoom
    if (ref_width + cand_width + 48) * (height + 120) > 20_000_000:
        raise ValueError("Review is too large; choose a tighter crop or smaller zoom.")
    sheet = Image.new("RGB", (ref_width + cand_width + 48, height + 120), "#30303e")
    draw = ImageDraw.Draw(sheet)
    records = []
    for x, role, path, native_size, crop, original, target in (
        (16, "APPROVED ORIGINAL (caller-selected)", reference, ref_native.size,
         ref_box, ref, (ref_width, height)),
        (ref_width + 32, "ACTUAL CANDIDATE EXPORT", candidate, candidate_native.size,
         cand_box, cand, (cand_width, height)),
    ):
        scale = target[1] / original.height
        label = "unresized crop" if target == original.size else f"nearest-neighbor {scale:g}x height"
        # Each panel has its own width: no stretching to disguise framing differences.
        draw.text((x, 8), role, fill="white")
        draw.text((x, 27), path.name, fill="white")
        draw.text((x, 46), f"crop {original.width}x{original.height}; {label}", fill="white")
        displayed = original.resize(target, Image.Resampling.NEAREST)
        sheet.paste(displayed, (x, 72), displayed)
        records.append({"role": role, "path": str(path),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                        "native_image_size": list(native_size), "crop_xyxy_half_open": list(crop),
                        "display_size": list(target), "display_height_ratio": scale,
                        "resampling": "none" if target == original.size else "nearest-neighbor"})
    draw.text((16, height + 88),
              "Matched crop heights only. Human/agent must inspect framing and likeness. No quality or resolution verdict.",
              fill="white")
    metadata = {"panels": records, "artistic_judgment": "not computed",
                "alignment": "crop heights only; anatomy not validated",
                "source_images_modified": False}
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    sidecar.write_text(json.dumps(metadata, indent=2) + "\n")
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--reference-crop", type=int, nargs=4)
    parser.add_argument("--candidate-crop", type=int, nargs=4)
    parser.add_argument("--candidate-zoom", type=int, default=4)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    create_review(args.reference, args.candidate, args.out, args.reference_crop,
                  args.candidate_crop, args.candidate_zoom)
    print(f"Saved {args.out} and its JSON sidecar; inspect the image before judging.")


if __name__ == "__main__":
    main()
