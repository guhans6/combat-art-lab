"""Authored cluster plan; existing-palette explicit shapes, clipped to visible owners.
No resampling, blur, silhouette expansion, or stochastic generation.
"""
from pathlib import Path
import sys,json,collections
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R.parents[2]/'tools'))
from check_native_pilot import read
N=read(R/'inputs/baseline.aseprite');B=Image.open(R/'inputs/baseline.png').convert('RGBA')
parts={l['name']:N['cels'][(0,i)]['image'].copy() for i,l in enumerate(N['layers'])}
original={n:i.copy() for n,i in parts.items()};notes=[]
def rgba(h):return tuple(bytes.fromhex(h.lstrip('#')))+(255,)
def poly(name,points,h,why,condition=None):
 mask=Image.new('1',B.size);ImageDraw.Draw(mask).polygon(points,fill=1)
 im=parts[name];count=0;c=rgba(h)
 for y in range(192):
  for x in range(128):
   p=im.getpixel((x,y))
   if mask.getpixel((x,y)) and p[3] and (condition is None or condition(p)):
    im.putpixel((x,y),c);count+=p!=c
 notes.append({'layer':name,'polygon':points,'color':h,'reason':why,'changed_at_step':count})
def line(name,points,h,why):
 m=Image.new('1',B.size);ImageDraw.Draw(m).line(points,fill=1,width=1)
 im=parts[name];c=rgba(h);count=0
 for y in range(192):
  for x in range(128):
   p=im.getpixel((x,y))
   if m.getpixel((x,y)) and p[3]:im.putpixel((x,y),c);count+=p!=c
 notes.append({'layer':name,'polyline':points,'color':h,'reason':why,'changed_at_step':count})
# Hair only, skin and defining eyes untouched. Sweep follows the canonical tied crown.
hair='08-hair-tie-and-hair'
poly(hair,[(48,11),(52,8),(61,7),(58,10),(53,13),(49,15),(47,14)],'#744433','Unify crown sweep into connected middle plane')
poly(hair,[(48,15),(51,13),(58,11),(54,15),(50,18),(47,19)],'#673a2c','Lower overlapping swept lock')
poly(hair,[(58,8),(65,7),(70,9),(67,10),(62,10)],'#79432d','Upper crown warm plane, no added strand outline')
poly(hair,[(40,16),(43,16),(44,19),(42,23),(39,25),(37,23),(38,19)],'#673a2c','Gather rear tied hair into a single bent mass')
poly(hair,[(38,20),(39,18),(41,18),(40,22),(38,24)],'#854529','Small bounded rim of tied mass')
poly(hair,[(44,22),(47,20),(48,24),(48,28),(44,29),(42,27)],'#482925','Continuous underside of tied hair')
poly(hair,[(55,16),(57,14),(60,13),(59,17),(57,20),(55,21)],'#673a2c','Join front fringe middle plane without moving openings')
# Jacket: coherent sleeve planes following bent elbow, retain selective contours and zipper.
for name in ['02a-jacket-left','02b-jacket-right']:
 im=parts[name]
 ramp=[rgba(h) for h in ['#2d2c22','#393628','#48432d','#4b4732','#5a5437','#665e3a','#6a613c']]
 for y in range(35,79):
  for x in range(32,96):
   p=im.getpixel((x,y));r,g,b,a=p
   if a and abs(r-g)<22 and g>b*1.12:
    c=min(ramp,key=lambda c:sum((p[k]-c[k])**2 for k in range(3)))
    if sum((p[k]-c[k])**2 for k in range(3))<450:im.putpixel((x,y),c)
 notes.append({'layer':name,'recipe':'existing-ramp nearest merge under squared RGB distance450; olive only','reason':'Join conversion microshades while preserving larger fold topology'})
poly('02a-jacket-left',[(37,56),(41,54),(44,55),(45,58),(40,58),(36,61),(34,61)],'#5a5437','Sleeve upper fold broad light plane')
poly('02a-jacket-left',[(35,63),(40,60),(44,61),(46,63),(41,63),(37,65),(34,65)],'#48432d','Bent elbow underside as a single wedge')
poly('02b-jacket-right',[(83,56),(87,54),(89,56),(91,58),(87,57),(84,59),(80,61)],'#5a5437','Upper forearm light plane')
poly('02b-jacket-right',[(82,63),(86,61),(91,62),(94,64),(91,65),(87,63),(82,65)],'#48432d','Quiet bent forearm shadow, avoid isolated vertical seams')
# Shirt: simplify a busy stair into a connected fabric fold, preserve neckline and hem.
poly('03-shirt',[(62,56),(65,55),(69,55),(68,57),(66,57),(68,60),(66,61),(63,58)],'#d9bcc1','Single tee diagonal fold plane')
poly('03-shirt',[(60,61),(64,62),(65,64),(63,64),(59,62)],'#fde7d3','Quiet light return below diagonal fold')
# Denim: keep silhouette, fly and weight bearing folds. Merge near duplicate midtones only.
im=parts['01-denim'];denim_map={'#5e7aa8':'#617caa','#60759e':'#58729e','#6581ae':'#617caa','#6884b1':'#617caa','#435e8c':'#445f90','#47618e':'#4a6594'}
for y in range(69,173):
 for x in range(39,98):
  p=im.getpixel((x,y));h='#'+bytes(p[:3]).hex()
  if p[3] and h in denim_map:im.putpixel((x,y),rgba(denim_map[h]))
notes.append({'layer':'01-denim','map':denim_map,'reason':'Resolve converted microshades into connected blue planes without adding creases'})
poly('01-denim',[(45,111),(47,116),(49,122),(52,129),(54,136),(54,141),(51,134),(48,127),(46,120)],'#4a6594','Reference broad left knee hanging fold, integrated interior plane')
poly('01-denim',[(73,121),(76,126),(80,131),(83,136),(86,140),(88,145),(84,141),(80,136),(76,131)],'#526d9a','Quiet transition along existing right shin diagonal')
# Tote: internal cloth planes only; outer alpha exactly fixed.
tote='04-tote'
poly(tote,[(84,81),(86,80),(88,83),(89,89),(91,94),(90,97),(88,94),(87,89),(85,86)],'#f8d2ae','Broad cloth light plane replaces scattered bag marks')
poly(tote,[(82,80),(83,79),(85,81),(85,85),(87,88),(87,92),(85,89),(84,85)],'#d2a595','Gathered fabric side fold connected to opening')
poly(tote,[(92,87),(94,89),(94,94),(91,98),(89,99),(91,94)],'#d2a595','Tote side turns into shadow using existing interior silhouette')
# Sneakers: coherent pale vamps and short laces, protected dark soles unchanged.
poly('00-shoes',[(36,175),(39,174),(44,175),(47,177),(44,178),(38,178),(35,177)],'#d9b3a7','Left shoe toe panel as a single material plane')
poly('00-shoes',[(87,176),(91,175),(95,177),(100,178),(99,180),(92,180),(89,178)],'#c49e91','Right shoe toe panel, retain sole and silhouette')
line('00-shoes',[(46,172),(48,173)],'#f2cdb5','Upper left lace bar')
line('00-shoes',[(44,174),(47,175)],'#f2cdb5','Lower left lace bar')
line('00-shoes',[(86,172),(88,173)],'#f2cdb5','Upper right lace bar')
line('00-shoes',[(85,174),(88,175)],'#f2cdb5','Lower right lace bar')
# Restrained shallow smile lives in actual current visible owner (hair ownership defect).
# Warm corners, not black punctuation; near/far eyes are protected throughout.
line(hair,[(68,28),(69,29),(71,29),(72,28)],'#c7744e','Subtle uneven shallow smile from canonical expression')
# Emit only changed pixels and preserve exact palette membership.
palette={tuple(p) for im in original.values() for p in im.getdata() if p[3]}
# Palette colors in native include unused entries; use palette chunk source instead of visible set.
import struct
raw=(R/'inputs/baseline.aseprite').read_bytes();pos=128;ln=int.from_bytes(raw[pos:pos+4],'little');q=pos+16
while q<pos+ln:
 size,kind=struct.unpack_from('<IH',raw,q);d=raw[q+6:q+size]
 if kind==0x2019:
  _,first,last=struct.unpack_from('<III',d);off=20
  for i in range(first,last+1):
   flags=struct.unpack_from('<H',d,off)[0];palette.add(tuple(d[off+2:off+6]));off+=6
   if flags&1:n=struct.unpack_from('<H',d,off)[0];off+=2+n
 q+=size
ops=[];expected=Image.new('RGBA',B.size)
for name,im in parts.items():
 if name.startswith('guide'):continue
 pts=[]
 for y in range(192):
  for x in range(128):
   p=im.getpixel((x,y));o=original[name].getpixel((x,y))
   if p!=o:
    assert p in palette,(name,x,y,p)
    pts.append({'x':x,'y':y,'color':'#'+bytes(p).hex()})
 if pts:ops.append({'sprite':'#3','layer':name,'frame':1,'paletteLock':True,'label':'Whole-character cluster and form finish','ops':[{'kind':'pixels','points':pts}]})
 expected.alpha_composite(im)
(R/'operations/pass-01.json').write_text(json.dumps(ops,indent=2));(R/'operations/authored-plan.json').write_text(json.dumps(notes,indent=2));expected.save(R/'proof/intended-pass-01.png')
print(json.dumps({'perlayer':{op['layer']:len(op['ops'][0]['points']) for op in ops},'visible_changes':sum(a!=b for a,b in zip(B.getdata(),expected.getdata()))}))
