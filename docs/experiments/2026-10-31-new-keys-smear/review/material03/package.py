from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import sys,json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'review/material03';sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'));from native_read import read,composite
B=read(R/'source/tote-smear.aseprite');A=read(R/'source/tote-smear-material03.aseprite');frames=[];evidence=[]
for f in [4,5,6,8,9,14,15,16]:
 before=composite(B,f-1);after=composite(A,f-1);sheet=Image.open(R/'proof/material03-smear-sheet.png').convert('RGBA').crop(((f-1)*256,0,f*256,208));assert after.tobytes()==sheet.tobytes();before.save(D/f'before-{f}.png');after.save(D/f'after-{f}.png')
 mask=Image.new('L',(256,208))
 for l in ([1,2,6] if f==9 else [2,6]):
  for ar in [B,A]:mask=ImageChops.lighter(mask,ar['cels'][(f-1,l)]['image'].getchannel('A'))
 mask.save(D/f'mask-{f}.png');frames.append({'id':f'F{f}','before':f'before-{f}.png','after':f'after-{f}.png','mask':f'mask-{f}.png','regions':[{'name':'sleeves-wrists-grip-through-root-context','crop':[85,32,185,123]}]})
 # Native actual owner-isolated and hidden views; clean composite beside them.
 imgs=[('clean',after)]
 for l in [1,2,4,5,6]:
  imgs.append((A['layers'][l]['name']+' alone',A['cels'][(f-1,l)]['image']))
 for l in [1,4,5,6]:
  z=Image.new('RGBA',(256,208))
  for k in range(8):
   if k!=l and (f-1,k) in A['cels']:z.alpha_composite(A['cels'][(f-1,k)]['image'])
  imgs.append(('hide '+A['layers'][l]['name'],z))
 crop=(85,32,225,140);w,h=420,324;out=Image.new('RGB',(w*5,(h+22)*2),'#343c49');dr=ImageDraw.Draw(out)
 for j,(name,im) in enumerate(imgs):
  v=Image.new('RGBA',(140,108),'#343c49');v.alpha_composite(im.crop(crop));x=j%5*w;y=j//5*(h+22);out.paste(v.resize((w,h),Image.Resampling.NEAREST).convert('RGB'),(x,y+22));dr.text((x+3,y+3),name,fill='white')
 out.save(D/f'ownership-{f}.png');evidence.append({'role':f'F{f} actualnativeownersandhide','path':f'ownership-{f}.png'})
# Before/after material2x allmodifiedfamilies, meaningful exact1x files above.
out=Image.new('RGB',(512*4,230*2),'#343c49');dr=ImageDraw.Draw(out)
for j,f in enumerate([4,5,6,8,9,14,15,16]):
 x=j%4*512;y=j//4*230
 for off,ar,label in [(0,B,'before'),(256,A,'after')]:
  im=composite(ar,f-1);out.paste(im,(x+off,y+20),im);dr.text((x+off+5,y+3),f'F{f} {label}',fill='white')
out.save(D/'material-before-after.png');evidence.append({'role':'allaffectednativecomposites matchedgrid','path':'material-before-after.png'})
spec={'baseline_role':'retained before final material/wrist/root correction; rejected material treatment','registration':'same256x208 grid; exact root/head/legs/prop except smearrearroot; anatomy-specific nativeowners checked separately','required_frame_ids':[f'F{f}' for f in [4,5,6,8,9,14,15,16]],'allow_new_colors':True,'allow_partial_alpha':False,'frames':frames,'evidence':evidence+[{'role':'candidate native','path':'../../source/tote-smear-material03.aseprite'},{'role':'baseline native','path':'../../source/tote-smear.aseprite'},{'role':'actual MCP sheet','path':'../../proof/material03-smear-sheet.png'},{'role':'scope and exact arm roles','path':'../../recipe/material03-scope.json'}],'zoom':3}
(D/'comparison.json').write_text(json.dumps(spec,indent=2))
checks=[]
for f in range(19):
 for l in range(8):
  x=B['cels'].get((f,l),{}).get('image',Image.new('RGBA',(256,208)));y=A['cels'].get((f,l),{}).get('image',Image.new('RGBA',(256,208)))
  if x.tobytes()!=y.tobytes():checks.append([f+1,A['layers'][l]['name']])
# Named far root must overlap actual far and body material, not only be near the silhouette.
checks2={'changed_cels':checks,'smear_FL_root':[160,99],'rear_at_FL':A['cels'][(8,1)]['image'].getpixel((160,99)),'body_at_FL':A['cels'][(8,4)]['image'].getpixel((160,99)),'all_frames_same_timing':B['frames']==A['frames']}
(D/'native-scope.json').write_text(json.dumps(checks2,indent=2));print(checks2)
