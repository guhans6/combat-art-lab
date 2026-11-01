local dir=assert(app.params.out)
local s=app.open(dir..'/standing-seed.aseprite');local cel
for _,l in ipairs(s.layers) do if l.name=='01-denim' then cel=l:cel(1) end end
assert(cel);local image=cel.image;local count=0
-- Explicit source-coordinate removal mask; color is not sufficient evidence of background.
-- Keep the source/seed and review alpha coverage on every exported body frame.
local removals=dofile(dir..'/denim-edge-removals.lua')
for _,p in ipairs(removals) do
 local x,y=p[1],p[2]
 assert(x>=0 and x<image.width and y>=114 and y<=191, 'Removal outside reviewed denim edge scope')
 assert(app.pixelColor.rgbaA(image:getPixel(x,y))>0, 'Removal mask does not match seed')
 image:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0));count=count+1
end
s:saveAs(dir..'/standing-cleaned.aseprite');s:saveCopyAs(dir..'/standing-cleaned.png');s:close()
s=app.open(dir..'/standing-cleaned.aseprite');s:saveCopyAs(dir..'/standing-cleaned-reopened.png');s:close()
-- Export each actual native background cel for independent Godot nodes.
s=app.open(dir..'/environment-parts.aseprite')
for _,l in ipairs(s.layers) do local im=Image(362,272,ColorMode.RGB);local c=l:cel(1);im:drawImage(c.image,c.position);im:saveAs(dir..'/environment-'..l.name..'.png') end
s:close();print('Removed '..count..' warm contaminated denim-edge samples; native background parts exported.')
