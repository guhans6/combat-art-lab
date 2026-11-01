from pathlib import Path
from PIL import Image
from tools.check_native_pilot import read
import hashlib,json
P=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol/reddit-motion-study/prototype');B=P.parent.parent;a=read(B/'pass01.aseprite');b=read(P/'pass01.aseprite');allowed=[3,4,5,7,10,11];mask=Image.open(P/'proof/allowed-mask.png').convert('L')
result={'native_sha256':hashlib.sha256((P/'pass01.aseprite').read_bytes()).hexdigest(),'canvas':b['canvas'],'layers':len(b['layers']),'cels':len(b['cels']),'header_equal':a['header']==b['header'],'layer_metadata_equal':a['layers']==b['layers'],'noncel_chunks_palette_tags_timing_equal':a['frames']==b['frames'],'cel_metadata_equal':True,'native_protection_violations':[],'frames':[]}
for key,old in a['cels'].items():
 f,l=key;new=b['cels'][key]
 if any(old[k]!=new[k]for k in ['geometry','opacity','z']):result['cel_metadata_equal']=False
 for y in range(192):
  for x in range(128):
   if old['image'].getpixel((x,y))!=new['image'].getpixel((x,y)) and (f not in [1,2,3]or l not in allowed or not mask.getpixel((x,y))):result['native_protection_violations'].append([f,l,x,y])
def holes(im):
 empty={(x,y)for y in range(192)for x in range(128)if im.getpixel((x,y))[3]==0};stack=[p for p in empty if p[0]in[0,127]or p[1]in[0,191]];seen=set(stack)
 while stack:
  x,y=stack.pop()
  for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if q in empty and q not in seen:seen.add(q);stack.append(q)
 return set(empty)-seen
native=[]
for f in range(8):
 im=Image.new('RGBA',(128,192))
 for l in range(1,12):im.alpha_composite(b['cels'][(f,l)]['image'])
 native.append(im);old=Image.open(B/f'frame-{f}.png').convert('RGBA');png=Image.open(P/f'frame-{f}.png').convert('RGBA');dy=1 if f in [1,2]else 0
 headexact=im.crop((0,0,128,44)).tobytes()==old.crop((0,dy,128,44+dy)).tobytes()
 registered=[]
 for l in [10,11]:
  before=a['cels'][(f,l)]['image'];expected=Image.new('RGBA',(128,192));expected.paste(before,(0,-dy));registered.append(expected.tobytes()==b['cels'][(f,l)]['image'].tobytes())
 rp=P/'proof/reopen'/f'frame-{f}.png'
 result['frames'].append({'frame':f+1,'duration_ms':b['frames'][f]['duration_ms'],'head_translation_y_px':-dy,'head_composite_exact_registered':headexact,'head_neck_hair_native_exact_registered':registered,'lower_body_y69_plus_exact':im.crop((0,69,128,192)).tobytes()==old.crop((0,69,128,192)).tobytes(),'feet_denim_tote_hands_native_exact':all(a['cels'][(f,l)]['image'].tobytes()==b['cels'][(f,l)]['image'].tobytes()for l in [1,2,6,8,9]),'blink_full_composite_exact':im.tobytes()==old.tobytes()if f in[4,5,6]else None,'png_native_exact':png.tobytes()==im.tobytes(),'fresh_reopen_png_exact':Image.open(rp).convert('RGBA').tobytes()==im.tobytes()if rp.exists()else None,'new_enclosed_alpha_holes':sorted(holes(im)-{(x,y-dy)if y<44 else(x,y) for x,y in holes(old)}),'coverage_head_holes_registered_y_px':-dy})
result['original_hashes_unchanged']={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in json.loads((P/'proof/input-hashes.json').read_text()).items()}
assert result['header_equal'] and result['layer_metadata_equal'] and result['noncel_chunks_palette_tags_timing_equal'] and result['cel_metadata_equal'] and not result['native_protection_violations']
for r in result['frames']:
 assert r['head_composite_exact_registered'] and all(r['head_neck_hair_native_exact_registered']) and r['lower_body_y69_plus_exact'] and r['feet_denim_tote_hands_native_exact'] and r['png_native_exact'] and not r['new_enclosed_alpha_holes'],r
assert all(result['original_hashes_unchanged'].values())
# Native GIF color/timing check separately from matte proof GIFs.
gif=Image.open(P/'pass01.gif');g=[]
for f,im in enumerate(native):
 gif.seek(f);actual=gif.convert('RGBA');g.append({'frame':f+1,'duration_ms':gif.info['duration'],'rgba_visible_exact':all((x==y)if x[3]else(y[3]==0)for x,y in zip(im.get_flattened_data(),actual.get_flattened_data()))})
assert all(r['rgba_visible_exact']and r['duration_ms']==b['frames'][i]['duration_ms']for i,r in enumerate(g))
result['native_gif']=g
sheet=Image.new('RGBA',(8*128,192))
for f,im in enumerate(native):sheet.alpha_composite(im,(f*128,0))
sheet.save(P/'proof/transparent-sheet.png')
(P/'proof/verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'native_sha256':result['native_sha256'],'all_protection_checks':True,'fresh_reopen':[r['fresh_reopen_png_exact']for r in result['frames']]},indent=2))
