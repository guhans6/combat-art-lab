#!/usr/bin/env python3
"""Make a review plate of a sprite over light, dark, and checker mattes."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "passes" / "pass-01.png"
OUTPUT = ROOT / "passes" / "pass-01-alpha-mattes.png"
SCALE = 4


def checker(size: tuple[int, int], cell: int = 8) -> Image.Image:
    image = Image.new("RGB", size, "#d8d8d8")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if ((x // cell) + (y // cell)) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#9b9b9b")
    return image


sprite = Image.open(SOURCE).convert("RGBA")
width, height = sprite.size
scaled = sprite.resize((width * SCALE, height * SCALE), Image.Resampling.NEAREST)
backgrounds = [
    Image.new("RGB", scaled.size, "#f5f1e8"),
    Image.new("RGB", scaled.size, "#30323a"),
    checker(scaled.size, 8 * SCALE),
]
labels = ["LIGHT", "DARK", "CHECKER"]
margin = 16
header = 24
plate = Image.new("RGB", (len(backgrounds) * scaled.width + (len(backgrounds) + 1) * margin, scaled.height + header + 2 * margin), "#ededeb")
draw = ImageDraw.Draw(plate)
for index, (background, label) in enumerate(zip(backgrounds, labels)):
    x = margin + index * (scaled.width + margin)
    y = margin + header
    draw.text((x, margin), label, fill="#202126")
    plate.paste(Image.alpha_composite(background.convert("RGBA"), scaled).convert("RGB"), (x, y))
plate.save(OUTPUT)
print(f"{OUTPUT} {plate.size[0]}x{plate.size[1]}")
