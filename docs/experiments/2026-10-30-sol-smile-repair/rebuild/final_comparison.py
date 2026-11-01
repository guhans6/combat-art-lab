from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];I=R/'inputs';ref=Image.open(I/'character-closeup.png').convert('RGBA');B=Image.open(I/'baseline.png').convert('RGBA');p1=Image.open(R/'passes/pass-01-reopen.png').convert('RGBA');p2=Image.open(R/'passes/pass-02-reopen.png').convert('RGBA')
# 10 source pixels -> 1 target preview pixel. Eyeline/chin map approximately, not a warped reference.
refbox=(520,170,820,470);box=(50,10,80,40);rp=ref.crop(refbox).resize((30,30),Image.Resampling.LANCZOS)
for s in [1,8,12]:
 panels=[('Approved ref preview',rp),('Unchanged baseline',B.crop(box)),('Pass01 heavier corners',p1.crop(box)),('Pass02 quieter',p2.crop(box))];cw=max(170,30*s+20);out=Image.new('RGB',(cw*4,30*s+80),'#303238');d=ImageDraw.Draw(out)
 for i,(label,im) in enumerate(panels):
  d.text((i*cw+8,8),label,fill='white');matte=Image.new('RGBA',im.size,'#303238');matte.alpha_composite(im);out.paste(matte.resize((30*s,30*s),Image.Resampling.NEAREST),(i*cw+(cw-30*s)//2,40))
 d.text((8,out.height-22),'Reference comparison resample; sprite panels exact native pixels at integer NN zoom.',fill='white');out.save(R/'reviews'/f'candidate-comparison-head-{s}x.png')
metadata={'reference_source':'inputs/character-closeup.png','reference_crop_half_open':refbox,'reference_preview_size':[30,30],'reference_resampling':'Lanczos for review only','candidate_crop_half_open':box,'candidate_resampling':'integer nearest neighbor only','approximate_alignment':'Ref near eye (655,289)->(63.5,21.9), far eye (720,278)->(70,20.8), chin y374->30.4, mouth center (691,340)->(67.1,27). Candidate mouth center68; residual source/native pose differences remain.','earlier_pass01_reference_crop':[570,210,770,410],'earlier_crop_limitation':'Equal crop size did not align eye-chin span. Anatomical comparison uses wider source crop; no sprite pixels transformed.'}
(R/'reviews/candidate-comparison-provenance.json').write_text(json.dumps(metadata,indent=2))
