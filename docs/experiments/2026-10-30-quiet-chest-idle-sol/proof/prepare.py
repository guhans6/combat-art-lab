from tools.check_native_pilot import read
from PIL import Image,ImageDraw
from pathlib import Path
from collections import defaultdict
import json,hashlib
P=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol');B=Path('docs/experiments/2026-10-30-natural-idle-sol/pass01.aseprite');a=read(B)
base=[a['cels'][(0,l)]['image'].copy() for l in range(12)]; editable=[3,4,5,7]
def compose(ims):
 im=Image.new('RGBA',(128,192))
 for l in range(1,12):im.alpha_composite(ims[l])
 return im
orig=compose(base)
# Hard registration: keep fixed rest shoulder/sleeve contour, collar, head and waist.
# Only internal front chest/open-jacket plane gets a one-pixel forward bow.
# Peak cloth fold is lifted by one pixel as the shirt grows taut over the ribcage.
def displacement(stage,x,y):
 dx=dy=0
 if stage==1:
  if 55<=x<=70 and 50<=y<=57:dx=1
  if 48<=x<=67 and 56<=y<=61:dy=-1
 elif stage==2:
  if 53<=x<=71 and 47<=y<=61:dx=1
  if 47<=x<=68 and 53<=y<=64:dy=-1
 elif stage==3:
  if 55<=x<=70 and 51<=y<=58:dx=1
  if 48<=x<=67 and 58<=y<=63:dy=-1
 return dx,dy
ops=[];mask=Image.new('L',(128,192));pose=[]
for f,stage in [(1,1),(2,2),(3,3)]:
 ims=[a['cels'][(f,l)]['image'].copy()for l in range(12)]
 for l in editable:ims[l]=base[l].copy() # undo inherited hoist on actual garment owners
 for y in range(44,67):
  for x in range(46,73):
   dx,dy=displacement(stage,x,y)
   if not(dx or dy):continue
   # This region is interior garment: no source skin/hair or outer alpha contour.
   for l in editable:ims[l].putpixel((x,y),base[l].getpixel((x-dx,y-dy)))
 for l in editable:
  old=a['cels'][(f,l)]['image'];new=ims[l];groups=defaultdict(list)
  for y in range(192):
   for x in range(128):
    c=new.getpixel((x,y))
    if c!=old.getpixel((x,y)):
     mask.putpixel((x,y),255);groups['#%02x%02x%02x%02x'%c].append({'x':x,'y':y})
  if groups:ops.append({'frame':f+1,'layer':a['layers'][l]['name'],'paletteLock':False,'ops':[{'kind':'pixels','color':c,'points':pts}for c,pts in groups.items()]})
 pose.append(compose(ims))
(P/'proof/operations.json').write_text(json.dumps(ops,indent=2)+'\n');mask.save(P/'proof/allowed-mask.png')
inputs=[B,*Path('assets/references/approved-2026-10-26').glob('character-*.png'),Path('docs/experiments/2026-10-30-idle-breathing-comparison/terra/pass01.aseprite')]
(P/'proof/input-hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in inputs},indent=2)+'\n')
# Planning image only; native delivery will be exported by Aseprite.
out=Image.new('RGB',(4*384,576),(48,50,57));d=ImageDraw.Draw(out)
for i,im in enumerate([orig]+pose):
 bg=Image.new('RGBA',im.size,(48,50,57,255));bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((384,576),Image.Resampling.NEAREST),(i*384,0))
out.save(P/'proof/planning.png')
print([(o['frame'],o['layer'],sum(len(g['points'])for g in o['ops']))for o in ops])
