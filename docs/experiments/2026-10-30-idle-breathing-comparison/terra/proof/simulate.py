from tools.check_native_pilot import read
from PIL import Image
from pathlib import Path
base=Path('docs/experiments/2026-10-30-idle-breath-blink/luna/passes/pass01/luna6-idle-breath-blink-pass01.aseprite')
x=read(base); out=Path('docs/experiments/2026-10-30-idle-breathing-comparison/terra/proof')
# Simulated deformation for exploration only; actual artwork must be edited via MCP.
for stage in (0,1,2):
 layers=[x['cels'][(0,i)]['image'].copy() for i in range(12)]
 if stage:
  for i,box,dx in [(3,(35,39,50,62),-1),(4,(77,39,91,62),1),(5,(54,46,65,69),0)]:
   src=layers[i].copy(); dst=layers[i]; pix=src.load(); op=dst.load(); x0,y0,x1,y1=box
   for y in range(y0,y1):
    for xx in range(x0,x1):
     # Fade deformation toward the waist; shift shoulder/chest up and gently outward.
     dy=stage if y<56 else (1 if y<63 else 0)
     shift=dx if y<56 else 0
     sx,sy=xx-shift,y+dy
     if x0<=sx<x1 and y0<=sy<y1 and pix[sx,sy][3]:op[xx,y]=pix[sx,sy]
 im=Image.new('RGBA',(128,192),(48,50,57,255))
 for layer in layers[1:]:im.alpha_composite(layer)
 im.crop((25,25,100,100)).resize((600,600),Image.Resampling.NEAREST).save(out/f'simulation-{stage}.png')
