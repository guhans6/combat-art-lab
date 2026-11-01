"""Two structural transfer drawings from native key3. Literal grids only."""
from pathlib import Path
from PIL import Image,ImageDraw
import sys,math,json,itertools
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'recipe'));import prepare as p
# prepare import regenerates reproducible source grids, never native.
a=p.read(R/'source/structural-pass03.aseprite');N=p.NAMES
base={n:a['cels'].get((2,i),{}).get('image',p.empty()).copy() for i,n in enumerate(N)}
def tube(im,s,e,w0,w1,c):
 dx=e[0]-s[0];dy=e[1]-s[1];ln=math.hypot(dx,dy);nx=-dy/ln;ny=dx/ln
 pts=[(round(s[0]+nx*w0),round(s[1]+ny*w0)),(round(e[0]+nx*w1),round(e[1]+ny*w1)),(round(e[0]-nx*w1),round(e[1]-ny*w1)),(round(s[0]-nx*w0),round(s[1]-ny*w0))]
 d=ImageDraw.Draw(im);d.polygon(pts,fill=c);d.ellipse((s[0]-w0,s[1]-w0,s[0]+w0,s[1]+w0),fill=c);d.ellipse((e[0]-w1,e[1]-w1,e[0]+w1,e[1]+w1),fill=c)
def pose(kind):
 out={n:im.copy() for n,im in base.items()}
 # Actual old sleeves/hands are replaced on their owners. Source torso core is retained.
 core=Image.new('L',(p.W,p.H));ImageDraw.Draw(core).polygon([(115,44),(137,44),(143,55),(140,78),(145,96),(133,92),(127,79),(118,91),(106,97),(111,77),(108,59)],fill=255)
 j=out[N[2]];j.putalpha(Image.composite(j.getchannel('A'),Image.new('L',j.size),core));out[N[2]]=j
 for n in [1,4,5,6]:out[N[n]]=p.empty()
 # Reconstruct continuous coat backing exposed by replacing the source sleeves.
 backing=p.empty();bd=ImageDraw.Draw(backing)
 bd.polygon([(112,46),(118,48),(117,62),(115,75),(114,85),(107,98),(103,96),(107,82),(108,65)],fill='#6b6342')
 bd.polygon([(135,47),(141,49),(144,65),(140,81),(144,96),(137,93),(132,81),(132,63)],fill='#48432d')
 backing.alpha_composite(out[N[2]]);out[N[2]]=backing
 sleeves=p.empty();arms=p.empty()
 if kind=='release':
  armspec=[((112,50),(126,73),(151,62),(156,61)),((140,49),(167,67),(157,44),(157,42))];g=(157,43);angle=-6;drop=32
 else:
  armspec=[((112,50),(110,74),(129,85),(132,85)),((140,49),(143,73),(136,84),(135,85))];g=(134,86);angle=-6;drop=18
 for s,e,w,h in armspec:
  # Connected sleeve: contour, two planes, cuff; no whole-part image warp.
  tube(sleeves,s,e,8,6,'#433b29');tube(sleeves,(s[0],s[1]-1),(e[0],e[1]-1),7,5,'#6b6342')
  d=ImageDraw.Draw(sleeves);d.line([(s[0]-2,s[1]+5),(e[0]-2,e[1]+3)],fill='#48432d',width=3);d.line([(s[0]+2,s[1]-4),(e[0]+2,e[1]-2)],fill='#7a7246',width=2)
  dx=w[0]-e[0];dy=w[1]-e[1];ln=math.hypot(dx,dy);v=(-dy/ln,dx/ln)
  d.line([(round(e[0]+v[0]*5),round(e[1]+v[1]*5)),(round(e[0]-v[0]*5),round(e[1]-v[1]*5))],fill='#48432d',width=2)
  tube(arms,e,w,4,3,'#c87453');tube(arms,(e[0],e[1]-1),(w[0],w[1]-1),3,2,'#fda977');tube(arms,w,h,3,3,'#fda977')
  ad=ImageDraw.Draw(arms);ad.line([(h[0]-2,h[1]+1),(h[0]+2,h[1]+1)],fill='#d68e69');ad.point((h[0]+2,h[1]-2),fill='#feb881')
 # Sleeve overlap replaces underlying shirt pixels on their real owner.
 shirt=out[N[3]];sa=shirt.getchannel('A');sa.paste(0,mask=sleeves.getchannel('A'));shirt.putalpha(sa);out[N[3]]=shirt
 out[N[2]].alpha_composite(sleeves);out[N[6]]=arms
 bg,sites=p.bag(g,angle,carry=(kind=='release'),drop=drop)
 out=p.merge(out,bg)
 return out,sites,armspec
calls=[];sites={}
for f,name in [(7,'release'),(8,'gather')]:
 out,ss,arms=pose(name);sites[name]={'frame':f,'sites':ss,'arms':arms,'roles':('Right hand retains original shoulder strap, lifts bundle outside shoulder atx157/y43; left catches lower strand at154/61. No strap remains resting on shoulder.' if name=='release' else 'Both hands gather same near/far straps at134/86; right retains original bundle; left closes around lower bundle; no release before strike.')}
 for n in N:
  op=p.grid(out[n])
  if op:
   op['rle']=[''.join(str(len(list(g)))+ch for ch,g in itertools.groupby(row)) for row in op.pop('rows')]
   c=dict(frame=f,layer=n,createCel=True,label=f'{name} structural transfer {n}',ops=[op]);(R/'recipe/calls'/f'transfer-{len(calls):03}.json').write_text(json.dumps(c,ensure_ascii=False,separators=(',',':')));calls.append(c)
(R/'recipe/transfer-sites.json').write_text(json.dumps({'forward':[3,7,8,4],'return':[6,8,7,3,2,1],'sites':sites,'intent':'On return, right lifts retained bundle to shoulder; shoulder accepts loop in key3; left releases only after shoulder supports load, then right releases to pocket through key2→neutral. No bag redesign.'},indent=2));print('transfer calls',len(calls))
