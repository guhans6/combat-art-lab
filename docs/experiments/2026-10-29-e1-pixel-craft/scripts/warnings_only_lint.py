"""Warnings-only E1 pixel-craft inventory; it never edits an image."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
image_path = ROOT / "inputs/control-a.png"
image = Image.open(image_path).convert("RGBA")
pixels = image.load()
warnings = []
for y in range(image.height):
    for x in range(image.width):
        r, g, b, a = pixels[x, y]
        if not a:
            continue
        neighbours = [
            pixels[nx, ny] for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
            if 0 <= nx < image.width and 0 <= ny < image.height
        ]
        if neighbours and all(n[3] and n[:3] != (r, g, b) for n in neighbours):
            warnings.append({"coordinate": [x, y], "rgb": [r, g, b], "kind": "no 4-neighbour with same RGB"})
colors = Counter(pixel for pixel in image.get_flattened_data() if pixel[3])
report = {
    "schema": 1,
    "mode": "warnings-only",
    "input": str(image_path.relative_to(ROOT)),
    "input_sha256": sha256(image_path.read_bytes()).hexdigest(),
    "canvas": list(image.size),
    "visible_color_count": len(colors),
    "isolated_rgb_warning_count": len(warnings),
    "warnings": warnings,
    "interpretation": "These are diagnostic candidates, not erase/repaint instructions. No warning is acted on without a separate visual hypothesis."
}
(ROOT / "warnings-only-lint.json").write_text(json.dumps(report, indent=2) + "\n")
print(f"PASS: warnings-only lint wrote {len(warnings)} non-actionable color-isolation observations")
