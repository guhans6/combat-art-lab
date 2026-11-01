"""Prepare final cycle/control/smear literal native grids. Native writer: dedicated MCP only."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,math,json,itertools,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'recipe'));import prepare as p;import transfers as tr
N=p.NAMES;a=p.read(R/'source/transfer-study02.aseprite')
def key(f):return {n:a['cels'].get((f-1,i),{}).get('image',p.empty()).copy() for i,n in enumerate(N)}
def clear_prop(k):
 o={n:im.copy() for n,im in k.items()}
 for i in [1,4,5]:o[N[i]]=p.empty()
 return o
def replace_bag(o,g,angle,carry=False,drop=18):
 o=clear_prop(o);bg,ss=p.bag(g,angle,detail=True,carry=carry,drop=drop);return p.merge(o,bg),ss

def detail_arms(o,arms):
 # Sparse pose-oriented sleeve folds, no random dither or relighting.
 for s,e,w,h in arms:
  dx=e[0]-s[0];dy=e[1]-s[1];ln=math.hypot(dx,dy);nx=-dy/ln;ny=dx/ln;d=ImageDraw.Draw(o[N[2]])
  for t in [.48,.78]:
   x=s[0]+dx*t;y=s[1]+dy*t
   d.line([(round(x+nx*4),round(y+ny*4)),(round(x-nx*2+dx*.06),round(y-ny*2+dy*.06))],fill='#48432d',width=1)
   d.line([(round(x+nx*3+1),round(y+ny*3-1)),(round(x-nx+1),round(y-ny-1))],fill='#7a7246',width=1)
 return o

def custom(kind,g,angle,legs):
 # Authored changing torso planes and arms; no row-band/body warp.
 o={n:p.empty() for n in N};o[N[0]]=legs.copy()
 shift=(-3,2) if kind in ['launch','counter','return'] else (-10,4)
 o[N[7]].alpha_composite(p.HEAD,shift)
 j=ImageDraw.Draw(o[N[2]]);sh=ImageDraw.Draw(o[N[3]])
 dx=shift[0]+3
 def P(pts):return [(x+dx if y<64 else x,y) for x,y in pts]
 j.polygon(P([(111,44),(120,44),(124,51),(119,63),(117,77),(112,92),(104,98),(102,91),(107,77),(106,62),(104,51)]),fill='#48432d')
 j.polygon(P([(112,46),(118,46),(121,52),(117,64),(115,77),(111,91),(106,94),(108,78),(108,62),(107,52)]),fill='#6b6342')
 j.polygon(P([(132,44),(140,46),(146,53),(149,69),(142,80),(146,94),(137,94),(131,81),(128,68),(129,55)]),fill='#48432d')
 j.polygon(P([(134,47),(139,48),(143,55),(145,68),(138,80),(143,91),(138,91),(133,79),(131,65)]),fill='#6b6342')
 sh.polygon(P([(121,45),(130,46),(132,54),(134,63),(137,76),(133,80),(121,79),(122,70),(119,59),(117,52)]),fill='#fef8ee')
 sh.polygon(P([(121,57),(125,61),(126,65),(123,63)]),fill='#d6b7bb');sh.polygon(P([(130,68),(134,73),(129,73),(125,76),(123,73)]),fill='#d9bcc1')
 # Neck follows same skull pivot, overlaps collar behind it.
 nx,ny=125+shift[0],41+shift[1];sh.polygon([(nx-3,ny-3),(nx+7,ny-1),(nx+7,ny+6),(nx+2,ny+8),(nx-4,ny+4)],fill='#fda977');sh.line([(nx-3,ny-1),(nx-2,ny+4)],fill='#d68e69',width=2)
 if kind in ['launch','counter']:
  arms=[((109,49),(108,76),(g[0]-3,g[1]-3),(g[0]-1,g[1])),((138,50),(140,76),(g[0]+3,g[1]-3),(g[0]+1,g[1]))]
 elif kind=='return':
  arms=[((109,49),(121,72),(g[0]-3,g[1]-2),(g[0]-1,g[1])),((138,50),(146,71),(g[0]+3,g[1]-2),(g[0]+1,g[1]))]
 else:
  arms=[((103,51),(126,69),(g[0]-5,g[1]-3),(g[0]-2,g[1])),((133,52),(141,72),(g[0]+2,g[1]-3),(g[0]+1,g[1]))]
 torso_mask=o[N[2]].getchannel('A').copy()
 sleeves=p.empty();skin=p.empty()
 for s,e,w,h in arms:
  tr.tube(sleeves,s,e,8,6,'#433b29');tr.tube(sleeves,(s[0],s[1]-1),(e[0],e[1]-1),7,5,'#6b6342')
  sd=ImageDraw.Draw(sleeves);sd.line([(s[0]-2,s[1]+5),(e[0]-2,e[1]+3)],fill='#48432d',width=3);sd.line([(s[0]+2,s[1]-4),(e[0]+2,e[1]-2)],fill='#7a7246',width=2)
  tr.tube(skin,e,w,4,3,'#c87453');tr.tube(skin,(e[0],e[1]-1),(w[0],w[1]-1),3,2,'#fda977');tr.tube(skin,w,h,3,3,'#fda977');ImageDraw.Draw(skin).line([(h[0]-2,h[1]+1),(h[0]+2,h[1]+1)],fill='#d68e69')
 shalpha=o[N[3]].getchannel('A');shalpha.paste(0,mask=sleeves.getchannel('A'));o[N[3]].putalpha(shalpha);o[N[2]].alpha_composite(sleeves);o[N[6]]=skin;o=detail_arms(o,arms)
 # Reuse corresponding neutral/source3 material clusters INSIDE the authored planes.
 # The silhouette/neck/arm redraw stays fixed; this transfers RGB only, never source alpha.
 refj=np.array(key(3)[N[2]]);refs=np.array(key(3)[N[3]]);dstj=np.array(o[N[2]]);dsts=np.array(o[N[3]]);tm=np.array(torso_mask)>0;sl=np.array(sleeves.getchannel('A'))>0
 for y in range(44,98):
  for x in range(98,155):
   # Map known body-plane correspondence; blend top neck shift into fixed waistband.
   topdelta=shift[0]+3;rx=round(x-topdelta*max(0,min(1,(80-y)/36)))
   if not 0<=rx<p.W:continue
   c=refj[y,rx];r0,g0,b0=[int(v) for v in c[:3]]
   if tm[y,x] and not sl[y,x] and c[3] and g0>b0+10 and abs(r0-g0)<30:dstj[y,x,:3]=c[:3]
   c=refs[y,rx];r0,g0,b0=[int(v) for v in c[:3]]
   if dsts[y,x,3] and y>=50 and c[3] and r0>145 and b0>120 and abs(r0-g0)<40:dsts[y,x,:3]=c[:3]
 o[N[2]]=Image.fromarray(dstj);o[N[3]]=Image.fromarray(dsts)
 return replace_bag(o,g,angle)

def half_leg(im,side):
 ar=np.array(im);yy,xx=np.mgrid[:p.H,:p.W];mask=(xx<128) if side=='left' else (xx>=128);mask|=(yy<103);ar[~mask]=0
 return Image.fromarray(ar)
def affine_bone(im,s,e,ns,ne):
 # One rigid-ish limb rotation/length registration; same width. No silhouette-box fitting.
 sv=np.array(e)-np.array(s);tv=np.array(ne)-np.array(ns);sl=np.linalg.norm(sv);tl=np.linalg.norm(tv);u=sv/sl;v=np.array([-u[1],u[0]]);tu=tv/tl;tvv=np.array([-tu[1],tu[0]])
 A=np.outer(u,tu)*(sl/tl)+np.outer(v,tvv);b=np.array(s)-A@np.array(ns);return im.transform(im.size,Image.Transform.AFFINE,(A[0,0],A[0,1],b[0],A[1,0],A[1,1],b[1]),Image.Resampling.NEAREST)
def legmix(left,right,top):
 o=p.empty();o.alpha_composite(half_leg(left,'left'));o.alpha_composite(half_leg(right,'right'));ar=np.array(o);t=np.array(top);ar[:103]=t[:103];return Image.fromarray(ar)
orig=key(1);reach=key(2);free=key(3);wind=key(4);hit=key(5);arrest=key(6);release=key(7);gather=key(8)
# Restore original source windup's one-pixel low sole with a sole extension only.
wl=np.array(wind[N[0]]);wl[192,:]=np.where((wl[191,:,3]>0)[:,None],wl[191,:],wl[192,:]);wind[N[0]]=Image.fromarray(wl)
# Step poses use registered leg endpoints and planted support, not sliding both whole cels.
stepfront=affine_bone(half_leg(orig[N[0]],'right'),(128,102),(150,184),(128,102),(160,177))
steplegs=legmix(orig[N[0]],stepfront,orig[N[0]])
launchleft=affine_bone(half_leg(hit[N[0]],'left'),(120,102),(85,175),(121,102),(104,184))
launchlegs=legmix(launchleft,hit[N[0]],hit[N[0]])
plantlegs=legmix(arrest[N[0]],hit[N[0]],arrest[N[0]])
frontstep=affine_bone(half_leg(hit[N[0]],'right'),(134,103),(173,184),(134,103),(160,177))
frontsteplegs=legmix(arrest[N[0]],frontstep,arrest[N[0]])
rearstep=affine_bone(half_leg(arrest[N[0]],'left'),(122,102),(96,184),(123,102),(104,178))
rearsteplegs=legmix(rearstep,orig[N[0]],orig[N[0]])
frames=[];sites=[]
def add(o,ss=None):frames.append(o);sites.append(ss)
add(orig)
for obj,g,angle,carry,drop in [(reach,(148,49),-3,True,33),(free,(143,62),-13,True,22)]:
 o,ss=replace_bag(obj,g,angle,carry,drop)
 if obj is free:
  for idx,w in [(1,1),(5,3)]:p.line(o[N[idx]],[(143,44),(142,56),g],p.M,w)
 add(o,ss)
# Transfer study retained, now only sparse cloth/prop material details.
for obj,f,carry,drop,angle,g in [(release,7,True,32,-6,(157,43)),(gather,8,False,18,-6,(134,86))]:
 o,ss=replace_bag(obj,g,angle,carry,drop);arms=json.loads((R/'recipe/transfer-sites.json').read_text())['sites']['release' if f==7 else 'gather']['arms'];o=detail_arms(o,arms);add(o,ss)
o,ss=custom('counter',(116,92),20,steplegs);add(o,ss)
o,ss=replace_bag(wind,(96,94),29);add(o,ss)
o,ss=custom('launch',(122,93),29,launchlegs);add(o,ss)
o,ss=custom('transit',(155,83),-15,hit[N[0]]);add(o,ss)
o,ss=replace_bag(hit,(174,68),-50);add(o,ss)
o,ss=replace_bag(hit,(174,68),-62);add(o,ss)
o,ss=replace_bag(arrest,(160,79),-43);o[N[0]]=hit[N[0]].copy();add(o,ss)
o,ss=replace_bag(arrest,(160,79),-35);o[N[0]]=plantlegs;add(o,ss)
o,ss=custom('return',(144,84),-24,frontsteplegs);add(o,ss)
o,ss=replace_bag(gather,(134,86),-6);o[N[0]]=arrest[N[0]].copy();arms=json.loads((R/'recipe/transfer-sites.json').read_text())['sites']['gather']['arms'];add(detail_arms(o,arms),ss)
o,ss=replace_bag(release,(157,43),-6,True,32);o[N[0]]=rearsteplegs;arms=json.loads((R/'recipe/transfer-sites.json').read_text())['sites']['release']['arms'];add(detail_arms(o,arms),ss)
add(frames[2]);add(frames[1]);add(orig)
assert len(frames)==19
# Authored smear changes only prop owners in frame9; body/head/feet/hands exactly control.
smear={n:im.copy() for n,im in frames[8].items()};smear=clear_prop(smear)
for side in [-1,1]:p.line(smear[N[1]],[(155+side,83),(157+side*2,90),(159+side*7,98)],p.M,2)
p.polygon(smear[N[4]],[(153,102),(161,95),(184,88),(207,87),(216,92),(218,98),(207,107),(183,116),(163,117),(154,111)],p.D)
p.polygon(smear[N[4]],[(155,102),(163,97),(185,90),(207,89),(214,93),(216,98),(205,105),(182,114),(164,115),(156,110)],p.B)
p.polygon(smear[N[4]],[(158,110),(182,111),(204,103),(215,96),(216,98),(205,105),(182,114),(164,115)],p.M)
p.polygon(smear[N[4]],[(158,100),(161,96),(174,92),(178,94),(165,101)],p.O)
for pts in [[(154,83),(157,90),(160,100),(163,104)],[(156,83),(163,89),(175,95),(180,98)]]:
 p.line(smear[N[5]],pts,p.M,3);p.line(smear[N[5]],pts,p.L,1)
p.line(smear[N[4]],[(166,108),(186,102),(204,96)],p.S,2);p.line(smear[N[4]],[(174,111),(192,105),(209,99)],p.M)
# Persistent near seams continue several pixels into deformed fabric, far roots behind rim.
for x,y in [(163,104),(180,98)]:p.line(smear[N[5]],[(x,y),(x+3,y)],p.S)
(R/'recipe/cycle-calls').mkdir(exist_ok=True)
count=0
for f,o in enumerate(frames,1):
 for n in N:
  op=p.grid(o[n])
  if not op:continue
  op['rle']=[''.join(str(len(list(g)))+ch for ch,g in itertools.groupby(row)) for row in op.pop('rows')]
  c=dict(frame=f,layer=n,createCel=True,label=f'cycle F{f} {n}',ops=[op]);(R/'recipe/cycle-calls'/f'{count:03}.json').write_text(json.dumps(c,ensure_ascii=False,separators=(',',':')));count+=1
smcalls=[]
for n in [N[1],N[4],N[5]]:
 op=p.grid(smear[n]);op['rle']=[''.join(str(len(list(g)))+ch for ch,g in itertools.groupby(row)) for row in op.pop('rows')];smcalls.append(dict(frame=9,layer=n,createCel=True,label='single authored smear prop deformation',ops=[op]))
(R/'recipe/smear-calls.json').write_text(json.dumps(smcalls,ensure_ascii=False,separators=(',',':')))
durations=[180,100,90,80,100,90,150,50,50,100,70,100,90,100,100,100,110,100,400]
phases=['idle','reach','free-hand','shoulder-clearance','two-hand-gather','counter-step','windup','launch','smear','contact','overshoot','arrest','rear-foot-plant','front-step-gather','inward-gather','re-shoulder-lift','shoulder-support','strap-settle','idle-return']
rects=[]
for o in frames:
 prop=p.empty()
 for idx in [1,4,5]:prop.alpha_composite(o[N[idx]])
 b=prop.getbbox() or (150,45,151,46);rects.append([b[0],b[1],b[2]-b[0],b[3]-b[1]])
meta=dict(frame_size=[256,208],frame_count=19,durations_ms=durations,phases=phases,contact_frames_1based=[10],smear_frames_1based=[9],target_rect_xywh=[210,80,12,40],trail_rects_xywh=rects,root=[128,193],original_offset=[60,8],normal_prop_sites=sites,smear_sites={'G':[155,83],'FL':[152,98],'FR':[166,98],'NL':[163,104],'NR':[180,98],'M':[166,97]},revision='timing01',total_ms=sum(durations),note='control frame9 is on-model transit; authored frame9 changes only rearhandle/body/nearhandle. Other18frames are identical; no genericblur. Normal keys return to original idle exactly.')
(R/'exports/timing.json').write_text(json.dumps(meta,indent=2));(R/'recipe/cycle-manifest.json').write_text(json.dumps({'calls':count,'frames':19,'durations':durations,'total_ms':sum(durations),'source':'transfer-study02.aseprite','source_reuse':'19 frame reconstruction; authored core/arm/step transitions, source-guided keys and one drawn prop smear'},indent=2));print('cycle calls',count,'frames19 total_ms',sum(durations))
