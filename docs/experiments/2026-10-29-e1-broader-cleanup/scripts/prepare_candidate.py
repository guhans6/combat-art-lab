"""Deterministic E1-v2 clothing-only material mapping; no source is overwritten."""
from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PREPARED = ROOT / "prepared"
OUT = ROOT / "candidate-parts"
OUT.mkdir(exist_ok=True)
names = ["01-jacket", "02-shirt", "03-neck-ear", "04-rear-hair", "05-face", "06-crown-fringe", "07-hair-tie", "08-eyes-brows", "09-mouth"]
jacket_ramp = [(60,53,44), (65,59,53), (86,74,53), (95,74,52), (95,75,57)]
shirt_ramp = [(198,152,132), (220,170,138), (229,179,125)]
changed = {}

def nearest_by_luma(rgb, ramp):
    lum = sum(rgb) / 3
    return min(ramp, key=lambda c: abs(sum(c) / 3 - lum))

for name in names:
    image = Image.open(PREPARED / f"{name}.png").convert("RGBA")
    before = list(image.get_flattened_data())
    after = before[:]
    if name == "01-jacket":
        for i, (r,g,b,a) in enumerate(before):
            if a and 45 <= r <= 110 and 40 <= g <= 95 and 30 <= b <= 70:
                after[i] = (*nearest_by_luma((r,g,b), jacket_ramp), a)
    elif name == "02-shirt":
        for i, (r,g,b,a) in enumerate(before):
            if a and r >= 150 and g >= 95 and b >= 65:
                after[i] = (*nearest_by_luma((r,g,b), shirt_ramp), a)
    result = Image.new("RGBA", image.size)
    result.putdata(after)
    result.save(OUT / f"{name}.png")
    changed[name] = sum(a != b for a, b in zip(before, after))

report = {
    "schema": 1,
    "mode": "warnings-first deterministic material mapping",
    "warnings": "Mapping is a candidate comparison, never an automatic cleanup instruction.",
    "ramps": {"jacket": jacket_ramp, "shirt": shirt_ramp},
    "changed_pixels_by_layer": changed,
    "changed_total": sum(changed.values())
}
(ROOT / "mapping-report.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report))
