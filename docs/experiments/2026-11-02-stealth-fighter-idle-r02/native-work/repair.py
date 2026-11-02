from pathlib import Path
from PIL import Image
import json
P=Path('/private/tmp/stealth-fighter-idle-r02');K=P/'keys';d=json.load(open(P/'key-ops.json'));logs={}
# Named repair is only the inspected NEW enclosed seam inventories, not an imagewide fill.
# Original REST has no holes. No original opaque pixel is repainted.
for k in [1,2]:
 im=Image.open(K/f'key-{k}.png').convert('RGBA');s={(x,y)for y in range(264)for x in range(128)if not im.getpixel((x,y))[3]};holes=[]
 while s:
  q=[s.pop()];edge=False
  for x,y in q:
   edge|=x in(0,127)or y in(0,263)
   for p in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if p in s:s.remove(p);q.append(p)
  if not edge:holes+=q
 groups={'neck-collar':[],'shoulder-plate':[],'inner-arm-body-hip':[],'far-arm-robe':[]};back=Image.new('RGBA',(128,264))
 for x,y in holes:
  if 53<=x<=60 and 40<=y<=51:g='neck-collar';c=(24,24,26,255)
  elif 40<=x<=48 and 49<=y<=55:g='shoulder-plate';c=(70,65,58,255)
  elif 40<=x<=54 and 60<=y<=152:g='inner-arm-body-hip';c=(24,24,26,255)
  elif 78<=x<=87 and 120<=y<=152:g='far-arm-robe';c=(40,47,63,255)
  else:raise AssertionError(('unreviewed',x,y))
  groups[g].append([x,y]);back.putpixel((x,y),c)
 back.save(K/f'data-{k}-body-occlusion-backing.png');bb=back.getbbox();x0,y0,x1,y1=bb;legend={'D':'#18181a','A':'#46413a','I':'#282f3f'};rev={(24,24,26,255):'D',(70,65,58,255):'A',(40,47,63,255):'I'}
 d['ops'][str(k)]['body-occlusion-backing']=[{'kind':'grid','x':x0,'y':y0,'rows':[''.join(rev.get(back.getpixel((x,y)),'.')for x in range(x0,x1))for y in range(y0,y1)],'legend':legend}];logs[str(k)]=groups
json.dump(d,open(P/'key-ops-repaired.json','w'),indent=2);json.dump({'kind':'scoped new-coverage attachment backing','material':'dark body surface behind moving arm, shadow collar, source shoulder armor, indigo behind far arm','inventories':logs,'scope':'listed pixels only; no source opaque pixels repainted'},open(P/'repair-inventory.json','w'),indent=2)
