from pathlib import Path
from PIL import Image
import json,hashlib,re,datetime
H=Path(__file__).resolve().parent;R=H.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=json.loads((H/'pre-task-files.json').read_text())
allowed={'CONTEXT.md','docs/handoff.md','docs/art/style-guide.md','docs/art/asset-contract.md','docs/art/motion-guide.md','docs/workflow/art-production.md','docs/research/concept-to-native-pixel-art.md','tools/pixel-art-director/SKILL.md','tools/pixel-art-director/references/reconstruction.md','tools/pixel-art-director/references/craft.md'}
changed=[];unchanged=[];missing=[];bad=[]
for path,digest in prior.items():
 p=R/path
 if not p.is_file():missing.append(path)
 elif sha(p)!=digest:
  changed.append(path)
  if path not in allowed:bad.append(path)
 else:unchanged.append(path)
assert not missing and not bad,(missing,bad)
assert all(not x.startswith(('assets/','art-runs/','docs/experiments/')) for x in changed)
report={'passed':True,'pre_task_files':len(prior),'unchanged':len(unchanged),'intended_modified':changed,'unexpected_modified':bad,'missing':missing,'all_preexisting_art_and_experiments_unchanged':True}
(H/'preservation-checks.json').write_text(json.dumps(report,indent=2)+'\n')
# Every new source is measurable, including intentional rejected checkpoints.
artifact=[]
for base in [H,R/'assets/source/assisted-bust-v01',R/'assets/export/assisted-bust-v01',R/'assets/previews/assisted-bust-v01']:
 for p in sorted(base.rglob('*')):
  if p.is_file() and p.name not in {'artifact-manifest.json','delivery-checks.json'} and '__pycache__' not in p.parts:
   artifact.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)})
(H/'artifact-manifest.json').write_text(json.dumps({'base_revision':'9e35c5c13987a153e942e6f93f49f247fad13c3a','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artifacts':artifact},indent=2)+'\n')

# Local Markdown links in task-modified docs/new skill reference/record.
link_files=[R/x for x in changed if x.endswith('.md')]+[H/'record.md',R/'tools/pixel-art-director/references/assisted-reconstruction.md']
missinglinks=[]
for p in link_files:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if target.startswith(('http:','https:','mailto:','#')):continue
  target=target.split('#')[0]
  if target and not (p.parent/target).exists():missinglinks.append({'file':str(p.relative_to(R)),'link':target})
# Existing inherited links are kept distinguishable from our additions.
new_missing=[x for x in missinglinks if 'assisted' in x['link'] or x['file'].endswith('assisted-reconstruction.md') or x['file'].endswith('assisted-head-comparison/record.md')]
assert not new_missing,new_missing
# Central deliverables are exact copies, not an unexplained subsequent revision.
for a,b in [(H/'c01-restored-mouth.aseprite',R/'assets/source/assisted-bust-v01/bust.aseprite'),(H/'blink-restored-mouth.aseprite',R/'assets/source/assisted-bust-v01/blink.aseprite'),(H/'c01-restored-mouth.png',R/'assets/export/assisted-bust-v01/bust.png')]:assert sha(a)==sha(b)
registry=json.loads((H/'reference-registry.json').read_text())
for row in registry:assert sha(R/row['path'])==row['sha256']
(H/'delivery-checks.json').write_text(json.dumps({'preservation':report,'new_local_links_valid':True,'all_checked_markdown_missing_links':missinglinks,'central_copies_exact':True,'registry_hashes_match':True,'artifact_count':len(artifact),'construction':'local static and expression native sources exported/reopened','playback':'browser observed with screenshots/events','godot':'not run','installation':'none','user_approval':'pending','publication':'not performed'},indent=2)+'\n')
print(json.dumps({'preserved_prior_files':len(unchanged),'intended_modified':changed,'artifact_count':len(artifact),'link_issues':missinglinks},indent=2))
