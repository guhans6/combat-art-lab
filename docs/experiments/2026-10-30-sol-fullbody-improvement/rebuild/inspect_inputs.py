from pathlib import Path
import json,hashlib,sys
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parents[1]; P=R.parent/'2026-10-30-fullbody-automated-reconstruction'
sys.path.insert(0,str(R.parents[2]/'tools'))
from check_native_pilot import read
files={'baseline.aseprite':P/'passes/candidate-b-structured.aseprite','baseline.png':P/'passes/candidate-b-structured-reopen.png','seed.png':P/'inputs/source-only-converted-seed.png','rejected.png':P/'passes/pass-01-fullbody-finish.png','rejected.aseprite':P/'passes/pass-01-fullbody-finish.aseprite','character-scene.png':P/'inputs/character-scene.png','character-closeup.png':P/'inputs/character-closeup.png','generated-cutout.png':P/'inputs/clean-generated-cutout-v1.png'}
for n,p in files.items(): (R/'inputs'/n).write_bytes(p.read_bytes())
(R/'inputs/hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files.values()},indent=2))
a=Image.open(files['baseline.png']).convert('RGBA');b=Image.open(files['rejected.png']).convert('RGBA')
diff=[]
for y in range(192):
 for x in range(128):
  ap,bp=a.getpixel((x,y)),b.getpixel((x,y))
  if ap!=bp and (ap[3] or bp[3]):diff.append({'x':x,'y':y,'before':ap,'after':bp})
(R/'proof/prior-visible-diff.json').write_text(json.dumps(diff,indent=2))
an,bn=read(files['baseline.aseprite']),read(files['rejected.aseprite'])
summary={'visible_changed':len(diff),'native_layers_before':[l['name'] for l in an['layers']],'native_layers_rejected':[l['name'] for l in bn['layers']],'bag_region_changes':[p for p in diff if p['x']>=94 and 74<=p['y']<=101]}
(R/'proof/prior-analysis.json').write_text(json.dumps(summary,indent=2))
for name,box,scale in [('head',(32,5,85,43),14),('tote',(75,68,100,103),16),('shoes',(30,163,108,185),10),('jacket',(32,35,96,78),10),('denim',(39,69,98,173),6)]:
 im=a.crop(box).resize(((box[2]-box[0])*scale,(box[3]-box[1])*scale),Image.Resampling.NEAREST)
 bg=Image.new('RGBA',im.size,'#34363a');bg.alpha_composite(im)
 d=ImageDraw.Draw(bg)
 for x in range(box[0],box[2],5):d.text(((x-box[0])*scale,0),str(x),fill='white')
 for y in range(box[1],box[3],5):d.text((0,(y-box[1])*scale),str(y),fill='white')
 bg.save(R/'reviews'/f'baseline-{name}-coordinates.png')
print(json.dumps(summary))
