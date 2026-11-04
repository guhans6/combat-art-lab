from pathlib import Path
import hashlib,json,math,subprocess,sys,tempfile
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
sys.path.insert(0,str(ROOT/'tools'))
from check_native_pilot import read
source=ROOT/'learning/aseprite/practice/lantern-144-2026-11-03/reference-original.png'
script=ROOT/'learning/aseprite/automation/convert_image.py';recipe=ROOT/'learning/aseprite/automation/lantern-144.json'
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
im=Image.open(P/'converted.png').convert('RGBA');src=Image.open(source).convert('RGBA')
assert H(source)=='6ecaa70adb6b0eb5625f1a8a2cb0b392f15ddb41620f918ec36e53a0f4fcc2fe'
assert H(script)=='b7fe64ac47772335e15b90ac3f906feacdbc3d1dae72df9fa74948731ab05f49'
assert im.size==(88,152) and im.getbbox()==(6,4,79,148)
assert set(im.getchannel('A').get_flattened_data())=={0,255}
# Independently check every output sample against the original's nearest center.
for y in range(152):
 for x in range(88):
  expected=(0,0,0,0)
  if 6<=x<79 and 4<=y<148:
   sx=107+math.floor((x-6+.5)*745/73);sy=57+math.floor((y-4+.5)*1461/144)
   r,g,b,a=src.getpixel((sx,sy));expected=(r,g,b,255) if a>=160 else (0,0,0,0)
  assert im.getpixel((x,y))==expected,(x,y)
for f in ['native-export.png','native-reopened.png']:
 assert Image.open(P/f).convert('RGBA').tobytes()==im.tobytes()
n=read(P/'converted.aseprite');assert n['canvas']==[88,152] and len(n['frames'])==1
assert [l['name'] for l in n['layers']]==['Converted original','Corrections']
assert n['cels'][(0,0)]['image'].tobytes()==im.tobytes() and (0,1) not in n['cels']
with tempfile.TemporaryDirectory(prefix='lantern-convert-replay-') as tmp:
 out=Path(tmp)/'replay'
 subprocess.run([sys.executable,str(script),'--recipe',str(recipe),'--out',str(out)],check=True,capture_output=True)
 assert (out/'converted.png').read_bytes()==(P/'converted.png').read_bytes()
 assert (out/'preview-3x.png').read_bytes()==(P/'preview-3x.png').read_bytes()
r={'passed':True,'canvas':[88,152],'visible_bounds':[6,4,79,148],'visible_height':144,'nearest_source_pixel_mapping_exact':True,'visible_colors':len({p[:3] for p in im.get_flattened_data() if p[3]}),'binary_alpha_threshold':160,'native_reopen_exact':True,'repeat_png_bytes_identical':True,'converter_unchanged':H(script),'source_unchanged':H(source),'converted_png_sha256':H(P/'converted.png'),'native_sha256':H(P/'converted.aseprite'),'pixel_generation':'Existing deterministic converter only; no generative model, redraw, palette quantization, dithering or cleanup'}
(P/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
