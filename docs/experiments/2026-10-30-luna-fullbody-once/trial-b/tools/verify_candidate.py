#!/usr/bin/env python3
"""Check a full-body candidate's PNG locks against the frozen baseline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def count_changes(before: bytes, after: bytes, width: int, height: int, box: tuple[int, int, int, int] | None = None) -> int:
    x0, y0, x1, y1 = box if box else (0, 0, width, height)
    changes = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            i = (y * width + x) * 4
            if before[i:i + 4] != after[i:i + 4]:
                changes += 1
    return changes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--regions", type=Path, required=True, help="JSON: {protected:[{name,bbox}], review:[{name,bbox}]}")
    parser.add_argument("--palette", type=Path, help="JSON list of exact native palette entries, from MCP sprite_info")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    before_image, after_image = rgba(args.before), rgba(args.after)
    if before_image.size != after_image.size:
        raise SystemExit(f"Canvas mismatch: before={before_image.size}, after={after_image.size}")
    width, height = before_image.size
    before, after = before_image.tobytes(), after_image.tobytes()
    changes: list[tuple[int, int]] = []
    alpha_changes = 0
    partial_alpha = 0
    before_visible_colors: set[tuple[int, int, int]] = set()
    after_visible_colors: set[tuple[int, int, int]] = set()
    visible_before = visible_after = 0
    for y in range(height):
        for x in range(width):
            i = (y * width + x) * 4
            b, a = before[i:i + 4], after[i:i + 4]
            if b[3] != a[3]:
                alpha_changes += 1
            if a[3] not in (0, 255):
                partial_alpha += 1
            if b[3]:
                visible_before += 1
                before_visible_colors.add(tuple(b[:3]))
            if a[3]:
                visible_after += 1
                after_visible_colors.add(tuple(a[:3]))
            if b[3] != a[3] or (b[3] and a[3] and b[:3] != a[:3]):
                changes.append((x, y))

    region_data = json.loads(args.regions.read_text())
    protected_results = []
    for region in region_data.get("protected", []):
        box = tuple(region["bbox"])
        changed = count_changes(before, after, width, height, box)
        protected_results.append({"name": region["name"], "bbox": box, "changed_pixels": changed})
    review_results = []
    for region in region_data.get("review", []):
        box = tuple(region["bbox"])
        x0, y0, x1, y1 = box
        changed = sum(x0 <= x < x1 and y0 <= y < y1 for x, y in changes)
        review_results.append({"name": region["name"], "bbox": box, "changed_pixels": changed})

    bbox = None
    if changes:
        xs = [p[0] for p in changes]
        ys = [p[1] for p in changes]
        bbox = [min(xs), min(ys), max(xs) + 1, max(ys) + 1]
    new_visible_colors = sorted(after_visible_colors - before_visible_colors)
    if args.palette:
        native_palette = json.loads(args.palette.read_text())
        allowed_colors = {tuple(bytes.fromhex(value.lstrip("#")[:6])) for value in native_palette if len(value.lstrip("#")) >= 6}
    else:
        allowed_colors = before_visible_colors
    off_palette_colors = sorted(after_visible_colors - allowed_colors)
    result = {
        "before": str(args.before),
        "after": str(args.after),
        "canvas": [width, height],
        "visible_pixels_before": visible_before,
        "visible_pixels_after": visible_after,
        "alpha_changed_pixels": alpha_changes,
        "partial_alpha_pixels_after": partial_alpha,
        "changed_composite_pixels": len(changes),
        "changed_bounds_xyxy": bbox,
        "new_visible_rgb_values_vs_baseline": [list(color) for color in new_visible_colors],
        "off_palette_rgb_values": [list(color) for color in off_palette_colors],
        "protected_regions": protected_results,
        "review_regions": review_results,
        "png_constraints_pass": (
            alpha_changes == 0
            and partial_alpha == 0
            and len(changes) > 0
            and not off_palette_colors
            and all(item["changed_pixels"] == 0 for item in protected_results)
        ),
        "note": "This is a composite PNG check. It does not verify hidden layers, layer ownership, artistic quality or user approval. With --palette, RGB membership is checked against the exact palette read from the native MCP document.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["png_constraints_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
