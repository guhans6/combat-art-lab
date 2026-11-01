"""Deterministically partition the frozen 128x192 seed into reviewed visible parts.

This script does no colour correction or resampling.  The polygons are native-grid
ownership guides reviewed against the frozen seed; each visible pixel is assigned to
the first matching semantic owner. Conservative-guide gaps are assigned to the
nearest already-owned native-grid coordinate; this is declared visible geometry
completion, not an inference of hidden anatomy. The output parts reassemble exactly.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[4]
RUN = ROOT / "docs/experiments/2026-10-30-fullbody-automated-reconstruction"
SEED = RUN / "inputs/source-only-converted-seed.png"
OUT = RUN / "masks"

# Each outline is a visible, source-grid ownership guide, not hidden anatomy.
# Order is front-to-back only where guides overlap; the result is disjoint.
REGIONS = [
    ("08-hair-tie-and-hair", [(35, 12), (43, 8), (49, 5), (64, 5), (76, 9),
      (84, 16), (82, 27), (77, 35), (69, 37), (58, 35), (53, 31), (48, 38),
      (39, 36), (33, 30), (32, 21)]),
    ("07-face-and-neck", [(57, 16), (69, 14), (76, 18), (77, 26), (73, 34),
      (69, 38), (70, 42), (61, 43), (58, 37), (54, 31), (54, 22)]),
    ("06a-left-hand", [(40, 66), (49, 67), (52, 72), (50, 78), (44, 80),
      (39, 75)]),
    ("06b-right-hand", [(70, 66), (79, 66), (82, 72), (78, 79), (72, 78),
      (69, 73)]),
    ("05-tote-strap", [(73, 37), (79, 38), (82, 63), (83, 74), (78, 76),
      (76, 57)]),
    ("04-tote", [(79, 69), (91, 69), (98, 78), (98, 94), (93, 102), (83, 100),
      (78, 88)]),
    ("03-shirt", [(55, 40), (71, 40), (75, 51), (72, 69), (54, 69), (51, 55)]),
    ("02a-jacket-left", [(41, 35), (56, 35), (60, 44), (57, 58), (55, 72),
      (50, 78), (41, 73), (36, 61), (37, 44)]),
    ("02b-jacket-right", [(70, 36), (82, 38), (92, 48), (96, 61), (93, 72),
      (85, 78), (77, 74), (73, 61), (75, 47)]),
    ("01-denim", [(47, 69), (78, 69), (87, 82), (91, 112), (96, 153),
      (91, 169), (78, 172), (70, 154), (65, 113), (61, 113), (59, 152),
      (54, 172), (42, 169), (40, 147), (42, 102), (43, 80)]),
    ("00-shoes", [(39, 165), (57, 166), (65, 174), (65, 183), (36, 183),
      (31, 178), (33, 172), (78, 165), (96, 166), (107, 176), (107, 183),
      (77, 183), (72, 176)]),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    seed = Image.open(SEED).convert("RGBA")
    if seed.size != (128, 192):
        raise SystemExit(f"unexpected seed size: {seed.size}")
    alpha = seed.getchannel("A")
    allocated = Image.new("L", seed.size)
    manifest: dict[str, object] = {"seed_sha256": sha256(SEED), "size": list(seed.size),
        "precedence": [name for name, _ in REGIONS], "parts": []}
    for name, polygon in REGIONS:
        guided = Image.new("L", seed.size)
        ImageDraw.Draw(guided).polygon(polygon, fill=255)
        mask = Image.new("L", seed.size)
        # A pixel belongs to the first guide that reaches it, always retaining seed alpha.
        mask.putdata([255 if a and g and not old else 0 for a, g, old in zip(alpha.getdata(), guided.getdata(), allocated.getdata())])
        allocated = Image.frombytes("L", seed.size, bytes(max(a, b) for a, b in zip(allocated.getdata(), mask.getdata())))
        part = Image.new("RGBA", seed.size)
        part.paste(seed, (0, 0), mask)
        part.save(OUT / f"{name}.png")
        mask.save(OUT / f"{name}-mask.png")
        manifest["parts"].append({"name": name, "polygon": polygon,
            "visible_pixels": sum(1 for v in mask.getdata() if v), "file": f"{name}.png"})
    # Complete only conservative-guide gaps. Each completed pixel remains in an
    # editable visible body/material part, rather than becoming an arbitrary residue.
    owner_masks = {entry["name"]: Image.open(OUT / (entry["name"] + "-mask.png")).convert("L") for entry in manifest["parts"]}
    owner_points = {name: [(x, y) for y in range(seed.height) for x in range(seed.width)
        if mask.getpixel((x, y))] for name, mask in owner_masks.items()}
    inferred = {name: 0 for name in owner_masks}
    for y in range(seed.height):
        for x in range(seed.width):
            if not alpha.getpixel((x, y)) or allocated.getpixel((x, y)):
                continue
            name = min(owner_points, key=lambda n: min((x - px) ** 2 + (y - py) ** 2 for px, py in owner_points[n]))
            owner_masks[name].putpixel((x, y), 255)
            inferred[name] += 1
    for entry in manifest["parts"]:
        name = entry["name"]
        mask = owner_masks[name]
        part = Image.new("RGBA", seed.size)
        part.paste(seed, (0, 0), mask)
        part.save(OUT / entry["file"])
        mask.save(OUT / (name + "-mask.png"))
        entry["visible_pixels"] = sum(1 for v in mask.getdata() if v)
    # Reassemble visible samples from the generated parts.  Transparent RGB is not
    # observable through normal compositing, so preserve the source's hidden RGB in
    # the evidence composite explicitly rather than pretending a transparent blit
    # retains it.  The actual native proof separately compares alpha and visible RGB.
    part_images = [Image.open(OUT / entry["file"]).convert("RGBA") for entry in manifest["parts"]]
    reconstructed = list(seed.getdata())
    for i, source_pixel in enumerate(seed.getdata()):
        if source_pixel[3]:
            for part_image in part_images:
                candidate = part_image.getdata()[i]
                if candidate[3]:
                    reconstructed[i] = candidate
                    break
    composite = Image.new("RGBA", seed.size)
    composite.putdata(reconstructed)
    composite.save(OUT / "automatic-composite.png")
    if composite.tobytes() != seed.tobytes():
        raise SystemExit("part composite does not equal the frozen seed")
    if sum(entry["visible_pixels"] for entry in manifest["parts"]) != sum(1 for v in alpha.getdata() if v):
        raise SystemExit("visible ownership coverage failed")
    manifest["automatic_composite_sha256"] = sha256(OUT / "automatic-composite.png")
    manifest["decoded_rgba_sha256"] = hashlib.sha256(composite.tobytes()).hexdigest()
    manifest["coverage"] = {entry["name"]: entry["visible_pixels"] for entry in manifest["parts"]}
    manifest["inferred_boundary_pixels"] = inferred
    (OUT / "ownership-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"status": "pass", "visible_pixels": sum(manifest["coverage"].values()),
        "inferred_boundary_pixels": sum(inferred.values()), "decoded_rgba_sha256": manifest["decoded_rgba_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
