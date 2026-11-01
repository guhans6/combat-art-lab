from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol/reddit-motion-study/prototype');B=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol');times=[600,350,550,600,50,80,50,250]
def matte(im):
 bg=Image.new('RGBA',im.size,(48,50,57,255));bg.alpha_composite(im.convert('RGBA'));return bg.convert('RGB')
frames=[matte(Image.open(P/f'frame-{i}.png'))for i in range(8)];before=[matte(Image.open(B/f'frame-{i}.png'))for i in range(8)];colors=sorted(set(c for im in frames+before for c in im.get_flattened_data()));assert len(colors)<=256
palette=[v for c in colors for v in c]+[0]*(768-3*len(colors));ids={c:i for i,c in enumerate(colors)}
def gif(ims,path):
 ps=[]
 for im in ims:
  qi=Image.new('P',im.size);qi.putpalette(palette);qi.putdata([ids[c]for c in im.get_flattened_data()]);ps.append(qi)
 ps[0].save(path,save_all=True,append_images=ps[1:],duration=times,loop=0,disposal=2,optimize=False)
 actual=Image.open(path);assert actual.n_frames==8
 for i,im in enumerate(ims):actual.seek(i);assert actual.convert('RGB').tobytes()==im.tobytes() and actual.info['duration']==times[i]
for scale in [1,3]:gif([im.resize((128*scale,192*scale),Image.Resampling.NEAREST)for im in frames],P/f'proof/neutral-{scale}x.gif')
pairs=[]
for old,new in zip(before,frames):
 pair=Image.new('RGB',(768,576));pair.paste(old.resize((384,576),Image.Resampling.NEAREST));pair.paste(new.resize((384,576),Image.Resampling.NEAREST),(384,0));pairs.append(pair)
gif(pairs,P/'proof/cloth-left-coordinated-right-3x.gif')
for scale,cols in [(1,8),(3,4)]:
 out=Image.new('RGB',(128*scale*cols,(192*scale+24)*(8//cols)),(48,50,57));d=ImageDraw.Draw(out)
 for i,im in enumerate(frames):
  x=i%cols*128*scale;y=i//cols*(192*scale+24);out.paste(im.resize((128*scale,192*scale),Image.Resampling.NEAREST),(x,y+24));d.text((x+4,y+5),f'F{i+1} {times[i]}ms',fill='white')
 out.save(P/f'proof/contact-{scale}x.png')
out=Image.new('RGB',(4*408,2*480),(225,225,225));d=ImageDraw.Draw(out)
for i in range(8):
 im=Image.open(P/f'frame-{i}.png').convert('RGBA');bg=Image.new('RGBA',im.size,(225,225,225,255));bg.alpha_composite(im);out.paste(bg.convert('RGB').crop((29,0,97,76)).resize((408,456),Image.Resampling.NEAREST),(i%4*408,i//4*480+24));d.text((i%4*408+4,i//4*480+5),f'F{i+1}',fill='black')
out.save(P/'proof/upper-contact-6x.png')
(P/'proof/gif-checks.json').write_text(json.dumps({'all_frames_exact':True,'durations_ms':times,'shared_colors':len(colors),'loop':0},indent=2)+'\n');print('GIFs and contact sheets ready')
