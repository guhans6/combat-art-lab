from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,hashlib
P=Path('/private/tmp/atmospheric-breathing-proxy-r02');K=P/'keys';sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(P/'baseline.aseprite');B=read(K/'amplitude-keys.aseprite');data=json.load(open(P/'correction-ops.json'));layers=data['layers'];mask=Image.open(P/'editable-upperbody-frozen.png')
def comp(a,f,omit=None):
 im=Image.new('RGBA',(96,160))
 for l,n in enumerate(layers):
  if n!=omit:im.alpha_composite(a['cels'][f,l]['image'])
 return im
def matte(im,c):
 out=Image.new('RGBA',im.size,c);out.alpha_composite(im);return out
changed=[]
for k,c in A['cels'].items():
 b=B['cels'][k];pts=[(i%96,i//96)for i,(x,y)in enumerate(zip(c['image'].getdata(),b['image'].getdata()))if x!=y]
 if pts:
  assert k[0]==5 and layers[k[1]]in data['moving'];assert all(mask.getpixel(p)for p in pts);changed.append({'frame':6,'owner':layers[k[1]],'pixels':len(pts)})
for f,n in[(0,'rest'),(1,'open'),(5,'apex')]:
 assert comp(B,f).tobytes()==Image.open(K/f'{n}.png').convert('RGBA').tobytes()
 for owner in['head-hair-face','neck-collar','thorax-coat','near-upper-sleeve','near-forearm-hand']:
  comp(B,f,owner).save(K/f'{n}-hide-{owner}.png')
sheet=Image.new('RGB',(6*192,345),'#74797c');dr=ImageDraw.Draw(sheet)
for j,(f,n)in enumerate([(0,'rest'),(1,'open'),(5,'apex')]):
 for v,a in enumerate([A,B]):
  x=(2*j+v)*192;sheet.paste(matte(comp(a,f),'#74797c').resize((192,320),Image.Resampling.NEAREST).convert('RGB'),(x,25));dr.text((x+4,5),f'{n} '+['r01','r02'][v],fill='white')
sheet.save(K/'before-after-2x.png')
sheet=Image.new('RGB',(6*144,315),'#555960');dr=ImageDraw.Draw(sheet)
for j,(f,n)in enumerate([(0,'rest'),(1,'open'),(5,'apex')]):
 for v,a in enumerate([A,B]):
  x=(2*j+v)*144;sheet.paste(matte(comp(a,f),'#d0c7b4').crop((25,4,73,100)).resize((144,288),Image.Resampling.NEAREST).convert('RGB'),(x,25));dr.text((x+4,5),f'{n} '+['r01','r02'][v],fill='white')
sheet.save(K/'upper-before-after-3x.png')
sheet=Image.new('RGB',(6*120,180),'#74797c');dr=ImageDraw.Draw(sheet)
for j,(f,n)in enumerate([(0,'rest'),(1,'open'),(5,'apex')]):
 for v,a in enumerate([A,B]):
  x=(2*j+v)*120;sheet.paste(matte(comp(a,f),'#74797c').resize((90,149),Image.Resampling.NEAREST).convert('RGB'),(x+15,25));dr.text((x+3,5),n+' '+['r01','r02'][v],fill='white')
sheet.save(K/'before-after-fixed128rest.png')
for a,ver in[(A,'r01'),(B,'r02')]:
 f=5;im=comp(a,f);sheet=Image.new('RGB',(5*144,3*332),'#555960');dr=ImageDraw.Draw(sheet)
 for j,n in enumerate(['head-hair-face','neck-collar','thorax-coat','near-upper-sleeve','near-forearm-hand']):
  for r,v in enumerate([im,a['cels'][f,layers.index(n)]['image'],comp(a,f,n)]):
   sheet.paste(matte(v,'#96968e').crop((24,4,72,108)).resize((144,312),Image.Resampling.NEAREST).convert('RGB'),(j*144,r*332+20));dr.text((j*144+2,r*332+2),n if r==0 else['','isolated','hidden'][r],fill='white')
 sheet.save(K/f'apex-{ver}-ownership.png')
out={'changed_native':changed,'allfixedowners_unchanged':True,'actual_MCP_key_exports_exact':True,'changed_pixels_inside_frozenmask':True,'palette_timing_header_layers_unchanged':A['header']==B['header']and A['frames']==B['frames']and A['layers']==B['layers'],'candidate_sha256':hashlib.sha256((K/'amplitude-keys.aseprite').read_bytes()).hexdigest()};assert out['palette_timing_header_layers_unchanged'];json.dump(out,open(K/'checks.json','w'),indent=2);print(json.dumps(out))
