from pathlib import Path
from PIL import Image,ImageDraw
import sys,json
P=Path('/private/tmp/atmospheric-idle-sample-r04');sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
S=read(P/'keys/connected-keys.aseprite');names=[l['name']for l in S['layers']];idx=names.index('near-forearm-hand');ims=[S['cels'][f,idx]['image']for f in range(3)];warm={(121,88,61),(173,128,86),(185,141,96)}
def skin(im):
 out=Image.new('RGBA',im.size)
 for y in range(160):
  for x in range(96):
   v=im.getpixel((x,y))
   if v[3]and v[:3]in warm:out.putpixel((x,y),v)
 return out
skins=[skin(im)for im in ims];reg=Image.new('RGBA',(96,160));reg.alpha_composite(skins[2],(1,1));assert skins[0].tobytes()==skins[1].tobytes()==reg.tobytes();n=sum(v[3]>0 for v in skins[0].getdata())
rows=[]
for f,im in enumerate(ims):
 widths=[sum(im.getpixel((x,y))[3]>0 for x in range(96))for y in range(160)];active=[(y,w)for y,w in enumerate(widths)if w];rows.append({'key':f,'native_owner_bounds':im.getbbox(),'active_rows':len(active),'row_width_sequence': [w for y,w in active],'opaque_pixels':sum(widths)})
assert rows[0]['row_width_sequence']==rows[1]['row_width_sequence']==rows[2]['row_width_sequence']
# Exact per-row correspondence: no material colors or stripe pixels changed, only named row shifts.
for f,im in enumerate(ims):
 for y in range(160):
  sy=y+(1 if f==2 else 0)
  if sy>=160:continue
  if f==2:dx=round(-2+(sy-65)/12)if 65<=sy<=77 else(-2 if sy<65 else -1)
  elif f==1:dx=round(-1+(sy-65)/13)if 65<=sy<=78 else(-1 if sy<65 else 0)
  else:dx=0
  for x in range(96):
   xx=x+dx
   if 0<=xx<96:assert ims[0].getpixel((x,sy))==im.getpixel((xx,y))
for f in range(3):
 out=Image.new('RGBA',(96,160))
 for i in range(12):out.alpha_composite(S['cels'][f,i]['image'])
 for typ,im in[('clean',out),('owner',ims[f]),('skin',skins[f])]:
  bg=Image.new('RGBA',(260,280),'#73777b');bg.alpha_composite(im.crop((28,70,54,98)).resize((260,280),Image.Resampling.NEAREST));bg.convert('RGB').save(P/f'keys/wrist-K{f}-{typ}-10x.png')
report={'passed':True,'warm_hand_pixels':n,'K1_hand_RGBA_exact_K0':True,'K2_hand_RGBA_exact_registered_K0_translation':[-1,-1],'forearm_all_source_rows_color_sequences_exact':True,'near_forearm_row_widths_and_active_row_count_equal':True,'rows':rows,'mechanism':'forearm source rows translated backward at elbow more than wrist; wrist/hand source drawing rigid; slanted source lit strip follows contour with exact color and width sequence','factual_conclusion':'No hand flattening, material replacement or hand-shape discontinuity. Source already contains horizontal skin upper edge. Narrow source lit sleeve strip changes projected path with elbow angle; not a new highlight/relight.','still_decision':'continue; temporal shrug/naturalness unobserved'}
json.dump(report,open(P/'keys/wrist-registered-proof.json','w'),indent=2)
print(json.dumps({'passed':True,'warm_hand_pixels':n,'hand_rgba_registered_exact':True,'forearm_color_rows_exact':True}))
