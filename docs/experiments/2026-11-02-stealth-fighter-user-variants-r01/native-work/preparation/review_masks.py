from PIL import Image,ImageDraw
from pathlib import Path
import json
O=Path('/private/tmp/fighter-user-variants-r01/native-work')
for i in ['01','03','04','05']:
 D=O/f'variant-{i}';src=Image.open(O/f'preparation/source-grid-{i}.png').convert('RGBA');seed=Image.open(D/'raw-seed.png').convert('RGBA');mask=Image.open(D/'source-spatial-mask-native.png').convert('L');overlay=src.copy()
 for y in range(1,263):
  for x in range(1,127):
   if mask.getpixel((x,y)) and any(not mask.getpixel((nx,ny)) for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):overlay.putpixel((x,y),(230,80,130,255))
 sheet=Image.new('RGBA',(128*3*3,264*3+30),(60,63,68,255));d=ImageDraw.Draw(sheet)
 for n,(im,label) in enumerate([(src,'original crop / NN reference'),(overlay,'spatial outline / pink inside edge'),(seed,'seed / light matte')]):
  pan=Image.new('RGBA',im.size,(222,218,210,255));pan.alpha_composite(im);sheet.alpha_composite(pan.resize((384,792),Image.Resampling.NEAREST),(n*384,30));d.text((n*384+5,8),label,fill='white')
 sheet.convert('RGB').save(D/'source-mask-review-3x.png')
 # Face source context, direct original pixel crop and native transfer paired at same registration.
 r=json.loads((D/'recipe.json').read_text());b=r['crop'];sr=Image.open(O.parent/f'inputs/user-{i}.png');source_face=(400,175,630,400) if i=='01' else ((55,10,225,175) if i in ['03','05'] else (410,95,615,305))
 out=Image.new('RGB',(720,350),(210,207,200));d=ImageDraw.Draw(out);d.text((5,5),'Original face crop (preview only) / native source transfer / 64-color seed',fill='black');f=sr.crop(source_face);f.thumbnail((300,315),Image.Resampling.NEAREST);out.paste(f,(5,30));out.paste(src.crop((43,13,82,49)).resize((195,180),Image.Resampling.NEAREST),(310,50));face=Image.new('RGBA',(39,36),(210,207,200,255));face.alpha_composite(seed.crop((43,13,82,49)));out.paste(face.resize((195,180),Image.Resampling.NEAREST),(515,50));out.save(D/'face-review.png')
# Smoke image-delivery observed: L-like dark cluster upper-left, isolated warm pixel12,4, two gray editable10..11,9.
S=O/'smoke';a=Image.open(S/'before.png').convert('RGBA');b=Image.open(S/'after.png').convert('RGBA');e=Image.open(S/'erase.png').convert('RGBA');r=Image.open(S/'reopened.png').convert('RGBA');changes=[(x,y) for y in range(16) for x in range(16) if a.getpixel((x,y))!=b.getpixel((x,y))];assert changes==[(11,9)] and b.tobytes()==r.tobytes() and e.getpixel((10,9))[3]==0
(S/'checks.json').write_text(json.dumps({'ready':True,'mode':'headless','aseprite':'1.3.18.6-dev','extension':'0.8.2','python':'/opt/homebrew/bin/python3.11','pillow':'12.0.0','image_delivery':'look preview actually inspected','readback':'10,9 and11,9 #7b8990 before edit','one_pixel_changes':changes,'reopen_exact':True,'dot_semantics':'erase, not transparent skip','protected_outside_editable_point_unchanged':True,'out_of_mask_negative_control':'pending','validate_tool':'not exposed; not called'},indent=2))
