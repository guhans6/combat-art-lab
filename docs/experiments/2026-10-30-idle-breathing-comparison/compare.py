from PIL import Image
from pathlib import Path
import json
r=Path(__file__).resolve().parent
roots=[r.parent/'2026-10-30-idle-breath-blink/luna/exports/pass01',r/'luna/exports/pass03',r/'terra']
frames=[]
for i in range(8):
 out=Image.new('RGB',(1152,576),'#303239')
 for n,d in enumerate(roots):
  im=Image.open(d/f'frame-{i}.png').convert('RGBA');m=Image.new('RGBA',im.size,'#303239');m.alpha_composite(im);out.paste(m.convert('RGB').resize((384,576),Image.Resampling.NEAREST),(384*n,0))
 frames.append(out)
colors=sorted(set(c for f in frames for c in f.getdata()));assert len(colors)<=256,len(colors)
lookup={c:i for i,c in enumerate(colors)};palette=[v for c in colors for v in c]+[0]*(768-len(colors)*3)
ps=[]
for f in frames:
 p=Image.new('P',f.size);p.putpalette(palette);p.putdata([lookup[c] for c in f.getdata()]);assert p.convert('RGB').tobytes()==f.tobytes();ps.append(p)
ds=[600,350,550,600,50,80,50,250]
p=r/'comparison-3x.gif';ps[0].save(p,save_all=True,append_images=ps[1:],duration=ds,loop=0,disposal=2,optimize=False)
g=Image.open(p);assert g.n_frames==8
for i,f in enumerate(frames):
 g.seek(i);assert g.convert('RGB').tobytes()==f.tobytes();assert g.info['duration']==ds[i]
frames[2].save(r/'peak-comparison.png')
(r/'comparison-checks.json').write_text(json.dumps({'columns':['Original current idle','Luna6 Max final attempt','Terra6.1 candidate'],'actual_frame_roots':list(map(str,roots)),'frames':8,'duration_ms':ds,'pixel_exact_composite':True,'palette_colors':len(colors)},indent=2)+'\n')
print({'frames':8,'palette_colors':len(colors),'exact':True})
