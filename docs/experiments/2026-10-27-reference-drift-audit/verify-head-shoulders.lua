-- Technical proof on a duplicate only; existing study and failed attempts stay intact.
local dir=assert(app.params.out)
local s=app.open(dir..'/head-shoulders-features.aseprite')
assert(s.width==120 and s.height==112 and #s.layers==10 and #s.frames==1)
print('source',s.width,s.height,#s.layers,#s.frames)
s:saveCopyAs(dir..'/head-shoulders-features-reopen.png')
local selected
for _,layer in ipairs(s.layers) do
 print('layer',layer.name)
 if layer.name=='07-pale-hair-tie' then selected=layer end
end
assert(selected)
local im=selected:cel(1).image
local changes=0
-- Reuse the shirt color for a localized lighter-tie variant; no palette extension.
for y=0,im.height-1 do for x=0,im.width-1 do
 if app.pixelColor.rgbaA(im:getPixel(x,y))>0 then
  im:drawPixel(x,y,app.pixelColor.rgba(222,212,195,255));changes=changes+1
 end
end end
assert(changes>0)
print('tie pixels revised',changes)
s:saveAs(dir..'/head-shoulders-tie-edit-proof.aseprite')
s:saveCopyAs(dir..'/head-shoulders-tie-edit-proof.png')
s:close()
s=app.open(dir..'/head-shoulders-tie-edit-proof.aseprite')
s:saveCopyAs(dir..'/head-shoulders-tie-edit-proof-reopen.png')
s:close()
