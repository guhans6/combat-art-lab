-- Restrained full-standing idle. Existing generated blink sheet guides eyelids only.
local dir=assert(app.params.out);local data=dofile(dir..'/data.lua')
local s=app.open(dir..'/standing-cleaned.aseprite')
local base={};for _,l in ipairs(s.layers) do local c=l:cel(1);local im=Image(96,216,ColorMode.RGB);im:drawImage(c.image,c.position);base[l.name]=im end
for i=2,8 do local f=s:newEmptyFrame(i);for _,l in ipairs(s.layers) do s:newCel(l,f,base[l.name],Point(0,0)) end end
local skin=app.pixelColor.rgba(217,135,91,255)
local lid=app.pixelColor.rgba(65,41,39,255)
local phases={'rest','inhale','half','closed','half','inhale','exhale','rest'}
local durations={700,650,50,100,70,600,500,330}
for i,phase in ipairs(phases) do
 local inhale=i>=2 and i<=6
 for _,l in ipairs(s.layers) do
  local original=base[l.name];local im=Image(96,216,ColorMode.RGB)
  for y=0,215 do for x=0,95 do
   local sy=y
   if inhale and l.name~='01-denim' and l.name~='02-shoes' and l.name~='03-far-shoe' then
    local entire=l.name~='05-jacket'
    if entire or y<90 then sy=y+1 end
   end
   if sy<216 then im:drawPixel(x,y,original:getPixel(x,sy)) end
  end end
  if l.name=='13-eyes-mouth' and (phase=='half' or phase=='closed') then
   -- Positions are read from the static export, then offset for the inhale.
   local dy=inhale and -1 or 0
   if phase=='closed' then
    for y=28,31 do for x=40,44 do im:drawPixel(x,y+dy,skin) end end
    for y=28,30 do for x=49,50 do im:drawPixel(x,y+dy,skin) end end
    for _,p in ipairs({{40,30},{41,31},{42,31},{43,30},{44,30},{49,30},{50,30}}) do im:drawPixel(p[1],p[2]+dy,lid) end
   else
    for y=28,29 do for x=40,44 do im:drawPixel(x,y+dy,skin) end end
    for x=49,50 do im:drawPixel(x,28+dy,skin) end
    for _,p in ipairs({{40,30},{41,30},{42,29},{43,29},{44,29},{49,29},{50,29}}) do im:drawPixel(p[1],p[2]+dy,lid) end
   end
  end
  local c=l:cel(i);c.image=im;c.position=Point(0,0)
 end
 s.frames[i].duration=durations[i]/1000
 local export=Image(96,216,ColorMode.RGB);export:drawSprite(s,i);export:saveAs(dir..'/idle-frame-'..string.format('%02d',i-1)..'.png')
end
-- Disjoint visible parts require backing where relative motion reveals their joins.
local backing=s:newLayer();backing.name='00-joint-underpaint';backing.stackIndex=1
for frame,points in pairs(dofile(dir..'/motion-underpaint.lua')) do
 local image=Image(96,216,ColorMode.RGB)
 for _,p in ipairs(points) do image:drawPixel(p[1],p[2],app.pixelColor.rgba(p[3],p[4],p[5],255)) end
 s:newCel(backing,s.frames[frame],image,Point(0,0))
end
-- Refresh actual frame exports after backing has been applied.
for i=1,8 do
 local image=Image(96,216,ColorMode.RGB);image:drawSprite(s,i)
 image:saveAs(dir..'/idle-frame-'..string.format('%02d',i-1)..'.png')
end
local tag=s:newTag(1,8);tag.name='idle-standing'
s:saveAs(dir..'/standing-idle.aseprite');s:close()
s=app.open(dir..'/standing-idle.aseprite')
for i=1,8 do local im=Image(96,216,ColorMode.RGB);im:drawSprite(s,i);im:saveAs(dir..'/idle-frame-'..string.format('%02d',i-1)..'-reopened.png') end
s:close();print('Saved/reopened 8 native idle frames; 3000 ms cycle; feet/denim fixed, inhale one native pixel, blink only eyes.')
