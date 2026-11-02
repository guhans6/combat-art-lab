from pathlib import Path
from PIL import Image
import numpy as np,json,shutil
O=Path('/private/tmp/fighter-user-variants-r01/native-work')
# Retain every initial preparation artifact before bounded quality repair.
for i in ['01','03','04','05']:
 D=O/f'variant-{i}'; S=D/'pass00-mediancut';S.mkdir(exist_ok=True)
 for p in list(D.iterdir()):
  if p.is_file() and p.suffix!='.aseprite' and not (S/p.name).exists():shutil.copy2(p,S/p.name)
# Allocation of palette entries by perceptual error, with no dither/no RGB invention.
# Deterministic weighted farthest-point initialization + 24 Lloyd rounds, each center replaced
# by the nearest ACTUAL source pixel medoid. This preserves source RGBs and source materials.
for group in [['01'],['03','05'],['04']]:
 imgs={i:Image.open(O/f'variant-{i}/raw-unquantized.png').convert('RGBA') for i in group}
 for i,im in imgs.items():
  # Independent reviewer traced two falsely erased U03/U05 hair openings into actual hair.
  if i in ['01','03','04','05']:
   source=Image.open(O/f'preparation/source-grid-{i}.png').convert('RGBA');mask=Image.open(O/f'variant-{i}/source-spatial-mask-native.png').convert('L');r=json.loads((O/f'variant-{i}/recipe.json').read_text());from PIL import ImageDraw
   d=ImageDraw.Draw(mask)
   for p in r['hair_negative_spaces']:d.polygon(p,fill=255)
   if i=='04':
    for y,runs in {39:[(37,43)],40:[(36,43)],41:[(35,36),(40,43)],42:[(35,35),(39,43)],43:[(35,35),(39,43)],44:[(39,43)],45:[(39,43)]}.items():
     for x0,x1 in runs:d.line((x0,y,x1,y),fill=255)
   im=source.copy();im.putalpha(mask);im.putdata([p if p[3] else (0,0,0,0) for p in im.getdata()]);imgs[i]=im;mask.save(O/f'variant-{i}/source-spatial-mask-native.png');im.save(O/f'variant-{i}/raw-unquantized.png');r['hair_negative_spaces']=[];r['cleanup']='pass01: perceptual source medoid palette + reviewer-backed restoration of incorrectly erased rear hair';(O/f'variant-{i}/recipe.json').write_text(json.dumps(r,indent=2))
 vals=np.array([p[:3] for im in imgs.values() for p in im.getdata() if p[3]],dtype=np.float64);colors,counts=np.unique(vals,axis=0,return_counts=True)
 centers=[colors[np.argmax(counts)]];dist=np.full(len(colors),np.inf)
 for k in range(1,64):
  dist=np.minimum(dist,((colors-centers[-1])**2).sum(axis=1));centers.append(colors[np.argmax(dist*counts**0.45)])
 centers=np.array(centers)
 for z in range(24):
  distances=((colors[:,None,:]-centers[None,:,:])**2).sum(axis=2);labels=distances.argmin(axis=1);new=centers.copy()
  for k in range(64):
   use=labels==k
   if use.any():
    mean=np.average(colors[use],axis=0,weights=counts[use]); ix=np.where(use)[0];new[k]=colors[ix[np.argmin(((colors[use]-mean)**2).sum(axis=1))]]
  if np.array_equal(centers,new):break
  centers=new
 for i,im in imgs.items():
  out=Image.new('RGBA',im.size);a=np.array(im);rgb=a[:,:,:3].reshape(-1,3).astype(float);nearest=((rgb[:,None,:]-centers[None,:,:])**2).sum(axis=2).argmin(axis=1);a[:,:,:3]=centers[nearest].reshape(264,128,3).astype('uint8');a[a[:,:,3]==0]=0;out=Image.fromarray(a);out.save(O/f'variant-{i}/raw-seed.png')
  (O/f'variant-{i}/repaired-palette.json').write_text(json.dumps(['#%02x%02x%02x'%tuple(c.astype(int)) for c in centers],indent=2))
print('Repaired palette and source-backed U03/U05 hair retained; regenerate semantic draw ops next')
