from PIL import Image,ImageDraw
from pathlib import Path
from collections import Counter
import hashlib,json
repo=Path(__file__).resolve().parents[3];out=Path(__file__).resolve().parent
roots=[repo/'docs/experiments/2026-10-30-idle-breathing-comparison/terra',repo/'docs/experiments/2026-10-30-natural-idle-sol',repo/'docs/experiments/2026-10-30-redrawn-breathing-sol']
labels=['A-left: earlier Terra','A-right: earlier Sol','B: latest redrawn Sol'];allims=[];reports=[]
for root,label in zip(roots,labels):
 files=sorted(root.glob('frame-*.png'),key=lambda p:int(p.stem.split('-')[-1]));ims=[Image.open(p).convert('RGBA') for p in files];allims.append(ims);base=ims[0]
 palette=set(p[:3] for p in base.getdata() if p[3]);frames=[]
 for k,im in enumerate(ims):
  hist=Counter(im.crop((53,45,67,66)).getdata());hist={('#%02x%02x%02x%02x'%c):n for c,n in hist.items()}
  frames.append({'frame':k+1,'visible_changes_vs_own_rest':sum(a!=b and bool(a[3] or b[3]) for a,b in zip(base.getdata(),im.getdata())),'new_rgb_vs_own_rest':len(set(p[:3] for p in im.getdata() if p[3])-palette),'fixed_shirt_core_roi_histogram':hist,'sha256':hashlib.sha256(files[k].read_bytes()).hexdigest()})
 reports.append({'label':label,'source':str(root),'frame_count':len(ims),'roi_halfopen':[53,45,67,66],'roi_warning':'Fixed unregistered core ROI; changes are observations, not automatic evidence of color drift or motion quality.','frames':frames})
# Exact 3x native poses on same matte. Representative rest and constructed peak, not synchronized timelines.
canvas=Image.new('RGB',(3*408,2*630),'#34363a');d=ImageDraw.Draw(canvas)
for j,(ims,label) in enumerate(zip(allims,labels)):
 for row,k in enumerate([0,2 if j<2 else 3]):
  x=j*408;y=row*630;d.text((x+10,y+8),f'{label}: F{k+1}',fill='white');m=Image.new('RGBA',(128,192),'#34363a');m.alpha_composite(ims[k]);canvas.paste(m.convert('RGB').resize((384,576),Image.Resampling.NEAREST),(x+10,y+32))
canvas.save(out/'normalized-rest-peak.png')
# Torso contact covers all actual frames, equal 4x crop; label durations from originals.
for j,(ims,label) in enumerate(zip(allims,labels)):
 c=Image.new('RGB',(4*256,((len(ims)+3)//4)*240),'#34363a');dd=ImageDraw.Draw(c)
 for k,im in enumerate(ims):
  m=Image.new('RGBA',im.size,'#34363a');m.alpha_composite(im);x=(k%4)*256;y=(k//4)*240;dd.text((x+6,y+6),f'{label} F{k+1}',fill='white');c.paste(m.crop((32,33,96,85)).convert('RGB').resize((256,208),Image.Resampling.NEAREST),(x,y+26))
 c.save(out/f'torso-{j}.png')
inputs=[]
for path in [repo/'docs/experiments/2026-10-30-natural-idle-sol/proof/terra-left-sol-right-3x.gif',repo/'docs/experiments/2026-10-30-redrawn-breathing-sol/proof/neutral-3x.gif']:
 im=Image.open(path);ts=[]
 for k in range(im.n_frames):im.seek(k);ts.append(im.info['duration'])
 inputs.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':im.size,'frames':im.n_frames,'durations_ms':ts,'total_ms':sum(ts),'loop':im.info.get('loop')})
(out/'measurements.json').write_text(json.dumps({'inputs':inputs,'native_sequences':reports},indent=2)+'\n');print(json.dumps({'inputs':inputs,'native_frame_counts':[r['frame_count']for r in reports]},indent=2))
