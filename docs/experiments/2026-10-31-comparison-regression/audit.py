"""Audit source discovery, task-scoped preservation, local links and packet freshness."""
from pathlib import Path
import hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
sys.path.insert(0,str(REPO/'tools/pixel-art-director/scripts'))
from comparison_review import verify_packet

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def require(condition,message):
 if not condition:raise RuntimeError(message)

def main():
 baseline=json.loads((ROOT/'baseline/preserved-files.json').read_text())
 owned={'tools/pixel-art-director/SKILL.md','tools/pixel-art-director/references/animation.md',
        'tools/pixel-art-director/scripts/pixel_checks.py','docs/workflow/art-production.md',
        'docs/experiments/experiment-template.md','docs/art/motion-guide.md','docs/handoff.md'}
 changed=[p for p,h in baseline.items() if not (REPO/p).is_file() or sha(REPO/p)!=h]
 metadata=[p for p in changed if Path(p).name=='.DS_Store']
 unexpected=set(changed)-owned-set(metadata)
 require(not unexpected,f'Unexpected historical changes: {unexpected}')
 art=[p for p in baseline if Path(p).suffix.lower() in {'.png','.gif','.aseprite','.ase'}]
 require(all(sha(REPO/p)==baseline[p] for p in art),'Historical art/native changed')
 inputs=json.loads((ROOT/'inputs/manifest.json').read_text())
 require(all(sha(ROOT/'inputs'/p)==entry['sha256'] for p,entry in inputs.items()),'Frozen user crop changed')
 canonical=REPO/'tools/pixel-art-director'
 installed=REPO/'.agents/skills/pixel-art-director'
 require(installed.resolve()==canonical.resolve(),'Local skill is not canonical source')
 require((installed/'scripts/comparison_review.py').is_file(),'New helper not discoverable')
 documents=[ROOT/'record.md',ROOT/'research.md',ROOT/'review.md',
            canonical/'references/comparison-review.md',canonical/'SKILL.md',
            REPO/'docs/workflow/art-production.md',REPO/'docs/experiments/experiment-template.md',
            REPO/'docs/art/motion-guide.md',REPO/'docs/handoff.md']
 missing=[]
 for path in documents:
  for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
   if '://' in target or target.startswith('#'):continue
   if not (path.parent/target.split('#')[0]).exists():missing.append([str(path),target])
 require(not missing,f'Missing Markdown targets: {missing}')
 packets={}
 for folder in ['replay/target-only','replay/complete','replay-verified/target-only','replay-verified/complete']:
  result=verify_packet(ROOT/folder/'packet.json');require(result['fresh'],f'Stale packet: {folder}')
  require(result['visual_acceptance']=='pending','Mechanical verifier cleared art')
  packets[folder]=result
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
 require(head==(ROOT/'baseline/git-head.txt').read_text().strip(),'Git HEAD changed')
 for name in ['tests-final.log','standalone-tests.log']:
  text=(ROOT/name).read_text();require('Ran 42 tests' in text and text.rstrip().endswith('OK'),name)
 report={'passed':True,'git_head':head,'baseline_file_count':len(baseline),
         'intentional_existing_changes':sorted(set(changed)&owned),
         'unrelated_folder_metadata_drift_preserved':metadata,
         'historical_art_native_files_byte_exact':len(art),
         'all_other_baseline_files_unchanged':True,'source_and_standalone_tests':42,
         'local_canonical_skill_discovery':True,'local_markdown_targets_exist':True,
         'packets':packets,'official_skill_validator':'unavailable: bundled Python lacks PyYAML; Ruby YAML frontmatter parse passed',
         'limits':'Mechanical/source-local evidence only; visual-probe false clearance retained. No semantic judge, art approval, bundle refresh, installation elsewhere or publication.'}
 (ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 manifest={str(p.relative_to(ROOT)):sha(p) for p in sorted(ROOT.rglob('*')) if p.is_file()
           and '__pycache__' not in p.parts and p.name!='artifact-manifest.json'}
 (ROOT/'artifact-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='packets'},indent=2))
if __name__=='__main__':main()
