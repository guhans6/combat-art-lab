"""Read-only source inspection; creates diagnostic panels, never edits artwork."""
from pathlib import Path
import sys,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'))
from native_read import read,composite
p=R.parent/'2026-10-31-full-attack-repair/source/attack-repaired.aseprite'
a=read(p); names={v['name']:i for i,v in enumerate(a['layers'])}
export=Image.open(R.parent/'2026-10-31-full-attack-repair/frames/candidate-8.png').convert('RGBA')
def visible_bytes(im):
 return bytes(v for px in im.getdata() for v in (px if px[3] else (0,0,0,0)))
if visible_bytes(composite(a,8)) != visible_bytes(export):
 raise RuntimeError('F9 native and export disagree')
bag=a['cels'][8,names['04-tote-and-handles']]['image'];strap=a['cels'][8,names['06-continuous-handle-tension']]['image']
combo=Image.new('RGBA',(320,192));combo.alpha_composite(strap);combo.alpha_composite(bag)
box=(148,76,183,123);scale=8
panels=[('F9 actual composite',composite(a,8)),('Bag owner only',bag),('Handle owner only',strap),('Handles + bag',combo)]
out=Image.new('RGB',(4*300,420),'#303336');d=ImageDraw.Draw(out)
for i,(label,im) in enumerate(panels):
 d.text((i*300+8,8),label,fill='white');part=im.crop(box).resize((280,376),Image.Resampling.NEAREST);out.paste(part,(i*300+8,30),part)
out.save(R/'f9-ownership-8x.png')
rows=[]
for y in range(88,101):
 pts=[x for x in range(148,183) if bag.getpixel((x,y))[3]]
 rows.append({'y':y,'bag_opaque_x':pts})
res={'native_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'native_export_visible_rgba_equal':True,'frame':9,'crop_xyxy':box,'scale':scale,'layers_in_order':[v['name'] for v in a['layers']],'authored_rim_endpoints':[[153,96],[173,90]],'rows':rows,'at_endpoints':[{'point':[x,y],'bag_rgba':bag.getpixel((x,y)),'strap_rgba':strap.getpixel((x,y))} for x,y in [(153,96),(173,90)]]}
(R/'f9-inspection.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k!='rows'},indent=2))
