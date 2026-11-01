local dir=assert(app.params.out)
for _,name in ipairs({'study-192-pass02','study-256-pass02'}) do
 local s=app.open(dir..'/'..name..'.aseprite');print(name,s.width,s.height,#s.layers,#s.frames)
 for _,layer in ipairs(s.layers) do print('layer',layer.name,layer.isVisible) end
 s:saveCopyAs(dir..'/'..name..'-reopen.png')
 local layer=s.layers[1];local cel=layer:cel(1);local image=cel.image;image:drawPixel(0,0,app.pixelColor.rgba(255,0,255,255));s:saveAs(dir..'/'..name..'-edit-proof.aseprite');s:saveCopyAs(dir..'/'..name..'-edit-proof.png');s:close()
end
local s=app.open(dir..'/baseline.aseprite');s:saveCopyAs(dir..'/baseline.png');s:close()
