#!/usr/bin/env python3
"""Inspect source-alpha coverage for candidate hole warnings at source scale."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


TRIAL = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--check", type=Path, required=True)
parser.add_argument("--prefix", required=True)
args = parser.parse_args()

source = Image.open(TRIAL / "input/source-cutout.png").convert("RGBA")
check = json.loads(args.check.read_text())
holes = check["frames"][0]["hole_pixels_xy"]
scale_factor = 8
scale = 3
region = (38, 3, 80, 38)
x0, y0, x1, y1 = region
crop = source.crop((x0 * scale_factor, y0 * scale_factor, x1 * scale_factor, y1 * scale_factor))
matte = Image.new("RGBA", crop.size, (48, 51, 60, 255))
view = Image.alpha_composite(matte, crop).convert("RGB").resize((crop.width * scale, crop.height * scale), Image.Resampling.NEAREST)
draw = ImageDraw.Draw(view)
for gx in range(x1 - x0 + 1):
    x = gx * scale_factor * scale
    draw.line((x, 0, x, view.height - 1), fill=(95, 98, 108))
for gy in range(y1 - y0 + 1):
    y = gy * scale_factor * scale
    draw.line((0, y, view.width - 1, y), fill=(95, 98, 108))
for x, y in holes:
    if x0 <= x < x1 and y0 <= y < y1:
        left, top = (x - x0) * scale_factor * scale, (y - y0) * scale_factor * scale
        right, bottom = left + scale_factor * scale - 1, top + scale_factor * scale - 1
        draw.rectangle((left, top, right, bottom), outline=(255, 30, 50), width=2)
view.save(TRIAL / "passes" / f"{args.prefix}-source-hole-grid.png")
print(f"region={region}, target-pixel-cell={scale_factor}x{scale_factor}, output={TRIAL / 'passes' / f'{args.prefix}-source-hole-grid.png'}")
