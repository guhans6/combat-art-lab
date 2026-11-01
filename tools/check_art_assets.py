#!/usr/bin/env python3
"""Check the current reviewed character and shop exports. Does not judge art style."""
from pathlib import Path
import argparse
import json
import sys
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools/pixel-art-director/scripts"))
from pixel_checks import check_alpha_coverage, canonical_pixels, pixel_values

def check_profile(profile):
    results = []
    def add(name, passed, **details):
        results.append(dict(name=name, passed=bool(passed), **details))
    character = profile["character"]
    layout = json.loads((ROOT / character["layout"]).read_text())
    directory = ROOT / "godot/standing-idle-lab" / layout["frame_directory"].removeprefix("res://")
    count = character["frame_count"]
    add("character_frame_count", len(list(directory.glob("frame-*.png"))) == count
        and len(layout["durations_ms"]) == count)
    for frame in range(count):
        path = directory / f"frame-{frame:02}.png"
        with Image.open(path) as image:
            report = check_alpha_coverage(image,
                allowed_holes=character["intentional_holes_xy"][frame])
            partial = sum(0 < a < 255 for r, g, b, a in pixel_values(image.convert("RGBA")))
            add(f"character_{frame:02}", report["passed"] and image.size == tuple(layout["canvas"]) and not partial and image.convert("RGBA").getchannel("A").getbbox() is not None,
                alpha=report, partial_alpha=partial)
    shop = profile["shop"]
    directory = ROOT / shop["exports"]
    manifest = json.loads((directory / "parts-layout.json").read_text())
    add("shop_part_count", len(manifest["parts"]) == shop["part_count"])
    assembled = Image.new("RGBA", tuple(manifest["native_canvas"]))
    for part in manifest["parts"]:
        with Image.open(directory / part["file"]) as source:
            image = source.convert("RGBA")
        role = shop["parts"][part["name"]]
        region = tuple(role["coverage_region"]) if "coverage_region" in role else None
        report = check_alpha_coverage(image, region=region)
        partial = sum(0 < a < 255 for r, g, b, a in pixel_values(image))
        shape_ok = list(image.size) == part["size"] and image.getchannel("A").getbbox() is not None
        add(part["name"], report["passed"] and not partial and shape_ok,
            alpha=report, partial_alpha=partial, role=role["role"])
        assembled.alpha_composite(image, tuple(part["offset"]))
    with Image.open(directory / "shop.png") as image:
        add("shop_composite_coverage", check_alpha_coverage(image)["passed"])
        add("shop_exact_assembly", canonical_pixels(assembled) == canonical_pixels(image))
    return {"passed": all(r["passed"] for r in results), "checks": results,
            "boundary": "Reviewed coverage regions/explicit cutouts and export assembly; visual review remains required."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, default=ROOT / "tools/art-quality-profile.json")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        report = check_profile(json.loads(args.profile.read_text()))
    except (OSError, ValueError, KeyError, TypeError) as error:
        report = {"passed": False, "error": str(error)}
    text = json.dumps(report, indent=2) + "\n"
    if args.out:
        if args.out.exists(): parser.error("Use a fresh output path; reports are preserved.")
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)
    print(text, end="")
    return 0 if report["passed"] else 1
if __name__ == "__main__": raise SystemExit(main())
