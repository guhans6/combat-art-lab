#!/usr/bin/env python3
"""Prepare fixed-scale source pose frames for MCP-native assembly.

Only transforms/alpha-threshold/palette mapping happen here. Native Aseprite
structure, frame timings, layers, drawing edits, save/reopen and exports use the
Aseprite AI Artist MCP.
"""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
INPUTS=ROOT/'inputs'; ART=Path(__file__).resolve().parent
OUT=ART/'source-frames'
CANVAS=(256,192)
TIMINGS=[220,110,140,210,70,60,90,110,140,170,140,160,220]
PHASES=['ready idle','pickup','shared grip','counter-windup','acceleration','committed contact','follow-through','arrest and redirect','controlled recovery','tote settle','re-shoulder','release and settle','ready idle return']
# Source panels: exact row-major user sheets, with one scale/offset per family.
MAP=[('neutral',None),('six',2),('six',3),('additional',1),('six',3),('six',4),('six',5),('six',3),('additional',2),('additional',2),('additional',3),('six',6),('neutral',None)]
# Traced source-sheet spill on six-key panel 5, after common-scale projection.
SPILL_MAIN5=(0,45,12,87)


def rgb(s):
 s=s.lstrip('#')
 if len(s)==8 and int(s[6:],16)==0:return None
 if len(s) not in (6,8):return None
 return tuple(int(s[i:i+2],16) for i in (0,2,4))
@lru_cache(maxsize=100000)
def nearest(c,pal):
 r,g,b=c
 return min(pal,key=lambda q:2*(r-q[0])**2+4*(g-q[1])**2+3*(b-q[2])**2)
def panel(path,columns,rows,index):
 im=Image.open(path).convert('RGBA')
 x0=round((index%columns)*im.width/columns);x1=round((index%columns+1)*im.width/columns)
 y0=round((index//columns)*im.height/rows);y1=round((index//columns+1)*im.height/rows)
 return im.crop((x0,y0,x1,y1))
def palette_map(im,pal):
 pix=im.load();
 for y in range(im.height):
  for x in range(im.width):
   r,g,b,a=pix[x,y]
   pix[x,y]=(0,0,0,0) if a<128 else (*nearest((r,g,b),pal),255)
 return im

def main():
 raw=json.loads((ART/'seed-palette.json').read_text())
 pal=tuple(dict.fromkeys(c for v in raw if (c:=rgb(v)) is not None))
 neutral=Image.open(INPUTS/'neutral.png').convert('RGBA')
 six=INPUTS/'six-keys.png'; add=INPUTS/'additional-keys.png'
 OUT.mkdir(parents=True,exist_ok=True)
 frames=[]; infos=[]
 for frame,(family,idx) in enumerate(MAP,1):
  if family=='neutral':
   im=Image.new('RGBA',CANVAS,(0,0,0,0)); im.alpha_composite(neutral,(64,0))
   meta={'source':'neutral.png','transform':'exact original layer composite translated +64px x','scale':1.0,'offset_xy':[64,0]}
  elif family=='six':
   p=panel(six,3,2,idx-1)
   # One frozen scale per six-key family; fitted once to the source panel grid.
   p=p.resize(CANVAS,Image.Resampling.NEAREST)
   # The middle follow-through panel contains 405 stray pixels from the adjacent
   # strike panel along its left border. Remove this spatially reviewed spill.
   spill=0
   if idx==5:
    q=p.load()
    for y in range(SPILL_MAIN5[1],SPILL_MAIN5[3]):
     for x in range(SPILL_MAIN5[0],SPILL_MAIN5[2]):
      if q[x,y][3]>=128:q[x,y]=(0,0,0,0);spill+=1
   im=palette_map(p,pal)
   meta={'source':'six-keys.png','panel_index_1based':idx,'shared_scale':256/panel(six,3,2,0).width,'panel_mapping':'each equal grid panel mapped to 256x192 at nearest-neighbour','offset_xy':[0,0],'reviewed_spill_mask_xyxy':list(SPILL_MAIN5) if idx==5 else None,'spill_pixels_removed':spill}
  else:
   p=panel(add,3,1,idx-1)
   p=p.resize((round(p.width*.264),round(p.height*.264)),Image.Resampling.NEAREST)
   im=Image.new('RGBA',CANVAS,(0,0,0,0)); im.alpha_composite(p,(50,-2))
   q=im.load();spill=0
   # Same local lower-left panel spill mask used by the v03 recovery proof.
   if idx==1:
    for y in range(167,190):
     for x in range(50,57):
      if q[x,y][3]>=128:q[x,y]=(0,0,0,0);spill+=1
   im=palette_map(im,pal)
   meta={'source':'additional-keys.png','panel_index_1based':idx,'shared_scale':.264,'source_root_foot_xy':[310,708],'target_root_foot_xy':[132,185],'offset_xy':[50,-2],'reviewed_spill_mask_canvas_xyxy':[50,167,57,190] if idx==1 else None,'spill_pixels_removed':spill}
  # Binary alpha is required by the neutral sprite/export and exact GIF route.
  a=im.getchannel('A').point(lambda v:255 if v>=128 else 0);im.putalpha(a)
  pth=OUT/f'frame-{frame:02d}.png';im.save(pth);frames.append(im)
  b=im.getchannel('A').getbbox()
  meta.update({'frame':frame,'phase':PHASES[frame-1],'duration_ms':TIMINGS[frame-1],'canvas':list(CANVAS),'opaque_bbox_xyxy':list(b) if b else None,'unique_visible_rgb':len({px[:3] for px in im.getdata() if px[3]}),'alpha_values':sorted(set(im.getchannel('A').getdata()))})
  infos.append(meta)
 # Review sheet is a deterministic preview only, not a native export.
 sheet=Image.new('RGBA',(CANVAS[0]*4,CANVAS[1]*4),(20,20,20,255));d=ImageDraw.Draw(sheet)
 for i,im in enumerate(frames):
  x=(i%4)*CANVAS[0];y=(i//4)*CANVAS[1]
  sheet.alpha_composite(im,(x,y));d.text((x+2,y+2),f'{i+1:02} {PHASES[i]} {TIMINGS[i]}ms',fill=(255,255,255,255))
 sheet.save(ART/'checkpoints'/'attack-seed-contact-sheet.png')
 (OUT/'manifest.json').write_text(json.dumps({'canvas':list(CANVAS),'durations_ms':TIMINGS,'phases':PHASES,'source_frame_map':MAP,'per_frame':infos},indent=2)+'\n')
 print(json.dumps({'frames':len(frames),'palette_colors':len(pal),'source_colors':max(i['unique_visible_rgb'] for i in infos),'sheet':str(ART/'checkpoints'/'attack-seed-contact-sheet.png')}))
if __name__=='__main__':main()
