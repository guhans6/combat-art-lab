exec(open(__file__.replace('repair_coverage.py','build_pass01.py')).read().split('calls=[]')[0])
from native_read import composite,holes
now=read(R/'source/attack-repaired.aseprite');neutral=composite(now,0);calls=[];record=[]
for f in [2,8,10,12]:
 im=composite(now,f-1);pts=[]
 if f in [2,12]:
  pts=[(x,y) for y in range(165,185) for x in range(100,170) if not im.getpixel((x,y))[3] and neutral.getpixel((x,y))[3]]
  pts += [(x,y) for x,y in holes(im) if 115<=x<=126 and 67<=y<=73]
 elif f==8:pts=[(133,90)]
 else:pts=[(x,y) for x,y in holes(im) if 140<=x<=155 and 85<=y<=150]
 for name in ['01-leg-base-and-shoes','02-jacket-shirt-and-sleeves']:
  selected=[p for p in pts if (p[1]>=90)==name.startswith('01')]
  if not selected:continue
  ops=[]
  for x,y in selected:
   if f in [2,12] and neutral.getpixel((x,y))[3]:c=neutral.getpixel((x,y))
   else:
    near=[(dx*dx+dy*dy,im.getpixel((x+dx,y+dy))) for dx in range(-3,4) for dy in range(-3,4) if (lambda c:c[3] and c[2]>c[1]>c[0])(im.getpixel((x+dx,y+dy)))]
    c=min(near,key=lambda a:a[0])[1] if near else (94,122,168,255)
   ops.append(dict(kind='grid',x=x,y=y,rows=['C'],legend={'C':'#%02x%02x%02x'%c[:3]}));record.append(dict(frame=f,xy=[x,y],rgba=c))
  calls.append(dict(frame=f,layer=name,label='Restore inspected shoe and denim alpha gaps',ops=ops))
(R/'operations/coverage-repair.json').write_text(json.dumps(calls));(R/'review/coverage-repair-pixels.json').write_text(json.dumps(record,indent=2));print('Coverage pixels',len(record))
