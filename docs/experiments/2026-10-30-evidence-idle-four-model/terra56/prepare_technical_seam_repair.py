#!/usr/bin/env python3
"""Prepare MCP pixel payloads for only parent-identified new alpha holes.

The source PNG supplies colour values; this script never alters any native file.
"""
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
CHECK = ROOT.parent / "terra56-parent-check.json"
BASELINE = ROOT / "exports" / "frames" / "terra56_0.png"
OUT = ROOT / "technical-repair-payload.json"

baseline = Image.open(BASELINE).convert("RGBA")
check = json.loads(CHECK.read_text())
frames = {}
for entry in check["alpha"]["frames"]:
    frame = entry["frame_1based"]
    holes = entry["new_enclosed_body_holes_xy"]
    if not holes:
        continue
    points = []
    for x, y in holes:
        r, g, b, a = baseline.getpixel((x, y))
        if a != 255:
            raise ValueError(f"baseline is not opaque at F{frame} ({x},{y})")
        points.append({"x": x, "y": y, "color": f"#{r:02x}{g:02x}{b:02x}"})
    frames[str(frame)] = points
OUT.write_text(json.dumps({
    "purpose": "seam backing only; exact parent-identified new enclosed alpha holes",
    "source": "exports/frames/terra56_0.png",
    "target_layer": "09-breath-seam-backing",
    "frames": frames,
}, indent=2) + "\n")
print(f"wrote {OUT}")
