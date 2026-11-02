from pathlib import Path
import hashlib,json,shutil
r=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning');p=r/'godot/stealth-fighter-playground-r02';e=r/'docs/experiments/2026-11-02-stealth-fighter-shadow-study-r01';sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
raw=json.loads(Path('/private/tmp/fighter-shadow-study-r01/live-debug.json').read_text());d=json.loads(raw['content'][0]['text']);assert d['errors']==[]and any('SHADOW_STUDY_READY'in s for s in d['output'])
shutil.copy2('/private/tmp/fighter-shadow-study-r01/live-debug.json',e/'evidence/live-debug.json')
status={'status':'running and left open for user interaction at handoff','project':str(p),'engine':'4.7.2.stable.official.ed1daf0bf','working_height':152,'default':'Single / B152 / Sprite colors','test_marker_absent':not(p/'RUN_CHECKS').exists(),'errors':[],'tested_script_bytes_exact':all((p/f).read_bytes()==(e/'tested-project'/f).read_bytes()for f in ['stage.gd','playground.gd','main.tscn','project.godot'])};assert status['tested_script_bytes_exact']
(e/'evidence/live-launch.json').write_text(json.dumps(status,indent=2))
q=e/'record.md';q.write_text(q.read_text()+'\nFinal saved r02 project launched through dedicated GodotMCP: SHADOW_STUDY_READY observed, errors[]. Script/config bytes equal the tested copy; no RUN_CHECKS marker. Left open at Single152 / Sprite colors. See evidence/live-launch.json.\n')
shutil.copy2(__file__,e/'finalize.py')
for rel in ['docs/handoff.md','docs/characters/stealth-fighter/brief.md','docs/characters/stealth-fighter/decisions.md']:
 q=r/rel;q.write_text(q.read_text().replace('##152px preferred; painted-shadow investigation —2November2026','## 152px preferred; painted-shadow investigation — 2 November 2026'))
m=json.loads((e/'artifact-hashes.json').read_text())
for q in [e/'record.md',e/'evidence/live-debug.json',e/'evidence/live-launch.json',e/'finalize.py',*p.glob('*.uid')]:m[str(q.relative_to(r))]={'sha256':sha(q),'bytes':q.stat().st_size}
assert all(sha(r/f)==v['sha256']for f,v in m.items());(e/'artifact-hashes.json').write_text(json.dumps(m,indent=2))
before=json.loads((e/'protected-before.json').read_text());assert all(sha(r/f)==h for f,h in before.items());print(json.dumps({'verified_new_artifacts':len(m),'protected_prior_files':len(before),'live':'Single152 / source colors','errors':[]}))
