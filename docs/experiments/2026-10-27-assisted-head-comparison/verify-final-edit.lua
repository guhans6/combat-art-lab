local dir=assert(app.params.out);local data=dofile(dir..'/data.lua')
local s=app.open(dir..'/c01-restored-mouth.aseprite');local tie
for _,l in ipairs(s.layers) do if l.name=='07-hair-tie' then tie=l:cel(1).image end end
local c=data.colors.skinlight;local value=app.pixelColor.rgba(c[1],c[2],c[3],255);local n=0
for y=0,tie.height-1 do for x=0,tie.width-1 do if app.pixelColor.rgbaA(tie:getPixel(x,y))>0 then tie:drawPixel(x,y,value);n=n+1 end end end
s:saveAs(dir..'/c01-restored-mouth-tie-edit.aseprite');s:saveCopyAs(dir..'/c01-restored-mouth-tie-edit.png');s:close()
s=app.open(dir..'/c01-restored-mouth-tie-edit.aseprite');s:saveCopyAs(dir..'/c01-restored-mouth-tie-edit-reopened.png');s:close();print('Final C tie edit '..n)
