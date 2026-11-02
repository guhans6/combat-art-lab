from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib
P=Path('/private/tmp/atmospheric-idle-sample-r04');D=P/'delivery';sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
eq=lambda a,b:a.tobytes()==b.tobytes()
def comp(s,f):
 im=Image.new('RGBA',s['canvas'])
 for i in range(len(s['layers'])):im.alpha_composite(s['cels'][f,i]['image'])
 return im
def palettes(s):return[c for f in s['frames']for c in f['non_cel_chunks']if c['type']in('0x2019','0x11','0x4')]
def matte(im):
 m=Image.new('RGBA',im.size,'#73777b');m.alpha_composite(im);return m
A=read(P/'baseline-r03.aseprite');K=read(P/'keys/connected-keys.aseprite');B=read(D/'relaxed-idle-r04.aseprite');E=read(D/'edit-proof.aseprite');stages=[0,1,2,1];timings=json.load(open(D/'timings.json'));dur=[f['duration_ms']for f in timings['frames']];names=[l['name']for l in B['layers']];mask=Image.open(P/'editable-upper-frozen.png').convert('L');rest=comp(A,0)
assert sha(P/'baseline-r03.aseprite')=='afbb2f8b9d947890b1eedc53be03f3950e234ad53d81559a7537b25b44622665'
assert sha('/Users/guhan/Guhan/Projects/combat-art-lab-learning/assets/source/atmospheric-traveler/idle-r03/grounded-idle.aseprite')==sha(P/'baseline-r03.aseprite')
assert A['canvas']==B['canvas']==[96,160]and B['layers']==A['layers']and len(B['frames'])==4
assert [f['duration_ms']for f in B['frames']]==dur and palettes(A)==palettes(B)
sheet=Image.open(D/'idle-sheet.png').convert('RGBA');rsheet=Image.open(D/'reopened-sheet.png').convert('RGBA');assert sheet.size==(384,160)and eq(sheet,rsheet)
changed=[];fixed=[];frames=[];cuffs=[];M=D/'masks';M.mkdir(exist_ok=True)
for f,k in enumerate(stages):
 im=Image.open(D/f'idle-{f}.png').convert('RGBA');frames.append(im);assert eq(im,comp(B,f))and eq(im,sheet.crop((96*f,0,96*(f+1),160)))
 assert set(im.getchannel('A').getdata())=={0,255}
 pts=[(i%96,i//96)for i,(a,b)in enumerate(zip(rest.getdata(),im.getdata()))if a!=b];assert all(mask.getpixel(p)for p in pts);changed.append(len(pts))
 assert eq(im.crop((0,96,96,160)),rest.crop((0,96,96,160)))
 for i,n in enumerate(names):
  assert eq(B['cels'][f,i]['image'],K['cels'][k,i]['image'])
  if i<6:assert eq(B['cels'][f,i]['image'],A['cels'][0,i]['image'])
  B['cels'][f,i]['image'].getchannel('A').save(M/f'f{f}-{n}.png')
 fixed.append({'frame':f,'both_pants_boots_pelvis_skirt_exact_native_rest':True,'all_y96plus_composite_exact_rest':True})
 contact={}
 for side,cut in[('near',136),('far',137)]:
  pant=B['cels'][f,names.index(side+'-leg-pants')]['image'];boot=B['cels'][f,names.index(side+'-boot-cuff-fixed')]['image'];xs=[x for x in range(96)if pant.getpixel((x,cut-1))[3]and boot.getpixel((x,cut))[3]];assert xs;contact[side]=xs
 cuffs.append(contact)
assert eq(frames[0],rest)and eq(frames[1],frames[3])and len({im.tobytes()for im in frames})==3
# Native source protection including hidden part pixels and exact duplicate-only edit.
assert all(B[k]==E[k]for k in['header','layers','frames'])and B['cels'].keys()==E['cels'].keys();edits=[]
for key,b in B['cels'].items():
 e=E['cels'][key];assert all(b[k]==e[k]for k in['geometry','opacity','z']);pts=[(i%96,i//96)for i,(a,c)in enumerate(zip(b['image'].getdata(),e['image'].getdata()))if a!=c]
 if pts:edits.append({'frame':key[0],'owner':names[key[1]],'pixels':pts})
expected=[{'frame':0,'owner':'thorax-coat','pixels':[(53,60),(53,61),(53,62)]}];assert edits==expected,edits
proof=Image.open(D/'edit-proof.png').convert('RGBA');assert eq(proof,Image.open(D/'edit-proof-reopened.png').convert('RGBA'))and eq(proof,comp(E,0));assert sum(a!=b for a,b in zip(rest.getdata(),proof.getdata()))==3 and eq(proof.getchannel('A'),rest.getchannel('A'))
for sc in[1,2,3]:
 out=Image.new('RGB',(4*96*sc,160*sc+24),'#73777b');d=ImageDraw.Draw(out)
 for f,im in enumerate(frames):out.paste(matte(im).resize((96*sc,160*sc),Image.Resampling.NEAREST).convert('RGB'),(f*96*sc,24));d.text((f*96*sc+3,5),f'F{f} key{stages[f]} {dur[f]}ms',fill='white')
 out.save(D/f'contact-{sc}x.png')
out=Image.new('RGB',(360,220),'#73777b');d=ImageDraw.Draw(out)
for j,im in enumerate([rest,proof]):out.paste(matte(im).crop((45,53,62,73)).resize((136,160),Image.Resampling.NEAREST).convert('RGB'),(j*180+16,35));d.text((j*180+16,9),['main unchanged','duplicate3pixel proof'][j],fill='white')
out.save(D/'edit-proof-comparison-8x.png')
report={'passed':True,'native_sha256':sha(D/'relaxed-idle-r04.aseprite'),'baseline_sha256':sha(P/'baseline-r03.aseprite'),'frames':4,'unique_drawings':3,'durations_ms':dur,'total_ms':sum(dur),'canvas':[96,160],'layers':12,'cels':48,'source_palette_chunks_exact':True,'source_rest_frame_exact':True,'all_changes_inside_frozen_uppermask':True,'changed_pixels_vs_rest':changed,'fixed_native_proof':fixed,'cuff_contacts':cuffs,'all_native_cels_exact_to_reviewed_key_drawings':True,'native_PNG_sheet_fresh_reopen_sheet_exact':True,'duplicate_only_edit':{'changed':edits,'all_other_native_pixels_metadata_timing_palette_unchanged':True,'visible_changed_composite_pixels':3,'alpha_exact':True,'fresh_reopen_exact':True},'limits':['still review does not establish natural temporal perception','no production fighter edits','sample traveler identity is disposable, not a design proposal','no callable backend validate tool; independent native/PNG readback used','lead owns Godot/environment and exact-palette playback delivery','all lower joints frozen; not a general purpose rig']}
json.dump(report,open(D/'checks.json','w'),indent=2)
print(json.dumps({'passed':True,'native_sha256':report['native_sha256'],'durations':dur,'fixed_lower_all_frames':True,'freshreopen':True,'proof_changed_pixels':3}))
