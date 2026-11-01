"""Emit a Pebbly `draw.pixels` payload from one frozen prepared part.

This is deterministic transfer input only: every opaque source-part RGBA sample is
represented once, with its native-grid coordinate and RGB colour. The Aseprite MCP
performs the drawing; this script never writes a native or final-art file.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

RUN = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("part")
args = parser.parse_args()
image = Image.open(RUN / "masks" / f"{args.part}.png").convert("RGBA")
groups: dict[str, list[dict[str, int]]] = {}
for y in range(image.height):
    for x in range(image.width):
        r, g, b, a = image.getpixel((x, y))
        if a:
            groups.setdefault(f"#{r:02x}{g:02x}{b:02x}", []).append({"x": x, "y": y})
ops = [{"kind": "pixels", "color": color, "points": points}
       for color, points in sorted(groups.items())]
print(json.dumps({"ops": ops}, separators=(",", ":")))
