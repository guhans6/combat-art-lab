from tools.check_native_pilot import read
from PIL import Image
from pathlib import Path
from collections import defaultdict
import hashlib,json
P=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol/reddit-motion-study/prototype');B=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol/pass01.aseprite');a=read(B)
# One-pixel common upper-mass rise, taper into fixed waist/pocketed hands.
# F2 chest motion stops at62, F3 fills the lower ribcage transition through66.
# Outer forearms stay relaxed: taper earlier than the central ribcage.
def stop(x,frame):
 if 47<=x<=74:return 62 if frame==1 else 66
 if 43<=x<=46 or 75<=x<=80:return 61
 if 39<=x<=42 or 81<=x<=85:return 59
 return 57
ops=[];mask=Image.new('L',(128,192));frames=[]
for f in range(8):
 ims=[a['cels'][(f,l)]['image'].copy()for l in range(12)]
 if f in [1,2,3]:
  for l in [3,4,5,7,10,11]:
   # All moving visible native owners read the same neutral field, so neck/head/collar
   # registration remains exact instead of lifting only the garment.
   src=a['cels'][(0,l)]['image'];dst=src.copy()
   if f in [1,2]:
    for x in range(128):
     for y in range(stop(x,f)+1):dst.putpixel((x,y),src.getpixel((x,y+1)))
   old=ims[l];ims[l]=dst;groups=defaultdict(list)
   for y in range(192):
    for x in range(128):
     c=dst.getpixel((x,y))
     if c!=old.getpixel((x,y)):
      mask.putpixel((x,y),255);groups['#%02x%02x%02x%02x'%c].append({'x':x,'y':y})
   if groups:ops.append({'frame':f+1,'layer':a['layers'][l]['name'],'paletteLock':False,'ops':[{'kind':'pixels','color':c,'points':pts}for c,pts in groups.items()]})
 im=Image.new('RGBA',(128,192))
 for l in range(1,12):im.alpha_composite(ims[l])
 frames.append(im)
(P/'proof/operations.json').write_text(json.dumps(ops,separators=(',',':'))+'\n');mask.save(P/'proof/allowed-mask.png')
inputs=[B,Path('docs/experiments/2026-10-30-natural-idle-sol/pass01.aseprite'),*Path('assets/references/approved-2026-10-26').glob('character-*.png')]
(P/'proof/input-hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in inputs},indent=2)+'\n')
print([(o['frame'],o['layer'],sum(len(v['points'])for v in o['ops']))for o in ops])
