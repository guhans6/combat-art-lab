from PIL import Image,ImageDraw
from pathlib import Path
O=Path('/private/tmp/fighter-user-variants-r01/native-work')
for i in ['01','03','04']:
 im=Image.open(O/f'preparation/source-grid-{i}.png').convert('RGB');print(i)
 for y in range(43,253,3):
  lo,hi=(65,83) if y<97 else ((73,89) if y>170 and y<240 else (80,100))
  if 97<=y<=170:continue
  supp=[]
  for x in range(lo,hi):
   r,g,b=im.getpixel((x,y))
   if (r-b>=(-3 if i=='01' else -4) and r>=19) or (b>=31 and r>=24):supp.append(x)
  print(f'{y}:{max(supp) if supp else None}',end=' ')
 print()
