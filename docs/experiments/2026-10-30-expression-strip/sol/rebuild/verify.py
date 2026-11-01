from pathlib import Path
from PIL import Image
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];repo=R.parents[3];sys.path.insert(0,str(repo/'tools'));from check_native_pilot import read,compare
baseline=repo/'docs/experiments/2026-10-30-luna-fullbody-once/trial-b/passes/luna6-fullbody-cleanup.aseprite';basepng=baseline.with_suffix('.png');B=Image.open(basepng).convert('RGBA');owner='08-hair-tie-and-hair';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=json.loads((R/'inputs/input-hashes.json').read_text());unchanged={p:sha(Path(p))==h for p,h in inputs.items()};assert all(unchanged.values())
results={}
for name in ['neutral','subtle-smile','surprise']:
 native=(R/f'inputs/luna6-{name}.aseprite') if name=='neutral' else R/f'passes/sol-{name}-pass01.aseprite'
 first=(R/f'inputs/luna6-{name}.png') if name=='neutral' else native.with_suffix('.png')
 fresh=R.parent/f'luna/proof/luna6-{name}-reopened.png' if name=='neutral' else native.with_name(native.stem+'-reopen.png')
 scope=json.loads((R.parent/f'luna/masks/{name}.json').read_text());mask=[0]*(128*192)
 for region in scope['editableRegions']:
  x1,y1,x2,y2=region['xyxy']
  for y in range(y1,y2):
   for x in range(x1,x2):mask[y*128+x]=255
 report=compare(baseline,native,[owner],mask);native_data=read(native);out=Image.open(fresh).convert('RGBA');comp=Image.new('RGBA',(128,192))
 for i,l in enumerate(native_data['layers']):
  if l['flags']&1:comp.alpha_composite(native_data['cels'][(0,i)]['image'])
 changes=[{'x':x,'y':y,'before':B.getpixel((x,y)),'after':out.getpixel((x,y))} for y in range(192) for x in range(128) if B.getpixel((x,y))!=out.getpixel((x,y))]
 negative=compare(baseline,native,[owner],[0]*(128*192));assert not negative['passed']
 report.update({'name':name,'native':str(native.relative_to(repo)),'native_sha256':sha(native),'fresh_export':str(fresh.relative_to(repo)),'png_sha256':sha(fresh),'native_composite_equals_fresh_export':comp.tobytes()==out.tobytes(),'first_reopen_rgba_equal':Image.open(first).convert('RGBA').tobytes()==out.tobytes(),'first_reopen_png_byte_equal':first.read_bytes()==fresh.read_bytes(),'alpha_equal':B.getchannel('A').tobytes()==out.getchannel('A').tobytes(),'canvas_equal':B.size==out.size,'changed_pixels':changes,'changed_count':len(changes),'protected_composite_changes':sum(not mask[v['y']*128+v['x']] for v in changes),'nose_equal':B.getpixel((71,24))==out.getpixel((71,24)),'opaque_pixels':sum(px[3]>0 for px in out.get_flattened_data()),'negative_scope_rejected':not negative['passed'],'expression_quality':'not established by this mechanical check'})
 if name!='neutral':
  luna=R/f'inputs/luna6-{name}.aseprite';L=Image.open(luna.with_suffix('.png')).convert('RGBA');report['incremental_rescue_composite_count']=sum(a!=b for a,b in zip(L.get_flattened_data(),out.get_flattened_data()));op=json.loads((R/f'operations/{name}-pass01.json').read_text());expected={(p['x'],p['y']) for v in op['ops'] for p in v['points']};actual={(x,y) for y in range(192) for x in range(128) if L.getpixel((x,y))!=out.getpixel((x,y))};report['rescue_matches_exact_operation_coordinates']=actual==expected
  exact=[255 if (x,y) in expected else 0 for y in range(192) for x in range(128)];report['incremental_rescue_native_check']=compare(luna,native,[owner],exact);assert report['incremental_rescue_native_check']['passed'] and report['rescue_matches_exact_operation_coordinates']
 assert report['passed'] and report['native_composite_equals_fresh_export'] and report['first_reopen_rgba_equal'] and report['alpha_equal'] and report['protected_composite_changes']==0 and report['nose_equal']
 (R/f'proof/{name}-checks.json').write_text(json.dumps(report,indent=2)+'\n');results[name]=report
# A cosmetic modified-session resave was retained; ensure it did not represent unseen artwork.
a=read(R/'passes/sol-subtle-smile-pass01.aseprite');b=read(R/'proof/smile-session-resave.aseprite');assert all(a['cels'][k]['image'].tobytes()==b['cels'][k]['image'].tobytes() for k in a['cels']);assert a['frames']==b['frames'] and a['layers']==b['layers'] and a['header']==b['header']
summary={'input_originals_unchanged':unchanged,'smile_cosmetic_session_resave_equals_final_native_content':True,'variants':{n:{k:v[k] for k in ['native','native_sha256','fresh_export','png_sha256','changed_count','passed','first_reopen_png_byte_equal','alpha_equal','protected_composite_changes']} for n,v in results.items()},'backend_validate':'Tool not exposed in connected inventory; independent strict native checker run.','user_visual_approval':'pending'}
(R/'proof/summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
