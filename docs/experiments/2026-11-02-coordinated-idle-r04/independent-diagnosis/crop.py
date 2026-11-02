from PIL import Image,ImageDraw
p='/private/tmp/atmospheric-idle-sample-r04/keys/'
out=Image.new('RGB',(900,640),(75,75,78));d=ImageDraw.Draw(out)
for i in range(3):
 im=Image.open(p+f'key-{i}.png').convert('RGBA'); im=im.crop((28,34,64,98)); bg=Image.new('RGBA',im.size,(75,75,78,255));bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((300,640),Image.Resampling.NEAREST),(i*300,0))
 for y in range(40,98,10):d.text((i*300,y*10-340),str(y),fill='white')
out.save('/private/tmp/idle-r04-diagnosis/upper-crop.png')
