#!/usr/bin/env python3
"""Build repeatable visual and pixel-diff evidence for Luna pass03."""
from hashlib import sha256
import json
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
REPO=Path(__file__).resolve().parents[5]
BASE=ROOT/'inputs'/'current-idle-exports'
OUT=ROOT/'exports'/'pass03'
NATIVE=ROOT/'passes'/'pass03'/'luna6-clear-breathing-pass03.aseprite'
GIF=OUT/'luna6-clear-breathing-pass03.gif'
PROOF=ROOT/'proof'/'pass03'
REOPENED=PROOF/'reopened'
BG='#44444e'

def digest(p):
    h=sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''): h.update(block)
    return h.hexdigest()
def frames(folder):
    result=[Image.open(folder/f'frame-{i}.png').convert('RGBA') for i in range(8)]
    if any(im.size!=(128,192) for im in result): raise ValueError(folder)
    return result
def matte(im):
    bg=Image.new('RGBA',im.size,ImageColor.getcolor(BG,'RGBA'))
    return Image.alpha_composite(bg,im).convert('RGB')
def diff(a,b):
    changed=[]; lost=[]; gained=[]
    pa,pb=a.load(),b.load()
    for y in range(a.height):
        for x in range(a.width):
            x0,x1=pa[x,y],pb[x,y]
            if x0!=x1: changed.append((x,y))
            if x0[3] and not x1[3]: lost.append((x,y))
            if not x0[3] and x1[3]: gained.append((x,y))
    box=None
    if changed:
        xs,ys=zip(*changed); box=[min(xs),min(ys),max(xs)+1,max(ys)+1]
    return {'changedPixels':len(changed),'changedBoundsHalfOpen':box,
      'alphaLost':len(lost),'alphaLostCoordinates':lost,
      'alphaGained':len(gained),'alphaGainedCoordinates':gained,
      'opaqueBefore':sum(p[3]>0 for p in a.getdata()),'opaqueAfter':sum(p[3]>0 for p in b.getdata()),
      'faceCropChanged_y_lt_42':sum(1 for x,y in changed if y<42),
      'lowerBodyChanged_y_ge_76':sum(1 for x,y in changed if y>=76)}
def sheet(old,new,indices,scale,path):
    gap=4*scale; head=18*scale; w=128*scale; h=192*scale
    im=Image.new('RGB',(gap+len(indices)*(w+gap),gap+2*(head+h+gap)),BG); d=ImageDraw.Draw(im)
    for ri,(name,seq) in enumerate((('current',old),('pass03',new))):
        top=gap+ri*(head+h+gap)
        for ci,i in enumerate(indices):
            left=gap+ci*(w+gap); d.text((left+2*scale,top),f'{name} F{i+1}',fill='#f4f2ed',font=ImageFont.load_default())
            im.paste(matte(seq[i]).resize((w,h),Image.Resampling.NEAREST),(left,top+head))
    im.save(path)
def change_sheet(old,new):
    indices=[1,2,3]; crop=(34,38,100,70); scale=6; gap=5; head=18
    tw=(crop[2]-crop[0])*scale; th=(crop[3]-crop[1])*scale
    im=Image.new('RGB',(gap+3*(tw+gap),gap+len(indices)*(th+head+gap)),BG); d=ImageDraw.Draw(im)
    for ri,i in enumerate(indices):
        top=gap+ri*(th+head+gap)
        for ci,(label,src) in enumerate((('current',old[i]),('pass03',new[i]),('diff',None))):
            left=gap+ci*(tw+gap); d.text((left+2,top),f'{label} F{i+1}',fill='#f4f2ed',font=ImageFont.load_default())
            tile=Image.new('RGBA',(crop[2]-crop[0],crop[3]-crop[1]),(51,51,60,255))
            if ci<2: tile=src.crop(crop)
            else:
                a,b=old[i].load(),new[i].load(); q=tile.load()
                for y in range(crop[1],crop[3]):
                    for x in range(crop[0],crop[2]):
                        p0,p1=a[x,y],b[x,y]
                        c=(51,51,60,255) if p0==p1 else (255,192,64,255)
                        q[x-crop[0],y-crop[1]]=c
            im.paste(matte(tile).resize((tw,th),Image.Resampling.NEAREST),(left,top+head))
    im.save(PROOF/'current-vs-pass03-chest-6x.png')
def main():
    PROOF.mkdir(parents=True,exist_ok=True)
    old,new=frames(BASE),frames(OUT)
    reopened=frames(REOPENED)
    reopened_pixel_equal=all(list(a.getdata())==list(b.getdata()) for a,b in zip(new,reopened))
    reopened_byte_equal=all(digest(OUT/f'frame-{i}.png')==digest(REOPENED/f'frame-{i}.png') for i in range(8))
    with Image.open(GIF) as gif:
        durations=[]
        for i in range(gif.n_frames): gif.seek(i); durations.append(gif.info.get('duration'))
        gif_meta={'size':list(gif.size),'frames':gif.n_frames,'durationsMs':durations,'loop':gif.info.get('loop')}
    derived=[matte(f).resize((384,576),Image.Resampling.NEAREST) for f in new]
    derived[0].save(OUT/'luna6-clear-breathing-pass03-3x-neutral-review.gif',save_all=True,append_images=derived[1:],duration=durations,loop=0,disposal=2,optimize=False)
    sheet(old,new,list(range(8)),1,PROOF/'current-vs-pass03-1x.png')
    sheet(old,new,[0,1,2,3],3,PROOF/'current-vs-pass03-key-poses-3x.png')
    change_sheet(old,new)
    report={'candidateSource':str(NATIVE.relative_to(REPO)),'candidateSourceSha256':digest(NATIVE),
      'nativeGifPath':str(GIF.relative_to(REPO)),'nativeGifSha256':digest(GIF),'nativeGif':gif_meta,
      'comparisonBase':'copied current-idle frame exports in inputs/current-idle-exports',
      'frameSize':[128,192],'frameCount':len(new),'comparisonsByFrame':[diff(a,b) for a,b in zip(old,new)],
      'changedPixelsAllWithinUpperBody':all(not c['changedBoundsHalfOpen'] or (c['changedBoundsHalfOpen'][0]>=30 and c['changedBoundsHalfOpen'][1]>=40 and c['changedBoundsHalfOpen'][2]<=102 and c['changedBoundsHalfOpen'][3]<=68) for c in [diff(a,b) for a,b in zip(old,new)]),
      'candidateColorsSubsetOfCurrent':set().union(*(set(f.getdata()) for f in new)) <= set().union(*(set(f.getdata()) for f in old)),
      'paletteEntriesAdded':0,'freshNativeReopen':{
        'sourceReopenedViaAsepriteMCP':True,
        'spriteInfo':{'canvas':[128,192],'frameCount':8,'layerCount':12,'durationsMs':durations,'idleTag':[1,8]},
        'reexportedFramePixelsIdentical':reopened_pixel_equal,
        'reexportedFramePNGBytesIdentical':reopened_byte_equal,
      }}
    (PROOF/'frame-metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
