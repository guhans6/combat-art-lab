from PIL import Image,ImageDraw
from pathlib import Path
import json,hashlib
K=Path('/private/tmp/stealth-fighter-idle-r01/keys');names=['rest','transition','apex'];parts=['body-occlusion-backing','upper-torso','near-arm','head-hair-neck']
def matte(im,c):b=Image.new('RGBA',im.size,c);b.alpha_composite(im);return b
for scale in [1,3]:
 sheet=Image.new('RGBA',(128*scale*3,264*scale+30),(55,59,65));d=ImageDraw.Draw(sheet)
 for i,n in enumerate(names):
  im=Image.open(K/('repaired-'+n+'.png'));sheet.alpha_composite(im.resize((128*scale,264*scale),Image.Resampling.NEAREST),(128*scale*i,26));d.text((128*scale*i+6,6),n,fill='white')
 sheet.convert('RGB').save(K/f'repaired-keys-{scale}x.png')
sheet=Image.new('RGB',(60*5*3,120*5+28),'#f03ab8');d=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
 im=Image.open(K/('repaired-'+n+'.png')).crop((28,36,88,156));sheet.paste(matte(im,'#f03ab8').resize((300,600),Image.Resampling.NEAREST).convert('RGB'),(i*300,28));d.text((i*300+5,7),n,fill='black')
sheet.save(K/'repaired-contrast-keys-5x.png')
sheet=Image.new('RGB',(300*3,600*4+28),'#697078');d=ImageDraw.Draw(sheet)
for row,p in enumerate(parts):
 for col,name in enumerate(['repaired-apex','apex-owner-'+p,'apex-hide-'+p]):
  im=Image.open(K/(name+'.png')).crop((28,36,88,156));sheet.paste(matte(im,'#697078').resize((300,600),Image.Resampling.NEAREST).convert('RGB'),(col*300,row*600+28));d.text((col*300+5,row*600+7),name,fill='white')
sheet.save(K/'actual-native-ownership-hide-5x.png')
checks={}
for n in names:
 im=Image.open(K/('repaired-'+n+'.png')).convert('RGBA');a=im.getchannel('A');s={(x,y) for y in range(264) for x in range(128) if not a.getpixel((x,y))};holes=[]
 while s:
  q=[s.pop()];edge=False
  for x,y in q:
   edge|=x in (0,127) or y in (0,263)
   for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if p in s:s.remove(p);q.append(p)
  if not edge:holes.append(q)
 checks[n]={'holes':holes,'alpha':sorted(set(a.getdata()))}
 assert not holes
 base=Image.open(K/'repaired-rest.png').convert('RGBA');assert base.crop((0,153,128,264)).tobytes()==im.crop((0,153,128,264)).tobytes()
checks['lower_y153_exact']=True;checks['native_sha256']=hashlib.sha256((K/'structural-keys-repaired.aseprite').read_bytes()).hexdigest();json.dump(checks,open(K/'repaired-checks.json','w'),indent=2)
