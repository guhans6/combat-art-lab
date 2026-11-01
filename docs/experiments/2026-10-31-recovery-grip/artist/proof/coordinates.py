from pathlib import Path
from PIL import Image,ImageDraw
R=Path('docs/experiments/2026-10-31-recovery-grip/artist')
im=Image.open(R/'proof/recovery-grip-pass01.png').convert('RGBA');S=20;x0,y0,x1,y1=158,76,194,112
out=Image.new('RGB',((x1-x0)*S+40,(y1-y0)*S+40),'#363844');d=ImageDraw.Draw(out)
for y in range(y0,y1):
 for x in range(x0,x1):
  p=im.getpixel((x,y));X=40+(x-x0)*S;Y=40+(y-y0)*S
  if p[3]:d.rectangle((X,Y,X+S-1,Y+S-1),fill=p[:3])
  d.rectangle((X,Y,X+S-1,Y+S-1),outline='#444444')
for x in range(x0,x1):d.text((40+(x-x0)*S,15),str(x),fill='white')
for y in range(y0,y1):d.text((3,40+(y-y0)*S),str(y),fill='white')
out.save(R/'proof/pass01-coordinate-view.png')
