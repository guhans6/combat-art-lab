from PIL import Image
from pathlib import Path
import json
K=Path('/private/tmp/stealth-fighter-idle-r01/keys')
# Enumerated inspected newly exposed attachment surfaces. No imagewide alpha fill.
chest=[(x,63) for x in range(62,72)]
armpit=[(51,63),(52,63),(51,74),(50,79),(49,82),(48,83),(47,84),(46,85),(45,86),(44,87)]
waist=[(51,99),(50,101),(49,103)]
forearm=[(50,113),(49,119),(48,125)]
hand=[(43,147),(44,147),(45,148),(46,148),(47,148),(48,149),(49,150),(50,151),(51,151),(52,151),(53,151)]
pts=chest+armpit+waist+forearm+hand;im=Image.new('RGBA',(128,264))
for p in pts:im.putpixel(p,(40,47,63,255) if p in chest else (24,24,26,255))
im.save(K/'body-occlusion-backing.png');b=im.getbbox();x0,y0,x1,y1=b
ops=[{'kind':'grid','x':x0,'y':y0,'rows':[''.join('I' if im.getpixel((x,y))==(40,47,63,255) else 'D' if im.getpixel((x,y))[3] else '.' for x in range(x0,x1)) for y in range(y0,y1)],'legend':{'I':'#282f3f','D':'#18181a'}}]
json.dump({'ops':ops,'points':{'chest':chest,'armpit':armpit,'waist':waist,'forearm':forearm,'hand':hand},'meaning':'inferred same-surface backing exposed behind lifted near arm / shoulder; chest y63 rest indigo continuity'},open(K/'repair-backing-ops.json','w'),indent=2)
