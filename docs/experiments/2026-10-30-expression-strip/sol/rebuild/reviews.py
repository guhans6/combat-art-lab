"""Build review-only sheets from exact supplied sprite exports; never alter native art."""
from pathlib import Path
from PIL import Image,ImageDraw
import argparse,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--neutral',required=True);p.add_argument('--smile',required=True);p.add_argument('--surprise',required=True);a=p.parse_args()
R=Path(__file__).resolve().parents[1];repo=R.parents[3];out=R/'reviews'
refpath=repo/'assets/references/approved-2026-10-26/character-closeup.png';scene=repo/'assets/references/approved-2026-10-26/character-scene.png';baseline=repo/'docs/experiments/2026-10-30-luna-fullbody-once/trial-b/passes/luna6-fullbody-cleanup.png'
paths=[baseline,Path(a.neutral),Path(a.smile),Path(a.surprise)];labels=['Original baseline','Neutral','Subtle smile','Surprise'];ims=[Image.open(q).convert('RGBA') for q in paths];assert all(im.size==(128,192) for im in ims)
ref=Image.open(refpath).convert('RGBA');rc=(520,170,820,470);sc=(50,10,80,40);refhead=ref.crop(rc).resize((30,30),Image.Resampling.LANCZOS)
for scale in [1,8]:
 panels=[('Approved original (preview)',refhead)]+[(label,im.crop(sc)) for label,im in zip(labels,ims)];cw=max(190,30*scale+20);sheet=Image.new('RGB',(len(panels)*cw,30*scale+100),'#303238');d=ImageDraw.Draw(sheet)
 for i,(label,im) in enumerate(panels):
  d.text((i*cw+8,10),label,fill='white');matte=Image.new('RGBA',im.size,'#303238');matte.alpha_composite(im);sheet.paste(matte.resize((30*scale,30*scale),Image.Resampling.NEAREST),(i*cw+(cw-30*scale)//2,40))
 d.text((8,sheet.height-38),'Reference crop reduced for approximate landmark registration; source/cutout pose differences remain.',fill='white');d.text((8,sheet.height-21),f'All actual sprite pixels shown at {scale}x nearest-neighbor; no sprite warp or smoothing.',fill='white');sheet.save(out/f'final-head-{scale}x.png')
for scale in [1,3]:
 cw=128*scale+28;sheet=Image.new('RGB',(len(ims)*cw,192*scale+76),'#303238');d=ImageDraw.Draw(sheet)
 for i,(label,im) in enumerate(zip(labels,ims)):
  d.text((i*cw+8,8),label,fill='white');matte=Image.new('RGBA',im.size,'#303238');matte.alpha_composite(im);sheet.paste(matte.resize((128*scale,192*scale),Image.Resampling.NEAREST),(i*cw+14,30))
 d.text((8,sheet.height-24),f'Exact actual exports at {scale}x NN. Diagnostic display; gameplay size not selected.',fill='white');sheet.save(out/f'final-fullbody-{scale}x.png')
# Direct reference at source pixels, with a sprite region at 8x alongside it.
direct=ref.crop(rc);sheet=Image.new('RGB',(direct.width+4*240+60,380),'#303238');d=ImageDraw.Draw(sheet);sheet.paste(direct,(10,40));d.text((10,10),'Approved original: source pixels',fill='white')
for i,(label,im) in enumerate(zip(labels,ims)):
 x=330+240*i;d.text((x,10),label,fill='white');matte=Image.new('RGBA',(30,30),'#303238');matte.alpha_composite(im.crop(sc));sheet.paste(matte.resize((240,240),Image.Resampling.NEAREST),(x,40))
sheet.save(out/'final-direct-original-head-8x.png')
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
meta={'reference':str(refpath),'reference_sha256':sha(refpath),'reference_crop':rc,'reference_preview':[30,30],'reference_preview_filter':'Lanczos for diagnostic only','sprite_head_crop':sc,'sprite_scale':'integer nearest-neighbor only','approximate_registration':'near eye ref(655,289)->native(63.5,21.9), far eye(720,278)->(70,20.8), mouth(690,342)->(67,27.2), chin y374->30.4. Residual pose and geometry differences remain.','panels':[{'label':l,'actual_export':str(q),'sha256':sha(q)} for l,q in zip(labels,paths)]};(out/'final-review-provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta,indent=2))
