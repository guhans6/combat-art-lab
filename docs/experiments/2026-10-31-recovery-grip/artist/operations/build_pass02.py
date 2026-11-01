import json
from pathlib import Path
R=Path('docs/experiments/2026-10-31-recovery-grip/artist')
# Round1: remove inherited upper-handle remnants on actual tote owner above its local rim;
# reroute far exposed branch to the existing far rim corner, keep bag body below rim.
erase=[]
for y in range(87,105):
 xs=[x for x in range(166,188) if y<106-(x-172)*7/17]
 if xs:erase.append({'kind':'grid','x':min(xs),'y':y,'rows':['.'*len(xs)],'legend':{}})
ops=[{'frame':9,'layer':'04-tote-and-handles','label':'F9 remove only inherited upper handle remnants above rim','ops':erase}]
grid=[list('.'*34) for _ in range(24)]
def put(x,y,c):
 assert 158<=x<192 and 86<=y<110
 grid[y-86][x-158]=c
for y in range(90,110):
 x=round(171-(y-90)*.5)
 for dx,c in [(-1,'O'),(0,'B'),(1,'L'),(2,'O')]:put(x+dx,y,c)
for y in range(90,101):
 x=round(175+(y-90)*1.3)
 for dx,c in [(-1,'O'),(0,'B'),(1,'L'),(2,'O')]:put(x+dx,y,c)
ops.append({'frame':9,'layer':'06-continuous-handle-tension','label':'F9 far branch to actual far rim; no detached upper stub','ops':[{'kind':'grid','x':158,'y':86,'rows':[''.join(r) for r in grid],'legend':{'O':'#795246','B':'#dfb39b','L':'#f2cdb5'}},{'kind':'grid','x':175,'y':83,'rows':['BO'],'legend':{'O':'#795246','B':'#dfb39b'}}]})
rows=['shhdoso','sbhhdso','hhdbhdo','hdbh sog'.replace(' ',''),'sbh dogg'.replace(' ',''),'bhdoggg','bdogggg','soggggg','ogggggg']
assert all(len(r)==7 for r in rows),[(r,len(r)) for r in rows]
ops.append({'frame':9,'layer':'05-loaded-grip-drawing','label':'F9 opposing thumb and stepped finger pads enclosing bundle','ops':[{'kind':'grid','x':170,'y':82,'rows':rows,'legend':{'o':'#78371c','h':'#fcaf80','b':'#fda977','s':'#ea9368','d':'#e48558','g':'#524c34'}}]})
(R/'operations/pass02.json').write_text(json.dumps(ops,indent=2))
