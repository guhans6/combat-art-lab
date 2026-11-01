#!/usr/bin/env python3
"""Build direct source/seed/candidate contact sheets at native and integer zoom."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
REVIEWS = ROOT / "reviews"
OUT = REVIEWS / "pass-01"
OUT.mkdir(parents=True, exist_ok=True)
FONT = ImageFont.load_default()
BACKGROUND = (184, 184, 184, 255)


def sheet(path: Path, panels: list[tuple[str, Image.Image]], scale: int) -> None:
    rendered = []
    for label, image in panels:
        image = image.convert("RGBA")
        if scale != 1:
            image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
        rendered.append((label, image))
    padding, header = 16, 30
    width = sum(image.width for _, image in rendered) + padding * (len(rendered) + 1)
    height = max(image.height for _, image in rendered) + header + padding * 2
    canvas = Image.new("RGBA", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    x = padding
    for label, image in rendered:
        draw.text((x, 8), label, fill=(22, 22, 22, 255), font=FONT)
        y = header + padding + (height - header - padding * 2 - image.height) // 2
        canvas.alpha_composite(image, (x, y))
        x += image.width + padding
    canvas.convert("RGB").save(path)


def main() -> None:
    scene = Image.open(REVIEWS / "reference-scene-character-context-1x.png")
    closeup = Image.open(REVIEWS / "reference-closeup-head-1x.png")
    seed = Image.open(ROOT / "input" / "seed-baseline.png").convert("RGBA")
    candidate = Image.open(ROOT / "pass-01" / "character-pass-01.png").convert("RGBA")

    full = [("scene", scene), ("seed", seed), ("pass1", candidate)]
    sheet(OUT / "full-body-1x.png", full, 1)
    sheet(OUT / "full-body-2x-nearest.png", full, 2)

    face_box = (48, 10, 84, 38)
    face = [("ref", closeup), ("seed", seed.crop(face_box)), ("pass1", candidate.crop(face_box))]
    sheet(OUT / "face-1x.png", face, 1)
    sheet(OUT / "face-2x-nearest.png", face, 2)
    face[2][1].resize((face[2][1].width * 18, face[2][1].height * 18), Image.Resampling.NEAREST).save(
        OUT / "pass-01-face-18x.png"
    )


if __name__ == "__main__":
    main()
