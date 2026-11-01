#!/usr/bin/env python3
"""Make matched 1x/4x reference sheets without scoring visual likeness."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


TRIAL = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[5]
MATTE = (48, 51, 60)
INK = (24, 26, 31)
PAPER = (238, 238, 234)
SCENE_CROP = (470, 220, 800, 1040)
HEAD_REFERENCE_CROP = (430, 100, 850, 500)
HEAD_CANDIDATE_CROP = (46, 3, 86, 50)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def composite(image: Image.Image, background: tuple[int, int, int]) -> Image.Image:
    back = Image.new("RGBA", image.size, (*background, 255))
    return Image.alpha_composite(back, image.convert("RGBA")).convert("RGB")


def scaled_to_height(image: Image.Image, height: int) -> Image.Image:
    width = max(1, round(image.width * height / image.height))
    return image.resize((width, height), Image.Resampling.NEAREST)


def panel_with_reference_crop(
    reference: Image.Image,
    canvas: tuple[int, int],
    content_top: int,
    content_height: int,
    scale: int,
) -> Image.Image:
    width, height = canvas
    panel = Image.new("RGB", (width * scale, height * scale), MATTE)
    crop = scaled_to_height(reference, content_height * scale)
    x = (width * scale - crop.width) // 2
    y = content_top * scale
    panel.paste(crop, (x, y))
    return panel


def labelled_panel(label: str, image: Image.Image, scale: int) -> Image.Image:
    label_height = 22 if scale == 1 else 32
    panel = Image.new("RGB", (image.width, image.height + label_height), PAPER)
    draw = ImageDraw.Draw(panel)
    font = ImageFont.load_default(size=10 if scale == 1 else 18)
    draw.text((8, 4 if scale == 1 else 5), label, fill=INK, font=font)
    panel.paste(image, (0, label_height))
    return panel


def compose_row(panels: list[Image.Image], gap: int, title: str) -> Image.Image:
    title_height = 28
    row_height = max(panel.height for panel in panels)
    width = sum(panel.width for panel in panels) + gap * (len(panels) - 1)
    row = Image.new("RGB", (width, title_height + row_height), PAPER)
    draw = ImageDraw.Draw(row)
    draw.text((8, 7), title, fill=INK, font=ImageFont.load_default())
    x = 0
    for panel in panels:
        row.paste(panel, (x, title_height))
        x += panel.width + gap
    return row


def compose_scale_sheet(rows: list[Image.Image], out: Path, metadata: dict[str, object]) -> None:
    page_gap = 28
    width = max(row.width for row in rows)
    height = sum(row.height for row in rows) + page_gap * (len(rows) - 1) + 16
    sheet = Image.new("RGB", (width, height), PAPER)
    y = 8
    for row in rows:
        sheet.paste(row, ((width - row.width) // 2, y))
        y += row.height + page_gap
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    out.with_suffix(".json").write_text(json.dumps(metadata, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--seed", type=Path, default=TRIAL / "prep/seed-128x192.png")
    parser.add_argument("--scene", type=Path, default=TRIAL / "input/character-scene.png")
    parser.add_argument("--closeup", type=Path, default=TRIAL / "input/character-closeup.png")
    parser.add_argument("--out-dir", type=Path, default=TRIAL / "passes")
    parser.add_argument("--prefix", type=str)
    args = parser.parse_args()

    prefix = args.prefix or args.candidate.stem

    candidate = Image.open(args.candidate).convert("RGBA")
    seed = Image.open(args.seed).convert("RGBA")
    scene = Image.open(args.scene).convert("RGB")
    closeup = Image.open(args.closeup).convert("RGB")
    if candidate.size != (128, 192) or seed.size != candidate.size:
        raise SystemExit(f"Expected 128x192 candidate/seed, got {candidate.size}/{seed.size}")
    alpha = candidate.getchannel("A")
    visible = alpha.getbbox()
    if visible is None:
        raise SystemExit("Candidate export is fully transparent")
    left, top, right, bottom = visible
    content_height = bottom - top
    neutral_candidate = composite(candidate, MATTE)
    neutral_seed = composite(seed, MATTE)
    scene_crop = scene.crop(SCENE_CROP)

    full_rows = []
    for scale in (1, 4):
        canvas = (128 * scale, 192 * scale)
        scene_panel = panel_with_reference_crop(
            scene_crop, (128, 192), top, content_height, scale
        )
        panels = [
            labelled_panel("SEED", neutral_seed.resize(canvas, Image.Resampling.NEAREST), scale),
            labelled_panel("APPROVED REFERENCE", scene_panel, scale),
            labelled_panel("CANDIDATE", neutral_candidate.resize(canvas, Image.Resampling.NEAREST), scale),
        ]
        full_rows.append(compose_row(
            panels,
            gap=18 * scale,
            title=("FULL BODY • 1x NATIVE CANVAS" if scale == 1 else "FULL BODY • 4x NEAREST-NEIGHBOR DISPLAY"),
        ))

    full_meta = {
        "candidate": str(args.candidate),
        "candidate_sha256": sha256(args.candidate),
        "seed": str(args.seed),
        "seed_sha256": sha256(args.seed),
        "scene_reference": str(args.scene),
        "scene_sha256": sha256(args.scene),
        "canvas": [128, 192],
        "candidate_alpha_bbox": list(visible),
        "approved_scene_crop": list(SCENE_CROP),
        "comparison": "Reference crop scaled nearest-neighbor to candidate visible height; candidate shown on a neutral matte. 4x is diagnostic display only.",
        "resampling": "nearest-neighbor for all display scaling",
    }
    compose_scale_sheet(full_rows, args.out_dir / f"{prefix}-review-sheet.png", full_meta)

    head = candidate.crop(HEAD_CANDIDATE_CROP)
    head_matte = composite(head, MATTE)
    head_reference = closeup.crop(HEAD_REFERENCE_CROP)
    head_rows = []
    for scale in (1, 4):
        ref = scaled_to_height(head_reference, head.height * scale)
        candidate_view = head_matte.resize((head.width * scale, head.height * scale), Image.Resampling.NEAREST)
        panel_width = max(ref.width, candidate_view.width) + 8 * scale
        ref_panel = Image.new("RGB", (panel_width, head.height * scale), MATTE)
        cand_panel = Image.new("RGB", (panel_width, head.height * scale), MATTE)
        ref_panel.paste(ref, ((panel_width - ref.width) // 2, 0))
        cand_panel.paste(candidate_view, ((panel_width - candidate_view.width) // 2, 0))
        panels = [
            labelled_panel("REF", ref_panel, scale),
            labelled_panel("SPRITE", cand_panel, scale),
        ]
        head_rows.append(compose_row(
            panels,
            gap=18 * scale,
            title=("HEAD • 1x NATIVE PIXELS" if scale == 1 else "HEAD • 4x NEAREST-NEIGHBOR DISPLAY"),
        ))
    head_meta = {
        "candidate": str(args.candidate),
        "candidate_sha256": sha256(args.candidate),
        "closeup_reference": str(args.closeup),
        "closeup_sha256": sha256(args.closeup),
        "candidate_head_crop": list(HEAD_CANDIDATE_CROP),
        "approved_closeup_crop": list(HEAD_REFERENCE_CROP),
        "candidate_crop_dimensions": list(head.size),
        "comparison": "Reference crop scaled nearest-neighbor to candidate head crop height; crop is for face/hair diagnostic only.",
        "resampling": "nearest-neighbor for all display scaling",
    }
    compose_scale_sheet(head_rows, args.out_dir / f"{prefix}-head-review.png", head_meta)
    print(json.dumps({
        "candidate_alpha_bbox": visible,
        "review_sheet": str(args.out_dir / f"{prefix}-review-sheet.png"),
        "head_review": str(args.out_dir / f"{prefix}-head-review.png"),
    }, indent=2))


if __name__ == "__main__":
    main()
