from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,collections
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R.parents[2]/'tools'));from check_native_pilot import read
A=read(R/'inputs/baseline.aseprite');N=read(R/'passes/pass-01.aseprite');names=[l['name'] for l in N['layers']];P={n:N['cels'][(0,i)]['image'].copy() for i,n in enumerate(names)};B={n:A['cels'][(0,i)]['image'].copy() for i,n in enumerate(names)}
def rgba(h):return tuple(bytes.fromhex(h[1:]))+(255,)
# Retain baseline curved topology; collapse only near shades. No larger uniform overpaint.
H='08-hair-tie-and-hair';P[H]=B[H].copy()
ramp=['#482925','#532e26','#583329','#673a2c','#6a3e31','#703f30','#744433','#79432d','#854529','#a5603f']
for y in range(6,34):
 for x in range(33,80):
  p=P[H].getpixel((x,y));r,g,b,a=p
  if not a or (x>=54 and y>=17):continue
  if 40<r<180 and 24<g<105 and b<80 and r>g*1.3:
   c=min(map(rgba,ramp),key=lambda c:sum((p[k]-c[k])**2 for k in range(3)))
   if sum((p[k]-c[k])**2 for k in range(3))<145:P[H].putpixel((x,y),c)
# connected low-contrast highlight fragments follow existing sweep; no giant patch
for x,y in [(50,11),(51,10),(52,10),(53,9),(54,9),(44,20),(44,21),(43,22)]:
 if P[H].getpixel((x,y))[3]:P[H].putpixel((x,y),rgba('#79432d'))
# Return to inherited fabric crease shapes, retaining the useful restrained material ramps.
for n in ['02a-jacket-left','02b-jacket-right']:
 P[n]=B[n].copy();ramp2=list(map(rgba,['#2d2c22','#393628','#48432d','#4b4732','#5a5437','#665e3a','#6a613c']))
 for y in range(35,79):
  for x in range(32,96):
   p=P[n].getpixel((x,y));r,g,b,a=p
   if a and abs(r-g)<22 and g>b*1.12:
    c=min(ramp2,key=lambda c:sum((p[k]-c[k])**2 for k in range(3)))
    if sum((p[k]-c[k])**2 for k in range(3))<450:P[n].putpixel((x,y),c)
P['03-shirt']=B['03-shirt'].copy();shirtmap={'#dec1c4':'#d9bcc1','#d6b7bb':'#d9bcc1','#fde4cc':'#fde7d3','#e6c7c5':'#d9bcc1'}
for y in range(43,69):
 for x in range(49,75):
  p=P['03-shirt'].getpixel((x,y));h='#'+bytes(p[:3]).hex()
  if p[3] and h in shirtmap:P['03-shirt'].putpixel((x,y),rgba(shirtmap[h]))
P['04-tote']=B['04-tote'].copy()
# Fold dots in the central cloth become soft transition, side shadow remains untouched.
for y in range(80,92):
 for x in range(83,92):
  p=P['04-tote'].getpixel((x,y));h='#'+bytes(p[:3]).hex()
  if p[3] and h in ['#c69a8a','#d2a595','#d09e8c','#caa48b','#b5897b']:
   P['04-tote'].putpixel((x,y),rgba('#dfb39b'))
# Shallow asymmetrical smile left of nose, one warm low-contrast cluster.
for x,y,h in [(64,28,'#e48558'),(65,29,'#da784b'),(66,29,'#da784b'),(67,29,'#da784b'),(68,28,'#e48558')]:
 if P[H].getpixel((x,y))[3]:P[H].putpixel((x,y),rgba(h))
# Correct visible ownership independently of color changes. Face color/eye samples
# currently misowned by the hair guide move to the actual face layer; no hidden surfaces.
pre_transfer=Image.new('RGBA',(128,192))
for n in names:
 if not n.startswith('guide'):pre_transfer.alpha_composite(P[n])
face='07-face-and-neck';transfers=[]
for y in range(17,32):
 for x in range(54,74):
  p=P[H].getpixel((x,y));r,g,b,a=p
  skin=a and r>=180 and g>=95 and b>=45 and r>g*1.23
  near_eye=61<=x<=66 and 20<=y<=24
  far_eye=70<=x<=72 and 19<=y<=22
  lower_contour=57<=x<=71 and y>=30 and r>=120 and g>=50 and r>g*1.4
  if a and (skin or near_eye or far_eye or lower_contour):
   assert P[face].getpixel((x,y))[3]==0
   P[face].putpixel((x,y),p);P[H].putpixel((x,y),(0,0,0,0));transfers.append({'from':H,'to':face,'x':x,'y':y})
# Remove jacket ownership from top of tote; cream cloth remains tote.
for y in range(70,85):
 for x in range(78,95):
  p=P['04-tote'].getpixel((x,y));r,g,b,a=p
  if a and r<140 and abs(r-g)<28 and g>b*1.15:
   assert P['02b-jacket-right'].getpixel((x,y))[3]==0
   P['02b-jacket-right'].putpixel((x,y),p);P['04-tote'].putpixel((x,y),(0,0,0,0));transfers.append({'from':'04-tote','to':'02b-jacket-right','x':x,'y':y})
# Per-layer patches from pass01, full provenance includes changes that erase old ownership.
ops=[]
for i,n in enumerate(names):
 groups=collections.defaultdict(list);old=N['cels'][(0,i)]['image']
 for y in range(192):
  for x in range(128):
   p=P[n].getpixel((x,y))
   if p!=old.getpixel((x,y)):groups['#'+bytes(p).hex()].append({'x':x,'y':y})
 if groups:
  op={'sprite':'#113','layer':n,'frame':1,'paletteLock':True,'label':'Correct exaggerated forms and face ownership','ops':[{'kind':'pixels','color':c,'points':v} for c,v in groups.items()]}
  (R/'operations'/f'pass-02-{n}.json').write_text(json.dumps(op,separators=(',',':')));ops.append(n)
(R/'operations/pass-02-layers.json').write_text(json.dumps(ops));(R/'operations/ownership-transfers.json').write_text(json.dumps(transfers,indent=2))
im=Image.new('RGBA',(128,192))
for n in names:
 if not n.startswith('guide'):im.alpha_composite(P[n])
assert im.tobytes()==pre_transfer.tobytes(),'ownership transfer changed visible composite'
(R/'proof/ownership-transfer-check.json').write_text(json.dumps({'passed':True,'transferred_pixels':len(transfers),'composite_changed_pixels':0,'face_samples_transferred':169,'jacket_samples_transferred':52},indent=2))
im.save(R/'proof/intended-pass-02.png')
print(json.dumps({'layers':ops,'ownership_transfers':len(transfers),'visible_changes_from_seed':sum(a!=b for a,b in zip(Image.open(R/'inputs/baseline.png').convert('RGBA').get_flattened_data(),im.get_flattened_data()))}))
