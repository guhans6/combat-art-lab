local dir=assert(app.params.out);local data=dofile(dir..'/data.lua')
local s=app.open(dir..'/shop-visible-parts.aseprite');local target
for _,l in ipairs(s.layers) do if l.name=='13-shop-lamp-pixels' then target=l end end
local desired={244,174,70};local best,dist
for _,c in ipairs(data.background_palette) do local d=0;for i=1,3 do d=d+(c[i]-desired[i])^2 end;if not dist or d<dist then best=c;dist=d end end
local value=app.pixelColor.rgba(best[1],best[2],best[3],255);local im=target:cel(1).image;local count=0
for y=0,im.height-1 do for x=0,im.width-1 do local v=im:getPixel(x,y)
 if app.pixelColor.rgbaA(v)>0 and app.pixelColor.rgbaR(v)>200 and app.pixelColor.rgbaG(v)>160 and v~=value then im:drawPixel(x,y,value);count=count+1 end
end end
assert(count>0);s:saveAs(dir..'/shop-lamp-edit.aseprite');s:saveCopyAs(dir..'/shop-lamp-edit.png');s:close()
s=app.open(dir..'/shop-lamp-edit.aseprite');s:saveCopyAs(dir..'/shop-lamp-edit-reopened.png');s:close();print('Isolated shop lamp-color proof pixels '..count)
