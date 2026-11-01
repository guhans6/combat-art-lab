#!/usr/bin/env python3
"""Verify an exported PNG against its expected local raster and seed."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument("--candidate", type=Path, required=True)
parser.add_argument("--seed", type=Path, default=Path(__file__).resolve().parents[1] / "prep/seed-128x192.png")
parser.add_argument("--expected", type=Path, required=True)
parser.add_argument("--out", type=Path, required=True)
parser.add_argument("--allow-box", type=int, nargs=4, action="append", default=[], metavar=("X0", "Y0", "X1", "Y1"))
args = parser.parse_args()


def load(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def canonical(pixel: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return pixel if pixel[3] else (0, 0, 0, 0)


candidate = load(args.candidate)
seed = load(args.seed)
expected = load(args.expected)
if candidate.size != seed.size or candidate.size != expected.size:
    raise SystemExit(f"Canvas mismatch: candidate={candidate.size}, seed={seed.size}, expected={expected.size}")

visible = candidate.getchannel("A").getbbox()
if visible is None:
    raise SystemExit("Candidate is fully transparent")
alpha_values = sorted(set(candidate.getchannel("A").getdata()))
changes = []
alpha_changed = []
semantic_mismatches = []
outside_allowed = []
for y in range(candidate.height):
    for x in range(candidate.width):
        before = canonical(seed.getpixel((x, y)))
        after = canonical(candidate.getpixel((x, y)))
        predicted = canonical(expected.getpixel((x, y)))
        if before[3] != after[3]:
            alpha_changed.append([x, y])
        elif before != after and after[3]:
            changes.append({"x": x, "y": y, "before": "#%02x%02x%02x%02x" % before, "after": "#%02x%02x%02x%02x" % after})
            if args.allow_box and not any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in args.allow_box):
                outside_allowed.append([x, y])
        if after != predicted:
            semantic_mismatches.append([x, y])

report = {
    "candidate": str(args.candidate),
    "sha256": hashlib.sha256(args.candidate.read_bytes()).hexdigest(),
    "size": list(candidate.size),
    "alpha_values": alpha_values,
    "visible_bbox": list(visible),
    "visible_pixels": sum(1 for pixel in candidate.getdata() if pixel[3]),
    "visible_colors": len({pixel[:3] for pixel in candidate.getdata() if pixel[3]}),
    "changed_visible_pixels_from_seed": len(changes),
    "changes": changes,
    "allowed_change_regions": args.allow_box,
    "changed_pixels_outside_allowed_regions": outside_allowed,
    "alpha_changed_pixels": len(alpha_changed),
    "alpha_changed_xy": alpha_changed,
    "matches_semantic_prediction": len(semantic_mismatches) == 0,
    "semantic_mismatch_count": len(semantic_mismatches),
    "semantic_mismatch_xy": semantic_mismatches,
}
args.out.parent.mkdir(parents=True, exist_ok=True)
args.out.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
if alpha_changed or semantic_mismatches or outside_allowed:
    raise SystemExit(2)
