from PIL import Image,ImageDraw
from pathlib import Path
O=Path('/private/tmp/fighter-user-variants-r01/native-work/preparation')
for i,b in [('01',(350,186,725,1448)),('03',(20,14,288,989)),('04',(360,102,710,1385)),('05',(20,14,288,989))]:
 im=Image.open(O.parent.parent/'inputs'/('user-'+i+'.png')).convert('RGBA'); crop=im.crop(b); w=round(crop.width*240/crop.height); sm=crop.resize((w,240),Image.Resampling.NEAREST);out=Image.new('RGBA',(128,264),(20,21,24,255));out.alpha_composite(sm,((128-w)//2,13));out.save(O/('source-grid-'+i+'.png'))
 big=out.resize((768,1584),Image.Resampling.NEAREST);d=ImageDraw.Draw(big)
 for x in range(0,128,5):d.line((x*6,0,x*6,1584),fill=(100,100,100));d.text((x*6,0),str(x),fill='white')
 for y in range(0,264,5):d.line((0,y*6,768,y*6),fill=(100,100,100));d.text((0,y*6),str(y),fill='white')
 big.save(O/('grid-'+i+'.png'))
