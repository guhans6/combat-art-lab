local dir=assert(app.params.out)
local s=app.open(dir..'/standing-seed.aseprite');local cel
for _,l in ipairs(s.layers) do if l.name=='01-denim' then cel=l:cel(1) end end
assert(cel);local image=cel.image;local count=0
-- Only remove warm source-background contamination in the denim's outer samples.
-- Pants are blue; no texture/single-pixel blanket filter is applied.
for y=114,191 do for x=0,image.width-1 do
 local v=image:getPixel(x,y);local a=app.pixelColor.rgbaA(v)
 if a>0 then local r=app.pixelColor.rgbaR(v);local g=app.pixelColor.rgbaG(v);local b=app.pixelColor.rgbaB(v)
  if b<=r+4 or g<=r+1 then image:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0));count=count+1 end
 end
end end
s:saveAs(dir..'/standing-cleaned.aseprite');s:saveCopyAs(dir..'/standing-cleaned.png');s:close()
s=app.open(dir..'/standing-cleaned.aseprite');s:saveCopyAs(dir..'/standing-cleaned-reopened.png');s:close()
-- Export each actual native background cel for independent Godot nodes.
s=app.open(dir..'/environment-parts.aseprite')
for _,l in ipairs(s.layers) do local im=Image(362,272,ColorMode.RGB);local c=l:cel(1);im:drawImage(c.image,c.position);im:saveAs(dir..'/environment-'..l.name..'.png') end
s:close();print('Removed '..count..' warm contaminated denim-edge samples; native background parts exported.')
