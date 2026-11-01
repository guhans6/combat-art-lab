from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent;src=R.parent/'2026-10-30-tote-attack/runtime/godot';dst=R/'runtime/godot'
if not dst.exists():shutil.copytree(src,dst,ignore=shutil.ignore_patterns('.godot','evidence','attack','*.import'))
(dst/'attack').mkdir(exist_ok=True);(dst/'evidence').mkdir(exist_ok=True)
meta=json.loads((R/'delivery.json').read_text())
for i,path in enumerate(meta['frames']):shutil.copy2(R/path,dst/'attack'/f'frame-{i:02}.png')
shutil.copy2(R/meta['frames'][0],dst/'attack/idle.png')
(dst/'attack/metadata.json').write_text(json.dumps(meta,indent=2))
print(dst)
