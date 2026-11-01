"""Hand-authored final grip, strap, hip and return corrections; MCP draw inputs."""
exec(open(__file__.replace('finish_pass03.py','build_pass01.py')).read().split('calls=[]')[0])
from PIL import ImageDraw
now=read(R/'source/attack-pass03.aseprite')
calls=[]
def send(f,l,im,label):
 calls.append(dict(frame=f,layer=now['layers'][l]['name'],createCel=True,label=label,ops=[dict(kind='clear')]+grid(im)))
# Fill the newly exposed upper hip under the lifted jacket, behind retained cloth.
for f,shape in [(2,[(126,68),(139,69),(149,99),(137,101)]),(12,[(126,67),(136,68),(145,98),(135,101)])]:
 support=Image.new('RGBA',(320,192));d=ImageDraw.Draw(support);d.polygon(shape,fill='#6884b1');d.line([shape[1],shape[2]],fill='#58729e',width=2)
 for l in [0,1]:
  p=support.copy();ImageDraw.Draw(p).rectangle((0,0 if l==0 else 90,319,89 if l==0 else 191),fill=(0,0,0,0));p.alpha_composite(now['cels'][f-1,l]['image']);send(f,l,p,'P03 upper hip backing under lifted jacket')
 bag=now['cels'][f-1,4]['image'];out=Image.new('RGBA',(320,192));p=out.load()
 for y in range(192):
  # Shoulder stays fixed; tote body lowers and turns toward its carried side.
  sy=y if f==2 or y<41 else (41+(y-41)*19/25 if y<66 else 60+(y-66)*30/35)
  for x in range(320):
   sx=150+(x-150)/(.8 if f==2 else .75)
   if 0<=round(sx)<320 and 0<=round(sy)<192:p[x,y]=bag.getpixel((round(sx),round(sy)))
 send(f,4,out,'P03 carried tote transition perspective')
# Both hands wrap a shared handle bundle. Straps are separately behind fingers.
L='#fcaf80';S='#fda977';M='#ea9368';D='#90472c';BD='#795246';BM='#dfb39b';BL='#f2cdb5'
for f,ox,oy,left,right in [(8,14,16,(184,109),(195,100)),(9,0,0,(153,96),(173,90)),(10,-10,-9,(143,87),(160,83))]:
 hand=Image.new('RGBA',(320,192));d=ImageDraw.Draw(hand)
 def polygon(points,fill):d.polygon([(x+ox,y+oy) for x,y in points],fill=fill)
 def line(points,fill,width=1):d.line([(x+ox,y+oy) for x,y in points],fill=fill,width=width)
 if f==8:
  d.polygon([(168,82),(173,82),(177,88),(177,94),(173,97),(169,93),(167,87)],fill=D)
  d.polygon([(169,83),(173,84),(175,89),(175,93),(173,95),(170,92),(169,87)],fill=S)
  d.line([(170,84),(172,85),(174,90)],fill=L,width=2)
 # Near palm comes from left wrist; far hand folds over the bundle from above-right.
 polygon([(153,72),(158,74),(161,72),(164,73),(166,76),(165,79),(162,82),(158,82),(154,79)],D)
 polygon([(154,73),(158,75),(161,73),(163,74),(164,76),(163,78),(161,80),(158,80),(155,78)],S)
 polygon([(154,73),(157,74),(159,76),(158,78),(155,76)],L)
 line([(161,74),(163,75),(163,77)],M)
 line([(158,77),(162,78),(163,77)],D)
 line([(158,79),(161,80),(163,78)],M)
 line([(160,74),(161,75),(160,76)],L)
 # Clear obsolete strap fan above the rim, preserving the actual bag body.
 bag=now['cels'][f-1,4]['image'].copy();bp=bag.load()
 lx,ly=left;rx,ry=right
 for y in range(192):
  for x in range(320):
   rim=ly+(x-lx)*(ry-ly)/(rx-lx)
   if y<rim and y>=72+oy:bp[x,y]=(0,0,0,0)
 straps=Image.new('RGBA',(320,192));sd=ImageDraw.Draw(straps)
 anchors=[((159+ox,80+oy),left),((161+ox,80+oy),right),((160+ox,80+oy),(left[0]+2,left[1]-1)),((162+ox,80+oy),(right[0]-2,right[1]+1))]
 for start,end in anchors:sd.line([start,end],fill=BD,width=3)
 for start,end in anchors:sd.line([start,end],fill=BM,width=1)
 sd.line([(159+ox,81+oy),left],fill=BL,width=1)
 sd.line([left,right],fill=BD,width=1)
 send(f,4,bag,'P03 remove obsolete handle fan above rim')
 send(f,5,hand,'P03 two hands with fingers over shared bundle')
 send(f,6,straps,'P03 continuous handle loops under fingers')
for f in [2,8,9,10,12]:(R/'operations'/f'finish-f{f:02}.json').write_text(json.dumps([c for c in calls if c['frame']==f],ensure_ascii=False))
print('Prepared',len(calls),'finishing batches')
