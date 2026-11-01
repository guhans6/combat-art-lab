-- v03: incremental native head edit. Opens preserved v02; reads no reference raster.
-- No drawing can write into the locked neck or anything below row 30.
local root=assert(app.params["root"])
local function path(p) return app.fs.joinPath(root,p) end
local source=app.open(path("assets/source/standing-v02/standing.aseprite"))
assert(source.width==128 and source.height==192 and #source.layers==12)
local W,H=128,192
local colors={
 hair_ink="402b29",hair_dark="49322d",hair_shadow="57382e",hair="6b4435",
 hair_light="7d503a",hair_glint="925e43",
 face_base="ffab79",face_light="ffb47f",face_mid="f69d6d",face_shadow="d7855a",face_blush="ef9470",
 skin_edge="995e48",skin_shadow="cd815b",eye_ink="3f2b28",eye_brown="754632",
 eye_light="b87850",eye_white="f8e7d2",eye_far="d1b9a5",tie="e8d8b9",
}
local C={clear=0}
for k,v in pairs(colors) do
 C[k]=app.pixelColor.rgba(tonumber(v:sub(1,2),16),tonumber(v:sub(3,4),16),tonumber(v:sub(5,6),16),255)
end
local function allowed(x,y)
 return x>=34 and x<=79 and y>=2 and y<=30 and not(y>=29 and x>=57 and x<=65)
end
local function fullImage(cel)
 local im=Image(W,H,ColorMode.RGB);im:drawImage(cel.image,cel.position);return im
end
local base,visibility={},{ }
for i,l in ipairs(source.layers) do base[i]=fullImage(l:cel(1));visibility[i]=l.isVisible end
local image,current
local function px(x,y,c)
 if allowed(x,y) then image:drawPixel(x,y,C[c]) end
end
local function line(c,points)
 for i=1,#points-1 do
  local x0,y0=points[i][1],points[i][2];local x1,y1=points[i+1][1],points[i+1][2]
  local dx,dy=math.abs(x1-x0),-math.abs(y1-y0)
  local sx,sy=x0<x1 and 1 or -1,y0<y1 and 1 or -1;local err=dx+dy
  while true do
   px(x0,y0,c);if x0==x1 and y0==y1 then break end
   local e=2*err;if e>=dy then err=err+dy;x0=x0+sx end
   if e<=dx then err=err+dx;y0=y0+sy end
  end
 end
end
local function poly(c,points,edge)
 local lo,hi=H,0
 for _,p in ipairs(points) do lo=math.min(lo,p[2]);hi=math.max(hi,p[2]) end
 for y=lo,hi do
  local hits={};local scan=y+0.5
  for i,a in ipairs(points) do
   local b=points[i%#points+1]
   if (a[2]<=scan and b[2]>scan) or (b[2]<=scan and a[2]>scan) then
    hits[#hits+1]=a[1]+(scan-a[2])*(b[1]-a[1])/(b[2]-a[2])
   end
  end
  table.sort(hits)
  for i=1,#hits-1,2 do
   for x=math.ceil(hits[i]-0.5),math.floor(hits[i+1]-0.5) do px(x,y,c) end
  end
 end
 if edge then
  local closed={};for _,p in ipairs(points) do closed[#closed+1]=p end
  closed[#closed+1]=points[1];line(edge,closed)
 end
end
local function rect(c,x,y,w,h) poly(c,{{x,y},{x+w,y},{x+w,y+h},{x,y+h}}) end
local function finish()
 if current then
  for y=0,H-1 do for x=0,W-1 do
   if not allowed(x,y) then assert(image:getPixel(x,y)==base[current]:getPixel(x,y)) end
  end end
  local cel=source.layers[current]:cel(1);cel.image=image;cel.position=Point(0,0)
 end
end
local function edit(i,name)
 finish();assert(source.layers[i].name==name);current=i;image=base[i]:clone()
 for y=2,30 do for x=34,79 do if allowed(x,y) then image:drawPixel(x,y,0) end end end
end

-- Rear hair: three overlapping clumps, partial gaps and a pale tie.
edit(1,"01-hair-back")
poly("hair_dark",{{49,10},{47,10},{45,11},{43,12},{40,13},{38,15},{37,17},{35,19},{35,21},{36,20},{35,23},{36,26},{38,27},{39,29},{42,30},{43,29},{45,30},{46,29},{48,31},{50,31},{51,29},{53,28},{55,25},{56,21},{55,17},{53,13}},"hair_ink")
poly("hair",{{44,12},{46,12},{49,14},{50,17},{48,20},{45,20},{42,18},{39,19},{38,21},{37,19},{39,16},{41,14}})
poly("hair_light",{{41,14},{44,13},{47,13},{48,14},{44,15},{41,16},{38,19},{38,17}})
poly("hair_shadow",{{43,17},{46,17},{47,20},{45,23},{42,25},{40,25},{38,23},{39,20}})
poly("hair",{{38,21},{40,19},{42,19},{41,23},{42,26},{45,27},{45,29},{42,29},{39,27},{37,24}})
poly("hair_light",{{39,21},{40,20},{40,23},{41,25},{43,26},{42,27},{40,26},{38,23}})
poly("hair_shadow",{{47,20},{50,18},{53,19},{53,23},{51,26},{49,28},{48,30},{46,29},{47,26},{45,25}})
poly("hair",{{49,21},{51,20},{52,22},{50,25},{48,27},{47,27}})
line("hair_ink",{{45,15},{44,18},{43,20}})
line("hair_ink",{{48,17},{47,20},{45,23}})
line("hair_ink",{{38,22},{39,25},{42,27}})
line("hair_ink",{{43,29},{45,28},{46,26}})
line("hair_light",{{49,23},{48,25},{47,26}})
line("clear",{{35,24},{36,26},{38,27}})
line("hair_dark",{{38,27},{40,29},{42,29}})
line("hair",{{49,28},{50,30},{51,30}})
poly("hair",{{49,10},{49,8},{51,6},{53,7},{54,9},{54,11},{52,13},{50,13}},"hair_ink")
line("hair_light",{{50,9},{51,8},{52,8},{53,10}})
poly("tie",{{45,12},{47,12},{48,13},{49,15},{48,16},{47,15},{47,14},{45,13}})

-- Face: a broad cheek, softly tapered jaw and compact features. Neck is masked off.
edit(5,"05-skin-face")
poly("face_base",{{58,16},{64,14},{68,15},{71,17},{72,20},{73,22},{73,24},{72,25},{72,27},{71,28},{70,29},{69,30},{67,31},{65,31},{62,30},{60,29},{59,27},{57,26},{56,24},{56,21}})
poly("face_mid",{{58,20},{60,20},{61,22},{60,25},{61,27},{63,29},{65,30},{64,31},{61,29},{59,27},{57,25}})
poly("face_light",{{63,19},{66,18},{69,19},{71,21},{71,24},{69,26},{65,27},{62,25},{61,22}})
poly("face_base",{{61,24},{64,24},{66,25},{69,25},{72,24},{72,27},{70,29},{68,30},{65,30},{63,29},{61,27}})
poly("face_blush",{{60,24},{62,24},{63,25},{62,26},{60,26}})
line("face_mid",{{71,24},{72,24}})
line("face_shadow",{{60,27},{61,28},{63,29}})
poly("face_mid",{{54,22},{55,21},{57,22},{57,24},{56,26},{55,26},{54,25}},"skin_shadow")
poly("face_base",{{55,22},{56,22},{56,24},{55,25},{54,24}})
line("face_shadow",{{55,23},{56,23},{55,24}})

-- Front hair: irregular fringe openings support both eyes, plus loose ear strands.
edit(10,"10-hair-front")
poly("hair",{{48,13},{49,10},{51,8},{54,7},{57,5},{61,5},{65,5},{68,6},{71,6},{73,5},{74,3},{73,2},{75,3},{76,5},{75,7},{74,8},{76,10},{78,12},{77,14},{78,16},{77,19},{76,22},{76,25},{74,28},{73,28},{74,24},{73,21},{72,18},{71,16},{70,18},{69,18},{69,16},{67,13},{67,16},{66,18},{64,19},{63,21},{61,22},{60,25},{59,24},{59,22},{57,21},{56,22},{55,22},{54,24},{54,26},{55,28},{56,30},{54,30},{52,28},{52,25},{50,24},{50,20},{49,17}},"hair_ink")
poly("hair_shadow",{{49,14},{52,13},{54,16},{56,18},{57,20},{55,21},{53,24},{54,27},{55,29},{53,28},{52,25},{50,23},{50,20}})
poly("hair_light",{{51,11},{54,9},{58,8},{61,8},{58,10},{56,11},{53,12},{51,14}})
poly("hair_light",{{61,7},{64,6},{67,7},{69,8},{66,8},{64,7}})
poly("hair_light",{{54,15},{57,13},{61,10},{64,9},{63,11},{60,13},{58,15},{56,17}})
poly("hair_shadow",{{61,12},{65,9},{68,9},{66,12},{64,15},{62,17},{60,20},{59,22},{58,21},{59,17}})
poly("hair_light",{{65,12},{68,10},{70,10},{71,12},{69,11},{68,14},{67,16},{66,16}})
poly("hair_shadow",{{70,12},{71,12},{72,15},{72,17},{71,18},{70,16}})
poly("hair_light",{{73,10},{75,11},{76,13},{75,16},{74,17},{74,14}})
poly("hair_dark",{{77,16},{76,20},{75,22},{75,25},{73,28},{74,24},{74,21},{75,18}})
line("hair_ink",{{61,8},{58,11},{55,13},{52,14}})
line("hair_ink",{{65,7},{68,9},{70,11}})
line("hair_dark",{{63,10},{60,13},{57,15},{54,16}})
line("hair_ink",{{66,11},{64,14},{62,17},{61,20}})
line("hair_ink",{{71,9},{73,11},{74,14},{74,17}})
line("hair_ink",{{57,17},{56,19},{57,21},{58,23},{59,24}})
line("hair_dark",{{53,25},{54,27},{55,28}})
line("hair_glint",{{52,11},{54,10}})
line("hair_glint",{{57,12},{59,11}})
line("hair_glint",{{57,8},{59,7},{61,7}})
rect("hair_light",62,5,3,1);rect("hair_glint",66,6,2,1)
line("hair_glint",{{73,8},{74,7},{75,5}})
line("hair_light",{{51,18},{52,20},{53,21}})

edit(11,"11-face-features")
-- Near pupil x64 and far pupil x70 look right; far eye is deliberately narrower.
poly("eye_white",{{61,21},{62,20},{64,20},{65,21},{65,23},{64,24},{62,24},{61,23}})
rect("eye_brown",63,21,2,3)
rect("eye_ink",64,21,1,2);px(63,23,"eye_light")
line("eye_ink",{{60,21},{61,20},{63,19},{65,20}})
px(61,21,"hair_shadow")
poly("eye_far",{{68,21},{69,20},{71,21},{71,23},{70,24},{68,23}})
rect("eye_brown",70,21,1,2);px(70,21,"eye_ink");px(69,23,"eye_far")
line("eye_ink",{{68,21},{69,20},{70,20}})
-- Uneven restrained brows, no extra sparkle pixels.
line("hair_shadow",{{61,17},{63,17},{64,18}})
line("hair_shadow",{{68,18},{70,18}})
px(71,24,"face_mid")
line("face_shadow",{{67,27},{68,27},{69,26}})
px(69,27,"face_mid")
finish()

local edited={ [1]=true,[5]=true,[10]=true,[11]=true }
local metadata={base="standing-v02",width=W,height=H,frames=#source.frames,layers={},headScope={xMin=34,xMax=79,yMin=2,yMax=30,neckNotch={xMin=57,xMax=65,yMin=29}},eyes={nearPupil={64,21},farPupil={70,21},nearWidth=5,farWidth=3},addedPaletteColors=0}
for i,l in ipairs(source.layers) do
 local after=fullImage(l:cel(1));local count=0
 for y=0,H-1 do for x=0,W-1 do
  if after:getPixel(x,y)~=base[i]:getPixel(x,y) then
   assert(edited[i] and allowed(x,y));count=count+1
  end
 end end
 if not edited[i] then assert(after:isEqual(base[i])) end
 metadata.layers[#metadata.layers+1]={name=l.name,changedPixels=count,visible=l.isVisible}
end
source:saveAs(path("assets/source/standing-v03/standing.aseprite"))
source:saveCopyAs(path("assets/export/standing-v03/standing.png"))
source:close()
local reopened=app.open(path("assets/source/standing-v03/standing.aseprite"))
assert(#reopened.layers==12 and #reopened.frames==1)
reopened:saveCopyAs(path("assets/export/standing-v03/standing-reopened.png"))
for _,l in ipairs(reopened.layers) do l.isVisible=false end
for i,l in ipairs(reopened.layers) do
 l.isVisible=true;reopened:saveCopyAs(path("assets/previews/standing-v03/layers/"..l.name..".png"));l.isVisible=false
end
reopened:close()
local f=assert(io.open(path("docs/experiments/2026-10-26-head-v03/source-checks.json"),"w"));f:write(json.encode(metadata));f:close()
print("PASS: v03 saved/reopened; every layer edit inside head mask; eight other layers unchanged")
