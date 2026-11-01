from pathlib import Path
import json,shutil
H=Path(__file__).resolve().parent;R=H.parents[2];P=R/'godot/standing-idle-lab';(P/'textures/environment').mkdir(parents=True,exist_ok=True);(P/'evidence').mkdir(exist_ok=True)
shutil.copy2(H/'standing-cleaned.png',P/'textures/standing.png')
for p in H.glob('environment-*.png'):
 if p.name in ['environment-parts.png','environment-parts-reopened.png']:continue
 shutil.copy2(p,P/'textures/environment'/p.name)
D=json.loads((H/'construction-data.json').read_text());(P/'textures/environment-layout.json').write_text(json.dumps({'layers':D['background_layers'],'shop_layers':['05-near-shop-wall','07-shop-glass','08-shop-awning','09-shop-posts','10-shop-steps','13-shop-lamp-pixels']},indent=2)+'\n')
(P/'project.godot').write_text('''; Isolated art-pipeline preview, not a game scaffold.
config_version=5

[application]
config/name="Standing Idle - Combat Art Lab"
run/main_scene="res://main.tscn"

[display]
window/size/viewport_width=362
window/size/viewport_height=296
window/size/window_width_override=724
window/size/window_height_override=592
window/stretch/mode="viewport"
window/stretch/scale_mode="integer"

[rendering]
renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"
textures/default_filters/use_nearest_mipmap_filter=false
textures/canvas_textures/default_texture_filter=0
environment/defaults/default_clear_color=Color(0.09,0.09,0.12,1)
''')
(P/'main.tscn').write_text('''[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://preview.gd" id="1"]

[node name="StandingIdleLab" type="Node2D"]
texture_filter = 1
script = ExtResource("1")
''')
print(P)
