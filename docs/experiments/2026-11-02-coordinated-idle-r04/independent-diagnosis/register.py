from PIL import Image
p='/private/tmp/atmospheric-idle-sample-r04/keys/'
a=[Image.open(p+f'f{i}-owner-near-forearm-hand.png').convert('RGBA') for i in range(3)]
for i in (1,2):
 for dx in range(-2,3):
  for dy in range(-2,3):
   diff=0;n=0
   for y in range(74,95):
    for x in range(34,48):
     xx,yy=x+dx,y+dy
     if a[0].getpixel((x,y))!=a[i].getpixel((xx,yy)):diff+=1
   if diff<20: print(i,dx,dy,diff)
# skin only map all image, locate pixel translation exact
skin={(173,128,86,255),(185,141,96,255),(121,88,61,255)}
for i in (1,2):
 for dx in range(-2,3):
  for dy in range(-2,3):
   base={(x,y,a[0].getpixel((x,y))) for y in range(73,95) for x in range(33,49) if a[0].getpixel((x,y)) in skin}
   dest={(x-dx,y-dy,a[i].getpixel((x,y))) for y in range(70,97) for x in range(30,52) if a[i].getpixel((x,y)) in skin}
   err=len(base^dest)
   if err<4: print('skin',i,dx,dy,err,len(base))
