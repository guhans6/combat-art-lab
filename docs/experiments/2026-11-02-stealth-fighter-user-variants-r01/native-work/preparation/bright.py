from PIL import Image,ImageEnhance,ImageDraw
from pathlib import Path
P=Path('/private/tmp/fighter-user-variants-r01/native-work/preparation')
for i in ['01','03','04']:
 im=Image.open(P/f'source-grid-{i}.png'); im=ImageEnhance.Brightness(im).enhance(3);im=im.resize((640,1320),Image.Resampling.NEAREST); d=ImageDraw.Draw(im)
 for x in range(0,128,5):d.text((x*5,0),str(x),fill='white')
 for y in range(0,264,5):d.text((0,y*5),str(y),fill='white'); d.line((20,y*5,640,y*5),fill=(70,70,70))
 im.save(P/f'bright-{i}.png')
