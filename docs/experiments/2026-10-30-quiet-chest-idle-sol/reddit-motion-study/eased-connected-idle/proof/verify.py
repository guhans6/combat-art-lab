from tools.check_native_pilot import read
from pathlib import Path
from PIL import Image
import hashlib,json
P=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol/reddit-motion-study/eased-connected-idle');a=read(P.parent/'prototype/pass01.aseprite');prepared=read(P/'proof/prepared-baseline.aseprite');b=read(P/'pass01.aseprite');m=json.loads((P/'proof/timing-map.json').read_text());mapping=m['old_frame_zero_based_mapping'];times=m['durations_ms'];mask=Image.open(P/'proof/allowed-mask.png').convert('L')
def compose(data,f):
 im=Image.new('RGBA',(128,192))
 for l in range(1,12):im.alpha_composite(data['cels'][(f,l)]['image'])
 return im
def holes(im):
 empty={(x,y)for y in range(192)for x in range(128)if im.getpixel((x,y))[3]==0};stack=[p for p in empty if p[0]in[0,127]or p[1]in[0,191]];seen=set(stack)
 while stack:
  x,y=stack.pop()
  for p in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if p in empty and p not in seen:seen.add(p);stack.append(p)
 return empty-seen
def field(f,x,y):
 centers={2:57,3:64,4:66,5:56};center=centers.get(f,0);stop=center if 47<=x<=74 else min(center,61)if 43<=x<=46 or 75<=x<=80 else min(center,59)if 39<=x<=42 or 81<=x<=85 else min(center,57)
 dy=1 if f in centers and y<=stop else 0
 ranges={1:(50,63),2:(52,68),3:(60,105),4:(56,117),5:(60,117),6:(66,113),7:(76,105)};span=ranges.get(f);dx=1 if span and span[0]<=y<=span[1]else 0
 return dx,dy
checks={'native_sha256':hashlib.sha256((P/'pass01.aseprite').read_bytes()).hexdigest(),'canvas':b['canvas'],'frame_count':len(b['frames']),'layers':len(b['layers']),'cels':len(b['cels']),'header_matches_prepared_retimed_baseline':prepared['header']==b['header'],'header_changed_legacy_speed_ms':{'before':600,'after':650},'original_header_except_legacy_speed_preserved':a['header'][:20]+a['header'][24:]==b['header'][:20]+b['header'][24:],'layers_preserved':a['layers']==b['layers'],'prepared_frame_metadata_palette_tags_unchanged':prepared['frames']==b['frames'],'durations_ms':[f['duration_ms']for f in b['frames']],'cycle_ms':sum(times),'cel_geometry_opacity_z_preserved':True,'protected_native_violations':[],'frames':[]}
# Only tag range and timing/frame count are intentional metadata differences vsold.
old0=[c for c in a['frames'][0]['non_cel_chunks']if c['type']!='0x2018'];new0=[c for c in b['frames'][0]['non_cel_chunks']if c['type']!='0x2018'];checks['original_non_tag_chunks_palette_exact']=old0==new0
for(f,l),cel in b['cels'].items():
 old=prepared['cels'][(f,l)]
 if any(old[k]!=cel[k]for k in['geometry','opacity','z']):checks['cel_geometry_opacity_z_preserved']=False
 for y in range(192):
  for x in range(128):
   if old['image'].getpixel((x,y))!=cel['image'].getpixel((x,y))and(l in[0,1]or f not in range(1,8)or not mask.getpixel((x,y))or y>=118):checks['protected_native_violations'].append([f,l,x,y])
native=[];coverage=[]
for f,s in enumerate(mapping):
 im=compose(b,f);native.append(im);old=compose(a,s);png=Image.open(P/f'frame-{f}.png').convert('RGBA');headsrc=compose(a,s if f in[8,9,10]else 0);dy=1 if f in[2,3,4,5]else 0
 hnative=[]
 for l in[10,11]:
  source=a['cels'][(s if f in[8,9,10]else 0,l)]['image'];shift=Image.new('RGBA',(128,192));shift.paste(source,(0,-dy));hnative.append(shift.tobytes()==b['cels'][(f,l)]['image'].tobytes())
 baselineholes=holes(compose(a,s if f in[8,9,10]else 0));newholes=holes(im);bad=[]
 for x,y in newholes:
  dx,up=field(f,x,y)
  if(x-dx,y+up)not in baselineholes:bad.append((x,y))
 coverage.append({'frame':f+1,'enclosed_hole_pixels':sorted(newholes),'unexplained_new_hole_pixels':bad})
 rp=P/'proof/reopen'/f'frame-{f}.png'
 checks['frames'].append({'frame':f+1,'old_source_frame':s+1,'head_translation_y_px':-dy,'head_composite_exact_registered':im.crop((0,0,128,44)).tobytes()==headsrc.crop((0,dy,128,44+dy)).tobytes(),'head_neck_hair_native_exact_registered':hnative,'lower_legs_y118_plus_exact':im.crop((0,118,128,192)).tobytes()==old.crop((0,118,128,192)).tobytes(),'shoes_native_exact':a['cels'][(s,1)]['image'].tobytes()==b['cels'][(f,1)]['image'].tobytes(),'hidden_guide_native_exact':a['cels'][(s,0)]['image'].tobytes()==b['cels'][(f,0)]['image'].tobytes(),'blink_full_composite_exact':im.tobytes()==old.tobytes()if f in[8,9,10]else None,'png_native_exact':im.tobytes()==png.tobytes(),'fresh_reopen_png_exact':Image.open(rp).convert('RGBA').tobytes()==im.tobytes()if rp.exists()else None})
checks['alpha_coverage']=coverage;checks['original_hashes_unchanged']={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in json.loads((P/'proof/input-hashes.json').read_text()).items()}
gif=Image.open(P/'pass01.gif');gc=[]
for f,im in enumerate(native):
 gif.seek(f);actual=gif.convert('RGBA');gc.append({'frame':f+1,'duration_ms':gif.info['duration'],'visible_pixels_exact':all((x==y)if x[3]else(y[3]==0)for x,y in zip(im.get_flattened_data(),actual.get_flattened_data()))})
checks['native_gif']=gc
assert checks['header_matches_prepared_retimed_baseline']and checks['original_header_except_legacy_speed_preserved']and checks['layers_preserved']and checks['prepared_frame_metadata_palette_tags_unchanged']and checks['original_non_tag_chunks_palette_exact']and checks['cel_geometry_opacity_z_preserved']and not checks['protected_native_violations']
assert checks['durations_ms']==times and len(times)==12
assert all(checks['original_hashes_unchanged'].values())
for r in checks['frames']:assert r['head_composite_exact_registered']and all(r['head_neck_hair_native_exact_registered'])and r['lower_legs_y118_plus_exact']and r['shoes_native_exact']and r['hidden_guide_native_exact']and r['png_native_exact'],r
assert all(checks['frames'][f]['blink_full_composite_exact']for f in[8,9,10])
assert all(r['visible_pixels_exact']and r['duration_ms']==times[i]for i,r in enumerate(gc))
assert all(not r['unexplained_new_hole_pixels']for r in coverage)
assert all(r['fresh_reopen_png_exact']for r in checks['frames'])
(P/'proof/verification.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps({'sha256':checks['native_sha256'],'structural_protection_checks':True,'new_holes':[(r['frame'],r['unexplained_new_hole_pixels'])for r in coverage if r['unexplained_new_hole_pixels']],'reopen':[r['fresh_reopen_png_exact']for r in checks['frames']]},indent=2))
