"""Source sampling only: no AI, painting, palette reduction or smoothing."""
import hashlib
import json
from collections import deque
from pathlib import Path
from PIL import Image, __version__

ROOT = Path(__file__).resolve().parent
source = Image.open(ROOT / 'original.png').convert('RGBA')
# The supplied backdrop is muted pink-brown. Keep source RGB untouched.
# Explicit color mask, inspected on the full source and contrasting mattes.
def background(p):
    r, g, b, _ = p
    return 100 <= r <= 155 and 80 <= g <= 135 and 80 <= b <= 135 and 15 <= r-g <= 36 and abs(g-b) <= 7

w, h = source.size
pending = bytearray(background(p) for p in source.getdata())
alpha = bytearray([255]) * (w*h)
removed_components = []
for i in range(w*h):
    if not pending[i]:
        continue
    queue = deque([i]); pending[i] = 0; component = []
    touches_edge = False
    while queue:
        j = queue.popleft(); component.append(j)
        x, y = j % w, j // w
        touches_edge |= x in (0,w-1) or y in (0,h-1)
        neighbors = ([j-1] if x else []) + ([j+1] if x<w-1 else []) + ([j-w] if y else []) + ([j+w] if y<h-1 else [])
        for k in neighbors:
            if pending[k]: pending[k] = 0; queue.append(k)
    # Visually reviewed: the three large enclosed backdrop components are
    # the blade opening and two arm-cage openings. Small shoulder-metal
    # flecks share backdrop colors and must remain opaque.
    if touches_edge or len(component) >= 200:
        for j in component: alpha[j] = 0
        removed_components.append(len(component))
mask = Image.frombytes('L',source.size,bytes(alpha))
mask.save(ROOT / 'foreground-mask.png')
bounds = mask.getbbox()
source.putalpha(mask)
crop = source.crop(bounds)
height = 64
size = (round(crop.width * height / crop.height), height)
sample = crop.resize(size, Image.Resampling.NEAREST)
canvas = Image.new('RGBA', (128, 80))
offset = ((128-size[0])//2, 8)
canvas.paste(sample, offset)
points = [{'x': x, 'y': y, 'color': '#%02x%02x%02x' % canvas.getpixel((x,y))[:3]}
          for y in range(80) for x in range(128) if canvas.getpixel((x,y))[3]]
(ROOT / 'pixels.json').write_text(json.dumps(points))
colors = sorted(set(p['color'] for p in points))
(ROOT / 'palette.json').write_text(json.dumps(colors))
for name, bg in [('light',(220,225,225,255)),('dark',(28,32,40,255))]:
    matte = Image.new('RGBA',canvas.size,bg)
    matte.alpha_composite(canvas)
    matte.resize((768,480),Image.Resampling.NEAREST).save(ROOT / ('review-'+name+'.png'))
source.thumbnail((768,512),Image.Resampling.NEAREST)
check = Image.new('RGBA',source.size,(40,180,190,255))
check.alpha_composite(source)
check.save(ROOT / 'mask-review.png')
report = dict(source_sha256=hashlib.sha256((ROOT/'original.png').read_bytes()).hexdigest(),
    pillow=__version__, source_size=[1536,1024], source_bounds=bounds,
    canvas=[128,80], sampled_size=size, offset=offset, visible_bounds=canvas.getbbox(),
    visible_height=canvas.getbbox()[3]-canvas.getbbox()[1], opaque_pixels=len(points),
    colors=len(colors), removed_components=removed_components, rgba_sha256=hashlib.sha256(canvas.tobytes()).hexdigest(),
    filter='nearest-neighbor', ai_corrections=False, quantization=False,
    scale_status='Provisional 64px visible height; exact RCG2 dimensions unverified')
(ROOT/'recipe.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
