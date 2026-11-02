from PIL import Image,ImageDraw,ImageChops,ImageSequence
from pathlib import Path
from collections import Counter
p=Path('/private/tmp/idle-r04-diagnosis'); b=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning'); fs=[Image.open(b/f'assets/export/atmospheric-traveler/idle-r03/frames/idle-0{i}.png').convert('RGBA') for i in range(4)]
canvas=Image.new('RGB',(4*384,700),'#777777'); d=ImageDraw.Draw(canvas)
for i,im in enumerate(fs):
 bg=Image.new('RGBA',im.size,'#777777');bg.alpha_composite(im);canvas.paste(bg.convert('RGB').resize((384,640),Image.Resampling.NEAREST),(i*384,30));d.text((i*384+5,5),f'frame {i}',fill='white')
canvas.save(p/'r03-frames.png')
a,b1=fs[0],fs[1]
diff=ImageChops.difference(a,b1);print('r03 changed by bands',[(y0,y1,sum(1 for y in range(y0,y1) for x in range(96) if a.getpixel((x,y))!=b1.getpixel((x,y)))) for y0,y1 in [(0,82),(82,100),(100,118),(118,136),(136,160)]])
for y in range(95,137,5):
 print('row',y,[(min(xs),max(xs),len(xs)) if (xs:=[x for x in range(96) if im.getpixel((x,y))[3]]) else None for im in (a,b1)])
for n in ['hero2-1','hero-2']:
 im=Image.open(Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning/docs/research/idle-animation-references-2026-11-02')/(n+'.gif')); print(n,im.size,im.n_frames,[im.seek(i) or im.info.get('duration') for i in range(im.n_frames)])
im=Image.open('/private/tmp/idle-reference-study-r03/saint11-character-idle.gif');print('saint',im.size,im.n_frames,Counter([im.seek(i) or im.info.get('duration') for i in range(im.n_frames)]))
# enlarged overlays and source pants comparisons
sheet=Image.new('RGB',(1152,640),'#777777'); dr=ImageDraw.Draw(sheet)
for i,key in enumerate(['0','1','2']):
 for j,part in enumerate(['near-leg-pants','far-leg-pants']):
  im=Image.open(f'/private/tmp/atmospheric-idle-sample-r03/drawing-data/{key}/{part}.png').convert('RGBA');bg=Image.new('RGBA',im.size,'#777777');bg.alpha_composite(im);sheet.paste(bg.convert('RGB').resize((192,320),Image.Resampling.NEAREST),(i*384+j*192,20));dr.text((i*384+j*192,0),key+' '+part,fill='white')
 near=Image.open(f'/private/tmp/atmospheric-idle-sample-r03/drawing-data/{key}/composite-drawing-data.png').convert('RGBA');bg=Image.new('RGBA',near.size,'#777777');bg.alpha_composite(near);sheet.paste(bg.convert('RGB').resize((192,320),Image.Resampling.NEAREST),(i*384,320))
sheet.save(p/'pants-owners.png')
