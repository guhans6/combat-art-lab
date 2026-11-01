"""Audit observed Godot attack timing, contact, return and rendered source pixels."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
TOLERANCE_MS=50 # Three60Hz ticks for sampled wall-clock events, not art scoring.

def main():
 folder=ROOT/'artist';delivery=json.loads((folder/'delivery.json').read_text())
 target=ROOT/'runtime/godot';observation=json.loads((target/'evidence/attack-observation.json').read_text())
 count=len(delivery['durations_ms']);authored=sum(delivery['durations_ms']);active=set(delivery['active_frames_1based'])
 assert observation['source_sha256']==hashlib.sha256((folder/delivery['native']).read_bytes()).hexdigest()
 assert observation['synthetic_space_events_sent']==observation['space_events_received']==3
 assert len(observation['completed'])==len(observation['hit_events'])==3
 starts=[];elapsed=0
 for duration in delivery['durations_ms']:starts.append(elapsed);elapsed+=duration
 timing=[]
 for completed in observation['completed']:
  run=int(completed['attack']);events=[e for e in observation['frame_events'] if int(e['attack'])==run]
  assert {int(e['frame']) for e in events}==set(range(1,count+1)),f'Run{run} missingframeevents'
  assert completed['returned_to_idle'] and completed['state_after']=='idle' and completed['frame_after']==0
  assert abs(completed['duration_ms']-authored)<=TOLERANCE_MS,(run,completed['duration_ms'],authored)
  per_frame=[]
  for event in events:
   index=int(event['frame'])-1;deviation=event['elapsed_ms']-starts[index]
   assert abs(deviation)<=TOLERANCE_MS,(run,index+1,deviation)
   per_frame.append({'frame':index+1,'deviation_ms':deviation})
  hits=[e for e in observation['hit_events'] if int(e['attack'])==run];assert len(hits)==1
  hit=hits[0];frame=int(hit['frame']);assert frame in active
  assert starts[frame-1]-TOLERANCE_MS<=hit['elapsed_ms']<=starts[frame-1]+delivery['durations_ms'][frame-1]+TOLERANCE_MS
  timing.append({'run':run,'observed_duration_ms':completed['duration_ms'],'authored_duration_ms':authored,'frame_clock_deviations':per_frame,'hit_frame':frame,'hit_elapsed_ms':hit['elapsed_ms']})
 live={int(v) for v in observation['live_rendered_frames_0based']};inspection={int(v)-1 for v in observation['inspection_only_frames_1based']}
 assert live|inspection==set(range(count))
 assert not live&inspection
 checked=[]
 root=observation['base_root']
 for index,relative in enumerate(delivery['frames']):
  label='frame' if index in live else 'inspection-frame'
  with Image.open(target/f'evidence/runtime-{label}-{index:02d}.png') as image:capture=image.convert('RGB')
  with Image.open(folder/relative) as image:source=image.convert('RGBA')
  dx,dy=delivery['root_offsets'][index];mismatches=[]
  for y in range(source.height):
   for x in range(source.width):
    pixel=source.getpixel((x,y))
    if pixel[3] and capture.getpixel((x+int(root[0])+dx,y+int(root[1])+dy))!=pixel[:3]:mismatches.append([x,y])
  assert not mismatches,(index+1,mismatches[:8]);checked.append({'frame':index+1,'rendered_opaque_pixels_equal_source':True,'mode':'live playback capture' if index in live else 'paused pose inspection, not live capture'})
 for run in range(1,4):
  with Image.open(target/f'evidence/runtime-return-{run:02d}.png') as image:returned=image.convert('RGB')
  with Image.open(folder/delivery['frames'][0]) as image:source=image.convert('RGBA')
  assert all(not source.getpixel((x,y))[3] or returned.getpixel((x+int(root[0]),y+int(root[1])))==source.getpixel((x,y))[:3] for y in range(source.height) for x in range(source.width)),f'Return{run} pixels differ'
 report={'passed':True,'engine':observation['engine'],'tolerance_ms':TOLERANCE_MS,'timing':timing,'rendered_frames':checked,'live_frame_capture_count':len(live),'paused_inspection_count':len(inspection),'three_idle_returns_pixel_exact':True,'physical_keyboard_tested':False,'synthetic_space_route_tested':True,'limits':'Observed one-shot/synthetic input/declared-hitbox/return and pixel-timing proof. Not continuous agent temporal perception, cloth physics, final combat balance or user artistic approval.'}
 (ROOT/'runtime-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['timing','rendered_frames']},indent=2))
if __name__=='__main__':main()
