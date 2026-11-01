from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import shutil,json
H=Path(__file__).resolve().parent;R=H.parents[2]
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18)
out=Image.new('RGB',(1024,1250),'#24242d');d=ImageDraw.Draw(out)
for x,title,path in [(16,'Approved original crop: identity/style anchor',H/'inputs/original-crop.png'),(520,'Actual final C export, 4x nearest neighbor',H/'c01-restored-mouth.png')]:
 d.text((x,12),title,font=font,fill='white');im=Image.open(path).convert('RGBA').resize((480,448),Image.Resampling.NEAREST);bg=Image.new('RGBA',im.size,'#34343e');bg.alpha_composite(im);out.paste(bg.convert('RGB'),(x,45))
d.text((16,515),'Generated 3-pose intermediate: eyelid guidance only; display reduced to fit',font=font,fill='white');im=Image.open(H/'generated-blink-reference.png');im.thumbnail((992,400));out.paste(im,(16,550))
d.text((16,960),'Final native blink: shared geometry/palette, eye changes only',font=font,fill='white');im=Image.open(H/'blink-filmstrip.png').resize((992,224),Image.Resampling.NEAREST);out.paste(im,(16,995));out.save(H/'motion-reference-comparison.png')
# Actual export crop proof of the source-supported smile rollback.
out=Image.new('RGB',(600,170),'#34343e');d=ImageDraw.Draw(out)
for i,n in enumerate(['b01-hair-cleanup','b02-expression','c01-restored-mouth']):
 im=Image.open(H/(n+'.png')).convert('RGB').crop((70,65,85,73)).resize((180,96),Image.Resampling.NEAREST);out.paste(im,(i*200,50));d.text((i*200,12),n,font=font,fill='white')
out.save(H/'mouth-restoration-proof.png')
for name in ['motion-reference-comparison.png','playback-playing.png','playback-closed.png','mouth-restoration-proof.png']:
 shutil.copy2(H/name,R/'assets/previews/assisted-bust-v01'/name)
print('Final generated/original/actual reference evidence and mouth rollback proof saved.')
