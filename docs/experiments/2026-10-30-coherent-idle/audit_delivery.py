"""Read-only audit of this task's delivered comparison/runtime/protected history."""
from pathlib import Path
import json,hashlib,sys,difflib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'source')]
from prepare import PLAN,A
from native_read import read,composite
from build_delivery import rgb
from gif_timeline import check as gif_check

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
 n=read(ROOT/'source/coherent-idle-v02.aseprite');times=[p[1] for p in PLAN]
 # Independent pixel-and-time comparison for the displayed two-panel artifact.
 expected=[]
 for f in range(8):
  pair=Image.new('RGBA',(272,212),'#34363a');pair.alpha_composite(composite(A,f),(0,20));pair.alpha_composite(composite(n,f),(144,20));d=ImageDraw.Draw(pair);d.fontmode='1';d.text((5,4),'Original Sol 6.1',fill='white');d.text((149,4),'Coherent v02',fill='white');expected.append(pair.convert('RGB').resize((816,636),Image.Resampling.NEAREST))
 gif_check(ROOT/'review/comparison-3x.gif',expected,times)
 # Actual rendered opaque character pixels equal source at the declared root.
 rendered=[]
 for f in range(8):
  with Image.open(ROOT/f'godot-preview/evidence/runtime-frame-{f:02d}.png') as capture:image=capture.convert('RGB')
  frame=composite(n,f);different=[]
  for y in range(192):
   for x in range(128):
    pixel=frame.getpixel((x,y))
    if pixel[3] and image.getpixel((x+88,y+69))!=pixel[:3]:different.append([x,y])
  assert not different,(f,different[:8]);rendered.append({'frame':f+1,'opaque_pixels_equal_native':True})
 runtime=json.loads((ROOT/'godot-preview/evidence/coherent-runtime.json').read_text());assert runtime['loops']>=3
 assert sorted({e['frame'] for e in runtime['events']})==list(range(8))
 assert all(e['root']==[88.0,69.0] for e in runtime['events'])
 events=runtime['events'];starts=[e['time_ms'] for e in events if e['frame']==0]
 observed_cycles=[b-a for a,b in zip(starts,starts[1:])]
 # Preserve expected task docs separately from all untouched historical files.
 before=json.loads((ROOT/'baseline/preserved-files.json').read_text());allowed={'docs/art/motion-guide.md','tools/pixel-art-director/references/animation.md','docs/handoff.md'}
 changed=[p for p,digest in before.items() if not (REPO/p).is_file() or sha(REPO/p)!=digest]
 unexpected=[p for p in changed if p not in allowed];assert not unexpected,unexpected
 patch=''
 for name,target in [('animation.md','tools/pixel-art-director/references/animation.md'),('motion-guide.md','docs/art/motion-guide.md'),('handoff.md','docs/handoff.md')]:
  patch+=''.join(difflib.unified_diff((ROOT/'baseline'/name).read_text().splitlines(True),(REPO/target).read_text().splitlines(True),fromfile='task-start/'+target,tofile=target))
 (ROOT/'review/task-docs.patch').write_text(patch)
 report={'comparison_native_pixels_and_timeline_exact':True,'comparison_gif_sha256':sha(ROOT/'review/comparison-3x.gif'),'runtime_rendered_frames':rendered,'runtime_cycle_intervals_ms':observed_cycles,'runtime_loops':runtime['loops'],'preserved_files_checked':len(before),'intentional_maintained_file_changes':changed,'unexpected_original_changes':unexpected,'all_four_original_experiments_preserved':True,'limits':'Runtime execution/pixel evidence; not continuous agent temporal perception or user artistic approval.'}
 (ROOT/'delivery-audit.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='runtime_rendered_frames'},indent=2))
if __name__=='__main__':main()
