#!/usr/bin/env python3
"""Batch the six existing source poses with frozen masks and one shared scale."""
import argparse,contextlib,io,json,shutil
from pathlib import Path
from convert_image import prepare

POSES = [('01-idle.png',685,1037,123), ('02-strap-lift.png',684,1052,123),
         ('03-strap-grip.png',704,1034,124), ('04-windup.png',738,1050,125),
         ('05-swing.png',718,1052,127), ('06-recovery.png',760,1054,127)]


def run(source_root, out):
    required=[source_root/'inputs'/p[0] for p in POSES]+[source_root/f'recipe/source-mask-{i:02}.png' for i in range(1,7)]
    if any(not p.is_file() for p in required):
        raise ValueError('source experiment must contain all six inputs and reviewed masks')
    out.mkdir(parents=True,exist_ok=False)
    (out/'inputs').mkdir();(out/'recipes').mkdir()
    frames=[]
    for i,(name,hx,floor,tx) in enumerate(POSES,1):
        shutil.copy2(source_root/'inputs'/name,out/'inputs'/name)
        shutil.copy2(source_root/f'recipe/source-mask-{i:02}.png',out/'inputs'/f'mask-{i:02}.png')
        recipe={'source':'../inputs/'+name,'mask':f'../inputs/mask-{i:02}.png',
                'scale':183/1022,'canvas':[256,208],'source_anchor':[hx,floor],'target_anchor':[tx,193]}
        path=out/'recipes'/f'{i:02}.json';path.write_text(json.dumps(recipe,indent=2)+'\n')
        with contextlib.redirect_stdout(io.StringIO()):prepare(path,out/f'pose-{i:02}')
        report=json.loads((out/f'pose-{i:02}/report.json').read_text())
        frames.append({'frame':i,'name':name,'duration_ms':400,'report':report})
    (out/'manifest.json').write_text(json.dumps({'mode':'deterministic source-only conversion','shared_scale':183/1022,'frames':frames,'timing_role':'400ms study holds, not finished combat timing','no_model_calls':True},indent=2)+'\n')
    print(json.dumps({'frames':len(frames),'shared_scale':183/1022,'out':str(out)}))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();run(a.source_root.resolve(),a.out.resolve())
