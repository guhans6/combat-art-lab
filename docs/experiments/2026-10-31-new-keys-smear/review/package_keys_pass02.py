from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'));from native_read import read,composite
p=R/'source/structural-pass02.aseprite';a=read(p);names=[v['name'] for v in a['layers']];site=json.loads((R/'recipe/key-sites.json').read_text());keyorder=site['key_order']
matte='#343c49'
def tile(im,s=3):
 b=Image.new('RGBA',im.size,matte);b.alpha_composite(im);return b.resize((im.width*s,im.height*s),Image.Resampling.NEAREST).convert('RGB')
strip=Image.new('RGB',(256*3,230*2),matte);d=ImageDraw.Draw(strip)
for f in range(6):
 im=composite(a,f);exp=Image.open(R/f'proof/structural02-{f+1}.png').convert('RGBA');assert im.tobytes()==exp.tobytes()
 x=f%3*256;y=f//3*230;strip.paste(tile(im,1),(x,y+20));d.text((x+5,y+3),['original','reach','free hand','windup','extension','recovery'][f],fill='white')
 # Actual native owner isolate/hide evidence. Fixed crop retains cuff through bag bottom.
 crop=(65,35,230,150);w=(crop[2]-crop[0])*3;h=(crop[3]-crop[1])*3
 sheet=Image.new('RGB',(w*3,(h+23)*3),matte);dd=ImageDraw.Draw(sheet)
 items=[('composite',im)]
 for l in [1,2,3,4,5,6,7]:
  owner=a['cels'].get((f,l),{}).get('image',Image.new('RGBA',a['canvas']));items.append((names[l]+' alone',owner))
 # final tile hides all prop, next sheets below show each relevant owner hidden.
 for j,(label,pix) in enumerate(items):
  xx=j%3*w;yy=j//3*(h+23);sheet.paste(tile(pix.crop(crop)),(xx,yy+23));dd.text((xx+4,yy+4),label,fill='white')
 sheet.save(R/f'review/key-{f+1}-owners.png')
 hidden=Image.new('RGB',(w*3,(h+23)*2),matte);hd=ImageDraw.Draw(hidden)
 for j,l in enumerate([1,4,5,6,7]):
  z=Image.new('RGBA',a['canvas'])
  for k,m in enumerate(a['layers']):
   if k==l:continue
   if (f,k) in a['cels']:z.alpha_composite(a['cels'][(f,k)]['image'])
  xx=j%3*w;yy=j//3*(h+23);hidden.paste(tile(z.crop(crop)),(xx,yy+23));hd.text((xx+4,yy+4),'hide '+names[l],fill='white')
 hidden.save(R/f'review/key-{f+1}-hidden.png')
 if f:
  g=im.copy();gd=ImageDraw.Draw(g)
  ss=site['sites'][str(keyorder[f])]
  for n,pt in ss.items():
   x,y=pt;gd.ellipse((x-1,y-1,x+1,y+1),fill='#ff75a3' if n[0]=='N' else '#75e7ff');gd.text((x+2,y-4),n,fill='white')
  for pt in [(128,193),tuple(site['source_registration'][str(f+1)]['pelvis'])]:
   x,y=pt;gd.line((x-3,y,x+3,y),fill='#ffcf67');gd.line((x,y-3,x,y+3),fill='#ffcf67')
  tile(g,3).save(R/f'review/key-{f+1}-guides.png')
strip.resize((1536,920),Image.Resampling.NEAREST).save(R/'review/structural02-keys-2x.png')
(R/'review/structural02-packet.json').write_text(json.dumps({'native':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'native_export_equal':True,'files':{str(x.relative_to(R)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (R/'review').glob('key-*.png')}},indent=2))
print('packaged actual native owner/composite/hidden/site evidence;6 exports exact')
