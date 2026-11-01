"""Produce a nearest-neighbour ownership diagnostic; no art pixels are changed."""
from pathlib import Path
from PIL import Image, ImageDraw

RUN = Path(__file__).resolve().parents[1]
MASKS = RUN / "masks"
COLORS = {
    "00-shoes": "#d9c2a1", "01-denim": "#5d88c8", "02-jacket": "#6c7844",
    "03-shirt": "#f6e5d3", "04-tote": "#f3bb9a", "05-tote-strap": "#ef7095",
    "06a-left-hand": "#fb9d69", "06b-right-hand": "#e95e52",
    "07-face-and-neck": "#f4c24c", "08-hair-tie-and-hair": "#79472d",
}
canvas = Image.new("RGBA", (128, 192))
for name, color in COLORS.items():
    mask = Image.open(MASKS / f"{name}-mask.png").convert("L")
    canvas.paste(Image.new("RGBA", canvas.size, color), (0, 0), mask)
out = canvas.resize((512, 768), Image.Resampling.NEAREST)
draw = ImageDraw.Draw(out)
draw.rectangle((0, 0, 512, 112), fill="#111111")
for index, (name, color) in enumerate(COLORS.items()):
    x = 8 + (index % 2) * 250
    y = 6 + (index // 2) * 20
    draw.rectangle((x, y, x + 10, y + 10), fill=color)
    draw.text((x + 15, y), name, fill="white")
out.save(MASKS / "ownership-review-4x.png")

# Coordinate aid for correcting visible-mask ownership against the frozen control.
seed = Image.open(RUN / "inputs/source-only-converted-seed.png").convert("RGBA").resize((512, 768), Image.Resampling.NEAREST)
grid = ImageDraw.Draw(seed)
for x in range(0, 128, 10):
    grid.line((x * 4, 0, x * 4, 768), fill="#00ffff", width=1)
    grid.text((x * 4 + 1, 1), str(x), fill="white")
for y in range(0, 192, 10):
    grid.line((0, y * 4, 512, y * 4), fill="#00ffff", width=1)
    grid.text((1, y * 4 + 1), str(y), fill="white")
seed.save(MASKS / "seed-coordinate-review-4x.png")
