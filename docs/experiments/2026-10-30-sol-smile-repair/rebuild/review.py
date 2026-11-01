from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
R=Path(__file__).resolve().parents[1]; name=sys.argv[1] if len(sys.argv)>1 else 'pass-01';B=Image.open(R/'inputs/baseline.png').convert('RGBA');C=Image.open(R/f'passes/{name}-reopen.png').convert('RGBA');ref=Image.open(R/'inputs/character-closeup.png').convert('RGBA');scene=Image.open(R/'inputs/character-scene.png').convert('RGBA')
def sheet(panels,s,path):
 w=sum(im.width*s+30 for label,im in panels);h=max(im.height*s for label,im in panels)+80
 out=Image.new('RGB',(w,h),'#303238');d=ImageDraw.Draw(out);x=10
 for label,im in panels:
  d.text((x,8),label,fill='white');p=Image.new('RGBA',im.size,'#303238');p.alpha_composite(im);out.paste(p.resize((im.width*s,im.height*s),Image.Resampling.NEAREST),(x,40));x+=im.width*s+30
 d.text((10,h-25),'Reference resampled for context only; candidate uses native pixels / integer NN zoom.',fill='white');out.save(path)
head=(50,10,80,40);refhead=ref.crop((570,210,770,410)).resize((30,30),Image.Resampling.LANCZOS)
fullref=scene.crop((464,228,769,1023)).resize((72,184),Image.Resampling.LANCZOS)
r=Image.new('RGBA',(128,192));r.alpha_composite(fullref,(32,5))
for s in [1,8,12]:sheet([('Approved ref preview',refhead),('Exact baseline',B.crop(head)),(name,C.crop(head))],s,R/'reviews'/f'{name}-head-{s}x.png')
for s in [1,4]:sheet([('Approved ref preview',r),('Exact baseline',B),(name,C)],s,R/'reviews'/f'{name}-fullbody-{s}x.png')
# Direct source mouth at integer zoom alongside native features; no fractional sprite scaling.
sheet([('Approved source crop 1x',ref.crop((650,305,740,365))),('Baseline 8x',B.crop((60,22,74,32)).resize((112,80),Image.Resampling.NEAREST)),(name+' 8x',C.crop((60,22,74,32)).resize((112,80),Image.Resampling.NEAREST))],1,R/'reviews'/f'{name}-mouth-direct.png')
