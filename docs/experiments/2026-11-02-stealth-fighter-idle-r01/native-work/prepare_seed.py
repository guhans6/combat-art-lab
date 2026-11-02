from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json,hashlib,string
O=Path('/private/tmp/stealth-fighter-idle-r01'); P=O/'seed'
src=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/concepts/stealth-fighter/game-specific-r01/silver-pines/corrected.png')
im=Image.open(src).convert('RGBA'); assert hashlib.sha256(src.read_bytes()).hexdigest()=='a3cc3ab1d658ac3d2d464ef4781ed966e815c7eedeefcf5801d81ca93924ab9c'
# Human-reviewed spatial outline. No global colour-key deletion; inner crotch opening is explicit.
poly=[(475,105),(519,105),(550,114),(566,124),(580,125),(584,131),(576,139),(582,151),(584,181),(578,174),(570,151),(560,147),(550,154),(548,165),(525,178),(521,201),(514,204),(512,188),(504,176),(495,175),(489,182),(488,199),(497,212),(502,213),(504,221),(487,216),(487,238),(474,250),(490,263),(510,271),(520,267),(508,234),(532,248),(539,242),(545,254),(551,253),(557,242),(558,233),(563,231),(562,222),(574,217),(565,192),(572,184),(568,165),(570,151),
(570,151),(572,184),(565,192),(574,217),(562,222),(563,231),(558,233),(557,242),(551,253),(545,254),(539,242),(532,248),(508,234),(521,267),(517,283),(540,289),(535,319),(550,334),(574,365),(584,414),(582,475),(579,500),(591,527),(589,541),(596,556),(592,567),(598,591),(607,626),(634,559),(640,541),(651,541),(660,552),(618,638),(624,650),(614,668),(602,678),(613,715),(620,719),(620,734),(631,756),(638,775),(638,799),(631,812),(637,841),(653,935),(658,982),(635,965),(609,943),(603,1003),(588,1029),(598,1049),(591,1103),(584,1196),(595,1229),(581,1258),(601,1276),(595,1297),(607,1308),(606,1323),(641,1348),(658,1354),(697,1359),(707,1385),(515,1385),(516,1358),(520,1330),(526,1307),(525,1282),(512,1269),(507,1228),(489,1148),(511,1077),(515,1054),(504,1040),(524,996),(513,969),(497,1019),(474,1067),(473,1096),(460,1141),(442,1204),(433,1253),(416,1273),(433,1301),(422,1327),(429,1347),(452,1363),(474,1362),(495,1365),(501,1385),(330,1385),(333,1350),(341,1332),(335,1316),(349,1304),(350,1292),(332,1286),(329,1271),(341,1238),(338,1185),(338,1102),(362,1066),(372,1041),(370,1016),(375,993),(370,984),(392,944),(399,881),(401,837),(389,833),(388,821),(402,819),(391,807),(383,807),(379,790),(377,770),(378,744),(380,730),(371,723),(363,675),(352,631),(345,611),(345,596),(343,582),(349,565),(347,548),(337,548),(332,534),(335,520),(333,510),(343,499),(334,487),(343,466),(330,457),(341,429),(346,401),(347,376),(339,363),(352,344),(355,328),(367,309),(354,315),(357,296),(368,282),(376,275),(374,260),(373,247),(387,234),(399,228),(399,216),(411,198),(425,188),(431,176),(413,180),(408,174),(415,168),(404,161),(404,145),(419,128),(436,128),(440,137),(449,137),(456,125)]
# Simplify the face route above: retain front facial contour from hairline through beard into collar.
# The first polygon's ear detour belongs inside hair; replace leading route with actual outer outline.
poly=[(475,105),(519,105),(550,114),(566,124),(580,125),(584,131),(576,139),(582,151),(584,181),(578,174),(570,151),(572,184),(565,192),(574,217),(562,222),(563,231),(558,233),(557,242),(551,253),(545,254),(539,242),(532,248),(508,234),(521,267)]+poly[poly.index((517,283)):]
mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
mask.save(P/'source-spatial-mask.png'); masked=im.copy();masked.putalpha(mask);masked.save(P/'source-masked.png')
crop=(300,88,732,1392); size=(81,244); off=(24,10)
small=masked.crop(crop).resize(size,Image.Resampling.NEAREST)
# Quantize source colours on retained pixels only; preserve binary alpha, no dithering.
pixels=[p[:3] for p in small.getdata() if p[3]]
swatch=Image.new('RGB',(len(pixels),1));swatch.putdata(pixels)
q=swatch.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
pal=q.getpalette(); colors=[tuple(pal[i:i+3]) for i in range(0,96,3)]
def nearest(p): return min(colors,key=lambda c:sum((a-b)**2 for a,b in zip(p,c)))
small.putdata([nearest(p[:3])+(255,) if p[3] else (0,0,0,0) for p in small.getdata()])
seed=Image.new('RGBA',(128,264));seed.alpha_composite(small,off);seed.save(P/'raw-seed.png')
# Native ownership is visible surface assignment, not hidden anatomy reconstruction.
# Coordinates on native grid. Mask priorities distal parts/head then torso; lower locked base last fallback.
polys={
'head-hair-neck':[(24,0),(95,0),(95,42),(65,43),(65,47),(61,46),(57,43),(55,46),(59,51),(61,54),(57,53),(51,48),(46,48),(42,49),(35,54),(34,52),(34,47),(30,49)],
'near-arm':[(28,55),(45,53),(49,60),(51,72),(49,82),(43,88),(49,91),(51,99),(48,104),(50,111),(48,123),(47,129),(48,136),(51,142),(53,149),(53,151),(50,151),(48,149),(47,148),(45,148),(43,147),(41,145),(39,145),(38,141),(38,132),(38,129),(37,126),(35,126),(33,115),(31,109),(29,104),(27,97),(27,91),(25,85),(24,77)],
'far-hand':[(79,122),(86,125),(90,133),(89,147),(86,152),(83,150)],
'sword-belt':[(48,92),(79,91),(83,94),(84,103),(87,105),(89,101),(91,94),(96,94),(96,99),(89,116),(87,120),(82,121),(79,112),(72,108),(65,112),(51,115),(44,113)],
'upper-torso':[(20,48),(63,44),(72,49),(80,58),(82,70),(82,82),(81,87),(84,94),(80,99),(73,99),(68,96),(61,97),(56,100),(49,108),(44,104),(40,89),(34,83),(25,83)]}
part_masks={}
for name,p in polys.items():
 m=Image.new('L',seed.size);ImageDraw.Draw(m).polygon(p,fill=255);part_masks[name]=m
parts={name:Image.new('RGBA',seed.size) for name in ['lower-body-fixed','upper-torso','sword-belt','far-hand','near-arm','head-hair-neck']}
for y in range(seed.height):
 for x in range(seed.width):
  px=seed.getpixel((x,y))
  if not px[3]: continue
  owner=next((n for n in ['head-hair-neck','near-arm','far-hand','sword-belt','upper-torso'] if part_masks[n].getpixel((x,y))), 'lower-body-fixed')
  if owner=='lower-body-fixed' and y<92: owner='head-hair-neck' if (x,y)==(57,44) else 'upper-torso'
  if owner=='lower-body-fixed' and 85<=x<=89 and 95<=y<=104: owner='sword-belt'
  if (x,y)==(37,128): owner='near-arm'
  parts[owner].putpixel((x,y),px)
chars=string.ascii_letters+string.digits+'!#$%&*+,-/:;<=>?@[]^_{|}~'
unique=sorted(set(seed.getdata())-{(0,0,0,0)});legend={chars[i]:'#%02x%02x%02x'%p[:3] for i,p in enumerate(unique)};lookup={p:chars[i] for i,p in enumerate(unique)}
ops={}
for name,part in parts.items():
 part.save(P/(name+'.png'))
 b=part.getbbox();x0,y0,x1,y1=b
 rows=[''.join(lookup.get(part.getpixel((x,y)),'.') for x in range(x0,x1)) for y in range(y0,y1)]
 ops[name]=[{ 'kind':'grid','x':x0,'y':y0,'rows':rows,'legend':legend}]
json.dump({'palette':list(legend.values()),'layers':list(parts),'ops':ops},open(P/'native-draw-ops.json','w'),indent=2)
json.dump({'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_size':im.size,'crop':crop,'resized':size,'offset':off,'canvas':seed.size,'silhouette_polygon_source':poly,'part_polygons_native':polys,'alpha':'manual spatial polygon; binary; nearest; no colour-key; no dither','palette':list(legend.values()),'grid_status':'agent provisional; not final game size','bounds':seed.getbbox()},open(P/'recipe.json','w'),indent=2)
# Still source and raw seed, common output scale. Labels outside art.
bg=(55,59,65,255)
sheet=Image.new('RGBA',(128*4+40,264*4+42),bg);d=ImageDraw.Draw(sheet);d.text((10,8),'RAW SEED / provisional 128 x 264 / body ~240px',fill='white');sheet.alpha_composite(seed.resize((512,1056),Image.Resampling.NEAREST),(20,32));sheet.convert('RGB').save(P/'seed-4x.png')
# Smoke independent check uses decoded actual exports.
a=Image.open(O/'smoke/before.png').convert('RGBA');b=Image.open(O/'smoke/after.png').convert('RGBA');r=Image.open(O/'smoke/reopened.png').convert('RGBA');bad=Image.open(O/'smoke/deliberate-out-of-mask.png').convert('RGBA')
diffs=[(x,y) for y in range(16) for x in range(16) if a.getpixel((x,y))!=b.getpixel((x,y))]
assert diffs==[(11,9)] and list(b.getdata())==list(r.getdata())
rejected=any(b.getpixel((x,y))!=bad.getpixel((x,y)) for y in range(16) for x in range(16) if (x,y)!=(11,9));assert rejected
json.dump({'one_pixel':diffs,'reopen_exact':True,'protected_export_exact':Image.open(O/'smoke/protected-after.png').tobytes()==Image.open(O/'smoke/protected-reopened.png').tobytes(),'out_of_mask_rejected':rejected,'grid_dot':'observed erase, not transparent skip; omit unaffected positions/regions'},open(O/'smoke/checks.json','w'),indent=2)
