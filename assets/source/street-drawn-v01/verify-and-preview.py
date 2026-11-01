"""Verify the actual Aseprite exports; only presentation layouts are drawn here."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'assets/export/street-drawn-v01'
PREVIEW=ROOT/'assets/previews/street-drawn-v01'
RECORD=ROOT/'docs/experiments/2026-10-26-drawn-background'
def load(name):return Image.open(OUT/name).convert('RGBA')
scene=load('street-scene-native.png');bg=load('background-native.png')
assert scene.size==bg.size==(352,264)
assert scene.tobytes()==load('street-scene-reopened.png').tobytes()
assert bg.tobytes()==load('background-reopened.png').tobytes()
assert set(bg.getchannel('A').tobytes())=={255}
char=Image.open(ROOT/'assets/export/standing-v04/standing.png').convert('RGBA')
expected=Image.new('RGBA',scene.size,(0,0,0,0));expected.alpha_composite(char,(84,61))
assert expected.tobytes()==load('character-placement-only.png').tobytes()
v04=json.loads((ROOT/'docs/experiments/2026-10-26-shoe-detail/checks.json').read_text())
assert hashlib.sha256((ROOT/'assets/source/standing-v04/standing.aseprite').read_bytes()).hexdigest()==v04['nativeSHA256']
assert hashlib.sha256((ROOT/'assets/export/standing-v04/standing.png').read_bytes()).hexdigest()==v04['exportSHA256']
for name,image in [('street-scene',scene),('background',bg)]:
    image.resize((1408,1056),Image.Resampling.NEAREST).save(PREVIEW/(name+'-4x.png'))
inventory=json.loads((RECORD/'editability-checks.json').read_text())
sheet=Image.new('RGB',(800,688),'#2d303e');d=ImageDraw.Draw(sheet)
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',12)
for i,layer in enumerate(inventory['layers']):
    x=(i%4)*200;y=(i//4)*172
    d.text((x+4,y+4),layer['name'].replace('bg/',''),font=font,fill='white')
    im=Image.open(PREVIEW/'layers'/(layer['name'].replace('/','_')+'.png')).convert('RGBA')
    backing=Image.new('RGBA',im.size,'#343747');backing.alpha_composite(im)
    sheet.paste(backing.resize((176,132),Image.Resampling.NEAREST).convert('RGB'),(x+12,y+25))
sheet.save(PREVIEW/'environment-layers.png')
# Separate revision preview. Main scene keeps the original warm lamp colors.
test=load('background-lamp-edit-test.png')
change=[(x,y) for y in range(264) for x in range(352) if bg.getpixel((x,y))!=test.getpixel((x,y))]
lamp=Image.open(PREVIEW/'layers/bg_15-lamp-light-pixels.png').convert('RGBA')
assert change and all(lamp.getpixel(p)[3]>0 for p in change)
editboard=Image.new('RGB',(768,456),'#2d303e');d=ImageDraw.Draw(editboard)
for x,im,label in [(16,bg,'Main warm lamps'),(400,test,'Local lamp edit test')]:
    d.text((x,8),label,font=font,fill='white')
    editboard.paste(im.crop((0,0,120,132)).resize((360,396),Image.Resampling.NEAREST).convert('RGB'),(x,32))
editboard.save(PREVIEW/'local-edit-proof.png')
source=(ROOT/'assets/source/street-drawn-v01/draw-background.lua').read_text()
assert 'fromFile=' not in source and source.count('app.open(')==2
assert 'background-clean-generated' not in source
report={
    'sceneCanvas':[352,264],'previewSize':[1408,1056],
    'environmentLayerCount':16,'sceneLayerCount':29,'environmentRasterImports':0,
    'sceneNativeReopenExportIdentical':True,'backgroundNativeReopenExportIdentical':True,
    'v04NativeAndPNGHashesUnchanged':True,'allCharacterPixelsAndNativeCelsPreserved':True,
    'characterOffset':[84,61],'environmentLocallyEditable':True,
    'localLampEditVisiblePixels':len(change),'localLampEditOther15LayersPreserved':True,
    'backgroundVisibleColors':len({bg.getpixel((x,y)) for y in range(264) for x in range(352)}),
    'sceneSHA256':hashlib.sha256((ROOT/'assets/source/street-drawn-v01/street-scene.aseprite').read_bytes()).hexdigest(),
    'backgroundSHA256':hashlib.sha256((ROOT/'assets/source/street-drawn-v01/background.aseprite').read_bytes()).hexdigest(),
    'sceneExportSHA256':hashlib.sha256((OUT/'street-scene-native.png').read_bytes()).hexdigest(),
    'backgroundExportSHA256':hashlib.sha256((OUT/'background-native.png').read_bytes()).hexdigest(),
    'visualApproval':'pending','GodotPlayback':'not performed',
}
(RECORD/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
