from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,sys,string,hashlib
P=Path('/private/tmp/atmospheric-idle-sample-r03');sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(P/'baseline-r02.aseprite');old=[l['name']for l in A['layers']];upper=old[2:];layers=['far-leg-pants','near-leg-pants','far-boot-cuff-fixed','near-boot-cuff-fixed']+upper
pal=['#00000000','#15191e','#1c1d20','#303035','#79583d','#ad8056','#b98d60','#24282d','#353a3f','#242d36','#3d4c59','#56636d','#626971','#303338'];legend=dict(zip(string.ascii_letters,pal[1:]));rev={c:k for k,c in legend.items()}
def blank():return Image.new('RGBA',(96,160))
def shifted(im,dy):
 out=blank();out.alpha_composite(im,(0,dy));return out
def poly(im,p,c):ImageDraw.Draw(im).polygon(p,fill=c)
base={n:A['cels'][0,i]['image'].copy()for i,n in enumerate(old)};boots={};pants={}
for n,new,cut in [('far-leg-boot','far',137),('near-leg-boot','near',136)]:
 b=base[n].copy();b.paste((0,0,0,0),(0,0,96,cut));boots[f'{new}-boot-cuff-fixed']=b
 q=base[n].copy();q.paste((0,0,0,0),(0,cut,96,160));pants[f'{new}-leg-pants']=q
def pose(d):
 out={n:im.copy()for n,im in pants.items()};out.update({n:im.copy()for n,im in boots.items()})
 for n in upper:out[n]=shifted(base[n],d)
 if d:
  # Anatomical construction hypothesis under plain trousers: pelvis drops, knees flex forward,
  # lower calf returns to original fixed ankle/cuff sites. Broad source material planes retained.
  q=blank();k=d
  poly(q,[(35,82+d),(49,83+d),(47+k,106),(43+k,119),(43+k,123),(42,136),(32,136),(32+k,124),(32+k,108)],'#24282d')
  poly(q,[(36,99+d),(42+k,100+d),(40+k,114),(37+k,126),(35,136),(32,136),(34+k,121)],'#353a3f')
  # Occlusion backing ends under source boot/cuff owner, never grows boot silhouette.
  q.paste((0,0,0,0),(0,136,96,160));out['near-leg-pants']=q
  q=blank()
  poly(q,[(46,82+d),(57,82+d),(56+d//2,105),(53+d,120),(52+d,125),(55,137),(47,137),(45+d,123),(46+d,105)],'#15191e')
  poly(q,[(51,96+d),(55,96+d),(52+d,121),(51,136),(48,136),(48+d,120)],'#24282d')
  q.paste((0,0,0,0),(0,137,96,160));out['far-leg-pants']=q
 return out
def grid(im):
 # Whole bounded artwork region including transparent clearing, to make later edits deterministic.
 x0,y0,x1,y1=28,6,65,147;rows=[]
 for y in range(y0,y1):
  r=''
  for x in range(x0,x1):
   a,b,c,d=im.getpixel((x,y));r+='.'if not d else rev[f'#{a:02x}{b:02x}{c:02x}']
  rows.append(r)
 return [{'kind':'grid','x':x0,'y':y0,'rows':rows,'legend':legend}]
poses={};landmarks={}
for d in range(3):
 data=pose(d);poses[str(d)]={n:grid(data[n])for n in layers};out=P/'drawing-data'/str(d);out.mkdir(parents=True,exist_ok=True);im=blank()
 for n in layers:data[n].save(out/f'{n}.png');im.alpha_composite(data[n])
 im.save(out/'composite-drawing-data.png')
 landmarks[str(d)]={'hair_top':[47,10+d],'shoulder':[38,40+d],'pelvis':[44,85+d],'near_hip_inferred':[40,94+d],'near_knee_inferred':[38+d,120],'near_ankle':[36,136],'far_hip_inferred':[52,94+d],'far_knee_inferred':[50+d,121],'far_ankle':[51,137],'soles_y':146}
mask=Image.new('L',(96,160));ImageDraw.Draw(mask).rectangle((28,6,64,136),fill=255);bootmask=Image.new('L',(96,160))
for im in boots.values():bootmask=ImageChops.lighter(bootmask,im.getchannel('A'))
mask.paste(0,(0,0),bootmask);mask.save(P/'editable-body-except-boots-frozen.png');bootmask.save(P/'protected-boots-frozen.png')
json.dump({'canvas':[96,160],'palette':pal,'layers':layers,'upper_rigid_owners':upper,'fixed_owners':list(boots),'ops':poses,'landmarks':landmarks,'method':'source REST upper/pelvis/skirt exact rigid descent; authored near/far pants knee/calf contour+plane redraw; source boots/cuffs immutable separate owners'},open(P/'drawing-ops.json','w'),indent=2)
(P/'observations.md').write_text('''# Grounded idle sample r03\n\nDisposable motion sample only. User rejects chest action; r01/r02/fighter and all repo assets preserved. Native source r02 SHA82e878fe5be2ebef488cd2465cc840280750eb2bc16636834212efca0ab1ebeb, source REST frame0 only. No chest expansion in any r03pose.\n\nReference inspection 2026-11-02 BEFORE plan: actual hero2-1-contact F0/1 higher, F2/3 lower while shoes stay; hero-2-contact F0toF4 hat/shoulders/coat lower then recover, feet stay; garments obscure knees, so no claim their skeletal weight transfer proven. Saint11contact actual tutorial shows bodydown/kneebend/openarms versusbodyup/armsdown;3frame example softens transition, warns against dance-like excess and suggests secondary compensation. Motion principle only: anchoredfeet plus coherent bodyrise/settle, no borrowed costume/pixels or100ms tempo. Luiz previews firstparty CC0 per lead research; Saint11tutorial reference-only rights unspecified. Findings/URLs copied inreference-evidence.\n\nTask profile frozen: one groundedmechanism study +one concrete jointrepair budget. Body/pelvis/torso/head/arms/skirt descend0/1/2px along onephase, boots/cuffs fixed. Legs redraw with forwardkneeflex returning to stable ankles. Chestwidth and all registeredrigid upper material pixels exactrest. No faceexpression/hairlag/independentbob or horizontal chestpuff. Grid96x160/palette14unchanged. Need actualrest/transition/sink nativekeys/ownerhide/markedlandmarks beforetimeline. Native12semanticparts separatepants and boots/cuffs; source bootpixels transferred exactly, not repainted. New authorizedmask allbody bounded x28..64/y6..136 excluding actualbootpixelunion; y137+ protected. Native bootowners protected beyondflatmask.\n\nAnatomical routes undercoat/trousers are inferred construction hypotheses, not proven by references. Landmarks in drawing-ops: nearhip(40,94+d)->knee(38+d,120)->ankle(36,136), farhip(52,94+d)->knee(50+d,121)->ankle(51,137). Sharedground soles146. Coat hides hips/upperthigh. Newknee/calf contours use broad source nearpants base/light and farpants black/base planes, preserving visualmaterial. Boot/cuff cutoff near136/far137 establishes narrow overlap/seam boundary; inspect nativeownerhide andcontrast for leaks beforeextending.\n\nBackend dedicatedheadlessMCP READY1.3.18.6-dev/Pebbly0.8.2; nativeinfo/restpreview inspected beforedrawing. No callablevalidate tool despite advertisedcapability; scopednative/PNGchecks planned. Pillow only drawingdata/masks/review/checks; actualnative viaMCP.\n''')
print(json.dumps({'layers':layers,'mask_sha256':hashlib.sha256((P/'editable-body-except-boots-frozen.png').read_bytes()).hexdigest()}))
