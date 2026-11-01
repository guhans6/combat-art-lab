"""Prepare native MCP drawing patches from the preserved Sol master.
Does not write native sources or animation PNGs. All changes applied in Aseprite.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]
sys.path.insert(0,str(ROOT.parent/'2026-10-30-evidence-idle-four-model/sol61'))
from native_read import read
A=read(ROOT/'baseline/sol-original.aseprite')
# One driver chooses a connected primary pose. No independent body-part clocks.
PLAN=[('rest',1100,0),('rise',180,1),('full',120,1),('full',360,1),
      ('full',220,1),('release',160,1),('rest',240,0),('rest',1000,0)]

def states():
 rest={l:A['cels'][(0,l)]['image'].copy() for l in range(len(A['layers']))}
 # Reuse the original Sol inhale key, including its collar coverage repair.
 # This is legitimate pose reuse, not a new image warp or layer-wide cutout move.
 core={l:A['cels'][(3,l)]['image'].copy() for l in rest}
 # Remove Sol's two-pixel fade. A fold does not vanish before the chest moves.
 for xy in [(60,55),(61,55)]:core[5].putpixel(xy,rest[5].getpixel(xy))
 full={l:im.copy() for l,im in core.items()}
 # Authored lower-rib fold tip: retain its two-pixel footprint and muted shadow
 # role, extending it one pixel within the shirt after the upper thorax rises.
 pale=(253,228,204,255);fold=(214,183,187,255)
 for x in [60,61]:
  assert core[5].getpixel((x,55))==fold
  assert core[5].getpixel((x,54))==pale
  full[5].putpixel((x,54),fold)
 return {'rest':rest,'rise':core,'full':full,'release':core}

def grid_patch(before,after):
 points=[(x,y) for y in range(192) for x in range(128) if before.getpixel((x,y))!=after.getpixel((x,y))]
 if not points:return None
 x0=min(x for x,y in points);x1=max(x for x,y in points)+1;y0=min(y for x,y in points);y1=max(y for x,y in points)+1
 colors=sorted({after.getpixel((x,y)) for x,y in points if after.getpixel((x,y))[3]})
 codes={c:chr(0x100+i) for i,c in enumerate(colors)}
 # Full target rectangle is intentional; transparent cells explicitly erase.
 allcolors=sorted({after.getpixel((x,y)) for y in range(y0,y1) for x in range(x0,x1) if after.getpixel((x,y))[3]})
 codes={c:chr(0x100+i) for i,c in enumerate(allcolors)}
 return {'kind':'grid','x':x0,'y':y0,'rows':[''.join(codes[after.getpixel((x,y))] if after.getpixel((x,y))[3] else '.' for x in range(x0,x1)) for y in range(y0,y1)],'legend':{v:'#%02x%02x%02x'%k[:3] for k,v in codes.items()},'transparent':'erase'}

def main():
 poses=states();calls=[]
 for f,(phase,ms,lift) in enumerate(PLAN):
  for l,target in poses[phase].items():
   op=grid_patch(A['cels'][(f,l)]['image'],target)
   if op:calls.append({'layer':A['layers'][l]['name'],'frame':f+1,'paletteLock':True,'label':f'coherent-v02 {phase} {A["layers"][l]["name"]}','ops':[op]})
 out={'baseline':'baseline/sol-original.aseprite','frames':[{'phase':s,'duration_ms':ms,'primary_lift_px':up} for s,ms,up in PLAN],'calls':calls}
 (ROOT/'source/operations.json').write_text(json.dumps(out,indent=2)+'\n')
 print('Prepared',len(calls),'native patches; cycle',sum(p[1] for p in PLAN),'ms')
if __name__=='__main__':main()
