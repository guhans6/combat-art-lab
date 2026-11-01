from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import runpy,json,shutil,hashlib
H=Path(__file__).resolve().parent;R=H.parents[2]
fontpath='/System/Library/Fonts/Supplemental/Arial.ttf'
font=ImageFont.truetype(fontpath,18);small=ImageFont.truetype(fontpath,14)
def panel(path,size=(480,448)):
 im=Image.open(path).convert('RGBA');im=im.resize(size,Image.Resampling.NEAREST)
 bg=Image.new('RGBA',size,'#34343e');bg.alpha_composite(im);return bg.convert('RGB')
def sheet(entries,out,title):
 w=1024;h=76+len(entries)//2*514+(514 if len(entries)%2 else 0)
 im=Image.new('RGB',(w,h),'#24242d');d=ImageDraw.Draw(im);d.text((16,14),title,font=font,fill='white')
 for i,(name,path) in enumerate(entries):
  x=16+(i%2)*504;y=62+(i//2)*514;d.text((x,y),name,font=small,fill='#dddde5');im.paste(panel(path),(x,y+28))
 im.save(H/out)
sheet([('Approved original crop 480x448; unresized',H/'inputs/original-crop.png'),('A: traced + refined; 120x112 at 4x',H/'gated/a02-expression.png'),('B: raw converted seed; 120x112 at 4x',H/'b00-separated-seed.png'),('C: conversion + restored smile; 120x112 at 4x',H/'c01-restored-mouth.png')],'comparison.png','One source / crop / grid / palette policy. Conversion route C preferred; user selection pending.')
sheet([('Historical redraw; same crop/grid; NOT controlled arm',H.parent/'2026-10-27-original-guided-head-v02/pass-03-refined.png'),('New B candidate; same original crop/grid',H/'c01-restored-mouth.png')],'historical-context.png','Historical context only: different construction history and effort.')
# Native 1x and provisional 2x display (240x224), not a game-camera validation.
im=Image.new('RGB',(800,310),'#34343e');d=ImageDraw.Draw(im)
for x,path,label in [(16,H/'gated/a02-expression.png','A 1x'),(170,H/'c01-restored-mouth.png','C 1x')]:
 d.text((x,12),label,font=font,fill='white');im.paste(panel(path,(120,112)),(x,45))
im.paste(panel(H/'c01-restored-mouth.png',(240,224)),(340,45));d.text((340,12),'C 2x: projected display assumption',font=font,fill='white');d.text((16,280),'Native crop only; full-character scale and Godot readability remain untested.',font=small,fill='white');im.save(H/'native-and-display.png')
# Show all semantic native layers from the independent reader.
native=runpy.run_path(str(R/'tools/check_native_pilot.py'));s=native['read'](H/'c01-restored-mouth.aseprite')
im=Image.new('RGB',(800,740),'#24242d');d=ImageDraw.Draw(im);d.text((16,12),'C native visible parts: separate semantic layers; no hidden surfaces inferred',font=font,fill='white')
for i,l in enumerate(s['layers']):
 x=16+(i%3)*260;y=58+(i//3)*220;d.text((x,y),l['name'],font=small,fill='white')
 bg=Image.new('RGBA',(240,180),'#34343e');part=s['cels'][(0,i)]['image'].resize((192,180),Image.Resampling.NEAREST);bg.alpha_composite(part,(24,0));im.paste(bg.convert('RGB'),(x,y+25))
im.save(H/'native-layers.png')
# Local edit proof includes actual exports, with a separately magnified tie patch.
sheet([('C selected candidate: cream tie',H/'c01-restored-mouth.png'),('Duplicate only: brighter existing skin-light tie shade',H/'c01-restored-mouth-tie-edit.png')],'localized-edit.png','23 native tie pixels changed; eight other layers + strict metadata protected.')
frames=[Image.open(H/f'blink-final-frame-{i}.png').convert('RGBA') for i in range(1,6)]
durations=[1600,50,90,60,600]
strip=Image.new('RGBA',(600,112));
for i,im in enumerate(frames):strip.alpha_composite(im,(i*120,0))
strip.save(H/'blink-sheet.png')
film=Image.new('RGB',(1240,280),'#34343e');d=ImageDraw.Draw(film)
for i,im in enumerate(frames):
 x=10+i*246;bg=Image.new('RGBA',(240,224),'#34343e');bg.alpha_composite(im.resize((240,224),Image.Resampling.NEAREST));film.paste(bg.convert('RGB'),(x,42));d.text((x,14),f'{i+1}: {durations[i]} ms',font=font,fill='white')
film.save(H/'blink-filmstrip.png')
preview=[]
for im in frames:
 bg=Image.new('RGBA',(480,448),'#34343e');bg.alpha_composite(im.resize((480,448),Image.Resampling.NEAREST));preview.append(bg.convert('RGB'))
preview[0].save(H/'blink-preview.gif',save_all=True,append_images=preview[1:],duration=durations,loop=0,optimize=False,disposal=2)
layout={'canvas':[120,112],'frame_count':5,'frame_slots':[[i*120,0,120,112] for i in range(5)],'durations_ms':durations,'root_offsets':[[0,0]]*5,'anchor':[64,104],'anchor_role':'fixed crop registration point, not ground contact','scale':'1:1 native; no per-frame fit','palette':'same source-derived palette as B02','generated_reference':'generated-blink-reference.png','generation_use':'eyelid closure guidance only; redraw on final C01 native eye layer','status':'expression probe; not combat or Godot proof'}
(H/'blink-layout.json').write_text(json.dumps(layout,indent=2)+'\n')
# User-facing delivery locations use existing asset folders, never replace old versions.
source=R/'assets/source/assisted-bust-v01';export=R/'assets/export/assisted-bust-v01';previews=R/'assets/previews/assisted-bust-v01'
for p in [source,export,previews]:p.mkdir(parents=True,exist_ok=True)
for a,b in [(H/'c01-restored-mouth.aseprite',source/'bust.aseprite'),(H/'blink-restored-mouth.aseprite',source/'blink.aseprite'),(H/'c01-restored-mouth.png',export/'bust.png'),(H/'blink-sheet.png',export/'blink-sheet.png'),(H/'blink-layout.json',export/'blink-layout.json')]:shutil.copy2(a,b)
for name in ['comparison.png','historical-context.png','native-and-display.png','native-layers.png','localized-edit.png','blink-filmstrip.png','blink-preview.gif']:shutil.copy2(H/name,previews/name)
(source/'README.md').write_text('''# Assisted bust v01 — provisional candidate

Canonical sources remain assets/references/approved-2026-10-26. Bust is C01, the conversion route with restored mouth from B01,
conversion-plus-cleanup result, 120x112, nine visible semantic layers. Blink uses
five frames with eye-layer changes only. Neither is user-approved or Godot-tested.

Reproducible inputs, masks, scripts, comparisons, all attempts and checks:
`docs/experiments/2026-10-27-assisted-head-comparison/record.md`.
''')
print('Evidence sheets, native/display previews, layers, edit proof, blink exports and central candidate locations saved.')
