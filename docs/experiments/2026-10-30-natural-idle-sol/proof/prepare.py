from tools.check_native_pilot import read
from PIL import Image,ImageDraw
from pathlib import Path
from collections import defaultdict
import json,hashlib
P=Path('docs/experiments/2026-10-30-natural-idle-sol');B=Path('docs/experiments/2026-10-30-idle-breathing-comparison/terra/pass01.aseprite');a=read(B)
editable=[3,4,5,7]
base=[a['cels'][(0,l)]['image'].copy() for l in range(12)]
def compose(ims):
 out=Image.new('RGBA',(128,192))
 for l,im in enumerate(ims):
  if a['layers'][l]['flags']&1:out.alpha_composite(im)
 return out
orig=compose(base)
# Exact composite ownership; only garment fields and transparent shoulder extension.
owner={}
for y in range(192):
 for x in range(128):
  own=-1
  for l in range(1,12):
   if base[l].getpixel((x,y))[3]:own=l
  owner[x,y]=own
# Cloth colors include olive planes, pale shirt and cream strap. Skin/hair marks
# misowned by garment layers stay fixed; garment motion never crosses them.
def cloth(c):
 r,g,b,alpha=c
 return alpha and ((r<150 and g>r*.70 and b<g*.95) or (r>175 and abs(r-g)<65 and abs(g-b)<65))
def safe(x,y):
 return 31<=x<96 and 34<=y<69 and (owner[x,y]==-1 or owner[x,y] in editable and cloth(orig.getpixel((x,y))))
ops=[];previews=[]
for frame,stage in [(1,1),(2,2),(3,1)]:
 ims=[im.copy() for im in base]
 # A single coherent vertical displacement field across actual owners. No x warp.
 # Peak lifts upper garment 2px; lower sleeve and waist are stable.
 for l in editable:
  src=base[l];dst=ims[l]
  for y in range(34,69):
   lift=stage if y<50 else (1 if stage==2 and y<60 else 0)
   for x in range(31,96):
    if not safe(x,y):continue
    sy=y+lift
    c=src.getpixel((x,sy))
    if c[3] and not cloth(c):continue
    # Keep source's skin/hair-bearing border frozen as well.
    if c[3] and owner[x,sy] not in editable:continue
    dst.putpixel((x,y),c)
  # Changes include restoring Terra's horizontal expansion to the neutral shape.
  old=a['cels'][(frame,l)]['image'];groups=defaultdict(list)
  for y in range(192):
   for x in range(128):
    c=dst.getpixel((x,y))
    if c!=old.getpixel((x,y)):
     key='#%02x%02x%02x%02x'%c
     groups[key].append([x,y])
  ops.append({'frame':frame+1,'layer':a['layers'][l]['name'],'ops':[{'kind':'pixels','color':c,'points':pts} for c,pts in groups.items()]})
 comp=compose(ims);comp.save(P/f'proof/planning-{stage}.png');previews.append(comp)
(P/'proof/operations.json').write_text(json.dumps(ops,indent=2)+'\n')
# Exact mask + native baseline provenance are audit inputs.
mask=Image.new('L',(128,192));mask.putdata([255 if safe(x,y) else 0 for y in range(192) for x in range(128)]);mask.save(P/'proof/allowed-mask.png')
(P/'proof/input-hashes.json').write_text(json.dumps({str(B):hashlib.sha256(B.read_bytes()).hexdigest(),**{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('assets/references/approved-2026-10-26').glob('character-*.png')}},indent=2)+'\n')
panels=[orig]+previews
out=Image.new('RGBA',(4*300,400),(48,50,57,255));d=ImageDraw.Draw(out)
for i,im in enumerate(panels):out.alpha_composite(im.crop((26,27,101,114)).resize((300,348),Image.Resampling.NEAREST),(i*300,25));d.text((i*300+5,5),['neutral','rise','peak','settle'][i],fill='white')
out.save(P/'proof/planning-contact.png')
print([(r['frame'],r['layer'],sum(len(o['points']) for o in r['ops'])) for r in ops])
