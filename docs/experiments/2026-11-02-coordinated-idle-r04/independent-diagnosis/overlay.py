from PIL import Image,ImageDraw
from pathlib import Path
p=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/export/atmospheric-traveler/idle-r03/frames')
a=[Image.open(p/f'idle-0{i}.png').convert('RGBA') for i in range(4)]
out=Image.new('RGB',(96*4*3,160*4),(80,80,80))
for i,(m,n) in enumerate([(0,1),(1,2),(2,3)]):
 im=Image.new('RGB',(96,160),(80,80,80));pix=im.load()
 for y in range(160):
  for x in range(96):
   u,v=a[m].getpixel((x,y)),a[n].getpixel((x,y))
   if u==v and u[3]:pix[x,y]=tuple(int(c*.5) for c in u[:3])
   elif u!=v:pix[x,y]=(255,100,40) if u[3] and not v[3] else ((30,220,255) if v[3] and not u[3] else (255,220,30))
 out.paste(im.resize((384,640),Image.Resampling.NEAREST),(384*i,0))
out.save('/private/tmp/idle-r04-diagnosis/diffs.png')
