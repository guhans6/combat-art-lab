-- Native layer inspection and local lamp edit, separate from the main scene.
local root=assert(app.params["root"])
local function path(p)return app.fs.joinPath(root,p)end
local s=app.open(path("assets/source/street-drawn-v01/background.aseprite"))
assert(s.width==352 and s.height==264 and #s.layers==16)
local original,positions={},{ }
local inventory={}
for i,l in ipairs(s.layers)do
 local cel=l:cel(1);original[i]=cel.image:clone();positions[i]=cel.position
 local n=0
 for it in cel.image:pixels()do if app.pixelColor.rgbaA(it())>0 then n=n+1 end end
 assert(n>0)
 inventory[#inventory+1]={name=l.name,nonTransparentPixels=n}
 l.isVisible=false
end
for i,l in ipairs(s.layers)do
 l.isVisible=true
 s:saveCopyAs(path("assets/previews/street-drawn-v01/layers/"..l.name:gsub("/","_")..".png"))
 l.isVisible=false
end
for _,l in ipairs(s.layers)do l.isVisible=true end
s:saveCopyAs(path("assets/export/street-drawn-v01/background-reopened.png"))
local lamp=s.layers[15];assert(lamp.name=="bg/15-lamp-light-pixels");local lampName=lamp.name
local im=lamp:cel(1).image:clone();local changed=0
local old=app.pixelColor.rgba(255,229,172,255)
local new=app.pixelColor.rgba(235,197,132,255)
for it in im:pixels()do if it()==old then it(new);changed=changed+1 end end
assert(changed>0);lamp:cel(1).image=im
s:saveAs(path("assets/source/street-drawn-v01/background-lamp-edit-test.aseprite"))
s:saveCopyAs(path("assets/export/street-drawn-v01/background-lamp-edit-test.png"));s:close()
local test=app.open(path("assets/source/street-drawn-v01/background-lamp-edit-test.aseprite"))
for i,l in ipairs(test.layers)do
 if i~=15 then
  local cel=l:cel(1);assert(cel.image:isEqual(original[i]))
  assert(cel.position.x==positions[i].x and cel.position.y==positions[i].y)
 end
end
test:close()
local f=assert(io.open(path("docs/experiments/2026-10-26-drawn-background/editability-checks.json"),"w"))
f:write(json.encode{layers=inventory,localEdit={layer=lampName,sourcePixelsChanged=changed,other15LayersUnchangedAfterReopen=true,variantOnly=true}});f:close()
print("PASS: 16 populated environment layers reopened/exported; isolated lamp edit changed "..changed.." pixels; other 15 layer images and positions preserved")
