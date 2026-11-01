"""Prepare authored literal MCP grids and diagnostic guides; never writes native art."""
from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,math,hashlib
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'))
from native_read import read,composite
BASE=R.parent/'2026-10-31-full-attack-repair/source/attack-repaired.aseprite'
a=read(BASE);names={v['name']:i for i,v in enumerate(a['layers'])}
# Existing hand positions are read against native exports. Body and all10other frames locked.
PLAN={8:dict(grip=[174,94],angle=43,crop=[155,73,221,145]),9:dict(grip=[160,79],angle=17,crop=[145,67,195,133]),10:dict(grip=[150,70],angle=10,crop=[135,60,183,124])}
# One object's construction coordinates, origin at shared grip. body22x26,
# mouth at v17, near sewn roots within its front panel at v20.
SITES={'grip':[0,0],'far_left':[-7,16],'far_right':[7,16],
       'near_left':[-7,20],'near_right':[7,20],'bottom':[0,42]}
O='#795246';D='#b78e82';S='#d2a595';M='#dfb39b';B='#fcd8b6';L='#fadcc4'
def point(f,p):
 g=PLAN[f]['grip'];t=math.radians(PLAN[f]['angle']);u,v=p
 return (round(g[0]+u*math.cos(t)+v*math.sin(t)),round(g[1]-u*math.sin(t)+v*math.cos(t)))
def paint(f,detailed):
 rear=Image.new('RGBA',(320,192));front=Image.new('RGBA',(320,192))
 def line(im,pts,c,w=1):ImageDraw.Draw(im).line([point(f,p) for p in pts],fill=c,width=w)
 def poly(im,pts,c):ImageDraw.Draw(im).polygon([point(f,p) for p in pts],fill=c)
 # Far loop terminates behind the rear rim, offset from near straps, not free horns.
 for side in [-1,1]:
  pts=[(side,0),(side*3,7),(side*7,16)]
  line(rear,pts,O,2);line(rear,pts,M,1)
 # F8's upper hand holds the same gathered bundle above the lower palm.
 if f==8:
  ImageDraw.Draw(rear).line([(175,84),(174,94)],fill=O,width=3)
  ImageDraw.Draw(rear).line([(175,84),(174,94)],fill=M,width=1)
 # Rear rim and shallow opening, consistent local orientation through all frames.
 poly(front,[(-10,16),(-7,14),(6,14),(10,16),(9,19),(-9,19)],D)
 poly(front,[(-8,16),(-5,15),(5,15),(8,16),(6,18),(-6,18)],O)
 # Soft body, slight widening below the gathered top and rounded corners.
 outline=[(-10,18),(-8,17),(-4,19),(3,19),(8,17),(10,18),(12,34),(11,39),(8,42),(-6,43),(-10,41),(-12,36)]
 poly(front,outline,D)
 poly(front,[(-9,18),(-7,18),(-3,20),(3,20),(8,18),(9,19),(11,34),(10,38),(7,41),(-6,42),(-9,40),(-11,35)],B)
 # Untextured proof uses only planes; details added after structural review.
 poly(front,[(7,20),(9,19),(11,34),(10,38),(7,41),(5,40),(7,34)],M)
 poly(front,[(-10,31),(-8,38),(-4,41),(4,40),(7,41),(-6,42),(-9,40)],S)
 # Near loop is integrated INTO the front face, roots inside its material boundary.
 for side in [-1,1]:
  pts=[(side,0),(side*3,7),(side*6,14),(side*7,19),(side*7,22)]
  line(front,pts,M,3);line(front,pts,L,1)
  # Small stitch shadow / fold begins at sewn root, does not protrude sideways.
  line(front,[(side*8,20),(side*8,23)],S,1)
 if detailed:
  poly(front,[(-6,24),(-5,29),(-5,36),(-3,40),(-5,39),(-7,34)],S)
  poly(front,[(5,24),(4,30),(5,36),(7,40),(5,39),(2,32)],M)
  line(front,[(-6,25),(-6,30)],M)
  line(front,[(-10,34),(-8,38),(-6,39)],M)
 return rear,front

def grid(im,crop):
 colors=list(dict.fromkeys(p for p in im.crop(crop).get_flattened_data() if p[3]));legend={chr(0x100+i):'#%02x%02x%02x'%c[:3] for i,c in enumerate(colors)};rev={c:chr(0x100+i) for i,c in enumerate(colors)}
 return dict(kind='grid',x=crop[0],y=crop[1],rows=[''.join(rev.get(im.getpixel((x,y)),'.') for x in range(crop[0],crop[2])) for y in range(crop[1],crop[3])],legend=legend,transparent='erase')
# Masks include previous owner extents and new connected form; only named owners allowed.
manifest={'base':str(BASE),'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'frames':{},'sites_local':SITES,'body_construction_width':24,'body_construction_height':26,'note':'geometry is a proposed common cloth construction, not a physical simulation or art score'}
for detail,tag in [(False,'structural'),(True,'detail')]:
 calls=[]
 for f,p in PLAN.items():
  rear,front=paint(f,detail)
  for name,im in [('06-continuous-handle-tension',rear),('04-tote-and-handles',front)]:
   # Explicit whole cel replacement only for these two prop owners; all previous pixels contained.
   calls.append(dict(frame=f,layer=name,createCel=True,label=f'{tag} connected bag F{f}',ops=[grid(im,p['crop'])]))
 (R/'operations'/f'{tag}.json').write_text(json.dumps(calls,ensure_ascii=False))
# Baseline ownership/landmark evidence, no proposed art raster output.
for f,p in PLAN.items():
 im=composite(a,f-1);c=p['crop'];scale=5;w=(c[2]-c[0])*scale;h=(c[3]-c[1])*scale
 out=Image.new('RGBA',(4*(w+16),h+45),'#303336');d=ImageDraw.Draw(out)
 bag=a['cels'][f-1,names['04-tote-and-handles']]['image'];strap=a['cels'][f-1,names['06-continuous-handle-tension']]['image']
 hidden=Image.new('RGBA',(320,192))
 for l,meta in enumerate(a['layers']):
  if l!=names['04-tote-and-handles'] and (f-1,l) in a['cels']:hidden.alpha_composite(a['cels'][f-1,l]['image'])
 for i,(lab,v) in enumerate([('actual composite',im),('bag owner',bag),('handle owner',strap),('bag hidden',hidden)]):
  x=i*(w+16);d.text((x+4,5),f'F{f} {lab}',fill='white');out.alpha_composite(v.crop(c).resize((w,h),Image.Resampling.NEAREST),(x,30))
 out.convert('RGB').save(R/'review'/f'baseline-owners-f{f}.png')
 mask=Image.new('L',(320,192));md=ImageDraw.Draw(mask);md.rectangle((c[0],c[1],c[2]-1,c[3]-1),fill=255);mask.save(R/'review'/f'allowed-f{f}.png')
 sites={name:list(point(f,xy)) for name,xy in SITES.items()};manifest['frames'][str(f)]={**p,'sites':sites,'allowed_owners':['06-continuous-handle-tension','04-tote-and-handles','05-loaded-grip-drawing']}
 # Body identity is locked exactly; mark same native points and construction proposal over baseline.
 guide=im.copy();gd=ImageDraw.Draw(guide)
 for name,xy in sites.items():gd.ellipse((xy[0]-1,xy[1]-1,xy[0]+1,xy[1]+1),fill='#ff00ff')
 gd.line([tuple(sites['grip']),tuple(sites['bottom'])],fill='#00ffff')
 guide.resize((960,576),Image.Resampling.NEAREST).save(R/'review'/f'baseline-guide-f{f}.png')
(R/'scope.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Prepared scoped grids and baseline owner/guide evidence. No native edits made by Python.')
