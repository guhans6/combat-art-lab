from pathlib import Path
from PIL import Image,ImageChops
import sys,json,hashlib
sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools')
from check_native_pilot import read
w=Path('/private/tmp/stealth-fighter-idle-r02');d=w/'delivery';out=Path('/private/tmp/fighter-r02-lead')
natives=list(d.glob('*.aseprite'));n=next(p for p in natives if 'proof' not in p.name and 'edit' not in p.name and 'reopen' not in p.name)
a=read(w/'inputs/idle-r01.aseprite');b=read(n)
def comp(s,f):
 im=Image.new('RGBA',s['canvas'])
 for i,l in enumerate(s['layers']):
  if l['flags']&1 and (f,i)in s['cels']:im.alpha_composite(s['cels'][(f,i)]['image'])
 return im
rest=comp(a,0);parts={l['name']:i for i,l in enumerate(b['layers'])};origparts={l['name']:i for i,l in enumerate(a['layers'])};errors=[]
assert b['canvas']==[128,264]
durs=[f['duration_ms']for f in b['frames']];assert durs==[700,260,500,340],durs
palette={c for c in rest.getdata()if c[3]};rows=[]
for f in range(4):
 im=comp(b,f);p=d/f'idle-{f}.png';assert p.exists(),p
 assert im.tobytes()==Image.open(p).convert('RGBA').tobytes(),f
 assert set(c for c in im.getdata()if c[3])<=palette
 assert set(im.getchannel('A').getdata())<={0,255}
 assert im.crop((0,153,128,264)).tobytes()==rest.crop((0,153,128,264)).tobytes()
 for name in ['lower-body-fixed','sword-belt']:
  assert b['cels'][(f,parts[name])]['image'].tobytes()==a['cels'][(0,origparts[name])]['image'].tobytes(),name
 if 'far-hem-fixed'in parts:assert b['cels'][(f,parts['far-hem-fixed'])]['image'].tobytes()==b['cels'][(0,parts['far-hem-fixed'])]['image'].tobytes()
 dx,dy=[(0,0),(0,-1),(-2,-2),(0,-1)][f];head=Image.new('RGBA',(128,264));head.alpha_composite(a['cels'][(0,origparts['head-hair-neck'])]['image'],(dx,dy));assert head.tobytes()==b['cels'][(f,parts['head-hair-neck'])]['image'].tobytes()
 rows.append({'frame':f,'native_matches_png':True,'lower_body_and_sword_native_exact':True,'lower_composite_y153_fixed':True,'head_registered_exact':True,'binary_alpha':True,'source_palette_only':True})
assert comp(b,0).tobytes()==rest.tobytes();assert comp(b,1).tobytes()==comp(b,3).tobytes()
r={'passed':True,'native':str(n),'sha256':hashlib.sha256(n.read_bytes()).hexdigest(),'canvas':b['canvas'],'layers':list(parts),'durations_ms':durs,'rest_composite_exact':True,'return_transition_exact':True,'frames':rows}
(out/'independent-native-checks.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
