"""Create faithful review GIFs/contact sheets from real native MCP exports."""
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'2026-10-30-coherent-idle'))
from gif_timeline import check as check_gif
MATTE='#34363a'

def matte(im):
 out=Image.new('RGBA',im.size,MATTE);out.alpha_composite(im.convert('RGBA'));return out.convert('RGB')

def encode(path,frames,times,scale):
 colors=sorted({c for frame in frames for c in matte(frame).get_flattened_data()});assert len(colors)<=256
 lookup={c:i for i,c in enumerate(colors)};palette=[v for c in colors for v in c]+[0]*(768-3*len(colors));images=[]
 for frame in frames:
  rgb=matte(frame);indexed=Image.new('P',rgb.size);indexed.putpalette(palette);indexed.putdata([lookup[c] for c in rgb.get_flattened_data()]);images.append(indexed.resize((rgb.width*scale,rgb.height*scale),Image.Resampling.NEAREST))
 images[0].save(path,save_all=True,append_images=images[1:],duration=times,loop=0,optimize=False,disposal=2)
 return check_gif(path,frames,times,scale)

def main():
 folder=ROOT/'artist';delivery=json.loads((folder/'delivery.json').read_text());frames=[]
 for p in delivery['frames']:
  with Image.open(folder/p) as im:frames.append(im.convert('RGBA'))
 times=delivery['durations_ms'];canvas=tuple(delivery['canvas']);target=ROOT/'review';target.mkdir(exist_ok=True)
 checks={}
 for scale in [1,3]:checks[f'{scale}x']=encode(target/f'attack-{scale}x.gif',frames,times,scale)
 columns=4;rows=(len(frames)+columns-1)//columns;contact=Image.new('RGB',(canvas[0]*columns,(canvas[1]+32)*rows),MATTE);d=ImageDraw.Draw(contact);d.fontmode='1'
 for f,frame in enumerate(frames):
  x=f%columns*canvas[0];y=f//columns*(canvas[1]+32);contact.paste(matte(frame),(x,y+32));d.text((x+3,y+3),f'F{f+1} | {times[f]} ms'+(' | ACTIVE' if f+1 in delivery['active_frames_1based'] else ''),fill='white');d.text((x+3,y+16),delivery['phases'][f],fill='white')
 contact.save(target/'contact-1x.png');contact.resize((contact.width*2,contact.height*2),Image.Resampling.NEAREST).save(target/'contact-2x.png')
 recovery=next(i for i,name in enumerate(delivery['phases']) if 'controlled' in name.lower() or name.lower()=='recovery')
 seed=folder/'checkpoints/recovery-source-v00.png'
 if seed.exists():
  with Image.open(seed) as im:before=im.convert('RGBA')
  pair=Image.new('RGB',(canvas[0]*2+16,canvas[1]+32),MATTE);pair.paste(matte(before),(0,32));pair.paste(matte(frames[recovery]),(canvas[0]+16,32));d=ImageDraw.Draw(pair);d.fontmode='1';d.text((4,5),'Generated middle pose: converted seed',fill='white');d.text((canvas[0]+20,5),'Native recovery repair',fill='white');pair.save(target/'recovery-before-after-1x.png');pair.resize((pair.width*3,pair.height*3),Image.Resampling.NEAREST).save(target/'recovery-before-after-3x.png')
 (target/'gif-verification.json').write_text(json.dumps(checks,indent=2)+'\n')
 (target/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Tote attack prototype review</title><style>body{background:#24262a;color:#f1f1eb;font:16px system-ui;margin:24px}img{image-rendering:pixelated;display:block;margin:12px 0}a{color:#a9d3ff}p{max-width:850px;line-height:1.5}.zoom{max-width:100%;height:auto}</style><h1>Tote swing attack — candidate for your review</h1><p>Native-size and3× nearest-neighbor display, both at authored speed. This preview loops for inspection; the Godot attack is a one-shot that returns to idle. No motion blur or hit effects are baked into the character.</p><h2>Native size · actual speed</h2><img src="attack-1x.gif" alt="Native attack playback"><h2>3× display · actual speed</h2><img class="zoom" src="attack-3x.gif" alt="Enlarged attack playback"><p>Review the shared grip, bag arc, elbow bend, braking foot and return to shoulder. File/native/runtime checks do not establish artistic approval.</p><p><a href="contact-1x.png">Contact with durations</a> · <a href="recovery-before-after-3x.png">Recovery before/after</a> · <a href="../record.md">Evidence and limits</a></p></html>''')
 print(json.dumps({'frames':len(frames),'cycle_ms':sum(times),'gif_checks':checks},indent=2))
if __name__=='__main__':main()
