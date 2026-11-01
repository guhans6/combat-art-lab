from PIL import Image,ImageDraw
from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parent
paths=[r/'trial-a/inputs/baseline.png',r/'trial-a/outputs/luna56-fullbody-cleanup.png',r/'trial-b/passes/luna6-fullbody-cleanup.png']
if not paths[0].exists():
 paths[0]=r.parent/'2026-10-30-fullbody-automated-reconstruction/passes/candidate-b-structured-reopen.png'
ims=[Image.open(p).convert('RGBA') for p in paths]
labels=['Unchanged seed','Luna 5.6 Max: rejected (43 alpha additions)','Luna 6 Max: candidate for review']
out=Image.new('RGB',(3*420,1080),'#252a31');d=ImageDraw.Draw(out)
for i,(im,label) in enumerate(zip(ims,labels)):
 x=i*420;d.text((x+12,12),label,fill='white')
 matte=Image.new('RGBA',im.size,'#414953');matte.alpha_composite(im)
 out.paste(matte.convert('RGB').resize((384,576),Image.Resampling.NEAREST),(x+12,42))
 head=matte.crop((38,7,83,44)).convert('RGB').resize((360,296),Image.Resampling.NEAREST)
 out.paste(head,(x+12,650))
 d.text((x+12,965),'Full body 3x; head 8x; neutral matte',fill='white')
out.save(r/'supervisor-comparison.png')
report=[]
for p,im in zip(paths,ims):
 a=list(ims[0].getdata());b=list(im.getdata())
 report.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'visible_changes':sum(x!=y and bool(x[3] or y[3]) for x,y in zip(a,b)),'alpha_changes':sum(x[3]!=y[3] for x,y in zip(a,b)),'head_changes':sum(ims[0].getpixel((x,y))!=im.getpixel((x,y)) for x in range(38,83) for y in range(7,44))})
(r/'supervisor-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
