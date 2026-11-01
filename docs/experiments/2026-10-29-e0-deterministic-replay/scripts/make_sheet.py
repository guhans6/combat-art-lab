from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
original = Image.open(root / "inputs/original-crop-historical.png").convert("RGB")
seed = Image.open(root / "run-a/replay-2/b00-separated-seed.png").convert("RGBA")
bg = Image.new("RGB", (1000, 1160), "#24242d")
draw = ImageDraw.Draw(bg)
draw.text((20, 16), "E0: approved original and deterministic B00 replay", fill="white")
bg.paste(original, (20, 52))
draw.text((20, 510), "Original crop: 1x (480x448)", fill="white")
bg.paste(seed, (540, 52), seed)
draw.text((540, 180), "B00 replay: 1x (120x112)", fill="white")
zoom = seed.resize((480, 448), Image.Resampling.NEAREST)
bg.paste(zoom, (20, 570), zoom)
draw.text((20, 1030), "B00 replay: 4x nearest-neighbour", fill="white")
bg.save(root / "original-b00-1x-4x.png")
