from pathlib import Path
import json,hashlib,shutil
w=Path('/private/tmp/fighter-playground-r01');p=w/'project';(p/'textures').mkdir(parents=True,exist_ok=True);(p/'evidence').mkdir(exist_ok=True)
r=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning')
for i in range(4):shutil.copy2(r/'assets/export/stealth-fighter/idle-r02/frames'/f'idle-{i:02}.png',p/'textures'/f'idle-{i}.png')
for name in ['backgrounds.png','tileset.png']:shutil.copy2(w/name,p/'textures'/name)
shutil.copy2(w/'public-license.txt',p/'ART-LICENSE.txt')
(p/'project.godot').write_text('''config_version=5
[application]
config/name="Current A — The Quiet Keep"
run/main_scene="res://main.tscn"
config/features=PackedStringArray("4.7")
[display]
window/size/viewport_width=1280
window/size/viewport_height=800
window/size/window_width_override=1280
window/size/window_height_override=800
window/stretch/mode="viewport"
window/stretch/aspect="keep"
[rendering]
renderer/rendering_method="gl_compatibility"
textures/canvas_textures/default_texture_filter=0
environment/defaults/default_clear_color=Color(0.055,0.067,0.078,1)
''')
(p/'main.tscn').write_text('''[gd_scene load_steps=2 format=3]
[ext_resource type="Script" path="res://playground.gd" id="1"]
[node name="QuietKeep" type="Control"]
layout_mode=3
anchors_preset=15
anchor_right=1.0
anchor_bottom=1.0
script=ExtResource("1")
''')
protected={str(q.relative_to(r)):hashlib.sha256(q.read_bytes()).hexdigest()for folder in ['assets/concepts/stealth-fighter','assets/source/stealth-fighter','assets/export/stealth-fighter','assets/previews/stealth-fighter']for q in (r/folder).rglob('*')if q.is_file()}
(w/'protected-before.json').write_text(json.dumps(protected,indent=2))
print('Prepared',p,'protected',len(protected),'fighter inputs')
