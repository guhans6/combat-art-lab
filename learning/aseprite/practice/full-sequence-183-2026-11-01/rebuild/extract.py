from pathlib import Path
import hashlib,json,shutil,importlib.util,html
ROOT=Path(__file__).resolve().parents[1]
COURSE=ROOT.parents[1]
SOURCE=Path('/Users/guhan/Guhan/Projects/combat-art-lab/docs/experiments/2026-10-31-new-keys-smear')
spec=importlib.util.spec_from_file_location('native_reader',COURSE/'practice/one-pose-183-2026-11-01/rebuild/verify_one_pose.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
files=[]
def copy(src,dest):
 dst=ROOT/dest;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SOURCE/src,dst)
 digest=hashlib.sha256(dst.read_bytes()).hexdigest();assert digest==hashlib.sha256((SOURCE/src).read_bytes()).hexdigest()
 files.append({'source':str(SOURCE/src),'copy':dest,'sha256':digest})
copy(Path('exports/timing.json'),'timing.json')
timing=json.loads((ROOT/'timing.json').read_text());checks={};images={}
for variant in ['clean','smear']:
 copy(Path(f'source/tote-{variant}-material03.aseprite'),f'{variant}-all-poses.aseprite')
 native=m.Ase(ROOT/f'{variant}-all-poses.aseprite')
 assert native.canvas==(256,208) and native.frame_count==19
 assert [f['duration_ms'] for f in native.frames]==timing['durations_ms']
 images[variant]=[]
 for i in range(1,20):
  name=f'{variant}-{i:02}.png';copy(Path('exports')/name,'frames/'+name)
  image=m.image(ROOT/'frames'/name);assert m.same(image,native.composite(i-1))
  images[variant].append(image)
 checks[variant]={'frames':19,'canvas':list(native.canvas),'layers':[x['name'] for x in native.layers],'native_matches_all_PNGs':True,'duration_ms':sum(f['duration_ms'] for f in native.frames)}
 copy(Path(f'review/tote-{variant}-1x.gif'),f'previews/{variant}-1x.gif')
 copy(Path(f'review/tote-{variant}-3x.gif'),f'previews/{variant}-3x.gif')
assert [i+1 for i in range(19) if not m.same(images['clean'][i],images['smear'][i])]==[9]
assert m.same(images['clean'][0],images['clean'][18])
ref=m.image(COURSE/'practice/one-pose-183-2026-11-01/inputs/reference.png')
assert m.same(images['clean'][0].crop((60,8,188,200)),ref)
manifest={'thread':'01a19024-f723-7a23-ad2b-74fbda7ff9e6','source_root':str(SOURCE),'date':'2026-11-01','operation':'Byte-identical extraction; no resampling, recoloring, native editing or new animation.','checks':checks,'only_variant_difference_frame':9,'entry_return_exact':True,'standing_reference_exact_at_offset':[60,8],'files':files}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
base='../practice/full-sequence-183-2026-11-01/'
cards=[]
for i,(phase,ms) in enumerate(zip(timing['phases'],timing['durations_ms']),1):
 content=f'<a href="{base}frames/clean-{i:02}.png"><img class="pixel" src="{base}frames/clean-{i:02}.png" width="256" height="208" loading="lazy" alt="Clean frame {i}: {html.escape(phase)}"></a>'
 if i==9:content+=f'<p>Smear alternative (same frame slot):</p><a href="{base}frames/smear-09.png"><img class="pixel" src="{base}frames/smear-09.png" width="256" height="208" alt="Frame 9 authored tote smear"></a>'
 cards.append(f'<section class="panel"><h2>{i:02} · {html.escape(phase.replace("-"," "))}</h2><p>{ms} ms · <a href="{base}frames/clean-{i:02}.png" download>Clean PNG</a> · <a href="{base}frames/smear-{i:02}.png" download>Smear PNG</a></p>{content}</section>')
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>All poses · Aseprite practice</title><link rel="stylesheet" href="../assets/course.css"></head><body><header><a href="../index.html">Aseprite field notes</a><a href="../lessons/0005-two-ways-to-start-your-character.html">One-pose lesson</a></header><main><span class="eyebrow">Optional reference library</span><h1>The complete tote swing</h1><p class="lead">19 timeline frames, 2.23 seconds. Original pixels and colors from the earlier chat, ready to inspect or trace one at a time.</p>'''
page+=f'''<p><a class="button" href="{base}clean-all-poses.aseprite" download>Open clean sequence</a> <a class="button secondary" href="{base}smear-all-poses.aseprite" download>Open smear sequence</a></p><div class="callout"><p>These are copies of the existing layered animation sources, with all frames and timing intact. Save your own copy before editing. They do not have the beginner starter’s Guide or Corrections layers.</p><p>The canvas is 256 × 208 to leave room for the bag swing. The standing character is still 183 pixels high; bent poses naturally change visible height. Nothing was fitted or resized frame by frame. Frame 19 repeats frame 1 for the return. Only frame 9 differs between clean and smear.</p></div><h2>Watch, then choose one drawing</h2><div class="two"><figure><img class="pixel" src="{base}previews/clean-1x.gif" width="256" height="208" alt="Existing clean tote swing playback"><figcaption>Clean sequence · native 1×. <a href="{base}previews/clean-3x.gif">3× preview</a></figcaption></figure><figure><img class="pixel" src="{base}previews/smear-1x.gif" width="256" height="208" alt="Existing authored-smear tote swing playback"><figcaption>Smear sequence · native 1×. <a href="{base}previews/smear-3x.gif">3× preview</a></figcaption></figure></div><h2>How to use these</h2><p>For automation and correction, open the clean native sequence, select the numbered frame in the Timeline, and add a new layer for your corrections. Layers are rows; frames are columns. Play the sequence to see how your change reads beside its neighbors.</p><p>For hand tracing another pose, open that frame’s PNG in Aseprite, save a new native copy, name its image layer Guide, lock it and lower its opacity. Add a blank drawing layer above it. The PNG is a full-opacity color reference; sample from the original palette or a separate full-opacity tab, rather than the faded guide. Keep this new document at 256 × 208 so the pose is not cropped.</p><p>Start with the clean pose. The brief smear is deliberately distorted for motion, so it is a later study. You can continue today’s tote-contour exercise in the separate one-pose starter; extracting the whole sequence does not require drawing every frame now. Ask the teacher about any frame or transition that looks unclear.</p><h2>Every timeline slot</h2>'''
page+=''.join(cards)
page+=f'<p class="sources">Provenance: <a href="codex://threads/01a19024-f723-7a23-ad2b-74fbda7ff9e6">earlier smear chat</a> · <a href="{base}manifest.json">copy hashes and verification</a> · <a href="{base}timing.json">original timing</a>. Existing provisional animation; no new Godot run or visual approval is claimed.</p></main><footer>Original-resolution reference library · 1 November 2026</footer></body></html>'
(COURSE/'reference/all-poses.html').write_text(page)
print(json.dumps({'copied_files':len(files),'verification':checks,'variant_difference':[9],'standing_reference_exact':True}))
