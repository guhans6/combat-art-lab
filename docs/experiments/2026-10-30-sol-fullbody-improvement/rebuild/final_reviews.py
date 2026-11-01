from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];I=R/'inputs';P=R/'passes';O=R/'reviews'
scene=Image.open(I/'character-scene.png').convert('RGBA').crop((464,228,769,1023)).resize((72,184),Image.Resampling.LANCZOS)
ref=Image.new('RGBA',(128,192));ref.alpha_composite(scene,(32,5))
close=Image.open(I/'character-closeup.png').convert('RGBA').crop((389,99,792,399)).resize((46,34),Image.Resampling.LANCZOS)
headref=Image.new('RGBA',(53,34));headref.alpha_composite(close,(3,0))
base=Image.open(I/'baseline.png').convert('RGBA');new=Image.open(P/'pass-02-reopen.png').convert('RGBA');box=(32,5,85,39)
def sheet(images,scale,path):
 w=sum(i.width*scale+12 for n,i in images);h=max(i.height*scale for n,i in images)+36
 out=Image.new('RGBA',(w,h),'#34363a');d=ImageDraw.Draw(out);x=0
 for n,i in images:
  d.text((x+3,5),n,fill='white');out.alpha_composite(i.resize((i.width*scale,i.height*scale),Image.Resampling.NEAREST),(x+3,28));x+=i.width*scale+12
 out.convert('RGB').save(path)
for s in [1,4]:sheet([('Reference preview',ref),('Before: seed = best prior',base),('New: pass02 review candidate',new)],s,O/f'final-fullbody-{s}x.png')
for s in [1,8]:sheet([('Reference preview',headref),('Before: seed = best prior',base.crop(box)),('New: pass02',new.crop(box))],s,O/f'final-head-{s}x.png')
sheet([('Selected candidate',new.crop(box)),('Proof-only smile shade edit',Image.open(R/'proof/face-edit-reopen.png').convert('RGBA').crop(box))],8,O/'face-edit-proof-8x.png')
# native ownership visual diagnostic; exact actual native cels.
import sys;sys.path.insert(0,str(R.parents[2]/'tools'));from check_native_pilot import read
n=read(P/'pass-02.aseprite')
for i,l in enumerate(n['layers']):
 if not l['flags']&1:continue
 im=n['cels'][(0,i)]['image'];im.save(R/'proof'/f'part-{l["name"]}.png')
sheet([(n['layers'][i]['name'],n['cels'][(0,i)]['image']) for i in [4,6,10,11]],2,O/'ownership-corrected-parts-2x.png')
# Prior exact bag expansion shown at same zoom with changed alpha highlighted.
a=Image.open(I/'rejected.png').convert('RGBA');b=base.copy();highlight=base.copy()
for y in range(192):
 for x in range(128):
  if a.getpixel((x,y))[3] and not base.getpixel((x,y))[3]:highlight.putpixel((x,y),(255,55,180,255))
sheet([('Seed edge',base.crop((77,70,99,103))),('Rejected extra contour',a.crop((77,70,99,103))),('Added alpha in magenta',highlight.crop((77,70,99,103)))],8,O/'prior-bag-line-evidence-8x.png')
