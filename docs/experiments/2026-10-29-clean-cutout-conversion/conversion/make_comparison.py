#!/usr/bin/env python3
"""Render an honest source-and-seed comparison; it does not modify source art."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def matte(image: Image.Image, color=(255, 255, 255, 255)) -> Image.Image:
    result = Image.new("RGBA", image.size, color)
    result.alpha_composite(image.convert("RGBA"))
    return result


def checker(size: tuple[int, int], cell: int = 12) -> Image.Image:
    out = Image.new("RGBA", size, (48, 56, 70, 255))
    draw = ImageDraw.Draw(out)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=(69, 80, 97, 255))
    return out


def scale(image: Image.Image, size: tuple[int, int], nearest=False) -> Image.Image:
    return image.resize(size, Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS)


def panel(canvas: Image.Image, image: Image.Image, xy: tuple[int, int], label: str, font: ImageFont.ImageFont) -> None:
    canvas.alpha_composite(image, xy)
    ImageDraw.Draw(canvas).text((xy[0], xy[1] + image.height + 10), label, fill=(236, 240, 246), font=font)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rough-source", type=Path, required=True)
    parser.add_argument("--clean-source", type=Path, required=True)
    parser.add_argument("--rough-seed", type=Path, required=True)
    parser.add_argument("--clean-seed", type=Path, required=True)
    parser.add_argument("--current-standing", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    font = ImageFont.load_default()
    canvas = Image.new("RGBA", (1560, 1360), (27, 31, 40, 255))
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 20), "Full-character source conversion: rough cutout / generated clean cutout / current standing context", fill=(255, 255, 255), font=font)
    draw.text((24, 44), "Top: source images composited on white. Bottom: matched 128x192 BOX + shared-palette seeds at 3x. Current standing is separate context.", fill=(205, 213, 224), font=font)
    rough_source = scale(matte(Image.open(args.rough_source)), (320, 480))
    clean_source = scale(matte(Image.open(args.clean_source)), (320, 480))
    current = Image.open(args.current_standing).convert("RGBA")
    context = checker((320, 480))
    contained = scale(current, (213, 480), nearest=True)
    context.alpha_composite(contained, ((320 - contained.width) // 2, 0))
    panel(canvas, rough_source, (36, 88), "Rough cutout source on white (supporting reference)", font)
    panel(canvas, clean_source, (410, 88), "Generated clean cutout source on white (candidate)", font)
    panel(canvas, context, (784, 88), "Current standing frame on checkerboard (independent context)", font)
    rough_seed = scale(Image.open(args.rough_seed).convert("RGBA"), (384, 576), nearest=True)
    clean_seed = scale(Image.open(args.clean_seed).convert("RGBA"), (384, 576), nearest=True)
    rough_bg = checker(rough_seed.size)
    clean_bg = checker(clean_seed.size)
    rough_bg.alpha_composite(rough_seed)
    clean_bg.alpha_composite(clean_seed)
    panel(canvas, rough_bg, (36, 710), "Rough-source seed: 128x192, 3x nearest", font)
    panel(canvas, clean_bg, (470, 710), "Generated-source seed: 128x192, 3x nearest", font)
    draw.text((36, 1330), "Same 1024x1536 canvas, BOX resampling, one 48-colour palette from rough near-opaque interior pixels; alpha was preserved, not binarized.", fill=(205, 213, 224), font=font)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(args.out)


if __name__ == "__main__":
    main()
