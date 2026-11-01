#!/usr/bin/env python3
"""Report whether an RGBA image change stayed inside an explicitly allowed mask."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", required=True, type=Path)
    parser.add_argument("--after", required=True, type=Path)
    parser.add_argument("--allow", action="append", default=[], metavar="X,Y")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    before = Image.open(args.before).convert("RGBA")
    after = Image.open(args.after).convert("RGBA")
    if before.size != after.size:
        report = {
            "accepted": False,
            "reason": "canvas dimensions differ",
            "before_size": before.size,
            "after_size": after.size,
            "changed_pixels": None,
            "outside_allowed": None,
        }
    else:
        allowed = set()
        for value in args.allow:
            x, y = (int(part) for part in value.split(",", 1))
            allowed.add((x, y))
        changed = []
        width, height = before.size
        for y in range(height):
            for x in range(width):
                if before.getpixel((x, y)) != after.getpixel((x, y)):
                    changed.append((x, y))
        outside = [point for point in changed if point not in allowed]
        report = {
            "accepted": not outside,
            "reason": "all changed pixels are within the allowed mask" if not outside else "changed pixels outside the allowed mask",
            "size": before.size,
            "allowed_pixels": [list(point) for point in sorted(allowed)],
            "changed_pixels": [list(point) for point in changed],
            "changed_count": len(changed),
            "outside_allowed": [list(point) for point in outside],
        }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["accepted"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
