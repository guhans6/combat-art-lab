"""Display existing contestant exports unchanged; no candidate artwork is edited."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
spec = [('Luna 5.6 Max: first', 'trial-a', 'pass-01'),
        ('Luna 5.6 Max: final', 'trial-a', 'pass-02'),
        ('Luna 6 Max: first', 'trial-b', 'pass-01'),
        ('Luna 6 Max: final', 'trial-b', 'pass-03')]
sheet = Image.new('RGB', (1640, 1000), '#242830')
draw = ImageDraw.Draw(sheet)
draw.text((20, 15), 'Independent image-to-sprite trials: unchanged exports, identical display sizes', fill='white')
draw.text((20, 38), 'Top: actual 128x192. Bottom: 3x nearest-neighbor. Each trial chose its own preparation and palette.', fill='white')
checks = []
for i, (title, trial, name) in enumerate(spec):
    p = root / trial / 'passes' / (name + '.png')
    im = Image.open(p).convert('RGBA')
    assert im.size == (128, 192)
    x = 20 + i * 405
    draw.text((x, 68), title, fill='white')
    for scale, y in [(1, 95), (3, 350)]:
        tile = Image.new('RGBA', (128, 192), '#353b43')
        td = ImageDraw.Draw(tile)
        for yy in range(0, 192, 8):
            for xx in range(0, 128, 8):
                if ((xx//8) + (yy//8)) % 2:
                    td.rectangle((xx, yy, xx+7, yy+7), fill='#414953')
        tile.alpha_composite(im)
        tile = tile.convert('RGB').resize((128*scale, 192*scale), Image.Resampling.NEAREST)
        sheet.paste(tile, (x, y))
    checks.append({'artifact': str(p.relative_to(root)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'size': list(im.size), 'alpha_extrema': list(im.getchannel('A').getextrema())})
sheet.save(root / 'supervisor-comparison.png')
for trial, name in [('trial-a', 'pass-02'), ('trial-b', 'pass-03')]:
    p = root / trial / 'passes'
    reopened = p / (name + '-reopen.png')
    if not reopened.exists():
        reopened = p / (name + '-reopened.png')
    if reopened.exists():
        assert Image.open(p / (name + '.png')).convert('RGBA').tobytes() == Image.open(reopened).convert('RGBA').tobytes()
        checks.append({'trial': trial, 'fresh_reopen_rgba_equal': True, 'reopen_path': str(reopened.relative_to(root))})
(root / 'supervisor-display-checks.json').write_text(json.dumps(checks, indent=2) + '\n')
print(json.dumps(checks, indent=2))
