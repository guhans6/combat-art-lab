#!/usr/bin/env python3
"""Create matched 1x and nearest-neighbor 4x full-body/head review sheets."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "inputs"
BG = (39, 40, 45)
GUTTER = 12
FULL_REF_CROP = (390, 210, 830, 1020)
HEAD_REF_CROP = (360, 95, 782, 530)
HEAD_NATIVE_CROP = (25, 0, 91, 68)


def font(size: int) -> ImageFont.ImageFont:
    candidates = (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default(size=size)


def read_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def background(size: tuple[int, int]) -> Image.Image:
    return Image.new("RGBA", size, (*BG, 255))


def composite(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    canvas = background(size)
    image = source.convert("RGBA")
    if image.size != size:
        raise ValueError(f"Expected {size}, received {image.size}")
    canvas.alpha_composite(image)
    return canvas.convert("RGB")


def native_panels(candidate_path: Path, head: bool, include_candidate: bool):
    labels: list[str] = []
    panels: list[Image.Image] = []
    if head:
        reference = read_rgba(INPUTS / "character-closeup.png").crop(HEAD_REF_CROP)
        target_size = (HEAD_NATIVE_CROP[2] - HEAD_NATIVE_CROP[0], HEAD_NATIVE_CROP[3] - HEAD_NATIVE_CROP[1])
        reference = reference.resize(target_size, Image.Resampling.LANCZOS)
        seed = read_rgba(INPUTS / "source-only-converted-seed.png").crop(HEAD_NATIVE_CROP)
        baseline = read_rgba(INPUTS / "candidate-b-baseline.png").crop(HEAD_NATIVE_CROP)
        candidate = read_rgba(candidate_path).crop(HEAD_NATIVE_CROP)
    else:
        reference = read_rgba(INPUTS / "character-scene.png").crop(FULL_REF_CROP)
        target_size = (round(reference.width * 192 / reference.height), 192)
        reference = reference.resize(target_size, Image.Resampling.LANCZOS)
        seed = read_rgba(INPUTS / "source-only-converted-seed.png")
        baseline = read_rgba(INPUTS / "candidate-b-baseline.png")
        candidate = read_rgba(candidate_path)

    panels.append(composite(reference, target_size))
    labels.append("Reference")
    panels.append(composite(seed, seed.size))
    labels.append("Seed")
    panels.append(composite(baseline.crop(HEAD_NATIVE_CROP) if head else baseline, target_size if head else baseline.size))
    labels.append("Baseline")
    if include_candidate:
        panels.append(composite(candidate, target_size if head else candidate.size))
        labels.append("Luna 6")
    return panels, labels


def make_sheet(panels: list[Image.Image], labels: list[str], scale: int, output: Path) -> None:
    scaled = [panel.resize((panel.width * scale, panel.height * scale), Image.Resampling.NEAREST) for panel in panels]
    label_font = font(9 * scale)
    label_heights = [ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), label, font=label_font)[3] for label in labels]
    label_height = max(label_heights) + 8 * scale
    panel_width = max(panel.width for panel in scaled)
    panel_height = max(panel.height for panel in scaled)
    width = GUTTER * scale + len(scaled) * panel_width + (len(scaled) - 1) * GUTTER * scale
    height = GUTTER * scale + label_height + panel_height + GUTTER * scale
    sheet = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(sheet)
    x = GUTTER * scale
    for panel, label in zip(scaled, labels):
        cell_x = x + (panel_width - panel.width) // 2
        bbox = draw.textbbox((0, 0), label, font=label_font)
        text_x = x + (panel_width - (bbox[2] - bbox[0])) // 2
        draw.text((text_x, GUTTER * scale), label, fill=(238, 235, 226), font=label_font)
        sheet.paste(panel, (cell_x, GUTTER * scale + label_height))
        x += panel_width + GUTTER * scale
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, optimize=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--prefix", type=str, required=True)
    parser.add_argument("--baseline-only", action="store_true")
    args = parser.parse_args()
    candidate_path = args.candidate.resolve()
    if not candidate_path.exists():
        parser.error(f"Missing candidate PNG: {candidate_path}")
    for kind, head in (("fullbody", False), ("head", True)):
        panels, labels = native_panels(candidate_path, head, not args.baseline_only)
        for scale in (1, 4):
            make_sheet(panels, labels, scale, ROOT / "reviews" / f"{args.prefix}-{kind}-{scale}x.png")


if __name__ == "__main__":
    main()
