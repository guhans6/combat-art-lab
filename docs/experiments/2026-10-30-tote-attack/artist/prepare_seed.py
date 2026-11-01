#!/usr/bin/env python3
"""Build the first deterministic, palette-mapped recovery pose seed.

This prepares a transparent PNG checkpoint only. It does not write native
Aseprite files; native layers/cels are assembled through the dedicated MCP.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "inputs"
ARTIST = Path(__file__).resolve().parent
OUT = ARTIST / "checkpoints" / "recovery-body-head-masked-v03.png"

# Additional-key sheet, middle panel: the upright recovery the task asks us to
# repair. Scale is one shared source-family scale (not a per-pose fit). The
# source pelvis/foot anchors are provisional and will be measured against the
# neutral at 1x before final assembly.
PANEL = (724, 0, 1448, 724)
SCALE = 0.264
SOURCE_ROOT = (310, 708)
TARGET_ROOT = (132, 185)
CANVAS = (256, 192)
HEAD_EDGE_CLEAR = [
    [163, 36],
    [162, 37], [163, 37], [164, 37],
    [160, 38], [161, 38], [162, 38], [163, 38], [164, 38],
    [159, 39], [160, 39], [161, 39], [162, 39], [163, 39], [164, 39], [165, 39],
]


def rgb(hex_color: str) -> tuple[int, int, int] | None:
    value = hex_color.lstrip("#")
    if len(value) == 8 and int(value[6:8], 16) == 0:
        return None
    if len(value) not in (6, 8):
        return None
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


@lru_cache(maxsize=50000)
def nearest(color: tuple[int, int, int], palette: tuple[tuple[int, int, int], ...]) -> tuple[int, int, int]:
    r, g, b = color
    return min(
        palette,
        key=lambda p: 2 * (r - p[0]) ** 2 + 4 * (g - p[1]) ** 2 + 3 * (b - p[2]) ** 2,
    )


def main() -> None:
    raw_palette = json.loads((ARTIST / "seed-palette.json").read_text())
    palette = tuple(dict.fromkeys(c for item in raw_palette if (c := rgb(item)) is not None))
    if not palette:
        raise SystemExit("neutral palette has no opaque RGB entries")

    sheet = Image.open(INPUTS / "additional-keys.png").convert("RGBA")
    panel = sheet.crop(PANEL)
    # This small bottom-left fragment is disconnected from the pose and spills
    # across the generated sheet's panel boundary. It is a spatial source mask,
    # not a hue/color-key removal.
    panel_pixels = panel.load()
    spill_removed = 0
    for y in range(640, panel.height):
        for x in range(0, 24):
            if panel_pixels[x, y][3] >= 128:
                panel_pixels[x, y] = (0, 0, 0, 0)
                spill_removed += 1
    alpha = panel.getchannel("A")
    # The input contains partial-alpha antialiasing. Make the export binary at
    # the source edge; do not recolour or delete material pixels by hue.
    mask = alpha.point(lambda a: 255 if a >= 128 else 0)
    cut = Image.new("RGBA", panel.size, (0, 0, 0, 0))
    cut.paste(panel, (0, 0), mask)

    scaled_size = (round(panel.width * SCALE), round(panel.height * SCALE))
    scaled = cut.resize(scaled_size, Image.Resampling.NEAREST)

    root_dx = TARGET_ROOT[0] - round(SOURCE_ROOT[0] * SCALE)
    root_dy = TARGET_ROOT[1] - round(SOURCE_ROOT[1] * SCALE)
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    mapped = Image.new("RGBA", scaled.size, (0, 0, 0, 0))
    source_pixels = scaled.load()
    mapped_pixels = mapped.load()
    for y in range(scaled.height):
        for x in range(scaled.width):
            r, g, b, a = source_pixels[x, y]
            if a:
                mapped_pixels[x, y] = (*nearest((r, g, b), palette), 255)
    # The pose reference has a larger and less faithful head than the neutral.
    # Clear only the head/face area so the native neutral layers can be placed
    # at the measured head anchor as independent editable cels.
    head_cut = Image.new("1", CANVAS, 0)
    ImageDraw.Draw(head_cut).polygon(
        [
            (111, 14), (115, 5), (124, 1), (137, -2), (151, 0),
            (162, 6), (169, 16), (170, 26), (165, 34), (158, 39),
            (149, 41), (139, 39), (130, 39), (122, 40), (116, 36),
            (110, 28), (108, 21),
        ],
        fill=1,
    )
    canvas_body = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    canvas_body.alpha_composite(mapped, (root_dx, root_dy))
    body_pixels = canvas_body.load()
    for y in range(CANVAS[1]):
        for x in range(CANVAS[0]):
            if head_cut.getpixel((x, y)):
                body_pixels[x, y] = (0, 0, 0, 0)
    # Remove only the generated sideburn edge that remains outside the smaller
    # native hair silhouette. This stops at y=39; the source jacket/collar
    # backing starting at y=40 stays intact.
    for x, y in HEAD_EDGE_CLEAR:
        body_pixels[x, y] = (0, 0, 0, 0)
    canvas = canvas_body

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT)
    metadata = {
        "source": "../inputs/additional-keys.png",
        "panel_xyxy": list(PANEL),
        "scale": SCALE,
        "source_root_foot_xy": list(SOURCE_ROOT),
        "target_root_foot_xy": list(TARGET_ROOT),
        "offset_xy": [root_dx, root_dy],
        "canvas": list(CANVAS),
        "alpha_threshold": 128,
        "palette_colors_opaque": len(palette),
        "edge_spill_mask_source_xyxy": [0, 640, 24, 724],
        "edge_spill_pixels_removed": spill_removed,
        "head_replacement_mask_canvas_polygon": [
            [111, 14], [115, 5], [124, 1], [137, -2], [151, 0],
            [162, 6], [169, 16], [170, 26], [165, 34], [158, 39],
            [149, 41], [139, 39], [130, 39], [122, 40], [116, 36],
            [110, 28], [108, 21],
        ],
        "head_source_sideburn_edge_removed_canvas_xy": HEAD_EDGE_CLEAR,
        "layer_state": "body checkpoint only; cleared head is replaced from exact neutral face/hair layers through MCP",
    }
    (OUT.with_suffix(".json")).write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata))


if __name__ == "__main__":
    main()
