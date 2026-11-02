from PIL import Image,ImageDraw
from pathlib import Path
import json,string
O=Path('/private/tmp/stealth-fighter-idle-r01');S=O/'seed';K=O/'keys'
data=json.load(open(S/'native-draw-ops.json'));layers=data['layers'];pal=data['palette'];chars=string.ascii_letters+string.digits
legend={chars[i]:c for i,c in enumerate(pal)};lookup={tuple(bytes.fromhex(c[1:]))+(255,):chars[i] for i,c in enumerate(pal)}
rest={n:Image.open(S/(n+'.png')).convert('RGBA') for n in layers}
# Material colors sampled from retained source-derived palette; no added colors.
indigo='#282f3f'; indigo_lit='#293040'; dark='#18181a'; edge='#191a1c'; armor='#48423b'
def poly(im,pts,c):ImageDraw.Draw(im).polygon(pts,fill=c)
def shifted(im,dy):o=Image.new('RGBA',im.size);o.alpha_composite(im,(0,dy));return o
transition={n:im.copy() for n,im in rest.items()}
# Draw shallow expanded front ribcage silhouette, retaining interior folds and waist.
t=transition['upper-torso']
# Front contour is explicitly redrawn from registered rest sites: rest front x76,
# transition/apex front x77 maximum; no copied horizontal row offsets.
ImageDraw.Draw(t).rectangle((74,67,82,79),fill=(0,0,0,0))
poly(t,[(74,67),(75,68),(76,71),(76,75),(75,78),(74,79)],indigo)
poly(t,[(75,67),(76,69),(77,72),(77,75),(76,78),(75,79)],edge)
apex={n:im.copy() for n,im in rest.items()}
apex['head-hair-neck']=shifted(rest['head-hair-neck'],-1)
apex['near-arm']=shifted(rest['near-arm'],-1)
a=apex['upper-torso'];d=ImageDraw.Draw(a)
# Rigid upper armor/collar lifts with supported shoulder/head chain.
# Source interior clusters below it are retained; changing contour is drawn below.
d.rectangle((0,0,127,63),fill=(0,0,0,0));top=rest['upper-torso'].crop((0,0,128,64));a.alpha_composite(top,(0,-1))
# Rebuild the supported chest contour from the same source landmark route.
d.rectangle((73,60,82,86),fill=(0,0,0,0))
poly(a,[(72,60),(73,60),(74,62),(75,66),(76,71),(76,76),(75,80),(75,84),(74,86),(72,86)],indigo)
poly(a,[(73,60),(74,61),(75,63),(76,67),(77,71),(77,76),(76,80),(76,84),(75,86),(74,86),(75,82),(75,78),(76,74),(75,69),(74,65),(73,63)],edge)
# Shoulder/chest junction backing follows armor underside rather than an old duplicate edge.
poly(a,[(52,62),(56,62),(60,62),(61,63),(60,64),(56,64),(53,63)],dark)
# Source lower torso at/below88 remains exact and attached to fixed waist.
for y in range(88,264):
 for x in range(128): a.putpixel((x,y),rest['upper-torso'].getpixel((x,y)))
# Redraw collar overlap under moved neck, with the same dark/indigo material roles.
poly(a,[(60,43),(63,43),(65,44),(66,46),(66,49),(64,50),(63,48),(62,46)],dark)
poly(a,[(63,45),(65,45),(65,48),(64,49)],indigo)
# Export grids only; these are reproducible drawing instructions, never a native file writer.
ops={}
for key,parts in [('rest',rest),('transition',transition),('apex',apex)]:
 comp=Image.new('RGBA',(128,264));ops[key]={}
 for n in layers:
  im=parts[n];im.save(K/(key+'-'+n+'.png'));comp.alpha_composite(im)
  b=im.getbbox();x0,y0,x1,y1=b;rows=[''.join(lookup.get(im.getpixel((x,y)),'.') for x in range(x0,x1)) for y in range(y0,y1)]
  ops[key][n]=[{'kind':'grid','x':x0,'y':y0,'rows':rows,'legend':legend}]
 comp.save(K/(key+'-drawing-plan.png'))
json.dump({'layers':layers,'ops':ops,'legend':legend,'method':'rigid head/near-arm reuse, hand-authored chest/shoulder/collar contour and planes; waist held'},open(K/'key-draw-ops.json','w'),indent=2)
