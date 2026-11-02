from pathlib import Path
import json,hashlib,shutil
r=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning');p=r/'godot/stealth-fighter-playground-r01';e=r/'docs/experiments/2026-11-02-stealth-fighter-playground-r01';sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
raw=json.loads(Path('/private/tmp/fighter-playground-r01/live-mcp-debug.json').read_text());data=json.loads(raw['content'][0]['text']);assert data['errors']==[];assert any('PLAYGROUND_READY' in s for s in data['output'])
shutil.copy2('/private/tmp/fighter-playground-r01/live-mcp-debug.json',e/'evidence/live-project-debug.json')
q=e/'evidence/live-launch.json';q.write_text(json.dumps({'project':str(p),'engine':'4.7.2.stable.official.ed1daf0bf','status':'running and left open for user interaction at handoff','self_test_marker_absent':not(p/'RUN_CHECKS').exists(),'errors':data['errors'],'main_script_sha256':sha(p/'playground.gd'),'stage_script_sha256':sha(p/'stage.gd'),'validated_copy_identical_scripts':all((p/n).read_bytes()==(e/'tested-project'/n).read_bytes()for n in ['stage.gd','playground.gd','project.godot','main.tscn'])},indent=2));assert json.loads(q.read_text())['validated_copy_identical_scripts']
q=e/'record.md';q.write_text(q.read_text()+'\nFinal saved project launched through dedicated GodotMCP from godot/stealth-fighter-playground-r01. PLAYGROUND_READY observed, errors[]. Same script/config bytes as tested copy, RUN_CHECKS absent. Final instance left running for the user, unlike the stopped test instance. See evidence/live-launch.json and live-project-debug.json.\n')
shutil.copy2(__file__,e/'finalize.py')
m=json.loads((e/'artifact-hashes.json').read_text())
for q in [e/'evidence/live-project-debug.json',e/'evidence/live-launch.json',e/'record.md',e/'finalize.py',*p.glob('*.uid')]:m[str(q.relative_to(r))]={'sha256':sha(q),'bytes':q.stat().st_size}
assert all(sha(r/f)==v['sha256']for f,v in m.items());(e/'artifact-hashes.json').write_text(json.dumps(m,indent=2))
before=json.loads((e/'protected-before.json').read_text());assert all(sha(r/f)==h for f,h in before.items());print(json.dumps({'verified_artifacts':len(m),'protected_fighter_files':len(before),'live_project':'running','errors':[]}))
