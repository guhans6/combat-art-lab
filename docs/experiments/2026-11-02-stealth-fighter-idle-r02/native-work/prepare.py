from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib,string
P=Path('/private/tmp/stealth-fighter-idle-r02');I=P/'inputs';K=P/'keys';sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(I/'idle-r01.aseprite');orig={l['name']:A['cels'].get((0,i),{}).get('image',Image.new('RGBA',(128,264))) for i,l in enumerate(A['layers'])}
base={n:im.copy() for n,im in orig.items()};far=base['far-hand'].copy();hem=Image.new('RGBA',far.size)
for yy in range(264):
 for xx in range(128):
  px=far.getpixel((xx,yy))
  if px[3] and ((px[2]>px[0]*1.2 and px[2]>45) or (xx,yy)==(87,151)):hem.putpixel((xx,yy),px);far.putpixel((xx,yy),(0,0,0,0))
base['far-hand']=far;base['far-hem-fixed']=hem
arm=base.pop('near-arm');sleeve=arm.copy();guard=arm.copy();ImageDraw.Draw(sleeve).rectangle((0,93,127,263),fill=(0,0,0,0));ImageDraw.Draw(guard).rectangle((0,0,127,92),fill=(0,0,0,0));base['near-upper-sleeve']=sleeve;base['near-guard-hand']=guard
layers=['body-occlusion-backing','lower-body-fixed','upper-torso','sword-belt','far-hand','far-hem-fixed','near-guard-hand','near-upper-sleeve','head-hair-neck']
colors=sorted({p[:3] for im in base.values() for p in im.getdata() if p[3]});legend={c:'#%02x%02x%02x'%v for c,v in zip(string.ascii_letters,colors)};rev={tuple(bytes.fromhex(v[1:]))+(255,):c for c,v in legend.items()}
def lerp(t,points):
 for (a,v),(b,w) in zip(points,points[1:]):
  if a<=t<=b:return v+(w-v)*(t-a)/(b-a)
 return points[0][1] if t<points[0][0] else points[-1][1]
def deform(im,ymap,xshift):
 out=Image.new('RGBA',im.size)
 for y in range(264):
  sy=round(lerp(y,[(d,s) for s,d in ymap]));dx=round(lerp(sy,xshift))
  if 0<=sy<264:out.paste(im.crop((0,sy,128,sy+1)),(dx,y))
 return out
def rigid(im,dx,dy):o=Image.new('RGBA',im.size);o.alpha_composite(im,(dx,dy));return o
poses=[];ops={}
for k in range(3):
 parts={n:im.copy() for n,im in base.items()}
 if k:
  if k==1:
   parts['head-hair-neck']=rigid(base['head-hair-neck'],0,-1)
   parts['upper-torso']=deform(base['upper-torso'],[(0,-1),(45,44),(49,47),(65,63),(80,79),(88,88),(263,263)],[(0,0),(65,-1),(88,0),(263,0)])
   parts['near-upper-sleeve']=deform(sleeve,[(0,-2),(53,51),(72,70),(86,85),(92,91),(263,262)],[(0,0),(55,0),(80,-1),(263,-1)])
   parts['near-guard-hand']=rigid(guard,-1,-1)
   parts['far-hand']=rigid(base['far-hand'],0,-1)
  else:
   parts['head-hair-neck']=rigid(base['head-hair-neck'],-2,-2)
   parts['upper-torso']=deform(base['upper-torso'],[(0,-3),(45,42),(49,45),(65,62),(80,79),(88,88),(263,263)],[(0,-2),(65,-2),(80,-1),(88,0),(263,0)])
   parts['near-upper-sleeve']=deform(sleeve,[(0,-4),(53,49),(72,69),(86,84),(92,90),(263,261)],[(0,-2),(55,-2),(80,-3),(263,-3)])
   parts['near-guard-hand']=rigid(guard,-2,-2)
   parts['far-hand']=rigid(base['far-hand'],-1,-2)
 comp=Image.new('RGBA',(128,264));ops[str(k)]={}
 for n in layers:
  im=parts[n];im.save(K/f'data-{k}-{n}.png');comp.alpha_composite(im)
  b=im.getbbox()
  if b:
   x0,y0,x1,y1=b;rows=[''.join(rev.get(im.getpixel((x,y)),'.') for x in range(x0,x1)) for y in range(y0,y1)];ops[str(k)][n]=[{'kind':'grid','x':x0,'y':y0,'rows':rows,'legend':legend}]
  else:ops[str(k)][n]=[]
 comp.save(K/f'data-key-{k}.png');poses.append(comp)
assert poses[0].tobytes()==Image.open(I/'rest-native-mcp.png').convert('RGBA').tobytes()
mask=Image.new('L',(128,264));ImageDraw.Draw(mask).rectangle((24,9,91,152),fill=255);mask.save(P/'editable-upper-frozen.png')
json.dump({'layers':layers,'ops':ops,'source_sha256':hashlib.sha256((I/'idle-r01.aseprite').read_bytes()).hexdigest(),'source_rest_exact':True,'split_y':93,'guard_hand_rigid_offsets':[[0,0],[-1,-1],[-2,-2]],'head_rigid_offsets':[[0,0],[0,-1],[-2,-2]],'motion_only_reference':'traveler r04 137body -> main240body; shoulders4up skull2up/back; sample width/no puff rules retained'},open(P/'key-ops.json','w'),indent=2)
