from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent
if (R/'operations/FROZEN').exists():
 raise SystemExit('Historical preparation recipe is frozen. Rebuild using operations/replay-plan.json through dedicated Aseprite MCP; see REPRODUCE.md.')
sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'))
from native_read import read
a=read(R/'source/attack-candidate.aseprite')
points={2:[(148,104),(148,105)],3:[(179,118),(182,121),(182,122),(176,115),(176,116),(189,128),(189,127)],5:[(174,118),(177,122),(177,121),(172,116),(172,115),(184,128),(184,127)],7:[(122,40),(121,40),(122,41),(123,41),(123,42),(124,43)],12:[(165,75)]}
calls=[]
for f,pts in points.items():
 for l,meta in enumerate(a['layers']):
  if (f-1,l) not in a['cels']:continue
  actual=[(x,y) for x,y in pts if a['cels'][f-1,l]['image'].getpixel((x,y))[3]]
  if actual:calls.append(dict(frame=f,layer=meta['name'],label='Remove reviewed detached old-outline remnants',ops=[dict(kind='grid',x=x,y=y,rows=['.'],legend={},transparent='erase') for x,y in actual]))
(R/'operations/remnant-cleanup.json').write_text(json.dumps(calls,indent=2));print(calls)
