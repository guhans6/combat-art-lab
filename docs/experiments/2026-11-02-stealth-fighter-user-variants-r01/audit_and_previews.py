from pathlib import Path
from PIL import Image,ImageDraw
import math,json,hashlib,sys
w=Path('/private/tmp/fighter-user-variants-r01');p=w/'check-project';ev=p/'evidence';o=w/'lead-review';o.mkdir(exist_ok=True)
meta=json.loads((ev/'runtime-checks.json').read_text());assert all(z['passed']for z in meta['checks']),meta['checks']
sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
results=[];nativehashes={}
for sid in [0,1,3,4,5]:
 f=p/'textures'/('current-rest.png'if sid==0 else f'variant-{sid:02}.png');src=Image.open(f).convert('RGBA');cap=Image.open(ev/f'native-look-{sid}.png').convert('RGB');crop=cap.crop((576,305,704,569));bad=sum(a[:3]!=b for a,b in zip(src.getdata(),crop.getdata())if a[3]);assert bad==0,(sid,bad)
 if sid:
  n=w/'native-work'/f'variant-{sid:02}'/'static.aseprite';a=read(n);comp=Image.new('RGBA',a['canvas'])
  for li,layer in enumerate(a['layers']):
   if layer['flags']&1 and(0,li)in a['cels']:comp.alpha_composite(a['cels'][(0,li)]['image'])
  assert comp.tobytes()==src.tobytes();assert a['canvas']==[128,264]and len(a['frames'])==1
  assert Image.open(w/'native-work'/f'variant-{sid:02}'/'static.png').convert('RGBA').tobytes()==src.tobytes()
  nativehashes[str(sid)]=hashlib.sha256(n.read_bytes()).hexdigest()
 # At152px, independently sample pixel centers; exclude only exact texel-boundary ties.
 fct=152/240;x0=640-64*fct;y0=558-253*fct;cap152=Image.open(ev/f'single-look-{sid}-152.png').convert('RGB');bad152=0;tested=0;ys=[]
 for y in range(math.floor(y0),math.ceil(y0+264*fct)):
  v=(y+.5-y0)/fct;sy=math.floor(v)
  for x in range(math.floor(x0),math.ceil(x0+128*fct)):
   u=(x+.5-x0)/fct;sx=math.floor(u)
   if min(abs(u-round(u)),abs(v-round(v)))<1e-5:continue
   if 0<=sx<128 and 0<=sy<264:
    c=src.getpixel((sx,sy))
    if c[3]:bad152+=c[:3]!=cap152.getpixel((x,y));tested+=1;ys.append(y)
 assert bad152==0,(sid,bad152);assert max(ys)-min(ys)+1==152 and max(ys)==557
 results.append({'source_id':sid,'native_render_opaque_rgb_mismatches':bad,'projection152_unambiguous_samples':tested,'projection152_mismatches':bad152,'drawn_height':152,'bottom_row':557})
# Four reference statics plus unchanged CurrentA; registration/source check for the near-identical pair.
a=Image.open(p/'textures/variant-03.png').convert('RGBA');b=Image.open(p/'textures/variant-05.png').convert('RGBA');changes=[(i%128,i//128)for i,(x,y)in enumerate(zip(a.getdata(),b.getdata()))if x!=y];assert all(33<=x<=66 and 47<=y<=65 for x,y in changes),changes[:3]
# Actual game captures, cropped at identical world coordinates and left at 1x.
labels=['Current A','Look 1','Look 3 · broad cap','Look 4','Look 5 · narrow cap'];board=Image.new('RGB',(1000,214),(23,27,31));d=ImageDraw.Draw(board);d.fontmode='1'
for i,sid in enumerate([0,1,3,4,5]):
 im=Image.open(ev/f'single-look-{sid}-152.png').convert('RGB').crop((540,392,740,582));board.paste(im,(i*200,24));d.text((i*200+8,7),labels[i],fill='white')
board.save(o/'five-looks-152.png');board.resize((2000,428),Image.Resampling.NEAREST).save(o/'five-looks-152-2x.png')
r={'passed':True,'ui_checks':len(meta['checks']),'static':True,'native_hashes':nativehashes,'frames':results,'shared03_05_changed_pixels':len(changes),'shared03_05_changes_only_shoulder':True,'projection_limit':'Exact texel-boundary ties excluded from fractional152/240 color oracle; native1xstrict.','preview_crop':[540,392,740,582],'preview_pixel_edits':False}
(o/'render-audit.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
