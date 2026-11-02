from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import sys,json,hashlib
P=Path('/private/tmp/atmospheric-idle-sample-r04');sys.path.insert(0,'/Users/guhan/Guhan/Projects/combat-art-lab-learning/tools');from check_native_pilot import read
A=read(P/'baseline-r03.aseprite');S=read(P/'keys/connected-keys.aseprite');names=[l['name']for l in S['layers']];fixed=names[:6]
def comp(f,hide=(),only=None):
 im=Image.new('RGBA',(96,160))
 for i,n in enumerate(names):
  if n not in hide and(only is None or n in only):im.alpha_composite(S['cels'][f,i]['image'])
 return im
def sheet(images,labels,path,scale=3,cols=3):
 rows=(len(images)+cols-1)//cols;w=96*scale;h=160*scale;out=Image.new('RGB',(cols*w,rows*(h+22)),(83,83,88));d=ImageDraw.Draw(out)
 for i,(im,lab) in enumerate(zip(images,labels)):
  x=(i%cols)*w;y=(i//cols)*(h+22);d.text((x+3,y+4),lab,fill='white');out.paste(im.resize((w,h),Image.Resampling.NEAREST),(x,y+22),im.resize((w,h),Image.Resampling.NEAREST))
 out.save(path)
checks=[];ims=[]
landmarks=[{'skull_top':[47,10],'near_shoulder':[38,40],'near_elbow_inferred':[37,64],'near_wrist':[43,79],'waist_inferred':[46,84],'near_knee_inferred':[38,120],'near_ankle':[36,136],'far_ankle':[51,137],'soles':[47,146]}, {'skull_top':[47,9],'near_shoulder':[38,39],'near_elbow_inferred':[36,64],'near_wrist':[43,79],'waist_inferred':[46,84],'near_knee_inferred':[38,120],'near_ankle':[36,136],'far_ankle':[51,137],'soles':[47,146]}, {'skull_top':[46,9],'near_shoulder':[37,38],'near_elbow_inferred':[35,63],'near_wrist':[42,78],'waist_inferred':[46,84],'near_knee_inferred':[38,120],'near_ankle':[36,136],'far_ankle':[51,137],'soles':[47,146]}]
for f in range(3):
 im=comp(f);ex=Image.open(P/f'keys/key-{f}.png').convert('RGBA');assert im.tobytes()==ex.tobytes();ims.append(im)
 checks.append({'frame':f,'native_export_equal':True,'fixed_native_owners_equal_rest':{n:S['cels'][f,names.index(n)]['image'].tobytes()==A['cels'][0,names.index(n)]['image'].tobytes()for n in fixed},'lower_y96_onwards_equal_rest':im.crop((0,96,96,160)).tobytes()==comp(0).crop((0,96,96,160)).tobytes()})
 for n in names:
  S['cels'][f,names.index(n)]['image'].save(P/f'keys/f{f}-owner-{n}.png');comp(f,hide=[n]).save(P/f'keys/f{f}-hide-{n}.png')
 guide=im.copy();d=ImageDraw.Draw(guide)
 for n,(x,y)in landmarks[f].items():d.line((x-1,y,x+1,y),fill='#ff5050');d.line((x,y-1,x,y+1),fill='#ff5050')
 guide.save(P/f'keys/f{f}-landmarks.png')
sheet(ims,['REST','transition','shoulder-led apex'],P/'keys/keys-3x.png')
sheet(ims,['REST','transition','apex'],P/'keys/keys-1x.png',1)
sheet([Image.open(P/f'keys/f{f}-landmarks.png')for f in range(3)],['REST red sites; inferred knees','transition','apex'],P/'keys/landmarks-3x.png')
sheet([comp(f,only=names[:6])for f in range(3)],['fixed lower owners REST','fixed lower owners transition','fixed lower owners apex'],P/'keys/lower-owners-3x.png')
sheet([comp(f,hide=names[:6])for f in range(3)],['upper owners REST','upper owners transition','upper owners apex'],P/'keys/upper-owners-3x.png')
for n in names[6:]:sheet([comp(f,hide=[n])for f in range(3)],[f'{n} hidden F{f}'for f in range(3)],P/f'keys/hide-{n}-3x.png')
json.dump({'checks':checks,'landmarks':landmarks,'landmark_caution':'elbows/pelvis/knees are inferred routes; sites are operational points, not proof of skeleton','source_sha256':hashlib.sha256((P/'baseline-r03.aseprite').read_bytes()).hexdigest()},open(P/'keys/checks.json','w'),indent=2)
print(json.dumps(checks))
