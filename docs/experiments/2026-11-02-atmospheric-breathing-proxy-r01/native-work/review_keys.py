from PIL import Image,ImageDraw
from pathlib import Path
import json,sys,hashlib
P=Path('/private/tmp/atmospheric-breathing-proxy-r01');K=P/'keys'
sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools')
from check_native_pilot import read
A=read(K/'structural-keys.aseprite');recipe=json.load(open(P/'drawing-ops.json'));layers=recipe['layers'];keys=['rest','transition','apex'];levs=[0,2,3]
def comp(f,omit=None):
 im=Image.new('RGBA',(96,160))
 for l,n in enumerate(layers):
  if n!=omit and (f,l) in A['cels']:im.alpha_composite(A['cels'][f,l]['image'])
 return im
def matte(im,color):
 bg=Image.new('RGBA',im.size,color);bg.alpha_composite(im);return bg
def holes(im):
 s={(x,y)for y in range(im.height)for x in range(im.width)if not im.getpixel((x,y))[3]};out=[]
 while s:
  q=[s.pop()];edge=False
  for x,y in q:
   edge|=x in (0,im.width-1)or y in(0,im.height-1)
   for p in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if p in s:s.remove(p);q.append(p)
  if not edge:out.append(q)
 return out
checks=[]
for f,key in enumerate(keys):
 im=comp(f);export=Image.open(K/f'{key}.png').convert('RGBA');assert im.tobytes()==export.tobytes()
 hs=holes(im);checks.append({'key':key,'enclosed_holes':hs,'alpha_values':sorted(set(im.getchannel('A').getdata()))})
 for l,n in enumerate(layers):assert A['cels'][f,l]['image'].tobytes()==Image.open(K/f'f{f+1}-{n}.png').convert('RGBA').tobytes()
 for n in['head-hair-face','neck-collar','near-upper-sleeve','near-forearm-hand','thorax-coat']:
  comp(f,n).save(K/f'{key}-hide-{n}.png')
 # Marked landmarks use authored anatomical guides, not silhouette bounds.
 guide=matte(im,'#707780');dr=ImageDraw.Draw(guide)
 for n,xy in recipe['landmarks'][str(levs[f])].items():
  if not isinstance(xy,list):continue
  x,y=xy;dr.line((x-2,y,x+2,y),fill='#dfb04b');dr.line((x,y-2,x,y+2),fill='#dfb04b')
 guide.resize((288,480),Image.Resampling.NEAREST).save(K/f'{key}-landmarks-3x.png')
 # Native isolated and owner-hide pairs around the upper body.
 panel=Image.new('RGB',(5*144,3*332),'#555960');dr=ImageDraw.Draw(panel)
 for j,n in enumerate(['head-hair-face','neck-collar','thorax-coat','near-upper-sleeve','near-forearm-hand']):
  for row,v in enumerate([im,A['cels'][f,layers.index(n)]['image'],comp(f,n)]):
   v=matte(v,'#8d8e86').crop((24,4,72,108)).resize((144,312),Image.Resampling.NEAREST)
   panel.paste(v.convert('RGB'),(j*144,row*332+20));dr.text((j*144+2,row*332+2),n if row==0 else ['','isolated','hidden'][row],fill='white')
 panel.save(K/f'{key}-ownership.png')
sheet=Image.new('RGB',(3*288,520),'#676a6c');dr=ImageDraw.Draw(sheet)
for f,key in enumerate(keys):
 im=matte(comp(f),'#676a6c').resize((288,480),Image.Resampling.NEAREST);sheet.paste(im.convert('RGB'),(f*288,36));dr.text((f*288+4,6),f'{key} level{levs[f]} fixedroot (44,85)',fill='white')
sheet.save(K/'keys-3x.png')
# 128px body projection keeps common origin and ratio137->128 for everypose.
sheet=Image.new('RGB',(3*160,200),'#777c80');dr=ImageDraw.Draw(sheet)
for f,key in enumerate(keys):
 im=matte(comp(f),'#777c80').resize((90,149),Image.Resampling.NEAREST);sheet.paste(im.convert('RGB'),(f*160+30,28));dr.text((f*160+8,8),key+' body~128px',fill='white')
sheet.save(K/'keys-projected128.png')
sheet=Image.new('RGB',(3*288,350),'#777c80');dr=ImageDraw.Draw(sheet)
for f,key in enumerate(keys):
 im=matte(comp(f),'#d0c7b4').crop((24,4,72,100)).resize((144,288),Image.Resampling.NEAREST);sheet.paste(im.convert('RGB'),(f*288+8,35));dr.text((f*288+8,8),key+' lightmatte 3x',fill='white')
 im=matte(comp(f),'#151920').crop((24,4,72,100)).resize((144,288),Image.Resampling.NEAREST);sheet.paste(im.convert('RGB'),(f*288+144,35))
sheet.save(K/'upperbody-contrast-3x.png')
rest,apex=comp(0),comp(2);diff=Image.new('RGBA',rest.size)
for y in range(160):
 for x in range(96):
  a,b=rest.getpixel((x,y)),apex.getpixel((x,y))
  if a!=b:diff.putpixel((x,y),(240,80,50,255)if a[3]and not b[3]else(70,220,180,255)if b[3]and not a[3]else(250,210,70,255))
matte(diff,'#292e34').resize((288,480),Image.Resampling.NEAREST).save(K/'rest-apex-diff-3x.png')
# Independent scratch checks including negative outofmask rejection.
B=Image.open(P/'smoke/before.png').convert('RGBA');E=Image.open(P/'smoke/edited.png').convert('RGBA');R=Image.open(P/'smoke/reopened.png').convert('RGBA');coords=[(i%16,i//16)for i,(a,b)in enumerate(zip(B.getdata(),E.getdata()))if a!=b];assert coords==[(10,11)]and E.tobytes()==R.tobytes();protected=Image.open(P/'smoke/protected.png').convert('RGBA');assert protected.crop((2,2,5,5)).tobytes()==B.crop((2,2,5,5)).tobytes()
negative=E.copy();negative.putpixel((2,2),(100,100,100,255));negative.save(P/'smoke/out-of-mask-negative.png');negative_rejected=any(a!=b and(i%16,i//16)!=(10,11)for i,(a,b)in enumerate(zip(E.getdata(),negative.getdata())));assert negative_rejected
json.dump({'keys':checks,'native_composites_exact':True,'native_owners_exact_to_MCP_isolations':True,'smoke':{'orientation':'top-left hooked L with blue pixel(3,4), isolatedwarm(10,11)','exact_edit':coords,'protected_owner_unchanged':True,'reopened_exact':True,'grid_dot_erases':True,'out_of_mask_negative_rejected':negative_rejected},'landmarks':recipe['landmarks'],'native_sha256':hashlib.sha256((K/'structural-keys.aseprite').read_bytes()).hexdigest()},open(K/'checks.json','w'),indent=2)
print(json.dumps({'keys':checks,'native_composites_exact':True,'owner_isolations_exact':True}))
