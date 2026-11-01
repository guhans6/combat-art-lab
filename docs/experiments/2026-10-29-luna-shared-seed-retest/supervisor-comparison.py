"""Review-only display of exact existing exports; no contestant art modifications."""
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
items = [
    ('Shared sharp seed', 'shared/source-only-converted-seed.png'),
    ('5.6 Max: candidate for user review', 'trial-a/passes/pass-03.png'),
    ('6 Max: rejected, none selected', 'trial-b/pass-01/character-pass-01.png'),
]
sheet = Image.new('RGB', (1240, 1230), '#242830')
draw = ImageDraw.Draw(sheet)
draw.text((15, 15), 'Same-seed retest: exact exports on neutral matte; 1x / 3x / head at 8x', fill='white')
for i, (title, relative) in enumerate(items):
    image = Image.open(root / relative).convert('RGBA')
    assert image.size == (128, 192)
    matte = Image.new('RGBA', image.size, '#414953')
    matte.alpha_composite(image)
    matte = matte.convert('RGB')
    x = 15 + 410 * i
    draw.text((x, 45), title, fill='white')
    sheet.paste(matte, (x, 70))
    sheet.paste(matte.resize((384, 576), Image.Resampling.NEAREST), (x, 290))
    sheet.paste(matte.crop((40, 10, 80, 42)).resize((320, 256), Image.Resampling.NEAREST), (x, 900))
sheet.save(root / 'supervisor-comparison.png')
