#!/usr/bin/env python3
"""Independent smoke checker: accept only the declared one-pixel edit at (6,6)."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
before = Image.open(ROOT / "scratch-smoke.png").convert("RGBA")
after = Image.open(ROOT / "scratch-out-of-mask.png").convert("RGBA")
if before.size != after.size:
    raise SystemExit(f"CHECKER ERROR: dimensions differ: {before.size} vs {after.size}")
diffs = [(x, y) for y in range(before.height) for x in range(before.width) if before.getpixel((x, y)) != after.getpixel((x, y))]
allowed = {(6, 6)}
if not diffs:
    raise SystemExit("CHECKER ERROR: expected controlled out-of-mask change is absent")
outside = [point for point in diffs if point not in allowed]
if not outside:
    raise SystemExit(f"CHECKER ERROR: all changes fell within the allowed mask: {diffs}")
if diffs != [(15, 15)]:
    raise SystemExit(f"CHECKER ERROR: unexpected changed coordinates: {diffs}")
print(f"REJECTED AS EXPECTED: changed composite pixel {diffs[0]} is outside allowed mask {sorted(allowed)}")
