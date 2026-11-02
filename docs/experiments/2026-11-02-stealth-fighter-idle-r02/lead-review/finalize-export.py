from pathlib import Path
import json,hashlib,shutil
from PIL import Image
r=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning');e=r/'docs/experiments/2026-11-02-stealth-fighter-idle-r02';s=r/'assets/source/stealth-fighter/idle-r02';x=r/'assets/export/stealth-fighter/idle-r02';p=r/'assets/previews/stealth-fighter/idle-r02';sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
f=x/'timings.json';t=json.loads(f.read_text())
for i,row in enumerate(t['frames']):row['file']=f'frames/idle-{i:02}.png'
f.write_text(json.dumps(t,indent=2))
rows=[]
for i,row in enumerate(t['frames']):
 fp=x/row['file'];assert fp.exists();a=Image.open(fp).convert('RGBA');b=Image.open(e/'godot-preview/textures'/f'idle-{i}.png').convert('RGBA');assert a.tobytes()==b.tobytes();rows.append({'frame':i,'path_resolves':True,'tested_engine_pixels_exact':True})
assert sum(z['duration_ms']for z in t['frames'])==1800
assert sha(s/'idle.aseprite')=='f4cb8fff0a460cde6845fb15bc0c5e3271259d9d38d5f3efa051e4970b2e6127'
before=json.loads((e/'lead-review/preservation-before.json').read_text());assert all(sha(r/rel)==h for rel,h in before.items())
manual=json.loads((e/'lead-review/manual-review.json').read_text());assert manual['packet_sha256']==sha(e/'native-work/comparison-final/packet.json');assert manual['native_sha256']==sha(s/'idle.aseprite')
shutil.copy2(__file__,e/'lead-review/finalize-export.py')
q=e/'record.md';q.write_text(q.read_text()+'\nPackaged timings.json uses frames/idle-00.png through idle-03.png; these delivered paths resolve and match the exact tested engine textures. Final hash and path verification is recorded in final-verification.json.\n')
(e/'final-verification.json').write_text(json.dumps({'passed':True,'native_sha256':sha(s/'idle.aseprite'),'packet_manual_binding_exact':True,'timing_ms':1800,'prior_assets_preserved':len(before),'export_frames':rows,'publication':'not performed'},indent=2))
m={str(q.relative_to(r)):{'sha256':sha(q),'bytes':q.stat().st_size}for base in [e,s,x,p]for q in base.rglob('*')if q.is_file()and q.name!='artifact-hashes.json'};(e/'artifact-hashes.json').write_text(json.dumps(m,indent=2))
assert all(sha(r/rel)==v['sha256']for rel,v in m.items())
print(json.dumps({'passed':True,'new_artifacts_verified':len(m),'prior_assets_preserved':len(before),'native_sha256':sha(s/'idle.aseprite')}))
