"""Exact visible-timeline verification for delivered GIFs, with scoped file reads."""
from pathlib import Path
import hashlib
from PIL import Image

def check(path, frames, times, scale=1):
 path=Path(path);decoded=[];gif_times=[]
 assert frames and len(frames)==len(times) and all(t>0 for t in times)
 size=(frames[0].width*scale,frames[0].height*scale)
 with Image.open(path) as gif:
  loop=gif.info.get('loop')
  assert loop==0,'GIF must loop indefinitely'
  for f in range(gif.n_frames):
   gif.seek(f);decoded.append(gif.convert('RGB'));gif_times.append(gif.info['duration'])
 assert all(im.size==size for im in decoded),'GIF dimensions differ'
 assert all(t>0 for t in gif_times),'GIF has nonpositive duration'
 assert sum(times)==sum(gif_times),'GIF cycle duration differs'
 bg=decoded[0].getpixel((0,0));expected=[]
 for frame in frames:
  matte=Image.new('RGBA',frame.size,(*bg,255));matte.alpha_composite(frame.convert('RGBA'))
  expected.append(matte.convert('RGB').resize(size,Image.Resampling.NEAREST))
 a=b=used_a=used_b=0
 while a<len(expected) and b<len(decoded):
  assert expected[a].tobytes()==decoded[b].tobytes(),'GIF pixels differ on timeline'
  step=min(times[a]-used_a,gif_times[b]-used_b);used_a+=step;used_b+=step
  if used_a==times[a]:a+=1;used_a=0
  if used_b==gif_times[b]:b+=1;used_b=0
 assert a==len(expected) and b==len(decoded),'GIF timeline incomplete'
 return {'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'encoded_frames':len(decoded),'durations_ms':gif_times,'cycle_ms':sum(gif_times),'loop':loop,'matte_rgb':bg,'timeline_equals_native':True}
