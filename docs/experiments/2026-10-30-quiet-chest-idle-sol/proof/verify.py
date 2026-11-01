from tools.check_native_pilot import read
from PIL import Image,ImageDraw
from pathlib import Path
from collections import deque
import hashlib,json
P=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol');B=Path('docs/experiments/2026-10-30-natural-idle-sol');a=read(B/'pass01.aseprite');b=read(P/'pass01.aseprite')
times=[f['duration_ms'] for f in b['frames']];native=[];frames=[];before=[];changes=[];violations=[]
mask=Image.open(P/'proof/allowed-mask.png').convert('L')
for (f,l),cel in a['cels'].items():
 old=cel['image'];new=b['cels'][(f,l)]['image'];diff=[(x,y)for y in range(192)for x in range(128)if old.getpixel((x,y))!=new.getpixel((x,y))]
 changes.append({'frame':f+1,'layer':a['layers'][l]['name'],'pixels':len(diff)})
 bad=[(x,y)for x,y in diff if f not in [1,2,3] or l not in [3,4,5,7] or not mask.getpixel((x,y))]
 if bad:violations.append({'frame':f+1,'layer':l,'coords':bad})
def holes(im):
 empty={(x,y)for y in range(192)for x in range(128)if im.getpixel((x,y))[3]==0};stack=[p for p in empty if p[0]in[0,127]or p[1]in[0,191]];seen=set(stack)
 while stack:
  x,y=stack.pop()
  for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if q in empty and q not in seen:seen.add(q);stack.append(q)
 return sorted(empty-seen)
def matte(im,scale=1):
 bg=Image.new('RGBA',im.size,(48,50,57,255));bg.alpha_composite(im);return bg.convert('RGB').resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
metrics=[]
for f in range(8):
 im=Image.new('RGBA',(128,192))
 for l in range(1,12):im.alpha_composite(b['cels'][(f,l)]['image'])
 png=Image.open(P/f'frame-{f}.png').convert('RGBA');old=Image.open(B/f'frame-{f}.png').convert('RGBA');assert im.tobytes()==png.tobytes()
 native.append(im);frames.append(matte(im));before.append(matte(old))
 metrics.append({'frame':f+1,'duration_ms':times[f],'png_native_equal':True,'head_rows_0_34_exact':im.crop((0,0,128,34)).tobytes()==old.crop((0,0,128,34)).tobytes(),'lower_body_rows_69_192_exact':im.crop((0,69,128,192)).tobytes()==old.crop((0,69,128,192)).tobytes(),'blink_composite_exact':im.tobytes()==old.tobytes() if f in [4,5,6] else None,'new_enclosed_hole_pixels':[p for p in holes(im)if p not in holes(old)],'opaque_pixels':sum(c[3]>0 for c in im.get_flattened_data())})
# One explicit palette shared by all frames, backgrounds, and both comparison panels.
colors=sorted(set(c for im in frames+before for c in im.get_flattened_data()));assert len(colors)<=256,len(colors)
pal=Image.new('P',(1,1));flat=[v for c in colors for v in c];pal.putpalette(flat+[0]*(768-len(flat)))
def exactgif(ims,path):
 quant=[]
 color_ids={c:i for i,c in enumerate(colors)}
 for im in ims:
  qi=Image.new('P',im.size);qi.putpalette(pal.getpalette());qi.putdata([color_ids[c]for c in im.get_flattened_data()]);quant.append(qi)
 quant[0].save(path,save_all=True,append_images=quant[1:],duration=times,loop=0,disposal=2,optimize=False)
 actual=Image.open(path);durs=[];matches=[]
 for f,im in enumerate(ims):actual.seek(f);durs.append(actual.info['duration']);matches.append(actual.convert('RGB').tobytes()==im.tobytes())
 assert all(matches)and durs==times,(path,matches,durs)
 return {'frames_exact':matches,'durations_ms':durs,'loop':actual.info.get('loop')}
gifs={}
gifs['neutral-1x']=exactgif(frames,P/'proof/neutral-1x.gif')
gifs['neutral-3x']=exactgif([im.resize((384,576),Image.Resampling.NEAREST)for im in frames],P/'proof/neutral-3x.gif')
pairs=[]
for old,new in zip(before,frames):
 pair=Image.new('RGB',(768,576),(48,50,57));pair.paste(old.resize((384,576),Image.Resampling.NEAREST));pair.paste(new.resize((384,576),Image.Resampling.NEAREST),(384,0));pairs.append(pair)
gifs['shrug-left-quiet-right']=exactgif(pairs,P/'proof/shrug-left-quiet-right-3x.gif')
contact=Image.new('RGB',(4*384,2*606),(48,50,57));d=ImageDraw.Draw(contact)
for i,f in enumerate(frames):
 x=i%4*384;y=i//4*606;contact.paste(f.resize((384,576),Image.Resampling.NEAREST),(x,y+30));d.text((x+5,y+8),f'F{i+1} {times[i]}ms',fill='white')
contact.save(P/'proof/contact-3x.png')
contact1=Image.new('RGB',(8*128,212),(48,50,57));d=ImageDraw.Draw(contact1)
for i,im in enumerate(frames):contact1.paste(im,(i*128,20));d.text((i*128+5,4),str(i+1),fill='white')
contact1.save(P/'proof/contact-1x.png')
result={'native_sha256':hashlib.sha256((P/'pass01.aseprite').read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256((B/'pass01.aseprite').read_bytes()).hexdigest(),'header_equal':a['header']==b['header'],'layers_equal':a['layers']==b['layers'],'noncel_chunks_timing_palette_equal':a['frames']==b['frames'],'cel_geometry_opacity_z_equal':all(all(c[k]==b['cels'][key][k] for k in ['geometry','opacity','z'])for key,c in a['cels'].items()),'protected_violations':violations,'changes':[r for r in changes if r['pixels']],'frames':metrics,'gif':gifs,'shared_gif_colors':len(colors)}


# Fixed anatomical landmarks compare to neutral F1; removal of rejected shrug is intentional.
rest=native[0]
shoulder_checks=[]
for f,im in enumerate(native):
 # Whole upper shoulder strip outside neck, plus outer sleeve regions and all alpha.
 regions=[(0,0,128,34),(30,34,53,44),(72,34,96,44),(0,44,46,69),(74,44,128,69),(0,69,128,192)]
 # First region includes intentional blink: compare per-frame old PNG there.
 vals=[im.crop(r).tobytes()==(Image.open(B/f'frame-{f}.png').convert('RGBA') if k==0 else rest).crop(r).tobytes()for k,r in enumerate(regions)]
 shoulder_checks.append({'frame':f+1,'head_perframe_shoulders_sleeves_lower_fixed':vals,'alpha_exact_rest':im.getchannel('A').tobytes()==rest.getchannel('A').tobytes()})
result['anatomical_fixed_regions']=shoulder_checks
result['original_hashes_unchanged']={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in json.loads((P/'proof/input-hashes.json').read_text()).items()}
result['reopen_png_equal']=[Image.open(P/'proof/reopen'/f'frame-{f}.png').convert('RGBA').tobytes()==im.tobytes() for f,im in enumerate(native)] if (P/'proof/reopen/frame-0.png').exists() else 'pending'
# Torso poses: actual exported pixels on light matte, not planning pixels.
contact=Image.new('RGB',(4*390,2*300),(225,225,225));d=ImageDraw.Draw(contact)
for i,im in enumerate(native):
 bg=Image.new('RGBA',im.size,(225,225,225,255));bg.alpha_composite(im)
 contact.paste(bg.convert('RGB').crop((30,30,95,75)).resize((390,270),Image.Resampling.NEAREST),(i%4*390,i//4*300+30));d.text((i%4*390+4,i//4*300+6),f'F{i+1} {times[i]}ms',fill='black')
contact.save(P/'proof/torso-contact-6x.png')
sheet=Image.new('RGBA',(128*8,192))
for f,im in enumerate(native):sheet.alpha_composite(im,(128*f,0))
sheet.save(P/'proof/transparent-sheet.png')
assert not violations
assert all(all(r['head_perframe_shoulders_sleeves_lower_fixed']) and r['alpha_exact_rest'] for r in shoulder_checks)
assert all(result['original_hashes_unchanged'].values())
assert result['header_equal'] and result['layers_equal'] and result['noncel_chunks_timing_palette_equal'] and result['cel_geometry_opacity_z_equal']
assert all(not m['new_enclosed_hole_pixels'] for m in metrics)
(P/'proof/verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('All fixed shoulder/sleeve/head/lower-body, alpha, original hash, native metadata checks passed')

# Distinguish removal of the rejected hoist from the newly authored chest motion.
internal_only=[]
for f in [1,2,3]:
 bad=[]
 for l in [3,4,5,7]:
  neutral=b['cels'][(0,l)]['image'];current=b['cels'][(f,l)]['image']
  for y in range(192):
   for x in range(128):
    if not(46<=x<73 and 44<=y<67) and neutral.getpixel((x,y))!=current.getpixel((x,y)):bad.append([l,x,y])
 internal_only.append({'frame':f+1,'all_garment_motion_inside_chest_box':not bad,'violations':bad,'composite_difference_from_rest':sum(x!=y for x,y in zip(native[0].get_flattened_data(),native[f].get_flattened_data()))})
assert all(v['all_garment_motion_inside_chest_box'] for v in internal_only)
assert all(result['reopen_png_equal'])
assert all(metrics[f]['blink_composite_exact'] for f in [4,5,6])
result['chest_only_motion_vs_neutral']=internal_only
(P/'proof/verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'native_sha256':result['native_sha256'],'reopen_png_equal':result['reopen_png_equal'],'chest_motion':internal_only,'passed':True},indent=2))
