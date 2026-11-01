"""Anatomical and prop correction inputs. No native or asset raster writes."""
exec(open(__file__.replace('build_pass02.py','build_pass01.py')).read().split('calls=[]')[0])
from PIL import ImageDraw
from native_read import composite
base=[composite(src,f) for f in range(13)]
# Native coordinates read against coordinate-labelled exports. Color is only
# a discriminator inside reviewed prop regions, never a global deletion key.
polys={
2:[(143,44),(151,45),(154,68),(171,79),(182,96),(184,122),(155,123),(147,86),(144,66)],
3:[(165,88),(235,86),(236,137),(181,139),(164,101)],
4:[(45,88),(109,82),(111,99),(86,145),(45,145)],
5:[(159,85),(230,83),(230,135),(173,136),(158,98)],
6:[(205,49),(272,45),(274,96),(216,98),(203,75)],
7:[(212,48),(286,46),(286,95),(217,96)],
8:[(187,99),(249,105),(250,154),(192,154),(182,109)],
9:[(160,92),(174,90),(210,117),(209,147),(159,147),(157,112)],
10:[(146,82),(159,81),(195,107),(195,137),(144,137)],
11:[(163,47),(174,45),(176,70),(190,88),(191,119),(167,120),(164,85)],
12:[(154,48),(165,46),(168,74),(189,87),(190,111),(163,114),(157,83)]}
grips={2:(150,76),3:(164,94),4:(110,94),5:(158,91),6:(204,69),7:(211,68),8:(186,102),9:(168,91),10:(155,80),11:(166,52),12:(160,73)}
backing={2:[(137,77),(149,84),(163,117),(174,145),(177,165),(154,168),(135,111)],8:[(167,99),(190,100),(205,160),(175,160)],9:[(149,84),(176,88),(183,122),(189,158),(190,168),(165,169),(150,112)],10:[(149,84),(176,88),(183,122),(189,158),(190,168),(165,169),(150,112)],11:[(145,74),(159,77),(179,134),(157,134)],12:[(145,78),(163,80),(182,134),(155,134)]}
# Skull/face/neck from exact neutral. Offsets follow the neck, not bounding boxes.
head_offsets={2:(0,0),3:(-5,8),4:(12,5),5:(-10,5),6:(12,3),7:(15,5),8:(9,10),9:(12,0),10:(12,0),11:(9,0),12:(10,3)}
# Neck offsets are inspected during the key checkpoint; no facial redraw.
def poly(points):
 m=Image.new('L',(320,192));ImageDraw.Draw(m).polygon(points,fill=255);return m

def fy(y):
 for (a,b),(c,d) in zip(K,K[1:]):
  if a<=y<c:return b+(y-a)*(d-b)/(c-a)
 return y

def propmask(f,im):
 m=poly(polys[f]);p=m.load()
 for y in range(192):
  for x in range(320):
   r,g,b,a=im.getpixel((x,y))
   allowed=a and r>g+4 and r>b+3
   # Hands occlude straps/body; keep actual wrist/fingers in the body.
   if f==2 and 143<=x<=170 and 49<=y<=80:allowed=False
   if f==11 and 170<=x<=183 and 74<=y<=95:allowed=False
   if f==12 and 152<=x<=177 and 65<=y<=79:allowed=False
   if not allowed:p[x,y]=0
 return m
calls=[];manifest=[]
for f in range(2,13):
 im=base[f-1];m=propmask(f,im);bag=Image.new('RGBA',(320,192));body=im.copy();bp=body.load();mp=m.load();gp=bag.load()
 for y in range(192):
  for x in range(320):
   if mp[x,y]:gp[x,y]=bp[x,y];bp[x,y]=(0,0,0,0)
 if f in backing:
  bm=poly(backing[f]);p=bm.load()
  for y in range(192):
   for x in range(320):
    if mp[x,y] and p[x,y]:
     choices=[im.getpixel((u,y)) for u in range(x-1,max(70,x-32),-1) if not mp[u,y] and (lambda c:c[3] and c[2]>c[0]*1.25 and c[2]>c[1])(im.getpixel((u,y)))]
     bp[x,y]=(94,122,168,255) if x < (174 if f in (9,10) else 154) else (88,114,158,255)
 # Reconstruct occluded thigh silhouette behind surviving source clusters.
 if f in backing:
  support=Image.new('RGBA',(320,192));ImageDraw.Draw(support).polygon(backing[f],fill=(88,114,158,255));support.alpha_composite(body);body=support
 body=mapped(body)
 # Re-register the bag as a physical form about its grip; uniform native scale.
 gx,gy=grips[f];tx=128+(gx-128)*.78;ty=fy(gy)
 newbag=Image.new('RGBA',(320,192));p=newbag.load()
 for y in range(192):
  for x in range(320):
   u=round(gx+(x-tx)/.78);v=round(gy+(y-ty)/.78)
   if 0<=u<320 and 0<=v<192:p[x,y]=bag.getpixel((u,v))
 dx,dy=head_offsets[f];cut=35+dy
 # Replace the skull as a connected source-supported part, leaving the action collar.
 ImageDraw.Draw(body).rectangle((0,0,319,cut-1),fill=(0,0,0,0))
 head=Image.new('RGBA',(320,192));head.alpha_composite(base[0].crop((0,0,320,35)),(dx,dy))
 # Same named source owners retained, but repaired cels now have explicit part roles.
 lower=body.copy();ImageDraw.Draw(lower).rectangle((0,0,319,89),fill=(0,0,0,0))
 upper=body.copy();ImageDraw.Draw(upper).rectangle((0,90,319,191),fill=(0,0,0,0))
 parts={0:lower,1:upper,3:head,4:newbag}
 for l,meta in enumerate(src['layers']):
  part=parts.get(l,Image.new('RGBA',(320,192)))
  calls.append(dict(frame=f,layer=meta['name'],createCel=True,label=f'P02 connected body and tote F{f}',ops=[dict(kind='clear')]+grid(part)))
 manifest.append(dict(frame=f,head_offset=[dx,dy],bag_mask_polygon=polys[f],source_grip=grips[f],target_grip=[tx,ty],bag_scale=.78,backing_polygon=backing.get(f)))
(R/'operations/pass02-provenance.json').write_text(json.dumps(manifest,indent=2))
for f in range(2,13):(R/'operations'/f'pass02-f{f:02}.json').write_text(json.dumps([c for c in calls if c['frame']==f],ensure_ascii=False))
print('Prepared',len(calls),'MCP grids; native render still required')
