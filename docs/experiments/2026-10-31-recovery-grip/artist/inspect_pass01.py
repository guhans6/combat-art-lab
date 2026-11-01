import sys,json
from pathlib import Path
from PIL import Image,ImageDraw
sys.path.insert(0,'docs/experiments/2026-10-30-evidence-idle-four-model/sol61')
from native_read import read,composite,sha,rgba_equal
R=Path('docs/experiments/2026-10-31-recovery-grip/artist'); b=read(R/'source/recovery-grip-baseline.aseprite');a=read(R/'source/recovery-grip-pass01.aseprite')
# Read-only owner sheets with shared matte; labels refer to native coordinates.
for l in [2,4,5,6]:
 out=Image.new('RGB',(720,400),'#363844');d=ImageDraw.Draw(out)
 for i,s in enumerate([b,a]):
  im=s['cels'][(8,l)]['image'].crop((158,76,194,112));m=Image.new('RGBA',im.size,'#363844');m.alpha_composite(im)
  out.paste(m.convert('RGB').resize((360,360),Image.Resampling.NEAREST),(360*i,24))
 d.text((4,4),f'Layer {l} before | pass01; native crop [158,76,194,112]',fill='white');out.save(R/f'proof/pass01-layer-{l}-before-after.png')
changes={}
mask=Image.open(R/'proof/allowed-mask.png')
for key in b['cels']:
 p=b['cels'][key]['image'];q=a['cels'][key]['image'];xy=[(x,y) for y in range(192) for x in range(320) if p.getpixel((x,y))!=q.getpixel((x,y))]
 if xy:changes[str(key)]={'pixels':len(xy),'bbox':[min(x for x,y in xy),min(y for x,y in xy),max(x for x,y in xy)+1,max(y for x,y in xy)+1],'outside_mask':sum(not mask.getpixel(p) for p in xy)}
(R/'proof/pass01-diff.json').write_text(json.dumps(changes,indent=2));print(changes)
