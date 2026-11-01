import json,sys
from pathlib import Path
sys.path.insert(0,'docs/experiments/2026-10-30-evidence-idle-four-model/sol61')
from native_read import read
R=Path('docs/experiments/2026-10-31-recovery-grip/artist')
a=read(R/'source/recovery-grip-baseline.aseprite')
legend={'.':'#00000000','o':'#78371c','h':'#fcaf80','b':'#fda977','s':'#ea9368','d':'#e48558','e':'#90472c','j':'#393628','g':'#524c34','k':'#4b4732','G':'#665e3a','z':'#c8683f'}
handrows=['ggggoshhhhsssoo','gggoshhhssosog.','ggoshhshhsooggj','hhhhhsdhsogkkj.','hhhhhhhsdogkkj.','hhhhhhsbsogkkj.','bhhhhsbbdogkkj.','bbhhsbbdoggkkj.','bbbhsbdooggkkj.','obbbbsdogggkkj.','goobsooggggkkj.','jggggggggggkkj.']
assert all(len(r)==15 for r in handrows),[(r,len(r)) for r in handrows]
hand={'layer':'05-loaded-grip-drawing','frame':9,'label':'F9 compact curved enclosure and wrist planes pass01','ops':[{'kind':'grid','x':166,'y':80,'rows':handrows,'legend':legend}]}
# Replace only this owner's local handle fan, retaining its native layer and all other frames.
grid=[list('.'*34) for _ in range(24)]
def put(x,y,c):
 assert 158<=x<192 and 86<=y<110
 grid[y-86][x-158]=c
for y in range(90,110):
 x=round(171-(y-90)*0.5)
 for dx,c in [(-1,'O'),(0,'B'),(1,'L'),(2,'O')]:put(x+dx,y,c)
for y in range(90,105):
 x=round(175+(y-90)*11/14)
 for dx,c in [(-1,'O'),(0,'B'),(1,'L'),(2,'O')]:put(x+dx,y,c)
# Short incoming folded bundle at the far side of thumb; finger mass covers y87..89.
for x,y,c in [(176,86,'O'),(177,86,'B'),(178,86,'O'),(176,87,'O'),(177,87,'L'),(178,87,'O')]:put(x,y,c)
handles={'layer':'06-continuous-handle-tension','frame':9,'label':'F9 narrow branches emerge below curled grip to both tote rim attachments pass01','ops':[{'kind':'grid','x':158,'y':86,'rows':[''.join(r) for r in grid],'legend':{'O':'#795246','B':'#dfb39b','L':'#f2cdb5'}}]}
ops=[hand,handles]
(R/'operations/pass01.json').write_text(json.dumps(ops,indent=2))
print('Native input operations saved. No sprite or painted PNG created by this preparation script.')
