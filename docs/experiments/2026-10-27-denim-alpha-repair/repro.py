import sys,json
from PIL import Image
from collections import deque
p=sys.argv[1]
im=Image.open(p).convert('RGBA');w,h=im.size;a=im.getchannel('A');seen=set();holes=[]
for y in range(h):
 for x in range(w):
  if a.getpixel((x,y)) or (x,y) in seen:continue
  q=deque([(x,y)]);seen.add((x,y));cells=[];edge=False
  while q:
   xx,yy=q.popleft();cells.append((xx,yy));edge |= xx in (0,w-1) or yy in (0,h-1)
   for nx,ny in [(xx-1,yy),(xx+1,yy),(xx,yy-1),(xx,yy+1)]:
    if 0<=nx<w and 0<=ny<h and not a.getpixel((nx,ny)) and (nx,ny) not in seen:seen.add((nx,ny));q.append((nx,ny))
  if not edge and any((int(sys.argv[2]) if len(sys.argv)>2 else 0)<=yy<(int(sys.argv[3]) if len(sys.argv)>3 else h) for xx,yy in cells):holes.append(cells)
print(json.dumps({'file':p,'leg_holes':holes,'missing_pixels':sum(map(len,holes))}))
sys.exit(1 if holes else 0)
