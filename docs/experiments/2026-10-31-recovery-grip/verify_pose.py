"""Independent read-only native/export/protection verification for the F9 pose proof."""
from pathlib import Path
import hashlib,json,sys
from PIL import Image
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
sys.path[:0]=[str(ROOT.parent/'2026-10-30-evidence-idle-four-model/sol61'),
              str(REPO/'tools/pixel-art-director/scripts'),str(ROOT.parent/'2026-10-30-tote-attack')]
from native_read import read,composite
from pixel_checks import canonical_pixels,read_mask,check_alpha_coverage
from verify_attack import palette_colors

def require(condition,message):
 if not condition:raise RuntimeError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
 artist=ROOT/'artist';delivery=json.loads((artist/'delivery.json').read_text())
 native=artist/delivery['native'];png=artist/delivery['png'];mask=artist/delivery['mask']
 frozen=json.loads((ROOT/'baseline/artist-pre-edit-scope.json').read_text())
 for relative,digest in frozen.items():require(sha(ROOT/relative)==digest,f'Pre-edit scope changed: {relative}')
 scope=json.loads((ROOT/'artist/scope.json').read_text())
 require(mask.resolve()==(ROOT/'artist/proof/allowed-mask.png').resolve(),'Different scope mask selected')
 require(set(delivery['allowed_layers_0based'])==set(scope['allowed_layers_0based']),'Owner scope changed')
 before=read(ROOT/'inputs/before.aseprite');after=read(native)
 require(before['canvas']==after['canvas']==[320,192],'Canvas changed')
 require(before['layers']==after['layers'],'Layer structure/settings changed')
 require(before['frames']==after['frames'],'Durations/palette/non-cel metadata changed')
 require(set(before['cels'])==set(after['cels']),'Native cel inventory changed')
 allowed=read_mask(mask,(320,192));owners=set(delivery['allowed_layers_0based'])
 changed=[]
 for key,old in before['cels'].items():
  new=after['cels'][key]
  metadata=['geometry','opacity','z','type']
  same=all(old[k]==new[k] for k in metadata) and old['small'].tobytes()==new['small'].tobytes()
  if same:continue
  frame,layer=key
  require(frame==8 and layer in owners,f'Protected native cel changed: {key}')
  op=canonical_pixels(old['image']);np=canonical_pixels(new['image'])
  changed_indices=[i for i,(a,b) in enumerate(zip(op,np)) if a!=b]
  require(all(allowed[i] for i in changed_indices),f'Native owner changed outside mask: {key}')
  changed.append({'frame_1based':9,'layer_0based':layer,'name':before['layers'][layer]['name'],
                  'changed_pixels':len(changed_indices)})
 require(changed,'No changed native cels')
 for frame in range(13):
  if frame!=8:require(composite(before,frame).tobytes()==composite(after,frame).tobytes(),f'Other pose changed F{frame+1}')
 old=composite(before,8);pose=composite(after,8)
 with Image.open(png) as im:exported=im.convert('RGBA')
 require(canonical_pixels(exported)==canonical_pixels(pose),'PNG visible RGBA differs from native F9')
 invisible_rgb=sum(p!=q for p,q in zip(pose.getdata(),exported.getdata()))
 with Image.open(artist/delivery['reopen_png']) as im:
  require(im.convert('RGBA').tobytes()==exported.tobytes(),'Fresh MCP reopen PNG differs from exported PNG')
 require(set(pose.getchannel('A').getdata())<={0,255},'Partial alpha')
 require({p[:3] for p in canonical_pixels(pose) if p[3]}<=palette_colors(before),'Off-palette RGB')
 b=canonical_pixels(old);a=canonical_pixels(pose)
 changed_indices=[i for i,(p,q) in enumerate(zip(b,a)) if p!=q]
 require(changed_indices and all(allowed[i] for i in changed_indices),'Composite mask failure or noop')
 for name,entry in json.loads((ROOT/'inputs/manifest.json').read_text()).items():
  require(sha(ROOT/'inputs'/name)==entry['sha256'],f'Frozen input changed: {name}')
 report={'passed':True,'native':str(native.relative_to(ROOT)),'native_sha256':sha(native),
         'png':str(png.relative_to(ROOT)),'png_sha256':sha(png),'mask_sha256':sha(mask),
         'changed_cels':changed,'composite_changed_pixels':len(changed_indices),
         'changed_bbox_xyxy':[min(i%320 for i in changed_indices),min(i//320 for i in changed_indices),
                               max(i%320 for i in changed_indices)+1,max(i//320 for i in changed_indices)+1],
         'all_other_12_poses_exact':True,'protected_owners_and_outside_mask_exact':True,
         'layer_structure_palette_timing_exact':True,'native_png_visible_RGBA_equal':True,
         'native_export_invisible_RGB_differences':invisible_rgb,'fresh_reopen_PNG_pixels_exact':True,
         'alpha_coverage_diagnostic':check_alpha_coverage(pose),
         'limits':'Pose-only technical proof. Alpha openings require visual review; no grip/anatomy or artistic approval inferred.'}
 (ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='alpha_coverage_diagnostic'},indent=2))
if __name__=='__main__':main()
