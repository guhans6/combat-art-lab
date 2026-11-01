from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1]; repo=R.parents[2]
paths={'baseline.aseprite':repo/'docs/experiments/2026-10-30-luna-fullbody-once/trial-b/passes/luna6-fullbody-cleanup.aseprite','baseline.png':repo/'docs/experiments/2026-10-30-luna-fullbody-once/trial-b/passes/luna6-fullbody-cleanup.png','character-closeup.png':repo/'assets/references/approved-2026-10-26/character-closeup.png','character-scene.png':repo/'assets/references/approved-2026-10-26/character-scene.png'}
hashes={}
for n,p in paths.items():
 hashes[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
 if not (R/'inputs'/n).exists():shutil.copy2(p,R/'inputs'/n)
(R/'inputs/hashes.json').write_text(json.dumps(hashes,indent=2))
ref=Image.open(R/'inputs/character-closeup.png').convert('RGBA'); base=Image.open(R/'inputs/baseline.png').convert('RGBA')
for n,im,box,s in [('reference-face',ref,(590,240,747,380),3),('reference-mouth',ref,(650,305,740,365),6),('baseline-face',base,(58,18,75,33),24)]:
 crop=im.crop(box); out=Image.new('RGB',(crop.width*s+80,crop.height*s+65),'#303238');out.paste(crop.resize((crop.width*s,crop.height*s),Image.Resampling.NEAREST),(50,35));d=ImageDraw.Draw(out);d.text((4,4),f'{n}: crop {box}; {s}x NN',fill='white')
 step=10 if n.startswith('reference') else 1
 for x in range(box[0],box[2],step):d.text((50+(x-box[0])*s,20),str(x),fill='white')
 for y in range(box[1],box[3],step):d.text((10,35+(y-box[1])*s),str(y),fill='white')
 out.save(R/'reviews'/f'{n}-rulers.png')
print(json.dumps(hashes,indent=2))
