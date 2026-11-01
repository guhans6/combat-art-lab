"""Prepare source-derived masks and literal pixel operations; never saves artwork.
Native editing/export is performed through the dedicated MCP by the artist.
"""
from pathlib import Path
import json
from PIL import Image,ImageDraw
from native_read import read
ROOT=Path(__file__).resolve().parent
INPUT=ROOT.parent/'inputs/neutral.aseprite'
A=read(INPUT)
BASE={l:A['cels'][(0,l)]['image'].copy() for l in range(len(A['layers']))}
# Each polygon is independently chosen from collar/shoulder/upper-arm landmarks.
# The sleeve wrists and pocket edge are outside these regions and remain fixed.
REGIONS={
 3:[(44,38),(49,35),(54,33),(59,34),(59,47),(54,49),(49,48),(45,50),(39,50),(39,46)],
 4:[(70,36),(80,36),(84,41),(86,45),(87,49),(83,51),(80,49),(76,48),(71,46)],
 5:[(50,39),(71,39),(75,43),(75,48),(70,50),(65,52),(58,51),(51,52)],
 7:[(72,35),(80,35),(82,42),(82,48),(80,51),(75,50),(72,45)]
}

def changed(src,dst):
 return [{'x':x,'y':y,'rgba':list(dst.getpixel((x,y)))} for y in range(192) for x in range(128) if src.getpixel((x,y))!=dst.getpixel((x,y))]

def lifted():
 out={l:im.copy() for l,im in BASE.items()}
 # Rigid head/neck, preserving all internal facial pixels exactly.
 for l in [10,11]:
  out[l]=Image.new('RGBA',(128,192));out[l].paste(BASE[l],(0,-1))
 for l,pts in REGIONS.items():
  src=BASE[l];dst=src.copy();m=Image.new('1',src.size);ImageDraw.Draw(m).polygon(pts,fill=1)
  selected={(x,y) for y in range(192) for x in range(128) if m.getpixel((x,y)) and src.getpixel((x,y))[3]}
  # Copy this locally rigid upper plane, leaving the rest of the cel intact.
  for x,y in selected:dst.putpixel((x,y),(0,0,0,0))
  for x,y in selected:dst.putpixel((x,y-1),src.getpixel((x,y)))
  # Reconstruct seam/overlap at the lower boundary using the continuing adjacent
  # material plane. This is constrained to vacancies, never fills outside anatomy.
  for x,y in selected:
   if not dst.getpixel((x,y))[3]:
    below=src.getpixel((x,min(y+1,191)))
    if below[3]:dst.putpixel((x,y),below)
  out[l]=dst
 return out

def patch(out,l,coords,color):
 for x,y in coords:
  assert out[l].getpixel((x,y))[3],(l,x,y)
  out[l].putpixel((x,y),color)

# Existing shirt fold roles, not a replacement material ramp.
PALE=(253,228,204,255);FOLD=(214,183,187,255)
def micro(base):
 out={l:im.copy() for l,im in base.items()}
 # Fade the leading edge of the short diagonal chest fold before the silhouette
 # changes. Coordinates are selected on that fold, not a whole garment recolour.
 for p in [(60,55),(61,55)]:
  if out[5].getpixel(p)==FOLD:out[5].putpixel(p,PALE)
 return out

def build():
 up=lifted();up=micro(up)
 # Upper shoulders lead the head by one short drawing; the retained rigid head
 # must meet the newly raised collar without new transparent cracks.
 shoulder={l:im.copy() for l,im in up.items()};shoulder[11]=BASE[11].copy();shoulder[10]=BASE[10].copy()
 states={'rest':BASE,'micro':micro(BASE),'shoulder':shoulder,'inhale':up}
 plan=[('rest',1100),('micro',180),('shoulder',120),('inhale',360),('inhale',220),('shoulder',160),('micro',240),('rest',1000)]
 payload={
 'source':str(INPUT),'method':'anatomical region copy plus seam reconstruction and targeted fold-edge changes',
 'regions':{str(k):v for k,v in REGIONS.items()},
 'frames':[{'state':s,'duration_ms':ms} for s,ms in plan],
 'states':{s:{str(l):changed(BASE[l],im) for l,im in layers.items() if changed(BASE[l],im)} for s,layers in states.items()}
 }
 (ROOT/'prepared-operations.json').write_text(json.dumps(payload,indent=2)+'\n')
 print({s:{l:len(p) for l,p in v.items()} for s,v in payload['states'].items()});print('duration',sum(ms for s,ms in plan))
 return states,plan
if __name__=='__main__':build()
