#!/usr/bin/env python3
"""Compare source, seed, and pass-1 faces at the same target pixel dimensions."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "reviews"
OUT = REVIEWS / "pass-01"
OUT.mkdir(parents=True, exist_ok=True)

# Crop the approved close-up around the fringe, both eyes, mouth, and chin.
# It is 180x140 and reduced 5x with nearest-neighbour sampling to the same 36x28
# footprint used for the seed/candidate. This is a review transform only.
REFERENCE_BOX = (145, 125, 325, 265)
TARGET_BOX = (48, 10, 84, 38)
SCALE = 16
FONT = ImageFont.load_default()
BACKGROUND = (184, 184, 184, 255)


def make_sheet(path: Path, panels: list[tuple[str, Image.Image]], zoom: int) -> None:
    padding, header = 16, 30
    images = []
    for label, image in panels:
        image = image.convert("RGBA")
        if zoom != 1:
            image = image.resize((image.width * zoom, image.height * zoom), Image.Resampling.NEAREST)
        images.append((label, image))
    width = sum(im.width for _, im in images) + padding * (len(images) + 1)
    height = max(im.height for _, im in images) + header + padding * 2
    canvas = Image.new("RGBA", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    x = padding
    for label, image in images:
        draw.text((x, 8), label, fill=(22, 22, 22, 255), font=FONT)
        y = header + padding + (height - header - padding * 2 - image.height) // 2
        canvas.alpha_composite(image, (x, y))
        x += image.width + padding
    canvas.convert("RGB").save(path)


def main() -> None:
    reference = Image.open(REVIEWS / "reference-closeup-head-1x.png").convert("RGBA").crop(REFERENCE_BOX)
    if reference.size != (180, 140):
        raise AssertionError(f"Unexpected approved source crop: {reference.size}")
    reference = reference.resize((36, 28), Image.Resampling.NEAREST)
    reference.save(OUT / "matched-face-reference-36x28.png")

    seed = Image.open(ROOT / "input" / "seed-baseline.png").convert("RGBA").crop(TARGET_BOX)
    candidate = Image.open(ROOT / "pass-01" / "character-pass-01.png").convert("RGBA").crop(TARGET_BOX)
    if seed.size != candidate.size or seed.size != reference.size:
        raise AssertionError("Reference, seed, and candidate face crops must share dimensions")
    panels = [("source", reference), ("seed", seed), ("pass1", candidate)]
    make_sheet(OUT / "matched-face-1x.png", panels, 1)
    make_sheet(OUT / "matched-face-16x-nearest.png", panels, SCALE)


if __name__ == "__main__":
    main()
