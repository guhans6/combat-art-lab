#!/usr/bin/env python3
"""Convert matched transparent full-character inputs for a source comparison.

This is a seed-only comparison, not a native master or a background-removal tool.
It intentionally uses one palette derived from the rough source for both arms.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

CANVAS = (1024, 1536)
GRID = (128, 192)
SOLID_ALPHA = 250
PALETTE_COLORS = 48


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(image: Image.Image) -> tuple[Image.Image, dict]:
    image = image.convert("RGBA")
    if image.size == CANVAS:
        return image, {"mode": "identity", "source_size": list(image.size)}
    # A generated source can have a different export size. Preserve its aspect ratio,
    # center it on the frozen canvas, and disclose the transform instead of stretching.
    scale = min(CANVAS[0] / image.width, CANVAS[1] / image.height)
    size = (round(image.width * scale), round(image.height * scale))
    placed = Image.new("RGBA", CANVAS)
    resized = image.resize(size, Image.Resampling.LANCZOS)
    offset = ((CANVAS[0] - size[0]) // 2, (CANVAS[1] - size[1]) // 2)
    placed.alpha_composite(resized, offset)
    return placed, {
        "mode": "contain-center-lanczos",
        "source_size": list(image.size),
        "scale": scale,
        "placed_size": list(size),
        "offset": list(offset),
    }


def palette_from_rough(image: Image.Image) -> tuple[Image.Image, list[list[int]]]:
    rgba = image.convert("RGBA")
    # Fully/near-opaque source pixels define the palette, avoiding edge halo colors.
    # Build a dense list rather than masking a rectangle, which would let transparent
    # black fill dominate a median-cut palette.
    selected = [pixel[:3] for pixel in rgba.getdata() if pixel[3] >= SOLID_ALPHA]
    if not selected:
        raise ValueError("rough source contains no alpha >= solid threshold pixels")
    palette_source = Image.new("RGB", (len(selected), 1))
    palette_source.putdata(selected)
    q = palette_source.quantize(colors=PALETTE_COLORS, method=Image.Quantize.MEDIANCUT)
    raw = q.getpalette()[: PALETTE_COLORS * 3]
    values = [raw[i : i + 3] for i in range(0, len(raw), 3)]
    policy = Image.new("P", (1, 1))
    policy.putpalette(raw + [0] * (768 - len(raw)))
    return policy, values


def convert(image: Image.Image, policy: Image.Image) -> Image.Image:
    # BOX RGBA resampling preserves coverage. Quantize RGB only after reduction, then
    # restore that coverage; this avoids treating transparent edge RGB as paint.
    reduced = image.resize(GRID, Image.Resampling.BOX)
    rgb = reduced.convert("RGB").quantize(palette=policy, dither=Image.Dither.NONE).convert("RGB")
    result = rgb.convert("RGBA")
    result.putalpha(reduced.getchannel("A"))
    return result


def alpha_stats(image: Image.Image) -> dict:
    values = list(image.getchannel("A").getdata())
    return {
        "transparent": values.count(0),
        "partial": sum(1 for value in values if 0 < value < 255),
        "opaque": values.count(255),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rough", type=Path, required=True)
    parser.add_argument("--clean", type=Path, help="generated clean cutout; omit for rough-source baseline only")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit(f"refusing existing output directory: {args.out}")
    args.out.mkdir(parents=True)
    rough, rough_transform = normalize(Image.open(args.rough))
    policy, palette = palette_from_rough(rough)
    rough_seed = convert(rough, policy)
    rough.save(args.out / "rough-normalized.png")
    rough_seed.save(args.out / "rough-seed-128x192.png")
    recipe = {
        "rough": {"path": str(args.rough), "sha256": digest(args.rough), "transform": rough_transform, "alpha": alpha_stats(rough)},
        "canvas": list(CANVAS),
        "grid": list(GRID),
        "resample": "BOX",
        "dither": "none",
        "alpha_policy": "preserve BOX-resampled alpha; do not binarize",
        "palette_policy": f"{PALETTE_COLORS}-color median-cut palette from rough input pixels with alpha >= {SOLID_ALPHA}",
        "palette_rgb": palette,
        "purpose": "matched source-conversion seed comparison only; not a production sprite or native master",
    }
    if args.clean:
        clean, clean_transform = normalize(Image.open(args.clean))
        clean_seed = convert(clean, policy)
        clean.save(args.out / "clean-normalized.png")
        clean_seed.save(args.out / "clean-seed-128x192.png")
        recipe["clean"] = {"path": str(args.clean), "sha256": digest(args.clean), "transform": clean_transform, "alpha": alpha_stats(clean)}
    else:
        recipe["clean"] = None
    (args.out / "recipe.json").write_text(json.dumps(recipe, indent=2) + "\n")


if __name__ == "__main__":
    main()
