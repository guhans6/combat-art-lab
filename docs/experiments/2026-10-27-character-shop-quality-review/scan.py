from PIL import Image
from pathlib import Path
import json,sys
sys.path.insert(0,"/Users/guhan/Guhan/Projects/combat-art-lab/tools/pixel-art-director/scripts")
from pixel_checks import check_alpha_coverage
def components(im):
 w,h=im.size;p=im.convert("RGBA");pix=p.load();active={(x,y) for y in range(h) for x in range(w) if pix[x,y][3]};seen=set();out=[]
 for start in sorted(active,key=lambda p:(p[1],p[0])):
  if start in seen:continue
  todo=[start];seen.add(start);cells=[]
  while todo:
   x,y=todo.pop();cells.append((x,y))
   for dx in (-1,0,1):
    for dy in (-1,0,1):
     n=(x+dx,y+dy)
     if n in active and n not in seen:seen.add(n);todo.append(n)
  out.append({"size":len(cells),"bbox":[min(x for x,y in cells),min(y for x,y in cells),max(x for x,y in cells)+1,max(y for x,y in cells)+1],"pixels":cells if len(cells)<8 else None})
 return sorted(out,key=lambda c:-c["size"])
root=Path("/Users/guhan/Guhan/Projects/combat-art-lab")
layout=json.loads((root/"godot/standing-idle-lab/textures/idle-layout.json").read_text())
files=[root/"godot/standing-idle-lab"/layout["frame_directory"].removeprefix("res://")/f"frame-{i:02}.png" for i in range(8)]
files+=sorted((root/"assets/export/shop-modular-v01").glob("*.png"))
result=[]
for path in files:
 im=Image.open(path).convert("RGBA")
 result.append({"path":str(path.relative_to(root)),"size":im.size,"partial_alpha":sum(0<p[3]<255 for p in im.get_flattened_data()),"alpha":check_alpha_coverage(im),"opaque_components":components(im)})
print(json.dumps(result))
