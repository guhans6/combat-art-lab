#!/usr/bin/env python3
"""Read-only verification for the final generated-seed cleanup candidate."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "inputs" / "baseline-generated-seed-128x192.png"
CANDIDATE = ROOT / "outputs" / "candidate-cleaned.png"
REOPENED = ROOT / "outputs" / "candidate-cleaned-reopened.png"
ALLOWED = {(51,131), (53,133), (48,148), (49,149), (50,150), (51,151),
           (52,152), (53,153), (84,148), (85,149), (86,150), (87,151),
           (88,152), (62,108), (62,109)}

def main() -> None:
    baseline = Image.open(BASELINE).convert("RGBA")
    candidate = Image.open(CANDIDATE).convert("RGBA")
    reopened = Image.open(REOPENED).convert("RGBA")
    if baseline.size != (128, 192) or candidate.size != baseline.size:
        raise SystemExit("unexpected dimensions")
    if candidate.tobytes() != reopened.tobytes():
        raise SystemExit("reopened PNG differs")
    changed = []
    for y in range(192):
        for x in range(128):
            old, new = baseline.getpixel((x, y)), candidate.getpixel((x, y))
            if old != new:
                if (x, y) not in ALLOWED:
                    raise SystemExit(f"protected pixel changed: {(x, y)}")
                if old[3] != new[3]:
                    raise SystemExit(f"alpha changed: {(x, y)}")
                changed.append((x, y))
    if not changed:
        raise SystemExit("no cleanup pixels changed")
    print(json.dumps({"pass": True, "changed_pixels": len(changed), "alpha_changes": 0,
                      "protected_changes": 0, "reopened_rgba_equal": True}))

if __name__ == "__main__":
    main()
