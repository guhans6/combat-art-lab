"""Read actual final Godot viewport captures and compare opaque actor pixels."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];report=[]
for f in range(19):
 cap=Image.open(R/f'godot/evidence/runtime-frame-{f:02}.png').convert('RGBA');row={'frame':f+1,'capture_size':list(cap.size)}
 for v,x in [('clean',28),('smear',356)]:
  src=np.array(Image.open(R/f'exports/{v}-{f+1:02}.png').convert('RGBA'));render=np.array(cap.crop((x,39,x+256,247)));mask=src[:,:,3]>0;mask[80:120,210:222]=False;diff=np.any(src[:,:,:3]!=render[:,:,:3],2)&mask
  row[v]={'opaque_pixels_checked_outside_target':int(mask.sum()),'rgb_mismatch_count':int(diff.sum()),'max_rgb_delta':int(abs(src[:,:,:3].astype(int)-render[:,:,:3].astype(int))[mask].max())}
 report.append(row)
log=json.loads((R/'godot/evidence/event-log.json').read_text());inputs=json.loads((R/'proof/runtime-material03-inputs.json').read_text());fresh=all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in inputs.items());auto=[e for e in log['loop_events'] if e['loop']<=4];out={'runtime_frame_pixel_checks':report,'total_rgb_mismatch_count':sum(q[v]['rgb_mismatch_count'] for q in report for v in ['clean','smear']),'scope':'actualGodotviewport captures, opaque actorpixels outside provisionaldummyrectangle; continuousmotionperception separate','engine':log['engine'],'loop_events':log['loop_events'],'contact_events':log['contact_events'],'contact_errors':log['contact_errors'],'three_ab_loops_plus_clean_trail_probe_completed':len(auto)==4,'source_inputs':inputs,'source_inputs_fresh':fresh,'runtime_trail_source':log['runtime_trail'],'capture_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'godot/evidence').glob('*.png')}};(R/'proof/runtime-material03-checks.json').write_text(json.dumps(out,indent=2));assert out['total_rgb_mismatch_count']==0 and fresh and not out['contact_errors'] and len(auto)==4;print('Runtime:19x2 panels exact;3ABloops+Cprobe; sourcehashesfresh; no contacterrors')
