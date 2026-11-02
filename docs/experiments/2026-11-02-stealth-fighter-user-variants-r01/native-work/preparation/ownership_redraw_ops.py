from PIL import Image
from pathlib import Path
import json,shutil,importlib.util
O=Path('/private/tmp/fighter-user-variants-r01/native-work');P=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools/check_native_pilot.py');spec=importlib.util.spec_from_file_location('n',P);n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
for i in ['01','03','04','05']:
 D=O/f'variant-{i}';prior=D/'pass02-preownership';prior.mkdir(exist_ok=True);old=n.read(D/'static.aseprite')
 for j,l in enumerate(old['layers']):old['cels'][(0,j)]['image'].save(prior/(l['name']+'.png'))
 for name in ['static.png','reopened.png','edit-proof.png','edit-proof-reopened.png','edit-proof-ops.json','edit-proof-mask.png','native-owner-contact-3x.png']:
  p=D/name
  if p.exists():shutil.copy2(p,prior/name)
 data=json.loads((D/'native-draw-ops.json').read_text());out={}
 for layer in ['head-hair-face','torso-cloth-armor','far-hand','near-arm-guard-hand']:
  original=data['ops'][layer][0];legend=original['legend'];lookup={tuple(bytes.fromhex(c[1:]))+(255,):ch for ch,c in legend.items()};im=Image.open(D/(layer+'.png')).convert('RGBA');out[layer]=[{'kind':'grid','x':0,'y':0,'rows':[''.join(lookup.get(im.getpixel((x,y)),'.') for x in range(128)) for y in range(264)],'legend':legend}]
 (D/'ownership-redraw-ops.json').write_text(json.dumps(out))
