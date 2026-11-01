"""Check this character's declared pose/anchor contract, not naturalness.
CLI: bundled-python verify_contract.py [--native path] [--sheet path] [--gif path]
A different character/key plan requires a separately reviewed contract.
"""
from pathlib import Path
import argparse,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT.parents[2]),str(ROOT.parent/'2026-10-30-evidence-idle-four-model/sol61'),str(ROOT.parent/'2026-10-30-evidence-idle-four-model')]
from native_read import read,composite
from check_deliveries import coverage
from gif_timeline import check as gif_check

def inspect(native, sheet=None, gif_path=None):
 reference=read(ROOT/'baseline/sol-original.aseprite');data=read(native);errors=[]
 def require(ok,message):
  if not ok:errors.append(message)
 require(data['canvas']==[128,192],'canvas changed')
 require(len(data['frames'])==8,'expected eight frames')
 if data['canvas']!=[128,192] or len(data['frames'])!=8:return {'passed':False,'errors':errors}
 require(data['layers']==reference['layers'],'native layer metadata changed')
 times=[f['duration_ms'] for f in data['frames']]
 require(times==[1100,180,120,360,220,160,240,1000],'native timing differs from declared plan')
 base=composite(reference,0);frames=[composite(data,f) for f in range(8)]
 for f in range(8):
  # The corrected Sol key supplies the declared shoulder/collar shape. This
  # classifier accepts either rest or inhale; it does not require all pixels to
  # move equally. The shirt's delayed fold is intentionally outside this check.
  jacket=data['cels'][(f,3)]['image']
  if jacket.tobytes()==reference['cels'][(0,3)]['image'].tobytes():key=0
  elif jacket.tobytes()==reference['cels'][(3,3)]['image'].tobytes():key=3
  else:
   errors.append(f'F{f+1}: unreviewed primary shoulder pose');continue
  for l in [10,11]:
   require(data['cels'][(f,l)]['image'].tobytes()==reference['cels'][(key,l)]['image'].tobytes(),f'F{f+1}: {data["layers"][l]["name"]} disconnected from primary pose')
  for l in [0,1,2,6,8,9]:
   require(data['cels'][(f,l)]['image'].tobytes()==reference['cels'][(0,l)]['image'].tobytes(),f'F{f+1}: protected {data["layers"][l]["name"]} changed')
  require(frames[f].crop((0,90,128,192)).tobytes()==base.crop((0,90,128,192)).tobytes(),f'F{f+1}: lower-body anchor changed')
 require(frames[0].tobytes()==frames[-1].tobytes()==base.tobytes(),'loop does not return to exact rest')
 alpha=coverage(frames,base);require(alpha['passed'],'new enclosed body hole or partial alpha')
 if sheet:
  im=Image.open(sheet).convert('RGBA');require(im.size==(1024,192),'sheet dimensions changed')
  if im.size==(1024,192):
   for f,frame in enumerate(frames):require(im.crop((128*f,0,128*(f+1),192)).tobytes()==frame.tobytes(),f'F{f+1}: exported sheet differs from native')
 if gif_path:
  try:gif_check(Path(gif_path),frames,times,1)
  except AssertionError as exc:errors.append(str(exc) if str(exc)=='GIF must loop indefinitely' else f'GIF: {exc}')
 return {'passed':not errors,'errors':errors,'native':str(native),'limits':'Declared phase/anchor/coverage/export constraints only; anatomy quality and naturalness need visual review.'}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--native',type=Path,default=ROOT/'source/coherent-idle-v02.aseprite');p.add_argument('--sheet',type=Path);p.add_argument('--gif',type=Path);a=p.parse_args()
 report=inspect(a.native,a.sheet,a.gif);print(json.dumps(report,indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
