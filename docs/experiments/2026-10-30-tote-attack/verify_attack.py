"""Independent verification of the actual native/export attack delivery.
No automated score or claim of anatomical/temporal artistic approval.
"""
from pathlib import Path
import hashlib,json,struct,sys
from PIL import Image
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
sys.path[:0]=[str(REPO),str(ROOT.parent/'2026-10-30-evidence-idle-four-model/sol61'),str(ROOT.parent/'2026-10-30-coherent-idle'),str(REPO/'tools/pixel-art-director/scripts')]
from native_read import read,composite
from gif_timeline import check as check_gif
from pixel_checks import check_alpha_coverage

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def connected_pair(image, start, end):
 """Declared opaque anchors must share an8-connected silhouette component."""
 width,height=image.size
 start=tuple(int(v) for v in start);end=tuple(int(v) for v in end)
 alpha=image.getchannel('A')
 for x,y in [start,end]:
  if not (0<=x<width and 0<=y<height and alpha.getpixel((x,y))):return False
 seen={start};queue=[start]
 for x,y in queue:
  if (x,y)==end:return True
  for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
   point=(x+dx,y+dy)
   if point not in seen and 0<=point[0]<width and 0<=point[1]<height and alpha.getpixel(point):
    seen.add(point);queue.append(point)
 return False

def palette_colors(native):
 colors={}
 for chunk in native['frames'][0]['chunks']:
  if chunk['type']!=0x2019:continue
  raw=bytes.fromhex(chunk['bytes']);size,first,last=struct.unpack_from('<III',raw);offset=20
  for index in range(first,last+1):
   flags=struct.unpack_from('<H',raw,offset)[0];offset+=2
   colors[index]=tuple(raw[offset:offset+4]);offset+=4
   if flags&1:
    length=struct.unpack_from('<H',raw,offset)[0];offset+=2+length
 return set(c[:3] for c in colors.values())

def inspect_delivery():
 folder=ROOT/'artist';delivery=json.loads((folder/'delivery.json').read_text());native_path=folder/delivery['native'];data=read(native_path)
 times=delivery['durations_ms'];count=len(times)
 assert data['canvas']==delivery['canvas']==[320,192]
 width,height=data['canvas']
 assert len(data['frames'])==len(delivery['frames'])==len(delivery['phases'])==len(delivery['root_offsets'])==len(delivery['bag_bounds_xyxy'])==count
 assert all(isinstance(t,int) and t>0 and t%10==0 for t in times),'Positive10ms timing needed for faithful GIF delivery'
 assert [f['duration_ms'] for f in data['frames']]==times
 assert len(data['layers'])>=4,'Need meaningful native parts beyond flattened frame imports'
 assert len({l['name'] for l in data['layers']})==len(data['layers'])
 for layer in data['layers']:assert layer['blend']==0 and layer['opacity']==255 and layer['level']==0 and layer['type']==0
 assert delivery['active_frames_1based'] and all(isinstance(f,int) and 1<=f<=count for f in delivery['active_frames_1based'])
 assert len(set(delivery['active_frames_1based']))==len(delivery['active_frames_1based'])
 colors=palette_colors(data);assert colors,'No native palette inspected'
 assert all(not any(c['type']==0x2019 for c in frame['chunks']) for frame in data['frames'][1:]),'Per-frame palette churn'
 neutral=Image.open(ROOT/'inputs/neutral.png').convert('RGBA');expected_rest=Image.new('RGBA',(width,height));expected_rest.paste(neutral,(64,0))
 frames=[];reports=[]
 for f,relative in enumerate(delivery['frames']):
  frame=composite(data,f)
  with Image.open(folder/relative) as exported:assert exported.convert('RGBA').tobytes()==frame.tobytes(),f'F{f+1} native/export mismatch'
  alpha=set(frame.getchannel('A').get_flattened_data());assert alpha<={0,255},f'F{f+1} partial alpha'
  assert frame.getbbox() and frame.getbbox()[0]>0 and frame.getbbox()[2]<width and frame.getbbox()[1]>0 and frame.getbbox()[3]<height,f'F{f+1} clipped canvas edge'
  visible={pixel[:3] for pixel in frame.get_flattened_data() if pixel[3]}
  assert visible<=colors,f'F{f+1} off-palette pixels'
  body=check_alpha_coverage(frame)
  box=delivery['bag_bounds_xyxy'][f]
  assert len(box)==4 and all(isinstance(v,(int,float)) for v in box) and 0<=box[0]<box[2]<=width and 0<=box[1]<box[3]<=height
  bag_area=frame.crop(tuple(int(v) for v in box));assert bag_area.getchannel('A').getbbox(),f'F{f+1} empty bag bounds'
  offset=delivery['root_offsets'][f];assert len(offset)==2 and all(isinstance(v,int) for v in offset)
  assert connected_pair(frame,delivery['head_xy'][f],delivery['thorax_xy'][f]),f'F{f+1} detached head/torso or invalid opaque landmarks'
  reports.append({'frame':f+1,'phase':delivery['phases'][f],'duration_ms':times[f],'bounds':frame.getbbox(),'opaque_pixels':frame.getchannel('A').histogram()[255],'visible_colors':len(visible),'alpha_holes_for_visual_review_xy':body['hole_pixels_xy'],'bag_bounds_xyxy':box,'root_offset':offset})
  frames.append(frame)
 assert frames[0].tobytes()==frames[-1].tobytes()==expected_rest.tobytes(),'Must return to exact existing idle at x64'
 # Fresh reopening must be real MCP evidence, not a second use of this decoder.
 reopen=delivery.get('reopen_sheet')
 assert reopen,'Missing independent fresh-MCP-reopen sheet path'
 with Image.open(folder/reopen) as image:
  image=image.convert('RGBA');assert image.size==(width*count,height),'Expected untrimmed horizontal reopen sheet'
  for f,frame in enumerate(frames):assert image.crop((width*f,0,width*(f+1),height)).tobytes()==frame.tobytes(),f'F{f+1} fresh reopen mismatch'
 gifs={}
 for scale in [1,3]:
  key=f'gif_{scale}x'
  if key in delivery:gifs[key]=check_gif(folder/delivery[key],frames,times,scale)
 return {'passed':True,'native':str(native_path.relative_to(ROOT)),'native_sha256':sha(native_path),'canvas':data['canvas'],'frame_count':count,'durations_ms':times,'cycle_ms':sum(times),'native_layers':data['layers'],'active_frames_1based':delivery['active_frames_1based'],'all_native_exports_and_fresh_reopen_exact':True,'rest_return_exact_existing_neutral':True,'shared_native_palette_and_binary_alpha':True,'frames':reports,'gifs':gifs,'limits':'Geometry/palette/timeline/source proof only. Coverage holes are diagnostic pending reviewed handle/limb/hair openings; movement quality requires visual/user review.'}

def main():
 report=inspect_delivery();(ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['frames','native_layers']},indent=2))
if __name__=='__main__':main()
