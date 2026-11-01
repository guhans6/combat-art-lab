-- Generated sheet guides eyelid closure only. Keep native base geometry and palette.
local dir=assert(app.params.out)
local s=app.open(dir..'/b02-expression.aseprite')
local data=dofile(dir..'/data.lua');local C={}
for k,c in pairs(data.colors) do C[k]=app.pixelColor.rgba(c[1],c[2],c[3],255) end
local target
for _,l in ipairs(s.layers) do if l.name=='08-eyes-brows' then target=l end end
assert(target)
-- Native base has visible-part extraction; this is a bust-expression sample, not a rig.
local base={};for _,l in ipairs(s.layers) do local c=l:cel(1);base[l.name]={image=Image(c.image),pos=Point(c.position.x,c.position.y)} end
for i=2,5 do
 local f=s:newEmptyFrame(i)
 for _,l in ipairs(s.layers) do local b=base[l.name];s:newCel(l,f,b.image,b.pos) end
end
local function xy(p) return math.floor((p[1]-380)/4+.5),math.floor((p[2]-64)/4+.5) end
local im
local function put(x,y,c) if x>=0 and x<120 and y>=0 and y<112 then im:drawPixel(x,y,C[c]) end end
local function line(c,pts)
 for i=1,#pts-1 do local x,y=xy(pts[i]);local tx,ty=xy(pts[i+1]);local dx=math.abs(tx-x);local dy=-math.abs(ty-y);local sx=x<tx and 1 or -1;local sy=y<ty and 1 or -1;local err=dx+dy
 while true do put(x,y,c);if x==tx and y==ty then break end;local e=2*err;if e>=dy then err=err+dy;x=x+sx end;if e<=dx then err=err+dx;y=y+sy end end end
end
local function poly(c,pts)
 local q={};local ymin,ymax=112,0
 for _,p in ipairs(pts) do local x,y=xy(p);q[#q+1]={x,y};ymin=math.min(ymin,y);ymax=math.max(ymax,y) end
 for y=ymin,ymax do local xs={};for i=1,#q do local a,b=q[i],q[i%#q+1];if (a[2]<=y+.5 and b[2]>y+.5) or (b[2]<=y+.5 and a[2]>y+.5) then xs[#xs+1]=a[1]+(y+.5-a[2])*(b[1]-a[1])/(b[2]-a[2]) end end;table.sort(xs);for i=1,#xs-1,2 do for x=math.ceil(xs[i]-.5),math.floor(xs[i+1]-.5) do put(x,y,c) end end end
end
for _,f in ipairs({2,3,4}) do
 im=Image(120,112,ColorMode.RGB);local cel=target:cel(f);im:drawImage(cel.image,cel.position)
 if f==3 then
  poly('skinlight',{{618,282},{628,274},{645,273},{665,277},{667,308},{658,312},{639,307},{622,300}})
  poly('skinlight',{{708,265},{718,260},{730,260},{732,288},{726,297},{714,290}})
  line('skinshadow',{{620,290},{634,286},{649,286},{661,282}})
  line('feature',{{620,297},{630,301},{645,300},{661,294}})
  line('feature',{{710,284},{719,288},{729,282}})
 else
  poly('skinlight',{{618,282},{628,274},{645,273},{665,277},{665,288},{646,291},{629,296},{619,298}})
  poly('skinlight',{{708,265},{718,260},{730,260},{732,278},{720,280},{710,282}})
  line('feature',{{620,296},{633,291},{648,287},{661,286}})
  line('feature',{{710,280},{719,275},{730,273}})
 end
 cel.image=im;cel.position=Point(0,0)
end
local durations={1.6,.05,.09,.06,.6}
for i,f in ipairs(s.frames) do f.duration=durations[i];local export=Image(120,112,ColorMode.RGB);export:drawSprite(s,i);export:saveAs(dir..'/blink-frame-'..i..'.png') end
local tag=s:newTag(1,5);tag.name='blink-probe'
s:saveAs(dir..'/blink-probe.aseprite');s:close()
s=app.open(dir..'/blink-probe.aseprite')
for i,f in ipairs(s.frames) do local export=Image(120,112,ColorMode.RGB);export:drawSprite(s,i);export:saveAs(dir..'/blink-frame-'..i..'-reopened.png') end
s:close();print('Blink: five frames, same native grid, eight protected layers, zero root travel.')
