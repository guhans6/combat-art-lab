from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib,math
P=Path('/private/tmp/atmospheric-idle-sample-r03');K=P/'keys';sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(P/'baseline-r02.aseprite');B=read(K/'grounded-keys.aseprite');R=json.load(open(P/'drawing-ops.json'));layers=R['layers'];mask=Image.open(P/'editable-body-except-boots-frozen.png');bootmask=Image.open(P/'protected-boots-frozen.png')
def comp(a,f):
 im=Image.new('RGBA',(96,160))
 for l in range(len(a['layers'])):im.alpha_composite(a['cels'][f,l]['image'])
 return im
def bcomp(f,omit=None):
 im=Image.new('RGBA',(96,160))
 for l,n in enumerate(layers):
  if n!=omit:im.alpha_composite(B['cels'][f,l]['image'])
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
frames=[];checks=[];rest=comp(A,0);assert rest.tobytes()==Image.open(P/'source-rest.png').convert('RGBA').tobytes()
for f,n in enumerate(['rest','transition','sink']):
 im=bcomp(f);frames.append(im);assert im.tobytes()==Image.open(K/f'{n}.png').convert('RGBA').tobytes()
 changes=[(i%96,i//96)for i,(a,b)in enumerate(zip(rest.getdata(),im.getdata()))if a!=b];assert all(mask.getpixel(p)for p in changes)
 for i,(a,b)in enumerate(zip(rest.getdata(),im.getdata())):
  if bootmask.getpixel((i%96,i//96)):assert a==b
 for owner in R['fixed_owners']:
  l=layers.index(owner);assert B['cels'][f,l]['image'].tobytes()==B['cels'][0,l]['image'].tobytes()
 for owner in R['upper_rigid_owners']:
  l=layers.index(owner);old=[x['name']for x in A['layers']].index(owner);shift=Image.new('RGBA',(96,160));shift.alpha_composite(A['cels'][0,old]['image'],(0,f));assert shift.tobytes()==B['cels'][f,l]['image'].tobytes()
 hs=holes(im);checks.append({'key':n,'changed_vsrest':len(changes),'enclosed_holes':hs,'boots_exact':True,'registered_rigid_chest_head_arms_pelvis_skirt_exact':True})
 for owner in['pelvis-root','near-leg-pants','far-leg-pants','near-boot-cuff-fixed','far-boot-cuff-fixed']:
  bcomp(f,owner).save(K/f'{n}-hide-{owner}.png')
 # Full-body landmark hypotheses, with hidden hip/knee routes labeled inferred.
 guide=matte(im,'#9c9b90');dr=ImageDraw.Draw(guide);lm=R['landmarks'][str(f)]
 for side in['near','far']:
  pts=[tuple(lm[side+'_hip_inferred']),tuple(lm[side+'_knee_inferred']),tuple(lm[side+'_ankle'])];dr.line(pts,fill='#e2b84e',width=1)
 for name,xy in lm.items():
  if isinstance(xy,list):x,y=xy;dr.line((x-1,y,x+1,y),fill='#ed8755');dr.line((x,y-1,x,y+1),fill='#ed8755')
 out=guide.resize((288,480),Image.Resampling.NEAREST);ImageDraw.Draw(out).text((4,4),'Hip/knee routes inferred; soles fixed',fill='white');out.save(K/f'{n}-landmarks-3x.png')
 panel=Image.new('RGB',(5*144,3*248),'#555960');dr=ImageDraw.Draw(panel)
 for j,owner in enumerate(['pelvis-root','near-leg-pants','far-leg-pants','near-boot-cuff-fixed','far-boot-cuff-fixed']):
  for r,v in enumerate([im,B['cels'][f,layers.index(owner)]['image'],bcomp(f,owner)]):
   v=matte(v,'#a3a397').crop((27,72,66,148)).resize((117,228),Image.Resampling.NEAREST);panel.paste(v.convert('RGB'),(j*144+12,r*248+20));dr.text((j*144+2,r*248+2),owner if r==0 else['','isolated','hidden'][r],fill='white')
 panel.save(K/f'{n}-lower-ownership.png')
assert frames[0].tobytes()==rest.tobytes()
for sc in[1,3]:
 out=Image.new('RGB',(3*96*sc,160*sc+30),'#74797c');dr=ImageDraw.Draw(out)
 for f,im in enumerate(frames):out.paste(matte(im,'#74797c').resize((96*sc,160*sc),Image.Resampling.NEAREST).convert('RGB'),(f*96*sc,30));dr.text((f*96*sc+3,5),['rest','transition1px','sink2px'][f],fill='white')
 out.save(K/f'keys-{sc}x.png')
out=Image.new('RGB',(3*180,200),'#74797c');dr=ImageDraw.Draw(out)
for f,im in enumerate(frames):out.paste(matte(im,'#74797c').resize((90,149),Image.Resampling.NEAREST).convert('RGB'),(f*180+40,30));dr.text((f*180+4,7),['rest','transition','sink'][f]+' fixed128rest',fill='white')
out.save(K/'keys-fixed128rest.png')
out=Image.new('RGB',(3*234,260),'#555960');dr=ImageDraw.Draw(out)
for f,im in enumerate(frames):
 for j,c in enumerate(['#d5cbb8','#171c24']):out.paste(matte(im,c).crop((27,72,66,148)).resize((117,228),Image.Resampling.NEAREST).convert('RGB'),(f*234+j*117,25))
 dr.text((f*234+3,5),['rest','transition','sink'][f],fill='white')
out.save(K/'knees-ankles-contrast-3x.png')
json.dump({'keys':checks,'rest_exact':True,'canvas':[96,160],'native_layers':12,'native_cels':36,'native_sha256':hashlib.sha256((K/'grounded-keys.aseprite').read_bytes()).hexdigest(),'landmarks':R['landmarks']},open(K/'checks.json','w'),indent=2);print(json.dumps(checks))
