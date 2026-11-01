"""Comparison images only; this script never edits native artwork or sprite exports."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]/'art-runs/2026-10-26-gpt61-sol-pilot-01'
E=R/'evidence';BG='#343342'
f=lambda n:ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',n)
def backed(im):
 b=Image.new('RGBA',im.size,BG);b.alpha_composite(im.convert('RGBA'));return b.convert('RGB')
def fit(im,w,h):
 im=backed(im);ratio=min(w/im.width,h/im.height);return im.resize((int(im.width*ratio),int(im.height*ratio)),Image.Resampling.NEAREST)
base=Image.open(R/'input/baseline.png');final=Image.open(R/'work/candidate.png');rej=Image.open(R/'passes/pass-02.png')
close=Image.open(E/'primary-closeup-head.png');scene=Image.open(R/'input/reference-01-primary-design-and-style.png');scenehead=Image.open(E/'primary-scene-head-3x.png')
heads=[close,scenehead,base.crop((32,0,82,34)),final.crop((32,0,82,34))]
labels=['Primary close-up (crop)','Primary scene (crop)','v03 frozen baseline','Candidate: selected pass 01']
board=Image.new('RGB',(1664,368),BG);d=ImageDraw.Draw(board)
for i,(im,label) in enumerate(zip(heads,labels)):
 x=16+i*416;d.text((x,12),label,font=f(20),fill='white');tile=backed(im)
 ratio=min(400/im.width,296/im.height);tile=tile.resize((int(im.width*ratio),int(im.height*ratio)),Image.Resampling.NEAREST);board.paste(tile,(x,48))
d.text((16,347),'Reference crops fitted for comparison; artwork zoomed by integer nearest-neighbor. User likeness review pending.',font=f(15),fill='white');board.save(E/'reference-before-after-head.png')
full=Image.new('RGB',(1600,660),BG);d=ImageDraw.Draw(full)
for x,im,label,w in [(16,scene,'Primary approved scene',752),(800,base,'v03 baseline - 3x',384),(1200,final,'Candidate - 3x',384)]:
 d.text((x,12),label,font=f(20),fill='white');tile=fit(im,w,576);full.paste(tile,(x,52))
d.text((16,638),'Head-only trial: neck and body pixels are identical. No Godot/gameplay-scale validation performed.',font=f(17),fill='white');full.save(E/'reference-before-after-full.png')
allp=Image.new('RGB',(1264,370),BG);d=ImageDraw.Draw(allp)
for i,(im,label) in enumerate([(base,'Baseline'),(final,'Pass 01 - selected'),(rej,'Pass 02 - rejected hair cut')]):
 x=16+i*416;d.text((x,12),label,font=f(20),fill='white');allp.paste(backed(im.crop((32,0,82,34))).resize((400,272),Image.Resampling.NEAREST),(x,52))
allp.save(E/'all-checkpoints-head.png')
# Pixel-coordinate edit history, including invisible layer pixels and per-pass comparisons.
import sys,json
sys.path.insert(0,str(Path(__file__).parent));from check_native_pilot import read
nativebase=read(R/'input/baseline.aseprite');history=[]
for name in ['pass-01','pass-02']:
 a=read(R/f'passes/{name}.aseprite');changes=[]
 for key,cel in nativebase['cels'].items():
  old=list(cel['image'].get_flattened_data());new=list(a['cels'][key]['image'].get_flattened_data())
  for i,(b,c) in enumerate(zip(old,new)):
   if b!=c:changes.append({'layer':nativebase['layers'][key[1]]['name'],'frame':key[0]+1,'xy':[i%128,i//128],'before_rgba':b,'after_rgba':c})
 history.append({'checkpoint':name,'selected':name=='pass-01','native_changes_vs_frozen_baseline':changes})
(R/'evidence/edit-history.json').write_text(json.dumps(history,indent=2)+'\n')
