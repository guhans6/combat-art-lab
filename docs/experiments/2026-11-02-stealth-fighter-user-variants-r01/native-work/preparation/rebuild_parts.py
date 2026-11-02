from PIL import Image,ImageDraw
from pathlib import Path
import json,string
O=Path('/private/tmp/fighter-user-variants-r01/native-work')
for i in ['01','03','04','05']:
 delta_a=Image.open(O/'variant-03/raw-seed.png').convert('RGBA');delta_b=Image.open(O/'variant-05/raw-seed.png').convert('RGBA')
 D=O/f'variant-{i}';r=json.loads((D/'recipe.json').read_text());full=Image.open(D/'raw-unquantized.png').convert('RGBA');seed=Image.open(D/'raw-seed.png').convert('RGBA')
 # Ownership follows visible surfaces only; no hidden anatomy/rig claim.
 parts={n:Image.new('RGBA',seed.size) for n in ['lowerbody-cloth-boots','torso-cloth-armor','waist-wrap-sword','far-hand','near-arm-guard-hand','head-hair-face']}
 for y in range(264):
  for x in range(128):
   p=seed.getpixel((x,y))
   if not p[3]:continue
   # Source-guided head/hair underside; broad horizontal head split crossed cap.
   edge=[(0,57),(30,57),(37,57),(40,54),(42,51),(45,49),(48,47),(51,46),(54,46),(57,46),(60,47),(64,48),(66,46),(128,46)]
   limit=next((round(ay+(by-ay)*(x-ax)/(bx-ax)) for (ax,ay),(bx,by) in zip(edge,edge[1:]) if ax<=x<bx),46)
   delta=False
   if i in ['03','05']:
    delta=delta_a.getpixel((x,y))!=delta_b.getpixel((x,y))
   if delta:name='torso-cloth-armor'
   elif y<limit:name='head-hair-face'
   elif y>=146:name='lowerbody-cloth-boots'
   elif x>=83 and y>=122 and full.getpixel((x,y))[0]>65 and full.getpixel((x,y))[0]-full.getpixel((x,y))[2]>25:name='far-hand'
   elif 94<=y<=119 and x>=49:name='waist-wrap-sword'
   elif x>=84 and 94<=y<=122:name='waist-wrap-sword'
   elif (y>=76 and x<(52 if y<128 else 57)) or (y>=59 and x<49):name='near-arm-guard-hand'
   else:name='torso-cloth-armor'
   parts[name].putpixel((x,y),p)
 chars=string.ascii_letters+string.digits+'!#'; unique=sorted(set(seed.getdata())-{(0,0,0,0)});legend={chars[n]:'#%02x%02x%02x'%p[:3] for n,p in enumerate(unique)};lookup={p:chars[n] for n,p in enumerate(unique)};ops={}
 for n,im in parts.items():
  im.save(D/f'{n}.png');b=im.getbbox(); x0,y0,x1,y1=b;ops[n]=[{'kind':'grid','x':x0,'y':y0,'rows':[''.join(lookup.get(im.getpixel((x,y)),'.') for x in range(x0,x1)) for y in range(y0,y1)],'legend':legend}]
 r.update({'alpha_policy':'reviewed native spatial polygon only; binary; no color key; explicit hair gaps','resampling':'NEAREST once; source-aligned native grid','palette_policy':'64 source-derived actual-RGB weighted medoids, no dither; 03/05 shared palette','palette':list(legend.values()),'part_ownership':'visible pixels only; source-guided head/hair underside; 03/05 known shoulder delta all torso; far-hand source skin inside spatialzone; lowerbody includes hanging cloth; disjoint owners, no hidden surfaces or motion claim','display_height':152,'display_scale':152/240,'pass_budget':'one conversion plus one named cleanup if needed','body_bounds':seed.getbbox()})
 (D/'recipe.json').write_text(json.dumps(r,indent=2));(D/'native-draw-ops.json').write_text(json.dumps({'layers':list(parts),'palette':list(legend.values()),'ops':ops},indent=2))
 # Original masked transfer, seed / bright-light mattes at true 152 body equivalence plus 3x native.
 sheet=Image.new('RGBA',(700,850),(61,63,68,255));d=ImageDraw.Draw(sheet);d.text((8,8),f'USER {i}: source / 64-color seed / light / dark; body 152px',fill='white')
 for k,(img,bg) in enumerate([(full,(61,63,68,255)),(seed,(61,63,68,255)),(seed,(221,218,210,255)),(seed,(15,19,25,255))]):
  panel=Image.new('RGBA',(150,190),bg);disp=img.resize((81,167),Image.Resampling.NEAREST);panel.alpha_composite(disp,(35,8));sheet.alpha_composite(panel,(12+k*170,32))
 for k,(img,bg) in enumerate([(full,(221,218,210,255)),(seed,(221,218,210,255)),(seed,(15,19,25,255))]):
  panel=Image.new('RGBA',(200,570),bg);pic=img.resize((256,528),Image.Resampling.NEAREST);panel.alpha_composite(pic,(-28,15));sheet.alpha_composite(panel,(12+k*225,245))
 sheet.convert('RGB').save(D/'review-seed.png')
 print(i,seed.getbbox(),len(unique))
