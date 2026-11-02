from PIL import Image
from pathlib import Path
import json
K=Path('/private/tmp/stealth-fighter-idle-r01/keys');S=K.parent/'seed';data=json.load(open(K/'key-draw-ops.json'));legend=data['legend'];lookup={tuple(bytes.fromhex(c[1:]))+(255,):ch for ch,c in legend.items()}
base=Image.open(S/'lower-body-fixed.png').convert('RGBA')
pts=[(x,y) for y in range(110,153) for x in range(29,56) if base.getpixel((x,y))[3] and base.getpixel((x,y))[0]>65]
# These exact inspected warm hand-edge pixels belonged to the wrong native owner.
# Reassign visible pixels at each cleared key's current coordinates, preserving composite.
for key in ['rest','transition','apex']:
 b=Image.open(K/(key+'-lower-body-fixed.png')).convert('RGBA');arm=Image.open(K/(key+'-near-arm.png')).convert('RGBA')
 for p in pts:
  px=b.getpixel(p)
  if not arm.getpixel(p)[3]:arm.putpixel(p,px)
  b.putpixel(p,(0,0,0,0))
 for n,im in [('lower-body-fixed',b),('near-arm',arm)]:
  im.save(K/(key+'-refined-'+n+'.png'));bb=im.getbbox();x0,y0,x1,y1=bb
  data['ops'][key][n]=[{'kind':'grid','x':x0,'y':y0,'rows':[''.join(lookup.get(im.getpixel((x,y)),'.') for x in range(x0,x1)) for y in range(y0,y1)],'legend':legend}]
json.dump(data,open(K/'refined-key-draw-ops.json','w'),indent=2)
json.dump({'source_owner':'lower-body-fixed','destination_owner':'near-arm','native_points':pts,'count':len(pts),'per_key_rule':'transfer visible hand-edge pixels at current coordinates, preserve already opaque near-arm pixels; clear lower-body owner; composite unchanged','interpretation':'one-pixel soft hand-edge accommodation retained from cleared key, not a rigid-arm registration claim'},open(K/'ownership-refinement.json','w'),indent=2)
