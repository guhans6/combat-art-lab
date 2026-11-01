local dir=assert(app.params.out);local data=dofile(dir..'/data.lua')
local function palette(colors)
 local p=Palette(#colors+1);p:setColor(0,app.pixelColor.rgba(0,0,0,0))
 for i,c in ipairs(colors) do p:setColor(i,app.pixelColor.rgba(c[1],c[2],c[3],255)) end
 return p
end
local function build(w,h,names,prefix,name,colors)
 local s=Sprite(w,h,ColorMode.RGB);s.layers[1].name=names[1]
 for i,n in ipairs(names) do local l=i==1 and s.layers[1] or s:newLayer();l.name=n
  local im=Image{fromFile=dir..'/prepared/'..prefix..n..'.png'};s:newCel(l,1,im,Point(0,0))
 end
 s:setPalette(palette(colors));s:saveAs(dir..'/'..name..'.aseprite');s:saveCopyAs(dir..'/'..name..'.png');s:close()
 s=app.open(dir..'/'..name..'.aseprite');s:saveCopyAs(dir..'/'..name..'-reopened.png');s:close()
end
build(96,216,data.character_layers,'','standing-seed',data.character_palette)
build(362,272,data.background_layers,'bg-','environment-parts',data.background_palette)
-- First building keeps six visible parts, not invented rear walls or hidden surfaces.
local names={'05-near-shop-wall','07-shop-glass','08-shop-awning','09-shop-posts','10-shop-steps','13-shop-lamp-pixels'}
build(362,272,names,'bg-','shop-visible-parts',data.background_palette)
print('Static native sources saved/reopened: 14 character, 13 environment, 6 first-building parts.')
