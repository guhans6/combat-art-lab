from PIL import Image, ImageDraw
from pathlib import Path
import json, string, hashlib
P=Path('/private/tmp/atmospheric-breathing-proxy-r01')
W,H=96,160
C={'ink':'#15191e','hair':'#1c1d20','hairlight':'#303035','skinshadow':'#79583d','skin':'#ad8056','skinlight':'#b98d60','trousers':'#24282d','trouserlight':'#353a3f','coatshadow':'#242d36','coat':'#3d4c59','coatlight':'#56636d','collar':'#626971','bootlight':'#303338'}
layers=['far-leg-boot','near-leg-boot','pelvis-root','coat-back-skirt','far-sleeve-hand','thorax-coat','neck-collar','head-hair-face','near-upper-sleeve','near-forearm-hand']
def image():return Image.new('RGBA',(W,H))
def poly(im,pts,c):ImageDraw.Draw(im).polygon(pts,fill=C.get(c,c))
def line(im,pts,c,width=1):ImageDraw.Draw(im).line(pts,fill=C[c],width=width)
def shape(level,expansion=None):
 p={n:image() for n in layers};d=level;e=d if expansion is None else expansion
 # Fixed leg roots, natural long limbs, plain boots; pelvis never moves.
 poly(p['far-leg-boot'],[(46,82),(57,82),(56,104),(53,123),(55,138),(63,142),(64,146),(48,146),(47,139),(45,121),(46,103)],'ink')
 poly(p['far-leg-boot'],[(51,96),(55,96),(52,122),(51,135),(48,135),(48,120)],'trousers')
 poly(p['far-leg-boot'],[(52,139),(58,141),(60,143),(51,143)],'bootlight')
 poly(p['near-leg-boot'],[(35,82),(49,83),(46,108),(43,123),(42,139),(45,143),(45,146),(31,146),(31,140),(32,124),(32,107)],'trousers')
 poly(p['near-leg-boot'],[(36,99),(42,100),(40,114),(37,126),(35,137),(32,138),(34,121)],'trouserlight')
 poly(p['near-leg-boot'],[(32,136),(40,137),(42,140),(45,143),(45,146),(31,146),(31,141)],'ink')
 poly(p['near-leg-boot'],[(34,139),(39,139),(42,142),(35,142)],'bootlight')
 poly(p['pelvis-root'],[(34,75),(54,75),(57,87),(51,95),(34,94),(32,85)],'trousers')
 # Coat skirt behind the legs/torso. Simple uninterrupted cloth, no armor or belts.
 poly(p['coat-back-skirt'],[(34,65),(53,67),(55,84),(57,101),(49,98),(43,93),(34,99),(30,96),(32,82)],'coatshadow')
 poly(p['coat-back-skirt'],[(33,77),(40,79),(39,93),(33,96),(31,95)],'coat')
 # Far arm is carried behind chest; complete hidden sleeve and hand backing.
 poly(p['far-sleeve-hand'],[(49,39-d),(56,41-d),(58,58-d),(59,73-d),(60,84-d),(56,87-d),(53,83-d),(52,70-d),(50,59-d)],'coatshadow')
 poly(p['far-sleeve-hand'],[(56,79-d),(60,79-d),(61,87-d),(58,90-d),(55,86-d)],'skinshadow')
 # Connected thorax: shoulder moves upward, chest expands forward 3px, waist tapers to fixed root.
 back=34-(1 if d>=2 else 0); front=57+e
 poly(p['thorax-coat'],[(back,41-d),(39,36-d),(47,35-d),(54,39-d),(front,48-d),(front,61-d),(55+e//2,73),(54,81),(48,85),(34,82),(32,70),(back-1,55-d)],'coat')
 poly(p['thorax-coat'],[(back,42-d),(40,39-d),(43,45-d),(40,60),(41,76),(47,84),(34,82),(32,70),(back-1,54-d)],'coatshadow')
 poly(p['thorax-coat'],[(46,38-d),(52,40-d),(front-1,49-d),(front-1,57-d),(52,54-d),(50,45-d)],'coatlight')
 poly(p['thorax-coat'],[(52,58-d),(front,56-d),(front,61-d),(55+e//2,73),(54,79),(49,81),(50,72)],'coatshadow')
 poly(p['thorax-coat'],[(43,70),(47,75),(48,81),(43,79)],'coatlight')
 # Neck belongs to collar owner, skull/face belongs entirely to head owner.
 poly(p['neck-collar'],[(46,27-d),(54,27-d),(55,35-d),(52,40-d),(45,36-d),(44,33-d)],'skinshadow')
 poly(p['neck-collar'],[(51,29-d),(54,29-d),(55,35-d),(52,38-d),(49,35-d)],'skin')
 poly(p['neck-collar'],[(42,35-d),(46,33-d),(50,38-d),(52,42-d),(46,40-d),(41,37-d)],'coatshadow')
 poly(p['neck-collar'],[(53,35-d),(57,37-d),(56,44-d),(52,40-d)],'collar')
 # Original young-adult profile. Two face planes, no eye/mouth/outline microdetail.
 poly(p['head-hair-face'],[(45,14-d),(54,12-d),(58,15-d),(59,21-d),(61,24-d),(59,25-d),(59,29-d),(56,32-d),(50,31-d),(45,26-d),(43,21-d)],'skin')
 poly(p['head-hair-face'],[(44,20-d),(49,19-d),(49,25-d),(52,29-d),(56,32-d),(50,31-d),(45,26-d)],'skinshadow')
 poly(p['head-hair-face'],[(43,13-d),(47,10-d),(54,10-d),(59,13-d),(59,17-d),(56,16-d),(53,19-d),(49,20-d),(48,25-d),(45,23-d),(42,22-d),(41,17-d)],'hair')
 poly(p['head-hair-face'],[(44,13-d),(48,11-d),(54,11-d),(57,13-d),(50,13-d),(46,16-d),(43,17-d)],'hairlight')
 # Near arm attached under shoulder; elbow and wrist share same displacement as shoulder.
 poly(p['near-upper-sleeve'],[(36,39-d),(42,40-d),(46,46-d),(44,58-d),(41,65-d),(34,64-d),(32,59-d),(32,47-d)],'coatshadow')
 poly(p['near-upper-sleeve'],[(35,40-d),(40,40-d),(43,45-d),(41,55-d),(36,58-d),(33,57-d),(33,47-d)],'coat')
 poly(p['near-upper-sleeve'],[(36,40-d),(40,40-d),(42,44-d),(39,46-d),(34,47-d)],'coatlight')
 poly(p['near-forearm-hand'],[(34,59-d),(41,60-d),(43,70-d),(46,79-d),(42,83-d),(38,80-d),(35,70-d),(32,65-d)],'coatshadow')
 poly(p['near-forearm-hand'],[(34,62-d),(37,62-d),(39,70-d),(42,77-d),(39,78-d),(36,70-d)],'coat')
 poly(p['near-forearm-hand'],[(40,78-d),(45,77-d),(48,85-d),(47,90-d),(43,91-d),(40,87-d),(40,83-d)],'skin')
 poly(p['near-forearm-hand'],[(40,81-d),(42,82-d),(44,89-d),(43,91-d),(40,87-d)],'skinshadow')
 return p
legend=dict(zip(string.ascii_letters,C.values()))
def grid(im):
 bb=im.getbbox()
 if not bb:return []
 x0,y0,x1,y1=bb; rev={v.lower():k for k,v in legend.items()}
 rows=[]
 for y in range(y0,y1):
  row=''
  for x in range(x0,x1):
   r,g,b,a=im.getpixel((x,y));row+='.' if not a else rev[f'#{r:02x}{g:02x}{b:02x}']
  rows.append(row)
 return [{'kind':'grid','x':x0,'y':y0,'rows':rows,'legend':legend}]
ops={}; landmarks={}
for lev in range(4):
 parts=shape(lev);out=P/'drawing-data'/f'level-{lev}';out.mkdir(parents=True,exist_ok=True)
 composite=image()
 for n,im in parts.items():
  im.save(out/f'{n}.png');composite.alpha_composite(im)
 composite.save(out/'composite-drawing-data.png')
 ops[str(lev)]={n:grid(im) for n,im in parts.items()}
 landmarks[str(lev)]={'hair_top':[47,10-lev],'chin':[56,32-lev],'neck':[51,35-lev],'shoulder':[38,40-lev],'chest_front':[57+lev,52-lev],'elbow':[37,62-lev],'wrist':[43,80-lev],'pelvis':[44,85],'knee_near':[37,119],'soles_y':146}
json.dump({'canvas':[W,H],'layers':layers,'palette':['#00000000']+list(C.values()),'ops':ops,'landmarks':landmarks},open(P/'drawing-ops.json','w'),indent=2)
(P/'observations.md').write_text('''# Atmospheric traveler breathing proxy r01\n\nOriginal proxy design, not the selected fighter or its successor. Style-only authority: corrected.png in selected fighterA/silver-pines. Actual reference inspected: nearblack broad shadow planes, muted indigo, warm face, restrained facial planes; its armor/weapon/tiedhair not copied. New silhouette: short dark hair, plain mid-thigh bluegrey coat, charcoal trousers/boots. No face feature changes.\n\n96x160 new native grid; rest drawn y10..146 (137px), head+hair22px approximately6.2visible heads, anatomical head20px approximately6.8 heads. Proxy experiment only. Intended projected body128px uses nearest-neighbor preview resampling, not production source resizing.\n\nTask profile: ONE original asset, ONE breath loop, ONE concrete structural repair budget. Keys rest / transition level2 / apex level3. Primary chain fixedsoles/pelvis -> expanded thorax -> elevated shoulders/collar/neck -> unchanged rigid skull/hair/face and arms. 3px chestforward and3px shoulder/head lift atapex; waist tapers to fixedroot. Looser coat redraw; no stretchrows. Arms translate with supported shoulder displacement preserving elbow/wrist length; hand not pocketed. Fararm has complete backing behind thorax; neck extends behind skull and collar; nearupper/lowerarm overlap y59..65 atrest. No props. No blinking.\n\nNative master is built with dedicated Aseprite MCP grid operations from authored polygon drawingdata. Pillow writes only drawingdata/masks/check/preview files, never native. Editor1.3.18.6-dev/Pebbly0.8.2 headless preflightREADY. validate capability advertised but no callable validate tool exposed. Native/PNG equivalent checks will be recorded, without claiming validate call.\n''')
print(json.dumps({'levels':4,'layers':layers,'palette':list(C.values())}))
