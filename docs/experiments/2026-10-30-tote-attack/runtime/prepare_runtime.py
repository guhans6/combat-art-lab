"""Bind verified artist exports to an isolated copy of the existing Godot preview."""
from pathlib import Path
import hashlib,json,shutil,sys
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[2]
sys.path.insert(0,str(ROOT))
from verify_attack import inspect_delivery

def main():
 proof=inspect_delivery()
 assert proof['passed'],'Native/export proof must pass before runtime binding'
 delivery_path=ROOT/'artist/delivery.json'
 data=json.loads(delivery_path.read_text());folder=delivery_path.parent
 native=folder/data['native'];frames=[folder/p for p in data['frames']]
 times=data['durations_ms'];count=len(frames)
 assert count==len(times)==len(data['phases'])==len(data['root_offsets'])==len(data['bag_bounds_xyxy'])
 assert data['active_frames_1based'] and all(1<=f<=count for f in data['active_frames_1based'])
 assert all(isinstance(ms,int) and ms>0 for ms in times)
 assert all(Image.open(p).size==tuple(data['canvas']) for p in frames)
 target=ROOT/'runtime/godot'
 if target.exists():raise SystemExit('Existing runtime preserved. Use a new target for another variant.')
 shutil.copytree(REPO/'godot/standing-idle-lab',target,ignore=shutil.ignore_patterns('.godot','evidence','.DS_Store'))
 (target/'evidence').mkdir();(target/'attack').mkdir()
 for f,p in enumerate(frames):shutil.copy2(p,target/f'attack/frame-{f:02d}.png')
 # First/last native drawing is the reviewed idle placed on the attack canvas.
 shutil.copy2(frames[0],target/'attack/idle.png')
 fields=['canvas','durations_ms','phases','active_frames_1based','root_offsets','bag_bounds_xyxy']
 meta={k:data[k] for k in fields};meta['native_sha256']=hashlib.sha256(native.read_bytes()).hexdigest()
 (target/'attack/metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 shutil.copy2(ROOT/'runtime/attack_preview.gd',target/'preview.gd')
 project=target/'project.godot';project.write_text(project.read_text().replace('Standing Idle - Combat Art Lab','Tote swing attack - isolated prototype'))
 print(target)
if __name__=='__main__':main()
