"""Prepare literal drawing grids; Aseprite MCP alone writes native artwork."""
from pathlib import Path
from PIL import Image
import sys,json
R=Path(__file__).resolve().parent
if (R/'operations/FROZEN').exists():
 raise SystemExit('Historical preparation recipe is frozen. Rebuild using operations/replay-plan.json through dedicated Aseprite MCP; see REPRODUCE.md.')
sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'))
from native_read import read
src=read(R.parent/'2026-10-30-tote-attack/artist/sol-rescue/source/tote-attack-v03.aseprite')
# Fixed anatomical correspondence, not frame bounding-box fitting.
# Head/torso smaller; long jeans restored; sneaker height preserved separately.
K=[(0,0),(85,73),(165,170),(185,185),(192,192)]
def sy(y):
 for (a,b),(c,d) in zip(K,K[1:]):
  if b<=y<d:return a+(y-b)*(c-a)/(d-b)
 return y
def mapped(im):
 out=Image.new('RGBA',(320,192));p=out.load();q=im.load()
 for y in range(192):
  v=min(191,max(0,int(sy(y)+.5)))
  for x in range(320):
   u=int(128+(x-128)/.78+.5)
   if 0<=u<320:p[x,y]=q[u,v]
 return out
def grid(im):
 b=im.getbbox()
 if not b:return []
 colors=list(dict.fromkeys(p for p in im.getdata() if p[3]));leg={chr(0x100+i):'#%02x%02x%02x'%p[:3] for i,p in enumerate(colors)};rev={p:chr(0x100+i) for i,p in enumerate(colors)}
 return [dict(kind='grid',x=b[0],y=b[1],rows=[''.join(rev[im.getpixel((x,y))] if im.getpixel((x,y))[3] else '.' for x in range(b[0],b[2])) for y in range(b[1],b[3])],legend=leg,transparent='erase')]
calls=[]
for f in range(1,12):
 for l,meta in enumerate(src['layers']):
  if (f,l) not in src['cels']:continue
  im=mapped(src['cels'][f,l]['image'])
  calls.append(dict(frame=f+1,layer=meta['name'],createCel=True,label=f'P01 anatomical registration F{f+1}',ops=[dict(kind='clear')]+grid(im)))
(R/'operations/pass01.json').write_text(json.dumps(calls))
print('Prepared',len(calls),'native drawing batches')
