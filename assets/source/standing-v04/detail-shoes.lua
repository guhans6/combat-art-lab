-- v04: small sneaker-detail edit of v03. Existing opaque shoe pixels only.
local root=assert(app.params["root"])
local function path(p)return app.fs.joinPath(root,p)end
local s=app.open(path("assets/source/standing-v03/standing.aseprite"))
assert(s.width==128 and s.height==192 and #s.layers==12)
local original={}
for i,l in ipairs(s.layers)do original[i]=l:cel(1).image:clone()end
local l=s.layers[4];assert(l.name=="04-sneakers")
local cel=l:cel(1);local image=Image(128,192,ColorMode.RGB)
image:drawImage(cel.image,cel.position)
local before=image:clone()
local hex={ink="41322f",dark="795c52",shadow="a37e6d",base="c9a591",light="e5c7ac",cream="f3dcc2",sole="aa8776"}
local C={}
for k,h in pairs(hex)do C[k]=app.pixelColor.rgba(tonumber(h:sub(1,2),16),tonumber(h:sub(3,4),16),tonumber(h:sub(5,6),16),255)end
local function px(c,x,y)
 assert(y>=172 and y<=184 and ((x>=42 and x<=66)or(x>=80 and x<=103)))
 if app.pixelColor.rgbaA(before:getPixel(x,y))==255 then image:drawPixel(x,y,C[c])end
end
local function line(c,points)
 for i=1,#points-1 do
  local x,y=points[i][1],points[i][2];local tx,ty=points[i+1][1],points[i+1][2]
  local dx,dy=math.abs(tx-x),-math.abs(ty-y);local sx,sy=x<tx and 1 or -1,y<ty and 1 or -1;local err=dx+dy
  while true do
   px(c,x,y);if x==tx and y==ty then break end
   local e=err*2;if e>=dy then err=err+dy;x=x+sx end
   if e<=dx then err=err+dx;y=y+sy end
  end
 end
end
-- Screen-left shoe: tongue edge, lace eyelets, toe/quarter seams and midsole.
line("shadow",{{51,173},{53,175},{54,177}})
line("cream",{{50,173},{52,174}})
line("cream",{{49,175},{52,176}})
line("cream",{{48,177},{50,178}})
px("dark",49,174);px("dark",53,175);px("dark",47,176);px("dark",52,177)
line("shadow",{{45,177},{47,177},{49,178},{50,180}})
line("light",{{44,179},{47,178},{48,179}})
line("dark",{{55,177},{56,178},{58,178}})
line("light",{{57,176},{59,177},{60,177}})
line("shadow",{{60,178},{62,178},{63,179}})
line("light",{{44,182},{47,183},{50,183}})
line("sole",{{50,182},{53,181},{55,181}})
line("shadow",{{59,181},{62,181},{64,180}})
-- Screen-right shoe: small matching details follow its different perspective.
line("shadow",{{89,174},{91,176},{92,178}})
line("cream",{{89,174},{91,175}})
line("cream",{{87,176},{90,177}})
line("cream",{{86,178},{89,179}})
px("dark",88,175);px("dark",92,176);px("dark",86,177);px("dark",91,178)
line("shadow",{{83,179},{85,178},{87,179},{88,181}})
line("light",{{82,181},{85,180},{86,181}})
line("dark",{{93,178},{94,180},{96,181}})
line("light",{{95,178},{97,179},{98,179}})
line("shadow",{{98,180},{100,181},{100,182}})
line("sole",{{82,183},{85,184},{87,183}})
line("light",{{90,183},{92,184},{96,184},{98,183}})
line("dark",{{100,183},{101,183}})

cel.image=image;cel.position=Point(0,0)
for i,layer in ipairs(s.layers)do if i~=4 then assert(layer:cel(1).image:isEqual(original[i]))end end
local changes=0
for y=0,191 do for x=0,127 do
 local a,b=before:getPixel(x,y),image:getPixel(x,y)
 assert(app.pixelColor.rgbaA(a)==app.pixelColor.rgbaA(b))
 if a~=b then changes=changes+1;assert(y>=172 and y<=184)end
end end
assert(changes>0)
s:saveAs(path("assets/source/standing-v04/standing.aseprite"))
s:saveCopyAs(path("assets/export/standing-v04/standing.png"));s:close()
local reopened=app.open(path("assets/source/standing-v04/standing.aseprite"))
assert(#reopened.layers==12 and #reopened.frames==1)
for i,layer in ipairs(reopened.layers)do if i~=4 then assert(layer:cel(1).image:isEqual(original[i]))end end
reopened:saveCopyAs(path("assets/export/standing-v04/standing-reopened.png"));reopened:close()
print("PASS: "..changes.." existing opaque shoe pixels refined; alpha silhouette and all 11 other layers preserved after native save/reopen")
