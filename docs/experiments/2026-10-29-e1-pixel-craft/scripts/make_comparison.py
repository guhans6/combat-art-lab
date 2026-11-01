"""Make E1 review images only; it does not change art."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
original = Image.open(ROOT / "inputs/original-crop.png").convert("RGB")
control = Image.open(ROOT / "inputs/control-a.png").convert("RGBA")
candidate = Image.open(ROOT / "outputs/candidate-b-normalized.png").convert("RGBA")
canvas = Image.new("RGB", (1520, 1160), "#1b2029")
draw = ImageDraw.Draw(canvas)

def checkerboard(size):
    bg = Image.new("RGB", size, "#323b48")
    d = ImageDraw.Draw(bg)
    for y in range(0, size[1], 16):
        for x in range(0, size[0], 16):
            if ((x // 16) + (y // 16)) % 2:
                d.rectangle((x, y, x + 15, y + 15), fill="#485463")
    return bg

def paste_rgba(image, pos, scale=1):
    if scale != 1:
        image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
    bg = checkerboard(image.size)
    bg.paste(image, (0, 0), image)
    canvas.paste(bg, pos)
    draw.rectangle((pos[0], pos[1], pos[0] + image.width - 1, pos[1] + image.height - 1), outline="#8291a3")

draw.text((20, 16), "E1: source / frozen Control A / scoped Candidate B", fill="white")
draw.text((20, 36), "Candidate changes only four existing-colour jacket pixels; no face, hair, alpha, palette, frame, or layer-structure change.", fill="#cbd5e1")
canvas.paste(original, (20, 72))
draw.text((20, 530), "Approved original crop, source pixels (480x448)", fill="white")
paste_rgba(control, (540, 72))
draw.text((540, 196), "Control A, actual 1x (120x112)", fill="white")
paste_rgba(candidate, (700, 72))
draw.text((700, 196), "Candidate B, actual 1x (120x112)", fill="white")

paste_rgba(control, (20, 570), 4)
paste_rgba(candidate, (540, 570), 4)
draw.text((20, 1038), "Control A, 4x nearest-neighbour", fill="white")
draw.text((540, 1038), "Candidate B, 4x nearest-neighbour", fill="white")

box = (24, 86, 38, 98)
for image, x, label in ((control, 1060, "Control A altered-region callout"), (candidate, 1280, "Candidate B altered-region callout")):
    crop = image.crop(box).resize((168, 144), Image.Resampling.NEAREST)
    bg = checkerboard(crop.size)
    bg.paste(crop, (0, 0), crop)
    canvas.paste(bg, (x, 570))
    draw.rectangle((x, 570, x + 167, 713), outline="#8ee3c8")
    draw.text((x, 724), label, fill="white")
    draw.text((x, 742), "four stepped pixels", fill="#cbd5e1")
canvas.save(ROOT / "source-control-candidate-comparison.png")
