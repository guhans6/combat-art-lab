#!/usr/bin/env python3
"""Read-only checks and before/after sheet for the generated-seed cleanup."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "inputs" / "baseline-generated-seed-128x192.png"
CANDIDATE = ROOT / "outputs" / "candidate-cleaned.png"
REOPENED = ROOT / "outputs" / "candidate-cleaned-reopened.png"
SOURCE = ROOT / "inputs" / "generated-clean-cutout-source.png"
OUT = ROOT / "evidence"

# The full head/hair block is locked.  The cleanup is confined to these denim pixels.
ALLOWED = {
    (51,131), (53,133),
    (48,148), (49,149), (50,150), (51,151), (52,152), (53,153),
    (84,148), (85,149), (86,150), (87,151), (88,152),
    (62,108), (62,109),
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def checker(size: tuple[int, int]) -> Image.Image:
    img = Image.new("RGBA", size, "#1d222b")
    d = ImageDraw.Draw(img)
    cell = 8
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                d.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#323b49")
    return img

def paste_alpha(target: Image.Image, image: Image.Image, at: tuple[int, int]) -> None:
    target.alpha_composite(image, at)

def main() -> None:
    baseline = Image.open(BASELINE).convert("RGBA")
    candidate = Image.open(CANDIDATE).convert("RGBA")
    reopened = Image.open(REOPENED).convert("RGBA")
    if baseline.size != (128, 192) or candidate.size != baseline.size:
        raise SystemExit("unexpected cleanup dimensions")
    if candidate.tobytes() != reopened.tobytes():
        raise SystemExit("fresh reopened export differs from candidate")

    changed = []
    alpha_changes = []
    protected_changes = []
    for y in range(192):
        for x in range(128):
            old = baseline.getpixel((x, y))
            new = candidate.getpixel((x, y))
            if old != new:
                changed.append({"x": x, "y": y, "old": old, "new": new})
                if old[3] != new[3]:
                    alpha_changes.append((x, y))
                if (x, y) not in ALLOWED:
                    protected_changes.append((x, y))
    if protected_changes or alpha_changes or not changed:
        raise SystemExit(json.dumps({"protected_changes": protected_changes, "alpha_changes": alpha_changes, "changed": len(changed)}))
    changed_coordinates = {(entry["x"], entry["y"]) for entry in changed}
    if not changed_coordinates.issubset(ALLOWED):
        raise SystemExit("candidate changes pixels outside the declared scoped patch")

    OUT.mkdir(exist_ok=True)
    (OUT / "change-ledger.json").write_text(json.dumps({
        "allowed_region": "denim folds and fly seam only",
        "face_lock": [19, 7, 78, 82],
        "alpha_changes": 0,
        "changes": changed,
    }, indent=2) + "\n")
    report = {
        "baseline_sha256": sha(BASELINE),
        "candidate_sha256": sha(CANDIDATE),
        "reopened_sha256": sha(REOPENED),
        "source_sha256": sha(SOURCE),
        "dimensions": [128, 192],
        "candidate_equals_reopened_rgba": True,
        "changed_pixels": len(changed),
        "alpha_changes": 0,
        "protected_changes": 0,
        "face_lock": [19, 7, 78, 82],
    }
    (OUT / "checks.json").write_text(json.dumps(report, indent=2) + "\n")

    canvas = Image.new("RGBA", (1660, 1360), "#161b23")
    draw = ImageDraw.Draw(canvas)
    draw.text((20, 16), "Generated-cutout conversion: source / baseline / cleaned candidate", fill="white")
    draw.text((20, 38), f"Face, expression, hair, silhouette and all alpha are locked. Red marks show only the {len(changed)} denim edits.", fill="#cbd5e1")
    source = Image.open(SOURCE).convert("RGBA")
    source.thumbnail((260, 390), Image.Resampling.NEAREST)
    white = Image.new("RGBA", source.size, "white")
    white.alpha_composite(source)
    canvas.alpha_composite(white, (20, 80))
    draw.text((20, 480), "Generated transparent source on white", fill="white")

    for x, image, title in [(340, baseline, "Baseline, actual 1x"), (520, candidate, "Candidate, actual 1x")]:
        panel = checker(image.size)
        panel.alpha_composite(image)
        canvas.alpha_composite(panel, (x, 100))
        draw.text((x, 300), title, fill="white")

    for x, image, title in [(20, baseline, "Baseline, 4x nearest"), (570, candidate, "Candidate, 4x nearest")]:
        panel = checker((512, 768))
        panel.alpha_composite(image.resize((512, 768), Image.Resampling.NEAREST))
        canvas.alpha_composite(panel, (x, 520))
        draw.text((x, 1295), title, fill="white")

    # 4x change mask at right, preserving the character-free indicator separately.
    mask = checker((512, 768))
    md = ImageDraw.Draw(mask)
    for x, y in changed_coordinates:
        md.rectangle((x * 4, y * 4, x * 4 + 3, y * 4 + 3), fill="#ff4d6d")
    canvas.alpha_composite(mask, (1120, 520))
    draw.text((1120, 1295), f"Changed pixels only ({len(changed)})", fill="white")
    canvas.save(OUT / "before-after-cleanup.png")

if __name__ == "__main__":
    main()
