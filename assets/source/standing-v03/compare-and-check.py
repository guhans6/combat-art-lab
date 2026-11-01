"""Check exact head-only scope and lay out reference/v01/v02/v03 comparisons.

Pillow is used for analysis and labeled previews only. The sprite is edited in
Aseprite Lua; reference pixels are never copied into the delivered sprite.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json

ROOT=Path(__file__).resolve().parents[3]
PREVIEW=ROOT/'assets/previews/standing-v03'
RECORD=ROOT/'docs/experiments/2026-10-26-head-v03'
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def font(n): return ImageFont.truetype(FONT,n)
def allowed(x,y):
    return 34<=x<=79 and 2<=y<=30 and not (y>=29 and 57<=x<=65)
def backed(im):
    bg=Image.new('RGBA',im.size,'#343342');bg.alpha_composite(im)
    return bg.convert('RGB')
def load(v): return Image.open(ROOT/f'assets/export/standing-v0{v}/standing.png').convert('RGBA')
v1,v2,v3=load(1),load(2),load(3)
assert v1.size==v2.size==v3.size==(128,192)
reopened=Image.open(ROOT/'assets/export/standing-v03/standing-reopened.png').convert('RGBA')
assert reopened.tobytes()==v3.tobytes()
assert set(v3.getchannel('A').tobytes())=={0,255}
hashes=json.loads((RECORD/'baseline-hashes.json').read_text())
for filename,digest in hashes.items():
    assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==digest,filename
changes=[(x,y) for y in range(192) for x in range(128) if v2.getpixel((x,y))!=v3.getpixel((x,y))]
assert changes and all(allowed(x,y) for x,y in changes)
assert v2.crop((0,31,128,192)).tobytes()==v3.crop((0,31,128,192)).tobytes()
palette2={v2.getpixel((x,y)) for y in range(192) for x in range(128) if v2.getpixel((x,y))[3]}
palette3={v3.getpixel((x,y)) for y in range(192) for x in range(128) if v3.getpixel((x,y))[3]}
assert palette3<=palette2, palette3-palette2

per_layer=[]
for p in sorted((ROOT/'assets/previews/standing-v02/layers').glob('*.png')):
    old=Image.open(p).convert('RGBA');new=Image.open(PREVIEW/'layers'/p.name).convert('RGBA')
    changes_in_layer=[(x,y) for y in range(192) for x in range(128) if old.getpixel((x,y))!=new.getpixel((x,y))]
    assert all(allowed(x,y) for x,y in changes_in_layer),p.name
    per_layer.append({'name':p.stem,'changedPixels':len(changes_in_layer)})
assert {x['name'] for x in per_layer if x['changedPixels']}=={'01-hair-back','05-skin-face','10-hair-front','11-face-features'}
# Explicit pupil/white positions: distinct clusters with the same rightward gaze.
eye_ink=(63,43,40,255)
assert v3.getpixel((64,21))==eye_ink and v3.getpixel((70,21))==eye_ink
assert v3.getpixel((62,22))[:3]==(248,231,210)
assert v3.getpixel((69,22))[:3]==(209,185,165)

original=Image.open(ROOT/'assets/references/approved-2026-10-26/character-cutout.png').convert('RGBA')
box=(32,0,80,32)
original_head=original.crop((box[0]*8,0,box[2]*8,box[3]*8))
original_head.save(PREVIEW/'original-head-crop.png')
heads=[original_head]+[im.crop(box) for im in (v1,v2,v3)]
names=['Original isolated reference','v01','v02 - starting point','v03 - corrected head']
def board(selected,scale,out):
    w,h=48*scale,32*scale;gap=4*scale;top=7*scale
    canvas=Image.new('RGB',(len(selected)*(w+gap),h+top+2*scale),'#343342')
    d=ImageDraw.Draw(canvas)
    for slot,i in enumerate(selected):
        x=slot*(w+gap)+2*scale
        d.text((x,scale),names[i],fill='white',font=font(max(12,3*scale)))
        # Reference has 8x the sprite's source resolution; same displayed head size.
        canvas.paste(backed(heads[i]).resize((w,h),Image.Resampling.NEAREST),(x,top))
    canvas.save(PREVIEW/out)
board([0,1,2,3],8,'all-heads-comparison.png')
board([0,2,3],8,'head-before-after.png')
board([0,1,2,3],16,'all-heads-comparison-16x.png')
# Native-scale head panel: no enlargement of any sprite head.
native=Image.new('RGB',(336,88),'#343342');d=ImageDraw.Draw(native)
for i,im in enumerate(heads):
    x=i*84+16;d.text((x,8),['Ref.','v01','v02','v03'][i],fill='white',font=font(13))
    crop=backed(im if i else im.resize((48,32),Image.Resampling.NEAREST))
    native.paste(crop,(x,35))
native.save(PREVIEW/'native-heads.png')
# Full body is context only; all edits must remain inside the head mask.
full=Image.new('RGB',(864,660),'#343342');d=ImageDraw.Draw(full)
for x,im,label in [(32,v2,'v02 base'),(448,v3,'v03 head-only edit')]:
    d.text((x,16),label,font=font(24),fill='white')
    full.paste(backed(im).resize((384,576),Image.Resampling.NEAREST),(x,60))
full.save(PREVIEW/'full-body-scope-comparison.png')
diff=Image.new('RGB',(128,192),'#222430')
for p in changes: diff.putpixel(p,(255,195,90))
diff.resize((512,768),Image.Resampling.NEAREST).save(PREVIEW/'head-only-difference.png')
mask=Image.new('RGBA',(128,192),(0,0,0,0))
for y in range(192):
    for x in range(128):
        if allowed(x,y):mask.putpixel((x,y),(80,190,160,255))
mask.save(PREVIEW/'editable-head-mask.png')
report={
    'base':'v02','nativeCanvas':[128,192],'baseVersionsFileHashesUnchanged':True,
    'changedCompositePixels':len(changes),'changesOutsideHeadMask':0,
    'neckAndAllRowsFrom31Unchanged':True,'paletteColorsAdded':len(palette3-palette2),
    'visibleColors':len(palette3),'nativeReopenExportIdentical':True,'binaryAlpha':True,
    'pupilLocations':{'near':[64,21],'far':[70,21]},'pupilSeparationPixels':6,
    'eyeCheckLimit':'Authored pupil and white-cluster pixels verified; native readability also needs visual review.',
    'layers':per_layer,
    'nativeSHA256':hashlib.sha256((ROOT/'assets/source/standing-v03/standing.aseprite').read_bytes()).hexdigest(),
    'exportSHA256':hashlib.sha256((ROOT/'assets/export/standing-v03/standing.png').read_bytes()).hexdigest(),
    'referenceComparison':'Original 384x256 crop and 48x32 sprite crops displayed at equal sizes; nearest neighbor for previews only.',
    'visualApproval':'pending','GodotPlayback':'not performed',
}
(RECORD/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
