-- Optional hybrid follow-up, supported by observed B02 mouth regression.
local dir=assert(app.params.out)
local previous=app.open(dir..'/b01-hair-cleanup.aseprite');local mouth
for _,l in ipairs(previous.layers) do if l.name=='09-mouth' then local c=l:cel(1);mouth={image=Image(c.image),position=Point(c.position.x,c.position.y)} end end
assert(mouth);previous:close()
local s=app.open(dir..'/b02-expression.aseprite')
for _,l in ipairs(s.layers) do if l.name=='09-mouth' then local c=l:cel(1);c.image=mouth.image;c.position=mouth.position end end
s:saveAs(dir..'/c01-restored-mouth.aseprite');s:saveCopyAs(dir..'/c01-restored-mouth.png');s:close()
s=app.open(dir..'/c01-restored-mouth.aseprite');s:saveCopyAs(dir..'/c01-restored-mouth-reopened.png');s:close()
if app.params.staticonly=='yes' then return end
-- Earlier blink stays as an explicit pre-rollback checkpoint.
s=app.open(dir..'/blink-probe.aseprite')
for _,l in ipairs(s.layers) do if l.name=='09-mouth' then for i=1,#s.frames do local c=l:cel(i);c.image=mouth.image;c.position=mouth.position end end end
s:saveAs(dir..'/blink-restored-mouth.aseprite')
for i=1,#s.frames do local im=Image(120,112,ColorMode.RGB);im:drawSprite(s,i);im:saveAs(dir..'/blink-final-frame-'..i..'.png') end
s:close();s=app.open(dir..'/blink-restored-mouth.aseprite')
for i=1,#s.frames do local im=Image(120,112,ColorMode.RGB);im:drawSprite(s,i);im:saveAs(dir..'/blink-final-frame-'..i..'-reopened.png') end
s:close();print('Restored only earlier mouth layer; pre-rollback native files and frames preserved.')
