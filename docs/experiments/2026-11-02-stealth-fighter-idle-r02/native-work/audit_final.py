from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import sys,json,hashlib
P=Path('/private/tmp/stealth-fighter-idle-r02');D=P/'delivery';sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(P/'inputs/idle-r01.aseprite');K=read(P/'keys/keys-final.aseprite');B=read(D/'idle-r02.aseprite');E=read(D/'edit-proof/buckle-revision.aseprite');dur=[700,260,500,340];km=[0,1,2,1];names=[l['name']for l in B['layers']];an=[l['name']for l in A['layers']]
def eq(a,b):return a.tobytes()==b.tobytes()
def cell(doc,f,i):return doc['cels'].get((f,i),{}).get('image',Image.new('RGBA',(128,264)))
def comp(doc,f):
 o=Image.new('RGBA',(128,264))
 for i in range(len(doc['layers'])):o.alpha_composite(cell(doc,f,i))
 return o
def palette(doc):return[x for f in doc['frames']for x in f['non_cel_chunks']if x['type']=='0x2019']
assert B['canvas']==[128,264]and[f['duration_ms']for f in B['frames']]==dur and len(names)==9 and len(B['frames'])==4
assert palette(A)==palette(B);assert names.index('far-hem-fixed')>names.index('far-hand')
frames=[];fr=[]
for f,k in enumerate(km):
 im=Image.open(D/f'idle-{f}.png').convert('RGBA');frames.append(im)
 assert eq(im,comp(B,f))and eq(im,comp(K,k))and eq(im,Image.open(D/'reopen'/f'idle-{f}.png').convert('RGBA'))
 for i in range(len(names)):assert eq(cell(B,f,i),cell(K,k,i))
 for n in['lower-body-fixed','sword-belt']:assert eq(cell(B,f,names.index(n)),cell(A,0,an.index(n)))
 assert eq(cell(B,f,names.index('far-hem-fixed')),cell(B,0,names.index('far-hem-fixed')))
 assert eq(im.crop((0,153,128,264)),frames[0].crop((0,153,128,264)))
 assert set(im.getchannel('A').getdata())=={0,255}
 s={(x,y)for y in range(264)for x in range(128)if not im.getpixel((x,y))[3]};holes=[]
 while s:
  q=[s.pop()];edge=False
  for x,y in q:
   edge|=x in(0,127)or y in(0,263)
   for v in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if v in s:s.remove(v);q.append(v)
  if not edge:holes.append(q)
 assert not holes;fr.append({'frame':f,'key':k,'native_png_reopen_exact':True,'all_native_cels_exact_cleared_key':True,'alpha_binary':True,'enclosed_holes':0,'y153_plus_exact':True})
assert eq(frames[0],comp(A,0))
# Duplicate-only useful local edit; protect every visible/hidden owner and metadata.
assert all(B[x]==E[x]for x in['canvas','header','frames','layers']);assert B['cels'].keys()==E['cels'].keys();changes=[]
for (f,i),b in B['cels'].items():
 e=E['cels'][f,i];assert all(b[x]==e[x]for x in['geometry','opacity','z']);pts=[(j%128,j//128)for j,(x,y)in enumerate(zip(b['image'].getdata(),e['image'].getdata()))if x!=y]
 if pts:changes.append({'frame':f,'layer':names[i],'points':pts})
assert changes==[{'frame':0,'layer':'sword-belt','points':[(75,99),(75,100),(75,101)]}];assert eq(Image.open(D/'edit-proof/edited.png'),Image.open(D/'edit-proof/reopened-edit.png'))
# Authored atlas exactly matches all four frames.
sheet=Image.open(D/'idle-sheet.png').convert('RGBA');assert sheet.size==(512,264)
for f,im in enumerate(frames):assert eq(im,sheet.crop((128*f,0,128*(f+1),264)))
# Raw MCP GIF limitation is reported, not silently certified.
g=Image.open(D/'idle-raw-mcp.gif');gt=[];gd=[]
for f,q in enumerate(ImageSequence.Iterator(g)):
 q=q.convert('RGBA');gt.append(g.info.get('duration',0));assert eq(q.getchannel('A'),frames[f].getchannel('A'));gd.append(sum(a[:3]!=b[:3]for a,b in zip(q.getdata(),frames[f].getdata())if b[3]))
assert gt==dur
for sc in[1,3]:
 c=Image.new('RGBA',(128*sc*4,264*sc+28),'#525760');d=ImageDraw.Draw(c)
 for f,im in enumerate(frames):c.alpha_composite(im.resize((128*sc,264*sc),Image.Resampling.NEAREST),(128*sc*f,26));d.text((128*sc*f+6,6),f'F{f} {dur[f]}ms',fill='white')
 c.convert('RGB').save(D/f'contact-{sc}x.png')
c=Image.new('RGBA',(384*3,792+28),'#525760');d=ImageDraw.Draw(c)
for col,f in enumerate([3,0,1]):c.alpha_composite(frames[f].resize((384,792),Image.Resampling.NEAREST),(384*col,26));d.text((384*col+6,6),'F'+str(f),fill='white')
c.convert('RGB').save(D/'loop-seam-3x.png')
c=Image.new('RGBA',(276*2,276+28),'#525760');d=ImageDraw.Draw(c)
for col,(label,im)in enumerate([('main REST',frames[0]),('duplicate-only buckle edit',Image.open(D/'edit-proof/edited.png').convert('RGBA'))]):c.alpha_composite(im.crop((66,90,89,113)).resize((276,276),Image.Resampling.NEAREST),(276*col,26));d.text((276*col+6,6),label,fill='white')
c.convert('RGB').save(D/'edit-proof/comparison-12x.png')
source=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/source/stealth-fighter/idle-r01/idle.aseprite');concept=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/concepts/stealth-fighter/game-specific-r01/silver-pines/corrected.png');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(source)=='e839783e58f01e61b1839f18ee6208437ec9424c0403a148f331f32e9ad653fd';assert sha(concept)=='a3cc3ab1d658ac3d2d464ef4781ed966e815c7eedeefcf5801d81ca93924ab9c'
r={'passed':True,'native_sha256':sha(D/'idle-r02.aseprite'),'source_sha256':sha(source),'identity_sha256':sha(concept),'native':{'canvas':[128,264],'frames':4,'layers':B['layers'],'cels':len(B['cels']),'duration_ms':1800,'durations_ms':dur,'palette_exact_source':True,'rest_exact_source':True,'all_native_cels_match_cleared_keys':True},'frames':fr,'protection':{'lower_body_native_exact_source':True,'sword_belt_native_exact_source':True,'far_split_hem_native_fixed':True,'head_face_hair_rigid_proven_by_key_checks':True,'near_guard_hand_rigid_proven_by_key_checks':True,'y153_plus_composite_exact':True,'originals_unchanged':True},'local_revision':{'changed':changes,'all_other_native_pixels_unchanged':True,'all_metadata_palette_exact':True,'save_reopen_export_exact':True,'selected_art':False},'sheet_exact':True,'raw_mcp_gif':{'timing_exact':True,'alpha_exact':True,'opaque_rgb_differences_per_frame':gd,'status':'known palette encoding remap; root packages exact-palette previews'},'backend':'Aseprite1.3.18.6-dev/Pebbly0.8.2 headless dedicated MCP','closed_documents':True,'producer_playback_perception':'still-only, no continuous motion claim','user_approval':'sample motion approved; main transfer pending','runtime':'root-owned separate Godot evidence'}
json.dump(r,open(D/'checks.json','w'),indent=2)
spec=json.load(open(P/'comparison-keys.json'));spec['required_frame_ids']=['F0','F1','F2','F3'];spec['frames']=[{'id':'F'+str(f),'before':f'inputs/before-{k}.png','after':f'delivery/idle-{f}.png','mask':'editable-upper-frozen.png','regions':spec['frames'][0]['regions']}for f,k in enumerate(km)];spec['evidence']=[x for x in spec['evidence']if x['role']!='candidate native']+[{'role':'final candidate native','path':'delivery/idle-r02.aseprite'},{'role':'final native/export/reopen/edit protection readback','path':'delivery/checks.json'},{'role':'actual final cycle and timing','path':'delivery/contact-3x.png'},{'role':'actual final return neighbors','path':'delivery/loop-seam-3x.png'},{'role':'useful duplicate-only local edit','path':'delivery/edit-proof/comparison-12x.png'}];json.dump(spec,open(P/'comparison-final.json','w'),indent=2)
print(json.dumps({'passed':True,'native_sha256':r['native_sha256'],'frames':4,'duration':1800,'rawGIF_rgb_diffs':gd}))
