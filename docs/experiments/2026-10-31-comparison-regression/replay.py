"""Read-only historical replay. Writes diagnostic copies/evidence only in this experiment."""
from pathlib import Path
import argparse,hashlib,json,sys,shutil
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
PRIOR=ROOT.parent/'2026-10-30-tote-attack'
sys.path[:0]=[str(REPO/'tools/pixel-art-director/scripts'),str(ROOT.parent/'2026-10-30-evidence-idle-four-model/sol61')]
from comparison_review import build_packet,verify_packet
from native_read import read,composite

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def require(condition, message):
 if not condition:raise RuntimeError(message)

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--out',type=Path,default=ROOT/'replay')
 out=parser.parse_args().out.resolve()
 if out.exists():raise FileExistsError('Preserve prior replay; choose another diagnostic run.')
 out.mkdir()
 locations={'before.png':PRIOR/'artist/sol-rescue/preparation/frame-09-base.png',
            'candidate.png':PRIOR/'artist/sol-rescue/frames/v03-frame-8.png',
            'unregistered-before.png':PRIOR/'artist/checkpoints/recovery-source-v00.png'}
 for name,source in locations.items():shutil.copyfile(source,out/name)
 native=PRIOR/'artist/sol-rescue/source/tote-attack-v03.aseprite'
 decoded=composite(read(native),8)
 with Image.open(out/'candidate.png') as im:
  require(decoded.tobytes()==im.convert('RGBA').tobytes(),'Native F9/export mismatch')
 (out/'native-readback.json').write_text(json.dumps({'native_sha256':sha(native),'frame_1based':9,
  'candidate_png_sha256':sha(out/'candidate.png'),'native_composite_equal_png':True,
  'scope':'Read-only F9 composite equality; no native mutation or new animation approval.'},indent=2)+'\n')
 evidence=[{'role':'candidate native','path':str(native)},
           {'role':'fresh read-only native/export proof','path':'native-readback.json'},
           {'role':'adjacent F8','path':str(PRIOR/'artist/sol-rescue/frames/v03-frame-7.png')},
           {'role':'adjacent F10','path':str(PRIOR/'artist/sol-rescue/frames/v03-frame-9.png')}]
 narrow=Image.new('L',(320,192),0);d=ImageDraw.Draw(narrow);d.rectangle((140,55,224,149),fill=255)
 narrow.save(out/'narrow-diagnostic-mask.png')
 complete=Image.new('L',(320,192),0);d=ImageDraw.Draw(complete)
 d.rectangle((140,55,224,164),fill=255);d.rectangle((155,0,169,2),fill=255)
 complete.save(out/'complete-diagnostic-mask.png')
 spec={'baseline_role':'diagnostic source-derived pre-repair F9; not approved art',
       'registration':'Same320x192 source-part composite from build_native_inputs.py; no fitting. '
                      'Masks are retrospective diagnostic scope, not original authorization.',
       'required_frame_ids':['F9'],'evidence':evidence,'allow_new_colors':True,
       'frames':[{'id':'F9','before':'before.png','after':'candidate.png',
                  'mask':'narrow-diagnostic-mask.png',
                  'regions':[{'name':'arms-grip-handles-target','crop':[140,55,225,150]}]}],'zoom':4}
 def build(name,data):
  path=out/f'{name}.json';path.write_text(json.dumps(data,indent=2)+'\n')
  return build_packet(path,out/name)
 narrow_report=build('target-only',spec)
 require(not narrow_report['mechanical_passed'],'Narrow packet should fail')
 require(narrow_report['frames'][0]['uncovered_changes']['count']==30,'Expected30uncovered changes')
 spec['frames'][0]['mask']='complete-diagnostic-mask.png'
 spec['frames'][0]['regions']=[{'name':'arms-grip-handles-rim-and-bag','crop':[140,55,225,165]},
                              {'name':'curl-tip-change','crop':[155,0,170,3]}]
 complete_report=build('complete',spec)
 require(complete_report['mechanical_passed'] and complete_report['visual_acceptance']=='pending','Complete bookkeeping must pass with visual pending')
 require(verify_packet(out/'complete/packet.json')['fresh'],'Packet sources are stale')
 spec['frames'][0]['before']='unregistered-before.png'
 try:build('unregistered',spec)
 except ValueError as e:unregistered=str(e)
 else:raise AssertionError('Unregistered historical pair was not rejected')
 require('canvas mismatch' in unregistered,'Wrong unregistered-pair failure')
 report={'narrow_changed_pixels':narrow_report['frames'][0]['checks']['changed_pixels'],
         'narrow_outside_scope_pixels':narrow_report['frames'][0]['checks']['outside_mask_changed_pixels'],
         'narrow_uncovered_changes':narrow_report['frames'][0]['uncovered_changes'],
         'complete_mechanical_passed':True,'visual_acceptance':'pending',
         'historical_user_disposition':'rejected grip; known label, not automatic discovery',
         'unregistered_pair_refusal':unregistered,'complete_packet_sha256':sha(out/'complete/packet.json'),
         'limits':'Retrospective diagnostic scopes; F9 only, not whole-animation clearance. '
                  'Native and source art unchanged. New-RGB allowed in this diagnostic; not a production palette decision.'}
 (out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
