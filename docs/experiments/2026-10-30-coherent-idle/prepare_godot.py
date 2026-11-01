"""Prepare an isolated copy of the existing preview; never replace current textures."""
from pathlib import Path
import shutil,json
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
source=REPO/'godot/standing-idle-lab';target=ROOT/'godot-preview'
if target.exists():raise SystemExit('Existing preview preserved; choose a fresh target')
shutil.copytree(source,target,ignore=shutil.ignore_patterns('.godot','evidence','.DS_Store'))
(target/'evidence').mkdir()
frames=target/'textures/coherent-v02';frames.mkdir()
for f in range(8):shutil.copy2(ROOT/f'exports/frame-{f:02d}.png',frames/f'frame-{f:02d}.png')
times=json.loads((ROOT/'exports/timing.json').read_text())['durations_ms']
layout={'canvas':[128,192],'durations_ms':times,'frame_directory':'res://textures/coherent-v02','alpha_review_region':[0,34,128,192],'intentional_alpha_holes':[[[63,116]] for _ in times],'ground_anchor':[68,185],'root_position':[88,69],'filter':'nearest','source_native_sha256':json.loads((ROOT/'verification.json').read_text())['native_sha256']}
(target/'textures/idle-layout.json').write_text(json.dumps(layout,indent=2)+'\n')
p=target/'preview.gd';s=p.read_text().replace('Vector2(108, 48)','Vector2(88, 69)').replace('root=(108,48)','root=(88,69)').replace('\t_verify_modular_shop()','\t# Shop modification exercise omitted for this character playback observation.')
s=s.replace('print("ART_LAB_LOOP %d" % loop_count)','''print("ART_LAB_LOOP %d" % loop_count)
	if loop_count == 3:
		var output := FileAccess.open("res://evidence/coherent-runtime.json", FileAccess.WRITE)
		output.store_string(JSON.stringify({"engine":Engine.get_version_info()["string"],"loops":loop_count,"frames":character.sprite_frames.get_frame_count("idle"),"durations_ms":[1100,180,120,360,220,160,240,1000],"root":[88,69],"viewport":[362,304],"filter":"nearest","native_scale":1,"default_window_scale":2,"display_server":DisplayServer.get_name(),"events":frame_events},"\\t"))
		print("COHERENT_IDLE_THREE_LOOPS_OK")
		# Keep preview alive for dedicated-MCP debug inspection.''')
s=s.replace('part.texture = load("res://textures/environment/environment-%s.png" % layer_name)', 'part.texture = ImageTexture.create_from_image(_read_preview_png("res://textures/environment/environment-%s.png" % layer_name))')
p.write_text(s)
project=target/'project.godot';s=project.read_text().replace('Standing Idle - Combat Art Lab','Coherent Idle v02 - isolated preview');project.write_text(s)
print(target)
