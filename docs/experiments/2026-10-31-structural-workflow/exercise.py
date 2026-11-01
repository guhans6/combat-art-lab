"""Read-only historical evidence; no asset or native file writes."""
from pathlib import Path
import sys,json,hashlib,difflib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'))
from native_read import read,composite
old=R.parent/'2026-10-30-tote-attack/artist/sol-rescue/source/tote-attack-v03.aseprite'
a=read(old);sheet=Image.new('RGBA',(960,600),'#303336');d=ImageDraw.Draw(sheet)
# All images share the real native grid. No individual fitting or registration.
for i,(label,f) in enumerate([('Neutral / exact entry',0),('Old pickup',1),('Old shared grip',2)]):
 im=composite(a,f);x=i*320;d.text((x+6,6),label,fill='white');sheet.alpha_composite(im,(x,25))
 # Same full-actor crop on every panel, nearest 2x; feet may exceed this close view.
 crop=(80,0,220,160);part=im.crop(crop).resize((280,320),Image.Resampling.NEAREST)
 sheet.alpha_composite(part,(x+10,240));d.text((x+6,570),'same crop [80,0,220,160), 2x',fill='white')
sheet.convert('RGB').save(R/'proportion-case.png')
paths=[old,R/'proportion-case.png',R.parent/'2026-10-31-attack-cause-audit/f9-ownership-8x.png',R.parent/'2026-10-31-full-attack-repair/source/attack-repaired.aseprite',R.parent/'2026-10-31-full-attack-repair/review/contact-2x.png']
(R/'evidence.json').write_text(json.dumps([{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],indent=2)+'\n')
files=json.loads((R/'maintained-files.json').read_text())+['tools/pixel-art-director/references/structure.md','docs/adr/0002-structural-animation-checkpoints.md']
patch=[]
for name in files:
 before=R/'baseline'/name;after=ROOT/name
 patch.extend(difflib.unified_diff(before.read_text().splitlines(True) if before.exists() else [],after.read_text().splitlines(True),fromfile='before/'+name,tofile='after/'+name))
(R/'workflow.patch').write_text(''.join(patch))
print('Historical same-grid proportion case, evidence hashes and task delta written.')
