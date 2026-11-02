from pathlib import Path
from PIL import Image
import json,hashlib,math
w=Path('/private/tmp/fighter-playground-r01');p=w/'check-project';ev=p/'evidence';r=json.loads((ev/'runtime-checks.json').read_text());assert all(c['passed']for c in r['checks'])
rows=[]
for i in range(4):
 a=Image.open(p/'textures'/f'idle-{i}.png').convert('RGBA');b=Image.open(ev/f'native-frame-{i:02}.png').convert('RGBA').crop((576,305,704,569));bad=sum(x[:3]!=y[:3]for x,y in zip(a.getdata(),b.getdata())if x[3]);assert bad==0,(i,bad);rows.append({'frame':i,'opaque_rgb_mismatches':bad})
# Independent nearest-sample checks for all three simultaneously displayed heights.
cap=Image.open(ev/'compare.png').convert('RGB');src=Image.open(p/'textures/idle-0.png').convert('RGBA');projections=[]
for i,h in enumerate([96,128,160]):
 f=h/240;x0=40+200+400*i-64*f;y0=158+400-253*f;bad=0;tested=0;ys=[]
 for y in range(math.floor(y0),math.ceil(y0+264*f)):
  sy=math.floor((y+.5-y0)/f)
  for x in range(math.floor(x0),math.ceil(x0+128*f)):
   sx=math.floor((x+.5-x0)/f)
   if 0<=sx<128 and 0<=sy<264:
    c=src.getpixel((sx,sy))
    if c[3]:
     bad+=cap.getpixel((x,y))!=c[:3];tested+=1;ys.append(y)
 assert bad==0,(h,bad)
 projections.append({'height':h,'opaque_pixels_tested':tested,'opaque_rgb_mismatches':bad,'drawn_height':max(ys)-min(ys)+1,'bottom_opaque_row':max(ys)})
 for_actual=max(ys)-min(ys)+1
 assert for_actual==h and max(ys)==557,(h,for_actual,max(ys))
a={'passed':True,'ui_checks':len(r['checks']),'native_frames':rows,'scaled_compare':projections,'viewport':[1280,800],'stage':[1200,480],'source_pixels_preserved':True,'camera_world_fixed':True}
(ev/'render-audit.json').write_text(json.dumps(a,indent=2));print(json.dumps(a))
