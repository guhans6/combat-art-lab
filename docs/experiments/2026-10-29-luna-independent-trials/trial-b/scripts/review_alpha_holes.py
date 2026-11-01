#!/usr/bin/env python3
"""Compare alpha-check warnings with the frozen source-derived seed."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


TRIAL = Path(__file__).resolve().parents[1]
SOURCE = TRIAL / "input" / "source-cutout.png"
SEED = TRIAL / "prep" / "seed-128x192.png"
SOURCE_ALPHA_THRESHOLD = 32
REDUCTION = 8
SCALE = 6

parser = argparse.ArgumentParser()
parser.add_argument("--candidate", type=Path, default=TRIAL / "passes" / "pass-01.png")
parser.add_argument("--check", type=Path, default=TRIAL / "passes" / "pass-01-alpha-check.json")
parser.add_argument("--prefix", default="pass-01")
args = parser.parse_args()
OUTPUT_JSON = TRIAL / "passes" / f"{args.prefix}-alpha-hole-review.json"
OUTPUT_IMAGE = TRIAL / "passes" / f"{args.prefix}-alpha-holes.png"

candidate = Image.open(args.candidate).convert("RGBA")
seed = Image.open(SEED).convert("RGBA")
source = Image.open(SOURCE).convert("RGBA")
check = json.loads(args.check.read_text())
holes = check["frames"][0]["hole_pixels_xy"]
baseline_check_path = TRIAL / "passes" / "pass-01-alpha-check.json"
baseline_holes = json.loads(baseline_check_path.read_text())["frames"][0]["hole_pixels_xy"] if baseline_check_path.exists() else []
alpha_candidate = candidate.getchannel("A")
alpha_seed = seed.getchannel("A")
alpha_source = source.getchannel("A")

records = []
for x, y in holes:
    sx0, sy0 = x * REDUCTION, y * REDUCTION
    crop = alpha_source.crop((sx0, sy0, sx0 + REDUCTION, sy0 + REDUCTION))
    covered = sum(1 for value in crop.getdata() if value >= SOURCE_ALPHA_THRESHOLD)
    records.append(
        {
            "xy": [x, y],
            "candidate_alpha": alpha_candidate.getpixel((x, y)),
            "seed_alpha": alpha_seed.getpixel((x, y)),
            "same_as_seed": alpha_candidate.getpixel((x, y)) == alpha_seed.getpixel((x, y)),
            "source_block_nontransparent_samples": covered,
            "source_block_samples": REDUCTION * REDUCTION,
            "source_alpha_threshold": SOURCE_ALPHA_THRESHOLD,
        }
    )

# Show warnings over a nearest-neighbor 6x render while keeping the sprite
# recognizable on a neutral matte.
matte = Image.new("RGBA", candidate.size, (48, 51, 60, 255))
render = Image.alpha_composite(matte, candidate).convert("RGB").resize(
    (candidate.width * SCALE, candidate.height * SCALE), Image.Resampling.NEAREST
)
overlay = Image.new("RGBA", render.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
for x, y in holes:
    left, top = x * SCALE, y * SCALE
    draw.rectangle((left, top, left + SCALE - 1, top + SCALE - 1), fill=(255, 30, 50, 220))
    draw.rectangle((left - 1, top - 1, left + SCALE, top + SCALE), outline=(255, 255, 255, 245))
render = Image.alpha_composite(render.convert("RGBA"), overlay).convert("RGB")
render.save(OUTPUT_IMAGE)

report = {
    "candidate": str(args.candidate),
    "seed": "prep/seed-128x192.png",
    "source": "input/source-cutout.png",
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "alpha_check": str(args.check),
    "warning_pixel_count": len(records),
    "same_as_seed_count": sum(item["same_as_seed"] for item in records),
    "same_warning_coordinates_as_pass_01": holes == baseline_holes,
    "interpretation_boundary": "A match with the seed shows a warning predates the face pass; it does not establish that the opening is intentional or visually acceptable.",
    "records": records,
}
OUTPUT_JSON.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"image": str(OUTPUT_IMAGE), "report": str(OUTPUT_JSON), "warnings": len(records), "unchanged_from_seed": report["same_as_seed_count"]}, indent=2))
