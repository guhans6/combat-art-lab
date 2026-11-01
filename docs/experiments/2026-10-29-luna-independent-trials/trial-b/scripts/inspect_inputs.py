#!/usr/bin/env python3
"""Freeze the authorized source/reference inputs and make alpha-matte evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


REPO = Path(__file__).resolve().parents[5]
TRIAL = Path(__file__).resolve().parents[1]
INTAKE = TRIAL / "intake"
INPUTS = {
    "production_source": REPO / "docs/experiments/2026-10-29-clean-cutout-conversion/inputs/clean-generated-cutout-v1.png",
    "identity_scene": REPO / "assets/references/approved-2026-10-26/character-scene.png",
    "identity_closeup": REPO / "assets/references/approved-2026-10-26/character-closeup.png",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_details(image: Image.Image) -> dict[str, object]:
    alpha = image.getchannel("A")
    histogram = alpha.histogram()
    counts = {
        "transparent": histogram[0],
        "partial": sum(histogram[1:255]),
        "opaque": histogram[255],
    }
    thresholds = {}
    for threshold in (1, 32, 64, 96, 128, 160, 192, 224, 248, 255):
        mask = alpha.point(lambda value, t=threshold: 255 if value >= t else 0)
        thresholds[str(threshold)] = {
            "pixels": sum(histogram[threshold:]),
            "bbox": mask.getbbox(),
        }
    return {
        "range": alpha.getextrema(),
        "counts": counts,
        "thresholds": thresholds,
    }


def checkerboard(size: tuple[int, int], tile: int = 16) -> Image.Image:
    image = Image.new("RGB", size, (218, 218, 218))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(172, 172, 172))
    return image


def matte(image: Image.Image, background: Image.Image | tuple[int, int, int]) -> Image.Image:
    if isinstance(background, tuple):
        back = Image.new("RGBA", image.size, (*background, 255))
    else:
        back = background.convert("RGBA")
    return Image.alpha_composite(back, image.convert("RGBA")).convert("RGB")


def main() -> None:
    INTAKE.mkdir(parents=True, exist_ok=True)
    report: dict[str, object] = {"inputs": {}}
    for role, path in INPUTS.items():
        image = Image.open(path).convert("RGBA")
        report["inputs"][role] = {
            "path": str(path.relative_to(REPO)),
            "sha256": digest(path),
            "size": image.size,
            "mode": "RGBA",
            "alpha": alpha_details(image) if role == "production_source" else None,
        }

    source = Image.open(INPUTS["production_source"]).convert("RGBA")
    preview_size = (source.width // 2, source.height // 2)
    source_preview = source.resize(preview_size, Image.Resampling.LANCZOS)
    panels = [
        ("white matte", matte(source_preview, (250, 250, 250))),
        ("dark matte", matte(source_preview, (28, 30, 38))),
        ("checkerboard", matte(source_preview, checkerboard(preview_size))),
        ("alpha coverage", source_preview.getchannel("A").convert("RGB")),
    ]
    label_height = 28
    sheet = Image.new("RGB", (preview_size[0] * len(panels), preview_size[1] + label_height), (245, 245, 245))
    draw = ImageDraw.Draw(sheet)
    for index, (label, panel) in enumerate(panels):
        x = index * preview_size[0]
        draw.text((x + 8, 7), label, fill=(20, 20, 20))
        sheet.paste(panel, (x, label_height))
    sheet.save(INTAKE / "source-alpha-mattes.png")
    (INTAKE / "input-observations.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
