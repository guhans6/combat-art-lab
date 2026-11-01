-- Drawn environment: authored pixel geometry and structured plant branches.
-- No reference, generated background, raster patch, or external asset is loaded.
-- The only image-bearing input is the preserved v04 native character.
local root=assert(app.params["root"])
local function path(p)return app.fs.joinPath(root,p)end
local W,H=352,264
local s=Sprite(W,H,ColorMode.RGB);s:deleteLayer(s.layers[1])
local hex={
 sky="454d86",skyTop="39477c",skyMid="625b91",skyLow="8b668e",skyHorizon="bd7e89",
 cloudDark="7d5b86",cloud="b77187",cloudLight="d98b91",cloudLow="c9838d",
 far="49527f",farSide="3c4978",farLight="596289",farWindow="bf958f",
 blueInk="283752",blueDark="304264",blue="3b5075",blueLight="4b6286",blueEdge="5a7293",
 bridge="344361",bridgeLight="536183",bridgeShadow="29364e",
 road="41465f",roadDark="353c56",roadLight="50536a",roadWarm="655265",mark="9a8c9a",
 paving="89715f",pavingShade="706678",pavingDark="695666",pavingWarm="a88060",pavingLight="c49868",pavingEdge="d6a86f",
 curb="80675c",curbShade="65565f",curbLight="b28a64",curbTop="d2a36b",
 wallShade="4a5064",wall="626171",wallLight="78716e",wallGold="a87d4f",wallAmber="c29155",wallSun="d6a55e",wallLine="926e4a",
 woodInk="392e2f",woodShadow="4a3530",wood="634633",woodLight="87613e",woodGold="a27b4e",
 glassShade="a46b37",glass="c4883f",glassLight="e0a34d",glassSun="efb65a",glassCream="f2c36d",
 greenInk="273d39",greenShade="34483e",green="46583f",greenMid="596646",greenLight="70754a",greenGold="8e8a50",greenSun="ada35c",
 coolGreen="344b4c",coolLeaf="435b52",coolTip="587163",stem="596041",stemLight="8e8750",
 potDark="5c4643",pot="81614f",potLight="a78062",potRim="b38e69",potPale="b5a195",potPaleShade="8c8188",
 railDark="485367",rail="6d7381",railLight="989795",railWarm="b49a79",
 poleShade="4d5063",pole="747078",poleWarm="ab8b6d",metal="36383e",
 lampRim="bb9759",lamp="ffd486",lampCore="ffe5ac",lampWarm="edb867",
 chalk="b3a49b",sign="3b4346",signEdge="87674c",
}
local C={}
for k,v in pairs(hex)do C[k]=app.pixelColor.rgba(tonumber(v:sub(1,2),16),tonumber(v:sub(3,4),16),tonumber(v:sub(5,6),16),255)end
local im,layer;local envNames={}
local function px(x,y,c)
 x=math.floor(x);y=math.floor(y)
 if x>=0 and x<W and y>=0 and y<H then im:drawPixel(x,y,type(c)=="string" and C[c] or c)end
end
local function line(c,points)
 for i=1,#points-1 do
  local x,y=math.floor(points[i][1]+0.5),math.floor(points[i][2]+0.5)
  local tx,ty=math.floor(points[i+1][1]+0.5),math.floor(points[i+1][2]+0.5)
  local dx,dy=math.abs(tx-x),-math.abs(ty-y);local sx,sy=x<tx and 1 or -1,y<ty and 1 or -1;local e=dx+dy
  while true do
   px(x,y,c);if x==tx and y==ty then break end
   local e2=e*2;if e2>=dy then e=e+dy;x=x+sx end;if e2<=dx then e=e+dx;y=y+sy end
  end
 end
end
local function poly(c,points,edge)
 local ymin,ymax=H,0
 for _,p in ipairs(points)do ymin=math.min(ymin,p[2]);ymax=math.max(ymax,p[2])end
 for y=math.max(0,math.floor(ymin)),math.min(H-1,math.ceil(ymax))do
  local hits={};local scan=y+0.5
  for i,a in ipairs(points)do local b=points[i%#points+1]
   if(a[2]<=scan and b[2]>scan)or(b[2]<=scan and a[2]>scan)then hits[#hits+1]=a[1]+(scan-a[2])*(b[1]-a[1])/(b[2]-a[2])end
  end
  table.sort(hits)
  for i=1,#hits-1,2 do for x=math.ceil(hits[i]-0.5),math.floor(hits[i+1]-0.5)do px(x,y,c)end end
 end
 if edge then local p={};for _,a in ipairs(points)do p[#p+1]=a end;p[#p+1]=points[1];line(edge,p)end
end
local function rect(c,x,y,w,h)poly(c,{{x,y},{x+w,y},{x+w,y+h},{x,y+h}})end
local function ellipse(c,cx,cy,rx,ry)
 for y=math.floor(cy-ry),math.ceil(cy+ry)do for x=math.floor(cx-rx),math.ceil(cx+rx)do
  if((x-cx)/rx)^2+((y-cy)/ry)^2<=1 then px(x,y,c)end
 end end
end
local function newLayer(name)
 if layer then s:newCel(layer,1,im,Point(0,0))end
 layer=s:newLayer();layer.name=name;im=Image(W,H,ColorMode.RGB);envNames[#envNames+1]=name
end
-- Clusters follow explicit branch trajectories, not a per-pixel noise field.
local function leaf(c,x,y,dx,dy,size)
 local mag=math.sqrt(dx*dx+dy*dy);dx=dx/mag;dy=dy/mag
 local nx,ny=-dy,dx
 poly(c,{{x,y},{x+dx*size*.3+nx*size*.3,y+dy*size*.3+ny*size*.3},{x+dx*size,y+dy*size},{x+dx*size*.55-nx*size*.23,y+dy*size*.55-ny*size*.23}})
end
local function fern(points,n,size,warm)
 line(warm and"stemLight"or"stem",points)
 local a,b=points[1],points[#points];local dx,dy=b[1]-a[1],b[2]-a[2];local mag=math.sqrt(dx*dx+dy*dy);dx=dx/mag;dy=dy/mag
 local nx,ny=-dy,dx
 for i=1,n do
  local t=i/(n+1);local x=a[1]+(b[1]-a[1])*t;local y=a[2]+(b[2]-a[2])*t
  local len=size*(1-.56*t)
  leaf(warm and"greenLight"or"green",x,y,dx*.35+nx,dy*.35+ny,len)
  leaf(warm and"greenGold"or"greenMid",x,y,dx*.35-nx,dy*.35-ny,len*.92)
 end
 leaf(warm and"greenSun"or"coolTip",b[1]-dx*3,b[2]-dy*3,dx,dy,size*.45)
end
local function cluster(x,y,r,base,lit)
 poly(base,{{x-r,y},{x-r+1,y-2},{x-r*.4,y-r*.65},{x+1,y-r*.6},{x+r*.65,y-r*.3},{x+r,y+1},{x+r*.45,y+r*.55},{x-1,y+r*.6},{x-r*.7,y+r*.25}})
 poly(lit,{{x-r*.7,y-1},{x-r*.35,y-r*.5},{x+1,y-r*.45},{x+r*.5,y-r*.15},{x+1,y},{x-r*.4,y+1}})
end

newLayer("bg/01-sky-planes")
rect("sky",0,0,W,H)
poly("skyTop",{{0,0},{352,0},{352,41},{319,45},{290,49},{251,48},{220,53},{0,50}})
poly("skyMid",{{0,91},{217,89},{255,82},{287,89},{319,82},{352,85},{352,153},{0,160}})
poly("skyLow",{{0,135},{229,132},{256,125},{275,130},{311,121},{352,126},{352,190},{0,192}})
poly("skyHorizon",{{0,176},{239,172},{270,162},{293,165},{320,157},{352,160},{352,204},{0,204}})

newLayer("bg/02-cloud-clusters")
poly("cloudDark",{{232,59},{241,59},{241,57},{249,57},{252,54},{260,55},{266,51},{270,51},{268,55},{261,58},{255,59},{251,62},{243,63},{240,62},{232,63}})
poly("cloud",{{259,77},{268,73},{273,73},{278,69},{283,70},{291,66},{296,67},{301,64},{305,65},{304,68},{298,70},{294,70},{290,74},{281,76},{278,78},{270,78},{265,81},{257,81}})
poly("cloud",{{302,60},{309,55},{315,55},{318,51},{325,50},{329,46},{332,46},{331,49},{326,53},{320,55},{317,59},{310,61},{307,64},{301,65}})
poly("cloudLight",{{318,76},{324,71},{329,70},{332,67},{338,66},{340,63},{346,61},{349,58},{352,58},{352,63},{348,66},{344,67},{341,70},{335,73},{331,73},{327,77},{322,79},{317,80}})
poly("cloudDark",{{275,91},{279,87},{285,85},{292,85},{297,80},{300,80},{298,84},{293,88},{288,89},{283,91}})
poly("cloud",{{235,106},{241,103},{244,103},{247,100},{255,99},{258,96},{265,96},{269,92},{272,93},{269,97},{263,100},{259,100},{254,103},{248,104},{244,108},{238,109}})
poly("cloudLight",{{278,112},{286,107},{293,107},{298,103},{304,103},{307,100},{313,100},{319,96},{325,95},{330,91},{336,90},{342,86},{347,84},{352,84},{352,89},{347,91},{340,94},{337,97},{332,97},{326,101},{320,102},{316,106},{309,107},{303,110},{297,110},{292,114},{285,115}})
poly("cloud",{{239,145},{246,141},{250,142},{256,138},{261,138},{267,134},{275,133},{280,130},{284,131},{281,135},{273,138},{269,138},{263,142},{256,144},{250,143},{246,146}})
poly("cloudLow",{{289,155},{295,151},{303,150},{309,147},{314,147},{318,144},{326,143},{333,139},{337,140},{334,144},{327,147},{321,147},{316,151},{308,153},{302,154},{297,157}})

newLayer("bg/03-distant-skyline")
local buildings={{231,111,11,64},{245,119,9,58},{258,127,10,54},{272,106,14,79},{289,121,12,65},{306,88,18,100},{327,116,9,75},{341,109,11,82}}
for i,b in ipairs(buildings)do
 rect(i%2==0 and"farSide"or"far",b[1],b[2],b[3],b[4]);rect("farLight",b[1],b[2],b[3]-2,1)
 for row=1,math.floor(b[4]/7)-1 do for col=1,math.max(1,math.floor(b[3]/5)-1)do
  if(row*3+col+i)%4~=0 then rect("farWindow",b[1]+col*4-1,b[2]+row*7,1,2)end
 end end
end
rect("farSide",311,85,3,5);rect("far",276,102,2,5)

newLayer("bg/04-street-buildings")
poly("blueDark",{{216,28},{237,38},{238,173},{257,177},{257,203},{216,211}},"blueInk")
poly("blue",{{221,54},{244,54},{244,171},{233,186},{220,187}})
rect("blueLight",220,52,25,3);rect("blueInk",224,56,20,2)
rect("blueDark",224,60,12,18);rect("lampWarm",226,63,7,12)
rect("blueInk",229,63,1,12);rect("blueInk",226,69,7,1)
rect("blueLight",222,82,23,3);rect("blueDark",225,89,19,2)
rect("blueDark",227,101,17,4);rect("blueLight",227,107,17,1)
poly("blue",{{238,123},{253,129},{253,196},{243,201},{237,179}})
poly("blueDark",{{250,143},{265,148},{265,203},{252,202}})
rect("lampWarm",246,146,3,7);rect("blueLight",242,144,1,12)
poly("blueDark",{{337,68},{352,58},{352,209},{327,205},{325,168},{333,127}},"blueInk")
poly("blue",{{342,74},{352,67},{352,204},{337,201},{336,162}})
line("blueLight",{{341,73},{339,126},{335,168},{334,202}})
poly("blueInk",{{348,110},{352,107},{352,125},{346,128}})
poly("lampWarm",{{348,113},{351,112},{351,123},{347,125}})
poly("blueInk",{{343,159},{348,156},{348,169},{341,172}})
poly("lampWarm",{{343,161},{346,160},{346,167},{342,169}})
poly("blue",{{322,151},{333,146},{330,202},{317,201}},"blueInk")
line("blueEdge",{{322,152},{319,199}})
rect("lampWarm",323,164,2,6);rect("farWindow",320,182,2,4)
poly("blueLight",{{268,171},{283,174},{286,202},{266,203}})
rect("blueDark",270,175,4,24);rect("lampWarm",278,179,2,6)

newLayer("bg/05-bridge-and-distant-street")
poly("bridgeShadow",{{229,134},{352,130},{352,145},{229,146}})
poly("bridge",{{229,129},{352,126},{352,133},{229,136}})
line("bridgeLight",{{229,130},{352,127}})
line("bridgeLight",{{229,135},{352,132}})
for x=234,351,9 do line("farLight",{{x,130},{x,133}})end
poly("bridgeLight",{{240,136},{246,136},{252,143},{255,163},{251,163},{247,144}})
poly("bridge",{{323,134},{328,134},{325,162},{321,163}})
rect("farSide",287,148,9,34);rect("farLight",289,150,5,1)
rect("farWindow",289,155,1,2);rect("farWindow",293,160,1,2)
poly("roadLight",{{284,185},{314,185},{337,204},{272,204}})
rect("farWindow",297,187,1,2);rect("bridgeLight",285,197,35,1)

newLayer("bg/06-pavement-and-road")
poly("road",{{0,214},{280,193},{352,193},{352,264},{0,264}})
poly("roadDark",{{316,199},{352,198},{352,264},{249,264},{277,239},{300,218}})
poly("roadLight",{{306,203},{340,204},{352,207},{352,214},{296,212}})
poly("roadWarm",{{289,217},{335,217},{352,221},{352,225},{282,223}})
poly("paving",{{0,226},{191,207},{303,194},{312,199},{219,264},{0,264}})
poly("pavingWarm",{{0,227},{165,213},{236,203},{260,204},{180,232},{0,252}})
poly("pavingShade",{{159,239},{255,217},{303,199},{312,199},{219,264},{0,264},{0,257}})
poly("pavingLight",{{0,239},{72,232},{161,219},{193,217},{149,230},{44,247},{0,249}})
poly("pavingDark",{{0,254},{41,249},{80,248},{106,243},{130,243},{106,250},{45,260},{0,262}})
poly("pavingWarm",{{153,251},{180,241},{207,234},{225,232},{214,240},{181,250},{168,256}})
line("pavingDark",{{0,249},{98,236},{196,221},{272,204}})
line("pavingDark",{{42,264},{153,238},{237,216},{291,200}})
line("pavingShade",{{4,240},{71,244},{127,248},{165,250}})
line("pavingDark",{{112,225},{148,230},{191,234},{224,235}})
line("pavingShade",{{198,213},{222,216},{254,219},{280,220}})
line("pavingDark",{{253,201},{270,204},{293,205}})
poly("mark",{{306,202},{309,202},{235,264},{227,264}})
poly("roadLight",{{305,202},{307,202},{233,264},{230,264}})

newLayer("bg/07-sidewall-and-shop-shell")
poly("wallShade",{{113,0},{213,0},{214,210},{141,204},{120,194}})
poly("wall",{{128,0},{186,0},{201,50},{198,206},{143,200},{139,43}})
poly("wallLight",{{143,9},{159,12},{160,199},{143,198}})
poly("blueDark",{{174,0},{208,0},{212,202},{195,205},{193,34}})
line("wallShade",{{146,46},{191,74}});line("wallShade",{{145,93},{192,109}})
line("wallShade",{{144,144},{194,149}})
poly("woodShadow",{{0,0},{79,0},{121,30},{121,199},{0,227}})
poly("wallGold",{{114,35},{140,47},{140,195},{114,194}})
poly("wallAmber",{{116,37},{130,43},{130,192},{116,193}})
poly("wallSun",{{116,42},{123,45},{123,191},{116,192}})
line("wallLine",{{115,68},{139,74}});line("wallLine",{{115,105},{139,109}})
line("wallLine",{{115,146},{139,149}})
rect("wallLine",127,47,1,22);rect("wallLine",132,110,1,37)

newLayer("bg/08-shop-window-interior")
poly("glassShade",{{0,14},{109,52},{109,195},{0,214}})
poly("glassSun",{{0,19},{26,28},{26,202},{0,208}})
poly("glassLight",{{33,31},{76,47},{76,198},{33,205}})
poly("glass",{{84,49},{106,57},{106,193},{84,198}})
poly("glassSun",{{37,39},{57,47},{57,195},{37,198}})
poly("glassCream",{{36,46},{44,49},{44,128},{36,130}})
poly("glassSun",{{87,59},{97,62},{97,190},{87,192}})
poly("glassShade",{{0,88},{25,91},{25,95},{0,92}})
poly("woodLight",{{0,122},{26,121},{26,125},{0,126}})
poly("woodLight",{{33,136},{76,132},{76,136},{33,141}})
poly("woodGold",{{33,133},{75,130},{75,132},{33,137}})
poly("woodLight",{{84,159},{106,154},{106,157},{84,162}})
-- Interior potted silhouettes are broad, quiet shapes behind the glazing.
for _,p in ipairs({{8,118,4},{19,120,3},{42,132,4},{62,130,5},{91,154,3}})do
 local x,y,r=p[1],p[2],p[3];poly("potDark",{{x-r,y},{x+r,y},{x+r-1,y+6},{x-r+1,y+6}})
 line("greenShade",{{x,y},{x-1,y-10}})
 leaf("greenMid",x,y-3,-1,-1,r+2);leaf("green",x,y-6,1,-1,r+1)
 leaf("greenLight",x-1,y-8,-.3,-1,r)
end
poly("glassLight",{{65,81},{69,82},{69,124},{65,125}})
line("glassCream",{{37,60},{37,111}});line("glassLight",{{89,70},{89,126}})

newLayer("bg/09-shop-frame-and-steps")
poly("woodInk",{{25,22},{32,25},{32,204},{26,207}})
poly("wood",{{26,22},{30,23},{30,202},{27,204}})
line("woodLight",{{27,25},{27,201}})
poly("woodInk",{{77,41},{83,44},{83,199},{78,201}})
poly("wood",{{78,42},{81,43},{81,197},{79,199}})
line("woodLight",{{79,44},{79,196}})
poly("woodInk",{{107,50},{114,52},{114,197},{108,198}})
poly("wood",{{108,52},{112,53},{112,194},{109,196}})
line("woodGold",{{109,56},{109,191}})
poly("woodInk",{{0,12},{109,49},{109,54},{0,18}})
line("woodLight",{{0,17},{108,54}})
poly("wood",{{0,205},{108,190},{115,194},{115,201},{0,218}})
line("woodGold",{{0,206},{108,192}})
poly("curbShade",{{92,194},{139,193},{141,204},{92,211}})
poly("curbLight",{{92,193},{139,191},{141,194},{93,199}})
poly("curbShade",{{88,205},{142,201},{147,209},{89,217}})
poly("curbLight",{{88,203},{142,199},{144,203},{89,211}})
line("curbTop",{{88,204},{141,200}})
-- Curved street curb is stepped cleanly in the native grid.
poly("curbShade",{{0,228},{193,204},{300,193},{299,199},{192,213},{0,240}})
poly("curb",{{0,230},{192,207},{299,195},{298,198},{192,211},{0,236}})
line("curbTop",{{0,228},{193,204},{300,193}})
line("curbLight",{{0,230},{192,206},{300,194}})
for _,p in ipairs({{31,224,31,232},{79,218,79,226},{126,212,126,220},{166,207,166,216},{202,203,202,211},{235,199,235,205},{267,196,267,201}})do line("curbShade",{{p[1],p[2]},{p[3],p[4]}})end

newLayer("bg/10-roof-and-overhang")
poly("woodShadow",{{0,0},{78,0},{119,24},{119,39},{0,5}})
poly("wood",{{0,0},{65,0},{117,26},{117,32},{0,3}})
poly("woodLight",{{0,1},{57,1},{112,26},{114,29},{59,6},{0,4}})
poly("blueInk",{{78,0},{114,0},{141,16},{140,25},{119,27}})
poly("blueDark",{{83,0},{108,0},{138,18},{138,22},{119,24}})
line("woodInk",{{0,7},{119,38}})
poly("woodShadow",{{0,26},{7,28},{7,197},{0,199}})
line("woodLight",{{7,31},{7,195}})

newLayer("bg/11-wall-vines-and-canopy")
poly("greenInk",{{143,0},{174,0},{176,7},{185,5},{193,0},{207,0},{209,15},{203,25},{205,37},{198,49},{202,62},{198,75},{203,83},{199,94},{204,105},{200,119},{205,130},{199,145},{202,158},{198,172},{203,187},{197,205},{181,211},{166,205},{147,208},{136,196},{133,179},{137,166},{133,151},{137,137},{135,122},{139,109},{135,95},{140,82},{137,68},{144,57},{141,43},{146,31},{140,16}})
line("stem",{{146,201},{149,175},{148,144},{155,118},{159,85},{164,56},{159,30},{164,3}})
line("coolGreen",{{178,205},{183,174},{179,150},{187,124},{185,95},{191,73},{188,45},{199,15}})
local vines={
 {146,10,7},{153,21,7},{149,33,6},{158,43,8},{146,53,7},{152,68,8},{145,81,6},{150,94,8},{142,108,6},{151,119,9},{143,134,7},{147,147,8},{142,162,7},{150,176,9},{144,190,7},{156,200,7},
 {167,8,8},{175,18,7},{165,31,8},{178,39,9},{168,53,8},{180,64,9},{170,76,7},{180,89,9},{169,104,8},{179,117,8},{166,130,9},{178,145,8},{167,158,9},{179,171,9},{167,187,8},{179,202,8},
 {193,7,8},{201,18,6},{190,31,8},{198,45,7},{191,58,8},{198,73,6},{191,86,7},{198,100,7},{192,113,8},{198,127,6},{191,140,8},{198,154,6},{190,167,8},{198,181,7},{189,195,8},
 }
for i,p in ipairs(vines)do
 local warm=p[1]<162
 cluster(p[1],p[2],p[3],warm and"greenShade"or"coolGreen",warm and"greenMid"or"coolLeaf")
 if i%3==1 then leaf(warm and"greenLight"or"coolTip",p[1]-2,p[2]-2,1,-1,4)end
end
-- Descending vine tips give the canopy an irregular, connected silhouette.
for _,p in ipairs({{142,8,132,21},{153,2,148,17},{186,13,175,29},{201,25,193,40},{144,77,134,91},{143,115,133,126},{195,174,187,190}})do fern({{p[1],p[2]},{p[3],p[4]}},4,4,false)end

newLayer("bg/12-potted-plants")
-- Three foreground pots, with plane-based shading matching the sprite.
poly("potPaleShade",{{23,203},{49,203},{46,222},{28,223}},"potDark")
poly("potPale",{{25,204},{46,204},{43,220},{29,221}})
rect("potPale",22,201,28,4);rect("potPaleShade",22,205,28,1)
poly("potDark",{{49,180},{83,180},{80,217},{56,219}},"woodShadow")
poly("pot",{{51,182},{77,182},{74,215},{57,216}})
poly("potLight",{{51,184},{58,184},{61,215},{56,216}})
rect("potRim",48,177,36,5);rect("pot",49,182,34,2)
poly("potDark",{{111,175},{135,175},{133,194},{115,195}},"woodShadow")
poly("pot",{{112,176},{130,176},{129,192},{116,193}})
rect("potRim",109,173,28,4)
-- Ferns attach to explicit roots and radiate across the reference's window shapes.
local fronds={
 {35,202,14,167,8,8},{35,202,24,163,8,8},{35,202,34,164,8,8},{35,202,47,166,8,8},{35,202,57,177,7,7},{35,202,13,184,6,7},{35,202,50,189,6,7},
 {66,179,18,128,10,10},{66,179,29,121,11,10},{66,179,43,120,10,11},{66,179,62,119,11,10},{66,179,79,125,10,10},{66,179,95,130,10,9},{66,179,104,145,9,9},{66,179,28,150,8,10},{66,179,20,162,8,9},{66,179,99,160,8,9},{66,179,91,174,6,8},
 {123,174,99,140,8,7},{123,174,113,135,8,7},{123,174,129,131,9,7},{123,174,144,142,8,7},{123,174,148,157,6,7},
 }
for _,p in ipairs(fronds)do fern({{p[1],p[2]},{p[3],p[4]}},p[5],p[6],true)end
-- Sparse wider leaves break up repetitive compound-leaf rhythms.
leaf("greenMid",32,194,-1,-1,11);leaf("greenGold",38,191,.7,-1,12)
leaf("green",56,169,-1,-.7,14);leaf("greenLight",76,167,1,-.8,14)
leaf("greenGold",53,156,-.7,-1,12);leaf("greenMid",83,151,1,-1,12)

newLayer("bg/13-railing")
-- Perspective converges toward the distant sidewalk near (306,198).
line("railDark",{{196,146},{207,151},{218,156},{233,164},{248,173},{266,181},{287,191},{307,197}})
line("rail",{{196,145},{207,150},{218,155},{233,163},{248,172},{266,180},{287,190},{307,196}})
line("railWarm",{{196,144},{208,150},{219,155}})
line("railLight",{{220,155},{248,171},{267,180},{287,189},{306,196}})
line("railDark",{{196,175},{224,183},{250,189},{276,196},{304,200}})
line("rail",{{196,174},{224,182},{250,188},{276,195},{304,199}})
for _,p in ipairs({{196,145,211,3},{208,152,212,3},{220,158,211,2},{234,165,207,2},{249,174,205,2},{266,182,203,1},{286,191,202,1},{302,197,201,1}})do
 rect("railDark",p[1],p[2],p[4]+1,p[3]-p[2]);rect("rail",p[1],p[2],p[4],p[3]-p[2]);line("railLight",{{p[1],p[2]},{p[1],p[3]-1}})
end

newLayer("bg/14-poles-wires-fixtures")
poly("poleShade",{{214,0},{221,0},{220,216},{214,216}})
rect("pole",215,0,4,216);rect("poleWarm",215,0,1,216)
rect("railDark",214,42,7,3);rect("railDark",214,101,7,3)
line("metal",{{220,24},{222,20},{246,20},{249,23},{249,27}})
poly("metal",{{241,26},{244,23},{251,23},{256,27},{257,29},{239,29}})
poly("lampRim",{{240,29},{257,29},{255,32},{242,32}})
-- Shorter lamps recede; lighting pixels are on the next layer.
for _,p in ipairs({{261,118,200,5},{284,146,202,4},{296,173,202,3},{333,150,209,4},{329,176,207,3},{316,191,202,2}})do
 line("blueInk",{{p[1]-1,p[2]+2},{p[1]-1,p[3]}})
 poly("metal",{{p[1]-p[4],p[2]},{p[1]-p[4]+1,p[2]-2},{p[1]+p[4]-1,p[2]-2},{p[1]+p[4],p[2]}})
end
line("blueInk",{{232,0},{235,14},{241,36},{248,56},{257,80},{269,103},{281,126},{294,153},{308,179},{318,196}})
line("blueInk",{{245,0},{249,25},{256,49},{263,69},{274,95},{285,120},{296,146},{310,177},{319,195}})
line("metal",{{258,0},{263,28},{270,55},{280,82},{291,108},{302,140},{316,177},{322,195}})
for _,p in ipairs({{271,68,10},{283,94,8},{296,125,6}})do
 line("blueInk",{{p[1],p[2]-12},{p[1]+2,p[2]+19}})
 line("blueInk",{{p[1]-p[3],p[2]},{p[1]+p[3],p[2]-1}})
 line("blueDark",{{p[1]-p[3]+1,p[2]+5},{p[1]+p[3]-1,p[2]+4}})
 rect("blueInk",p[1]-2,p[2]-8,4,5)
end
-- Shop pendant stems and shades.
line("woodInk",{{45,25},{45,53}})
poly("woodShadow",{{45,51},{39,57},{37,59},{53,59},{50,56}})
line("woodInk",{{88,52},{88,72}})
poly("woodShadow",{{88,70},{84,74},{83,76},{94,76},{92,73}})

newLayer("bg/15-lamp-light-pixels")
-- Stepped halos, no blur. Lights remain a separate locally revisable layer.
ellipse(app.pixelColor.rgba(243,177,78,25),248,31,12,7)
ellipse("lamp",248,31,8,3);ellipse("lampCore",248,31,5,2)
ellipse("lampWarm",39,9,10,3);ellipse("lampCore",39,9,8,2)
ellipse("lampWarm",101,40,7,3);ellipse("lampCore",101,40,5,2)
ellipse("lampWarm",45,60,7,2);rect("lamp",40,59,10,2);rect("lampCore",42,59,6,1)
ellipse("lampWarm",88,77,5,2);rect("lamp",85,76,7,2)
for _,p in ipairs({{261,120,4},{284,148,3},{296,175,2},{333,152,3},{329,178,2},{316,193,1}})do
 ellipse(app.pixelColor.rgba(235,173,89,22),p[1],p[2],p[3]+3,p[3]+3)
 ellipse("lamp",p[1],p[2],p[3],p[3]+1);ellipse("lampCore",p[1],p[2],math.max(1,p[3]-1),p[3])
end

newLayer("bg/16-foreground-sign-and-small-details")
poly("woodShadow",{{4,137},{22,136},{28,218},{22,228},{1,229},{0,222}})
poly("signEdge",{{4,139},{21,138},{23,221},{1,224}})
poly("sign",{{5,141},{18,140},{20,217},{3,220}})
line("woodLight",{{5,140},{2,224}});line("woodInk",{{21,139},{27,224}})
line("woodLight",{{1,225},{0,231}})
-- Suggest chalk strokes without inventing legible storefront text.
line("chalk",{{7,150},{10,148},{13,150},{11,152},{7,152}})
line("rail",{{6,157},{13,157}});line("rail",{{7,161},{15,161}})
line("rail",{{6,167},{12,167}});line("rail",{{6,172},{14,171}})
poly("greenInk",{{0,187},{3,184},{6,185},{7,188},{10,189},{10,196},{4,198},{0,195}})
leaf("greenMid",3,192,1,-1,5)

-- Preserve actual background source structure before adding the character.
s:newCel(layer,1,im,Point(0,0));layer=nil
local bgLayerCount=#s.layers
s:saveAs(path("assets/source/street-drawn-v01/background-pass01.aseprite"))
s:saveCopyAs(path("assets/export/street-drawn-v01/background-pass01.png"))

-- Grounding shadow remains independent of both environment and character.
local shadow=s:newLayer();shadow.name="ground-shadow"
local sh=Image(W,H,ColorMode.RGB)
for y=244,251 do for x=121,195 do
 if((x-158)/36)^2+((y-248)/3)^2<=1 then sh:drawPixel(x,y,app.pixelColor.rgba(36,31,48,54))end
end end
for _,p in ipairs({{137,246,13},{176,247,12}})do
 for y=p[2]-1,p[2]+1 do for x=p[1]-p[3],p[1]+p[3]do
  if((x-p[1])/p[3])^2+((y-p[2])/1.5)^2<=1 then sh:drawPixel(x,y,app.pixelColor.rgba(34,25,35,105))end
 end end
end
s:newCel(shadow,1,sh,Point(0,0))
local character=app.open(path("assets/source/standing-v04/standing.aseprite"))
local originals,positions,visibility={},{},{}
for i,l in ipairs(character.layers)do
 originals[i]=l:cel(1).image:clone();positions[i]=l:cel(1).position;visibility[i]=l.isVisible
 local copy=s:newLayer();copy.name="character/"..l.name;copy.isVisible=l.isVisible
 s:newCel(copy,1,originals[i]:clone(),Point(positions[i].x+84,positions[i].y+61))
end
s.frames[1].duration=character.frames[1].duration
local tag=s:newTag(1,1);tag.name="drawn-street-static"
s.data="Environment drawn entirely by authored pixel geometry/branch constructions. No reference raster or generated background imported. v04 copied unchanged at (84,61). Static appearance proof only."
s:saveAs(path("assets/source/street-drawn-v01/street-scene-pass01.aseprite"))
s:saveCopyAs(path("assets/export/street-drawn-v01/street-scene-pass01.png"))
s:close();character:close()
local reopened=app.open(path("assets/source/street-drawn-v01/street-scene-pass01.aseprite"))
assert(#reopened.layers==bgLayerCount+1+12)
for i=1,12 do
 local l=reopened.layers[bgLayerCount+1+i];local cel=l:cel(1)
 assert(cel.image:isEqual(originals[i]))
 assert(cel.position.x==positions[i].x+84 and cel.position.y==positions[i].y+61)
 assert(l.isVisible==visibility[i])
end
reopened:saveCopyAs(path("assets/export/street-drawn-v01/street-scene-pass01-reopened.png"))
for i,l in ipairs(reopened.layers)do l.isVisible=i>bgLayerCount+1 and visibility[i-bgLayerCount-1]or false end
reopened:saveCopyAs(path("assets/export/street-drawn-v01/character-placement-pass01.png"))
reopened:close()
local f=assert(io.open(path("docs/experiments/2026-10-26-drawn-background/source-checks-pass01.json"),"w"))
f:write(json.encode{canvas={W,H},backgroundLayers=envNames,backgroundLayerCount=bgLayerCount,sceneLayerCount=bgLayerCount+13,characterOffset={84,61},characterNativeCelsUnchangedAfterReopen=true,rasterBackgroundImports=0});f:close()
print("PASS: drawn background has "..bgLayerCount.." editable layers; scene reopened with "..(bgLayerCount+13).." layers; all v04 cel images unchanged")
