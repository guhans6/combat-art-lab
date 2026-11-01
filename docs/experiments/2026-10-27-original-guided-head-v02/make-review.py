"""Original/prior/new sheet: display evidence only; native sources stay separate."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
entries = [
    (ROOT / 'assets/references/approved-2026-10-26/character-closeup.png', (380, 64, 860, 512), 1,
     'APPROVED ORIGINAL', '480x448 crop; no resizing'),
    (HERE / 'baseline.png', None, 4, 'PRIOR REJECTED STUDY', '120x112 native; nearest-neighbor 4x'),
    (HERE / 'pass-03-refined.png', None, 4, 'NEW PROVISIONAL REVISION', '120x112 native; nearest-neighbor 4x'),
]
canvas = Image.new('RGB', (1488, 560), '#30303e')
draw = ImageDraw.Draw(canvas)
metadata = []
for index, (path, box, zoom, title, label) in enumerate(entries):
    with Image.open(path) as image:
        native_size = image.size
        cropped = image.convert('RGBA').crop(box) if box else image.convert('RGBA')
    displayed = cropped.resize((cropped.width * zoom, cropped.height * zoom), Image.Resampling.NEAREST)
    assert displayed.size == (480, 448)
    x = index * 496 + 8
    draw.text((x, 12), title, fill='white')
    draw.text((x, 32), label, fill='white')
    canvas.paste(displayed, (x, 64), displayed)
    metadata.append({'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                     'native_size': list(native_size), 'crop': box, 'display_zoom': zoom})
draw.text((8, 532), 'Fixed crop/framing. New artwork is not user-approved; no production-grid or Godot claim.', fill='white')
out = HERE / 'original-prior-new.png'
assert not out.exists() and not out.with_suffix('.json').exists(), 'Preserve evidence; choose new output names.'
canvas.save(out)
out.with_suffix('.json').write_text(json.dumps(metadata, indent=2) + '\n')
print(out)
