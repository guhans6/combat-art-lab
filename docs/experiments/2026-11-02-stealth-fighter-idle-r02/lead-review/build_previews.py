from pathlib import Path
from PIL import Image,ImageDraw
import json,bisect
src=Path('/private/tmp/build-proxy-previews.py').read_text();exec(src[src.index('def encode('):src.index('checks={}')])
w=Path('/private/tmp/stealth-fighter-idle-r02/delivery');o=Path('/private/tmp/fighter-r02-lead');g=Path('/private/tmp/fighter-r02-godot-preview')
layout=json.loads((g/'layout.json').read_text());dur=layout['durations_ms'];ims=[Image.open(w/name).convert('RGBA')for name in layout['files']];bg=(36,40,45)
checks={'native':encode(ims,dur,o/'idle-exact-native.gif',True)}
neutral=[];context=[];full=[];gameplay=[]
for i,im in enumerate(ims):
 a=Image.new('RGBA',im.size,bg+(255,));a.alpha_composite(im);neutral.append(a.convert('RGB').resize((im.width*2,im.height*2),Image.Resampling.NEAREST))
 cap=Image.open(g/'evidence'/f'runtime-frame-{i:02}.png').convert('RGB');full.append(cap)
 c=cap.crop((90,35,280,326)).resize((380,582),Image.Resampling.NEAREST);out=Image.new('RGB',(380,604),bg);d=ImageDraw.Draw(out);d.fontmode='1';d.text((8,6),'Current A / connected idle / 2x scene crop',fill='white');out.paste(c,(0,22));context.append(out)
checks['preview2x']=encode(neutral,dur,o/'idle-2x.gif');checks['environment2x']=encode(context,dur,o/'idle-environment-2x.gif')
for cap in full:
 c=cap.crop((405,135,565,326)).resize((320,382),Image.Resampling.NEAREST);a=Image.new('RGB',(320,404),bg);d=ImageDraw.Draw(a);d.fontmode='1';d.text((8,6),'Current A / 128px body preview / 2x',fill='white');a.paste(c,(0,22));gameplay.append(a)
checks['gameplay128_2x']=encode(gameplay,dur,o/'idle-gameplay-128px-2x.gif')
contact=Image.new('RGB',(ims[0].width*2*len(ims),ims[0].height*2+24),bg);d=ImageDraw.Draw(contact);d.fontmode='1'
for i,im in enumerate(neutral):contact.paste(im,(i*im.width,24));d.text((i*im.width+8,6),f'F{i} / {dur[i]}ms',fill='white')
contact.save(o/'cycle-2x.png');checks['environment_crop']=[90,35,280,326];checks['caption']='Exact Godot pose captures reconstructed at authored timing; not continuous video.';(o/'preview-checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks))
