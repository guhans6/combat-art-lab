exec(open(__file__.replace('clarify_arrest_grip.py','build_pass01.py')).read().split('calls=[]')[0])
from PIL import ImageDraw
now=read(R/'source/attack-repaired.aseprite');names={v['name']:i for i,v in enumerate(now['layers'])}
im=Image.new('RGBA',(320,192));d=ImageDraw.Draw(im)
# Far wrist grips the upper gathered handle; lower palm is separately occluded.
d.polygon([(166,75),(170,75),(173,80),(176,81),(178,83),(177,86),(175,88),(172,87),(170,84),(168,81)],fill='#90472c')
d.polygon([(167,76),(169,76),(172,81),(175,82),(176,83),(176,85),(175,86),(173,85),(171,82),(169,80)],fill='#fda977')
d.line([(168,77),(170,80),(173,82)],fill='#fcaf80',width=2)
d.line([(174,83),(176,84),(175,85)],fill='#ea9368')
# Near forearm from left cuff, grasping the lower portion of the same bundle.
d.polygon([(160,83),(165,85),(169,88),(172,89),(175,90),(178,92),(177,95),(174,97),(171,96),(169,93),(164,91),(160,88)],fill='#90472c')
d.polygon([(161,84),(165,86),(169,89),(172,90),(175,91),(176,93),(175,95),(173,95),(171,94),(170,92),(164,90),(161,87)],fill='#fda977')
d.polygon([(161,84),(165,86),(169,89),(168,91),(164,89),(161,86)],fill='#fcaf80')
d.line([(173,92),(176,93),(175,94)],fill='#90472c')
d.line([(172,94),(174,95)],fill='#ea9368')
strap=now['cels'][7,names['06-continuous-handle-tension']]['image'].copy();sd=ImageDraw.Draw(strap)
sd.line([(175,85),(174,96)],fill='#795246',width=3);sd.line([(175,85),(174,96)],fill='#dfb39b',width=1)
calls=[dict(frame=8,layer=name,createCel=True,label='F8 separate upper and lower grip with exposed handle between',ops=[dict(kind='clear')]+grid(part)) for name,part in [('05-loaded-grip-drawing',im),('06-continuous-handle-tension',strap)]]
(R/'operations/arrest-grip-clarity.json').write_text(json.dumps(calls,ensure_ascii=False))
