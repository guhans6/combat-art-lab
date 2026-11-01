"""Render a faithful, presentation-only view of E0's prepared layers."""
from pathlib import Path
from hashlib import sha256
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "run-a/replay-2"
PREPARED = RUN / "prepared"
ORDER = [
    "01-jacket", "02-shirt", "03-neck-ear", "04-rear-hair", "05-face",
    "06-crown-fringe", "07-hair-tie", "08-eyes-brows", "09-mouth",
]
SCALE = 3
CANVAS = (120, 112)
PANEL = (400, 410)
SHEET = (4 * PANEL[0] + 40, 3 * PANEL[1] + 100)
OUT = ROOT / "nine-layers-and-composite.png"
REPORT = ROOT / "nine-layers-and-composite-check.json"


def checkerboard(size):
    image = Image.new("RGB", size, "#2e3440")
    draw = ImageDraw.Draw(image)
    cell = 12
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if ((x // cell) + (y // cell)) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill="#46505d")
    return image


def visible_and_alpha_equal(left, right):
    for a, b in zip(left.get_flattened_data(), right.get_flattened_data()):
        if a[3] != b[3] or (a[3] and a[:3] != b[:3]):
            return False
    return True


parts = [Image.open(PREPARED / f"{name}.png").convert("RGBA") for name in ORDER]
if any(part.size != CANVAS for part in parts):
    raise ValueError("prepared parts must retain the frozen 120x112 canvas")

composite = Image.new("RGBA", CANVAS)
for part in parts:
    composite.alpha_composite(part)
native = Image.open(RUN / "b00-separated-seed.png").convert("RGBA")
if not visible_and_alpha_equal(composite, native):
    raise ValueError("prepared layer composite does not match native B00 visible pixels/alpha")

sheet = Image.new("RGB", SHEET, "#171b22")
draw = ImageDraw.Draw(sheet)
draw.text((20, 20), "E0: nine extracted semantic layers + native B00 composite", fill="white")
draw.text((20, 46), "Each panel is the original 120x112 canvas, displayed at 3x nearest-neighbour.", fill="#c7d2de")

def add_panel(index, label, image, detail):
    col, row = index % 4, index // 4
    x, y = 20 + col * PANEL[0], 82 + row * PANEL[1]
    draw.rounded_rectangle((x, y, x + 380, y + 390), radius=8, fill="#202632", outline="#596675")
    draw.text((x + 12, y + 12), label, fill="white")
    draw.text((x + 12, y + 32), detail, fill="#c7d2de")
    scaled = image.resize((CANVAS[0] * SCALE, CANVAS[1] * SCALE), Image.Resampling.NEAREST)
    panel_bg = checkerboard(scaled.size)
    panel_bg.paste(scaled, (0, 0), scaled)
    sheet.paste(panel_bg, (x + 10, y + 58))
    draw.rectangle((x + 10, y + 58, x + 370, y + 394), outline="#78899b")

for i, (name, part) in enumerate(zip(ORDER, parts)):
    add_panel(i, name, part, "prepared semantic layer")
add_panel(9, "B00 composite", native, "actual native export")

sheet.save(OUT)
report = {
    "schema": 1,
    "presentation_only": True,
    "source_run": "run-a/replay-2",
    "order": ORDER,
    "scale": SCALE,
    "layer_canvas": list(CANVAS),
    "sheet": OUT.name,
    "native_b00": "run-a/replay-2/b00-separated-seed.png",
    "visible_rgb_and_alpha_match": True,
    "parts_sha256": {
        name: sha256((PREPARED / f"{name}.png").read_bytes()).hexdigest()
        for name in ORDER
    },
    "native_b00_sha256": sha256((RUN / "b00-separated-seed.png").read_bytes()).hexdigest(),
    "sheet_sha256": sha256(OUT.read_bytes()).hexdigest(),
}
REPORT.write_text(json.dumps(report, indent=2) + "\n")
print(f"PASS: {OUT} — prepared composite equals native B00 visible pixels and alpha")
