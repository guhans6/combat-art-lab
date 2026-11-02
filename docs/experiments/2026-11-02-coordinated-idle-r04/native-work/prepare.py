from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib,string,shutil
P=Path('/private/tmp/atmospheric-idle-sample-r04');sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
src=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/source/atmospheric-traveler/idle-r03/grounded-idle.aseprite');shutil.copy2(src,P/'baseline-r03.aseprite');A=read(src);names=[l['name']for l in A['layers']];base={n:A['cels'][0,i]['image']for i,n in enumerate(names)}
pal=['#15191e','#1c1d20','#303035','#79583d','#ad8056','#b98d60','#24282d','#353a3f','#242d36','#3d4c59','#56636d','#626971','#303338'];legend=dict(zip(string.ascii_letters,pal));rev={v:k for k,v in legend.items()}
def lerp(t,points):
 for (a,v),(b,w) in zip(points,points[1:]):
  if a<=t<=b:return v+(w-v)*(t-a)/(b-a)
 return points[0][1]if t<points[0][0]else points[-1][1]
def warp(im,ymap,xshift):
 out=Image.new('RGBA',im.size)
 # Inverse-map each destination row to the named source form. Pixel rows preserve widths,
 # value roles and hand/head drawings; only a shoulder-to-waist interval stretches.
 for y in range(160):
  sy=round(lerp(y,[(d,s)for s,d in ymap]));dx=round(lerp(sy,xshift))
  if 0<=sy<160:out.paste(im.crop((0,sy,96,sy+1)),(dx,y))
 return out
fixed=names[:6]
def pose(k):
 out={n:im.copy()for n,im in base.items()}
 if not k:return out
 extreme=k==2
 # Connected lift/return hypothesis: shoulders rise slightly toward skull, lean back
 # about a quiet waist. Elbow folds open a little; wrist and hand follow a smaller arc.
 # Pants, cuffs, pelvis and coat skirt remain exact REST throughout.
 if extreme:
  specs={
   'thorax-coat':([(0,-2),(35,33),(48,46),(65,64),(84,84),(159,159)],[(0,-1),(55,-1),(78,0),(159,0)]),
   'neck-collar':([(0,-1),(27,26),(33,32),(45,43),(159,157)],[(0,-1),(159,-1)]),
   'head-hair-face':([(0,-1),(159,158)],[(0,-1),(159,-1)]),
   'near-upper-sleeve':([(0,-2),(39,37),(45,43),(63,62),(66,65),(159,158)],[(0,-1),(45,-1),(60,-2),(159,-2)]),
   'near-forearm-hand':([(0,-1),(159,158)],[(0,-2),(65,-2),(77,-1),(159,-1)]),
   'far-sleeve-hand':([(0,-2),(39,37),(56,54),(72,71),(91,90),(159,158)],[(0,-1),(60,-1),(79,0),(159,0)])}
 else:
  specs={
   'thorax-coat':([(0,-1),(35,34),(60,59),(82,82),(159,159)],[(0,0),(159,0)]),
   'neck-collar':([(0,-1),(159,158)],[(0,0),(159,0)]),
   'head-hair-face':([(0,-1),(159,158)],[(0,0),(159,0)]),
   'near-upper-sleeve':([(0,-1),(39,38),(55,54),(66,66),(159,159)],[(0,0),(45,0),(62,-1),(159,-1)]),
   'near-forearm-hand':([(0,0),(159,159)],[(0,-1),(65,-1),(78,0),(159,0)]),
   'far-sleeve-hand':([(0,-1),(39,38),(60,59),(78,78),(159,159)],[(0,0),(159,0)])}
 for n,(ym,xs)in specs.items():out[n]=warp(base[n],ym,xs)
 return out
ops={}
for k in range(3):
 data=pose(k);ops[str(k)]={};im=Image.new('RGBA',(96,160))
 for n in names:
  q=data[n];im.alpha_composite(q);rows=[]
  for y in range(6,148):
   row=''
   for x in range(28,66):
    v=q.getpixel((x,y));row+='.'if not v[3]else rev['#%02x%02x%02x'%v[:3]]
   rows.append(row)
  ops[str(k)][n]=[{'kind':'grid','x':28,'y':6,'rows':rows,'legend':legend}]
 im.save(P/f'keys/drawing-data-{k}.png')
mask=Image.new('L',(96,160));ImageDraw.Draw(mask).rectangle((28,6,65,94),fill=255);mask.save(P/'editable-upper-frozen.png')
json.dump({'ops':ops,'fixed_native_owners':fixed,'layers':names,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest()},open(P/'key-ops.json','w'),indent=2)
(P/'observations.md').write_text('''# r04 frozen mechanism and key checkpoint\n\nDisposable traveler motion test only; no character proposal and no fighter edits. Baseline is exact r03 REST frame0, not its rejected moving pants. Exact native source frozen as baseline-r03.aseprite (SHA in key-ops.json). Canvas96x160, same14-entry palette including transparent. Soley146, fixed world registration. No palette/light/costume/face change.\n\nInspected native r03 and actual r03-frame/diff/owner diagnosis images, hero2-1 four-pose contact, hero-2 eight-pose contact and Saint11 actual tutorial contact on2026-11-02. Visible principle: shoulder/upper-garment and arm relationships change over planted feet; reference loose clothes conceal knees. Saint11 exaggerated bounce is expressly not target tempo. No source pixels copied. Discrete reference frames inspected; continuous perception not claimed.\n\nOne correction hypothesis: relaxed shoulder girdle rise and mild backward lean about a quiet waist, then return. Upper sleeves rise toward skull by2px at apex while skull moves up/back1px; near elbow retreats2px and rises1px, near hand follows back/up1px. Far elbow/hand follows same gesture with smaller lateral travel. Thorax top follows shoulders while lower waist retains exact registration; torso widths are source row widths, never chest expansion. This is an inferred modest pose mechanism, not an asserted anatomical truth. Critique keys before timing.\n\nPer-part method: rigid exact source reuse for head/hair/face and hand drawing; inverse discrete row mapping retains material planes on torso/sleeves and changes their contour path/arm angles. Pants, bothboots/cuffs, pelvis/root and lowercoat/skirt preserve source REST pixels exactly on every key. No need to expose/invent knee mechanics. Native ownership actually inspected: sleeve overlaps forearm at59–65; near hand belongs forearm77–91; neck/collar27–44 overlaps thorax35–44 and skull27–32; pelvis75–95 and skirt65–101 overlap thorax to85. Must inspect these joins in clean and owner-hidden exports.\n\nBudget one meaningful correction +one concrete qualityrepair. Keys REST/transition/raised-settled built first, no cycle propagation until lead and independent reviewer clear proportions/joins/material continuity. Intended later loop is one slow rise/settle with different holds, not independent clocks. Engine/perceived playback and user approval remain separate.\n\nBackend soleowner: dedicatedMCP headless preflight READY1.3.18.6-dev/Pebbly0.8.2; source sprite_info and composite/forearm ASCII read before edit. Native writes onlyMCP; Pillow used only data/mask/evidence/checks. Callable validate absent; will use independent native/PNG checks and report limitation.\n''')
print('Data prepared; no native file writing in script.')
