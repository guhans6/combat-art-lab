#!/usr/bin/env python3
"""Offline inspection of the frozen neutral export; no native writes."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "inputs" / "neutral.png"
OUT = Path(__file__).resolve().parent


def main() -> None:
    image = Image.open(INPUT).convert("RGBA")
    pixels = list(image.getdata())
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    colors = Counter(pixels)
    opaque = [p for p in pixels if p[3] != 0]
    opaque_bbox = bbox
    preview = image.resize((image.width * 4, image.height * 4), Image.Resampling.NEAREST)
    preview.save(OUT / "neutral-4x.png")
    summary = {
        "input": str(INPUT),
        "sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
        "size": [image.width, image.height],
        "alpha_bbox_xyxy": list(opaque_bbox) if opaque_bbox else None,
        "opaque_pixels": len(opaque),
        "visible_rgba_count": len(colors),
        "top_visible_rgba": [
            {"rgba": list(rgba), "count": count}
            for rgba, count in colors.most_common(16)
            if rgba[3] != 0
        ],
    }
    (OUT / "neutral-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
