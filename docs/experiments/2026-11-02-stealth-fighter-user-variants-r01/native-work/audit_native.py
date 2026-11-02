from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,hashlib,importlib.util
O=Path('/private/tmp/fighter-user-variants-r01/native-work');REPO=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning');DIRECTOR=Path('/Users/guhan/Guhan/Projects/combat-art-lab/tools/pixel-art-director')
def mod(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
# Existing strict reader calls the modern iterator only in compare; compatibility alias
# changes its Python iteration API, never its independent binary/native checks.
if not hasattr(Image.Image,'get_flattened_data'):Image.Image.get_flattened_data=Image.Image.getdata
native=mod('native',REPO/'tools/check_native_pilot.py');checks=mod('checks',DIRECTOR/'scripts/pixel_checks.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report={'boundary':'native static assembly/coverage/reopen/edit only; runtime and user selection separate','toolchain':{'native':'dedicated Aseprite AI Artist MCP only','mode':'headless','aseprite':'1.3.18.6-dev','extension':'0.8.2','python':'/opt/homebrew/bin/python3.11','pillow':'12.0.0','native_reader':str(REPO/'tools/check_native_pilot.py'),'validate':'not exposed; not called'},'variants':{}}
for i in ['01','03','04','05']:
 D=O/f'variant-{i}';a=Image.open(D/'static.png').convert('RGBA');r=Image.open(D/'reopened.png').convert('RGBA');seed=Image.open(D/'raw-seed.png').convert('RGBA');proof=Image.open(D/'edit-proof.png').convert('RGBA');proofr=Image.open(D/'edit-proof-reopened.png').convert('RGBA');n=native.read(D/'static.aseprite');allowed=Image.open(D/'edit-proof-mask.png').convert('L');ops=json.loads((D/'edit-proof-ops.json').read_text());data=json.loads((D/'native-draw-ops.json').read_text());mask=Image.open(D/'source-spatial-mask-native.png').convert('L');pix=list(a.getdata());colors=set(p for p in pix if p[3]);assert a.size==(128,264) and a.getbbox()[1]==13 and a.getbbox()[3]==253 and len(colors)<=64 and set(p[3] for p in pix)=={0,255}
 comp=Image.new('RGBA',a.size);owner_errors=[];layercounts={}
 for ix,l in enumerate(n['layers']):
  actual=n['cels'][(0,ix)]['image'];planned=Image.open(D/(l['name']+'.png')).convert('RGBA');assert actual.tobytes()==planned.tobytes(),l['name'];comp.alpha_composite(actual);layercounts[l['name']]=sum(p[3]>0 for p in actual.getdata());assert l['flags']&1 and l['opacity']==255 and l['blend']==0
 assert comp.tobytes()==a.tobytes()==seed.tobytes()==r.tobytes();assert sum(layercounts.values())==sum(p[3]>0 for p in pix);assert len(n['frames'])==1 and n['frames'][0]['duration_ms']==100 and len(n['layers'])==6
 coverage=checks.check_alpha_coverage(a,solid_mask=mask)
 # Named U04 loose-hair loop may be a real enclosed opening; list exact points only after review.
 changes=checks.check_files(D/'static.png',D/'edit-proof.png',D/'edit-proof-mask.png');protection=native.compare(D/'static.aseprite',D/'edit-proof.aseprite',['near-arm-guard-hand'],[bool(v) for v in allowed.getdata()]);assert changes['passed'] and protection['passed'] and changes['changed_pixels']==24 and proof.tobytes()==proofr.tobytes() and sha(D/'static.aseprite')==ops['source_native_sha256'];assert coverage['passed'],(i,coverage)
 pal={tuple(bytes.fromhex(c[1:])) for c in data['palette']};assert {p[:3] for p in colors}<=pal
 rec=json.loads((D/'recipe.json').read_text());assert sha(O.parent/f'inputs/user-{i}.png')==rec['source_sha256']
 local=checks.review_sheet(a,proof,(31,100,57,136),8);local.save(D/'edit-proof-comparison-8x.png')
 # Six semantic owners, same registration, useful inspectable part separation.
 sheet=Image.new('RGBA',(384*3,792*2+60),(215,212,205,255));d=ImageDraw.Draw(sheet)
 for k,l in enumerate(n['layers']):
  x=(k%3)*384;y=(k//3)*822;d.text((x+5,y+5),l['name'],fill='black');part=n['cels'][(0,k)]['image'];sheet.alpha_composite(part.resize((384,792),Image.Resampling.NEAREST),(x,y+25))
 sheet.convert('RGB').save(D/'native-owner-contact-3x.png')
 for name,obj in [('coverage.json',coverage),('edit-proof-protection.json',protection),('edit-proof-png-check.json',changes)]: (D/name).write_text(json.dumps(obj,indent=2))
 report['variants'][i]={'passed':True,'native_sha256':sha(D/'static.aseprite'),'png_sha256':sha(D/'static.png'),'canvas':a.size,'opaque_bounds_half_open':a.getbbox(),'visible_body_height':240,'visible_colors':len(colors),'palette_entries_including_transparent':65,'binary_alpha':True,'native_export_seed_reopen_exact':True,'disjoint_owners_reassemble_exactly':True,'owner_pixel_counts':layercounts,'frame_count':1,'duration_ms':100,'coverage':coverage,'useful_local_edit':{'purpose':ops['purpose'],'changed_pixels':24,'only_layer':'near-arm-guard-hand','protected_native_pass':protection['passed'],'fresh_reopen_exact':True,'master_unchanged':True},'user_visual_approval':'pending','runtime':'root-owned separate evidence'}
a=Image.open(O/'variant-03/static.png').convert('RGBA');b=Image.open(O/'variant-05/static.png').convert('RGBA');changed=[(x,y) for y in range(264) for x in range(128) if a.getpixel((x,y))!=b.getpixel((x,y))];report['u03_u05']={'changed_pixels':len(changed),'bounds_half_open':[min(x for x,y in changed),min(y for x,y in changed),max(x for x,y in changed)+1,max(y for x,y in changed)+1],'all_changes_within_source_supported_shoulder':all(34<=x<=67 and 47<=y<=65 for x,y in changed),'masks_identical':Image.open(O/'variant-03/source-spatial-mask-native.png').tobytes()==Image.open(O/'variant-05/source-spatial-mask-native.png').tobytes()};assert report['u03_u05']['all_changes_within_source_supported_shoulder']
na=native.read(O/'variant-03/static.aseprite');nb=native.read(O/'variant-05/static.aseprite');report['u03_u05']['per_native_owner_changed_pixels']={na['layers'][k[1]]['name']:sum(p!=q for p,q in zip(c['image'].getdata(),nb['cels'][k]['image'].getdata())) for k,c in na['cels'].items()}
# Protection negative-control must be rejected by the same scoped PNG checker.
S=O/'smoke';before=Image.open(S/'after.png');bad=Image.open(S/'out-of-mask.png');allow=[False]*256;allow[9*16+11]=True;negative=checks.check_images(before,bad,allow);assert not negative['passed'] and 'protected_pixels_changed' in negative['failures'];report['smoke_negative_control']={'rejected':True,'check':negative};smoke=json.loads((S/'checks.json').read_text());smoke['out_of_mask_negative_control']='dedicated MCP changed protected(0,0) on duplicate; independent checker rejects';(S/'checks.json').write_text(json.dumps(smoke,indent=2))
# Baseline compare only, verify canonical hash; never opened or edited in backend.
baseline=REPO/'assets/source/stealth-fighter/idle-r02/idle.aseprite';report['existing_current_baseline']={'sha256':sha(baseline),'expected_sha256':'f4cb8fff0a460cde6845fb15bc0c5e3271259d9d38d5f3efa051e4970b2e6127','unchanged':sha(baseline)=='f4cb8fff0a460cde6845fb15bc0c5e3271259d9d38d5f3efa051e4970b2e6127'};assert report['existing_current_baseline']['unchanged'];(O/'checks.json').write_text(json.dumps(report,indent=2));print(json.dumps({i:r['native_sha256'] for i,r in report['variants'].items()},indent=2));print('ALL4PASS',report['u03_u05'])
