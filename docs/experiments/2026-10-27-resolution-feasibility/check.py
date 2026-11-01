from PIL import Image,ImageDraw
from pathlib import Path
import hashlib
p=Path(__file__).parent
baseline=Image.open(p/'baseline.png').convert('RGBA').crop((24,0,104,88))
studies=[Image.open(p/f'study-{n}.png').convert('RGBA') for n in (192,256)]
ims=[baseline,*studies]
for n,im in zip((192,256),studies):
 reopened=Image.open(p/f'study-{n}-reopen.png').convert('RGBA');edit=Image.open(p/f'study-{n}-edit-proof.png').convert('RGBA')
 assert im.size == ((120,132) if n == 192 else (160,176))
 assert reopened.size == edit.size == im.size
 assert list(im.get_flattened_data())==list(reopened.get_flattened_data())
 assert sum(a!=b for a,b in zip(im.get_flattened_data(),edit.get_flattened_data()))==1
 assert im.getpixel((0,0))[3]==0
 print(n,im.size,'reopen exact, edit one pixel, transparent corner',len(set(im.get_flattened_data())))
for im,scale,name in zip(ims,(4,4,4),('baseline-crop','study-192','study-256')):
 im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST).save(p/f'{name}-4x.png')
canvas=Image.new('RGB',(1480,570),'#30303e');draw=ImageDraw.Draw(canvas)
for idx,(im,scale,label) in enumerate(zip(ims,(6,4,3),('v04 baseline crop: 80x88, 6x','192-equivalent: 120x132, 4x','256-equivalent: 160x176, 3x'))):
 x=idx*490+5;draw.text((x,8),label,fill='white');canvas.paste(im.resize((480,528),Image.Resampling.NEAREST),(x,34),im.resize((480,528),Image.Resampling.NEAREST))
canvas.save(p/'matched-display.png')
for file in sorted(p.glob('*.aseprite')):print(hashlib.sha256(file.read_bytes()).hexdigest(),file.name)
