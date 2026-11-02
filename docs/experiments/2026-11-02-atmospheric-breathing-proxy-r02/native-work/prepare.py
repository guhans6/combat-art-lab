from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,sys,string,hashlib
P=Path('/private/tmp/atmospheric-breathing-proxy-r02');sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(P/'baseline.aseprite');layers=[l['name']for l in A['layers']];moving=layers[4:];fixed=layers[:4];pal=['#00000000','#15191e','#1c1d20','#303035','#79583d','#ad8056','#b98d60','#24282d','#353a3f','#242d36','#3d4c59','#56636d','#626971','#303338'];legend=dict(zip(string.ascii_letters,pal[1:]));rev={c:k for k,c in legend.items()}
mask=Image.new('L',(96,160));bounds={};ops={}
for n in moving:
 l=layers.index(n);union=Image.new('L',(96,160))
 for f in range(12):union=ImageChops.lighter(union,A['cels'][f,l]['image'].getchannel('A'))
 bounds[n]=union.getbbox();mask=ImageChops.lighter(mask,union)
assert not mask.crop((0,102,96,160)).getbbox();mask.save(P/'editable-upperbody-frozen.png')
for pose,f in [('rest',0),('open',1),('rise',2),('apex',3)]:
 ops[pose]={}
 for n in moving:
  im=A['cels'][f,layers.index(n)]['image'];x0,y0,x1,y1=bounds[n];rows=[]
  for y in range(y0,y1):
   row=''
   for x in range(x0,x1):
    r,g,b,a=im.getpixel((x,y));row+='.'if not a else rev[f'#{r:02x}{g:02x}{b:02x}']
   rows.append(row)
  ops[pose][n]=[{'kind':'grid','x':x0,'y':y0,'rows':rows,'legend':legend}]
mapping=['rest','open','open','open','rise','apex','apex','rise','open','open','open','rest'];dur=[200,180,180,200,220,300,200,220,260,280,300,260];stages={'rest':[0,0],'open':[0,1],'rise':[1,1],'apex':[1,2]}
json.dump({'layers':layers,'moving':moving,'fixed':fixed,'palette':pal,'ops':ops,'pose_source_frames_0based':{'rest':0,'open':1,'rise':2,'apex':3},'mapping':mapping,'durations_ms':dur,'stages':stages,'bounds':bounds,'method':'reuse exact whole valid native part forms from immutable r01; no redesign/redraw/rowstretch/globalbob'},open(P/'correction-ops.json','w'),indent=2)
(P/'observations.md').write_text('''# Traveler breathing amplitude r02\n\nUser rejects r01 motion as too bouncy; accepts appearance only as disposable motion-test sample, not a characterproposal. One bounded amplitudecorrection plus one concrete jointrepair budget; no newstyle/outfit/grid/palette/fighterapplication. Canonical immutablebaseline is selectedlearningrepo assets/source/atmospheric-traveler/breathing-r01/traveler-breathing.aseprite SHAa34a66c188f0f3f63fd0bb06e1ccdf1ed68c82b2f8fe0b617e42489be1313417, copiedbyteexact tobaseline.aseprite. Alloutputs r02only.\n\nExisting pixel-art-director exactskill and animation/structure/comparison-review procedures retained. HeadlesspreflightREADY1.3.18.6-dev/Pebbly0.8.2, allprior documentsclosed beforeopen. Actualnative baseline info/palette read and apexpreview inspected beforemutation. Recent fullscratchsmoke validsamebackend; final visibleduplicateedit/reopen supplies fresh localizedproof. No callablevalidate despite advertisedfeature; independent PNG/nativechecks reported.\n\nFrozen editmask editable-upperbody-frozen.png BEFORE keymutation is union actualnative alpha of sixmovingowners across12baselineframes, including hidden neck/thorax/sleeve overlap. Outsideblack protected; all y102+ protected, four complete fixedowners protected separately. Editableowners far-sleeve-hand,thorax-coat,neck-collar,head-hair-face,near-upper-sleeve,near-forearm-hand only. Gridclearrects may include transparentpixels within theseowners, but actualchangedpixels must passmask.\n\nMotiontarget max1px supported shoulder/headlift and2px chestforward expansion versus3/3. Existingvalid sourcepose0rest,1open(0,1),2rise(1,1),3apex(1,2) zerobased. Reuseexactwholeforms with same sharedphase; no newfeatures/materials or intermediatejoint invention. Collar/neck/head/upperarm/forearm travel together, chest planes already drawn for widths1/2. Exactrestentry/last/first and fixedpelvis/feet. Same12durations2800ms forfair amplitudecomparison. Newmapping rest/open/open/open/rise/apex/apex/rise/open/open/open/rest, fouruniqueactualposes; reducedgridrange createsheldquantizedlevels, honestlyreported.\n\nKeyscheckpoint1rest/2open/6apex only beforetimelinepropagation. Nativekeys file retains12slots, untouchedothers are r01context, notcompletedr02cycle. Requiredstructuralrelationships: skull-neck-collar-thorax; shoulder-cap-upperarm-elbow-forearm-wrist; thorax-waist-fixedpelvis; fixedlegs/soles. No props. No expressions or hairmotion.\n''')
print(json.dumps({'mask_sha256':hashlib.sha256((P/'editable-upperbody-frozen.png').read_bytes()).hexdigest(),'mask_pixels':sum(v>0 for v in mask.getdata()),'moving':moving,'source_frames_0based':[0,1,2,3]}))
