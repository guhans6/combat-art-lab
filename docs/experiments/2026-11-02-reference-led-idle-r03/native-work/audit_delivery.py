from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import json,sys,hashlib
P=Path('/private/tmp/atmospheric-idle-sample-r03');D=P/'delivery';sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(P/'baseline-r02.aseprite');B=read(D/'grounded-idle-r03.aseprite');E=read(D/'edit-proof.aseprite');R=json.load(open(P/'drawing-ops.json'));layers=R['layers'];old=[l['name']for l in A['layers']];stages=[0,1,2,1];dur=[500,180,420,300];mask=Image.open(P/'editable-body-except-boots-frozen.png');bootmask=Image.open(P/'protected-boots-frozen.png');M=D/'masks';M.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def eq(a,b):return a.tobytes()==b.tobytes()
def comp(a,f):
 im=Image.new('RGBA',(96,160))
 for l in range(len(a['layers'])):im.alpha_composite(a['cels'][f,l]['image'])
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
baselinehash='82e878fe5be2ebef488cd2465cc840280750eb2bc16636834212efca0ab1ebeb';assert sha(P/'baseline-r02.aseprite')==baselinehash and sha('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/source/atmospheric-traveler/breathing-r02/traveler-breathing.aseprite')==baselinehash
assert A['canvas']==B['canvas']==[96,160]and len(B['frames'])==4 and [f['duration_ms']for f in B['frames']]==dur
def palettes(a):return[c for f in a['frames']for c in f['non_cel_chunks']if c['type']in('0x2019','0x11','0x4')]
assert palettes(A)==palettes(B)
rest=comp(A,0);assert eq(rest,Image.open(P/'source-rest.png').convert('RGBA'));sheet=Image.open(D/'idle-sheet.png').convert('RGBA');assert sheet.size==(384,160)and eq(sheet,Image.open(D/'reopened-sheet.png').convert('RGBA'));frames=[];alpha=[];cuffs=[];changes=[]
for f,d in enumerate(stages):
 im=Image.open(D/f'idle-{f}.png').convert('RGBA');assert eq(im,comp(B,f))and eq(im,sheet.crop((f*96,0,(f+1)*96,160)));frames.append(im)
 assert set(im.getchannel('A').getdata())=={0,255}and not holes(im);alpha.append({'frame':f+1,'binary_alpha':True,'enclosed_holes':0})
 pts=[(i%96,i//96)for i,(a,b)in enumerate(zip(rest.getdata(),im.getdata()))if a!=b];assert all(mask.getpixel(p)for p in pts);changes.append(len(pts))
 assert eq(im.crop((0,137,96,160)),rest.crop((0,137,96,160)))
 for i,(a,b)in enumerate(zip(rest.getdata(),im.getdata())):
  if bootmask.getpixel((i%96,i//96)):assert a==b
 for n in R['upper_rigid_owners']:
  source=A['cels'][0,old.index(n)]['image'];target=B['cels'][f,layers.index(n)]['image'];moved=Image.new('RGBA',(96,160));moved.alpha_composite(source,(0,d));assert eq(moved,target)
 for n,src,cut in[('near-boot-cuff-fixed','near-leg-boot',136),('far-boot-cuff-fixed','far-leg-boot',137)]:
  source=A['cels'][0,old.index(src)]['image'].copy();source.paste((0,0,0,0),(0,0,96,cut));assert eq(source,B['cels'][f,layers.index(n)]['image'])
 for n in layers:
  expected=Image.open(P/f'drawing-data/{d}/{n}.png').convert('RGBA');assert eq(expected,B['cels'][f,layers.index(n)]['image']);B['cels'][f,layers.index(n)]['image'].getchannel('A').save(M/f'f{f}-{n}.png')
 contacts={}
 for side,cut in[('near',136),('far',137)]:
  pants=B['cels'][f,layers.index(side+'-leg-pants')]['image'];boot=B['cels'][f,layers.index(side+'-boot-cuff-fixed')]['image'];xs=[x for x in range(96)if pants.getpixel((x,cut-1))[3]and boot.getpixel((x,cut))[3]];assert xs;contacts[side]=xs
 cuffs.append(contacts)
assert eq(frames[0],rest)and eq(frames[1],frames[3])and len({im.tobytes()for im in frames})==3
# Duplicate-only visible localized edit preserves every other native cel/pixel and metadata.
assert B['header']==E['header']and B['layers']==E['layers']and B['frames']==E['frames']and B['cels'].keys()==E['cels'].keys();edits=[]
for k,b in B['cels'].items():
 e=E['cels'][k];assert all(b[x]==e[x]for x in['geometry','opacity','z']);pts=[(i%96,i//96)for i,(x,y)in enumerate(zip(b['image'].getdata(),e['image'].getdata()))if x!=y]
 if pts:edits.append({'frame':k[0]+1,'owner':layers[k[1]],'pixels':pts})
assert edits==[{'frame':1,'owner':'thorax-coat','pixels':[(47,75),(47,76),(47,77)]}];edit=Image.open(D/'edit-proof.png').convert('RGBA');assert eq(edit,Image.open(D/'edit-proof-reopened.png').convert('RGBA'));assert eq(edit.getchannel('A'),rest.getchannel('A'));assert sum(a!=b for a,b in zip(edit.getdata(),rest.getdata()))==3
gif=Image.open(D/'raw-mcp-idle.gif');gf=[(im.convert('RGBA').copy(),im.info.get('duration',0))for im in ImageSequence.Iterator(gif)];assert len(gf)==4 and [ms for _,ms in gf]==dur;rgbdiff=[]
for(g,_),im in zip(gf,frames):assert eq(g.getchannel('A'),im.getchannel('A'));rgbdiff.append(sum(a[:3]!=b[:3]for a,b in zip(g.getdata(),im.getdata())if b[3]))
for sc in[1,2,3]:
 out=Image.new('RGB',(96*sc*4,160*sc+30),'#74797c');dr=ImageDraw.Draw(out)
 for f,im in enumerate(frames):out.paste(matte(im,'#74797c').resize((96*sc,160*sc),Image.Resampling.NEAREST).convert('RGB'),(f*96*sc,30));dr.text((f*96*sc+3,5),f'{f+1} down{stages[f]} {dur[f]}ms',fill='white')
 out.save(D/f'contact-{sc}x.png')
out=Image.new('RGB',(4*150,200),'#74797c');dr=ImageDraw.Draw(out)
for f,im in enumerate(frames):out.paste(matte(im,'#74797c').resize((90,149),Image.Resampling.NEAREST).convert('RGB'),(f*150+30,30));dr.text((f*150+3,5),f'{f+1} fixed128rest',fill='white')
out.save(D/'contact-fixed128rest.png')
out=Image.new('RGB',(360,210),'#74797c');dr=ImageDraw.Draw(out)
for j,im in enumerate([rest,edit]):out.paste(matte(im,'#74797c').crop((35,68,55,88)).resize((160,160),Image.Resampling.NEAREST).convert('RGB'),(j*180+10,30));dr.text((j*180+10,7),['originalfold','duplicate3pxnarrow'][j],fill='white')
out.save(D/'edit-proof-comparison-8x.png')
timings={'animation':'grounded-idle','canvas':[96,160],'rest_body_height_px':137,'feet_baseline_y':146,'ground_root':[44,147],'rest_pelvis':[44,85],'timeline_frames':4,'unique_height_poses':3,'duration_ms':1400,'loop':True,'filter':'nearest','projection':'fixed128/137 scale allframes','frames':[{'file':f'idle-{f}.png','duration_ms':dur[f],'body_down_px':stages[f],'pelvis':[44,85+stages[f]],'chest_expansion_px':0}for f in range(4)],'timing_role':'agentproposed slower than400/800ms referencepreviews, not artistnative source timing'};json.dump(timings,open(D/'timings.json','w'),indent=2)
report={'passed':True,'baseline_sha256':baselinehash,'native_sha256':sha(D/'grounded-idle-r03.aseprite'),'canvas':[96,160],'palette_native_chunks_exact':True,'native_layers':12,'native_cels':48,'frames':4,'unique_height_poses':3,'durations_ms':dur,'total_ms':1400,'semantic_split':'source twolegboot owners split into two pants+two immutable boot/cuff owners','all_source_rest_upper_pelvis_skirt_owners_exact_registered_translation':True,'chest_expansion_px_allframes':0,'pelvis_down_px':stages,'head_shoulder_arm_same_primary_downphase':True,'both_boot_owner_pixels_exact_source_rest_allframes':True,'all_composite_bootmask_pixels_protected':True,'all_y137plus_exact_source_rest':True,'rest_composite_exact_source':True,'authored_leg_redraw_native_exact_to_inputdata':True,'cuff_contact_x_perframe':cuffs,'alpha':alpha,'changed_vs_source_rest_pixels':changes,'changes_inside_frozenmask':True,'native_PNG_sheet_freshreopened_sheet_exact':True,'duplicate_edit':{'changed':edits,'visible_composite_changed_pixels':3,'all_other_native_pixels_cels_geometry_metadata_palette_timing_exact':True,'alpha_unchanged':True,'fresh_reopen_exact':True},'raw_mcp_gif':{'frames':4,'durations_exact':True,'alpha_exact':True,'opaque_rgb_differences_perframe':rgbdiff},'limits':['Disposable sample only, no fighterdesign/application','Pants/boot cuff coverage abuts and is validated for these3poses only, not a complete hidden surface rig','Hip/knee routes under clothing inferred construction hypotheses','Producer inspected stills, not temporalnaturalness','Lead owns Godot environment/playback/artreview','No callable validate tool; independentnative/PNG checks','No r01/r02/repo/fighter writes']};json.dump(report,open(D/'checks.json','w'),indent=2)
spec={'baseline_role':'retained r02 sample appearance REST only; entire chest-puff mechanism rejected','registration':'same96x160 grid and immutable sourceREST; pose-delta comparison, not temporalalignment with prior rejected chestcycle; boots/groundfixed','required_frame_ids':[f'F{i+1}'for i in range(4)],'evidence':[{'role':'immutable source native','path':'baseline-r02.aseprite'},{'role':'candidate native','path':'delivery/grounded-idle-r03.aseprite'},{'role':'native/export/boot/registeredmaterial readback','path':'delivery/checks.json'},{'role':'frozen protected bootmask','path':'protected-boots-frozen.png'},{'role':'native lowerownership/hide rest','path':'keys/rest-lower-ownership.png'},{'role':'native lowerownership/hide sink','path':'keys/sink-lower-ownership.png'},{'role':'marked inferred route rest','path':'keys/rest-landmarks-3x.png'},{'role':'marked inferred route sink','path':'keys/sink-landmarks-3x.png'},{'role':'neighbor3keys native','path':'keys/keys-3x.png'},{'role':'all4nativeframes','path':'delivery/contact-3x.png'},{'role':'actual Saint11 motionreference contact','path':'reference-evidence/saint11-contact.png'}],'frames':[{'id':f'F{i+1}','before':'source-rest.png','after':f'delivery/idle-{i}.png','mask':'editable-body-except-boots-frozen.png','regions':[{'name':'head-neck-shoulders-pelvis-knees-ankle-joins','crop':[28,6,65,137]}]}for i in range(4)],'zoom':3};json.dump(spec,open(P/'comparison.json','w'),indent=2)
print(json.dumps({'passed':True,'native_sha256':report['native_sha256'],'frames':4,'poses':3,'total_ms':1400,'gif_rgb_differences':rgbdiff}))
