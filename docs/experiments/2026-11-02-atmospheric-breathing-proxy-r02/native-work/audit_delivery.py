from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import json,sys,hashlib
P=Path('/private/tmp/atmospheric-breathing-proxy-r02');D=P/'delivery';sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(P/'baseline.aseprite');B=read(D/'traveler-breathing-r02.aseprite');E=read(D/'edit-proof.aseprite');R=json.load(open(P/'correction-ops.json'));layers=R['layers'];dur=R['durations_ms'];mask=Image.open(P/'editable-upperbody-frozen.png');expected='a34a66c188f0f3f63fd0bb06e1ccdf1ed68c82b2f8fe0b617e42489be1313417'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def eq(a,b):return a.tobytes()==b.tobytes()
def comp(a,f,omit=None):
 im=Image.new('RGBA',(96,160))
 for l,n in enumerate(layers):
  if n!=omit:im.alpha_composite(a['cels'][f,l]['image'])
 return im
def matte(im,c):
 out=Image.new('RGBA',im.size,c);out.alpha_composite(im);return out
def holes(im):
 s={(x,y)for y in range(160)for x in range(96)if not im.getpixel((x,y))[3]};out=[]
 while s:
  q=[s.pop()];edge=False
  for x,y in q:
   edge|=x in(0,95)or y in(0,159)
   for p in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if p in s:s.remove(p);q.append(p)
  if not edge:out.append(q)
 return out
assert sha(P/'baseline.aseprite')==expected and sha('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/source/atmospheric-traveler/breathing-r01/traveler-breathing.aseprite')==expected
assert A['header']==B['header']and A['layers']==B['layers']and A['frames']==B['frames']and A['cels'].keys()==B['cels'].keys();assert[f['duration_ms']for f in B['frames']]==dur
changed=[];frames=[];before=[];alpha=[];fixedowners={n:True for n in R['fixed']};hidden={};M=D/'masks';M.mkdir(exist_ok=True)
sheet=Image.open(D/'breath-sheet.png').convert('RGBA');reopen=Image.open(D/'reopened-sheet.png').convert('RGBA');assert eq(sheet,reopen)and sheet.size==(1152,160)
for f,pose in enumerate(R['mapping']):
 sf=R['pose_source_frames_0based'][pose];im=Image.open(D/f'breath-{f}.png').convert('RGBA');old=Image.open(P/f'before/breath-{f:02}.png').convert('RGBA');assert eq(old,comp(A,f));before.append(old);assert eq(im,comp(B,f))and eq(im,sheet.crop((f*96,0,(f+1)*96,160)));frames.append(im)
 assert eq(im.crop((0,102,96,160)),old.crop((0,102,96,160)))
 for l,n in enumerate(layers):
  a=A['cels'][f,l];b=B['cels'][f,l];assert all(a[x]==b[x]for x in['geometry','opacity','z'])
  if n in R['fixed']:assert eq(a['image'],b['image'])
  else:assert eq(b['image'],A['cels'][sf,l]['image'])
  pts=[(i%96,i//96)for i,(x,y)in enumerate(zip(a['image'].getdata(),b['image'].getdata()))if x!=y]
  if pts:assert n in R['moving']and all(mask.getpixel(p)for p in pts);changed.append({'frame':f+1,'owner':n,'changed_pixels':len(pts)})
  b['image'].getchannel('A').save(M/f'f{f:02}-{n}.png')
 assert not holes(im);assert set(im.getchannel('A').getdata())=={0,255};alpha.append({'frame':f+1,'enclosed_holes':0,'binary_alpha':True})
 for y in range(46,74):
  for x in range(45,51):assert im.getpixel((x,y))[3]==255
assert eq(frames[0],before[0])and eq(frames[-1],before[-1])and eq(frames[0],frames[-1]);assert len({im.tobytes()for im in frames})==4
for n in['neck-collar','thorax-coat','near-upper-sleeve','far-sleeve-hand']:
 l=layers.index(n);counts=[]
 for f in range(12):
  owner=B['cels'][f,l]['image'];above=Image.new('RGBA',(96,160))
  for q in range(l+1,len(layers)):above.alpha_composite(B['cels'][f,q]['image'])
  counts.append(sum(a[3]>0 and b[3]>0 for a,b in zip(owner.getdata(),above.getdata())))
 hidden[n]=counts;assert min(counts)>0
assert B['header']==E['header']and B['layers']==E['layers']and B['frames']==E['frames']and B['cels'].keys()==E['cels'].keys();edit_changed=[]
for k,b in B['cels'].items():
 e=E['cels'][k];assert all(b[x]==e[x]for x in['geometry','opacity','z']);pts=[(i%96,i//96)for i,(x,y)in enumerate(zip(b['image'].getdata(),e['image'].getdata()))if x!=y]
 if pts:edit_changed.append({'frame':k[0]+1,'owner':layers[k[1]],'pixels':pts})
assert edit_changed==[{'frame':1,'owner':'thorax-coat','pixels':[(47,75),(47,76),(47,77)]}]
edit=Image.open(D/'edit-proof.png').convert('RGBA');assert eq(edit,Image.open(D/'edit-proof-reopened.png').convert('RGBA'));assert eq(edit.getchannel('A'),frames[0].getchannel('A'));assert sum(a!=b for a,b in zip(edit.getdata(),frames[0].getdata()))==3
g=Image.open(D/'raw-mcp-breath.gif');gf=[(im.convert('RGBA').copy(),im.info.get('duration',0))for im in ImageSequence.Iterator(g)]
# GIF may legally coalesce adjacent identical poses: compare the complete authored timeline at every boundary.
def at(items,t):
 pos=0
 for im,ms in items:
  if t<pos+ms:return im
  pos+=ms
 raise AssertionError('timelineoutside')
assert sum(ms for _,ms in gf)==2800;rgbdiff=[];pos=0
for im,ms in zip(frames,dur):
 gi=at(gf,pos);assert eq(gi.getchannel('A'),im.getchannel('A'));rgbdiff.append(sum(a[:3]!=b[:3]for a,b in zip(gi.getdata(),im.getdata())if b[3]));pos+=ms
for sc in[1,2,3]:
 out=Image.new('RGB',(96*sc*4,(160*sc+24)*3),'#74797c');dr=ImageDraw.Draw(out)
 for f,im in enumerate(frames):
  x=f%4*96*sc;y=f//4*(160*sc+24);out.paste(matte(im,'#74797c').resize((96*sc,160*sc),Image.Resampling.NEAREST).convert('RGB'),(x,y+24));dr.text((x+3,y+4),f'{f+1} {dur[f]}ms {R["mapping"][f]}',fill='white')
 out.save(D/f'contact-{sc}x.png')
out=Image.new('RGB',(6*96,4*216),'#555960');dr=ImageDraw.Draw(out)
for f in range(12):
 for v,im in enumerate([before[f],frames[f]]):
  k=f*2+v;x=k%6*96;y=k//6*216;out.paste(matte(im,'#d0c7b4').crop((25,4,73,100)).resize((96,192),Image.Resampling.NEAREST).convert('RGB'),(x,y+24));dr.text((x+3,y+4),f'{f+1} '+['r01','r02'][v],fill='white')
out.save(D/'before-after-upper-all-2x.png')
out=Image.new('RGB',(6*120,4*180),'#74797c');dr=ImageDraw.Draw(out)
for f in range(12):
 for v,im in enumerate([before[f],frames[f]]):
  k=f*2+v;x=k%6*120;y=k//6*180;out.paste(matte(im,'#74797c').resize((90,149),Image.Resampling.NEAREST).convert('RGB'),(x+15,y+25));dr.text((x+3,y+4),f'{f+1} '+['r01','r02'][v],fill='white')
out.save(D/'before-after-fixed128rest.png')
out=Image.new('RGB',(360,210),'#74797c');dr=ImageDraw.Draw(out)
for j,im in enumerate([frames[0],edit]):out.paste(matte(im,'#74797c').crop((35,68,55,88)).resize((160,160),Image.Resampling.NEAREST).convert('RGB'),(j*180+10,30));dr.text((j*180+10,7),['originalfold','duplicate3pxnarrow'][j],fill='white')
out.save(D/'edit-proof-comparison-8x.png')
timings={'animation':'breath','canvas':[96,160],'rest_body_height_px':137,'feet_baseline_y':146,'root':[44,85],'loop':True,'total_ms':2800,'projection':'fixed128/137 scale allframes, no perposefitting','frames':[{'file':f'breath-{f}.png','duration_ms':dur[f],'pose':p,'lift_px':R['stages'][p][0],'chest_forward_px':R['stages'][p][1]}for f,p in enumerate(R['mapping'])]};json.dump(timings,open(D/'timings.json','w'),indent=2)
report={'passed':True,'baseline_sha256':expected,'native_sha256':sha(D/'traveler-breathing-r02.aseprite'),'canvas':[96,160],'frames':12,'unique_pose_drawings':4,'durations_ms':dur,'total_ms':2800,'native_layers':10,'native_cels':120,'palette_entries':14,'palette_header_metadata_layers_timing_allunchanged':True,'allcel_geometry_opacity_z_unchanged':True,'moving_cels_exact_validbaselineforms':True,'fixedowners_hiddenpixels_exact':fixedowners,'changed_native_inventory':changed,'changes_inside_prefrozenmask':True,'mask_sha256':sha(P/'editable-upperbody-frozen.png'),'lowerbody_y102plus_exact':True,'firstlast_rest_exact':True,'native_PNG_sheet_reopened_sheet_all_exact':True,'alpha':alpha,'hidden_backing_overlap_pixels':hidden,'max_lift_px':1,'max_chest_forward_px':2,'duplicate_edit':{'changed':edit_changed,'allotherpixels_cels_metadata_alpha_exact':True,'visible_composite_changed_pixels':3,'fresh_reopen_exact':True},'raw_mcp_gif':{'encoded_frames':len(gf),'encoded_durations_ms':[ms for _,ms in gf],'total_timeline_exact':True,'RGB_differences_at12authoredboundaries':rgbdiff,'alpha_exact':True},'limits':['Disposable motion sample only; no fighter application','Native producer inspected stills, no continuous motion naturalness claim','Lead owns Godot/GIF comparison and manual packet review','No callable validate tool; independent native and PNG audits only','No repo edits, source r01 untouched']};json.dump(report,open(D/'checks.json','w'),indent=2)
spec={'baseline_role':'retained r01 motion rejected as too bouncy; sample appearance only','registration':'same native96x160 grid, root(44,85), soles146, no per-imagefitting; exactbaseline native andMCPbeforeexports','required_frame_ids':[f'F{f+1}'for f in range(12)],'evidence':[{'role':'immutablebaseline native','path':'baseline.aseprite'},{'role':'candidate native','path':'delivery/traveler-breathing-r02.aseprite'},{'role':'native/export/protection readback','path':'delivery/checks.json'},{'role':'pre-mutation frozen editmask','path':'editable-upperbody-frozen.png'},{'role':'key structural ownerisolation andhide','path':'keys/apex-r02-ownership.png'},{'role':'baseline structural ownerisolation andhide','path':'keys/apex-r01-ownership.png'},{'role':'key comparisonfullform','path':'keys/before-after-2x.png'},{'role':'all12neighbors upperbody beforeafter','path':'delivery/before-after-upper-all-2x.png'},{'role':'all12 projectedfixed128rest','path':'delivery/before-after-fixed128rest.png'}],'frames':[{'id':f'F{f+1}','before':f'before/breath-{f:02}.png','after':f'delivery/breath-{f}.png','mask':'editable-upperbody-frozen.png','regions':[{'name':'head-neck-collar-chest-shoulders-elbow-wrist-waist','crop':[29,6,63,94]}]}for f in range(12)],'zoom':3};json.dump(spec,open(P/'comparison.json','w'),indent=2)
print(json.dumps({'passed':True,'native_sha256':report['native_sha256'],'unique_poses':4,'changed_cels':len(changed),'rawgif_encodedframes':len(gf),'gif_rgb_diffs':rgbdiff}))
