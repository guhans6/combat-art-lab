"""Read-only native checks and packaging of actual editor exports."""
from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib,shutil
R=Path(__file__).resolve().parent;OLD=R.parent/'2026-10-30-tote-attack'
sys.path[:0]=[str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'),str(R.parent/'2026-10-30-coherent-idle')]
from native_read import read,composite,holes
from gif_timeline import check
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=read(R/'source/attack-repaired.aseprite');old=read(OLD/'artist/sol-rescue/source/tote-attack-v03.aseprite');proof=read(R/'scratch/hand-highlight-final.aseprite')
frames=[composite(a,f) for f in range(13)];before=[composite(old,f) for f in range(13)];times=[f['duration_ms'] for f in a['frames']]
def canon(im):return bytes(v for c in im.get_flattened_data() for v in (c if c[3] else (0,0,0,0)))
def require(test,message):
 if not test:raise RuntimeError(message)
require(a['canvas']==[320,192] and len(a['frames'])==13,'native canvas/frame count')
reopen=Image.open(R/'review/reopened-sheet.png').convert('RGBA')
for i,im in enumerate(frames):
 require(canon(im)==canon(Image.open(R/'frames'/f'candidate-{i}.png').convert('RGBA')),f'export F{i+1}')
 require(canon(im)==canon(reopen.crop((i*320,0,(i+1)*320,192))),f'reopen F{i+1}')
 require(set(im.getchannel('A').get_flattened_data())<={0,255},f'alpha F{i+1}')
neutral=Image.new('RGBA',(320,192));neutral.alpha_composite(Image.open(OLD/'inputs/neutral.png').convert('RGBA'),(64,0))
require(canon(frames[0])==canon(neutral)==canon(frames[-1]),'exact neutral seam against direct neutral input')
# Frame-local new colors are permitted only within the unchanged native palette.
palette=set()
for chunk in old['chunks']:
 if chunk['type']!=0x2019:continue
 import struct
 raw=bytes.fromhex(chunk['bytes']);size,first,last=struct.unpack_from('<III',raw);offset=20
 for index in range(first,last+1):
  flags=struct.unpack_from('<H',raw,offset)[0];offset+=2;rgba=tuple(raw[offset:offset+4]);offset+=4;palette.add(rgba)
  if flags&1:
   length=struct.unpack_from('<H',raw,offset)[0];offset+=2+length
require(all(c in palette for im in frames for c in im.get_flattened_data() if c[3]),'candidate pixels outside retained native palette')
require([c['bytes'] for c in a['chunks'] if c['type']==0x2019]==[c['bytes'] for c in old['chunks'] if c['type']==0x2019],'palette changed')
require(times==[f['duration_ms'] for f in old['frames']],'timing changed')
changed=[]
for key,cel in a['cels'].items():
 if canon(cel['image'])!=canon(proof['cels'][key]['image']):changed.append(key)
require(len(changed)==1 and changed[0][0]==8 and a['layers'][changed[0][1]]['name']=='05-loaded-grip-drawing','local proof damaged other cels')
diff=[(x,y) for y in range(192) for x in range(320) if frames[8].getpixel((x,y))!=composite(proof,8).getpixel((x,y))]
require(diff==[(159,77)],'local proof changed more than one pixel')
require(canon(composite(proof,8))==canon(Image.open(R/'scratch/proof-final-reopened.png').convert('RGBA')),'proof reopen mismatch')
# Actual editor GIFs, exact decoded timeline, no perceptual playback claim.
gifs={}
for n in [1,3]:
 try:gifs[str(n)]=check(R/'review'/f'attack-{n}x.gif',frames,times,n)
 except AssertionError as e:raise RuntimeError(f'GIF {n}x validation failed: {e}')
# Shared-matte contact sheets and paired comparisons. No independent pose fitting.
ph=json.loads((OLD/'artist/delivery.json').read_text())['phases']
def matte(im):
 out=Image.new('RGBA',im.size,(50,52,55,255));out.alpha_composite(im);return out
for scale in [1,2]:
 out=Image.new('RGBA',(320*4*scale,216*4*scale),(50,52,55,255));d=ImageDraw.Draw(out)
 for i,im in enumerate(frames):
  x=(i%4)*320*scale;y=(i//4)*216*scale
  out.alpha_composite(im.resize((320*scale,192*scale),Image.Resampling.NEAREST),(x,y+24*scale));d.text((x+4,y+4),f'F{i+1} | {times[i]} ms | {ph[i]}',fill='white')
 out.convert('RGB').save(R/'review'/f'contact-{scale}x.png')
for i in range(13):
 out=Image.new('RGBA',(640,216),(50,52,55,255));d=ImageDraw.Draw(out)
 for j,im in enumerate([before[i],frames[i]]):out.alpha_composite(im,(320*j,24));d.text((320*j+4,4),f'F{i+1} '+('original rejected' if j==0 else 'repair candidate'),fill='white')
 out.convert('RGB').resize((1280,432),Image.Resampling.NEAREST).save(R/'review'/f'compare-f{i+1:02}.png')
# Compact entry, contact, recovery, return comparison at native scale.
out=Image.new('RGBA',(640,216*5),(50,52,55,255));d=ImageDraw.Draw(out)
for row,f in enumerate([1,5,8,11,12]):
 for col,seq in enumerate([before,frames]):out.alpha_composite(seq[f],(320*col,row*216+24));d.text((320*col+4,row*216+4),f'F{f+1} '+('original' if col==0 else 'candidate'),fill='white')
out.convert('RGB').save(R/'review/before-after.png')
# Palette-wide scope allows existing colors to newly appear in individual frames.
mask=Image.new('L',(320,192));ImageDraw.Draw(mask).rectangle((45,0,289,185),fill=255);mask.save(R/'review/allowed-actor.png')
spec={'baseline_role':'rejected v03 diagnostic baseline','registration':'same320x192 native canvas/root plane185; explicit per-form reconstruction, no independent bbox fitting','required_frame_ids':[f'F{i}' for i in range(2,13)],'allow_new_colors':True,'zoom':2,'evidence':[{'role':'identity full scene','path':'../../2026-10-30-tote-attack/inputs/character-scene.png'},{'role':'identity close-up','path':'../../2026-10-30-tote-attack/inputs/character-closeup.png'},{'role':'exact neutral','path':'../../2026-10-30-tote-attack/inputs/neutral.png'},{'role':'candidate native','path':'../source/attack-repaired.aseprite'},{'role':'fresh reopen','path':'reopened-sheet.png'},{'role':'authored playback candidate','path':'attack-1x.gif'}],'frames':[{'id':f'F{i+1}','before':f'../../2026-10-30-tote-attack/artist/sol-rescue/frames/v03-frame-{i}.png','after':f'../frames/candidate-{i}.png','mask':'allowed-actor.png','regions':[{'name':'head-neck-shoulders','crop':[75,0,205,65]},{'name':'arms-hands-tote-torso','crop':[45,35,290,160]},{'name':'hips-legs-feet','crop':[65,70,225,186]}]} for i in range(1,12)]}
(R/'review/comparison-spec.json').write_text(json.dumps(spec,indent=2))
names={v['name']:i for i,v in enumerate(a['layers'])}
delivery={'native':'source/attack-repaired.aseprite','native_sha256':sha(R/'source/attack-repaired.aseprite'),'frames':[f'frames/candidate-{i}.png' for i in range(13)],'canvas':[320,192],'durations_ms':times,'phases':ph,'active_frames_1based':[6],'root_pivot':[128,185],'root_offsets':[[0,0]]*13,'bag_bounds_xyxy':[list(a['cels'][i,names['04-tote-and-handles']]['image'].getbbox()) for i in range(13)],'gif_1x':'review/attack-1x.gif','gif_3x':'review/attack-3x.gif','status':'candidate; user artistic approval pending','limits':'Inherited neutral owner bounds include non-bag pixels; contact F6 tote owner is isolated. Still-only agent review; coarse source stance steps remain.'}
(R/'delivery.json').write_text(json.dumps(delivery,indent=2))
report={'native_sha256':delivery['native_sha256'],'canvas':[320,192],'frames':13,'cycle_ms':sum(times),'native_export_and_reopen_visible_rgba_exact':True,'neutral_endpoints_exact':True,'direct_neutral_input_sha256':sha(OLD/'inputs/neutral.png'),'all_pixels_in_retained_palette':True,'palette_chunks_unchanged':True,'binary_alpha':True,'layer_names':[x['name'] for x in a['layers']],'local_edit_proof':{'changed_cel':changed,'changed_pixels':diff,'all_other_cels_exact':True,'fresh_reopen_exact':True},'gif_checks':gifs,'enclosed_transparent_pixels_by_frame':[len(holes(im)) for im in frames],'old_native_unchanged':sha(OLD/'artist/sol-rescue/source/tote-attack-v03.aseprite')=='1f6d68c6927bbcc594be9913156f74a6b0939aa373a9be9971dcd5be8ab52065','validate_tool':'not exposed by connected MCP; independent native/export checks used','visual_approval':'pending'}
(R/'review/verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
