from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];I=R/'inputs';P=R/'passes';O=R/'reviews'
scene=Image.open(I/'character-scene.png').convert('RGBA').crop((464,228,769,1023)).resize((72,184),Image.Resampling.LANCZOS)
ref=Image.new('RGBA',(128,192));ref.alpha_composite(scene,(32,5))
close=Image.open(I/'character-closeup.png').convert('RGBA').crop((392,124,789,400)).resize((48,34),Image.Resampling.LANCZOS)
imgs=[('reference preview',ref),('raw seed',Image.open(I/'seed.png')),('best prior = seed',Image.open(I/'baseline.png')),('new pass01',Image.open(P/'pass-01-reopen.png'))]
def sheet(images,scale,path):
 w=sum(i.width*scale+12 for n,i in images);h=max(i.height*scale for n,i in images)+36
 out=Image.new('RGBA',(w,h),'#34363a');d=ImageDraw.Draw(out);x=0
 for n,i in images:
  d.text((x+3,5),n,fill='white');out.alpha_composite(i.convert('RGBA').resize((i.width*scale,i.height*scale),Image.Resampling.NEAREST),(x+3,28));x+=i.width*scale+12
 out.convert('RGB').save(path)
for s in [1,4]:sheet(imgs,s,O/f'fullbody-{s}x-reference-seed-best-new.png')
box=(32,5,85,39);heads=[('ref preview',close)]+[(n,i.crop(box)) for n,i in imgs[1:]]
for s in [1,12]:sheet(heads,s,O/f'head-{s}x-reference-seed-best-new.png')
a=Image.open(I/'baseline.png').convert('RGBA');b=Image.open(P/'pass-01-reopen.png').convert('RGBA');intended=Image.open(R/'proof/intended-pass-01.png').convert('RGBA')
assert a.size==b.size==(128,192)
assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes()
assert intended.tobytes()==b.tobytes(),'unexpected native/export difference'
assert (P/'pass-01.png').read_bytes()==(P/'pass-01-reopen.png').read_bytes()
print('PASS native export equals authored plan; reopen PNG byte equal; alpha unchanged')
