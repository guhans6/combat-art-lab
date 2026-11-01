"""Fixed source-coordinate traces and shared-palette seed; no automatic art score."""
from pathlib import Path
from PIL import Image, ImageDraw,ImageStat
import json,hashlib,argparse
HERE=Path(__file__).resolve().parent
# This E0 adapter lives one directory deeper than the historical script.
# Anchor source lookup at the workspace without mutating the original recipe.
ROOT=HERE.parents[3]
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path);args=parser.parse_args()
if args.out: HERE=args.out.resolve();HERE.mkdir(parents=True,exist_ok=False)
CROP=(380,64,860,512); SIZE=(120,112)
SOURCE=ROOT/'assets/references/approved-2026-10-26/character-closeup.png'
source=Image.open(SOURCE).convert('RGB'); crop=source.crop(CROP)
# Visible-part traces, measured against source-coordinate-guide.png. No hidden surfaces.
regions={
'01-jacket':[(430,512),(439,485),(454,454),(485,430),(518,413),(551,395),(580,386),(597,381),(625,385),(669,377),(702,382),(731,389),(754,406),(780,425),(799,446),(818,477),(842,512)],
'02-shirt':[(556,454),(575,442),(594,434),(627,433),(663,438),(686,451),(676,478),(671,512),(536,512),(544,479)],
'03-neck-ear':[(593,350),(670,367),(671,390),(679,412),(693,431),(687,451),(670,472),(637,488),(610,494),(583,484),(565,475),(562,457),(576,438),(592,417),(597,393)],
'04-rear-hair':[(489,202),(477,207),(462,202),(441,213),(422,226),(408,239),(398,253),(404,247),(395,266),(399,269),(393,284),(397,302),(404,318),(415,329),(422,329),(419,347),(429,356),(440,354),(448,367),(461,368),(474,358),(487,359),(494,366),(510,371),(523,370),(536,380),(544,379),(537,370),(550,368),(557,381),(567,384),(560,375),(555,361),(570,357),(584,350),(594,338),(590,311),(574,287),(549,266),(524,237),(503,214)],
'05-face':[(582,284),(603,273),(628,251),(654,239),(673,238),(690,244),(707,239),(722,240),(731,250),(735,272),(735,294),(740,311),(736,330),(728,348),(719,362),(702,373),(673,377),(646,374),(620,366),(602,355),(589,340),(574,343),(559,338),(548,329),(546,314),(551,300),(561,291),(573,289)],
'06-crown-fringe':[(473,204),(462,194),(458,181),(460,168),(467,158),(481,146),(493,143),(507,151),(517,152),(539,141),(562,135),(582,127),(605,125),(631,124),(653,127),(670,131),(684,127),(698,131),(714,136),(731,138),(742,124),(747,107),(746,128),(738,141),(751,148),(756,158),(767,166),(771,178),(781,186),(787,204),(785,220),(781,235),(784,249),(777,267),(765,280),(768,301),(781,315),(779,330),(774,320),(768,320),(763,308),(758,301),(757,321),(751,345),(740,354),(731,355),(740,339),(742,320),(735,305),(733,284),(730,266),(723,244),(718,234),(708,236),(700,235),(702,252),(696,264),(691,278),(684,279),(684,267),(680,254),(673,241),(666,228),(663,211),(661,232),(654,245),(646,248),(638,258),(629,268),(617,275),(609,287),(610,303),(620,319),(616,326),(605,322),(596,311),(590,300),(583,286),(573,290),(568,304),(569,317),(580,326),(582,337),(577,345),(566,342),(558,330),(555,314),(553,302),(548,300),(543,312),(539,313),(533,300),(528,282),(523,271),(510,256),(503,239),(500,224),(489,222),(483,213)],
'07-hair-tie':[(486,218),(493,218),(496,223),(496,238),(488,240),(487,229)],
'08-eyes-brows':[(608,259),(675,253),(677,317),(611,318)],
'09-mouth':[(669,331),(714,331),(714,349),(669,349)]}
# Far-eye second island is part of the features region.
extras={'08-eyes-brows':[[(702,243),(735,243),(737,308),(704,308)]]}
# Generated masks are preparation only; actual native sources are saved by Aseprite.
prep=HERE/'prepared';prep.mkdir(exist_ok=True)
mask_source={}
for name,pts in regions.items():
 m=Image.new('L',crop.size);d=ImageDraw.Draw(m)
 for poly in [pts,*extras.get(name,[])]:d.polygon([(x-380,y-64) for x,y in poly],fill=255)
 mask_source[name]=m
# Regions for facial features are ownership masks, not parts of the outer silhouette.
fg=Image.new('L',crop.size)
for name,m in mask_source.items():
 if not name.startswith(('08','09')):fg=Image.frombytes('L',fg.size,bytes(max(a,b) for a,b in zip(fg.tobytes(),m.tobytes())))
fg.save(prep/'source-silhouette-mask.png')
# Source-derived palette extracted from foreground only; 48 is this study's policy.
pixels=[p for p,a in zip(crop.get_flattened_data(),fg.get_flattened_data()) if a]
strip=Image.new('RGB',(len(pixels),1));strip.putdata(pixels)
q=strip.quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
pal=q.getpalette()[:48*3]; palette=[tuple(pal[i:i+3]) for i in range(0,len(pal),3)]
policy=Image.new('P',(1,1));policy.putpalette(pal+[0]*(768-len(pal)))
seed=crop.resize(SIZE,Image.Resampling.BOX).quantize(palette=policy,dither=Image.Dither.NONE).convert('RGBA')
# Binary alpha from majority coverage. Expose raw unmasked seed separately.
seed.save(prep/'raw-seed-with-background.png')
alpha=fg.resize(SIZE,Image.Resampling.BOX).point(lambda v:255 if v>=128 else 0)
seed.putalpha(alpha);seed.save(prep/'converted-seed.png')
# Ownership masks by layer, top-down. Only actual visible samples are extracted.
small={n:m.resize(SIZE,Image.Resampling.BOX).point(lambda v:255 if v>0 else 0) for n,m in mask_source.items()}
used=Image.new('L',SIZE)
for n in reversed(regions):
 m=Image.frombytes('L',SIZE,bytes(255 if a and b and not c else 0 for a,b,c in zip(small[n].tobytes(),alpha.tobytes(),used.tobytes())))
 layer=Image.new('RGBA',SIZE);layer.paste(seed,(0,0),m);layer.save(prep/(n+'.png'));m.save(prep/(n+'-mask.png'))
 used=Image.frombytes('L',SIZE,bytes(max(a,b) for a,b in zip(used.tobytes(),m.tobytes())))
assert used.tobytes()==alpha.tobytes(), 'Mask coverage failed'
# Colors sampled at role points, snapped once to shared source palette.
roles={'edge':(534,210),'hair':(560,185),'hairplane':(572,159),'hairlight':(598,203),'hairdeep':(485,313),'skin':(655,325),'skinlight':(710,323),'skinshadow':(615,369),'skindeep':(626,390),'blush':(639,319),'white':(640,292),'iris':(659,296),'lid':(643,273),'mouth':(689,340),'tie':(491,229),'jacket':(700,405),'jacketlight':(749,424),'jacketdeep':(714,468),'shirt':(595,505),'shirtshadow':(576,509),'strap':(797,473)}
def color(pt):
 box=source.crop((pt[0]-1,pt[1]-1,pt[0]+2,pt[1]+2));rgb=tuple(int(v) for v in ImageStat.Stat(box).median)
 return min(palette,key=lambda c:sum((a-b)**2 for a,b in zip(c,rgb)))
rolecolors={k:color(v) for k,v in roles.items()}
# Additional deep feature role; selected from source brow cluster.
rolecolors['feature']=min(palette,key=lambda c:sum((a-b)**2 for a,b in zip(c,(55,33,26))))
def lua(v):
 if isinstance(v,str):return json.dumps(v)
 if isinstance(v,(tuple,list)):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
 return str(v)
(HERE/'traces.json').write_text(json.dumps({'crop':CROP,'grid':SIZE,'visible_part_polygons':regions,'feature_islands':extras,'sample_points':roles,'role_colors':rolecolors,'palette':palette,'source':str(SOURCE.relative_to(ROOT)),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()},indent=2)+'\n')
(HERE/'data.lua').write_text('return '+lua({'regions':regions,'colors':rolecolors,'palette':palette})+'\n')
print('Prepared 48-color shared palette, source-coordinate trace masks, BOX seed and nine visible semantic parts.')
