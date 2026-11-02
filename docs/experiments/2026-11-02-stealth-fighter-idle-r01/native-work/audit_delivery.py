from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import json,sys,hashlib
sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools')
from check_native_pilot import read
O=Path('/private/tmp/stealth-fighter-idle-r01');D=O/'delivery';A=read(D/'stealth-fighter-idle-r01.aseprite');B=read(D/'edit-proof/local-buckle-edit.aseprite');dur=[850,450,500,650,550];keys=['rest','transition','apex','transition','rest']
frames=[Image.open(D/'frames'/f'idle-{i:02}.png').convert('RGBA') for i in range(5)]
def eq(a,b):return a.tobytes()==b.tobytes()
assert A['canvas']==[128,264] and [f['duration_ms'] for f in A['frames']]==dur
native=[]
for f in range(5):
 comp=Image.new('RGBA',(128,264))
 for l in range(len(A['layers'])):
  if (f,l) in A['cels']:comp.alpha_composite(A['cels'][f,l]['image'])
 assert eq(comp,frames[f]);assert eq(frames[f],Image.open(D/'reopen'/f'idle-{f:02}.png').convert('RGBA'));assert eq(frames[f],Image.open(O/'keys'/('final-'+keys[f]+'.png')).convert('RGBA'));native.append(True)
 assert eq(frames[0].crop((0,153,128,264)),frames[f].crop((0,153,128,264)))
# Fixed semantic owners including hidden pixels, not only flattened appearance.
fixed={}
for name in ['lower-body-fixed','sword-belt','far-hand']:
 l=[x['name'] for x in A['layers']].index(name);fixed[name]=all(eq(A['cels'][0,l]['image'],A['cels'][f,l]['image']) for f in range(5));assert fixed[name]
head=[x['name'] for x in A['layers']].index('head-hair-neck');h0=A['cels'][0,head]['image'];ha=Image.new('RGBA',h0.size);ha.alpha_composite(h0,(0,-1));assert eq(ha,A['cels'][2,head]['image'])
# All alpha gaps are inventoried independently on actual export; none allowed/needed here.
alpha=[]
for im in frames:
 assert set(im.getchannel('A').getdata())=={0,255}
 s={(x,y) for y in range(264) for x in range(128) if not im.getpixel((x,y))[3]};holes=[]
 while s:
  q=[s.pop()];edge=False
  for x,y in q:
   edge|=x in (0,127) or y in (0,263)
   for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if p in s:s.remove(p);q.append(p)
  if not edge:holes.append(q)
 assert not holes;alpha.append({'enclosed_holes':0,'alpha_binary':True})
# Local revision changes exactly 3 intended buckle pixels; all hidden owners and metadata protected.
assert A['header']==B['header'] and A['layers']==B['layers'] and A['frames']==B['frames'] and A['cels'].keys()==B['cels'].keys()
changed=[]
for k,c in A['cels'].items():
 d=B['cels'][k];assert all(c[x]==d[x] for x in ['geometry','opacity','z'])
 pts=[(i%128,i//128) for i,(x,y) in enumerate(zip(c['image'].getdata(),d['image'].getdata())) if x!=y]
 if pts:changed.append({'frame':k[0]+1,'layer':A['layers'][k[1]]['name'],'pixels':pts})
assert changed==[{'frame':1,'layer':'sword-belt','pixels':[(75,99),(75,100),(75,101)]}]
assert eq(Image.open(D/'edit-proof/edited.png'),Image.open(D/'edit-proof/reopened-edit.png'))
gif=Image.open(D/'idle-native.gif');gf=[]
for f in ImageSequence.Iterator(gif):gf.append((f.convert('RGBA').copy(),f.info.get('duration',0)))
assert len(gf)==5 and [t for _,t in gf]==dur
gif_color_diffs=[]
for (a,_),b in zip(gf,frames):
 assert eq(a.getchannel('A'),b.getchannel('A'))
 gif_color_diffs.append(sum(pa[:3]!=pb[:3] for pa,pb in zip(a.getdata(),b.getdata()) if pb[3]))
assert gif_color_diffs==[89,89,86,89,89]
sheet=Image.open(D/'idle-sheet.png').convert('RGBA');assert sheet.size==(640,264)
for i,im in enumerate(frames):assert eq(im,sheet.crop((128*i,0,128*(i+1),264)))
# Native size / 3x contact and useful duplicate-only revision comparison.
for sc in [1,3]:
 canvas=Image.new('RGBA',(128*sc*5,264*sc+34),'#373b41');dr=ImageDraw.Draw(canvas)
 for i,im in enumerate(frames):
  canvas.alpha_composite(im.resize((128*sc,264*sc),Image.Resampling.NEAREST),(128*sc*i,28));dr.text((128*sc*i+5,7),f'{i+1} {keys[i]} {dur[i]}ms',fill='white')
 canvas.convert('RGB').save(D/f'contact-{sc}x.png')
# Native-derived skin-free owner-hide evidence, not recreated from producer intent.
la=[x['name'] for x in A['layers']].index('near-arm');hide=Image.new('RGBA',(128,264))
for l in range(len(A['layers'])):
 if l!=la and (2,l) in A['cels']:hide.alpha_composite(A['cels'][2,l]['image'])
assert eq(hide,Image.open(O/'keys/final-apex-hide-near-arm.png').convert('RGBA'))
no_skin=all(not(hide.getpixel((x,y))[3] and hide.getpixel((x,y))[:3] in [(147,101,66),(104,80,62)]) for y in range(110,153) for x in range(29,56));assert no_skin
report={'passed':True,'native':{'canvas':A['canvas'],'frames':5,'unique_drawings':3,'durations_ms':dur,'duration_ms':sum(dur),'layers':A['layers'],'cels':len(A['cels']),'all_native_composites_match':native,'reopened_exports_exact':True,'palette_metadata_unchanged_in_edit':True},'anchors':{'soles_y':252,'root':[64,253],'composite_y153_plus_exact_all_frames':True,'fixed_native_owners':fixed,'head_face_hair_neck_exact_registered_rise_1px':True},'alpha':alpha,'raw_mcp_gif':{'timing_exact':True,'alpha_exact':True,'opaque_rgb_differences_per_frame':gif_color_diffs,'status':'preview encoding remaps first near-black palette color; lead owns exact-palette preview re-encoding from PNGs'},'sheet_exact':True,'local_edit':{'changed':changed,'all_protected_native_unchanged':True,'all_metadata_unchanged':True,'reopen_export_exact':True},'owner_hide_near_arm_no_residual_skin':no_skin,'source_sha256':hashlib.sha256(Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/concepts/stealth-fighter/game-specific-r01/silver-pines/corrected.png').read_bytes()).hexdigest(),'native_sha256':hashlib.sha256((D/'stealth-fighter-idle-r01.aseprite').read_bytes()).hexdigest(),'limits':['continuous animation perception not observed by producer','user art approval pending','Godot playback lead-owned','grid provisional','single-view source-derived visible parts, not complete hidden-surface rig','no validate tool exposed; independent scoped PNG/native checks performed']}
assert report['source_sha256']=='a3cc3ab1d658ac3d2d464ef4781ed966e815c7eedeefcf5801d81ca93924ab9c'
json.dump(report,open(D/'checks.json','w'),indent=2)
json.dump({'animation':'idle','canvas':[128,264],'body_height_rest_px':240,'root':[64,253],'frames':[{'file':f'frames/idle-{i:02}.png','duration_ms':t,'pose':keys[i]} for i,t in enumerate(dur)],'loop':True,'filter':'nearest','grid':'provisional'},open(D/'timings.json','w'),indent=2)
print(json.dumps({'passed':True,'sha256':report['native_sha256'],'frames':5,'duration_ms':3000,'native_layers':7,'local_edit_pixels':3}))
