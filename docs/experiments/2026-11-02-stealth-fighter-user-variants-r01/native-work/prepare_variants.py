from PIL import Image,ImageDraw,ImageEnhance
from pathlib import Path
import json,string,hashlib
O=Path('/private/tmp/fighter-user-variants-r01/native-work'); P=O/'preparation'; I=O.parent/'inputs'
recipes={'01':{'crop':[350,186,725,1448]},'03':{'crop':[20,14,288,989]},'04':{'crop':[360,102,710,1385]},'05':{'crop':[20,14,288,989]}}
# Authored spatial outlines on the fixed native grid. Color never selects alpha.
polys={
'01':[(58,13),(68,13),(72,15),(76,18),(78,18),(79,20),(80,20),(80,25),(79,26),(78,23),(77,22),(76,24),(75,25),(75,28),(76,29),(75,31),(76,32),(76,34),(74,34),(74,36),(73,37),(73,40),(71,41),(70,39),(68,40),(67,39),(66,41),(65,43),(66,47),(68,51),(70,52),(72,55),(75,58),(77,61),(79,66),(80,71),(81,77),(80,84),(80,88),(82,94),(81,98),(83,102),(84,106),(85,110),(87,109),(89,103),(90,99),(89,98),(89,96),(91,95),(93,96),(94,97),(92,99),(91,99),(89,106),(88,109),(87,113),(89,113),(89,115),(87,117),(85,117),(84,119),(85,123),(86,126),(86,128),(87,130),(88,133),(89,135),(89,137),(90,138),(89,143),(88,144),(87,143),(88,151),(90,162),(91,167),(88,165),(86,164),(85,171),(84,178),(82,184),(82,193),(81,198),(81,206),(81,212),(81,218),(82,225),(81,228),(83,231),(82,233),(84,238),(85,240),(87,242),(90,244),(94,246),(98,247),(98,251),(66,252),(66,243),(66,238),(67,235),(65,232),(65,228),(63,221),(62,211),(62,205),(63,201),(63,197),(64,193),(61,198),(59,203),(58,209),(56,214),(54,221),(51,227),(49,232),(48,238),(50,241),(53,243),(55,245),(59,246),(64,248),(64,252),(30,252),(30,244),(31,239),(30,236),(31,232),(30,229),(30,226),(32,224),(31,220),(31,213),(30,210),(30,200),(32,196),(34,193),(36,189),(36,185),(35,181),(36,178),(39,174),(41,169),(41,164),(42,158),(41,155),(42,149),(41,146),(40,145),(40,141),(39,138),(39,133),(38,130),(38,125),(36,120),(35,117),(34,111),(33,108),(33,105),(34,102),(33,100),(34,97),(33,95),(31,94),(30,91),(30,87),(31,86),(30,83),(31,81),(30,80),(32,77),(32,76),(31,75),(31,73),(33,70),(33,66),(34,62),(35,59),(34,57),(32,57),(31,56),(31,55),(34,55),(35,52),(35,49),(37,46),(39,45),(41,42),(40,40),(40,38),(42,36),(44,36),(44,33),(45,31),(46,30),(48,30),(49,28),(51,27),(51,25),(50,23),(48,23),(47,22),(45,23),(44,22),(44,20),(45,18),(47,17),(49,17),(50,19),(53,19),(54,17),(56,15)],
'03':[(59,13),(67,13),(70,14),(75,17),(77,18),(79,20),(80,23),(79,27),(78,25),(77,24),(76,26),(76,28),(77,30),(76,32),(77,33),(77,34),(75,35),(75,37),(74,38),(74,40),(71,41),(69,40),(66,39),(65,41),(64,43),(65,47),(67,50),(68,52),(70,54),(72,56),(74,59),(76,63),(78,68),(79,73),(79,81),(78,87),(79,90),(80,93),(79,96),(81,99),(81,102),(83,106),(85,109),(86,106),(88,101),(89,99),(89,97),(90,96),(93,97),(94,98),(94,100),(92,101),(91,101),(89,108),(88,112),(86,114),(87,115),(88,115),(88,117),(85,119),(84,119),(85,123),(85,128),(86,130),(86,133),(87,135),(88,137),(88,140),(89,142),(88,145),(87,146),(87,150),(88,156),(89,164),(90,170),(89,170),(87,167),(85,164),(85,170),(83,177),(82,182),(81,184),(82,188),(82,195),(81,198),(81,202),(82,207),(82,214),(83,218),(82,223),(83,226),(82,229),(83,234),(84,238),(86,241),(90,244),(93,245),(96,246),(96,249),(95,251),(66,252),(65,249),(66,243),(66,240),(65,236),(66,231),(64,227),(64,223),(63,219),(64,216),(63,212),(63,207),(62,205),(62,200),(61,198),(61,193),(62,188),(64,185),(64,181),(61,184),(59,189),(58,193),(56,197),(55,203),(54,207),(52,212),(51,216),(49,220),(48,224),(48,227),(48,230),(47,234),(47,237),(48,240),(51,242),(53,244),(56,246),(60,247),(61,250),(59,252),(32,252),(31,251),(32,245),(32,241),(33,238),(33,235),(32,232),(33,229),(32,226),(31,224),(32,218),(33,214),(33,210),(34,205),(33,202),(33,197),(35,193),(36,189),(36,184),(39,181),(39,179),(38,177),(39,174),(39,171),(42,167),(43,163),(44,158),(44,154),(44,151),(43,149),(43,146),(42,145),(41,141),(39,139),(38,135),(38,130),(37,127),(36,123),(36,120),(35,117),(34,114),(34,111),(35,108),(35,105),(34,102),(35,100),(34,97),(34,95),(32,94),(31,92),(31,89),(30,87),(31,85),(31,83),(32,81),(31,79),(32,77),(33,74),(32,73),(32,72),(34,70),(34,67),(34,63),(35,60),(36,58),(35,56),(33,57),(32,56),(33,54),(34,52),(34,50),(35,47),(37,46),(38,44),(37,43),(35,44),(34,43),(36,41),(39,40),(41,38),(42,35),(43,34),(44,31),(46,29),(49,27),(51,25),(51,24),(49,22),(47,23),(45,22),(44,21),(44,19),(46,17),(48,16),(50,17),(51,19),(53,19),(54,17),(56,15)],
'04':[(58,13),(65,13),(70,14),(74,17),(77,19),(79,20),(80,23),(80,26),(78,25),(77,23),(76,25),(76,28),(75,29),(76,31),(75,33),(76,34),(76,35),(74,35),(74,38),(73,40),(70,40),(67,38),(66,40),(65,41),(65,44),(66,47),(68,50),(69,53),(71,55),(74,59),(76,63),(78,68),(79,73),(79,82),(79,86),(80,89),(80,94),(79,96),(80,99),(81,102),(81,105),(84,109),(85,110),(86,106),(88,102),(89,100),(88,98),(89,97),(92,96),(94,98),(94,100),(92,101),(91,101),(90,105),(88,111),(87,113),(87,115),(88,115),(88,117),(85,118),(84,120),(85,125),(85,128),(86,131),(87,134),(87,136),(88,137),(89,139),(88,143),(87,144),(87,150),(89,161),(89,169),(87,168),(84,165),(84,171),(82,178),(81,184),(81,189),(80,193),(80,198),(80,204),(81,210),(81,217),(81,221),(82,225),(81,228),(82,232),(81,235),(83,239),(84,241),(87,243),(89,245),(94,247),(97,248),(97,252),(65,252),(65,246),(65,240),(66,237),(65,233),(64,229),(64,225),(63,221),(62,216),(62,210),(62,205),(63,200),(63,195),(64,190),(64,185),(65,181),(64,178),(63,182),(61,187),(59,193),(57,197),(55,202),(53,207),(51,214),(49,219),(48,224),(47,228),(47,233),(46,237),(47,240),(49,242),(52,245),(56,247),(60,249),(60,252),(32,252),(30,251),(30,247),(31,244),(31,240),(32,237),(31,234),(32,231),(32,227),(30,226),(30,223),(32,220),(33,216),(33,211),(32,207),(32,202),(32,198),(33,194),(35,191),(37,188),(38,185),(37,182),(38,179),(40,177),(41,173),(41,168),(43,163),(43,159),(44,155),(44,151),(43,148),(42,146),(41,143),(39,141),(38,138),(38,134),(37,131),(36,126),(35,122),(35,119),(34,115),(33,111),(33,108),(34,106),(35,103),(34,100),(34,96),(32,94),(32,91),(31,88),(31,86),(32,83),(32,80),(33,78),(34,76),(32,75),(32,73),(34,71),(35,68),(35,64),(36,61),(36,59),(35,58),(35,55),(35,53),(37,50),(36,49),(35,50),(34,49),(33,48),(33,46),(36,47),(38,44),(39,42),(40,39),(41,36),(43,33),(45,32),(45,30),(47,29),(49,27),(51,25),(51,24),(49,25),(47,24),(45,24),(44,22),(44,19),(45,17),(46,16),(48,16),(50,18),(50,19),(53,19),(54,16),(56,15)]}
polys['05']=polys['03']
raw={};masks={}
for i,r in recipes.items():
 im=Image.open(I/f'user-{i}.png').convert('RGBA'); b=r['crop'];w=round((b[2]-b[0])*240/(b[3]-b[1]));off=((128-w)//2,13);small=im.crop(b).resize((w,240),Image.Resampling.NEAREST);full=Image.new('RGBA',(128,264));full.alpha_composite(small,off)
 mask=Image.new('L',full.size);d=ImageDraw.Draw(mask);d.polygon(polys[i],fill=255)
 # Explicit open negative spaces behind loose hair. Kept compact; no material-color removal.
 gaps={'01':[[(41,37),(44,35),(44,38),(42,40),(41,40)],[(47,30),(49,29),(48,32),(47,33)]], '03':[[(39,41),(42,38),(43,36),(44,37),(43,40),(40,43)],[(37,47),(39,44),(40,44),(39,47)]], '04':[[(39,42),(41,39),(42,37),(42,40),(40,43)]]}
 for p in gaps.get(i,gaps.get('03',[])): d.polygon(p,fill=0)
 full.putalpha(mask);full.putdata([p if p[3] else (0,0,0,0) for p in full.getdata()]);raw[i]=full;masks[i]=mask
 r.update({'canvas':[128,264],'body_height':240,'baseline_exclusive':253,'source_size':im.size,'resize':[w,240],'offset':off,'silhouette_native':polys[i],'hair_negative_spaces':gaps.get(i,gaps.get('03',[])),'source_sha256':hashlib.sha256((I/f'user-{i}.png').read_bytes()).hexdigest()})
# Shared U03/U05 quantization makes all source-identical regions exactly identical.
pals={}
for group in [['01'],['03','05'],['04']]:
 px=[p[:3] for i in group for p in raw[i].getdata() if p[3]];sw=Image.new('RGB',(len(px),1));sw.putdata(px);q=sw.quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE);pal=q.getpalette();colors=[tuple(pal[n:n+3]) for n in range(0,64*3,3)]
 for i in group:pals[i]=colors
for i,r in recipes.items():
 D=O/f'variant-{i}';D.mkdir(exist_ok=True);full=raw[i];full.save(D/'raw-unquantized.png');masks[i].save(D/'source-spatial-mask-native.png');colors=pals[i]; cache={}
 def nearest(p):
  if p not in cache:cache[p]=min(colors,key=lambda c:sum((a-b)**2 for a,b in zip(p,c)))
  return cache[p]
 seed=Image.new('RGBA',full.size);seed.putdata([nearest(p[:3])+(255,) if p[3] else (0,0,0,0) for p in full.getdata()]);seed.save(D/'raw-seed.png')
 # Ownership follows visible surfaces only; no hidden anatomy/rig claim.
 parts={n:Image.new('RGBA',seed.size) for n in ['lowerbody-boots','torso-cloth-armor','waist-wrap-sword','far-hand','near-arm-guard-hand','head-hair-face']}
 for y in range(264):
  for x in range(128):
   p=seed.getpixel((x,y))
   if not p[3]:continue
   headend=48 if i=='01' else 50
   if y<headend or (y<58 and x<53):name='head-hair-face'
   elif y>=146:name='lowerbody-boots'
   elif x>=83 and y>=122:name='far-hand'
   elif 94<=y<=119 and x>=49:name='waist-wrap-sword'
   elif x>=84 and 94<=y<=122:name='waist-wrap-sword'
   elif (y>=76 and x<(52 if y<128 else 57)) or (y>=59 and x<49):name='near-arm-guard-hand'
   else:name='torso-cloth-armor'
   parts[name].putpixel((x,y),p)
 chars=string.ascii_letters+string.digits+'!#'; unique=sorted(set(seed.getdata())-{(0,0,0,0)});legend={chars[n]:'#%02x%02x%02x'%p[:3] for n,p in enumerate(unique)};lookup={p:chars[n] for n,p in enumerate(unique)};ops={}
 for n,im in parts.items():
  im.save(D/f'{n}.png');b=im.getbbox(); x0,y0,x1,y1=b;ops[n]=[{'kind':'grid','x':x0,'y':y0,'rows':[''.join(lookup.get(im.getpixel((x,y)),'.') for x in range(x0,x1)) for y in range(y0,y1)],'legend':legend}]
 r.update({'alpha_policy':'reviewed native spatial polygon only; binary; no color key; explicit hair gaps','resampling':'NEAREST once; source-aligned native grid','palette_policy':'64 source-derived MEDIANCUT no dither; 03/05 shared palette','palette':list(legend.values()),'part_ownership':'visible pixels only; disjoint semantic owners, no hidden surfaces or motion claim','display_height':152,'display_scale':152/240,'pass_budget':'one conversion plus one named cleanup if needed','body_bounds':seed.getbbox()})
 (D/'recipe.json').write_text(json.dumps(r,indent=2));(D/'native-draw-ops.json').write_text(json.dumps({'layers':list(parts),'palette':list(legend.values()),'ops':ops},indent=2))
 # Original masked transfer, seed / bright-light mattes at true 152 body equivalence plus 3x native.
 sheet=Image.new('RGBA',(700,850),(61,63,68,255));d=ImageDraw.Draw(sheet);d.text((8,8),f'USER {i}: source / 64-color seed / light / dark; body 152px',fill='white')
 for k,(img,bg) in enumerate([(full,(61,63,68,255)),(seed,(61,63,68,255)),(seed,(221,218,210,255)),(seed,(15,19,25,255))]):
  panel=Image.new('RGBA',(150,190),bg);disp=img.resize((81,167),Image.Resampling.NEAREST);panel.alpha_composite(disp,(35,8));sheet.alpha_composite(panel,(12+k*170,32))
 for k,(img,bg) in enumerate([(full,(221,218,210,255)),(seed,(221,218,210,255)),(seed,(15,19,25,255))]):
  panel=Image.new('RGBA',(200,570),bg);pic=img.resize((256,528),Image.Resampling.NEAREST);panel.alpha_composite(pic,(-28,15));sheet.alpha_composite(panel,(12+k*225,245))
 sheet.convert('RGB').save(D/'review-seed.png')
 print(i,seed.getbbox(),len(unique))
# Confirm crop/palette registration guarantee outside mapped source changed ROI.
a=Image.open(O/'variant-03/raw-seed.png');b=Image.open(O/'variant-05/raw-seed.png');changes=[(x,y) for y in range(264) for x in range(128) if a.getpixel((x,y))!=b.getpixel((x,y))]; (O/'shared-03-05-check.json').write_text(json.dumps({'changed_count':len(changes),'changed_bounds':[min(x for x,y in changes),min(y for x,y in changes),max(x for x,y in changes)+1,max(y for x,y in changes)+1],'all_changes_source_supported':all(156<=14+(y-13+0.5)*975/240<228 for x,y in changes)},indent=2))
