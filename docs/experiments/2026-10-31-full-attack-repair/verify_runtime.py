from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parent;E=R/'runtime/godot/evidence'
meta=json.loads((R/'delivery.json').read_text());obs=json.loads((E/'attack-observation.json').read_text())
def require(test,message):
 if not test:raise RuntimeError(message)
require(obs['source_sha256']==meta['native_sha256'],'runtime artifact mismatch')
require(len(obs['completed'])==3 and all(c['hit'] and c['returned_to_idle'] for c in obs['completed']),'contact/return failure')
require(len(obs['hit_events'])==3 and all(e['frame']==6 for e in obs['hit_events']),'active frame mismatch')
require(obs['synthetic_space_events_sent']==obs['space_events_received']==3,'synthetic input path failure')
require(set(obs['live_rendered_frames_0based'])==set(range(13)) and not obs['inspection_only_frames_1based'],'missing live captures')
require(all(abs(c['duration_ms']-sum(meta['durations_ms']))<=50 for c in obs['completed']),'duration outside observed-frame allowance')
counts=[]
for i,path in enumerate(meta['frames']):
 frame=Image.open(R/path).convert('RGBA');shot=Image.open(E/f'runtime-frame-{i:02}.png').convert('RGB');n=0
 for y in range(192):
  for x in range(320):
   p=frame.getpixel((x,y))
   if p[3]:require(shot.getpixel((x+30,y+69))==p[:3],f'live pixels differ F{i+1} at{x,y}');n+=bool(p[3])
 counts.append(n)
idle=Image.open(R/meta['frames'][0]).convert('RGBA')
for i in range(1,4):
 shot=Image.open(E/f'runtime-return-{i:02}.png').convert('RGB')
 for y in range(192):
  for x in range(320):
   p=idle.getpixel((x,y))
   if p[3]:require(shot.getpixel((x+30,y+69))==p[:3],f'non-neutral runtime return{i}')
report={'native_sha256':meta['native_sha256'],'engine':obs['engine'],'target':'isolated macOS Godot desktop preview, OpenGL Compatibility, nearest filtering','viewport':obs['viewport'],'root':obs['base_root'],'window_scale':2,'attacks':3,'contacts':3,'active_frame':6,'exact_idle_returns':3,'live_captures':13,'opaque_pixel_exact_counts':counts,'durations_ms':[c['duration_ms'] for c in obs['completed']],'authored_ms':sum(meta['durations_ms']),'timing_allowance_ms':50,'physical_keyboard_tested':False,'continuous_temporal_perception_by_agent':False,'limits':'Synthetic input and copied fixture; bounds-based contact, not collision tuning or artistic acceptance.'}
(R/'review/runtime-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
