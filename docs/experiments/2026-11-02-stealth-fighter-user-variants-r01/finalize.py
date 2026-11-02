from pathlib import Path
import json,hashlib,shutil
r=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning');p=r/'godot/stealth-fighter-playground-r03';e=r/'docs/experiments/2026-11-02-stealth-fighter-user-variants-r01';sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
raw=json.loads(Path('/private/tmp/fighter-user-variants-r01/live-debug.json').read_text());v=json.loads(raw['content'][0]['text']);assert v['errors']==[]and any('APPEARANCE_STUDY_READY'in t for t in v['output'])
shutil.copy2('/private/tmp/fighter-user-variants-r01/live-debug.json',e/'godot-evidence/live-debug.json')
state={'project':str(p),'status':'running; left open for user comparison at handoff','engine':'4.7.2.stable.official.ed1daf0bf','source_ids':[0,1,3,4,5],'default_height':152,'static':True,'test_marker_absent':not(p/'RUN_CHECKS').exists(),'script_config_equal_tested_copy':all((p/f).read_bytes()==(e/'tested-project'/f).read_bytes()for f in ['playground.gd','stage.gd','project.godot','main.tscn']),'errors':[]};assert state['script_config_equal_tested_copy'];(e/'godot-evidence/live-launch.json').write_text(json.dumps(state,indent=2))
q=e/'record.md';q.write_text(q.read_text()+'\nSaved r03 project launched through dedicated GodotMCP from its final path. APPEARANCE_STUDY_READY observed with5staticlooks/default152, errors[]. Core scripts/config bytes equal the tested copy; RUN_CHECKS absent. Final instance is left running for user comparison. See godot-evidence/live-launch.json.\n')
shutil.copy2(__file__,e/'finalize.py')
m=json.loads((e/'artifact-hashes.json').read_text())
for q in [e/'record.md',e/'godot-evidence/live-debug.json',e/'godot-evidence/live-launch.json',e/'finalize.py',*p.glob('*.uid')]:m[str(q.relative_to(r))]={'sha256':sha(q),'bytes':q.stat().st_size}
assert all(sha(r/f)==a['sha256']for f,a in m.items());(e/'artifact-hashes.json').write_text(json.dumps(m,indent=2));before=json.loads((e/'protected-before.json').read_text());assert all(sha(r/f)==h for f,h in before.items())
print(json.dumps({'verified_artifacts':len(m),'protected_prior_files':len(before),'live':'r03 static appearance comparison at152px','errors':[]}))
