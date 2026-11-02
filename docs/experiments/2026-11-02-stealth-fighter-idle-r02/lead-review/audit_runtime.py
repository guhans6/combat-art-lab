from pathlib import Path
from PIL import Image
import json,hashlib
root=Path('/private/tmp/fighter-r02-godot-preview')
layout=json.loads((root/'layout.json').read_text())
checks=[]
for i,name in enumerate(layout['files']):
 src=Image.open(root/'textures'/name).convert('RGBA')
 cap=Image.open(root/'evidence'/f'runtime-frame-{i:02}.png').convert('RGBA')
 x,y=130,int(300-layout['feet_y'])
 crop=cap.crop((x,y,x+src.width,y+src.height))
 bad=sum(a[:3]!=b[:3] for a,b in zip(src.getdata(),crop.getdata()) if a[3])
 checks.append({'frame':i,'opaque_rgb_mismatches':bad})
record=json.loads((root/'evidence/runtime.json').read_text())
result={'passed':all(c['opaque_rgb_mismatches']==0 for c in checks) and record['loops']>=3 and len(record['captured'])==len(layout['files']),'frames':checks,'runtime_loops':record['loops'],'engine':record['engine'],'source_rect':[130,47,258,311]}
(root/'evidence/pixel-checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result));assert result['passed']
