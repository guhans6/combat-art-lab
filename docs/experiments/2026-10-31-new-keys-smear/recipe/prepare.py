"""Source-guided literal grids/masks. Native art is drawn/saved/exported ONLY by MCP.
No Aseprite writer or editor subprocess. See plan.md for registration and ownership.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np, json,sys,math,hashlib
R=Path(__file__).resolve().parents[1]; W,H=256,208
sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'))
from native_read import read,composite
NAMES=['00-legs-shoes','01-rear-handle','02-jacket-sleeves','03-shirt-neck-backing','04-tote-body-rim','05-near-handles-seams','06-hands-forearms','07-rigid-head']
base=read(R/'inputs/original-neutral.aseprite');pal=next(c for c in base['chunks'] if c['type']==0x2019)
# palette read from actual opaque baseline pixels; all are native palette entries.
cols=sorted(set(composite(base,0).get_flattened_data())-{(0,0,0,0)})
COL=np.array([c[:3] for c in cols],dtype=np.int32)
PALETTE=['#00000000']+['#%02x%02x%02x'%tuple(c) for c in COL]
(R/'recipe/palette.json').write_text(json.dumps(PALETTE))
def empty():return Image.new('RGBA',(W,H))
def rgba(c):return tuple(int(c[i:i+2],16) for i in (1,3,5))+(255,)
def polygon(im,p,c):ImageDraw.Draw(im).polygon(p,fill=c)
def line(im,p,c,w=1):ImageDraw.Draw(im).line(p,fill=c,width=w)
def grid(im):
 box=im.getbbox()
 if not box:return None
 cs=list(dict.fromkeys(im.crop(box).get_flattened_data()));cs=[c for c in cs if c[3]]
 rev={c:chr(0x100+i) for i,c in enumerate(cs)}
 return dict(kind='grid',x=box[0],y=box[1],rows=[''.join(rev.get(im.getpixel((x,y)),'.') for x in range(box[0],box[2])) for y in range(box[1],box[3])],legend={rev[c]:'#%02x%02x%02x'%c[:3] for c in cs},transparent='erase')
def snap(im):
 a=np.array(im); op=a[:,:,3]>0;pix=a[:,:,:3][op].astype(np.int32);out=np.zeros_like(a)
 # chunk distances to avoid enormous allocation
 q=[]
 for j in range(0,len(pix),10000):q.extend(np.argmin(((pix[j:j+10000,None,:]-COL[None,:,:])**2).sum(2),axis=1))
 out[:,:,:3][op]=COL[np.array(q,dtype=int)];out[:,:,3][op]=255
 return Image.fromarray(out)
def orig():
 out={n:empty() for n in NAMES}
 mapping={'00-shoes':0,'01-denim':0,'02a-jacket-left':2,'02b-jacket-right':2,'03-shirt':3,'04-tote':4,'05-tote-strap':5,'06a-left-hand':6,'06b-right-hand':6,'07-face-and-neck':7,'08-hair-tie-and-hair':7}
 for li,meta in enumerate(base['layers']):
  if not meta['flags']&1:continue
  im=base['cels'][(0,li)]['image'];out[NAMES[mapping[meta['name']]]].alpha_composite(im,(60,8))
 return out
ORIG=orig()
# Head copied as a RIGID form, neck excluded at y42 and reconstructed on owner03.
HEAD=ORIG[NAMES[7]].copy();ha=np.array(HEAD);ha[42:]=0;HEAD=Image.fromarray(ha)
# Raw images are complete poses. Spatial limits enclose subject, never inferred from alpha box.
P={
 1:dict(file='01-idle.png',hip=(685,431),floor=1037,pelvis=(123,76),cut=230,neck=(706,240),grip=(0,0),angle=0,roi=(520,30,980,1060)),
 2:dict(file='02-strap-lift.png',hip=(684,430),floor=1052,pelvis=(123,76),cut=224,neck=(699,239),grip=(147,49),angle=0,roi=(510,15,980,1070)),
 3:dict(file='03-strap-grip.png',hip=(704,424),floor=1034,pelvis=(124,76),cut=222,neck=(730,238),grip=(145,62),angle=0,roi=(530,15,990,1060)),
 4:dict(file='04-windup.png',hip=(738,474),floor=1050,pelvis=(125,81),cut=231,neck=(751,247),grip=(96,94),angle=29,roi=(330,15,1100,1070)),
 5:dict(file='05-swing.png',hip=(718,430),floor=1052,pelvis=(127,78),cut=235,neck=(650,250),grip=(174,68),angle=-50,roi=(400,10,1290,1070)),
 6:dict(file='06-recovery.png',hip=(760,455),floor=1054,pelvis=(127,78),cut=238,neck=(685,255),grip=(160,79),angle=-43,roi=(490,15,1250,1075))}
def clean_source(k):
 p=P[k];im=Image.open(R/'inputs'/p['file']).convert('RGBA')
 cache=R/f'recipe/source-mask-{k:02}.png'
 if cache.exists():
  a=np.array(im);m=np.array(Image.open(cache))>0;a[~m]=0;a[m,3]=255;return Image.fromarray(a)
 a=np.array(im);rgb=a[:,:,:3].astype(int);rr,gg,bb=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
 spatial=np.zeros(a.shape[:2],dtype=bool);x0,y0,x1,y1=p['roi'];spatial[y0:y1,x0:x1]=True
 # Reviewed contamination hues: red/yellow fringes, royal blue/cyan/green spill.
 chroma=((rr>220)&(gg<105)&(bb<105))|((rr>200)&(gg>180)&(bb<95))|((bb>180)&(rr<65))|((gg>170)&(rr<85)&(bb<140))
 mask=(a[:,:,3]>=160)&spatial&~chroma
 # Keep main eight-connected figure. Threshold removed disconnected low-alpha distant pixels.
 seen=np.zeros(mask.shape,bool);components=[]
 for yy,xx in zip(*np.where(mask)):
  if seen[yy,xx]:continue
  todo=[(int(xx),int(yy))];seen[yy,xx]=True;comp=[]
  while todo:
   x,y=todo.pop();comp.append((x,y))
   for dy in (-1,0,1):
    for dx in (-1,0,1):
     nx,ny=x+dx,y+dy
     if 0<=nx<im.width and 0<=ny<im.height and mask[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;todo.append((nx,ny))
  components.append(comp)
 keep=max(components,key=len);m=np.zeros(mask.shape,bool)
 for x,y in keep:m[y,x]=True
 a[~m]=0;a[m,3]=255
 Image.fromarray((m*255).astype('uint8')).save(R/f'recipe/source-mask-{k:02}.png')
 # Raw source diagnostic, explicitly not a native master/runtime export.
 diagnostic=Image.fromarray(a).resize((261,195),Image.Resampling.NEAREST)
 diagnostic.save(R/f'review/raw-conversion-{k:02}.png')
 return Image.fromarray(a)
def xy(k,x,y):
 p=P[k];hx,hy=p['hip'];px,py=p['pelvis'];sy=.18 if y<=hy else (192-py)/(p['floor']-hy)
 return px+.18*(x-hx),py+sy*(y-hy)
def source_parts(k):
 p=P[k];im=clean_source(k);src=np.array(im);out={n:empty() for n in NAMES}
 # Inverse sample with anatomical hip/sole registration, no silhouette fitting.
 yy,xx=np.mgrid[0:H,0:W];hx,hy=p['hip'];px,py=p['pelvis'];sx=np.rint(hx+(xx-px)/.18).astype(int);sy=np.rint(hy+(yy-py)/np.where(yy<=py,.18,(192-py)/(p['floor']-hy))).astype(int)
 valid=(sx>=0)&(sx<im.width)&(sy>=0)&(sy<im.height);sample=np.zeros((H,W,4),dtype=np.uint8);sample[valid]=src[sy[valid],sx[valid]]
 # Source head omitted; canonical head/neck join is explicit.
 sample[sy<p['cut']]=0
 r,g,b=[sample[:,:,j].astype(int) for j in range(3)];skin=(r>155)&(r-g>38)&(g-b>10)
 blue=(b>r+10)&(g>r+5)
 beige=(r>130)&(r>=g)&((r-g)<65)&(b>g-55)
 # Color classification is subordinate to reviewed anatomical skin regions.
 hand_regions={
 1:[[(550,425),(625,425),(625,495),(550,495)],[(748,430),(832,430),(832,500),(748,500)]],
 2:[[(790,220),(855,220),(865,355),(815,355)],[(545,425),(610,425),(610,495),(545,495)]],
 3:[[(765,310),(815,315),(855,370),(838,402),(780,370)],[(575,385),(656,390),(660,450),(575,452)]],
 4:[[(568,410),(623,422),(600,484),(575,536),(538,548),(530,515)],[(676,413),(721,439),(629,527),(601,552),(565,545),(563,515)]],
 5:[[(870,302),(1010,350),(1012,389),(973,392),(854,345)],[(819,337),(970,361),(991,402),(963,421),(816,378)]],
 6:[[(866,377),(937,422),(959,455),(944,481),(910,465),(848,420)],[(789,394),(922,432),(953,460),(945,486),(887,479),(784,434)]]}
 hm=Image.new('1',im.size);hd=ImageDraw.Draw(hm)
 for poly in hand_regions[k]:hd.polygon(poly,fill=1)
 hand_region=np.array(hm)[np.clip(sy,0,im.height-1),np.clip(sx,0,im.width-1)]
 skin=skin&((sy<310)|hand_region)
 prop=np.zeros((H,W),bool)
 if k<=3:
  bp={1:[(792,440),(865,440),(910,599),(800,625)],2:[(791,419),(865,410),(935,600),(883,638),(812,628),(789,470)],3:[(798,422),(870,424),(930,544),(889,607),(818,609),(790,474)]}
  bm=Image.new('1',im.size);ImageDraw.Draw(bm).polygon(bp[k],fill=1)
  prop=(np.array(bm)[np.clip(sy,0,im.height-1),np.clip(sx,0,im.width-1)]|((sx>775)&(sy>220)&beige))&~(skin&hand_region)
 elif k==4:
  bm=Image.new('1',im.size);ImageDraw.Draw(bm).polygon([(325,545),(621,532),(598,662),(572,850),(325,850)],fill=1)
  prop=np.array(bm)[np.clip(sy,0,im.height-1),np.clip(sx,0,im.width-1)]&~(skin&hand_region)
 elif k==5:prop=(sx>949)&(sy<750)&~(skin&hand_region)
 elif k==6:prop=(sx>917)&(sy<790)&~(skin&hand_region)
 sample[prop]=0
 # Explicit semantic material ownership; shoes belong to legs, skin neck separate from arms.
 leg=blue|(sy>900)
 hand_skin=hand_region&(r>95)&(r-g>20)&(g-b>5)
 neck=skin&(sy<310)&(abs(sx-p['neck'][0])<65)&~hand_region
 hands=(skin|hand_skin)&~neck&~leg
 shirt=(beige&~skin&~leg)|neck
 jacket=~(leg|hands|shirt)
 for idx,mask in [(0,leg),(2,jacket),(3,shirt),(6,hands)]:
  ar=sample.copy();ar[~mask]=0;out[NAMES[idx]]=snap(Image.fromarray(ar))
 if k<=3:out[NAMES[0]]=ORIG[NAMES[0]].copy()
 # Put source top at the original skull/neck pivot; no original neck below y41.
 nx,ny=xy(k,*p['neck']);dx=round(nx-125);dy=round(ny-41)
 head=empty();head.alpha_composite(HEAD,(dx,dy));out[NAMES[7]]=head
 # Skin backing under the head to source collar. Native palette samples from baseline.
 d=ImageDraw.Draw(out[NAMES[3]]);d.polygon([(123+dx,37+dy),(133+dx,39+dy),(132+dx,47+dy),(126+dx,49+dy),(121+dx,45+dy)],fill='#fda977')
 d.line([(123+dx,39+dy),(124+dx,44+dy)],fill='#d68e69',width=2)
 # Ensure the shoulder/hood junction has material backing, not an isolated neck overlay.
 # Existing source collar remains uppermost where its actual coverage supports the form.
 return out
O='#795246';D='#b78e82';S='#d2a595';M='#dfb39b';B='#fcd8b6';L='#fadcc4'
def bag(grip,angle,detail=False,smear=False,carry=False,drop=18):
 out={n:empty() for n in NAMES};g=grip;t=math.radians(angle)
 def pt(p):
  u,v=p
  if v>0:v=v*drop/18 if v<=18 else v+drop-18
  if carry:u*=.67
  # Deliberate one-frame directional deformation, not normal body rescaling.
  if smear:
   u=u*1.35+(v-20)*.7;v=20+(v-20)*.72
  return round(g[0]+u*math.cos(t)-v*math.sin(t)),round(g[1]+u*math.sin(t)+v*math.cos(t))
 def ln(layer,p,c,w=1):line(out[NAMES[layer]],[pt(v) for v in p],c,w)
 def poly(layer,p,c):polygon(out[NAMES[layer]],[pt(v) for v in p],c)
 for side in (-1,1):ln(1,[(side,0),(side*3,8),(side*8,17)],M,2)
 poly(4,[(-11,18),(-8,15),(8,15),(11,18),(9,21),(-9,21)],D)
 poly(4,[(-8,18),(-5,17),(6,17),(8,18),(6,20),(-6,20)],O)
 outline=[(-11,19),(-8,18),(-4,20),(4,20),(9,18),(11,20),(13,38),(12,43),(8,47),(-6,48),(-11,44),(-13,39)]
 poly(4,outline,D)
 poly(4,[(-10,20),(-7,20),(-3,22),(4,22),(9,20),(10,21),(12,38),(11,42),(7,46),(-6,47),(-10,43),(-12,38)],B)
 poly(4,[(8,22),(10,21),(12,38),(11,42),(7,46),(5,44),(7,37)],M)
 poly(4,[(-12,37),(-8,43),(-4,46),(5,45),(7,46),(-6,47),(-10,43)],S)
 for side in (-1,1):
  ln(5,[(side,0),(side*3,8),(side*7,16),(side*8,21),(side*8,24)],M,3)
  ln(5,[(side,0),(side*3,8),(side*7,16),(side*8,21),(side*8,24)],L,1)
  ln(5,[(side*9,21),(side*9,25)],S)
 if detail:
  poly(4,[(-6,25),(-5,32),(-5,40),(-2,45),(-5,43),(-7,36)],S)
  poly(4,[(5,26),(3,34),(5,41),(7,44),(4,42),(1,34)],M)
  ln(4,[(-9,39),(-7,42),(-5,43)],M)
 return out,{n:pt(v) for n,v in {'G':(0,0),'FL':(-8,17),'FR':(8,17),'NL':(-8,23),'NR':(8,23),'M':(0,18),'bottom':(0,48)}.items()}
def merge(a,b):
 out={n:a[n].copy() for n in NAMES}
 for n in NAMES:out[n].alpha_composite(b[n])
 return out
KEYS={1:ORIG};sites={}
for k in range(1,7):
 parts=source_parts(k)
 if k<=3:
  if k==3:g,angle,drop=(143,62),-13,22
  elif k==2:g,angle,drop=(148,49),-3,33
  else:g,angle,drop=(143,62),-13,22
  bg,ss=bag(g,angle,carry=True,drop=drop)
  # Shoulder-side span behind gripping fingers; fabric bands meet the same bundle.
  if k==3:
   for n,wid in [(1,1),(5,3)]:
    line(bg[NAMES[n]],[(143,44),(142,56),g],M,wid)
    if n==5:line(bg[NAMES[n]],[(143,45),(143,56),g],L)
  parts=merge(parts,bg)
 else:
  bg,ss=bag(p['grip'] if False else P[k]['grip'],P[k]['angle']);parts=merge(parts,bg)
 # Source proposal01 is correspondence/seed only; exact original remains key1.
 KEYS[k+1]=parts;sites[k+1]=ss

def save_calls(parts,frame):
 calls=[]
 for n in NAMES:
  op=grid(parts[n])
  if op:calls.append(dict(frame=frame,layer=n,createCel=True,label=f'structural key F{frame} {n}',ops=[op]))
 return calls
calls=[]
# six structural frames: exact neutral, reach, free-hand, windup, extension, recovery.
key_order=[1,3,4,5,6,7]
for f,k in enumerate(key_order,1):calls+=save_calls(KEYS[k],f)
(R/'recipe/structural-calls.json').write_text(json.dumps(calls,ensure_ascii=False))
(R/'recipe/key-sites.json').write_text(json.dumps({'key_order':key_order,'sites':sites,'source_registration':P,'original_landmarks':{'crown':[125,10],'chin':[132,38],'waist':[123,76],'crotch':[126,99],'knees_y':143,'sole_y':192},'native_layers':NAMES},indent=2))
# Serialized literal grids retained as canonical build inputs, no authored PNG/native writing here.
(R/'recipe/keys.json').write_text(json.dumps({str(k):{n:grid(im) for n,im in v.items()} for k,v in KEYS.items()},ensure_ascii=False))
print('Prepared',len(calls),'MCP cel drawings; palette',len(PALETTE),'source masks6; native files not written.')
