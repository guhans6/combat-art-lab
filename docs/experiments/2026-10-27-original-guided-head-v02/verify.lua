local dir=assert(app.params.out)
local palette_hex=dofile(dir..'/palette.lua')
local function pin(s)
 local p=Palette(#palette_hex+1);p:setColor(0,app.pixelColor.rgba(0,0,0,0))
 for i,h in ipairs(palette_hex) do p:setColor(i,app.pixelColor.rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255)) end
 s:setPalette(p)
end
for _,name in ipairs({'baseline','pass-01-hair','pass-02-face','pass-03-refined'}) do
 local s=app.open(dir..'/'..name..'.aseprite')
 assert(s.width==120 and s.height==112 and #s.layers==10 and #s.frames==1)
 print(name,s.width,s.height,#s.layers,#s.frames)
 s:saveCopyAs(dir..'/'..name..'-reopened.png');s:close()
end
local s=app.open(dir..'/pass-03-refined.aseprite')
local target
for _,l in ipairs(s.layers) do if l.name=='07-pale-hair-tie' then target=l end end
assert(target)
local im=target:cel(1).image;local changed=0
for y=0,im.height-1 do for x=0,im.width-1 do
 if app.pixelColor.rgbaA(im:getPixel(x,y))>0 then
  im:drawPixel(x,y,app.pixelColor.rgba(222,208,178,255));changed=changed+1
 end
end end
assert(changed>0)
s:saveCopyAs(dir..'/tie-edit-proof.png');pin(s);s:saveAs(dir..'/tie-edit-proof.aseprite');s:close()
s=app.open(dir..'/tie-edit-proof.aseprite');s:saveCopyAs(dir..'/tie-edit-proof-reopened.png');s:close()
print('tie edit scoped pixels',changed)
