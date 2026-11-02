from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import json,sys,hashlib
P=Path('/private/tmp/atmospheric-breathing-proxy-r01');D=P/'delivery';M=D/'masks';M.mkdir(exist_ok=True)
sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(D/'traveler-breathing-r01.aseprite');B=read(D/'edit-proof.aseprite');recipe=json.load(open(P/'cycle-draw-ops.json'));layers=recipe['layers'];stages=recipe['stages'];dur=recipe['durations_ms']
assert A['canvas']==[96,160]and len(A['frames'])==12 and[f['duration_ms']for f in A['frames']]==dur
def eq(a,b):return a.tobytes()==b.tobytes()
def comp(f,omit=None):
 im=Image.new('RGBA',(96,160))
 for l,n in enumerate(layers):
  if n!=omit:im.alpha_composite(A['cels'][f,l]['image'])
 return im
def matte(im,color):
 out=Image.new('RGBA',im.size,color);out.alpha_composite(im);return out
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
sheet=Image.open(D/'breath-sheet.png').convert('RGBA');reopen=Image.open(D/'reopened-sheet.png').convert('RGBA');assert eq(sheet,reopen)and sheet.size==(1152,160)
frames=[];fixed={n:True for n in layers[:4]};alpha=[];hidden_counts={}
head0=A['cels'][0,layers.index('head-hair-face')]['image']
for f,(lift,expansion)in enumerate(stages):
 im=Image.open(D/f'breath-{f}.png').convert('RGBA');native=comp(f);assert eq(native,im)and eq(im,sheet.crop((f*96,0,(f+1)*96,160)));frames.append(im)
 assert eq(im.crop((0,102,96,160)),frames[0].crop((0,102,96,160)))
 for n in fixed:
  l=layers.index(n);assert eq(A['cels'][f,l]['image'],A['cels'][0,l]['image'])
 # Rigid skull and both arm segments register exactly to shared supported shoulder lift.
 for n in['head-hair-face','near-upper-sleeve','near-forearm-hand','far-sleeve-hand','neck-collar']:
  l=layers.index(n);moved=Image.new('RGBA',(96,160));moved.alpha_composite(A['cels'][0,l]['image'],(0,-lift));assert eq(moved,A['cels'][f,l]['image'])
 assert not holes(im);assert set(im.getchannel('A').getdata())=={0,255};alpha.append({'frame':f,'enclosed_holes':0,'alpha_binary':True})
 for l,n in enumerate(layers):
  mask=A['cels'][f,l]['image'].getchannel('A');mask.save(M/f'f{f:02}-{n}.png')
 # Core chest coverage is genuinely solid through all phase combinations.
 for y in range(46,74):
  for x in range(45,51):assert im.getpixel((x,y))[3]==255
assert len({im.tobytes()for im in frames})==7
# Masks record fixed feet/root composite and authorized duplicate proof patch.
protected=Image.new('L',(96,160));ImageDraw.Draw(protected).rectangle((0,102,95,159),fill=255);protected.save(M/'protected-lower-body.png')
allowed=Image.new('L',(96,160));ImageDraw.Draw(allowed).rectangle((47,75,47,77),fill=255);allowed.save(M/'duplicate-edit-allowed.png')
solid=Image.new('L',(96,160));ImageDraw.Draw(solid).rectangle((45,46,50,73),fill=255);solid.save(M/'solid-core-chest.png')
# Native hidden backing inventory, beyond flattened PNG correctness.
for n in['neck-collar','thorax-coat','near-upper-sleeve','far-sleeve-hand']:
 l=layers.index(n);counts=[]
 for f in range(12):
  owner=A['cels'][f,l]['image'];above=Image.new('RGBA',(96,160))
  for q in range(l+1,len(layers)):above.alpha_composite(A['cels'][f,q]['image'])
  counts.append(sum(a[3]>0 and b[3]>0 for a,b in zip(owner.getdata(),above.getdata())))
 hidden_counts[n]=counts;assert min(counts)>0
# Useful duplicate edit: three visible opaque base pixels narrow coatfold highlight only in first cel.
assert A['header']==B['header']and A['layers']==B['layers']and A['frames']==B['frames']and A['cels'].keys()==B['cels'].keys()
changed=[]
for k,c in A['cels'].items():
 b=B['cels'][k];assert all(c[x]==b[x]for x in['geometry','opacity','z'])
 pts=[(i%96,i//96)for i,(x,y)in enumerate(zip(c['image'].getdata(),b['image'].getdata()))if x!=y]
 if pts:changed.append({'frame':k[0]+1,'layer':layers[k[1]],'pixels':pts})
assert changed==[{'frame':1,'layer':'thorax-coat','pixels':[(47,75),(47,76),(47,77)]}]
edit=Image.open(D/'edit-proof.png').convert('RGBA');assert eq(edit,Image.open(D/'edit-proof-reopened.png').convert('RGBA'));assert eq(edit.getchannel('A'),frames[0].getchannel('A'));assert sum(a!=b for a,b in zip(edit.getdata(),frames[0].getdata()))==3
gif=Image.open(D/'raw-mcp-breath.gif');gif_frames=[(im.convert('RGBA').copy(),im.info.get('duration',0))for im in ImageSequence.Iterator(gif)]
assert len(gif_frames)==12 and[t for _,t in gif_frames]==dur
gifdiff=[]
for (gf,_),im in zip(gif_frames,frames):
 assert eq(gf.getchannel('A'),im.getchannel('A'));gifdiff.append(sum(a[:3]!=b[:3]for a,b in zip(gf.getdata(),im.getdata())if b[3]))
# Native contacts at1x/2x/3x, plus 128px restbody projection; common grid throughout.
for sc in[1,2,3]:
 out=Image.new('RGB',(96*sc*4,(160*sc+24)*3),'#74797c');dr=ImageDraw.Draw(out)
 for f,im in enumerate(frames):
  x=f%4*96*sc;y=f//4*(160*sc+24);out.paste(matte(im,'#74797c').resize((96*sc,160*sc),Image.Resampling.NEAREST).convert('RGB'),(x,y+24));dr.text((x+3,y+4),f'{f+1} {dur[f]}ms L{stages[f][0]} C{stages[f][1]}',fill='white')
 out.save(D/f'contact-{sc}x.png')
out=Image.new('RGB',(144*4,180*3),'#74797c');dr=ImageDraw.Draw(out)
for f,im in enumerate(frames):
 x=f%4*144;y=f//4*180;out.paste(matte(im,'#74797c').resize((90,149),Image.Resampling.NEAREST).convert('RGB'),(x+27,y+26));dr.text((x+3,y+4),f'{f+1} fixed128rest',fill='white')
out.save(D/'contact-projected128.png')
out=Image.new('RGB',(144*4,300*3),'#454b50');dr=ImageDraw.Draw(out)
for f,im in enumerate(frames):
 x=f%4*144;y=f//4*300;out.paste(matte(im,'#d3cab9').crop((25,5,73,95)).resize((144,270),Image.Resampling.NEAREST).convert('RGB'),(x,y+28));dr.text((x+3,y+4),f'{f+1} L{stages[f][0]} C{stages[f][1]}',fill='white')
out.save(D/'upperbody-all-3x.png')
out=Image.new('RGB',(360,210),'#74797c');dr=ImageDraw.Draw(out)
for j,im in enumerate([frames[0],edit]):out.paste(matte(im,'#74797c').crop((35,68,55,88)).resize((160,160),Image.Resampling.NEAREST).convert('RGB'),(j*180+10,30));dr.text((j*180+10,7),['originalcoatfold','duplicate3pxnarrow'][j],fill='white')
out.save(D/'edit-proof-comparison-8x.png')
timings={'animation':'breath','canvas':[96,160],'rest_body_height_px':137,'rest_hair_top':10,'feet_baseline_y':146,'root':[44,85],'loop':True,'display_projection':'fixed128px restbody=scale128/137; no perposefitting','filter':'nearest','frames':[{'file':f'breath-{f}.png','duration_ms':dur[f],'lift_px':stages[f][0],'chest_expansion_px':stages[f][1],'phase':recipe['phases'][f]}for f in range(12)]};json.dump(timings,open(D/'timings.json','w'),indent=2)
source=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/concepts/stealth-fighter/game-specific-r01/silver-pines/corrected.png');sourcehash=hashlib.sha256(source.read_bytes()).hexdigest();assert sourcehash=='a3cc3ab1d658ac3d2d464ef4781ed966e815c7eedeefcf5801d81ca93924ab9c'
report={'passed':True,'native_sha256':hashlib.sha256((D/'traveler-breathing-r01.aseprite').read_bytes()).hexdigest(),'source_sha256':sourcehash,'canvas':[96,160],'native_layers':10,'native_cels':120,'frames':12,'unique_pose_drawings':7,'durations_ms':dur,'total_ms':sum(dur),'native_composites_match_all_MCP_PNGs':True,'reopened_sheet_exact':True,'palette_entries':14,'binary_alpha_frames':alpha,'fixed_native_owners':fixed,'fixed_composite_y102plus':True,'rigid_head_face_arms_collar_exact_registered':True,'solid_core_chest_all_frames':True,'hidden_backing_overlap_pixels':hidden_counts,'local_edit':{'changed':changed,'all_other_native_pixels_metadata_geometry_palette_timing_exact':True,'alpha_unchanged':True,'reopened_export_exact':True},'raw_mcp_gif':{'durations_and_alpha_exact':True,'opaque_rgb_differences_per_frame':gifdiff,'exact_RGB':not any(gifdiff),'retained_as_raw':True},'limits':['Producer inspected stillfilmstrip only, continuous naturalness not established','Lead owns Godot and exactpalette GIF packaging','User artistic approval pending','Original proxy not final fighter identity or design direction','No callable validate tool despite advertised capability; independent native and PNG checks substitute honestly','No repository/Git edits or installation/publication']}
json.dump(report,open(D/'checks.json','w'),indent=2)
with open(P/'observations.md','a')as o:o.write('\n## Cycle validation\nLead cleared corrected native structural keys and ownerhide before timeline extension.12frames2800ms;7distinct posecombinations, one shared asymmetric breathingphase. All12 actualMCP PNGs match native composites and freshreopenedMCPsheet. Producer inspected all12 fullbodyfilmstrip2x and upperbody-all-3x/nativeprojected128; no doubled neck/cuff marks or gaps. 3pxhead/shoulderrise andchestforward atapex; root, feet and four fullnative lowerowners fixed. Naturalness remains userplayback judgment.\n\nDuplicateproof firstattempt used dot which erasedone intendedpaintpixel; rejected, preserved separately. First corrected4pixel patch fell behind arm and proved hiddenowner preservation only; retained as rejected hidden-fold proof. Final duplicate-only3opaque basepixels narrow visible coatfoldhighlight at(47,75)-(47,77), noalpha change, metadata/119othercels andallotherpixels unchanged; saved/reopened exact. It is editabilityproof, not a production variant. AllownedMCPdocumentsclosed.\n')
hashes={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest()for f in sorted(P.rglob('*'))if f.is_file()and f.name!='SHA256.json'};json.dump(hashes,open(P/'SHA256.json','w'),indent=2)
print(json.dumps({'passed':True,'native_sha256':report['native_sha256'],'frames':12,'unique_pose_drawings':7,'raw_mcp_gif_rgb_diffs':gifdiff,'native_cels':120,'duplicate_changed':changed}))
