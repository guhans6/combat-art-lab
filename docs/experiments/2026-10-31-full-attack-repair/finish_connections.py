"""Final frame-specific ownership cleanup, prepared as dedicated MCP grids."""
exec(open(__file__.replace('finish_connections.py','build_pass01.py')).read().split('calls=[]')[0])
from PIL import ImageDraw
now=read(R/'source/attack-candidate.aseprite');names={v['name']:i for i,v in enumerate(now['layers'])};calls=[]
def send(f,name,im):calls.append(dict(frame=f,layer=name,createCel=True,label='P03 frame-specific grip and strap continuity',ops=[dict(kind='clear')]+grid(im)))
# Remove the obsolete F8 knuckle drawing on its actual body owners.
for name in ['01-leg-base-and-shoes','02-jacket-shirt-and-sleeves']:
 im=now['cels'][7,names[name]]['image'].copy();p=im.load()
 for y in range(77,103):
  for x in range(165,182):
   r,g,b,a=p[x,y]
   if a and r>60 and r>g*1.3:
    p[x,y]=(94,122,168,255) if y>=84 and x<172 else ((82,76,52,255) if x<173 and y<90 else (0,0,0,0))
 send(8,name,im)
im=Image.new('RGBA',(320,192));d=ImageDraw.Draw(im)
d.polygon([(166,75),(171,76),(174,82),(176,85),(176,89),(173,91),(170,87),(168,82)],fill='#90472c')
d.polygon([(167,76),(170,77),(172,83),(174,86),(174,89),(172,88),(170,83)],fill='#fda977')
d.line([(168,77),(170,82),(173,86)],fill='#fcaf80',width=2)
d.polygon([(160,83),(165,85),(170,87),(173,87),(177,89),(179,92),(178,95),(175,97),(171,97),(168,94),(163,91),(160,88)],fill='#90472c')
d.polygon([(161,84),(165,86),(170,89),(173,88),(176,90),(177,92),(176,94),(174,95),(171,95),(169,93),(164,90),(161,87)],fill='#fda977')
d.polygon([(161,84),(165,86),(170,89),(169,91),(164,89),(161,86)],fill='#fcaf80')
d.line([(173,90),(176,91),(176,92)],fill='#ea9368')
d.line([(172,92),(175,93),(177,92)],fill='#90472c')
d.line([(172,94),(174,95),(176,94)],fill='#ea9368')
send(8,'05-loaded-grip-drawing',im)
# Continuous return loop: hand covers gathered handles; both edges reach rim.
for f,left,right,grip in [(12,(146,74),(158,74),(148,64)),(2,(145,73),(160,73),(150,65))]:
 name='06-continuous-handle-tension';im=now['cels'][f-1,names[name]]['image'].copy();d=ImageDraw.Draw(im)
 for endpoint in [left,right]:
  d.line([grip,endpoint],fill='#795246',width=3);d.line([grip,endpoint],fill='#dfb39b',width=1)
 send(f,name,im)
(R/'operations/connections.json').write_text(json.dumps(calls,ensure_ascii=False))
print(len(calls))
