from pathlib import Path
from PIL import Image
import json
R=Path(__file__).resolve().parent
ops=[]
def poly(ps,c,f):return dict(kind='polyline',points=[dict(x=x,y=y) for x,y in ps],closed=True,color=c,fill=f)
def ln(a,b,c,n=1):return dict(kind='line',**{'from':dict(x=a[0],y=a[1]),'to':dict(x=b[0],y=b[1])},color=c,thickness=n)
for f in [9,10]:
 a=[poly([(151,73),(176,73),(172,81),(165,87),(157,80)],'#48432d','#524c34'),poly([(157,74),(168,74),(165,80),(160,79)],'#665e3a','#665e3a')]
 ops.append(dict(frame=f,layer='04a-underarm-and-waist-backing',createCel=True,label='cloth backing beneath folded elbows',ops=a))
 # Restore corresponding source denim planes under the changed occlusion, retaining
 # new skin/coat pixels. This sampled patch is preparation for native grid painting.
 im=Image.open(R/'review'/f'native-key-{f}-v01.png').convert('RGBA');src=Image.open(R/'preparation/frame-09-base.png').convert('RGBA');legend={};rev={};rows=[]
 for y in range(82,104):
  row=''
  for x in range(151,170):
   p=im.getpixel((x,y));s=src.getpixel((x,y+8))
   if p[:3] not in [(67,94,140),(53,79,128)] or s[2]<=s[0]*1.2:row+='.';continue
   color='#%02x%02x%02x'%s[:3]
   if color not in rev:k=chr(0x100+len(rev));rev[color]=k;legend[k]=color
   row+=rev[color]
  rows.append(row)
 ops.append(dict(frame=f,layer='05-loaded-grip-drawing',createCel=True,label='source-corresponding denim occlusion backing',ops=[dict(kind='grid',x=151,y=82,rows=rows,legend=legend,transparent='skip')]))
 if f==9:pairs=[((167,90),(161,110)),((172,89),(185,101))]
 else:pairs=[((155,84),(149,102)),((161,83),(174,98))]
 a=[]
 for p,q in pairs:
  a+=[ln(p,q,'#795246',4),ln((p[0],p[1]+1),(q[0],q[1]),'#dfb39b',2),ln((p[0]-1,p[1]+1),(q[0]-1,q[1]),'#f2cdb5')]
 ops.append(dict(frame=f,layer='06-continuous-handle-tension',createCel=True,label='two taut handles connect clasp to tote rim',ops=a))
(R/'operations/key-finish.json').write_text(json.dumps(ops,indent=2))
