"""Read-only native verification and faithful export previews. Never writes native art."""
from pathlib import Path
from PIL import Image, ImageDraw
from tools.check_native_pilot import read
import json, hashlib

P=Path('docs/experiments/2026-10-30-redrawn-breathing-sol')
S=Path('docs/experiments/2026-10-30-expression-strip/luna/passes/luna6-neutral.aseprite')
O=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol/reddit-motion-study/prototype/pass01.aseprite')
a,b,old=read(S),read(P/'pass01.aseprite'),read(O)
def compose(d,f):
    im=Image.new('RGBA',(128,192))
    for l in range(1,12): im.alpha_composite(d['cels'][(f,l)]['image'])
    return im
def holes(im):
    empty={(x,y) for y in range(192) for x in range(128) if not im.getpixel((x,y))[3]}
    stack=[v for v in empty if v[0] in [0,127] or v[1] in [0,191]]; seen=set(stack)
    while stack:
        x,y=stack.pop()
        for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if q in empty and q not in seen: seen.add(q);stack.append(q)
    return empty-seen
base=compose(a,0); baseholes=holes(base); frames=[compose(b,f) for f in range(12)]
times=[f['duration_ms'] for f in b['frames']]
checks={'artifact_sha256':hashlib.sha256((P/'pass01.aseprite').read_bytes()).hexdigest(),
        'canvas':b['canvas'],'frame_count':len(b['frames']),'layers_exact_metadata':a['layers']==b['layers'],
        'palette_chunk_exact':next(c for c in a['frames'][0]['non_cel_chunks'] if c['type']=='0x2019')==next(c for c in b['frames'][0]['non_cel_chunks'] if c['type']=='0x2019'),
        'durations_ms':times,'cycle_ms':sum(times),'frames':[],'protected_native_violations':[]}
mask=Image.new('L',(128,192))
for f,im in enumerate(frames):
    dy=1 if f in [3,4,5] else 0; blinksrc={8:4,9:5,10:6}.get(f)
    head=compose(old,blinksrc) if blinksrc is not None else base
    allowedholes={(x,y-dy) for x,y in baseholes if y<34}|{q for q in baseholes if q[1]>=34}
    changed=[];headnative=True;celmeta=True
    for l in range(12):
        src=a['cels'][(0,l)];dst=b['cels'][(f,l)];count=0
        celmeta &= src['opacity']==dst['opacity'] and src['z']==dst['z']
        if l in [10,11]:
            hs=old['cels'][(blinksrc,l)]['image'] if blinksrc is not None else src['image']
            headnative &= dst['image'].crop((0,0,128,31-dy)).tobytes()==hs.crop((0,dy,128,31)).tobytes()
        for y in range(192):
            for x in range(128):
                if src['image'].getpixel((x,y))!=dst['image'].getpixel((x,y)):
                    count+=1;mask.putpixel((x,y),255)
                    if l in [0,1,6,8,9] or y>=90:checks['protected_native_violations'].append([f+1,l,x,y])
        changed.append(count)
    checks['frames'].append({'frame':f+1,'native_export_exact':im.tobytes()==Image.open(P/f'frame-{f}.png').convert('RGBA').tobytes(),
        'fresh_reopen_export_exact':im.tobytes()==Image.open(P/f'proof/reopen-{f}.png').convert('RGBA').tobytes(),
        'rest_native_exact':all(a['cels'][(0,l)]['image'].tobytes()==b['cels'][(f,l)]['image'].tobytes() for l in range(12)),
        'registered_head_expression_native_exact_above31':headnative,'registered_head_composite_exact_above31':im.crop((30,0,82,31-dy)).tobytes()==head.crop((30,dy,82,31)).tobytes(),
        'lower_body_y90_exact':im.crop((0,90,128,192)).tobytes()==base.crop((0,90,128,192)).tobytes(),
        'shoe_native_exact':a['cels'][(0,1)]['image'].tobytes()==b['cels'][(f,1)]['image'].tobytes(),
        'cel_opacity_z_exact':celmeta,'new_unexplained_internal_holes':sorted(holes(im)-allowedholes),
        'changed_native_pixels_by_layer':changed,'opaque_pixel_count':sum(c[3]>0 for c in im.get_flattened_data())})
checks['blink_native_full_composite_exact']={str(f+1):compose(b,f).tobytes()==compose(old,of).tobytes() for f,of in [(8,4),(9,5),(10,6)]}
checks['inputs_recorded_after_construction']={str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in [S,O,Path('assets/references/approved-2026-10-26/character-scene.png'),Path('assets/references/approved-2026-10-26/character-closeup.png'),O.parent.parent/'reference.mp4']}
for sc in [1,3]:
    out=[]
    for im in frames:
        m=Image.new('RGBA',(128,192),'#dddddd');m.alpha_composite(im)
        out.append(m.convert('RGB').resize((128*sc,192*sc),Image.Resampling.NEAREST))
    out[0].save(P/f'proof/neutral-{sc}x.gif',save_all=True,append_images=out[1:],duration=times,loop=0,optimize=False,disposal=2)
    gif=Image.open(P/f'proof/neutral-{sc}x.gif');decoded=[];dur=[]
    for f in range(gif.n_frames):
        gif.seek(f);dur.append(gif.info['duration']);decoded.append(gif.convert('RGB').tobytes()==out[f].tobytes())
    checks[f'gif_{sc}x']={'frames':gif.n_frames,'durations':dur,'decoded_pixels_exact':decoded}
for name,box,sc in [('body',(0,0,128,192),1),('torso',(38,30,92,80),4),('hip',(39,61,86,100),5)]:
    w,h=(box[2]-box[0])*sc,(box[3]-box[1])*sc;o=Image.new('RGB',(w*4,(h+23)*3),'#ddd');d=ImageDraw.Draw(o)
    for i,im in enumerate(frames):
        x,y=(i%4)*w,(i//4)*(h+23);c=im.crop(box).resize((w,h),Image.Resampling.NEAREST);o.paste(c,(x,y+23),c);d.text((x+3,y+4),f'F{i+1} {times[i]}ms',fill='black')
    o.save(P/f'proof/contact-{name}.png')
checks['passed']=checks['layers_exact_metadata'] and checks['palette_chunk_exact'] and not checks['protected_native_violations'] and all(all(row[k] for k in ['native_export_exact','fresh_reopen_export_exact','registered_head_expression_native_exact_above31','registered_head_composite_exact_above31','lower_body_y90_exact','shoe_native_exact','cel_opacity_z_exact']) and not row['new_unexplained_internal_holes'] for row in checks['frames']) and all(checks['blink_native_full_composite_exact'].values())
(P/'proof/verification.json').write_text(json.dumps(checks,indent=2)+'\n');mask.save(P/'proof/observed-change-mask.png')
print(json.dumps({'passed':checks['passed'],'sha256':checks['artifact_sha256'],'cycle_ms':sum(times),'new_holes':[r['new_unexplained_internal_holes'] for r in checks['frames']],'all12_native_reopen_exact':all(r['fresh_reopen_export_exact'] for r in checks['frames'])},indent=2))
