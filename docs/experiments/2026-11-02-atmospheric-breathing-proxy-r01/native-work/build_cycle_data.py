from pathlib import Path
import json,runpy
P=Path('/private/tmp/atmospheric-breathing-proxy-r01');obs=(P/'observations.md').read_text()
ns=runpy.run_path(str(P/'construct.py'));(P/'observations.md').write_text(obs)
stages=[(0,0),(0,1),(1,1),(1,2),(2,2),(3,3),(2,3),(2,2),(1,2),(1,1),(0,1),(0,0)]
durations=[200,180,180,200,220,300,200,220,260,280,300,260]
phases=['rest','inhale-open','inhale','inhale','inhale','apex','exhale','exhale','exhale','exhale','settle','rest']
ops={}
for i,(lift,expansion)in enumerate(stages):ops[str(i+1)]={n:ns['grid'](im)for n,im in ns['shape'](lift,expansion).items()}
json.dump({'canvas':[96,160],'layers':ns['layers'],'palette':['#00000000']+list(ns['C'].values()),'ops':ops,'stages':stages,'durations_ms':durations,'phases':phases,'total_ms':sum(durations)},open(P/'cycle-draw-ops.json','w'),indent=2)
print(json.dumps({'frames':len(stages),'unique_pose_combinations':len(set(stages)),'total_ms':sum(durations)}))
