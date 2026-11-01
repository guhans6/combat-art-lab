from PIL import Image,ImageDraw
from pathlib import Path
import hashlib
p=Path(__file__).parent
baseline=Image.open(p/'baseline.png').convert('RGBA').crop((24,0,104,88))
ims=[baseline]+[Image.open(p/f'study-{n}-pass02.png').convert('RGBA') for n in (192,256)]
for n,im in zip((192,256),ims[1:]):
 reopened=Image.open(p/f'study-{n}-pass02-reopen.png').convert('RGBA');edit=Image.open(p/f'study-{n}-pass02-edit-proof.png').convert('RGBA')
 assert im.size == ((120,132) if n == 192 else (160,176))
 assert reopened.size == edit.size == im.size
 assert list(im.get_flattened_data())==list(reopened.get_flattened_data())
 assert sum(a!=b for a,b in zip(im.get_flattened_data(),edit.get_flattened_data()))==1
 assert im.getpixel((0,0))[3]==0
 print(n,im.size,'reopen exact, edit one pixel, transparent corner',hashlib.sha256((p/f'study-{n}-pass02.aseprite').read_bytes()).hexdigest())
 im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(p/f'study-{n}-pass02-4x.png')
canvas=Image.new('RGB',(1480,570),'#30303e');draw=ImageDraw.Draw(canvas)
for idx,(im,scale,label) in enumerate(zip(ims,(6,4,3),('v04 baseline crop 6x','192 equivalent pass 02 4x','256 equivalent pass 02 3x'))):
 x=idx*490+5;draw.text((x,8),label,fill='white');large=im.resize((480,528),Image.Resampling.NEAREST);canvas.paste(large,(x,34),large)
canvas.save(p/'matched-display-pass02.png')
