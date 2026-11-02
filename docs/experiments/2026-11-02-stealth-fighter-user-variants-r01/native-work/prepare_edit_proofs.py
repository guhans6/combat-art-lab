from PIL import Image,ImageDraw
from pathlib import Path
import json,hashlib
O=Path('/private/tmp/fighter-user-variants-r01/native-work')
for i in ['01','03','04','05']:
 D=O/f'variant-{i}';data=json.loads((D/'native-draw-ops.json').read_text());pal=data['palette'];metal=[]
 for c in pal:
  r,g,b=bytes.fromhex(c[1:])
  if r>=g>=b and r-b<36 and r>55:metal.append((r+g+b,c))
 color=max(metal)[1];im=Image.open(D/'near-arm-guard-hand.png').convert('RGBA');mask=Image.new('L',im.size);ops=[];pixels=[]
 for y in range(111,123):
  x=40+(y-111)//7
  for xx in [x,x+1]:
   p=im.getpixel((xx,y))
   if p[3] and '#%02x%02x%02x'%p[:3]!=color:
    ops.append({'kind':'grid','x':xx,'y':y,'rows':['a'],'legend':{'a':color}});mask.putpixel((xx,y),255);pixels.append([xx,y])
 mask.save(D/'edit-proof-mask.png');(D/'edit-proof-ops.json').write_text(json.dumps({'layer':'near-arm-guard-hand','frame':1,'ops':ops,'palette_color':color,'purpose':'duplicate-only widening of the existing bracer ridge highlight; show target metal panel can be revised without hair/body/sword changes','changed_points':pixels,'source_native_sha256':hashlib.sha256((D/'static.aseprite').read_bytes()).hexdigest()},indent=2));print(i,color,len(ops))
