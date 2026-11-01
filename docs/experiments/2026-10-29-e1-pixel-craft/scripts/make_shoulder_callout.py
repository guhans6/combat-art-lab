"""Display-only source/control shoulder-plane hypothesis callout."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
source = Image.open(ROOT / "inputs/original-crop.png").convert("RGB")
control = Image.open(ROOT / "inputs/control-a.png").convert("RGBA")
# E1 hypothesis bounds on the 120x112 grid, shown against the mapped 4x original.
box = (20, 80, 120, 112)
source_patch = source.crop(tuple(v * 4 for v in box))
control_patch = control.crop(box).resize(source_patch.size, Image.Resampling.NEAREST)
canvas = Image.new("RGB", (source_patch.width * 2 + 60, source_patch.height + 90), "#202630")
draw = ImageDraw.Draw(canvas)
canvas.paste(source_patch, (20, 50))
canvas.paste(control_patch, (40 + source_patch.width, 50), control_patch)
draw.text((20, 16), "E1 inspection callout — source crop (left) vs frozen B00 Control A at 4x (right)", fill="white")
draw.text((20, 34), "Hypothesis only: shoulder-plane separation; face and hair are not in scope.", fill="#c7d2de")
draw.rectangle((20 + (29 - 20) * 4, 50 + (91 - 80) * 4, 20 + (32 - 20 + 1) * 4 - 1, 50 + (92 - 80 + 1) * 4 - 1), outline="#8ee3c8", width=2)
right = 40 + source_patch.width
draw.rectangle((right + (29 - 20) * 4, 50 + (91 - 80) * 4, right + (32 - 20 + 1) * 4 - 1, 50 + (92 - 80 + 1) * 4 - 1), outline="#8ee3c8", width=2)
draw.rectangle((right + (91 - 20) * 4, 50 + (85 - 80) * 4, right + (95 - 20 + 1) * 4 - 1, 50 + (87 - 80 + 1) * 4 - 1), outline="#8ee3c8", width=2)
canvas.save(ROOT / "source-control-shoulder-hypothesis.png")
