from pathlib import Path
from PIL import Image
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R.parents[2]/'tools'));from check_native_pilot import read,compare
name=sys.argv[1] if len(sys.argv)>1 else 'pass-01';mask=[0]*(128*192)
for y in range(27,29):
 for x in range(66,71):mask[y*128+x]=255
native=R/f'passes/{name}.aseprite';p=R/f'passes/{name}.png';q=R/f'passes/{name}-reopen.png';a=read(R/'inputs/baseline.aseprite');b=read(native)
report=compare(R/'inputs/baseline.aseprite',native,['08-hair-tie-and-hair'],mask)
base=Image.open(R/'inputs/baseline.png').convert('RGBA');out=Image.open(q).convert('RGBA');changes=[]
for y in range(192):
 for x in range(128):
  if base.getpixel((x,y))!=out.getpixel((x,y)):changes.append({'x':x,'y':y,'before':base.getpixel((x,y)),'after':out.getpixel((x,y))})
comp=Image.new('RGBA',(128,192))
for i,l in enumerate(b['layers']):
 if l['flags']&1:comp.alpha_composite(b['cels'][(0,i)]['image'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=json.loads((R/'inputs/hashes.json').read_text());inputs={p:sha(Path(p))==v for p,v in inputs.items()}
report.update({'native_sha256':sha(native),'png_sha256':sha(q),'native_equals_fresh_export':comp.tobytes()==out.tobytes(),'first_and_reopen_png_byte_equal':p.read_bytes()==q.read_bytes(),'alpha_equal':base.getchannel('A').tobytes()==out.getchannel('A').tobytes(),'changed_pixels':changes,'protected_composite_changes':sum(not mask[v['y']*128+v['x']] for v in changes),'input_originals_unchanged':inputs,'visible_opaque_count':sum(px[3]>0 for px in out.get_flattened_data()),'backend_validate':'Not exposed in current inventory. Independent binary/native and export protection checks run instead.','expression_verdict':'not evaluated by mechanical checker'})
assert report['passed'] and report['native_equals_fresh_export'] and report['first_and_reopen_png_byte_equal'] and report['alpha_equal'] and report['protected_composite_changes']==0 and all(inputs.values()),report
(R/f'proof/{name}-checks.json').write_text(json.dumps(report,indent=2)+'\n')
# Negative checker test: reject the identical patch when every pixel is protected.
negative=compare(R/'inputs/baseline.aseprite',native,['08-hair-tie-and-hair'],[0]*(128*192));assert not negative['passed'];(R/f'proof/{name}-negative-scope-check.json').write_text(json.dumps(negative,indent=2)+'\n')
print(json.dumps(report,indent=2))
