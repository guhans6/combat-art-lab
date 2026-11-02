from pathlib import Path
import collections,hashlib,importlib.util,json
from PIL import Image
R=Path('/private/tmp/fighter-user-variants-r01/native-work')
M=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools/check_native_pilot.py')
spec=importlib.util.spec_from_file_location('independent_native_reader',M);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
if not hasattr(Image.Image,'get_flattened_data'):Image.Image.get_flattened_data=Image.Image.getdata
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'method':'independent repository native reader; RGBA compositing, owner pixels and producer proof comparison; no Aseprite interaction','variants':{}}
images={}
for n in ('01','03','04','05'):
 d=R/f'variant-{n}'; fn=d/'static.aseprite'; old=d/'pass02-preownership/static.aseprite'
 cur=mod.read(fn);pre=mod.read(old)
 orig=Image.open(d/'static.png').convert('RGBA'); prior=Image.open(d/'pass02-preownership/static.png').convert('RGBA');reopened=Image.open(d/'reopened.png').convert('RGBA')
 assert cur['canvas']==[128,264] and len(cur['frames'])==1 and len(cur['layers'])==6
 assert [l['name'] for l in cur['layers']]==[l['name'].replace('lowerbody-boots','lowerbody-cloth-boots') for l in pre['layers']]
 assert orig.tobytes()==prior.tobytes()==reopened.tobytes()
 comp=Image.new('RGBA',orig.size);opacity_count=[0]*(128*264);per_owner={};owner_transfer={}
 for i,layer in enumerate(cur['layers']):
  im=cur['cels'][(0,i)]['image'];before=pre['cels'][(0,i)]['image'];images[n,layer['name']]=im
  assert layer['flags']&1 and layer['opacity']==255 and layer['blend']==0
  p=list(im.getdata());oldp=list(before.getdata()); per_owner[layer['name']]=sum(v[3]>0 for v in p)
  owner_transfer[layer['name']]={'changed':sum(a!=b for a,b in zip(oldp,p)),'gained':sum(bool(not a[3] and b[3]) for a,b in zip(oldp,p)),'lost':sum(a[3] and not b[3] for a,b in zip(oldp,p))}
  for j,v in enumerate(p):opacity_count[j] += bool(v[3])
  comp.alpha_composite(im)
 assert comp.tobytes()==orig.tobytes()
 assert not any(x>1 for x in opacity_count),f'overlapping owners {n}'
 mask=list(Image.open(d/'edit-proof-mask.png').convert('L').getdata())
 protected=mod.compare(fn,d/'edit-proof.aseprite',['near-arm-guard-hand'],mask)
 assert protected['passed'],protected
 proof=Image.open(d/'edit-proof.png').convert('RGBA');reproof=Image.open(d/'edit-proof-reopened.png').convert('RGBA')
 assert proof.tobytes()==reproof.tobytes()
 pixel_changes=sum(a!=b for a,b in zip(orig.getdata(),proof.getdata()))
 assert pixel_changes==24
 report['variants'][n]={'native_sha256':H(fn),'png_sha256':H(d/'static.png'),'prior_native_sha256':H(old),'proof_native_sha256':H(d/'edit-proof.aseprite'),'previous_and_reopened_composites_exact':True,'six_disjoint_visible_owners_recompose_exactly':True,'per_owner_pixels':per_owner,'preownership_to_final_native_owner_changes':owner_transfer,'proof_changed_composite_pixels':pixel_changes,'proof_native_protection':protected['passed'],'proof_reopened_exact':True}
changes={}
for name in [l['name'] for l in mod.read(R/'variant-03/static.aseprite')['layers']]:
 a,b=images['03',name],images['05',name]
 changes[name]=sum(x!=y for x,y in zip(a.getdata(),b.getdata()))
report['u03_u05_native_owner_difference']=changes
report['u03_u05_only_armor_diff']=all(v==0 for k,v in changes.items() if k!='torso-cloth-armor') and changes['torso-cloth-armor']==154
out=Path('/private/tmp/fighter-user-variants-r01/review/ownership-audit.json');out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert report['u03_u05_only_armor_diff']
