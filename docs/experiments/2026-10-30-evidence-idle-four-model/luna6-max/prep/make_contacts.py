#!/usr/bin/env python3
"""Make neutral-matte 1x/3x contact sheets from the MCP-exported PNGs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def load_frames(frame_list: list[str], matte: tuple[int, int, int]) -> list[Image.Image]:
    result = []
    for path in frame_list:
        with Image.open(path) as source:
            rgba = source.convert("RGBA")
        background = Image.new("RGBA", rgba.size, matte + (255,))
        background.alpha_composite(rgba)
        result.append(background.convert("RGB"))
    return result


def sheet(frames: list[Image.Image], scale: int, columns: int, gap: int,
          crop: tuple[int, int, int, int] | None, matte: tuple[int, int, int]) -> Image.Image:
    tiles = []
    for frame in frames:
        tile = frame.crop(crop) if crop else frame.copy()
        if scale != 1:
            tile = tile.resize((tile.width * scale, tile.height * scale), Image.Resampling.NEAREST)
        tiles.append(tile)
    tile_w, tile_h = tiles[0].size
    scaled_gap = gap * scale
    rows = (len(tiles) + columns - 1) // columns
    width = columns * tile_w + (columns + 1) * scaled_gap
    height = rows * tile_h + (rows + 1) * scaled_gap
    canvas = Image.new("RGB", (width, height), matte)
    for index, tile in enumerate(tiles):
        x = scaled_gap + (index % columns) * (tile_w + scaled_gap)
        y = scaled_gap + (index // columns) * (tile_h + scaled_gap)
        canvas.paste(tile, (x, y))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames-json", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--matte", default="808080")
    args = parser.parse_args()
    paths = json.loads(Path(args.frames_json).read_text(encoding="utf-8"))
    matte_hex = args.matte.lstrip("#")
    matte = tuple(int(matte_hex[i:i + 2], 16) for i in (0, 2, 4))
    frames = load_frames(paths, matte)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    torso_crop = (28, 30, 104, 88)
    report = {"order": "frame 1–5 left to right on top row; frame 6–10 left to right on bottom row",
              "matte_rgb": list(matte), "torso_crop_xyxy": list(torso_crop), "columns": 5, "files": {}}
    for scale in (1, 3):
        for name, crop in (("full", None), ("torso", torso_crop)):
            image = sheet(frames, scale, 5, 6, crop, matte)
            path = out / f"{name}-contact-{scale}x.png"
            image.save(path, format="PNG", optimize=False)
            report["files"][f"{name}_{scale}x"] = {"path": str(path), "dimensions": list(image.size)}
    (out / "contact-sheet-index.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
