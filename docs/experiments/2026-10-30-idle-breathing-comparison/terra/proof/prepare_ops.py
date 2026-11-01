from tools.check_native_pilot import read
from collections import defaultdict
from pathlib import Path
import json
p=Path('docs/experiments/2026-10-30-idle-breathing-comparison/terra')
x=read('docs/experiments/2026-10-30-idle-breath-blink/luna/passes/pass01/luna6-idle-breath-blink-pass01.aseprite')
result=[]
for frame,stage in [(1,1),(2,2),(3,1)]:
 for i,box,dx in [(3,(35,39,50,62),-1),(4,(77,39,91,62),1),(5,(54,46,65,69),0)]:
  src=x['cels'][(frame,i)]['image']; pix=src.load(); groups=defaultdict(list);x0,y0,x1,y1=box
  for y in range(y0,y1):
   for xx in range(x0,x1):
    dy=stage if y<56 else (1 if y<63 else 0);shift=dx if y<56 else 0
    sx,sy=xx-shift,y+dy
    if x0<=sx<x1 and y0<=sy<y1:
     c=pix[sx,sy]
     if c[3]==255 and c!=pix[xx,y]:groups['#%02x%02x%02x'%c[:3]].append([xx,y])
  result.append({'frame':frame+1,'layer':x['layers'][i]['name'],'ops':[{'kind':'pixels','color':c,'points':pts} for c,pts in groups.items()]})
(p/'proof/operations.json').write_text(json.dumps(result,indent=2)+'\n')
print([(r['frame'],r['layer'],sum(len(o['points']) for o in r['ops'])) for r in result])
