from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path('docs/experiments/2026-10-30-quiet-chest-idle-sol/reddit-motion-study/eased-connected-idle');m=json.loads((P/'proof/timing-map.json').read_text());times=m['durations_ms'];n=len(times)
def matte(im):
 bg=Image.new('RGBA',im.size,(48,50,57,255));bg.alpha_composite(im.convert('RGBA'));return bg.convert('RGB')
frames=[matte(Image.open(P/f'frame-{i}.png'))for i in range(n)];colors=sorted(set(c for im in frames for c in im.get_flattened_data()));assert len(colors)<=256
palette=[v for c in colors for v in c]+[0]*(768-3*len(colors));ids={c:i for i,c in enumerate(colors)}
def gif(ims,path):
 ps=[]
 for im in ims:
  q=Image.new('P',im.size);q.putpalette(palette);q.putdata([ids[c]for c in im.get_flattened_data()]);ps.append(q)
 # Low-level writer preserves explicit hold frames too; no identical-frame merging.
 from PIL import GifImagePlugin
 with open(path,'wb')as f:
  for block in GifImagePlugin.getheader(ps[0],info={'loop':0})[0]:f.write(block)
  for q,duration in zip(ps,times):
   for block in GifImagePlugin.getdata(q,duration=duration,disposal=2):f.write(block)
  f.write(b';')
 actual=Image.open(path);assert actual.n_frames==n
 for i,im in enumerate(ims):actual.seek(i);assert actual.convert('RGB').tobytes()==im.tobytes() and actual.info['duration']==times[i]
for scale in[1,3]:gif([im.resize((128*scale,192*scale),Image.Resampling.NEAREST)for im in frames],P/f'proof/neutral-{scale}x.gif')
for scale,cols in[(1,6),(3,4)]:
 out=Image.new('RGB',(128*scale*cols,(192*scale+35)*(n//cols)),(48,50,57));d=ImageDraw.Draw(out)
 for i,im in enumerate(frames):
  x=i%cols*128*scale;y=i//cols*(192*scale+35);out.paste(im.resize((128*scale,192*scale),Image.Resampling.NEAREST),(x,y+35));d.text((x+3,y+4),f'F{i+1} {times[i]}ms',fill='white');d.text((x+3,y+18),m['phases'][i],fill='white')
 out.save(P/f'proof/contact-{scale}x.png')
out=Image.new('RGB',(4*390,3*430),(225,225,225));d=ImageDraw.Draw(out)
for i in range(n):
 im=Image.open(P/f'frame-{i}.png').convert('RGBA');bg=Image.new('RGBA',im.size,(225,225,225,255));bg.alpha_composite(im);out.paste(bg.convert('RGB').crop((34,58,99,125)).resize((390,402),Image.Resampling.NEAREST),(i%4*390,i//4*430+28));d.text((i%4*390+4,i//4*430+5),f'F{i+1} {m["phases"][i]} {times[i]}ms',fill='black')
out.save(P/'proof/hip-contact-6x.png')
# Separate cycles retain their own timing; phase-pair stills make comparison explicit.
oldP=P.parent/'prototype';out=Image.new('RGB',(768,606),(48,50,57));d=ImageDraw.Draw(out)
for k,p in enumerate([oldP/'frame-2.png',P/'frame-4.png']):out.paste(matte(Image.open(p)).resize((384,576),Image.Resampling.NEAREST),(k*384,30))
d.text((4,8),'Old peak F3 / loop2.53s',fill='white');d.text((388,8),'New turnaround F5 / loop3.95s',fill='white');out.save(P/'proof/old-new-phase-comparison.png')
chart=Image.new('RGB',(1300,320),(245,245,245));d=ImageDraw.Draw(chart);d.text((12,8),'New cycle3.95s — timings are authored; reference video timing is separate',fill='black');start=0
for i,t in enumerate(times):
 x=130+int(start/3950*1150);x2=130+int((start+t)/3950*1150);d.rectangle((x,32,x2,57),fill=(130,165,190)if i%2 else(170,195,210),outline='white');d.text((x,62),str(i+1),fill='black');start+=t
for r,(name,states,col)in enumerate([('Head up1px',[0,0,1,1,1,1,0,0,0,0,0,0],(90,120,155)),('Chest response',[0,1,1,1,1,1,1,0,0,0,0,0],(110,145,100)),('Pelvis/upperleg',[0,0,0,1,1,1,1,1,0,0,0,0],(175,125,90))]):
 d.text((12,94+r*45),name,fill='black');start=0
 for state,t in zip(states,times):
  if state:d.rectangle((130+int(start/3950*1150),90+r*45,130+int((start+t)/3950*1150),116+r*45),fill=col)
  start+=t
for i,(phase,t)in enumerate(zip(m['phases'],times)):d.text((12+(i%4)*320,235+(i//4)*24),f'{i+1}. {phase}: {t}ms',fill='black')
chart.save(P/'proof/timing-chart.png');(P/'proof/gif-checks.json').write_text(json.dumps({'frames':n,'all_frames_exact':True,'durations_ms':times,'shared_colors':len(colors),'loop':0},indent=2)+'\n');print('Actual 1x/3x GIFs, body/hip contacts and timing chart ready')
