from pathlib import Path
import sys,json,hashlib
from PIL import Image,ImageDraw
sys.path.insert(0,'docs/experiments/2026-10-30-evidence-idle-four-model/sol61')
from native_read import read,composite,rgba_equal,sha
R=Path('docs/experiments/2026-10-31-recovery-grip/artist')
B=Path('docs/experiments/2026-10-30-tote-attack/artist/sol-rescue/source/tote-attack-v03.aseprite')
a=read(B)
mask=Image.new('L',(320,192));d=ImageDraw.Draw(mask)
rects=[[163,77,184,94],[158,86,192,110]]
for x0,y0,x1,y1 in rects:d.rectangle([x0,y0,x1-1,y1-1],fill=255)
mask.save(R/'proof/allowed-mask.png')
record={'baseline':str(B),'baseline_sha256':sha(B),'mode':'isolated F9 pose candidate; full 13-frame native copy, no animation propagation','frame_1based':9,'frame_index_0based':8,'mask_rectangles_half_open':rects,'allowed_layers_0based':[2,4,5,6],'protected':'all other frames/cels, all other layers, all pixels outside mask, canvas/palette/timing/layer metadata','priority':'cuff to wrist to enclosed handle bundle to both rim attachments; compact shaped fingers, cream strap and warm skin material continuity','method':'native owner edits with dedicated MCP grid operations, read-only native decoder for checks; only exported F9 used for visual review','budget':'one main pass and at most two specific correction rounds','review_status':'awaiting candidate, independent review and user approval','layers':a['layers'],'cels_F9':{a['layers'][l]['name']:{k:v for k,v in c.items() if k not in ('image','small')} for (f,l),c in a['cels'].items() if f==8}}
(R/'scope.json').write_text(json.dumps(record,indent=2))
legend={'.':(0,0,0,0),'o':(120,55,28,255),'h':(252,175,128,255),'b':(253,169,119,255),'s':(234,147,104,255),'d':(228,133,88,255),'e':(144,71,44,255),'j':(57,54,40,255),'g':(82,76,52,255),'k':(75,71,50,255),'G':(102,94,58,255),'z':(200,104,63,255)}
rev={v:k for k,v in legend.items()}
for l in [2,4,5,6]:
 im=a['cels'][(8,l)]['image']; print(a['layers'][l]['name'])
 for y in range(77,95):print(y,''.join(rev.get(im.getpixel((x,y)),'?') for x in range(163,184)))
 crop=im.crop((150,65,200,115)).resize((600,600),Image.Resampling.NEAREST);crop.save(R/f'proof/baseline-layer-{l}.png')
# scratch exact one-pixel change is green->red; subsequent blue erase is independently checked
s0=read(R/'scratch/before.aseprite');s1=read(R/'scratch/after.aseprite')
assert all(rgba_equal(s0['cels'][key]['image'],s1['cels'][key]['image']) for key in s0['cels'] if key[1]!=2)
p0=composite(s0,0);p1=composite(s1,0)
changes=[(x,y) for y in range(16) for x in range(16) if p0.getpixel((x,y))!=p1.getpixel((x,y))]
assert changes==[(10,4),(9,5)] and rgba_equal(p1,Image.open(R/'scratch/reopen.png').convert('RGBA'))
(R/'scratch/checks.json').write_text(json.dumps({'asymmetric_pattern':'red triangle expands right/down at2,2; blue column9,4..5 greenpixel10,4','single_color_change_xy':[10,4],'transparent_skip_preserved_xy':[9,4],'erase_xy':[9,5],'protected_layer_exact':True,'save_reopen_export_exact':True,'changed_pixels_total_after_separate_erase':changes,'controlled_out_of_mask_detection':any(x!=10 or y!=4 for x,y in changes)},indent=2))
