"""Literal dedicated-MCP correction inputs; no Aseprite files written here."""
from PIL import Image
from pathlib import Path
import json
R=Path(__file__).resolve().parent;C=(320,192)
def grid(im):
 b=im.getbbox();crop=im.crop(b);cs=list(dict.fromkeys(p for p in crop.getdata() if p[3]));legend={chr(0x100+i):'#%02x%02x%02x'%p[:3] for i,p in enumerate(cs)};rev={v:k for k,v in legend.items()}
 return dict(kind='grid',x=b[0],y=b[1],legend=legend,transparent='erase',rows=[''.join('.' if crop.getpixel((x,y))[3]==0 else rev['#%02x%02x%02x'%crop.getpixel((x,y))[:3]] for x in range(crop.width)) for y in range(crop.height)])
def poly(points,outline,fill=None):return dict(kind='polyline',points=[dict(x=x,y=y) for x,y in points],closed=True,color=outline,fill=fill or outline)
def line(points,color,thick=1):return [dict(kind='line',color=color,thickness=thick,**{'from':dict(x=a[0],y=a[1]),'to':dict(x=b[0],y=b[1])}) for a,b in zip(points,points[1:])]
ops=[]
# Tote frames: derive actual source pixels, preserving folds/material volume.
wind=Image.open(R/'preparation/frame-04-04-tote-and-handles.png').convert('RGBA')
rec=Image.open(R/'preparation/frame-09-04-tote-and-handles.png').convert('RGBA')
for f in [8,9,10]:
 out=Image.new('RGBA',C)
 if f==8:
  for y in range(192):
   for x in range(320):
    p=wind.getpixel((x,y));u=277-x;v=y+2
    if p[3] and 0<=u<320 and v<192:out.putpixel((u,v),p)
 else:out.alpha_composite(rec,(-12,3) if f==9 else (-25,-5))
 out.save(R/'preparation'/f'recovery-bag-{f}.png')
 ops.append(dict(frame=f,layer='04-tote-and-handles',createCel=True,label=f'F{f} full source tote load arc',ops=[dict(kind='clear'),grid(out)]))
# F8: keep the elbow flexion of the source, draw the shared handle clasp and tension.
# Both wrists now terminate on one handle bundle; lower forearm has a clear underside.
a=[poly([(145,85),(153,86),(161,90),(168,87),(171,90),(167,96),(159,96),(151,91),(144,89)],'#78371c','#fda977'),poly([(146,86),(154,87),(161,91),(165,90),(164,93),(158,93),(151,90),(146,89)],'#fcaf80'),poly([(158,85),(163,83),(167,85),(168,89),(165,93),(161,91)],'#90472c','#fda977')]
a+=line([(163,85),(166,87),(165,91)],'#e48558')+line([(160,93),(164,94),(168,91)],'#c8683f')
ops.append(dict(frame=8,layer='05-loaded-grip-drawing',createCel=True,label='F8 authored bent-elbow shared clasp',ops=a))
# F9/F10: remove the old outstretched arm silhouettes on their actual owner.
for f in [9,10]:
 # Pixel erasure is spatial and limited to forearms/old hands, retaining upper sleeves.
 rows=[];legend={'.':None}
 # Native clear op is used, then underlying visible waist/side-coat is reconstructed.
 clear=[dict(kind='clear',region=dict(x=151,y=73,width=36,height=18))]
 ops.append(dict(frame=f,layer='02-jacket-shirt-and-sleeves',createCel=True,label=f'F{f} remove weak source forearms',ops=clear))
 # Structural backing at waist and side coat, with material-colored contours.
 a=[poly([(151,82),(164,84),(169,93),(162,102),(151,101)],'#354f80','#435e8c'),poly([(164,81),(175,80),(177,89),(175,98),(171,103),(168,99)],'#393628','#4b4732'),poly([(166,82),(173,82),(174,91),(171,98),(169,96)],'#524c34')]
 if f==9:
  # Far forearm folds inward from the retained cuff rather than hanging vertically.
  a+=[poly([(176,70),(183,73),(182,78),(172,86),(165,85),(164,81),(173,77)],'#78371c','#ea9368'),poly([(177,72),(181,74),(179,77),(170,83),(167,82),(173,79)],'#fcaf80'),poly([(150,72),(155,73),(160,78),(165,82),(170,83),(173,87),(169,91),(164,91),(157,86),(149,80)],'#78371c','#fda977'),poly([(151,74),(155,75),(161,81),(167,84),(169,86),(166,88),(160,84),(151,78)],'#fcaf80'),poly([(165,81),(169,79),(174,82),(175,86),(171,89),(167,88)],'#90472c','#fda977')]
  a+=line([(168,81),(172,83),(172,85)],'#e48558')+line([(165,87),(168,89),(171,87)],'#c8683f')
 else:
  a+=[poly([(176,70),(182,73),(179,78),(165,82),(156,82),(154,78),(162,75),(172,74)],'#78371c','#ea9368'),poly([(176,72),(179,74),(176,77),(162,79),(158,78),(164,77)],'#fcaf80'),poly([(150,72),(155,72),(158,75),(160,78),(159,83),(155,86),(151,85),(147,79)],'#78371c','#fda977'),poly([(151,74),(154,74),(157,77),(157,81),(154,83),(150,79)],'#fcaf80'),poly([(155,75),(159,74),(164,76),(164,80),(160,84),(157,82)],'#90472c','#fda977')]
  a+=line([(158,76),(162,77),(162,79)],'#e48558')+line([(156,82),(160,83),(162,81)],'#c8683f')
 # Rearticulated cuff/fold emphasizes elbow compression, within unchanged palette.
 a+=[poly([(145,70),(151,70),(155,73),(152,80),(149,81),(145,78)],'#393628','#524c34'),poly([(146,71),(150,71),(152,74),(150,77),(147,77)],'#665e3a')]
 ops.append(dict(frame=f,layer='05-loaded-grip-drawing',createCel=True,label=f'F{f} authored load absorption and hand bundle',ops=a))
(R/'operations/recovery-correction.json').write_text(json.dumps(ops,indent=2))
print('correction batches',len(ops))
