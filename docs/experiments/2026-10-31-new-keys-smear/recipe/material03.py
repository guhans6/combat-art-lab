"""Focused final material/wrist correction. Native mutation is performed by MCP grids only."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,sys,math,json,itertools
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'recipe'));import prepare as p;import transfers as tr
N=p.NAMES;a=p.read(R/'source/tote-clean.aseprite');ref=p.read(R/'source/structural-pass03.aseprite');rj=ref['cels'][(3,2)]['image'];rh=ref['cels'][(3,6)]['image'];spec=json.loads((R/'recipe/transfer-sites.json').read_text())
G={6:(116,92),8:(122,93),9:(155,83),14:(144,84)}
def arms_for(f):
 if f in [4,16]:return spec['sites']['release']['arms']
 if f in [5,15]:return spec['sites']['gather']['arms']
 g=G[f]
 if f in [6,8]:return [((109,49),(108,76),(g[0]-3,g[1]-3),(g[0]-2,g[1]-1)),((138,50),(140,76),(g[0]+3,g[1]-3),(g[0]+2,g[1]))]
 if f==14:return [((109,49),(121,72),(g[0]-3,g[1]-2),(g[0]-2,g[1]-1)),((138,50),(146,71),(g[0]+3,g[1]-2),(g[0]+2,g[1]))]
 return [((103,51),(126,69),(g[0]-5,g[1]-3),(g[0]-2,g[1]-1)),((133,52),(141,72),(g[0]+2,g[1]-3),(g[0]+2,g[1]))]
def axes(s,e):
 s=np.array(s,dtype=float);e=np.array(e,dtype=float);u=(e-s)/np.linalg.norm(e-s);return s,e,u,np.array([-u[1],u[0]]),float(np.linalg.norm(e-s))
def sample(im,s,e,t,n):
 s,e,u,v,L=axes(s,e);xy=s+(e-s)*t+v*n;x,y=round(xy[0]),round(xy[1]);return im.getpixel((x,y)) if 0<=x<256 and 0<=y<208 else (0,0,0,0)
def hand(im,w,h,near):
 w=np.array(w,float);h=np.array(h,float);u=h-w;u=u/np.linalg.norm(u) if np.linalg.norm(u) else np.array([0.,1.]);v=np.array([-u[1],u[0]])
 def pt(x,y):return tuple(np.rint(h+u*x+v*y).astype(int))
 d=ImageDraw.Draw(im);d.polygon([pt(-3,-2),pt(1,-3),pt(3,-1),pt(3,1),pt(1,2),pt(-3,2)],fill='#c87453')
 d.polygon([pt(-2,-1),pt(1,-2),pt(2,-1),pt(2,1),pt(0,1),pt(-2,1)],fill='#fda977' if near else '#fa9e74')
 # Light knuckle plane; short curved thumb crosses retained handle bundle.
 d.line([pt(-1,-1),pt(1,-1)],fill='#feb881');d.line([pt(1,-2),pt(2,-1),pt(2,0)],fill='#e48558')
 d.polygon([pt(-2,1),pt(-1,3),pt(1,3),pt(1,1)],fill='#f69968');d.line([pt(-1,2),pt(0,2)],fill='#fbc095')
 # Finger divisions at the grip-facing edge, not bands across the entire forearm.
 d.point(pt(3,-1),fill='#c7744e');d.point(pt(3,1),fill='#d68e69');d.point(pt(1,1),fill='#f18755')

def correct(f):
 oldj=a['cels'][(f-1,2)]['image'];j=oldj.copy();skin=p.empty();arms=arms_for(f)
 for i,(s,e,w,h) in enumerate(arms):
  srcs,srce=([(113,49),(108,75)] if i==0 else [(143,49),(128,77)])
  sleeve=p.empty();tr.tube(sleeve,s,e,8,6,'white');sm=np.array(sleeve.getchannel('A'))>0;ja=np.array(j);s0,e0,u,v,L=axes(s,e)
  for yy,xx in zip(*np.where(sm & (ja[:,:,3]>0))):
   q=np.array([xx,yy])-s0;t=float(np.dot(q,u)/L);n=float(np.dot(q,v));c=sample(rj,srcs,srce,max(0,min(1,t)),n)
   rr,gg,bb=c[:3]
   if c[3] and gg>bb+8 and abs(rr-gg)<35:ja[yy,xx,:3]=c[:3]
  j=Image.fromarray(ja)
  # Forearm anatomical contour: cuff has substance, wrist narrows before distinct palm.
  tr.tube(skin,e,w,3,2,'#c87453');tr.tube(skin,(e[0],e[1]-1),(w[0],w[1]-1),2,1,'#fda977')
  sk=np.array(skin);ss,ee,uu,vv,ll=axes(e,w)
  # Read source winding-arm material, mapped to corresponding anatomical length/cross-section.
  source_e,source_w=([(108,75),(96,92)] if i==0 else [(128,77),(99,93)])
  for yy,xx in zip(*np.where(sk[:,:,3]>0)):
   q=np.array([xx,yy])-ss;t=float(np.dot(q,uu)/ll);n=float(np.dot(q,vv))
   if not -.05<=t<=1.03 or abs(n)>3.1:continue
   c=sample(rh,source_e,source_w,max(0,min(1,t)),n)
   rr,gg,bb=c[:3]
   if c[3] and rr>120 and rr-gg>22 and gg-bb>5:sk[yy,xx,:3]=c[:3]
  skin=Image.fromarray(sk);d=ImageDraw.Draw(skin)
  # Wrist crease is short and follows the palm axis; no orange cylindrical cap.
  vx,vy=vv;d.line([(round(w[0]+vx),round(w[1]+vy)),(round(w[0]-vx),round(w[1]-vy))],fill='#d68e69');hand(skin,w,h,i==1)
 return j,skin
out=[];masks=[]
for f in [4,5,6,8,9,14,15,16]:
 j,skin=correct(f)
 for l,im in [(2,j),(6,skin)]:
  op=p.grid(im);op['rle']=[''.join(str(len(list(g)))+ch for ch,g in itertools.groupby(row)) for row in op.pop('rows')]
  c=dict(frame=f,layer=N[l],createCel=True,label=f'F{f} source-guided sleeve and anatomical wrist material pass',ops=[op]);out.append(c)
(R/'recipe/material03-calls').mkdir(exist_ok=True)
for i,c in enumerate(out):(R/'recipe/material03-calls'/f'{i:03}.json').write_text(json.dumps(c,ensure_ascii=False,separators=(',',':')))
(R/'recipe/material03-scope.json').write_text(json.dumps({'frames':[4,5,6,8,9,14,15,16],'layers':[N[2],N[6]],'method':'Actual windup source sleeve/forearm colors sampled by anatomical length and crosssection; jacketRGB-only inside existing sleeve; hands contours tapered and palms/fingers/thumbs authored at same grips; head/neck/shirt/legs/prop/timing/palette protected','arms':{f:arms_for(f) for f in [4,5,6,8,9,14,15,16]}},indent=2));print(len(out),'focused calls prepared')
