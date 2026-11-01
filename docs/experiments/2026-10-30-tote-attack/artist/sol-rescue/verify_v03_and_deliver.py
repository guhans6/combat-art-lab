"""Read-only native verification plus delivery metadata and evidence records."""
from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parents[1];REPO=ROOT.parents[2]
sys.path[:0]=[str(ROOT.parent/'2026-10-30-evidence-idle-four-model/sol61'),str(ROOT.parent/'2026-10-30-coherent-idle')]
from native_read import read,composite
from gif_timeline import check
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
native=R/'source/tote-attack-v03.aseprite';data=read(native);proof=read(R/'source/tote-fold-v03-revision-proof.aseprite');times=[f['duration_ms'] for f in data['frames']];frames=[composite(data,i) for i in range(13)]
assert data['canvas']==[320,192] and len(data['layers'])==7 and len(frames)==13
sheet=Image.open(R/'review/fresh-reopen-v03-sheet.png').convert('RGBA');assert sheet.size==(4160,192)
for i,frame in enumerate(frames):
 assert Image.open(R/'frames'/f'v03-frame-{i}.png').convert('RGBA').tobytes()==frame.tobytes()
 assert sheet.crop((320*i,0,320*(i+1),192)).tobytes()==frame.tobytes()
 assert set(frame.getchannel('A').getdata())<={0,255}
 assert frame.getbbox()[3]==185, (i+1,frame.getbbox())
neutral=Image.new('RGBA',(320,192));neutral.alpha_composite(Image.open(ROOT/'inputs/neutral.png').convert('RGBA'),(64,0));assert frames[0].tobytes()==frames[-1].tobytes()==neutral.tobytes()
# Demonstrate all native owners except the proof-only tote frame remain exact.
assert data['layers']==proof['layers'];changed=[]
for key,cel in data['cels'].items():
 if cel['image'].tobytes()!=proof['cels'][key]['image'].tobytes():changed.append(key)
assert changed==[(8,4)],changed
before=frames[8];after=composite(proof,8);changes=[(x,y) for y in range(192) for x in range(320) if before.getpixel((x,y))!=after.getpixel((x,y))]
assert changes and all(184<=x<190 and 121<=y<131 for x,y in changes)
assert after.tobytes()==Image.open(R/'review/tote-fold-v03-proof-reopened.png').convert('RGBA').tobytes()
inputs=json.loads((ROOT/'inputs/manifest.json').read_text());assert all(sha(ROOT/'inputs'/name)==info['sha256'] for name,info in inputs.items())
# Declare opaque landmarks closest to the visually identified anatomy/grip centers.
def opaque_near(im,xy,layer=None):
 points=[(x,y) for y in range(im.height) for x in range(im.width) if im.getpixel((x,y))[3]]
 return list(min(points,key=lambda p:(p[0]-xy[0])**2+(p[1]-xy[1])**2))
def owner(f,l):return data['cels'][(f,l)]['image']
head_targets=[(130,20),(132,24),(125,30),(137,30),(123,27),(136,24),(125,26),(130,35),(140,24),(140,24),(149,25),(136,25),(130,20)]
grips=[[134,79],[142,75],[160,94],[112,85],[154,91],[196,73],[180,77],[164,96],[169,86],[159,79],[157,67],[157,68],[134,79]]
head_targets=[(p[0]+(18 if i in [6,7] else 0),p[1]) for i,p in enumerate(head_targets)]
grips=[[p[0]+(18 if i in [6,7] else 0),p[1]] for i,p in enumerate(grips)]
heads=[opaque_near(owner(i,3),p) for i,p in enumerate(head_targets)]
thorax=[opaque_near(owner(i,1),(p[0],75)) for i,p in enumerate(heads)]
feet=[];bags=[]
for i,im in enumerate(frames):
 leg=owner(i,0);a=leg.getchannel('A');pts=[(x,y) for y in range(145,192) for x in range(320) if a.getpixel((x,y))]
 mid=(min(p[0] for p in pts)+max(p[0] for p in pts))/2;ends=[]
 for side in [0,1]:
  ps=[p for p in pts if (p[0]<mid)==(side==0)];my=max(p[1] for p in ps);xs=sorted(x for x,y in ps if y==my);ends.append([xs[len(xs)//2],my])
 feet.append(ends);bag=owner(i,4).getbbox();bags.append(list(bag))
ph=json.loads((R/'operations/phase-data.json').read_text())
delivery=dict(native='sol-rescue/source/tote-attack-v03.aseprite',native_sha256=sha(native),frames=[f'sol-rescue/frames/v03-frame-{i}.png' for i in range(13)],reopen_sheet='sol-rescue/review/fresh-reopen-v03-sheet.png',gif_1x='sol-rescue/review/attack-v03-1x.gif',gif_3x='sol-rescue/review/attack-v03-3x.gif',durations_ms=times,phases=ph['phases'],active_frames_1based=[6],canvas=[320,192],root_pivot=[128,185],root_offsets=[[0,0] for _ in frames],bag_bounds_xyxy=bags,grip_xy=[opaque_near(im,p) for im,p in zip(frames,grips)],head_xy=heads,thorax_xy=thorax,foot_contacts=feet,source_registration_translation_y=[0,-2,-1,1,2,6,6,6,0,0,0,5,0],source_registration_translation_x=[0,0,0,0,0,0,18,18,0,0,0,0,0],registration_note='Translations are baked into all native cels, exports and GIFs; no engine offset is required. Front sole plane y184 with ground anchor185. Raised rear toe is retained in lunge keys.',local_revision_proof='sol-rescue/review/native-v03-verification.json')
(ROOT/'artist/delivery.json').write_text(json.dumps(delivery,indent=2)+'\n')
report=dict(native_sha256=sha(native),native_frames=13,canvas=[320,192],layer_names=[l['name'] for l in data['layers']],native_png_and_fresh_MCP_reopen_exact=True,binary_alpha=True,first_last_exact_neutral_at_x64=True,inputs_unchanged=True,cycle_ms=sum(times),gif_1x=check(R/'review/attack-v03-1x.gif',frames,times,1),gif_3x=check(R/'review/attack-v03-3x.gif',frames,times,3),duplicate_only_revision=dict(native='source/tote-fold-v03-revision-proof.aseprite',sha256=sha(R/'source/tote-fold-v03-revision-proof.aseprite'),changed_native_cels_0based=changed,changed_visible_pixels=len(changes),changed_box_xyxy=[184,121,190,131],all_other_native_cels_exact=True,fresh_MCP_reopen_export_exact=True),limits='Native/export/scope checks only. Parent owns independent whole-cycle review and Godot; continuous temporal perception and user visual approval remain pending.')
(R/'review/native-v03-verification.json').write_text(json.dumps(report,indent=2)+'\n')
# Native-size + integer-zoom localized edit comparison, proof only.
a=Image.new('RGBA',(560,320),(65,59,73,255));d=ImageDraw.Draw(a)
for i,im in enumerate([before,after]):a.alpha_composite(im.crop((170,110,205,145)).resize((280,280),Image.Resampling.NEAREST),(i*280,25));d.text((i*280+5,5),'Main candidate unchanged' if i==0 else 'Duplicate-only fold revision',fill='white')
a.convert('RGB').save(R/'review/tote-fold-v03-local-revision.png')
print(json.dumps(report,indent=2))
