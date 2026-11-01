from tools.check_native_pilot import read
from PIL import Image
from pathlib import Path
from collections import defaultdict
import json,hashlib
P=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol/reddit-motion-study/eased-connected-idle');B=P.parent/'prototype/pass01.aseprite';a=read(B);mapping=[0,0,1,2,2,2,3,3,4,5,6,7];times=[650,240,240,420,380,260,360,500,50,80,50,720]
# head up1 duringF3–6. No facial redraw. All actual visible owners share field.
def stop(x,f):
 center={2:57,3:64,4:66,5:56}[f]
 if 47<=x<=74:return center
 if 43<=x<=46 or 75<=x<=80:return min(center,61)
 if 39<=x<=42 or 81<=x<=85:return min(center,59)
 return min(center,57)
def field(f,x,y):
 dy=1 if f in[2,3,4,5]and y<=stop(x,f)else 0
 ranges={1:(50,63),2:(52,68),3:(60,105),4:(56,117),5:(60,117),6:(66,113),7:(76,105)}
 span=ranges.get(f);dx=1 if span and span[0]<=y<=span[1]else 0
 return dx,dy
ops=[];mask=Image.new('L',(128,192));native=[]
for f,srcf in enumerate(mapping):
 ims=[a['cels'][(srcf,l)]['image'].copy()for l in range(12)]
 for l in range(1,12):
  src=a['cels'][(srcf if f in[8,9,10]else 0,l)]['image'];dst=src.copy()
  for y in range(192):
   for x in range(128):
    dx,dy=field(f,x,y)
    if dx or dy:dst.putpixel((x,y),src.getpixel((x-dx,y+dy))if x-dx>=0 else (0,0,0,0))
  old=ims[l];ims[l]=dst;groups=defaultdict(list)
  for y in range(192):
   for x in range(128):
    c=dst.getpixel((x,y))
    if c!=old.getpixel((x,y)):
     mask.putpixel((x,y),255);groups['#%02x%02x%02x%02x'%c].append({'x':x,'y':y})
  if groups:ops.append({'frame':f+1,'layer':a['layers'][l]['name'],'paletteLock':False,'ops':[{'kind':'pixels','color':c,'points':pts}for c,pts in groups.items()]})
 native.append(ims)
(P/'proof/operations.json').write_text(json.dumps(ops,separators=(',',':'))+'\n');mask.save(P/'proof/allowed-mask.png')
(P/'proof/timing-map.json').write_text(json.dumps({'old_frame_zero_based_mapping':mapping,'durations_ms':times,'cycle_ms':sum(times),'head_up_frames_one_based':[3,4,5,6],'blink_new_frames_one_based':[9,10,11],'blink_old_frames_one_based':[5,6,7],'foot_fixed_y_min':118,'phases':['rest','chest onset','rise','lower response','turnaround','upper release','waist release','leg settle','blink half','blink closed','blink half','rest']},indent=2)+'\n')
inputs=[B,P.parent/'reference.mp4',*Path('assets/references/approved-2026-10-26').glob('character-*.png')]
(P/'proof/input-hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in inputs},indent=2)+'\n')
print('drawing calls',len(ops),'total changed native samples',sum(len(v['points'])for o in ops for v in o['ops']))
