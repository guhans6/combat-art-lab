from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];I=R/'inputs';ref=Image.open(I/'character-closeup.png').convert('RGBA');B=Image.open(I/'baseline.png').convert('RGBA');C=Image.open(R/'passes/pass-02-reopen.png').convert('RGBA');rp=ref.crop((520,170,820,470)).resize((30,30),Image.Resampling.LANCZOS)
for s in [1,8,12]:
 panels=[('Approved ref preview',rp),('Unchanged baseline',B.crop((50,10,80,40))),('Pass02 review candidate',C.crop((50,10,80,40)))];cw=max(170,30*s+20);out=Image.new('RGB',(cw*3,30*s+80),'#303238');d=ImageDraw.Draw(out)
 for i,(label,im) in enumerate(panels):
  d.text((i*cw+8,8),label,fill='white');m=Image.new('RGBA',im.size,'#303238');m.alpha_composite(im);out.paste(m.resize((30*s,30*s),Image.Resampling.NEAREST),(i*cw+(cw-30*s)//2,40))
 d.text((8,out.height-22),'Ref resampled for review only; sprites at exact native / integer nearest-neighbor scale.',fill='white');out.save(R/'reviews'/f'final-head-{s}x.png')
