from tools.check_native_pilot import read
from PIL import Image,ImageDraw
from pathlib import Path
p=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol/proof');a=read('docs/experiments/2026-10-30-natural-idle-sol/pass01.aseprite')
im=Image.new('RGBA',(128,192))
for l in range(1,12): im.alpha_composite(a['cels'][(0,l)]['image'])
bg=Image.new('RGBA',im.size,(210,215,220,255));bg.alpha_composite(im)
out=bg.crop((35,32,91,76)).resize((560,440),Image.Resampling.NEAREST);d=ImageDraw.Draw(out)
for x in range(35,91,5):d.text(((x-35)*10,0),str(x),fill='red')
for y in range(35,76,5):d.text((0,(y-32)*10),str(y),fill='red')
out.save(p/'coordinate-crop.png')
