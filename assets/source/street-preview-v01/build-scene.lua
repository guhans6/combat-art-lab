-- Static placement preview: generated clean plate + untouched v04 native layers.
-- No character pixels are repainted, resampled or regenerated.
local root=assert(app.params["root"])
local function path(p)return app.fs.joinPath(root,p)end
local W,H=352,264
local ox,oy=84,61
local background=Image{fromFile=path("assets/source/street-preview-v01/background-clean-generated.png")}
local bg=Image(W,H,ColorMode.RGB)
-- Explicit nearest-neighbor sampling: no interpolation or softening.
for y=0,H-1 do for x=0,W-1 do
 local sx=math.min(background.width-1,math.floor((x+0.5)*background.width/W))
 local sy=math.min(background.height-1,math.floor((y+0.5)*background.height/H))
 bg:drawPixel(x,y,background:getPixel(sx,sy))
end end
bg:saveAs(path("assets/export/street-preview-v01/background-native.png"))
local character=app.open(path("assets/source/standing-v04/standing.aseprite"))
assert(character.width==128 and character.height==192 and #character.layers==12)
local original={};local positions={};local visibility={}
for i,l in ipairs(character.layers)do
 original[i]=l:cel(1).image:clone();positions[i]=l:cel(1).position;visibility[i]=l.isVisible
end
local scene=Sprite(W,H,ColorMode.RGB)
scene.layers[1].name="00-background-inpainted-flat"
scene.cels[1].image=bg
scene.cels[1].position=Point(0,0)
local shadow=scene:newLayer();shadow.name="01-ground-shadow"
local sh=Image(W,H,ColorMode.RGB)
local function ellipse(cx,cy,rx,ry,color)
 for y=math.floor(cy-ry),math.ceil(cy+ry)do
  for x=math.floor(cx-rx),math.ceil(cx+rx)do
   if x>=0 and x<W and y>=0 and y<H and ((x-cx)/rx)^2+((y-cy)/ry)^2<=1 then sh:drawPixel(x,y,color)end
  end
 end
end
ellipse(158,248,36,3,app.pixelColor.rgba(33,29,47,52))
ellipse(137,246,13,1.5,app.pixelColor.rgba(34,25,35,105))
ellipse(176,247,12,1.5,app.pixelColor.rgba(34,25,35,105))
scene:newCel(shadow,1,sh,Point(0,0))
sh:saveAs(path("assets/export/street-preview-v01/ground-shadow.png"))
for i,l in ipairs(character.layers)do
 local copy=scene:newLayer();copy.name="character/"..l.name;copy.isVisible=visibility[i]
 scene:newCel(copy,1,original[i]:clone(),Point(positions[i].x+ox,positions[i].y+oy))
end
scene.frames[1].duration=character.frames[1].duration
local tag=scene:newTag(1,1);tag.name="static-street-placement"
scene.data="Static preview. Clean background is AI-inpainted raster, not a hand-built environment. Character v04 layers copied exactly at offset (84,61). No gameplay/animation validation."
scene:saveAs(path("assets/source/street-preview-v01/street-scene.aseprite"))
scene:saveCopyAs(path("assets/export/street-preview-v01/street-scene-native.png"))
scene:close();character:close()
local reopened=app.open(path("assets/source/street-preview-v01/street-scene.aseprite"))
assert(reopened.width==W and reopened.height==H and #reopened.layers==14)
for i=1,12 do
 local layer=reopened.layers[i+2];local cel=layer:cel(1)
 assert(cel.image:isEqual(original[i]))
 assert(cel.position.x==positions[i].x+ox and cel.position.y==positions[i].y+oy)
 assert(layer.isVisible==visibility[i])
end
reopened:saveCopyAs(path("assets/export/street-preview-v01/street-scene-reopened.png"))
for i,l in ipairs(reopened.layers)do l.isVisible=(i>=3 and visibility[i-2])or false end
reopened:saveCopyAs(path("assets/export/street-preview-v01/character-placement-only.png"))
reopened:close()
print("PASS: 352x264 static scene saved/reopened with 14 layers; all 12 v04 layers and visibility copied unchanged at (84,61)")
