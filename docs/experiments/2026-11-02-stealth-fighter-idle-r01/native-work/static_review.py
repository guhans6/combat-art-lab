from PIL import Image,ImageDraw
from pathlib import Path
import json,hashlib
P=Path('/private/tmp/stealth-fighter-idle-r01/seed')
raw=Image.open(P/'raw-seed.png').convert('RGBA'); native=Image.open(P/'native-export.png').convert('RGBA');assert raw.tobytes()==native.tobytes()
source=Image.open(P/'source-masked.png').crop((300,88,732,1392));source.thumbnail((81,244),Image.Resampling.LANCZOS)
ref=Image.new('RGBA',raw.size);ref.alpha_composite(source,(24,10))
for sc in [1,3]:
 panelw=128*sc+20;h=264*sc+48;sheet=Image.new('RGBA',(panelw*3,h),(55,59,65,255));d=ImageDraw.Draw(sheet)
 for i,(name,im) in enumerate([('Original / preview resample',ref),('Raw seed / provisional grid',raw),('Actual native export',native)]):
  d.text((i*panelw+8,8),name,fill='white');sheet.alpha_composite(im.resize((128*sc,264*sc),Image.Resampling.NEAREST),(i*panelw+10,34))
 sheet.convert('RGB').save(P/f'source-seed-native-{sc}x.png')
parts=list(json.load(open(P/'native-draw-ops.json'))['layers'])
sheet=Image.new('RGBA',(6*256,264*2+40),(55,59,65,255));d=ImageDraw.Draw(sheet)
for i,n in enumerate(parts):
 im=Image.open(P/('native-owner-'+n+'.png'));sheet.alpha_composite(im.resize((256,528),Image.Resampling.NEAREST),(256*i,32));d.text((256*i+6,8),n,fill='white')
sheet.convert('RGB').save(P/'actual-owner-isolated-2x.png')
landmarks={'crown':(59,13),'chin':(70,41),'ear':(61,29),'neck-base':(63,46),'near-shoulder':(43,59),'far-shoulder':(74,60),'near-elbow':(37,96),'near-wrist':(45,130),'near-hand':(47,144),'pelvis':(66,124),'near-knee':(45,179),'far-knee':(74,177),'near-ankle':(36,234),'far-ankle':(68,233),'sole-line':(64,252),'sword-waist-root':(79,102)}
marked=Image.new('RGBA',raw.size,(55,59,65,255));marked.alpha_composite(native);m=marked.resize((512,1056),Image.Resampling.NEAREST);d=ImageDraw.Draw(m)
for n,(x,y) in landmarks.items():
 x*=4;y*=4;d.ellipse((x-3,y-3,x+3,y+3),fill='#ffbb44');d.text((x+5,y-4),n,fill='#ffdd99')
m.save(P/'landmarks-4x.png');json.dump(landmarks,open(P/'landmarks.json','w'),indent=2)
json.dump({'raw_native_pixel_exact':True,'native_size':native.size,'body_bounds':native.getbbox(),'visible_body_height':native.getbbox()[3]-native.getbbox()[1],'alpha_values':sorted(set(native.getchannel('A').getdata())),'visible_rgb_count':len({p[:3] for p in native.getdata() if p[3]}),'source_sha256':hashlib.sha256(Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/concepts/stealth-fighter/game-specific-r01/silver-pines/corrected.png').read_bytes()).hexdigest(),'native_sha256':hashlib.sha256((P/'static-seed.aseprite').read_bytes()).hexdigest()},open(P/'checks.json','w'),indent=2)
