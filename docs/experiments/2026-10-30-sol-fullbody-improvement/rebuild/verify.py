from pathlib import Path
import json,sys,hashlib,struct
from PIL import Image
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R.parents[2]/'tools'));from check_native_pilot import read,compare
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=read(R/'inputs/baseline.aseprite');b=read(R/'passes/pass-02.aseprite');layers=[];composite=Image.new('RGBA',(128,192));coverage=[0]*24576
for i,l in enumerate(b['layers']):
 ai=a['cels'][(0,i)]['image'];bi=b['cels'][(0,i)]['image'];changed=sum(p!=q for p,q in zip(ai.get_flattened_data(),bi.get_flattened_data()))
 layers.append({'name':l['name'],'changed_native_pixels':changed,'before_geometry':a['cels'][(0,i)]['geometry'],'after_geometry':b['cels'][(0,i)]['geometry'],'visible_pixels':sum(p[3]>0 for p in bi.get_flattened_data())})
 if l['flags']&1:
  composite.alpha_composite(bi)
  for j,p in enumerate(bi.get_flattened_data()):coverage[j]+=p[3]>0
 else:assert ai.tobytes()==bi.tobytes(),'hidden guide changed'
assert max(coverage)==1 and sum(coverage)==7844
out=Image.open(R/'passes/pass-02-reopen.png').convert('RGBA');base=Image.open(R/'inputs/baseline.png').convert('RGBA')
assert composite.tobytes()==out.tobytes()
assert base.getchannel('A').tobytes()==out.getchannel('A').tobytes()
assert a['header']==b['header'];assert a['frames']==b['frames'];assert a['layers']==b['layers']
assert (R/'passes/pass-02.png').read_bytes()==(R/'passes/pass-02-reopen.png').read_bytes()
for i,l in enumerate(b['layers']):
 if l['name'] in ['05-tote-strap','06a-left-hand','06b-right-hand','guide-source-seed (hidden)']:assert a['cels'][(0,i)]['image'].tobytes()==b['cels'][(0,i)]['image'].tobytes()
assert all(base.getpixel((x,y))==out.getpixel((x,y)) for y in range(19,25) for x in range(61,73))
# Native local feature edit, with independent positive and negative scope tests.
mask=[0]*24576
for x in [65,66]:mask[29*128+x]=255
proof=compare(R/'passes/pass-02.aseprite',R/'proof/face-edit.aseprite',['07-face-and-neck'],mask)
assert proof['passed'],proof
negative=compare(R/'passes/pass-02.aseprite',R/'proof/face-edit.aseprite',['07-face-and-neck'],[0]*24576)
assert not negative['passed']
assert (R/'proof/face-edit.png').read_bytes()==(R/'proof/face-edit-reopen.png').read_bytes()
assert sum(p!=q for p,q in zip(out.get_flattened_data(),Image.open(R/'proof/face-edit-reopen.png').convert('RGBA').get_flattened_data()))==2
(R/'proof/face-edit-check.json').write_text(json.dumps(proof,indent=2));(R/'proof/negative-scope-check.json').write_text(json.dumps(negative,indent=2))
# Smoke: asymmetric protected shape and exact transparent erase survive actual reopen.
s0=read(R/'proof/scratch-initial.aseprite');s1=read(R/'proof/scratch-edit.aseprite')
assert len(s1['layers'])==2
assert s0['cels'][(0,0)]['image'].tobytes()==s1['cels'][(0,0)]['image'].tobytes()
sim=Image.open(R/'proof/scratch-reopen.png').convert('RGBA');assert sim.getpixel((10,12))[3]==0 and sim.getpixel((11,12))==(252,216,182,255)
for x,y in [(2,3),(3,3),(3,4)]:assert sim.getpixel((x,y))==(85,51,34,255)
originals=json.loads((R/'inputs/hashes.json').read_text());unchanged={p:sha(Path(p))==h for p,h in originals.items()};assert all(unchanged.values())
report={'passed':True,'native_sha256':sha(R/'passes/pass-02.aseprite'),'png_sha256':sha(R/'passes/pass-02-reopen.png'),'native_canvas':[128,192],'native_layers':12,'visible_parts':11,'visible_pixels':7844,'visible_changed_pixels':sum(p!=q for p,q in zip(base.get_flattened_data(),out.get_flattened_data())),'alpha_changed_pixels':0,'eye_patch_changed_pixels':0,'header_equal':a['header']==b['header'],'frame_non_cel_chunks_equal':a['frames']==b['frames'],'layer_metadata_equal':a['layers']==b['layers'],'reopen_png_byte_equal':True,'native_composite_equals_actual_export':True,'disjoint_visible_ownership':True,'protected_inputs_unchanged':unchanged,'layers':layers,'two_pixel_face_edit_check_passed':True,'negative_scope_check_rejected':True,'backend_validate':'not exposed in current MCP tool inventory; independent native/PNG checks used'}
(R/'proof/final-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
