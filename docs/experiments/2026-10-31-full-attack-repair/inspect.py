from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'))
from native_read import read,composite
old=R.parent/'2026-10-30-tote-attack'
a=read(old/'artist/sol-rescue/source/tote-attack-v03.aseprite')
ims=[composite(a,i) for i in range(13)]
for subset,name,scale in [([0,1,2,5,8,10],'baseline-keys',3),([0,1,2,3,4,5,6,7,8,9,10,11,12],'baseline-all',1)]:
 out=Image.new('RGBA',(320*scale*3,216*scale*((len(subset)+2)//3)),(50,52,55,255));d=ImageDraw.Draw(out)
 for j,i in enumerate(subset):
  x=j%3*320*scale;y=j//3*216*scale
  out.alpha_composite(ims[i].resize((320*scale,192*scale),Image.Resampling.NEAREST),(x,y+24*scale));d.text((x+5,y+5),f'F{i+1}',fill='white')
 out.convert('RGB').save(R/'review'/f'{name}.png')
# Show actual owners for neutral, pickup and recovery without relabelling rectangular masks as anatomy.
out=Image.new('RGBA',(320*3,216*7),(50,52,55,255));d=ImageDraw.Draw(out)
for j,f in enumerate([0,1,8]):
 for l,meta in enumerate(a['layers']):
  if (f,l) in a['cels']:out.alpha_composite(a['cels'][f,l]['image'],(j*320,l*216+24))
  d.text((j*320+5,l*216+5),f'F{f+1} {meta["name"]}',fill='white')
out.convert('RGB').save(R/'review/owners.png')
b=read(R/'scratch/before.aseprite');c=read(R/'scratch/after.aseprite')
changes=[(x,y) for y in range(16) for x in range(16) if composite(b,0).getpixel((x,y))!=composite(c,0).getpixel((x,y))]
assert changes==[(3,2)] and b['cels'][0,1]['image'].tobytes()==c['cels'][0,1]['image'].tobytes()
print('Scratch exact single-pixel change / protected layer PASS',changes)
print(json.dumps([dict(frame=f+1,owners=[(m['name'],a['cels'][f,l]['image'].getbbox()) for l,m in enumerate(a['layers']) if (f,l) in a['cels']]) for f in [0,1,2,5,8,10]],indent=2))
