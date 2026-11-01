"""Full-sheet connected-component masks at frozen family scales. No native writes."""
from PIL import Image,ImageDraw
from pathlib import Path
from functools import lru_cache
import json,sys
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
CANVAS=(320,192)
PAL=tuple(tuple(int(v.lstrip('#')[i:i+2],16) for i in (0,2,4)) for v in json.loads((ROOT/'artist/seed-palette.json').read_text()) if len(v.lstrip('#'))==6)
@lru_cache(maxsize=200000)
def nearest(c):return min(PAL,key=lambda p:2*(c[0]-p[0])**2+4*(c[1]-p[1])**2+3*(c[2]-p[2])**2)
def components(im):
 w,h=im.size;a=im.getchannel('A');p=a.load();seen=set();cs=[]
 for y in range(h):
  for x in range(w):
   if p[x,y]<128 or (x,y) in seen:continue
   q=[(x,y)];seen.add((x,y))
   for u,v in q:
    for dx,dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)]:
     t=(u+dx,v+dy)
     if 0<=t[0]<w and 0<=t[1]<h and t not in seen and p[t[0],t[1]]>=128:seen.add(t);q.append(t)
   if len(q)>1000:
    bbox=(min(z[0] for z in q),min(z[1] for z in q),max(z[0] for z in q)+1,max(z[1] for z in q)+1)
    mask=Image.new('L',im.size);mask.putdata([0]*(w*h));m=mask.load()
    for u,v in q:m[u,v]=255
    cs.append((bbox,mask,len(q)))
 return cs
provenance=[];poses=[]
for family,scale,columns,rows in [('six',.4333,3,2),('additional',.264,3,1)]:
 path=ROOT/'inputs'/('six-keys.png' if family=='six' else 'additional-keys.png');im=Image.open(path).convert('RGBA');cs=components(im)
 cs.sort(key=lambda c:(0 if c[0][1]<300 else 1,c[0][0]) if family=='six' else (0,c[0][0]))
 for i,(box,mask,count) in enumerate(cs):
  # Keep original sheet-grid registration; wider masks recover tote beyond cell edges.
  col=i%columns;row=i//columns;origin=(round(col*im.width/columns),round(row*im.height/rows))
  x0,y0,x1,y1=box;selected=im.crop(box);selected.putalpha(mask.crop(box))
  selected=selected.resize((round((x1-x0)*scale),round((y1-y0)*scale)),Image.Resampling.NEAREST)
  q=selected.load()
  for y in range(selected.height):
   for x in range(selected.width):
    r,g,b,a=q[x,y];q[x,y]=(*nearest((r,g,b)),255) if a else (0,0,0,0)
  off=(round((x0-origin[0])*scale),round((y0-origin[1])*scale))
  if family=='additional':off=(off[0]+50,off[1]-2)
  # Windup stance/body registration: shared scale, authored root translation only.
  if family=='additional' and i==0:off=(off[0]-24,off[1])
  canvas=Image.new('RGBA',CANVAS);canvas.alpha_composite(selected,off)
  name=f'{family}-{i+1}';canvas.save(OUT/'preparation'/f'{name}.png');poses.append((name,canvas))
  provenance.append(dict(name=name,source=str(path.relative_to(ROOT)),source_bbox_xyxy=list(box),source_component_pixels=count,grid_origin_xy=list(origin),family_scale=scale,target_offset_xy=list(off),canvas=list(CANVAS),policy='largest pose-connected component, binary128 alpha, weighted RGB projection to existing palette; no per-pose fitting'))
(OUT/'preparation/provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
sheet=Image.new('RGBA',(320*3,216*3),(65,59,73,255));d=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(poses):x=i%3*320;y=i//3*216;sheet.alpha_composite(im,(x,y+24));d.text((x+5,y+5),name,fill='white')
sheet.convert('RGB').save(OUT/'review/raw-component-poses.png')
print(json.dumps(provenance))
