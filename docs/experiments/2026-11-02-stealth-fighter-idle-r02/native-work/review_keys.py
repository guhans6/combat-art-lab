from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib
P=Path('/private/tmp/stealth-fighter-idle-r02');K=P/'keys';sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(K/'keys-final.aseprite');names=[l['name']for l in A['layers']];ims=[];points={'crown':(59,13),'chin':(70,41),'neck':(63,46),'near-shoulder':(43,59),'near-elbow':(37,96),'near-wrist':(45,130),'pelvis':(66,124),'sword-root':(79,102),'sole':(64,252)}
checks={'native_sha256':hashlib.sha256((K/'keys-final.aseprite').read_bytes()).hexdigest(),'keys':[]}
for k in range(3):
 parts={n:A['cels'].get((k,i),{}).get('image',Image.new('RGBA',(128,264)))for i,n in enumerate(names)};comp=Image.new('RGBA',(128,264))
 for n,im in parts.items():comp.alpha_composite(im);im.save(K/f'f{k}-owner-{n}.png')
 assert comp.tobytes()==Image.open(K/f'repaired-key-{k}.png').convert('RGBA').tobytes();ims.append(comp)
 for n in names:
  hide=Image.new('RGBA',(128,264))
  for other,q in parts.items():
   if n!=other:hide.alpha_composite(q)
  hide.save(K/f'f{k}-hide-{n}.png')
 assert comp.crop((0,153,128,264)).tobytes()==ims[0].crop((0,153,128,264)).tobytes()
 s={(x,y)for y in range(264)for x in range(128)if not comp.getpixel((x,y))[3]};holes=[]
 while s:
  q=[s.pop()];edge=False
  for x,y in q:
   edge|=x in(0,127)or y in(0,263)
   for v in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if v in s:s.remove(v);q.append(v)
  if not edge:holes.append(q)
 assert not holes
 marks={n:list(p)for n,p in points.items()}
 for n in['crown','chin','neck']:
  dx,dy=[(0,0),(0,-1),(-2,-2)][k];marks[n]=[marks[n][0]+dx,marks[n][1]+dy]
 for n in['near-elbow','near-wrist']:
  dx,dy=[(0,0),(-1,-1),(-2,-2)][k];marks[n]=[marks[n][0]+dx,marks[n][1]+dy]
 dx,dy=[(0,0),(0,-2),(-2,-4)][k];marks['near-shoulder']=[43+dx,59+dy]
 marked=Image.new('RGBA',comp.size,'#525760');marked.alpha_composite(comp);marked=marked.resize((384,792),Image.Resampling.NEAREST);d=ImageDraw.Draw(marked)
 for n,(x,y)in marks.items():d.ellipse((x*3-2,y*3-2,x*3+2,y*3+2),fill='#ffd078');d.text((x*3+4,y*3),n,fill='#ffd078')
 marked.save(K/f'f{k}-landmarks-3x.png');checks['keys'].append({'key':k,'holes':0,'native_matches_MCP':True,'y153_fixed':True,'landmarks':marks})
for sc in[1,3]:
 c=Image.new('RGBA',(128*sc*3,264*sc+28),'#525760');d=ImageDraw.Draw(c)
 for k,im in enumerate(ims):c.alpha_composite(im.resize((128*sc,264*sc),Image.Resampling.NEAREST),(128*sc*k,26));d.text((128*sc*k+6,6),['REST','transition','apex'][k],fill='white')
 c.convert('RGB').save(K/f'keys-{sc}x.png')
# Upper-body contrasting review exposes any remaining open gap; clean actual native pixels only.
c=Image.new('RGBA',(68*5*3,119*5+26),'#f03ab8');d=ImageDraw.Draw(c)
for k,im in enumerate(ims):
 q=Image.new('RGBA',(68,119),'#f03ab8');q.alpha_composite(im.crop((24,36,92,155)));c.alpha_composite(q.resize((340,595),Image.Resampling.NEAREST),(k*340,26));d.text((k*340+6,6),['REST','transition','apex'][k],fill='black')
c.convert('RGB').save(K/'upper-contrast-5x.png')
for owner in ['head-hair-neck','upper-torso','near-upper-sleeve','near-guard-hand','body-occlusion-backing','far-hand']:
 c=Image.new('RGBA',(340*3,595*3+26),'#697078');d=ImageDraw.Draw(c)
 for k in range(3):
  for col,kind in enumerate(['clean','owner','hide']):
   im=ims[k]if kind=='clean'else Image.open(K/f'f{k}-{kind}-{owner}.png').convert('RGBA');q=Image.new('RGBA',(68,119),'#697078');q.alpha_composite(im.crop((24,36,92,155)));c.alpha_composite(q.resize((340,595),Image.Resampling.NEAREST),(col*340,k*595+26));d.text((col*340+6,k*595+6),f'K{k} {kind} {owner}',fill='white')
 c.convert('RGB').save(K/f'ownership-{owner}-5x.png')
json.dump(checks,open(K/'checks.json','w'),indent=2)
# Original concept preview and exact native REST; concept resample is comparison-only.
src=Image.open('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/concepts/stealth-fighter/game-specific-r01/silver-pines/corrected.png').convert('RGBA').crop((300,88,732,1392)).resize((81,244),Image.Resampling.LANCZOS)
c=Image.new('RGBA',(128*3*2,264*3+28),'#525760');c.alpha_composite(src.resize((243,732),Image.Resampling.NEAREST),(24*3,10*3+26));c.alpha_composite(ims[0].resize((384,792),Image.Resampling.NEAREST),(384,26));ImageDraw.Draw(c).text((6,6),'Current A crop / preview resample | exact native REST',fill='white');c.convert('RGB').save(P/'inputs/source-native-rest-3x.png')
