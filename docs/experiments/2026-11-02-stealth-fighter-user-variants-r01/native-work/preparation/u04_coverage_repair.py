from PIL import Image
from pathlib import Path
import json,shutil
O=Path('/private/tmp/fighter-user-variants-r01/native-work');D=O/'variant-04';S=D/'pass01-precoverage';S.mkdir(exist_ok=True)
for p in list(D.iterdir()):
 if p.is_file() and p.suffix!='.aseprite':shutil.copy2(p,S/p.name)
source=Image.open(O/'preparation/source-grid-04.png').convert('RGBA');mask=Image.open(D/'source-spatial-mask-native.png').convert('L');raw=Image.open(D/'raw-unquantized.png').convert('RGBA');seed=Image.open(D/'raw-seed.png').convert('RGBA');data=json.loads((D/'native-draw-ops.json').read_text());pal=[tuple(bytes.fromhex(c[1:])) for c in data['palette']];patch=[]
for p in [(50,25),(36,50)]:
 color=source.getpixel(p);c=min(pal,key=lambda c:sum((a-b)**2 for a,b in zip(c,color[:3])));mask.putpixel(p,255);raw.putpixel(p,color);seed.putpixel(p,c+(255,));patch.append({'layer':'head-hair-face','x':p[0],'y':p[1],'color':'#%02x%02x%02x'%c})
p=(63,183);mask.putpixel(p,0);raw.putpixel(p,(0,0,0,0));seed.putpixel(p,(0,0,0,0));patch.append({'layer':'lowerbody-boots','x':63,'y':183,'color':None})
mask.save(D/'source-spatial-mask-native.png');raw.save(D/'raw-unquantized.png');seed.save(D/'raw-seed.png');(D/'coverage-patch.json').write_text(json.dumps({'source_supported_points':patch,'reason':'reviewed source hair restorations50,25/36,50; source background63,183 opens existing diagonal leggap to4connectivity without removing trouser64,184','reviewer':'independent Terra seed/final critic'},indent=2))
