#!/usr/bin/env python3
"""Encode the prepared seed as a reproducible Aseprite MCP grid operation."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from PIL import Image


TRIAL = Path(__file__).resolve().parents[1]
SEED = TRIAL / "prep/seed-128x192.png"
OUT = TRIAL / "prep/seed-grid.json"
GLYPHS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def main() -> None:
    image = Image.open(SEED).convert("RGBA")
    counts = Counter((r, g, b) for r, g, b, a in image.getdata() if a)
    colors = [rgb for rgb, _ in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]
    if len(colors) > len(GLYPHS):
        raise SystemExit(f"Need {len(colors)} glyphs; only {len(GLYPHS)} available")
    legend = {
        GLYPHS[index]: "#%02x%02x%02x" % color
        for index, color in enumerate(colors)
    }
    glyph_for = {color: glyph for color, glyph in zip(colors, GLYPHS)}
    rows = []
    for y in range(image.height):
        row = []
        for x in range(image.width):
            r, g, b, a = image.getpixel((x, y))
            row.append(glyph_for[(r, g, b)] if a else ".")
        rows.append("".join(row))
    payload = {
        "operation": {
            "kind": "grid",
            "x": 0,
            "y": 0,
            "rows": rows,
            "legend": legend,
            "transparent": "skip",
        },
        "paletteLock": False,
        "source": "prep/seed-128x192.png",
        "colors": len(colors),
        "visiblePixels": sum(counts.values()),
        "canvas": [image.width, image.height],
    }
    OUT.write_text(json.dumps(payload, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in payload.items() if k != "operation"}, indent=2))
    print(f"rows={len(rows)} columns={len(rows[0])} payload={OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
