"""Source-assisted full character and one building's visible parts. Preparation only."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[2];P=H/'prepared';P.mkdir(exist_ok=True)
CROP=(448,208,800,1040);N=(96,216);SOURCE=R/'assets/references/approved-2026-10-26/character-scene.png';src=Image.open(SOURCE).convert('RGB');crop=src.crop(CROP)
# Manual source-coordinate visible silhouette, reviewed against source-guide.png.
outline=[(531,244),(544,240),(555,241),(568,240),(584,238),(600,239),(616,242),(632,245),(640,239),(646,229),(648,233),(645,248),(653,252),(662,264),(665,278),(660,297),(653,314),(653,332),(645,350),(635,356),(629,357),(628,366),(643,358),(657,360),(664,366),(670,375),(680,389),(690,411),(699,438),(713,468),(724,491),(730,512),(725,530),(715,543),(723,565),(727,589),(731,613),(731,637),(726,650),(712,659),(696,662),(689,665),(691,688),(696,725),(701,763),(709,809),(721,850),(733,890),(740,915),(740,936),(733,956),(741,967),(751,979),(762,990),(766,1003),(760,1013),(740,1018),(717,1016),(699,1014),(681,1011),(670,1005),(670,995),(667,986),(658,975),(653,968),(644,957),(640,944),(634,923),(627,893),(618,859),(610,824),(604,788),(599,758),(591,735),(591,769),(594,805),(596,846),(602,887),(613,926),(622,947),(623,963),(614,975),(613,986),(608,998),(594,1005),(575,1009),(554,1010),(533,1011),(514,1009),(509,1002),(510,990),(518,980),(533,972),(538,960),(536,948),(529,937),(524,909),(522,879),(519,841),(516,802),(514,763),(512,723),(509,683),(511,645),(509,620),(502,641),(496,643),(491,631),(490,615),(493,594),(494,577),(492,565),(487,549),(486,539),(476,526),(470,515),(464,504),(464,488),(469,469),(476,445),(484,420),(493,400),(500,383),(511,370),(527,361),(544,357),(549,351),(542,351),(536,358),(530,367),(527,365),(530,350),(519,350),(510,345),(506,349),(505,340),(497,338),(495,329),(490,321),(489,309),(491,298),(486,303),(490,292),(494,284),(489,287),(495,278),(505,269),(512,261),(520,259),(523,258),(522,249),(526,243)]
# Disjoint semantic ownership, based on source position; no hidden surfaces inferred.
regions={
'01-denim':[(490,510),(650,507),(700,685),(752,964),(650,980),(589,741),(628,981),(521,981),(495,686)],
'02-shoes':[(500,958),(629,958),(629,1024),(500,1024)],
'03-far-shoe':[(643,958),(777,958),(777,1024),(643,1024)],
'04-tote':[(643,378),(666,375),(675,472),(694,525),(727,540),(743,659),(690,674),(665,647),(647,552)],
'05-jacket':[(461,377),(542,351),(606,350),(659,353),(692,396),(736,493),(733,536),(689,580),(657,565),(627,551),(615,500),(544,510),(513,643),(492,649),(483,565),(462,519)],
'06-shirt':[(560,383),(606,384),(631,379),(612,438),(605,494),(609,518),(581,514),(549,523),(539,514),(548,472),(548,427)],
'07-hands':[(488,527),(509,523),(527,544),(516,568),(503,569),(492,549)],
'08-near-hand':[(658,527),(678,525),(696,538),(683,559),(660,584),(643,578),(625,557)],
'09-neck-face':[(560,285),(594,273),(633,278),(648,304),(648,340),(635,356),(622,357),(627,374),(620,393),(594,405),(577,402),(559,395),(562,381),(576,368),(577,350),(554,334)],
'10-rear-hair':[(522,255),(541,269),(563,296),(567,340),(541,356),(527,368),(511,355),(492,344),(481,319),(486,282)],
'11-crown-fringe':[(518,260),(519,240),(556,231),(611,228),(647,224),(662,252),(672,277),(665,306),(655,323),(657,341),(649,352),(642,351),(642,326),(638,308),(635,288),(628,282),(627,300),(619,310),(616,299),(611,286),(607,280),(601,292),(589,303),(580,314),(579,332),(576,339),(571,334),(562,320),(555,322),(553,337),(546,341),(542,326),(541,308),(535,302),(527,289)],
'12-hair-tie':[(525,279),(533,279),(534,287),(526,289)],
'13-eyes-mouth':[(586,302),(614,302),(614,326),(586,326)],
'14-strap':[(651,379),(662,377),(659,419),(660,463),(667,495),(661,498),(652,468),(647,421)]}
extra={'13-eyes-mouth':[[(625,296),(641,296),(641,322),(625,322)],[(610,331),(634,331),(634,344),(610,344)]]}
outer=Image.new('L',crop.size);d=ImageDraw.Draw(outer);d.polygon([(x-448,y-208) for x,y in outline],fill=255)
# Reinstate the open space between the planted legs from measured source boundaries.
d.polygon([(590-448,721-208),(600-448,762-208),(610-448,814-208),(620-448,857-208),(631-448,906-208),(640-448,943-208),(634-448,955-208),(624-448,963-208),(618-448,934-208),(608-448,904-208),(602-448,868-208),(596-448,826-208),(592-448,785-208)],fill=0)
outer.save(P/'character-source-mask.png')
pixels=[px for px,a in zip(crop.get_flattened_data(),outer.get_flattened_data()) if a]
strip=Image.new('RGB',(len(pixels),1));strip.putdata(pixels);q=strip.quantize(colors=64,dither=Image.Dither.NONE);pal=q.getpalette()[:192]
policy=Image.new('P',(1,1));policy.putpalette(pal+[0]*(768-len(pal)))
seed=crop.resize((88,208),Image.Resampling.BOX).quantize(palette=policy,dither=Image.Dither.NONE).convert('RGBA');a=outer.resize((88,208),Image.Resampling.BOX).point(lambda v:255 if v>=128 else 0);seed.putalpha(a)
full=Image.new('RGBA',N);full.paste(seed,(4,4));full.save(P/'raw-character-seed.png')
maskdict={}
for name,pts in regions.items():
 m=Image.new('L',crop.size);dd=ImageDraw.Draw(m)
 for poly in [pts,*extra.get(name,[])]:dd.polygon([(x-448,y-208) for x,y in poly],fill=255)
 native=Image.new('L',N);native.paste(m.resize((88,208),Image.Resampling.BOX).point(lambda v:255 if v>0 else 0),(4,4));maskdict[name]=native
# Reviewed neck curl belongs to moving rear hair, rather than the denim fallback.
maskdict['10-rear-hair'].putpixel((33,38),255)
# Explicit fallback for visible samples at traced ownership boundaries.
used=Image.new('L',N)
for name in reversed(regions):
 m=Image.frombytes('L',N,bytes(255 if x and y and not z else 0 for x,y,z in zip(maskdict[name].tobytes(),full.getchannel('A').tobytes(),used.tobytes())))
 if name=='01-denim':m=Image.frombytes('L',N,bytes(255 if y and not z else 0 for y,z in zip(full.getchannel('A').tobytes(),used.tobytes())))
 im=Image.new('RGBA',N);im.paste(full,(0,0),m);im.save(P/(name+'.png'));m.save(P/(name+'-mask.png'));used=Image.frombytes('L',N,bytes(max(x,y) for x,y in zip(used.tobytes(),m.tobytes())))
assert used.tobytes()==full.getchannel('A').tobytes()
# Same spatial reduction for background; earlier generated plate is supporting source.
BG=R/'assets/source/street-preview-v01/background-clean-generated.png';bg=Image.open(BG).convert('RGB');padded=Image.new('RGB',(1448,1088));padded.paste(bg,(0,0));padded.paste(bg.crop((0,1085,1448,1086)).resize((1448,2)),(0,1086));env=padded.resize((362,272),Image.Resampling.BOX).quantize(colors=96,dither=Image.Dither.NONE).convert('RGBA');env.save(P/'background-converted-seed.png')
envregions={
'01-sky-and-distant-context':None,
'02-distant-city':[(1020,330),(1400,330),(1448,520),(1448,806),(1070,806)],
'03-mid-left-building':[(902,218),(1002,219),(1061,470),(1103,801),(1010,846),(901,809)],
'04-right-building':[(1395,0),(1448,0),(1448,815),(1373,787),(1366,360)],
'05-near-shop-wall':[(0,0),(608,0),(813,211),(849,841),(0,970)],
'06-ground-and-road':[(0,944),(804,838),(1107,799),(1448,785),(1448,1088),(0,1088)],
'07-shop-glass':[(0,46),(467,230),(469,790),(0,929)],
'08-shop-awning':[(0,0),(263,0),(610,151),(610,213),(0,22)],
'09-shop-posts':[(438,205),(461,216),(463,801),(437,811)],
'10-shop-steps':[(350,786),(592,783),(685,837),(328,917)],
'11-bridge':[(1043,507),(1448,503),(1448,602),(1056,590)],
'12-pole-and-lamp':[(897,0),(921,0),(921,79),(982,78),(1019,100),(1028,124),(1011,143),(972,142),(947,124),(948,111),(920,112),(922,831),(895,839)],
'13-shop-lamp-pixels':[(375,152),(441,152),(448,180),(375,180)]}
used=Image.new('L',env.size)
for name in reversed(envregions):
 m=Image.new('L',env.size)
 if envregions[name] is None:m=Image.frombytes('L',env.size,bytes(255 if not x else 0 for x in used.tobytes()))
 else:
  ImageDraw.Draw(m).polygon([(round(x/4),round(y/4)) for x,y in envregions[name]],fill=255);m=Image.frombytes('L',env.size,bytes(255 if a and not b else 0 for a,b in zip(m.tobytes(),used.tobytes())))
 im=Image.new('RGBA',env.size);im.paste(env,(0,0),m);im.save(P/('bg-'+name+'.png'));m.save(P/('bg-'+name+'-mask.png'));used=Image.frombytes('L',env.size,bytes(max(a,b) for a,b in zip(used.tobytes(),m.tobytes())))
assert set(used.get_flattened_data())=={255}
data={'character_layers':list(regions),'background_layers':list(envregions),'character_palette':[pal[i:i+3] for i in range(0,192,3)],'character_outline':outline,'character_regions':regions,'feature_regions':extra,'background_regions':envregions,'background_palette':[list(c[:3]) for c in sorted(set(env.get_flattened_data()))],'character_crop':CROP,'character_canvas':N,'scene_canvas':[362,272],'character_scene_position':[108,48],'palette_policies':{'character':64,'background':96},'inputs':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SOURCE,BG,R/'assets/references/approved-2026-10-26/character-closeup.png',R/'assets/source/assisted-bust-v01/bust.aseprite']}}
(H/'construction-data.json').write_text(json.dumps(data,indent=2)+'\n')
def lua(v):
 if v is None:return 'false'
 if isinstance(v,str):return json.dumps(v)
 if isinstance(v,(list,tuple)):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,dict):return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'
 return str(v)
(H/'data.lua').write_text('return '+lua(data)+'\n')
print('Prepared controlled full-character conversion, 14 visible parts, and 13 background visible-part masks.')
