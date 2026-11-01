"""Read-only native->literal drawing replay capture. Does not write/open/save native files."""
from pathlib import Path
from PIL import Image
import sys,json,itertools,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'));from native_read import read
D=R/'recipe/final-replay';D.mkdir(exist_ok=True);manifest={'schema':1,'backend':'dedicated Aseprite MCP Pebbly0.8.2/headless Aseprite1.3.18.6-dev','scope':'Reproducible visible pixels/layers/timing. Native byte identity or a fresh full replay is not claimed. Original conversion and authored stage recipes retained separately.','variants':{}}
for v in ['clean','smear']:
 p=R/f'source/tote-{v}-material03.aseprite';a=read(p);calls=[]
 for (f,l),c in sorted(a['cels'].items()):
  im=c['image'];b=im.getbbox()
  if not b:continue
  crop=im.crop(b);colors=list(dict.fromkeys(px for px in crop.get_flattened_data() if px[3]));rev={c:chr(0x100+i) for i,c in enumerate(colors)};rows=[''.join(rev.get(im.getpixel((x,y)),'.') for x in range(b[0],b[2])) for y in range(b[1],b[3])]
  op={'kind':'grid','x':b[0],'y':b[1],'rows_rle':[''.join(str(len(list(g)))+ch for ch,g in itertools.groupby(row)) for row in rows],'legend':{rev[c]:'#%02x%02x%02x'%c[:3] for c in colors},'transparent':'erase'}
  calls.append({'frame':f+1,'layer':a['layers'][l]['name'],'createCel':True,'ops':[op]})
 q=D/f'{v}-cel-grids.json';q.write_text(json.dumps(calls,ensure_ascii=False,separators=(',',':')))
 manifest['variants'][v]={'native':str(p.relative_to(R)),'native_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'canvas':a['canvas'],'layers':a['layers'],'durations_ms':[f['duration_ms'] for f in a['frames']],'tag':{'name':'tote_attack','from':1,'to':19,'direction':'forward'},'palette':'../palette.json','calls':str(q.relative_to(R)),'calls_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'cel_count':len(calls)}
(D/'manifest.json').write_text(json.dumps(manifest,indent=2));print({k:v['native_sha256'] for k,v in manifest['variants'].items()})
