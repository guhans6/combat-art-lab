import sys,json
from pathlib import Path
sys.path.insert(0,'docs/experiments/2026-10-30-evidence-idle-four-model/sol61')
from native_read import read,composite,sha
R=Path('docs/experiments/2026-10-31-recovery-grip/artist');a=read(R/'source/recovery-grip-pass02.aseprite');c=composite(a,8)
def color(im,x,y):
 p=im.getpixel((x,y));return '#'+''.join(f'{v:02x}' for v in p)
pts=[(175,83),(176,83),(174,84),(175,84),(176,84),(173,85),(174,85),(175,85),(172,86),(173,86),(174,86),(171,87),(172,87),(173,87),(170,88),(171,88),(172,88),(170,89),(171,89),(171,90),(172,90),(173,90),(174,90),(175,90),(176,90),(172,91),(174,91),(175,91),(161,109),(162,109),(163,109),(187,99),(188,99),(189,99)]
out={'native_sha256':sha(R/'source/recovery-grip-pass02.aseprite'),'coordinates_native_320x192':{},'F9':9}
for x,y in pts:out['coordinates_native_320x192'][f'{x},{y}']={'composite':color(c,x,y),'owners':{a['layers'][l]['name']:color(a['cels'][(8,l)]['image'],x,y) for l in [4,5,6]}}
(R/'proof/attachment-readback.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v['composite'] for k,v in out['coordinates_native_320x192'].items()},indent=2))
