local dir=assert(app.params.out)
local data=dofile(dir..'/data.lua')
local candidates={'gated/a00-traced-planes','gated/a01-hair-clusters','gated/a02-expression','b00-separated-seed','b01-hair-cleanup','b02-expression'}
for _,name in ipairs(candidates) do
 local s=app.open(dir..'/'..name..'.aseprite')
 assert(s.width==120 and s.height==112 and #s.layers==9 and #s.frames==1)
 s:saveCopyAs(dir..'/'..name..'-reopened.png');s:close()
end
for _,name in ipairs({'gated/a02-expression','b02-expression'}) do
 local s=app.open(dir..'/'..name..'.aseprite');local layer
 for _,l in ipairs(s.layers) do if l.name=='07-hair-tie' then layer=l end end
 assert(layer and layer:cel(1));local image=layer:cel(1).image;local changed=0
 -- Existing palette shade, duplicate only. No other layer is edited.
 local c=data.colors.skinlight;local target=app.pixelColor.rgba(c[1],c[2],c[3],255)
 for y=0,image.height-1 do for x=0,image.width-1 do local v=image:getPixel(x,y)
  if app.pixelColor.rgbaA(v)>0 and v~=target then image:drawPixel(x,y,target);changed=changed+1 end
 end end
 assert(changed>0)
 s:saveAs(dir..'/'..name..'-tie-edit.aseprite');s:saveCopyAs(dir..'/'..name..'-tie-edit.png');s:close()
 s=app.open(dir..'/'..name..'-tie-edit.aseprite');s:saveCopyAs(dir..'/'..name..'-tie-edit-reopened.png');s:close()
 print(name..' isolated tie edit '..changed)
end
