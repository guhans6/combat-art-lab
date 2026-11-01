import sys,json,hashlib
from pathlib import Path
from PIL import Image
sys.path.insert(0,'docs/experiments/2026-10-30-evidence-idle-four-model/sol61')
from native_read import read,composite,sha,rgba_equal,holes
R=Path('docs/experiments/2026-10-31-recovery-grip/artist');B=Path('docs/experiments/2026-10-30-tote-attack/artist/sol-rescue/source/tote-attack-v03.aseprite')
b=read(B);a=read(R/'source/recovery-grip-pass02.aseprite');mask=Image.open(R/'proof/allowed-mask.png')
changed={};viol=[]
for key in b['cels']:
 p=b['cels'][key]['image'];q=a['cels'][key]['image'];xy=[(x,y) for y in range(192) for x in range(320) if p.getpixel((x,y))!=q.getpixel((x,y))]
 if xy:
  changed[str(key)]={'pixels':len(xy),'bbox_half_open':[min(x for x,y in xy),min(y for x,y in xy),max(x for x,y in xy)+1,max(y for x,y in xy)+1],'outside_mask':sum(not mask.getpixel(p) for p in xy)}
  if key[0]!=8 or key[1] not in [2,4,5,6] or changed[str(key)]['outside_mask']:viol.append(str(key))
 assert b['cels'][key]['geometry']==a['cels'][key]['geometry']
 for m in ['opacity','z','type']:assert b['cels'][key][m]==a['cels'][key][m]
assert set(b['cels'])==set(a['cels']) and b['layers']==a['layers'] and b['frames']==a['frames'] and b['canvas']==a['canvas'] and not viol
p=composite(b,8);q=composite(a,8);png=Image.open(R/'proof/recovery-grip-pass02.png').convert('RGBA');assert all(u==v or not(u[3] or v[3]) for u,v in zip(q.getdata(),png.getdata()))
xy=[(x,y) for y in range(192) for x in range(320) if p.getpixel((x,y))!=q.getpixel((x,y))]
newcols=sorted(set(q.getdata())-set(p.getdata()));assert not newcols
report={'native_sha256':sha(R/'source/recovery-grip-pass02.aseprite'),'baseline_original_hash':sha(B),'changed_native_cels_0based':changed,'all_other_cels_exact':True,'layers_palette_chunks_frame_durations_exact':True,'all_cel_geometry_opacity_type_z_exact':True,'canonical_native_composite_equals_MCP_export':True,'PNG_invisible_RGB_difference_count':sum(u!=v for u,v in zip(q.getdata(),png.getdata())),'composite_changed_pixels':len(xy),'composite_bbox_half_open':[min(x for x,y in xy),min(y for x,y in xy),max(x for x,y in xy)+1,max(y for x,y in xy)+1],'outside_mask':sum(not mask.getpixel(p) for p in xy),'new_visible_colors':newcols,'partial_alpha':sum(0<p[3]<255 for p in q.getdata()),'enclosed_transparent_pixels_before':len(holes(p)),'enclosed_transparent_pixels_after':len(holes(q)),'new_enclosed_transparent_pixels':sorted(holes(q)-holes(p)),'evidence_limit':'mechanical protection check; shape, anatomy and grip approval remain visual decisions'}
(R/'proof/pass02-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
