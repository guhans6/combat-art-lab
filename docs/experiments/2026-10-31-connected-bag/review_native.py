"""Read real native cels to assemble diagnostic evidence; no artwork mutation."""
from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'))
from native_read import read,composite
src=Path(sys.argv[1]);tag=sys.argv[2];a=read(src);plan=json.loads((R/'scope.json').read_text())
names={m['name']:i for i,m in enumerate(a['layers'])}
base=read(plan['base'])
full=Image.new('RGBA',(320*5,250),'#303336');d=ImageDraw.Draw(full)
for j,f in enumerate(range(7,12)):
 full.alpha_composite(composite(a,f-1),(j*320,30));d.text((j*320+8,8),f'F{f}'+(' repaired unit' if 8<=f<=10 else ' unchanged context'),fill='white')
full.convert('RGB').save(R/'review'/f'{tag}-neighbors.png')
contact=Image.new('RGBA',(3*320,2*222),'#303336');d=ImageDraw.Draw(contact)
for j,f in enumerate([8,9,10]):
 for row,obj in enumerate([base,a]):
  im=composite(obj,f-1);contact.alpha_composite(im,(j*320,row*222+25));d.text((j*320+8,row*222+5),f'F{f} '+('before' if row==0 else tag),fill='white')
contact.resize((1920,888),Image.Resampling.NEAREST).convert('RGB').save(R/'review'/f'{tag}-before-after.png')
for f in [8,9,10]:
 p=plan['frames'][str(f)];c=p['crop'];scale=5;w=(c[2]-c[0])*scale;h=(c[3]-c[1])*scale
 out=Image.new('RGBA',(4*(w+16),h+45),'#303336');d=ImageDraw.Draw(out)
 im=composite(a,f-1);bag=a['cels'][f-1,names['04-tote-and-handles']]['image'];strap=a['cels'][f-1,names['06-continuous-handle-tension']]['image']
 hidden=Image.new('RGBA',(320,192))
 for l,meta in enumerate(a['layers']):
  if l!=names['04-tote-and-handles'] and (f-1,l) in a['cels']:hidden.alpha_composite(a['cels'][f-1,l]['image'])
 for j,(label,v) in enumerate([('composite',im),('body + near loop',bag),('rear loop',strap),('body/near loop hidden',hidden)]):
  x=j*(w+16);out.alpha_composite(v.crop(c).resize((w,h),Image.Resampling.NEAREST),(x,30));d.text((x+3,5),f'F{f} {label}',fill='white')
 out.convert('RGB').save(R/'review'/f'{tag}-owners-f{f}.png')
 guide=im.copy();gd=ImageDraw.Draw(guide)
 for name,xy in p['sites'].items():gd.ellipse((xy[0]-1,xy[1]-1,xy[0]+1,xy[1]+1),fill='#ff00ff')
 gd.line([tuple(p['sites']['grip']),tuple(p['sites']['bottom'])],fill='#00ffff')
 guide.resize((960,576),Image.Resampling.NEAREST).save(R/'review'/f'{tag}-guide-f{f}.png')
# Report exact raw cel protection instead of inferring anatomy from owner bounds.
changes=[]
for k,c in a['cels'].items():
 old=base['cels'].get(k);p=c['image'];q=old['image'] if old else Image.new('RGBA',p.size)
 pts=[(i%320,i//320) for i,(x,y) in enumerate(zip(p.get_flattened_data(),q.get_flattened_data())) if x!=y]
 if pts:
  f,l=k;crop=plan['frames'].get(str(f+1),{}).get('crop',[0,0,0,0]);allowed=a['layers'][l]['name'] in plan['frames'].get(str(f+1),{}).get('allowed_owners',[])
  outside=[xy for xy in pts if not crop[0]<=xy[0]<crop[2] or not crop[1]<=xy[1]<crop[3]]
  changes.append({'frame':f+1,'layer':a['layers'][l]['name'],'pixels':len(pts),'allowed_owner':allowed,'outside_mask':len(outside)})
report={'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'changed_cels':changes,'all_other_cels_exact':all(x['allowed_owner'] and not x['outside_mask'] for x in changes),'durations_exact':[f['duration_ms'] for f in a['frames']]==[f['duration_ms'] for f in base['frames']],'palette_chunks_exact':[x for x in a['chunks'] if x['type']==0x2019]==[x for x in base['chunks'] if x['type']==0x2019]}
(R/'review'/f'{tag}-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
