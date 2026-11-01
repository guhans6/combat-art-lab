"""Read-only preservation and independent native revision proof; no native writes."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
sys.path.insert(0,str(ROOT.parent/'2026-10-30-evidence-idle-four-model/sol61'))
from native_read import read,composite

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
 intentional={'docs/handoff.md','docs/art/motion-guide.md','tools/pixel-art-director/references/adapters.md','tools/pixel-art-director/references/animation.md'}
 baseline=json.loads((ROOT/'baseline/preserved-files.json').read_text())
 changed=[p for p,h in baseline.items() if not (REPO/p).is_file() or sha(REPO/p)!=h]
 assert not set(changed)-intentional,changed
 attempts={}
 for name in ['luna','terra']:
  frozen=json.loads((ROOT/f'baseline/{name}-artist-handoff-hashes.json').read_text())
  assert all((ROOT/p).is_file() and sha(ROOT/p)==h for p,h in frozen.items()),name
  attempts[name]={'files':len(frozen),'unchanged':True}
 inputs=json.loads((ROOT/'inputs/manifest.json').read_text())
 assert all(sha(ROOT/'inputs'/p)==v['sha256'] for p,v in inputs.items())
 folder=ROOT/'artist/sol-rescue'
 native=read(folder/'source/tote-attack-v03.aseprite')
 revision=read(folder/'source/tote-fold-v03-revision-proof.aseprite')
 assert native['canvas']==revision['canvas'] and native['layers']==revision['layers'] and native['frames']==revision['frames']
 assert set(native['cels'])==set(revision['cels'])
 changed_cels=[]
 for key,cel in native['cels'].items():
  other=revision['cels'][key]
  if cel['image'].tobytes()!=other['image'].tobytes():changed_cels.append(list(key))
 assert changed_cels==[[8,4]],changed_cels
 a=composite(native,8);b=composite(revision,8)
 pixels=[(x,y) for y in range(a.height) for x in range(a.width) if a.getpixel((x,y))!=b.getpixel((x,y))]
 assert len(pixels)==20 and all(184<=x<190 and 121<=y<131 for x,y in pixels)
 report={'passed':True,'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),'historical_files':len(baseline),'historical_files_unchanged':len(baseline)-len(changed),'intentional_maintained_changes':changed,'prior_attempts':attempts,'frozen_inputs_unchanged':len(inputs),'native_sha256':sha(folder/'source/tote-attack-v03.aseprite'),'duplicate_revision':{'changed_cels_0based':changed_cels,'changed_visible_pixels':len(pixels),'other_cels_exact':True},'limits':'Byte preservation and native editability evidence only; no artistic approval.'}
 (ROOT/'preservation-verification.json').write_text(json.dumps(report,indent=2)+'\n')
 manifest={str(p.relative_to(ROOT)):sha(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and not any(part in {'.godot','__pycache__'} for part in p.relative_to(ROOT).parts) and p.name!='artifact-manifest.json'}
 (ROOT/'artifact-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
