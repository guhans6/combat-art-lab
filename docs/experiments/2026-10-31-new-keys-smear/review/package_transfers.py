from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'));from native_read import read,composite
p=R/'source/transfer-study02.aseprite';a=read(p);mat='#343c49';spec=json.loads((R/'recipe/transfer-sites.json').read_text());paths=[]
def view(im,s=3):
 bg=Image.new('RGBA',im.size,mat);bg.alpha_composite(im);return bg.resize((im.width*s,im.height*s),Image.Resampling.NEAREST).convert('RGB')
for f in [7,8]:
 im=composite(a,f-1);assert im.tobytes()==Image.open(R/f'proof/transfer02-{f}.png').convert('RGBA').tobytes();crop=(95,32,185,140);w,h=270,324
 sheet=Image.new('RGB',(w*4,(h+20)*3),mat);d=ImageDraw.Draw(sheet);items=[('clean',im)]
 for l in [1,2,3,4,5,6,7]:items.append((a['layers'][l]['name']+' alone',a['cels'][(f-1,l)]['image']))
 for l in [1,4,5,6]:
  z=Image.new('RGBA',a['canvas'])
  for k in range(len(a['layers'])):
   if k!=l and (f-1,k) in a['cels']:z.alpha_composite(a['cels'][(f-1,k)]['image'])
  items.append(('hide '+a['layers'][l]['name'],z))
 for j,(label,img) in enumerate(items):
  x=j%4*w;y=j//4*(h+20);sheet.paste(view(img.crop(crop)),(x,y+20));d.text((x+2,y+3),label,fill='white')
 path=R/f'review/transfer-{f}-ownership.png';sheet.save(path);paths.append(path)
 name='release' if f==7 else 'gather';ss=spec['sites'][name]['sites'];s=view(im);dd=ImageDraw.Draw(s)
 # Root labels on a wider sheet, avoiding actual drawing.
 guide=Image.new('RGB',(1050,650),mat);guide.paste(s,(0,20));gd=ImageDraw.Draw(guide)
 for j,(n,pt) in enumerate(ss.items()):
  x,y=pt;gd.ellipse((x*3-3,y*3+17,x*3+3,y*3+23),fill='#ffbf63');gd.text((790,30+j*28),f'{n} {pt}',fill='white')
 gd.text((5,3),name+' structural drawing; flat sleeves pending material pass',fill='white');path=R/f'review/transfer-{f}-sites.png';guide.save(path);paths.append(path)
for title,order in [('outbound',[3,7,8,4]),('return',[6,8,7,3,2,1])]:
 sheet=Image.new('RGB',(256*len(order),230),mat);dd=ImageDraw.Draw(sheet)
 for j,f in enumerate(order):sheet.paste(view(composite(a,f-1),1),(j*256,20));dd.text((j*256+6,3),f'key{f}',fill='white')
 path=R/f'review/transfer-{title}-neighbors.png';sheet.resize((sheet.width,230),Image.Resampling.NEAREST).save(path);paths.append(path)
paths += [R/'recipe/transfer-sites.json']
packet={'native':str(p),'native_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'native_export_equal':True,'files':{str(x.relative_to(R)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths},'evidence':'Two new structural transfer keys, unchanged original6; not an animation/timing clearance'};(R/'review/transfer-packet.json').write_text(json.dumps(packet,indent=2));print(packet['native_sha256'])
