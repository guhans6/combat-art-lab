from pathlib import Path
import shutil,json,hashlib
r=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning');w=Path('/private/tmp/fighter-user-variants-r01');p=w/'project';src=r/'godot/stealth-fighter-playground-r02'
shutil.copytree(src,p,ignore=shutil.ignore_patterns('.godot','*.import','evidence','*.uid'))
(p/'evidence').mkdir(exist_ok=True)
shutil.copy2(r/'assets/export/stealth-fighter/idle-r02/frames/idle-00.png',p/'textures/current-rest.png')
for q in (p/'textures').glob('idle-*.png'):q.unlink()
meta=[{'source_id':0,'label':'Current A','short':'Original','file':'current-rest.png','native_canvas':[128,264],'body_height':240,'feet_y':253},{'source_id':1,'label':'1 · Quiet face','short':'Look 1','file':'variant-01.png','native_canvas':[128,264],'body_height':240,'feet_y':253},{'source_id':3,'label':'3 · Broad cap','short':'Look 3','file':'variant-03.png','native_canvas':[128,264],'body_height':240,'feet_y':253},{'source_id':4,'label':'4 · Chunky planes','short':'Look 4','file':'variant-04.png','native_canvas':[128,264],'body_height':240,'feet_y':253},{'source_id':5,'label':'5 · Narrow cap','short':'Look 5','file':'variant-05.png','native_canvas':[128,264],'body_height':240,'feet_y':253}]
(p/'variants.json').write_text(json.dumps(meta,indent=2))
q=p/'project.godot';q.write_text(q.read_text().replace('Current A — 152px Lighting Study','Current A — Appearance Variants'))
files=[]
for folder in ['assets/concepts/stealth-fighter','assets/source/stealth-fighter','assets/export/stealth-fighter','godot/stealth-fighter-playground-r01','godot/stealth-fighter-playground-r02']:
 files.extend(q for q in(r/folder).rglob('*')if q.is_file()and'.godot'not in q.parts and q.suffix!='.import')
(w/'protected-before.json').write_text(json.dumps({str(q.relative_to(r)):hashlib.sha256(q.read_bytes()).hexdigest()for q in files},indent=2))
print('Prepared static appearance project; inputs pending native export')
