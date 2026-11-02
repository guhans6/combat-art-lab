from pathlib import Path
from PIL import Image
import sys,json,hashlib,string
P=Path('/private/tmp/stealth-fighter-idle-r02');sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(P/'inputs/idle-r01.aseprite');B=read(P/'keys/keys-final.aseprite');names=[x['name']for x in B['layers']];anames=[x['name']for x in A['layers']]
def eq(a,b):return a.tobytes()==b.tobytes()
def source(n):return A['cels'][0,anames.index(n)]['image']
def target(k,n):return B['cels'].get((k,names.index(n)),{}).get('image',Image.new('RGBA',(128,264)))
def move(im,dx,dy):o=Image.new('RGBA',im.size);o.alpha_composite(im,(dx,dy));return o
basecomp=Image.new('RGBA',(128,264))
for i in range(len(anames)):
 if (0,i)in A['cels']:basecomp.alpha_composite(A['cels'][0,i]['image'])
assert eq(basecomp,Image.open(P/'keys/repaired-key-0.png').convert('RGBA'))
for k in range(3):
 for n in ['lower-body-fixed','sword-belt']:assert eq(source(n),target(k,n))
 assert eq(target(0,'far-hem-fixed'),target(k,'far-hem-fixed'))
 assert eq(move(target(0,'near-guard-hand'),*[(0,0),(-1,-1),(-2,-2)][k]),target(k,'near-guard-hand'))
 assert eq(move(target(0,'head-hair-neck'),*[(0,0),(0,-1),(-2,-2)][k]),target(k,'head-hair-neck'))
 assert eq(move(target(0,'far-hand'),*[(0,0),(0,-1),(-1,-2)][k]),target(k,'far-hand'))
# Fixed cool splithem now occludes moving hand; exact original mixed owner's REST reconstructed.
q=target(0,'far-hand').copy();q.alpha_composite(target(0,'far-hem-fixed'));assert eq(q,source('far-hand'))
q=target(0,'near-guard-hand').copy();q.alpha_composite(target(0,'near-upper-sleeve'));assert eq(q,source('near-arm'))
# Palette bytes before/after are equal even though unrelated timing/tag/layer chunks legitimately differ.
palA=[x for f in A['frames']for x in f['non_cel_chunks']if x['type']=='0x2019'];palB=[x for f in B['frames']for x in f['non_cel_chunks']if x['type']=='0x2019'];assert palA==palB
for k in range(3):
 out=Image.new('RGBA',(128,264))
 for n in names:out.alpha_composite(target(k,n))
 assert eq(out,Image.open(P/'keys'/f'repaired-key-{k}.png').convert('RGBA'))
 # before-motion diagnostic frames, not approved appearance/motion.
 pre=Image.new('RGBA',(128,264))
 for i in range(len(anames)):
  if (k,i)in A['cels']:pre.alpha_composite(A['cels'][k,i]['image'])
 pre.save(P/'inputs'/f'before-{k}.png')
colors=sorted({v[:3]for k in range(3)for n in names for v in target(k,n).getdata()if v[3]});legend=dict(zip(string.ascii_letters,['#%02x%02x%02x'%c for c in colors]));rev={tuple(bytes.fromhex(c[1:]))+(255,):ch for ch,c in legend.items()};ops={}
for k in range(3):
 ops[str(k)]={}
 for n in names:
  q=target(k,n);b=q.getbbox()
  if not b:ops[str(k)][n]=[];continue
  x0,y0,x1,y1=b;ops[str(k)][n]=[{'kind':'grid','x':x0,'y':y0,'rows':[''.join(rev.get(q.getpixel((x,y)),'.')for x in range(x0,x1))for y in range(y0,y1)],'legend':legend}]
json.dump({'native_sha256':hashlib.sha256((P/'keys/keys-final.aseprite').read_bytes()).hexdigest(),'layers':names,'ops':ops,'native_derived':'exact final native readback grids, not native-file writing'},open(P/'final-key-ops.json','w'),indent=2)
json.dump({'passed':True,'rest_exact':True,'original_lower_body_native_exact':True,'original_sword_belt_native_exact':True,'split_near_arm_rest_exact':True,'split_far_hand_cloth_rest_exact':True,'far_hem_native_fixed_allkeys':True,'head_face_hair_rigid_source':True,'guard_hand_rigid_source':True,'far_arm_rigid_source':True,'palette_chunks_exact':True,'native_png_allkeys_exact':True,'key_native_sha256':hashlib.sha256((P/'keys/keys-final.aseprite').read_bytes()).hexdigest()},open(P/'keys/native-checks.json','w'),indent=2)
spec={'baseline_role':'main r01 REST retained appearance; r01 transition/apex diagnostic rejected as too subtle, no approval inherited','registration':'same128x264 grid/root; source240px body; no fitting. Native REST exact. Traveler r04 motion-only transfer scaled by body ratio240/137, rigid main equipment adapted.','required_frame_ids':['K0','K1','K2'],'zoom':4,'evidence':[{'role':'candidate native','path':'keys/keys-final.aseprite'},{'role':'native/export protection readback','path':'keys/native-checks.json'},{'role':'alpha and actual landmarks','path':'keys/checks.json'},{'role':'CurrentA original identity','path':'/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/concepts/stealth-fighter/game-specific-r01/silver-pines/corrected.png'},{'role':'approved traveler motion only','path':'/private/tmp/atmospheric-idle-sample-r04/keys/keys-3x.png'},{'role':'contrasting native poses','path':'keys/upper-contrast-5x.png'}]+[{'role':'actual native owner-hide '+n,'path':'keys/ownership-'+n+'-5x.png'}for n in ['head-hair-neck','upper-torso','near-upper-sleeve','near-guard-hand','far-hand']]+[{'role':'fixed hem owner K'+str(k),'path':f'keys/f{k}-owner-far-hem-fixed.png'}for k in range(3)],'frames':[{'id':'K'+str(k),'before':f'inputs/before-{k}.png','after':f'keys/repaired-key-{k}.png','mask':'editable-upper-frozen.png','regions':[{'name':'head-hair-neck','crop':[24,9,80,58]},{'name':'shoulder-collar-sleeve-elbow','crop':[24,40,81,110]},{'name':'guard-hand-waist-fararm-hem','crop':[24,90,92,153]}]}for k in range(3)]}
json.dump(spec,open(P/'comparison-keys.json','w'),indent=2)
print('native key checks PASS')
