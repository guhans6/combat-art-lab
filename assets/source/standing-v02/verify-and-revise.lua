-- Reopen the native master, export its real layers, then perform a local edit.
local root=assert(app.params["root"])
local function path(rel) return app.fs.joinPath(root,rel) end
local s=app.open(path("assets/source/standing-v02/standing.aseprite"))
assert(s and s.width==128 and s.height==192)
assert(#s.layers==12 and #s.frames==1)
assert(s.tags[1].name=="standing-study")
assert(not s.layers[12].isVisible)
local original,visible={},{}
local metadata={width=s.width,height=s.height,frames=#s.frames,layers={},groundY=186}
for i,l in ipairs(s.layers) do
 original[i]=l:cel(1).image:clone();visible[i]=l.isVisible
 local count=0
 for it in l:cel(1).image:pixels() do
  local a=app.pixelColor.rgbaA(it());assert(a==0 or a==255)
  if a==255 then count=count+1 end
 end
 metadata.layers[#metadata.layers+1]={name=l.name,visible=l.isVisible,pixelCount=count}
end
for _,l in ipairs(s.layers) do l.isVisible=false end
for i,l in ipairs(s.layers) do
 l.isVisible=true
 s:saveCopyAs(path("assets/previews/standing-v02/layers/"..l.name..".png"))
 l.isVisible=false
end
for i,l in ipairs(s.layers) do l.isVisible=visible[i] end
s:saveCopyAs(path("assets/export/standing-v02/standing-reopened.png"))
local target=s.layers[2];assert(target.name=="02-tote-body")
local img=target:cel(1).image:clone()
local base=app.pixelColor.rgba(240,204,176,255)
local light=app.pixelColor.rgba(249,217,186,255)
local revisedBase=app.pixelColor.rgba(185,200,188,255)
local revisedLight=app.pixelColor.rgba(212,223,208,255)
local changed=0
for it in img:pixels() do
 if it()==base then it(revisedBase);changed=changed+1
 elseif it()==light then it(revisedLight);changed=changed+1 end
end
assert(changed>0)
target:cel(1).image=img
for i,l in ipairs(s.layers) do
 if i~=2 then assert(l:cel(1).image:isEqual(original[i])) end
end
s:saveAs(path("assets/source/standing-v02/standing-tote-revision-test.aseprite"))
s:saveCopyAs(path("assets/export/standing-v02/standing-tote-revision-test.png"))
metadata.revision={layer=target.name,changedSourcePixels=changed,otherLayerImagesUnchanged=true,scope="test variant only; cream tote retained in main master"}
local f=assert(io.open(path("docs/experiments/2026-10-26-standing-refinement/source-checks.json"),"w"))
f:write(json.encode(metadata));f:close()
s:close()
local revised=app.open(path("assets/source/standing-v02/standing-tote-revision-test.aseprite"))
assert(#revised.layers==12)
for i,l in ipairs(revised.layers) do
 if i~=2 then assert(l:cel(1).image:isEqual(original[i])) end
end
revised:close()
print("PASS: native master reopened; 12 layers/1 frame; binary alpha; layer exports saved")
print("PASS: local tote revision changed "..changed.." source pixels; all 11 other layer images unchanged after save/reopen")
