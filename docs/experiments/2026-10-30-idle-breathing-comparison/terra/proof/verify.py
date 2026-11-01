from tools.check_native_pilot import read
from PIL import Image,ImageChops,ImageDraw
from pathlib import Path
import json,hashlib
p=Path('docs/experiments/2026-10-30-idle-breathing-comparison/terra'); base=Path('docs/experiments/2026-10-30-idle-breath-blink/luna'); src=base/'passes/pass01/luna6-idle-breath-blink-pass01.aseprite';a=read(src); b=read(p/'pass01.aseprite')
boxes={3:(35,39,50,62),4:(77,39,91,62),5:(54,46,65,69)}; violations=[]; counts={}
for key,cel in a['cels'].items():
 f,l=key; before=cel['image'];after=b['cels'][key]['image'];coords=[]
 for y in range(192):
  for x in range(128):
   if before.getpixel((x,y))!=after.getpixel((x,y)):
    coords.append((x,y)); box=boxes.get(l)
    if f not in (1,2,3) or not box or not(box[0]<=x<box[2] and box[1]<=y<box[3]): violations.append([f,l,x,y])
 counts[f'{f}:{l}']=len(coords)
frames=[]; panels=[]; times=[600,350,550,600,50,80,50,250];metrics=[]
for i in range(8):
 before=Image.open(base/f'exports/pass01/frame-{i}.png').convert('RGBA');after=Image.open(p/f'frame-{i}.png').convert('RGBA');re=Image.open(p/f'proof/reopen-{i}.png').convert('RGBA')
 dif=[(x,y) for y in range(192) for x in range(128) if before.getpixel((x,y))!=after.getpixel((x,y))];lost=[(x,y) for x,y in dif if before.getpixel((x,y))[3] and not after.getpixel((x,y))[3]]
 metrics.append({'frame':i,'changed':len(dif),'alpha_lost':len(lost),'alpha_gained':sum(not before.getpixel(pt)[3] and after.getpixel(pt)[3]>0 for pt in dif),'reopen_pixels_equal':after.tobytes()==re.tobytes()})
 def matte(im):
  back=Image.new('RGBA',im.size,(48,50,57,255));back.alpha_composite(im);return back.convert('RGB').resize((384,576),Image.Resampling.NEAREST)
 f=matte(after);frames.append(f)
 pair=Image.new('RGB',(768,606),(48,50,57));pair.paste(matte(before),(0,30));pair.paste(f,(384,30));d=ImageDraw.Draw(pair);d.text((6,8),'BASELINE',fill='white');d.text((390,8),'TERRA pass01',fill='white');panels.append(pair)
frames[0].save(p/'proof/neutral-3x.gif',save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=2,optimize=False)
panels[0].save(p/'proof/baseline-vs-pass01.gif',save_all=True,append_images=panels[1:],duration=times,loop=0,disposal=2,optimize=False)
contact=Image.new('RGB',(4*384,2*606),(48,50,57));d=ImageDraw.Draw(contact)
for i,im in enumerate(frames):
 x=(i%4)*384;y=(i//4)*606;contact.paste(im,(x,y+30));d.text((x+4,y+8),f'F{i+1} {times[i]}ms',fill='white')
contact.save(p/'proof/contact.png')
gif=Image.open(p/'pass01.gif');dur=[]
for i in range(gif.n_frames):gif.seek(i);dur.append(gif.info.get('duration'))
result={'metadata_header_equal':a['header']==b['header'],'noncel_chunks_equal':a['frames']==b['frames'],'layers_equal':a['layers']==b['layers'],'all_cels_equal_set':a['cels'].keys()==b['cels'].keys(),'protected_pixel_violations':violations,'changes_per_layer_frame':counts,'frames':metrics,'gif_durations_ms':dur,'gif_loop':gif.info.get('loop'),'baseline_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256((p/'pass01.aseprite').read_bytes()).hexdigest()}
(p/'proof/verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
