"""Read-only native/PNG/GIF review; writes only its own review evidence.
No editor launch, no art writes. Native facts do not establish artistic quality.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, sys
from PIL import Image
ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'tools'))
from check_native_pilot import read
old = ROOT/'docs/experiments/2026-10-30-idle-breath-blink/review/inspect_candidate.py'
spec = importlib.util.spec_from_file_location('review_helpers',old)
helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
compose, sheet = helper.compose, helper.sheet
def holes(im):
    w,h=im.size;transparent={i for i,v in enumerate(im.getchannel('A').getdata()) if not v};seen=set();result=[]
    for seed in transparent:
        if seed in seen:continue
        stack=[seed];seen.add(seed);region=[];edge=False
        while stack:
            i=stack.pop();region.append(i);x,y=i%w,i//w;edge |= x in (0,w-1) or y in (0,h-1)
            for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                n=ny*w+nx
                if 0<=nx<w and 0<=ny<h and n in transparent and n not in seen:seen.add(n);stack.append(n)
        if not edge:result.append({'size':len(region),'xy':sorted([[i%w,i//w] for i in region])})
    return sorted(result,key=lambda x:(-x['size'],x['xy']))
BASE = ROOT/'docs/experiments/2026-10-30-idle-breath-blink/luna/passes/pass01/luna6-idle-breath-blink-pass01.aseprite'
sha = lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def pix(im):return list(im.getdata())
def changed(a,b):return [i for i,(x,y) in enumerate(zip(pix(a),pix(b))) if x!=y]
def bounds(ids,w):return [min(i%w for i in ids),min(i//w for i in ids),max(i%w for i in ids)+1,max(i//w for i in ids)+1] if ids else None
def norm(im):
    im=im.convert('RGBA');return bytes(v for p in pix(im) for v in (p if p[3] else (0,0,0,0)))
def main():
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--label',required=True)
    p.add_argument('--exports',nargs='*',type=Path,default=[]);p.add_argument('--reopen',nargs='*',type=Path,default=[]);p.add_argument('--gifs',nargs='*',type=Path,default=[])
    a=p.parse_args();assert '/' not in a.label and '..' not in a.label
    out=HERE/a.label;out.mkdir(exist_ok=True)
    bd=read(BASE);cd=read(a.native);bf=[compose(bd,i) for i in range(len(bd['frames']))];cf=[compose(cd,i) for i in range(len(cd['frames']))]
    report={'candidate':str(a.native.resolve()),'candidate_sha256':sha(a.native),'baseline':str(BASE),'baseline_sha256':sha(BASE),'baseline_expected_sha256':'d5b9d7675de8bea50a1941361d3e3bed3c187b3ee7e1d7e0585d51f8d37cc8ed','canvas':cd['canvas'],'frame_count':len(cf),'header_equal':bd['header']==cd['header'],'layer_metadata_equal':bd['layers']==cd['layers'],'frame_metadata_equal':bd['frames']==cd['frames'],'cel_keys_equal':bd['cels'].keys()==cd['cels'].keys(),'layers':cd['layers'],'durations_ms':[x['duration_ms'] for x in cd['frames']],'frames':[],'artistic_quality':'not established by script','actual_speed_watched':False}
    w,h=cf[0].size
    for f,im in enumerate(cf):
        ref=bf[f];neutral=bf[0];ip,rp,np=pix(im),pix(ref),pix(neutral)
        ids=changed(neutral,im);prev=changed(cf[f-1],im) if f else []
        row={'frame':f,'duration_ms':report['durations_ms'][f],'vs_same_baseline_frame':len(changed(ref,im)),'vs_neutral':len(ids),'changed_bounds':bounds(ids,w),'vs_previous':len(prev),'vs_previous_bounds':bounds(prev,w),'opaque':sum(p[3]>0 for p in ip),'nonbinary_alpha':sum(p[3] not in (0,255) for p in ip),'alpha_lost_vs_neutral':sum(p[3]>0 and q[3]==0 for p,q in zip(np,ip)),'alpha_added_vs_neutral':sum(p[3]==0 and q[3]>0 for p,q in zip(np,ip)),'holes':holes(im),'holes_equal_baseline':holes(im)==holes(neutral),'face_head_y0_43_equal_same_baseline_frame':im.crop((0,0,w,43)).tobytes()==ref.crop((0,0,w,43)).tobytes(),'lower_y105_plus_equal':im.crop((0,105,w,h)).tobytes()==ref.crop((0,105,w,h)).tobytes(),'native_layers':[]}
        for l,meta in enumerate(cd['layers']):
            cc=cd['cels'].get((f,l));bc=bd['cels'].get((f,l));empty=Image.new('RGBA',(w,h));bi=bc['image'] if bc else empty;ci=cc['image'] if cc else empty
            row['native_layers'].append({'name':meta['name'],'changed_vs_same_baseline_frame':len(changed(bi,ci)),'geometry_baseline':bc['geometry'] if bc else None,'geometry_candidate':cc['geometry'] if cc else None,'opacity_equal':cc and bc and cc['opacity']==bc['opacity'],'z_equal':cc and bc and cc['z']==bc['z']})
        im.save(out/f'frame-{f}.png');report['frames'].append(row)
    labels=[f'{i}: {d}ms' for i,d in enumerate(report['durations_ms'])]
    sheet(cf,labels,out/'full-1x.png',scale=1,columns=8)
    sheet(cf,labels,out/'full-3x.png',scale=3,columns=4)
    sheet(cf,labels,out/'torso-1x.png',crop=(29,29,105,106),scale=1,columns=8)
    sheet(cf,labels,out/'torso-3x.png',crop=(29,29,105,106),scale=3,columns=4)
    sheet(cf,labels,out/'torso-6x-light.png',crop=(29,29,105,106),scale=6,columns=4,matte=(230,230,230,255))
    sheet([bf[0]]+cf[:4],['base neutral']+labels[:4],out/'breath-with-neutral-3x.png',crop=(29,29,105,106),scale=3,columns=5)
    report['seam_changed_pixels']=len(changed(cf[-1],cf[0]));report['blink_frames_4_5_6_exact']=[cf[i].tobytes()==bf[i].tobytes() for i in (4,5,6)]
    for key,paths in [('exports',a.exports),('reopen_exports',a.reopen)]:
        report[key]={'count':len(paths),'count_matches_native':len(paths)==len(cf),'frames':[]}
        for i,path in enumerate(paths):
            im=Image.open(path).convert('RGBA');report[key]['frames'].append({'path':str(path.resolve()),'sha256':sha(path),'equals_native':i<len(cf) and im.size==cf[i].size and im.tobytes()==cf[i].tobytes()})
    report['gifs']=[]
    for path in a.gifs:
        gif=Image.open(path);gr={'path':str(path.resolve()),'sha256':sha(path),'size':gif.size,'frame_count':gif.n_frames,'loop':gif.info.get('loop'),'frames':[]}
        for i in range(gif.n_frames):
            gif.seek(i);im=gif.convert('RGBA');scale=im.width/w
            row={'duration_ms':gif.info.get('duration'),'nearest_integer_scale':scale if scale.is_integer() and im.height==h*scale else None}
            if row['nearest_integer_scale'] and i<len(cf):
                ni=cf[i].resize(im.size,Image.Resampling.NEAREST);matte=im.getpixel((0,0));bg=Image.new('RGBA',im.size,matte);bg.alpha_composite(ni)
                row['equals_native_transparent']=norm(im)==norm(ni);row['equals_native_on_corner_matte']=im.tobytes()==bg.tobytes()
            gr['frames'].append(row)
        gr['durations_equal_native']=[x['duration_ms'] for x in gr['frames']]==report['durations_ms'];report['gifs'].append(gr)
    (out/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['frames','layers']},indent=2))
if __name__=='__main__':main()
