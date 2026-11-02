from pathlib import Path
from PIL import Image,ImageDraw
p=Path('/private/tmp/stealth-fighter-idle-r02/keys');out=Path('/private/tmp/fighter-r02-lead');files=[p/f'key-{i}.png' for i in range(3)]
ims=[Image.open(f).convert('RGBA') for f in files];sheet=Image.new('RGB',(128*3*3,264*3+24),(55,60,67));d=ImageDraw.Draw(sheet);d.fontmode='1'
for i,im in enumerate(ims):
 a=Image.new('RGBA',im.size,(55,60,67,255));a.alpha_composite(im);sheet.paste(a.convert('RGB').resize((384,792),Image.Resampling.NEAREST),(i*384,24));d.text((i*384+8,6),str(files[i]),fill='white')
sheet.save(out/'keys-3x.png')
