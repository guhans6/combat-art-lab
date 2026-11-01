#!/usr/bin/env python3
"""Partition the frozen target raster into editable, non-overlapping parts."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


TRIAL = Path(__file__).resolve().parents[1]
SEED_PATH = TRIAL / "prep" / "seed-128x192.png"
OUTPUT = TRIAL / "prep" / "semantic-pass02"
SCALE = 3

PARTS = (
    "Face, neck, hands",
    "Hair",
    "Tote and strap",
    "Shirt",
    "Jacket",
    "Jeans",
    "Shoes",
    "Contour details",
    "Facial features",
)
SKIN = {
    (0xF5, 0xA1, 0x72), (0xEE, 0xAE, 0x8A), (0xE8, 0xC7, 0xB4),
    (0xCD, 0xA7, 0x98), (0xFD, 0xE4, 0xCD), (0xFB, 0xDA, 0xBC),
    (0xBF, 0x99, 0x8A), (0xAA, 0x83, 0x78),
}
PALE = SKIN | {(0x42, 0x4D, 0x5B), (0x2F, 0x36, 0x40), (0x3F, 0x43, 0x44)}
OLIVE = {(0x68, 0x60, 0x3C), (0x59, 0x50, 0x38), (0x61, 0x59, 0x3A), (0x64, 0x61, 0x4A), (0x69, 0x61, 0x3C)}
FEATURE_COLORS = {
    (0x2D, 0x24, 0x27), (0x4C, 0x2A, 0x24), (0x77, 0x46, 0x34),
    (0x83, 0x63, 0x4B), (0xFD, 0xE4, 0xCD), (0xFB, 0xDA, 0xBC),
    (0xE8, 0xC7, 0xB4), (0xAA, 0x83, 0x78),
}


def polygon_mask(size: tuple[int, int], points: list[tuple[int, int]]) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    return mask


seed = Image.open(SEED_PATH).convert("RGBA")
size = seed.size
alpha = seed.getchannel("A")
head_mask = polygon_mask(size, [(41, 2), (84, 2), (84, 23), (80, 27), (77, 31), (74, 34), (72, 37), (68, 41), (55, 44), (43, 39), (40, 30)])
face_mask = polygon_mask(size, [(61, 16), (73, 17), (78, 22), (78, 28), (75, 35), (70, 40), (68, 45), (62, 46), (55, 44), (57, 40), (59, 34), (59, 27), (60, 21)])
left_hand_mask = polygon_mask(size, [(34, 69), (43, 69), (46, 79), (42, 84), (35, 81)])
right_hand_mask = polygon_mask(size, [(70, 67), (83, 67), (85, 78), (80, 84), (73, 81), (68, 76)])
skin_mask = Image.new("L", size, 0)
for mask in (face_mask, left_hand_mask, right_hand_mask):
    skin_mask = Image.frombytes("L", size, bytes(max(a, b) for a, b in zip(skin_mask.tobytes(), mask.tobytes())))

tote_shape = polygon_mask(size, [(77, 35), (82, 36), (86, 68), (96, 65), (99, 72), (97, 91), (90, 98), (79, 93), (75, 80), (79, 68)])
shirt_shape = polygon_mask(size, [(52, 40), (70, 40), (75, 46), (79, 61), (76, 77), (70, 86), (52, 85), (47, 67)])
jeans_shape = polygon_mask(size, [(43, 75), (80, 76), (88, 102), (88, 160), (84, 175), (72, 176), (57, 170), (43, 175), (40, 146), (41, 98)])
jacket_shape = polygon_mask(size, [(34, 37), (75, 36), (91, 42), (97, 61), (93, 83), (84, 95), (74, 92), (63, 94), (48, 93), (36, 99), (30, 79), (32, 55)])
shoe_shape = polygon_mask(size, [(42, 172), (104, 172), (106, 187), (41, 188)])
feature_mask = polygon_mask(size, [(62, 19), (75, 19), (76, 24), (72, 25), (71, 30), (67, 30), (64, 25), (61, 23)])

layers = {name: Image.new("RGBA", size, (0, 0, 0, 0)) for name in PARTS}
assignments: Counter[str] = Counter()

for y in range(size[1]):
    for x in range(size[0]):
        pixel = seed.getpixel((x, y))
        if pixel[3] == 0:
            continue
        rgb = pixel[:3]
        inside = lambda mask: mask.getpixel((x, y)) != 0

        if inside(shoe_shape) or y >= 172:
            part = "Shoes"
        elif inside(feature_mask) and rgb in FEATURE_COLORS:
            part = "Facial features"
        elif inside(skin_mask) and rgb in SKIN and (y <= 40 or rgb in {(0xF5, 0xA1, 0x72), (0xBF, 0x99, 0x8A), (0xAA, 0x83, 0x78)}):
            part = "Face, neck, hands"
        elif inside(tote_shape) and (rgb in PALE or rgb in {(0x68, 0x60, 0x3C), (0x3F, 0x43, 0x44), (0x2F, 0x36, 0x40)}):
            part = "Tote and strap"
        elif inside(shirt_shape) and rgb in PALE:
            part = "Shirt"
        elif inside(jeans_shape) and y >= 75:
            part = "Jeans"
        elif inside(jacket_shape):
            part = "Jacket"
        elif inside(head_mask) and rgb in OLIVE:
            part = "Jacket"
        elif inside(head_mask):
            part = "Hair"
        else:
            part = "Contour details"

        layers[part].putpixel((x, y), pixel)
        assignments[part] += 1

seed_partition = Image.new("RGBA", size, (0, 0, 0, 0))
for part in PARTS:
    seed_partition = Image.alpha_composite(seed_partition, layers[part])
if any(
    seed_partition.getpixel((x, y)) != seed.getpixel((x, y))
    for y in range(size[1])
    for x in range(size[0])
    if seed.getpixel((x, y))[3] != 0
):
    raise SystemExit("Semantic partition does not recompose the source seed")

# Redraw only the small eye and mouth regions. The untouched skin stays on its
# semantic layer, while the new marks remain independently editable above it.
eye_box = (63, 20, 74, 24)
mouth_box = (66, 27, 71, 30)
face_base = (0xF5, 0xA1, 0x72, 255)
for x0, y0, x1, y1 in (eye_box, mouth_box):
    for y in range(y0, y1):
        for x in range(x0, x1):
            if seed.getpixel((x, y))[3] == 0:
                continue
            old_feature = layers["Facial features"].getpixel((x, y))
            if old_feature[3] != 0:
                layers["Facial features"].putpixel((x, y), (0, 0, 0, 0))
                layers["Face, neck, hands"].putpixel((x, y), face_base)

new_marks = {
    # Near eye: a dark upper lid, two compact sclera pixels, and a right-set pupil.
    (63, 20): (0x4C, 0x2A, 0x24, 255),
    (64, 20): (0x4C, 0x2A, 0x24, 255),
    (63, 21): (0xFD, 0xE4, 0xCD, 255),
    (64, 21): (0xFD, 0xE4, 0xCD, 255),
    (65, 21): (0x2D, 0x24, 0x27, 255),
    (64, 22): (0x4C, 0x2A, 0x24, 255),
    # Far eye: smaller and shifted toward the character's rightward gaze.
    (71, 20): (0x4C, 0x2A, 0x24, 255),
    (71, 21): (0xFB, 0xDA, 0xBC, 255),
    (72, 21): (0x2D, 0x24, 0x27, 255),
    # Four warm pixels make a shallow upturned smile rather than a solid mark.
    (67, 28): (0xAA, 0x83, 0x78, 255),
    (68, 29): (0xAA, 0x83, 0x78, 255),
    (69, 29): (0xAA, 0x83, 0x78, 255),
    (70, 28): (0xAA, 0x83, 0x78, 255),
}
for (x, y), color in new_marks.items():
    if seed.getpixel((x, y))[3] == 0:
        raise SystemExit(f"Face mark would fill transparent silhouette at {(x, y)}")
    layers["Facial features"].putpixel((x, y), color)

composite = Image.new("RGBA", size, (0, 0, 0, 0))
for part in PARTS:
    composite = Image.alpha_composite(composite, layers[part])
changed = []
for y in range(size[1]):
    for x in range(size[0]):
        before = seed.getpixel((x, y))
        after = composite.getpixel((x, y))
        if before[3] != after[3]:
            raise SystemExit(f"Face cleanup changed alpha at {(x, y)}")
        if before[3] and before != after:
            changed.append((x, y))
if not set(changed) <= {(x, y) for x0, y0, x1, y1 in (eye_box, mouth_box) for y in range(y0, y1) for x in range(x0, x1)}:
    raise SystemExit("Face cleanup changed pixels outside its documented edit boxes")
if sum(assignments.values()) != sum(1 for value in alpha.getdata() if value):
    raise SystemExit("Semantic partition did not assign every visible seed pixel")

OUTPUT.mkdir(parents=True, exist_ok=True)
composite.save(OUTPUT / "candidate-preview.png")
composite.resize((size[0] * 4, size[1] * 4), Image.Resampling.NEAREST).save(OUTPUT / "candidate-preview-4x.png")
palette = [color for color, _ in Counter(pixel[:3] for pixel in seed.getdata() if pixel[3]).most_common()]
glyphs = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
if len(palette) > len(glyphs):
    raise SystemExit("Palette exceeds grid legend capacity")
legend = {glyphs[i]: f"#{r:02x}{g:02x}{b:02x}" for i, (r, g, b) in enumerate(palette)}
grids = {}
sheet = Image.new("RGB", (len(PARTS) * size[0] * SCALE + (len(PARTS) + 1) * 12, size[1] * SCALE + 44), (238, 238, 234))
draw = ImageDraw.Draw(sheet)
for part_index, part in enumerate(PARTS):
    layer = layers[part]
    safe_name = part.lower().replace(" ", "-").replace(",", "")
    layer.save(OUTPUT / f"{safe_name}.png")
    rows = [
        "".join(glyphs[palette.index(layer.getpixel((x, y))[:3])] if layer.getpixel((x, y))[3] else "." for x in range(size[0]))
        for y in range(size[1])
    ]
    grids[part] = {"kind": "grid", "x": 0, "y": 0, "rows": rows, "legend": legend, "transparent": "skip"}
    x = 12 + part_index * (size[0] * SCALE + 12)
    draw.text((x, 8), part, fill=(24, 26, 31))
    view = Image.alpha_composite(Image.new("RGBA", size, (48, 51, 60, 255)), layer).convert("RGB")
    sheet.paste(view.resize((size[0] * SCALE, size[1] * SCALE), Image.Resampling.NEAREST), (x, 28))

(OUTPUT / "draw-grids.json").write_text(json.dumps(grids, indent=2) + "\n")
sheet.save(OUTPUT / "part-isolation-sheet.png")
metadata = {
    "seed_sha256": hashlib.sha256(SEED_PATH.read_bytes()).hexdigest(),
    "canvas": list(size),
    "parts": dict(assignments),
    "visible_pixels": sum(assignments.values()),
    "palette_colors": len(palette),
    "source_semantic_partition_recomposes_exactly": True,
    "final_alpha_matches_seed": True,
    "changed_pixels_vs_seed": len(changed),
    "changed_xy": [list(point) for point in changed],
    "editable_parts": list(PARTS),
    "mask_basis": "Hand-defined masks follow visible object boundaries in the supplied downsample; source colors and alpha are retained except the documented face cleanup.",
    "face_cleanup": {"eye_box_half_open": list(eye_box), "mouth_box_half_open": list(mouth_box), "new_mark_count": len(new_marks), "new_visible_marks": {f"{x},{y}": f"#{r:02x}{g:02x}{b:02x}" for (x, y), (r, g, b, a) in new_marks.items()}, "alpha_changed": False},
}
(OUTPUT / "manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")
print(json.dumps(metadata, indent=2))
