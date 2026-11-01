"""Prepare source-bound comparison and clean display derivatives, never alter source art."""
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
sys.path.insert(0,str(REPO/'tools/pixel-art-director/scripts'))
from comparison_review import build_packet,verify_packet
from pixel_checks import checkerboard

def main():
 artist=ROOT/'artist';delivery=json.loads((artist/'delivery.json').read_text())
 out=ROOT/'review'
 if out.exists():raise FileExistsError('Preserve old review; choose a fresh pass directory.')
 out.mkdir()
 spec={'baseline_role':'user-rejected native tote v03 F9; not approved art',
       'registration':'Exact same320x192 native frame9; no scaling/fitting/translation. '
                      'Native owner/frame/palette protection independently verified.',
       'required_frame_ids':['F9'],'zoom':6,
       'allow_new_colors':False,
       'color_policy':'Existing native palette and frame-local RGB set only; independently checked.',
       'evidence':[{'role':'candidate native','path':str(artist/delivery['native'])},
                   {'role':'independent native and fresh-reopen audit','path':'../verification.json'},
                   {'role':'pre-edit scope','path':str(artist/delivery['scope_record'])},
                   {'role':'parent frozen scope hashes','path':'../baseline/artist-pre-edit-scope.json'}],
       'frames':[{'id':'F9','before':'../inputs/before.png','after':str(artist/delivery['png']),
                  'mask':str(artist/delivery['mask']),
                  'regions':[{'name':'cuffs-wrists-grip-handles-and-rim','crop':[140,60,205,130]}]}]}
 path=out/'comparison.json';path.write_text(json.dumps(spec,indent=2)+'\n')
 report=build_packet(path,out/'packet')
 if not report['mechanical_passed']:raise RuntimeError('Comparison mechanical gate failed; inspect packet')
 if not verify_packet(out/'packet/packet.json')['fresh']:raise RuntimeError('Stale comparison evidence')
 with Image.open(ROOT/'inputs/before.png') as im:before=im.convert('RGBA')
 with Image.open(artist/delivery['png']) as im:after=im.convert('RGBA')
 bodycrop=(96,0,224,192);focus=(140,60,205,130);scale=6
 # Same-coordinate clean views; crop/nearest scaling only, no authored pixels changed.
 after.crop(bodycrop).resize((384,576),Image.Resampling.NEAREST).save(out/'corrected-pose-3x.png')
 after.save(out/'corrected-pose-native.png')
 width=focus[2]-focus[0];height=focus[3]-focus[1];column=max(320,width*scale)+24
 sheet=Image.new('RGB',(column*2,192+height*scale+90),(38,38,49));draw=ImageDraw.Draw(sheet)
 for index,(im,label) in enumerate([(before,'BEFORE - rejected F9'),(after,'AFTER - pose candidate')]):
  x=index*column+12;draw.text((x,8),label,fill='white')
  tile=checkerboard(im.size);tile.alpha_composite(im)
  sheet.paste(tile.convert('RGB'),(x,30))
  draw.text((x,234),'Same native crop; 6x nearest-neighbor',fill='white')
  sheet.paste(tile.crop(focus).resize((width*scale,height*scale),Image.Resampling.NEAREST).convert('RGB'),(x,254))
 draw.text((12,sheet.height-20),'Pose proof only. Full animation unchanged. User approval pending.',fill='white')
 sheet.save(out/'before-after.png')
 (out/'display-metadata.json').write_text(json.dumps({'body_crop_native_xyxy':bodycrop,
    'focus_crop_native_xyxy':focus,'focus_display_scale':scale,'pose_display_scale':3,
    'source_rgba_pixels_modified':False,'note':'Clean display derivatives only; packet contains exact-grid differences and hashes.'},indent=2)+'\n')
 print(json.dumps({'mechanical_passed':True,'visual_acceptance':'pending','review_folder':str(out)},indent=2))
if __name__=='__main__':main()
