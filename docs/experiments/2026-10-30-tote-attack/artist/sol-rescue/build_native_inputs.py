"""Source part masks and literal grid inputs for dedicated-MCP native assembly."""
from PIL import Image,ImageDraw
from pathlib import Path
import json
R=Path(__file__).resolve().parent;ROOT=R.parents[1];C=(320,192)
DUR=[60,110,140,210,70,60,90,110,140,170,140,160,220]
PH=['ready idle','pickup','shared grip','counter-windup','acceleration','committed contact','follow-through','arrest and redirect','controlled recovery','tote settle','re-shoulder','release and settle','ready idle return']
def load(n):return Image.open(R/'preparation'/f'{n}.png').convert('RGBA')
def shifted(im,x,y):
 a=Image.new('RGBA',C);a.alpha_composite(im,(x,y));return a
def maskpoly(points):
 m=Image.new('L',C);ImageDraw.Draw(m).polygon(points,fill=255);return m
def take(im,m):
 a=im.copy();a.putalpha(Image.composite(im.getchannel('A'),Image.new('L',C),m));return a
def remove(im,m):
 a=im.copy();a.putalpha(Image.composite(Image.new('L',C),im.getchannel('A'),m));return a
neutral=Image.new('RGBA',C);neutral.alpha_composite(Image.open(ROOT/'inputs/neutral.png').convert('RGBA'),(64,0))
ims=[neutral,load('six-2'),shifted(load('six-3'),20,-1),load('additional-1'),shifted(load('six-3'),14,-4),load('six-4'),load('six-5'),shifted(load('six-3'),20,-3),load('additional-2'),load('additional-2'),load('additional-3'),shifted(load('six-6'),23,0),neutral]
# All source-specific tote/handle masks are spatial, never global color deletion.
polys=[[(141,41),(151,41),(169,79),(172,130),(144,130),(143,78)],[(144,48),(153,48),(184,88),(190,139),(154,140),(145,87)],[(162,88),(177,88),(239,88),(241,140),(179,140),(162,104)],[(48,86),(112,76),(118,91),(82,142),(47,137)],[(156,85),(171,85),(233,85),(235,137),(173,137),(156,101)],[(205,52),(276,43),(280,106),(207,103)],[(194,53),(278,44),(280,109),(195,106)],[(162,86),(177,86),(239,86),(241,138),(179,138),(162,102)],[(172,85),(184,83),(222,107),(223,153),(181,153),(171,102)],[(172,85),(184,83),(222,107),(223,153),(181,153),(171,102)],[(166,44),(176,44),(201,95),(199,132),(167,131),(165,96)],[(161,40),(172,42),(195,92),(192,129),(162,128),(157,85)],[(141,41),(151,41),(169,79),(172,130),(144,130),(143,78)]]
frames=[];calls=[];parts_names=['01-leg-base-and-shoes','02-jacket-shirt-and-sleeves','03-head-neck-collar','04-tote-and-handles']
for i,im in enumerate(ims):
 bagmask=maskpoly(polys[i]);bag=take(im,bagmask);body=remove(im,bagmask)
 # F8 is the braking key: lunge leg base persists while shoulders/arms fold back.
 if i==7:
  lunge=load('six-5');bodypx=body.load();lp=lunge.load()
  # Lower-body replacement is source-supported anatomy, not per-row displacement.
  legmask=maskpoly([(122,87),(145,85),(163,104),(214,184),(56,184),(94,116)])
  body=remove(body,legmask);body.alpha_composite(take(lunge,legmask))
 # Keep original hair/face/neck together through native decomposition.
 headmask=maskpoly([(0,0),(319,0),(319,49 if i not in [5,6] else 42),(0,49 if i not in [5,6] else 42)])
 head=take(body,headmask);body=remove(body,headmask)
 legmask=maskpoly([(0,105),(319,105),(319,191),(0,191)])
 legs=take(body,legmask);torso=remove(body,legmask)
 parts=[legs,torso,head,bag];flat=Image.new('RGBA',C)
 for part in parts:flat.alpha_composite(part)
 flat.save(R/'preparation'/f'frame-{i+1:02}-base.png');frames.append(flat)
 for name,part in zip(parts_names,parts):
  b=part.getbbox()
  if not b:continue
  part.save(R/'preparation'/f'frame-{i+1:02}-{name}.png')
  crop=part.crop(b);colors=list(dict.fromkeys(px for px in crop.getdata() if px[3]));legend={chr(0x100+k):'#%02x%02x%02x'%px[:3] for k,px in enumerate(colors)};rev={v:k for k,v in legend.items()}
  rows=[''.join('.' if crop.getpixel((x,y))[3]==0 else rev['#%02x%02x%02x'%crop.getpixel((x,y))[:3]] for x in range(crop.width)) for y in range(crop.height)]
  calls.append(dict(frame=i+1,layer=name,createCel=True,label=f'source-mask {i+1:02} {name}',ops=[dict(kind='grid',x=b[0],y=b[1],rows=rows,legend=legend,transparent='erase')]))
(R/'operations/native-assembly.json').write_text(json.dumps(calls))
(R/'operations/phase-data.json').write_text(json.dumps(dict(canvas=list(C),durations_ms=DUR,phases=PH,part_names=parts_names),indent=2))
sheet=Image.new('RGBA',(960,216*5),(64,59,73,255));d=ImageDraw.Draw(sheet)
for i,im in enumerate(frames):x=i%3*320;y=i//3*216;sheet.alpha_composite(im,(x,y+24));d.text((x+5,y+5),f'F{i+1} {PH[i]}',fill='white')
sheet.convert('RGB').save(R/'review/pre-native-sequence.png')
print('prepared',len(calls),'native grid batches')
