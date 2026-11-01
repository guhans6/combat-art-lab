"""Independent mechanical evidence, no art scoring or relaxed native checks."""
from pathlib import Path
from PIL import Image,ImageChops
import runpy,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
native=runpy.run_path(str(ROOT/'tools/check_native_pilot.py'))
checks={};rgba=lambda p:Image.open(p).convert('RGBA')
# Scratch orientation and exact pixel change. Reject an intentionally wrong mask.
a=rgba(HERE/'smoke-base.png');b=rgba(HERE/'smoke-edited.png')
assert a.getpixel((2,3))==(180,60,40,255) and a.getpixel((3,4))==(180,60,40,255)
assert a.getpixel((12,10))==(230,210,170,255) and a.getpixel((2,4))[3]==0
mask=[False]*256;mask[0]=True
smoke=native['compare'](HERE/'smoke-base.aseprite',HERE/'smoke-edited.aseprite',['editable'],mask)
assert smoke['passed'],smoke
assert b.tobytes()==rgba(HERE/'smoke-reopened.png').tobytes()
assert not native['compare'](HERE/'smoke-base.aseprite',HERE/'smoke-edited.aseprite',['editable'],[False]*256)['passed']
checks['scratch']={'one_pixel_native_edit':smoke,'reopen_match':True,'wrong_mask_rejected':True,'changed_coordinate':[0,0],'pattern':'red right-elbow at (2,3),(3,3),(3,4), cream isolated at (12,10)'}
paths=['gated/a00-traced-planes','gated/a01-hair-clusters','gated/a02-expression','b00-separated-seed','b01-hair-cleanup','b02-expression']
checks['candidates']={}
for name in paths:
 src=HERE/(name+'.aseprite');info=native['read'](src);png=rgba(HERE/(name+'.png'))
 assert png.size==(120,112) and info['canvas']==[120,112] and len(info['layers'])==9 and len(info['frames'])==1
 assert png.tobytes()==rgba(HERE/(name+'-reopened.png')).tobytes()
 assert set(png.getchannel('A').get_flattened_data())=={0,255}
 checks['candidates'][name]={'reopen_rgba_exact':True,'layers':[x['name'] for x in info['layers']],'canvas':png.size,'visible_colors':len({p[:3] for p in png.get_flattened_data() if p[3]}),'alpha':'binary','native_sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
checks['isolated_edits']={}
for name in ['gated/a02-expression','b02-expression']:
 info=native['read'](HERE/(name+'.aseprite'));idx=next(i for i,x in enumerate(info['layers']) if x['name']=='07-hair-tie')
 mask=[p[3]>0 for p in info['cels'][(0,idx)]['image'].get_flattened_data()]
 res=native['compare'](HERE/(name+'.aseprite'),HERE/(name+'-tie-edit.aseprite'),['07-hair-tie'],mask)
 assert res['passed'],res
 assert rgba(HERE/(name+'-tie-edit.png')).tobytes()==rgba(HERE/(name+'-tie-edit-reopened.png')).tobytes()
 checks['isolated_edits'][name]=res
# B00 is exact semantic reassembly of the masked converted seed (visible pixels).
seed=rgba(HERE/'prepared/converted-seed.png');native_seed=rgba(HERE/'b00-separated-seed.png')
assert seed.getchannel('A').tobytes()==native_seed.getchannel('A').tobytes()
assert all(x==y for x,y in zip(seed.get_flattened_data(),native_seed.get_flattened_data()) if x[3] or y[3])
checks['seed_visible_reassembly_exact']=True
for before,after in [('b00-separated-seed','b01-hair-cleanup'),('b01-hair-cleanup','b02-expression')]:
 a=rgba(HERE/(before+'.png'));b=rgba(HERE/(after+'.png'))
 checks[before+' -> '+after]={'composite_changed_pixels':sum(x!=y for x,y in zip(a.get_flattened_data(),b.get_flattened_data()))}
# Temporal check is explicit frame/cel inspection. Existing strict checker unchanged.
base=native['read'](HERE/'b02-expression.aseprite');motion=native['read'](HERE/'blink-probe.aseprite')
assert motion['canvas']==[120,112] and len(motion['frames'])==5 and motion['layers']==base['layers']
assert [f['duration_ms'] for f in motion['frames']]==[1600,50,90,60,600]
# Eye masks: allow only actual source eye interiors, not brow/hair or costume.
eye=Image.new('L',(120,112));from PIL import ImageDraw
d=ImageDraw.Draw(eye);d.rectangle((59,51,73,64),fill=255);d.rectangle((81,48,90,61),fill=255)
eye.save(HERE/'blink-eye-edit-mask.png');allowed=list(eye.get_flattened_data())
frame_checks=[]
for f in range(5):
 rows=[]
 for i,l in enumerate(base['layers']):
  a=base['cels'][(0,i)];b=motion['cels'][(f,i)]
  ap=list(a['image'].get_flattened_data());bp=list(b['image'].get_flattened_data())
  changes=[k for k,(x,y) in enumerate(zip(ap,bp)) if x!=y]
  if l['name']!='08-eyes-brows':
   assert not changes,(f,l['name'])
   assert a['geometry']==b['geometry'] and a['opacity']==b['opacity'] and a['z']==b['z']
  else:assert all(allowed[k] for k in changes),(f,'out of eye mask')
  rows.append({'layer':l['name'],'changed_pixels':len(changes)})
 frame=rgba(HERE/f'blink-frame-{f+1}.png');assert frame.tobytes()==rgba(HERE/f'blink-frame-{f+1}-reopened.png').tobytes()
 assert frame.getchannel('A').tobytes()==rgba(HERE/'b02-expression.png').getchannel('A').tobytes()
 frame_checks.append(rows)
assert rgba(HERE/'blink-frame-1.png').tobytes()==rgba(HERE/'blink-frame-5.png').tobytes()==rgba(HERE/'b02-expression.png').tobytes()
checks['motion']={'native_reopen_exports_exact':True,'timings_ms':[1600,50,90,60,600],'frame_changes':frame_checks,'protected_layers_equal':8,'outside_eye_changes':0,'root_offsets':[[0,0]]*5,'alpha_silhouette_equal':True,'played_preview':'pending visual playback','godot':'not run'}
(HERE/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('PASS: six static sources, two strict native isolated edits, exact reopened outputs, semantic seed reassembly, five motion frames/protected layers/mask/timing; playback still separate.')
# Final optional hybrid follow-up: preserve B02 eyes, restore B01 mouth only.
a=native['read'](HERE/'b02-expression.aseprite');final=native['read'](HERE/'c01-restored-mouth.aseprite')
mask=list(Image.open(HERE/'prepared/09-mouth-mask.png').convert('L').get_flattened_data())
rollback=native['compare'](HERE/'b02-expression.aseprite',HERE/'c01-restored-mouth.aseprite',['09-mouth'],mask)
assert rollback['passed'],rollback
assert rgba(HERE/'c01-restored-mouth.png').tobytes()==rgba(HERE/'c01-restored-mouth-reopened.png').tobytes()
idx=next(i for i,l in enumerate(final['layers']) if l['name']=='07-hair-tie')
tie_mask=[p[3]>0 for p in final['cels'][(0,idx)]['image'].get_flattened_data()]
tie=native['compare'](HERE/'c01-restored-mouth.aseprite',HERE/'c01-restored-mouth-tie-edit.aseprite',['07-hair-tie'],tie_mask)
assert tie['passed'],tie
assert rgba(HERE/'c01-restored-mouth-tie-edit.png').tobytes()==rgba(HERE/'c01-restored-mouth-tie-edit-reopened.png').tobytes()
old=native['read'](HERE/'blink-probe.aseprite');updated=native['read'](HERE/'blink-restored-mouth.aseprite')
assert old['frames']==updated['frames'] and old['layers']==updated['layers'] and old['header']==updated['header']
for f in range(5):
 for i,l in enumerate(updated['layers']):
  cel=updated['cels'][(f,i)]
  expected=final['cels'][(0,i)] if l['name']=='09-mouth' else old['cels'][(f,i)]
  assert cel['image'].tobytes()==expected['image'].tobytes()
  assert cel['geometry']==expected['geometry'] and cel['opacity']==expected['opacity'] and cel['z']==expected['z']
 assert rgba(HERE/f'blink-final-frame-{f+1}.png').tobytes()==rgba(HERE/f'blink-final-frame-{f+1}-reopened.png').tobytes()
assert rgba(HERE/'blink-final-frame-1.png').tobytes()==rgba(HERE/'c01-restored-mouth.png').tobytes()==rgba(HERE/'blink-final-frame-5.png').tobytes()
checks['selected_final']={'name':'c01-restored-mouth','method':'converted + cleaned; restore earlier source-derived mouth','visible_colors':len({p[:3] for p in rgba(HERE/'c01-restored-mouth.png').get_flattened_data() if p[3]}),'native_reopen_exact':True,'mouth_rollback_strict_native':rollback,'isolated_tie_strict_native':tie,'final_blink_reopen_exact':True,'final_blink_changes_only_eyes_relative_to_final_static':True,'pre_rollback_sources_preserved':True}
(HERE/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('PASS: final C rollback and tie edit satisfy unchanged strict checker; final blink inherits only restored mouth and reopens exactly.')
