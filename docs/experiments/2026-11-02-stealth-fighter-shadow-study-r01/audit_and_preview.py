from pathlib import Path
from PIL import Image,ImageDraw
import json,math
w=Path('/private/tmp/fighter-shadow-study-r01');p=w/'check-project';ev=p/'evidence';meta=json.loads((ev/'runtime-checks.json').read_text());assert all(q['passed']for q in meta['checks'])
def source_samples(src,center,h):
 f=h/240;x0=center-64*f;y0=558-253*f;points=[]
 for y in range(math.floor(y0),math.ceil(y0+264*f)):
  v=(y+.5-y0)/f;sy=math.floor(v)
  for x in range(math.floor(x0),math.ceil(x0+128*f)):
   u=(x+.5-x0)/f;sx=math.floor(u)
   # Exact texel-boundary ties differ across CPU double and GPU float precision.
   # Exclude only those mathematical ties from the color-oracle comparison.
   if min(abs(u-round(u)),abs(v-round(v)))<1e-5:continue
   if 0<=sx<128 and 0<=sy<264:
    c=src.getpixel((sx,sy))
    if c[3]:points.append((x,y,c[:3]))
 return points
rows=[]
for i in range(4):
 src=Image.open(p/'textures'/f'idle-{i}.png').convert('RGBA');cap=Image.open(ev/f'native-frame-{i:02}.png').convert('RGB');pts=source_samples(src,640,240);bad=sum(cap.getpixel((x,y))!=c for x,y,c in pts);assert bad==0,(i,bad)
 cap152=Image.open(ev/f'source-152-frame-{i:02}.png').convert('RGB');pts152=source_samples(src,640,152);bad152=sum(cap152.getpixel((x,y))!=c for x,y,c in pts152);assert bad152==0,(i,bad152)
 rows.append({'frame':i,'native_opaque_rgb_mismatches':bad,'projection152_unambiguous_opaque_rgb_mismatches':bad152})
src=Image.open(p/'textures/idle-0.png').convert('RGBA');cap=Image.open(ev/'compare-128-152-160.png').convert('RGB');projections=[]
for i,h in enumerate([128,152,160]):
 pts=source_samples(src,240+i*400,h);assert all(cap.getpixel((x,y))==c for x,y,c in pts);ys=[v[1]for v in pts];assert max(ys)-min(ys)+1==h and max(ys)==557
 projections.append({'height':h,'drawn_height':max(ys)-min(ys)+1,'opaque_mismatches':0,'bottom_row':557})
files=['sprite-colors-152','dim-room-152','lamp-fill-152'];caps=[Image.open(ev/(f+'.png')).convert('RGB')for f in files];base=caps[0]
for im in caps[1:]:
 bad=0
 for y in range(800):
  for x in range(1280):
   if not(40<=x<1240 and 158<=y<638)and not(640<=x<1240 and 25<=y<92):bad+=im.getpixel((x,y))!=base.getpixel((x,y))
 assert bad==0,bad
pts=source_samples(src,640,152)
means=[sum((.2126*im.getpixel((x,y))[0]+.7152*im.getpixel((x,y))[1]+.0722*im.getpixel((x,y))[2])for x,y,c in pts)/len(pts)for im in caps]
assert means[1]<means[0]and means[2]>means[1],means
out=Image.new('RGB',(960,488),(24,28,32));draw=ImageDraw.Draw(out);draw.fontmode='1'
labels=['Original painted colors','Dim room: no fill','Dim room + actual lamp fill']
for i,im in enumerate(caps):
 c=im.crop((560,350,720,582)).resize((320,464),Image.Resampling.NEAREST);out.paste(c,(i*320,24));draw.text((i*320+8,7),labels[i],fill='white')
out.save(w/'lighting-comparison-2x.png')
result={'passed':True,'ui_checks':len(meta['checks']),'frames':rows,'projections':projections,'ui_unaffected_by_world_light':True,'lighting_character_sample_mean_Y8':dict(zip(files,means)),'source_RGBA_unchanged':True,'preview_crop':[560,350,720,582],'preview_zoom':2,'projection_check_limit':'Exact mathematical texel-boundary samples excluded because GPU/CPU tie rounding differs at fractional scale19/30; all other opaque samples and native1x pixels exact. No color error tolerance added.','normal_maps':False,'cast_shadow_occluders':False}
(ev/'render-audit.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
