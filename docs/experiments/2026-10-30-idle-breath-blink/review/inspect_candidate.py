"""Read-only independent candidate inspection; writes evidence only in review/.

Uses the repository's fail-closed decoder. It refuses unsupported cel types and
non-normal visible blend/opacity rather than guessing a composite. No editor launch.
This script measures pixels/timing; it does not judge anatomy or perceived rhythm.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import argparse, hashlib, json, sys

REVIEW = Path(__file__).resolve().parent
REPO = REVIEW.parents[3]
sys.path.insert(0, str(REPO / 'tools'))
from check_native_pilot import read

BASE = REPO / 'docs/experiments/2026-10-30-expression-strip/luna/passes/luna6-neutral.aseprite'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def pixels(im):
    return list(im.get_flattened_data())


def compose(data, frame):
    result = Image.new('RGBA', tuple(data['canvas']))
    for layer, meta in enumerate(data['layers']):
        if not meta['flags'] & 1:
            continue
        assert meta['blend'] == 0 and meta['opacity'] == 255, meta
        cel = data['cels'].get((frame, layer))
        if cel:
            assert cel['opacity'] == 255 and cel['z'] == 0, cel
            result.alpha_composite(cel['image'])
    return result


def holes(im):
    w, h = im.size
    a = list(im.getchannel('A').get_flattened_data())
    transparent = {i for i, value in enumerate(a) if value == 0}
    seen = set()
    enclosed = []
    for seed in transparent:
        if seed in seen:
            continue
        stack, region, edge = [seed], [], False
        seen.add(seed)
        while stack:
            point = stack.pop()
            region.append(point)
            x, y = point % w, point // w
            edge |= x in (0, w-1) or y in (0, h-1)
            for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                n = ny*w+nx
                if 0 <= nx < w and 0 <= ny < h and n in transparent and n not in seen:
                    seen.add(n)
                    stack.append(n)
        if not edge:
            enclosed.append({'size':len(region), 'xy':sorted([[i%w,i//w] for i in region])})
    return sorted(enclosed, key=lambda x:(-x['size'], x['xy']))


def sheet(images, labels, path, crop=None, scale=1, columns=8, matte=(55,60,68,255)):
    images = [im.crop(crop) if crop else im for im in images]
    w,h = images[0].size
    columns = min(columns,len(images))
    cellw,cellh = w*scale+12,h*scale+32
    out = Image.new('RGB',(cellw*columns,cellh*((len(images)+columns-1)//columns)),matte[:3])
    draw=ImageDraw.Draw(out)
    for i,(im,label) in enumerate(zip(images,labels)):
        x,y=(i%columns)*cellw,(i//columns)*cellh
        draw.text((x+4,y+4),label,fill=(245,245,245))
        bg=Image.new('RGBA',im.size,matte);bg.alpha_composite(im)
        out.paste(bg.resize((w*scale,h*scale),Image.Resampling.NEAREST).convert('RGB'),(x+6,y+25))
    out.save(path)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--native',required=True,type=Path)
    p.add_argument('--gif',type=Path)
    p.add_argument('--exports',nargs='*',type=Path,default=[])
    p.add_argument('--label',required=True)
    args=p.parse_args()
    assert '/' not in args.label and '..' not in args.label
    destination=REVIEW/args.label
    destination.mkdir(exist_ok=False)
    base=read(BASE); data=read(args.native)
    original=compose(base,0); native=[compose(data,i) for i in range(len(data['frames']))]
    assert data['canvas']==base['canvas']
    bp=pixels(original); w,h=original.size
    report={'native':str(args.native.resolve()),'native_sha256':sha(args.native),
        'baseline_native_sha256':sha(BASE),'canvas':data['canvas'],
        'layer_metadata_equals_baseline':data['layers']==base['layers'],
        'layers':data['layers'],'frame_count':len(native),
        'native_durations_ms':[f['duration_ms'] for f in data['frames']],
        'non_cel_chunks_by_frame':data['frames'], 'baseline_holes':holes(original),
        'frames':[], 'artistic_quality':'not established by this script'}
    report['native_loop_ms']=sum(report['native_durations_ms'])
    for i,im in enumerate(native):
        pp=pixels(im); diff=[j for j,(a,b) in enumerate(zip(bp,pp)) if a!=b]
        imagepath=destination/f'native-frame-{i+1:02d}.png';im.save(imagepath)
        layerchanges=[]
        for j,meta in enumerate(data['layers']):
            cel=data['cels'].get((i,j));bc=base['cels'].get((0,j))
            before=bc['image'] if bc else Image.new('RGBA',original.size)
            after=cel['image'] if cel else Image.new('RGBA',original.size)
            changed=sum(a!=b for a,b in zip(pixels(before),pixels(after)))
            layerchanges.append({'layer':meta['name'],'changed_pixels_vs_baseline':changed,
                'geometry':cel['geometry'] if cel else None})
        report['frames'].append({'frame':i+1,'duration_ms':data['frames'][i]['duration_ms'],
            'rgba_sha256':hashlib.sha256(im.tobytes()).hexdigest(),
            'alpha_bounds':im.getchannel('A').getbbox(),'opaque_count':sum(a[3]==255 for a in pp),
            'nonbinary_alpha_count':sum(a[3] not in (0,255) for a in pp),
            'changed_pixels_vs_baseline':len(diff),'changed_bounds':(
                [min(j%w for j in diff),min(j//w for j in diff),max(j%w for j in diff)+1,max(j//w for j in diff)+1] if diff else None),
            'changed_pixels_y165_plus':sum(j//w>=165 for j in diff),
            'changed_pixels_y95_plus':sum(j//w>=95 for j in diff),
            'holes':holes(im),'native_layers':layerchanges})
    labels=[f'{i+1}: {d}ms' for i,d in enumerate(report['native_durations_ms'])]
    sheet(native,labels,destination/'all-native-1x.png',scale=1,columns=8)
    sheet(native,labels,destination/'all-native-3x.png',scale=3,columns=4)
    sheet(native,labels,destination/'all-heads-8x.png',crop=(34,0,87,43),scale=8,columns=4)
    sheet(native,labels,destination/'all-bodies-4x-light.png',crop=(30,30,105,105),scale=4,columns=4,matte=(230,230,230,255))
    report['loop_seam_changed_pixels']=sum(a!=b for a,b in zip(pixels(native[-1]),pixels(native[0])))
    if args.exports:
        assert len(args.exports)==len(native)
        report['export_checks']=[{'path':str(p.resolve()),'sha256':sha(p),
            'rgba_matches_native':Image.open(p).convert('RGBA').tobytes()==im.tobytes() and Image.open(p).size==im.size}
            for p,im in zip(args.exports,native)]
    if args.gif:
        gif=Image.open(args.gif);seq=[];durations=[]
        for i in range(gif.n_frames):
            gif.seek(i);seq.append(gif.convert('RGBA').copy());durations.append(gif.info.get('duration'))
        report['gif']={'path':str(args.gif.resolve()),'sha256':sha(args.gif),'size':gif.size,
            'frame_count':len(seq),'durations_ms':durations,'loop':gif.info.get('loop'),
            'loop_ms':sum(durations) if all(isinstance(d,int) for d in durations) else None,
            'watched_actual_speed':False,'matches_native_frame_by_frame':[]}
        for im in seq:
            matches=[]
            for j,ni in enumerate(native):
                if im.size==ni.size and im.tobytes()==ni.tobytes():matches.append(j+1)
            report['gif']['matches_native_frame_by_frame'].append(matches)
        sheet(seq,[f'GIF {i+1}: {d}ms' for i,d in enumerate(durations)],destination/'all-gif-1x.png',columns=8)
    (destination/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['layers','frames','non_cel_chunks_by_frame','baseline_holes']},indent=2))


if __name__=='__main__':main()
