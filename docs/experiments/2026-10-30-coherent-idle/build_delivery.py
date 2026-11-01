"""Package real Aseprite exports without redrawing animation artwork."""
from pathlib import Path
import sys,json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[2]))
sys.path.insert(0,str(ROOT/'source'))
from prepare import states,PLAN,A
from native_read import read,composite,sha
sys.path.insert(0,str(ROOT.parent/'2026-10-30-evidence-idle-four-model'))
from check_deliveries import coverage
from gif_timeline import check as gif_check
MATTE='#34363a'

def rgb(im):
 bg=Image.new('RGBA',im.size,MATTE);bg.alpha_composite(im);return bg.convert('RGB')

def gif(path,frames,times,scale=1):
 frames=[rgb(im).resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST) for im in frames]
 colors=sorted(set(c for im in frames for c in im.get_flattened_data()))
 assert len(colors)<=256,'Exact GIF palette exceeded; no silent quantization'
 lookup={c:i for i,c in enumerate(colors)};palette=[v for c in colors for v in c]+[0]*(768-3*len(colors));ps=[]
 for im in frames:
  p=Image.new('P',im.size);p.putpalette(palette);p.putdata([lookup[c] for c in im.get_flattened_data()]);ps.append(p)
 ps[0].save(path,save_all=True,append_images=ps[1:],duration=times,loop=0,optimize=False,disposal=2)

def main():
 n=read(ROOT/'source/coherent-idle-v02.aseprite');poses=states();times=[ms for _,ms,_ in PLAN]
 raw=Image.open(ROOT/'exports/final-sheet.png').convert('RGBA');fresh=Image.open(ROOT/'reopen/sheet.png').convert('RGBA')
 assert raw.size==fresh.size==(1024,192) and raw.tobytes()==fresh.tobytes()
 frames=[];old=[composite(A,f) for f in range(8)]
 for f,(phase,ms,lift) in enumerate(PLAN):
  im=raw.crop((f*128,0,(f+1)*128,192));assert im.tobytes()==composite(n,f).tobytes()
  for l,target in poses[phase].items():assert target.tobytes()==n['cels'][(f,l)]['image'].tobytes(),(f,l)
  im.save(ROOT/f'exports/frame-{f:02d}.png');frames.append(im)
 assert n['canvas']==[128,192] and n['layers']==A['layers']
 assert [f['duration_ms'] for f in n['frames']]==times
 assert [c for c in n['chunks'] if c['type']==0x2019]==[c for c in A['chunks'] if c['type']==0x2019]
 protected=[0,1,2,6,8,9]
 for f,im in enumerate(frames):
  for l in protected:assert n['cels'][(f,l)]['image'].tobytes()==A['cels'][(0,l)]['image'].tobytes(),(f,l)
  assert im.crop((0,90,128,192)).tobytes()==old[0].crop((0,90,128,192)).tobytes()
 assert frames[0].tobytes()==frames[-1].tobytes()==old[0].tobytes()
 alpha=coverage(frames,old[0]);assert alpha['passed'],alpha
 # Native joint relation: the head/neck owners and primary garment poses must
 # match the same source key. These are declared pose constraints, not art scores.
 phase_audit=[]
 for name,data in [('original',A),('candidate',n)]:
  violations=[]
  for f in range(8):
   up=data['cels'][(f,3)]['image'].tobytes()==A['cels'][(3,3)]['image'].tobytes()
   head_up=data['cels'][(f,11)]['image'].tobytes()==A['cels'][(3,11)]['image'].tobytes()
   neck_up=data['cels'][(f,10)]['image'].tobytes()==A['cels'][(3,10)]['image'].tobytes()
   if len({up,head_up,neck_up})>1:violations.append(f+1)
  phase_audit.append({'artifact':name,'primary_pose_mismatch_frames_1based':violations})
 assert phase_audit[0]['primary_pose_mismatch_frames_1based']==[3,6]
 assert not phase_audit[1]['primary_pose_mismatch_frames_1based']
 for scale in [1,3]:gif(ROOT/f'exports/idle-{scale}x.gif',frames,times,scale)
 gif(ROOT/'exports/sol-original-1x.gif',old,times)
 # Both periods match intentionally; compare the native timeline without retiming.
 pair=[]
 for left,right in zip(old,frames):
  im=Image.new('RGBA',(272,212),MATTE);im.alpha_composite(left,(0,20));im.alpha_composite(right,(144,20));d=ImageDraw.Draw(im);d.fontmode='1';d.text((5,4),'Original Sol 6.1',fill='white');d.text((149,4),'Coherent v02',fill='white');pair.append(im)
 gif(ROOT/'review/comparison-3x.gif',pair,times,3)
 contact=Image.new('RGB',(4*128,2*222),MATTE);d=ImageDraw.Draw(contact)
 for f,im in enumerate(frames):
  x=f%4*128;y=f//4*222;contact.paste(rgb(im),(x,y+30));d.text((x+3,y+2),f'F{f+1} {times[f]}ms',fill='white');d.text((x+3,y+15),PLAN[f][0],fill='white')
 contact.save(ROOT/'review/contact-1x.png');contact.resize((1024,888),Image.Resampling.NEAREST).save(ROOT/'review/contact-2x.png')
 torso=Image.new('RGB',(8*54,2*76),MATTE);d=ImageDraw.Draw(torso)
 for row,sequence in enumerate([old,frames]):
  for f,im in enumerate(sequence):
   x=f*54;y=row*76;torso.paste(rgb(im).crop((36,29,90,87)),(x,y+18));d.text((x+1,y+2),f'{["Old","New"][row]} F{f+1}',fill='white')
 torso.resize((1728,608),Image.Resampling.NEAREST).save(ROOT/'review/torso-old-new-4x.png')
 # Reference/candidate review with explicit reference scaling, no source edits.
 ref=Image.open(ROOT.parents[2]/'assets/references/approved-2026-10-26/character-scene.png').convert('RGB')
 ref.thumbnail((480,480))
 comparison=Image.new('RGB',(1000,606),MATTE);comparison.paste(ref,(0,40));comparison.paste(rgb(old[0]).resize((256,384),Image.Resampling.NEAREST),(480,40));comparison.paste(rgb(frames[3]).resize((256,384),Image.Resampling.NEAREST),(744,40));d=ImageDraw.Draw(comparison)
 for x,t in [(5,'Approved concept: display reduction'),(480,'Sol rest: native 2x'),(744,'Candidate inhale: native 2x')]:d.text((x,10),t,fill='white')
 comparison.save(ROOT/'review/reference-sol-candidate.png')
 gifchecks={str(s):gif_check(ROOT/f'exports/idle-{s}x.gif',frames,times,s) for s in [1,3]}
 revision=read(ROOT/'source/coherent-idle-v01.aseprite');delta=[]
 for f in range(8):
  changes=[]
  for l in range(12):
   a=revision['cels'][(f,l)]['image'];b=n['cels'][(f,l)]['image']
   points=[(x,y) for y in range(192) for x in range(128) if a.getpixel((x,y))!=b.getpixel((x,y))]
   if points:changes.append({'layer':l,'points':points})
  delta.append(changes)
 assert all(delta[f]==([{'layer':5,'points':[(60,55),(61,55)]}] if f in [2,3,4] else []) for f in range(8))
 report={'native':str(ROOT/'source/coherent-idle-v02.aseprite'),'native_sha256':sha(ROOT/'source/coherent-idle-v02.aseprite'),'canvas':[128,192],'frames':8,'durations_ms':times,'cycle_ms':sum(times),'all_native_targets_and_fresh_exports_exact':True,'native_original_layer_metadata_and_palette_exact':True,'protected_layers':[n['layers'][l]['name'] for l in protected],'lower_body_y90_plus_exact':True,'loop_seam_exact_rest':True,'primary_phase_audit':phase_audit,'alpha':alpha,'gifs':gifchecks,'localized_v01_v02_edit':delta,'artistic_approval':'pending user','temporal_perception':'not established by decoded frames','godot':'separate runtime report'}
 (ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 (ROOT/'exports/timing.json').write_text(json.dumps({'durations_ms':times,'cycle_ms':sum(times),'loop':True,'tag':'idle-coherent','root_offset':[0,0],'ground_row':185,'frame_size':[128,192]},indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k in ['native_sha256','all_native_targets_and_fresh_exports_exact','primary_phase_audit','lower_body_y90_plus_exact','loop_seam_exact_rest','cycle_ms']},indent=2))
if __name__=='__main__':main()
