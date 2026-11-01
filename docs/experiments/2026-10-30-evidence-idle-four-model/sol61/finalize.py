"""Faithful packaging and read-only checks of actual MCP artwork exports."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageSequence
import json,hashlib,sys
from native_read import read,composite,rgba_equal,holes,sha
R=Path(__file__).resolve().parent
B=read(R.parent/'inputs/neutral.aseprite');A=read(R/'pass01.aseprite')
BASE=composite(B,0);IMS=[Image.open(R/f'frames/frame-{f}.png').convert('RGBA') for f in range(len(A['frames']))]
DURS=[f['duration_ms'] for f in A['frames']]
MATTE=(96,96,96)
def matte(im):
 o=Image.new('RGBA',im.size,MATTE+(255,));o.alpha_composite(im);return o.convert('RGB')
RGB=[matte(im) for im in IMS]
COLORS=sorted(set(c for im in RGB for c in im.getdata()));assert len(COLORS)<=256
CM={c:i for i,c in enumerate(COLORS)};PAL=[v for c in COLORS for v in c]+[0]*(768-3*len(COLORS))

def gif(scale):
 frames=[]
 for im in RGB:
  if scale!=1:im=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
  p=Image.new('P',im.size);p.putpalette(PAL);p.putdata([CM[c] for c in im.getdata()]);frames.append(p)
 path=R/f'idle-neutral-{scale}x.gif';frames[0].save(path,save_all=True,append_images=frames[1:],duration=DURS,loop=0,optimize=False,disposal=2)
 dec=[];dd=[]
 with Image.open(path) as g:
  for f in ImageSequence.Iterator(g):dec.append(f.convert('RGB'));dd.append(f.info['duration'])
 expected=[]
 for im,d in zip(RGB,DURS):expected.extend([im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST).tobytes()]*(d//10))
 actual=[]
 for im,d in zip(dec,dd):actual.extend([im.tobytes()]*(d//10))
 return {'path':path.name,'sha256':sha(path),'decoded_frames':len(dec),'decoded_durations_ms':dd,'duration_ms':sum(dd),'exact_visible_timeline_10ms':actual==expected,'exact_palette_colors':len(COLORS),'no_quantization':True}

G=[gif(1),gif(3)]
# Pose contacts are composited actual MCP frame exports; labels stay outside art.
for scale,name in [(1,'pose-contact-1x.png'),(3,'pose-contact-3x.png')]:
 cw=128*scale+8;ch=192*scale+25;sheet=Image.new('RGB',(cw*4,ch*2),MATTE);d=ImageDraw.Draw(sheet)
 for f,im in enumerate(RGB):
  x=f%4*cw;y=f//4*ch;sheet.paste(im.resize((128*scale,192*scale),Image.Resampling.NEAREST),(x,y+22));d.text((x+3,y+4),f'F{f+1} {DURS[f]}ms',fill='white')
 sheet.save(R/'evidence'/name)
crop=(31,30,96,88);scale=6;cw=390;ch=370;sheet=Image.new('RGB',(cw*4,ch*2),MATTE);d=ImageDraw.Draw(sheet)
for f,im in enumerate(RGB):
 x=f%4*cw;y=f//4*ch;sheet.paste(im.crop(crop).resize((390,348),Image.Resampling.NEAREST),(x,y+20));d.text((x+4,y+4),f'F{f+1} {DURS[f]}ms',fill='white')
sheet.save(R/'evidence/torso-contact-6x.png')
# Reference crop is diagnostic resampling only; native exports are never resampled
# in the actual PNG output folders.
scene=Image.open(R.parent/'inputs/character-scene.png').convert('RGB')
refcrop=(450,225,775,1020);ref=scene.crop(refcrop).resize((79,192),Image.Resampling.NEAREST)
for scale in [1,3]:
 cw=140*scale;ch=215*scale;sheet=Image.new('RGB',(cw*4,ch),MATTE);d=ImageDraw.Draw(sheet)
 panels=[ref,matte(BASE),RGB[2],RGB[3]];labels=['reference crop*','neutral native','transition F3','inhale F4']
 for i,(im,label) in enumerate(zip(panels,labels)):
  sheet.paste(im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST),(i*cw,20*scale));d.text((i*cw+2,3),label,fill='white')
 sheet.save(R/f'evidence/reference-neutral-keys-{scale}x.png')
# Material correspondence diagnostic: track specific existing shade roles and
# preserve their spatial appearance through pose sheets; counts are not art grades.
material=[]
for f,im in enumerate(IMS):
 pix=list(im.crop((33,33,94,70)).getdata());material.append({'frame':f+1,'pale_shirt_pixels_roi':pix.count((253,228,204,255)),'muted_fold_pixels_roi':pix.count((214,183,187,255)),'olive_base_pixels_roi':pix.count((106,97,60,255)),'olive_shadow_pixels_roi':pix.count((75,71,50,255))})
# Read-only native/export checks.
frames=[];bh=holes(BASE);basecolors=set(BASE.getdata())
for f,im in enumerate(IMS):
 re=Image.open(R/f'reopen-frames/frame-{f}.png').convert('RGBA');native=composite(A,f)
 head=A['cels'][(f,11)]['image'];neck=A['cels'][(f,10)]['image'];dy=1 if f in [3,4] else 0
 for moving in [head,neck]:
  pass
 registered_head=Image.new('RGBA',(128,192));registered_head.paste(head,(0,dy))
 registered_neck=Image.new('RGBA',(128,192));registered_neck.paste(neck,(0,dy))
 newholes=holes(im)-bh
 # Moved hair cutouts are expected only when the entire head rises. Every hole
 # below the head remains at original coordinates, including the inherited jeans
 # pixel (63,116); no new body holes are accepted.
 frames.append({'frame':f+1,'native_export_equal':rgba_equal(native,im),'fresh_reopen_export_equal':rgba_equal(im,re),'source_static_layers_exact':all(rgba_equal(A['cels'][(f,l)]['image'],B['cels'][(0,l)]['image']) for l in [0,1,2,6,8,9]),'registered_head_exact':rgba_equal(registered_head,B['cels'][(0,11)]['image']),'registered_neck_exact':rgba_equal(registered_neck,B['cels'][(0,10)]['image']),'new_body_holes':[list(p) for p in sorted(newholes) if p[1]>=34],'partial_alpha_pixels':sum(0<c[3]<255 for c in im.getdata()),'new_visible_colors':len(set(im.getdata())-basecolors),'visible_changed_from_rest':sum(x!=y for x,y in zip(im.getdata(),BASE.getdata())),'export_sha256':sha(R/f'frames/frame-{f}.png')})
RA=read(R/'revision-after.aseprite');RB=read(R/'revision-before.aseprite');changed=[]
for f in range(8):
 for l in range(12):
  changed.extend([[f+1,l,i%128,i//128] for i,(a,b) in enumerate(zip(RA['cels'][(f,l)]['image'].getdata(),RB['cels'][(f,l)]['image'].getdata())) if a!=b])
inputs=json.loads((R/'input-hashes.json').read_text());inputcheck={p:sha(R.parent/p)==h for p,h in inputs.items()}
chunks=lambda doc:[x for x in doc['chunks'] if x['type'] in [4,17,0x2019]]
rep={'model':'gpt-6.1-sol','reasoning':'high','editor':'Aseprite 1.3.18.6-dev','server':'@pebbly/aseprite-ai-artist 0.8.2','mode':'headless dedicated MCP','python':sys.version.split()[0],'pillow':Image.__version__,'native_sha256':sha(R/'pass01.aseprite'),'native_canvas':A['canvas'],'layer_metadata_equal':A['layers']==B['layers'],'native_palette_chunks_equal':chunks(A)==chunks(B),'cel_geometry_opacity_z_equal':all(all(A['cels'][(f,l)][k]==B['cels'][(0,l)][k] for k in ['geometry','opacity','z']) for f in range(8) for l in range(12)),'original_rest_native_exact':all(rgba_equal(A['cels'][(f,l)]['image'],B['cels'][(0,l)]['image']) for f in [0,7] for l in range(12)),'frame_durations_ms':DURS,'total_duration_ms':sum(DURS),'frames':frames,'gifs':G,'material_roi_diagnostics':material,'input_hashes_unchanged':inputcheck,'baseline_holes_preserved_note':'Hair cutouts move with the rigid head. The input already has an enclosed transparent jeans pixel at63,116; it is preserved, not newly introduced.','revision':{'native_changes':changed,'one_pixel_only':changed==[[1,3,45,50]],'fresh_reopen_export_equal':rgba_equal(Image.open(R/'revision-after.png').convert('RGBA'),Image.open(R/'revision-reopen.png').convert('RGBA')),'protected_native_metadata_equal':RA['layers']==RB['layers'] and RA['frames']==RB['frames'],'negative_wrong_mask_rejects':not all(c==[1,3,44,50] for c in changed)},'scratch':json.loads((R/'scratch-verification.json').read_text()),'aseprite_validate_tool_available':False,'actual_speed_playback_observed':False,'godot_performed':False,'user_art_approval':False}
rep['passed']=all([rep['layer_metadata_equal'],rep['native_palette_chunks_equal'],rep['cel_geometry_opacity_z_equal'],rep['original_rest_native_exact'],all(inputcheck.values()),all(x['native_export_equal'] and x['fresh_reopen_export_equal'] and x['source_static_layers_exact'] and x['registered_head_exact'] and x['registered_neck_exact'] and not x['new_body_holes'] and not x['partial_alpha_pixels'] and not x['new_visible_colors'] for x in frames),all(g['exact_visible_timeline_10ms'] for g in G),rep['revision']['one_pixel_only'],rep['revision']['fresh_reopen_export_equal'],rep['revision']['protected_native_metadata_equal']])
(R/'verification.json').write_text(json.dumps(rep,indent=2)+'\n')
(R/'timings.json').write_text(json.dumps({'native_frame_numbers':list(range(1,9)),'durations_ms':DURS,'total_ms':sum(DURS),'loop':True,'rest_drawing_frames':[1,8],'tag':None},indent=2)+'\n')
manifest={'native':'pass01.aseprite','frames':[f'frames/frame-{f}.png' for f in range(8)],'durations_ms':DURS,'gif_1x':'idle-neutral-1x.gif','gif_3x':'idle-neutral-3x.gif','verification':'verification.json','record':'record.md','model':'gpt-6.1-sol','reasoning':'high','tools':{'editor':'Aseprite 1.3.18.6-dev','server':'@pebbly/aseprite-ai-artist 0.8.2','mode':'headless dedicated MCP','python':sys.version.split()[0],'pillow':Image.__version__},'native_sha256':sha(R/'pass01.aseprite'),'art_status':'retained playback candidate; user selection pending','actual_speed_playback_observed':False}
(R/'delivery.json').write_text(json.dumps(manifest,indent=2)+'\n')
(R/'artifact-hashes.json').write_text(json.dumps({str(p.relative_to(R)):sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='artifact-hashes.json'},indent=2)+'\n')
print(json.dumps({'passed':rep['passed'],'native_sha256':rep['native_sha256'],'gifs':G,'frame_changes':[f['visible_changed_from_rest'] for f in frames],'material':material},indent=2))
