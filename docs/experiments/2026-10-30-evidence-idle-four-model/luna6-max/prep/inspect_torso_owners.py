#!/usr/bin/env python3
"""Read-only owner map and material counts for the frozen neutral torso."""
from __future__ import annotations

import collections
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location("native_reader", HERE / "check_native_candidate.py")
native_reader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(native_reader)

SOURCE = ROOT / "inputs" / "neutral.aseprite"
doc = native_reader.read_aseprite(SOURCE)
width, height = doc["canvas"]
names = [layer["name"] for layer in doc["layers"]]
symbols = {
    "02a-jacket-left": "L",
    "02b-jacket-right": "R",
    "03-shirt": "S",
    "04-tote": "B",
    "05-tote-strap": "T",
    "06a-left-hand": "l",
    "06b-right-hand": "r",
    "07-face-and-neck": "N",
}
layers = {i: symbols[name] for i, name in enumerate(names) if name in symbols}
x0, y0, x1, y1 = 44, 34, 84, 80
rows = [f"x tens {''.join(str((x // 10) % 10) for x in range(x0, x1))}",
        f"x ones {''.join(str(x % 10) for x in range(x0, x1))}"]
for y in range(y0, y1):
    row = []
    for x in range(x0, x1):
        owners = []
        for layer_index, symbol in layers.items():
            pixels = doc["cels"][(0, layer_index)]["pixels"]
            if pixels[(y * width + x) * 4 + 3]:
                owners.append(symbol)
        row.append("." if not owners else owners[0] if len(owners) == 1 else "*")
    rows.append(f"{y:02d} {''.join(row)}")
rows.extend(["", "Symbols: L/R jacket panels; S shirt; B tote; T strap; l/r hands; N face/neck; * overlapping owners; . transparent."])
(HERE / "native-torso-ownership.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")

palette_counts = {}
for index, name in enumerate(names):
    pixels = doc["cels"][(0, index)]["pixels"]
    counts = collections.Counter(tuple(pixels[i:i + 4]) for i in range(0, len(pixels), 4) if pixels[i + 3])
    palette_counts[name] = {
        "opaque_pixels": sum(counts.values()),
        "unique_rgba": len(counts),
        "most_common_12": [
            {"rgba": list(rgba), "hex": "#%02X%02X%02X" % rgba[:3], "count": count}
            for rgba, count in counts.most_common(12)
        ],
    }
(HERE / "native-layer-color-counts.json").write_text(json.dumps(palette_counts, indent=2) + "\n", encoding="utf-8")
print(HERE / "native-torso-ownership.txt")
print(HERE / "native-layer-color-counts.json")
