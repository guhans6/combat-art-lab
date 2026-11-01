"""Package existing dedicated-MCP exports and verify native/scope boundaries."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,hashlib,math
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'))
sys.path.insert(0,str(R.parent/'2026-10-30-coherent-idle'))
from native_read import read,composite
from gif_timeline import check
scope=json.loads((R/'scope.json').read_text());a=read(R/'source/connected-bag.aseprite');b=read(scope['base'])
def require(x,msg):
 if not x:raise RuntimeError(msg)
def visible(im):return bytes(v for p in im.get_flattened_data() for v in (p if p[3] else (0,0,0,0)))
frames=[composite(a,f) for f in range(13)];times=[f['duration_ms'] for f in a['frames']]
require(a['canvas']==b['canvas']==[320,192],'canvas drift')
require(a['layers']==b['layers'],'layer metadata drift')
require(times==[f['duration_ms'] for f in b['frames']],'timing drift')
require(a['chunks']==b['chunks'],'non-cel chunks drift')
require(set(a['cels'])==set(b['cels']),'cel inventory drift')
checks=json.loads((R/'review/final-checks.json').read_text());require(checks['all_other_cels_exact'],'scope drift')
colors={p for c in b['cels'].values() for p in c['image'].get_flattened_data() if p[3]}
# New drawing colors are a subset of base used colors; stronger than palette-only.
require(all(p in colors for im in frames for p in im.get_flattened_data() if p[3]),'color outside base used palette')
for f,im in enumerate(frames):
 require(visible(im)==visible(Image.open(R/'frames'/f'candidate-{f}.png').convert('RGBA')),f'export mismatch F{f+1}')
 require(set(im.getchannel('A').get_flattened_data())<={0,255},'partialalpha')
 if not 7<=f<=9:require(visible(im)==visible(composite(b,f)),f'protectedframe{f+1}')
sheet=Image.open(R/'scratch/reopened-sheet.png').convert('RGBA')
for f,im in enumerate(frames):require(visible(im)==visible(sheet.crop((f*320,0,(f+1)*320,192))),f'reopen mismatch F{f+1}')
# Clean common-scale presentation, no independently fitted poses.
box=(85,0,225,192);s=3;out=Image.new('RGBA',(3*140*s,192*s+30),'#303336');d=ImageDraw.Draw(out)
for j,f in enumerate([8,9,10]):
 out.alpha_composite(frames[f-1].crop(box).resize((420,576),Image.Resampling.NEAREST),(j*420,30));d.text((j*420+10,8),f'F{f} | {times[f-1]} ms',fill='white')
out.convert('RGB').save(R/'review/three-poses.png')
# Region-only diagnostic before/after, fixed common crop, complete bag and grip.
box=(135,65,221,145);out=Image.new('RGBA',(3*344,2*350),'#303336');d=ImageDraw.Draw(out)
for j,f in enumerate([8,9,10]):
 for row,obj in enumerate([b,a]):
  im=composite(obj,f-1).crop(box).resize((344,320),Image.Resampling.NEAREST);out.alpha_composite(im,(j*344,row*350+26));d.text((j*344+5,row*350+5),f'F{f} '+('before' if row==0 else 'after'),fill='white')
out.convert('RGB').save(R/'review/join-comparison.png')
# GIFs package actual native-proven exports. Explicitly retain original timing.
gifchecks={}
for name,indices,scale in [('context',range(6,11),3),('full-cycle',range(13),2)]:
 ims=[];raw=[frames[i] for i in indices];ts=[times[i] for i in indices]
 for im in raw:
  bg=Image.new('RGBA',im.size,'#303336');bg.alpha_composite(im);ims.append(bg.convert('RGB').resize((320*scale,192*scale),Image.Resampling.NEAREST))
 # Full common palette avoids per-frame re-quantization flicker.
 allcolors=set(c for im in ims for c in im.get_flattened_data());require(len(allcolors)<=256,'GIF too many colors')
 pal=Image.new('P',(1,1));flat=[v for c in sorted(allcolors) for v in c];pal.putpalette(flat+[0]*(768-len(flat)))
 index={c:i for i,c in enumerate(sorted(allcolors))};pframes=[]
 for im in ims:
  pf=Image.new('P',im.size);pf.putpalette(pal.getpalette());pf.putdata([index[c] for c in im.get_flattened_data()]);pframes.append(pf)
 path=R/'review'/f'{name}.gif';pframes[0].save(path,save_all=True,append_images=pframes[1:],duration=ts,loop=0,disposal=2,optimize=False)
 gifchecks[name]=check(path,raw,ts,scale)
# Bind full ownership and neighbor evidence through existing packet.
spec={'baseline_role':'rejected diagnostic full-attack-repair, not artistically approved','registration':'same320x192 native canvas; unchanged body cels/root, no image fitting','required_frame_ids':['F8','F9','F10'],'allow_new_colors':True,'zoom':5,'evidence':[{'role':'candidate native','path':'source/connected-bag.aseprite'},{'role':'frozen scope and object sites','path':'scope.json'},{'role':'all-frame native scope proof','path':'review/final-checks.json'},{'role':'neighbor poses F7-F11','path':'review/final-neighbors.png'}],'frames':[]}
for f in [8,9,10]:
 spec['evidence'] += [{'role':f'F{f} actual owner/hide evidence','path':f'review/final-owners-f{f}.png'},{'role':f'F{f} site guide','path':f'review/final-guide-f{f}.png'}]
 spec['frames'].append({'id':f'F{f}','before':f'../2026-10-31-full-attack-repair/frames/candidate-{f-1}.png','after':f'frames/candidate-{f-1}.png','mask':f'review/allowed-f{f}.png','regions':[{'name':'whole connected grip-straps-rim-body','crop':scope['frames'][str(f)]['crop']}]})
(R/'comparison.json').write_text(json.dumps(spec,indent=2)+'\n')
report={'native_sha256':hashlib.sha256((R/'source/connected-bag.aseprite').read_bytes()).hexdigest(),'base_unchanged':hashlib.sha256(Path(scope['base']).read_bytes()).hexdigest()==scope['base_sha256'],'all13_native_export_reopen_equal':True,'other10frames_exact':True,'scope_and_body_protection':checks['all_other_cels_exact'],'palette_timing_layers_chunks_exact':True,'gif_checks':gifchecks,'runtime':'not run; scoped pose repair; no gameplay validation claimed','validate_tool':'advertised but not exposed; independent checks used'}
(R/'review/verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
