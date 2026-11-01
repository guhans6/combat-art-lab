-- A: measured source-coordinate tracing. B: source-derived seed + semantic cleanup.
-- All native creation/saves occur in the installed Aseprite, never a file encoder.
local dir=assert(app.params.out)
local limit=tonumber(app.params.limit or '0')
local arm=assert(app.params.arm);assert(arm=='a' or arm=='b')
local data=dofile(dir..'/data.lua')
local s=Sprite(120,112,ColorMode.RGB)
s.layers[1].name='01-jacket'
local names={'01-jacket','02-shirt','03-neck-ear','04-rear-hair','05-face','06-crown-fringe','07-hair-tie','08-eyes-brows','09-mouth'}
local layers={};layers[names[1]]=s.layers[1]
for i=2,#names do local l=s:newLayer();l.name=names[i];layers[names[i]]=l end
local palette=Palette(#data.palette+1);palette:setColor(0,app.pixelColor.rgba(0,0,0,0))
for i,c in ipairs(data.palette) do palette:setColor(i,app.pixelColor.rgba(c[1],c[2],c[3],255)) end
s:setPalette(palette)
local C={};for k,c in pairs(data.colors) do C[k]=app.pixelColor.rgba(c[1],c[2],c[3],255) end
local im,active
local function flush()
 if active and im then local cel=active:cel(1);if cel then cel.image=im;cel.position=Point(0,0) else s:newCel(active,1,im,Point(0,0)) end end
end
local function xy(p) return math.floor((p[1]-380)/4+.5),math.floor((p[2]-64)/4+.5) end
local function put(x,y,key)
 if x>=0 and x<120 and y>=0 and y<112 then im:drawPixel(x,y,C[key]) end
end
local function line(key,pts)
 for i=1,#pts-1 do
 local x,y=xy(pts[i]);local tx,ty=xy(pts[i+1]);local dx=math.abs(tx-x);local dy=-math.abs(ty-y);local sx=x<tx and 1 or -1;local sy=y<ty and 1 or -1;local err=dx+dy
 while true do put(x,y,key);if x==tx and y==ty then break end;local e=2*err;if e>=dy then err=err+dy;x=x+sx end;if e<=dx then err=err+dx;y=y+sy end end
 end
end
local function poly(key,pts)
 local q={};local ymin,ymax=112,0
 for _,p in ipairs(pts) do local x,y=xy(p);q[#q+1]={x,y};ymin=math.min(ymin,y);ymax=math.max(ymax,y) end
 for y=math.max(0,ymin),math.min(111,ymax) do
 local xs={};for i=1,#q do local a,b=q[i],q[i%#q+1];if (a[2]<=y+.5 and b[2]>y+.5) or (b[2]<=y+.5 and a[2]>y+.5) then xs[#xs+1]=a[1]+(y+.5-a[2])*(b[1]-a[1])/(b[2]-a[2]) end end
 table.sort(xs);for i=1,#xs-1,2 do for x=math.ceil(xs[i]-.5),math.floor(xs[i+1]-.5) do put(x,y,key) end end
 end
end
local function select(name)
 flush();active=layers[name];local cel=active:cel(1)
 im=Image(120,112,ColorMode.RGB)
 if cel then im:drawImage(cel.image,cel.position) end
end
-- Save normalizes trimmed cel geometry. Reopen and expand before subsequent source-coordinate ops.
local checkpoint_index=-1
local function checkpoint(name)
 flush();checkpoint_index=checkpoint_index+1
 if checkpoint_index~=limit then return end
 local out=app.params.destination or dir
 assert(not app.fs.isFile(out..'/'..name..'.aseprite'), 'Refuse overwrite')
 s:setPalette(palette);s:saveAs(out..'/'..name..'.aseprite');s:saveCopyAs(out..'/'..name..'.png')
 print('saved '..name)
end
if arm=='b' then
 for _,name in ipairs(names) do
  local image=Image{fromFile=dir..'/prepared/'..name..'.png'}
  s:newCel(layers[name],1,image,Point(0,0))
 end
 checkpoint('b00-separated-seed')
else
 select('01-jacket');poly('jacketdeep',data.regions['01-jacket']);poly('jacket',{{442,512},{458,460},{520,422},{564,402},{583,407},{562,451},{549,512}});poly('jacket',{{670,387},{702,385},{734,397},{771,424},{801,463},{828,512},{690,512},{679,475},{698,433}})
 poly('jacketlight',{{704,398},{727,396},{747,411},{760,428},{738,459},{720,491},{693,512},{687,493},{704,450},{712,421}})
 select('02-shirt');poly('shirt',data.regions['02-shirt']);poly('shirtshadow',{{556,463},{563,488},{588,501},{594,512},{577,512},{552,493},{546,481}})
 select('03-neck-ear');poly('skin',data.regions['03-neck-ear']);poly('skindeep',{{595,352},{627,365},{670,371},{669,407},{649,404},{621,387},{601,376}});poly('skinshadow',{{596,377},{615,388},{644,407},{666,411},{678,423},{657,419},{629,407},{607,396},{597,390}})
 select('04-rear-hair');poly('hairdeep',data.regions['04-rear-hair']);poly('hair',{{483,222},{463,221},{442,239},{422,268},{418,298},{427,325},{444,340},{465,345},{477,330},{498,338},{519,339},{536,329},{536,301},{516,268},{499,244}})
 select('05-face');poly('skin',data.regions['05-face']);poly('skinlight',{{612,285},{638,259},{670,246},{695,253},{722,247},{730,268},{730,297},{736,315},{731,333},{717,352},{695,368},{666,369},{640,363},{619,351},{610,332}});poly('skinshadow',{{551,307},{560,299},{570,301},{574,320},{586,322},{585,334},{570,339},{557,331}})
 select('06-crown-fringe');poly('hairdeep',data.regions['06-crown-fringe']);poly('hair',{{467,177},{478,158},{495,149},{509,159},{537,148},{563,139},{593,131},{631,130},{666,139},{686,134},{716,143},{742,150},{758,170},{777,196},{780,219},{774,245},{761,269},{758,289},{766,311},{748,295},{739,264},{725,234},{710,230},{695,219},{691,245},{687,250},{678,227},{665,196},{657,207},{650,235},{634,244},{621,262},{606,280},{602,295},{609,312},{601,307},{587,282},{575,279},{562,285},{555,299},{546,289},{532,269},{517,248},{510,224},{489,214},{476,200}})
 select('07-hair-tie');poly('tie',data.regions['07-hair-tie'])
 -- Empty semantic feature cels support later coherent feature placement.
 select('08-eyes-brows');select('09-mouth')
 checkpoint('a00-traced-planes')
end
if limit==0 then s:close();return end
-- Checkpoint 1: major hair-cluster cleanup, identical pass budget in both arms.
if arm=='a' then
 select('04-rear-hair')
 poly('hairplane',{{480,226},{461,234},{442,253},{432,278},{430,302},{435,320},{444,326},{440,307},{443,283},{454,257},{473,242}})
 poly('hairdeep',{{481,241},{469,263},{463,288},{466,311},{478,331},{489,334},{480,313},{475,296},{479,272},{493,248}})
 poly('hairplane',{{499,245},{492,268},{494,292},{506,310},{522,322},{532,323},{517,307},{506,288},{502,266}})
 line('hairdeep',{{445,329},{445,347},{456,357},{466,355},{474,346}})
 line('hair',{{487,338},{494,353},{511,362},{525,361},{535,352}})
 line('hair',{{537,346},{544,363},{555,371},{562,372}})
 select('06-crown-fringe')
 poly('hairplane',{{511,166},{537,150},{567,140},{597,134},{623,132},{603,143},{579,155},{552,171},{528,180},{510,177}})
 poly('hairplane',{{507,190},{529,195},{550,188},{574,176},{598,159},{618,141},{624,137},{614,156},{596,177},{571,193},{544,206},{521,215},{508,211}})
 poly('hairdeep',{{516,219},{539,215},{561,205},{585,187},{601,170},{594,190},{575,213},{550,234},{535,251},{528,260},{521,249},{514,232}})
 line('hairdeep',{{605,136},{583,156},{560,175},{539,185},{515,194}})
 line('hairdeep',{{630,135},{614,153},{600,169},{578,185},{553,199},{530,207},{510,211}})
 poly('hairplane',{{639,144},{645,156},{643,177},{634,198},{624,215},{612,245},{604,261},{611,254},{628,229},{641,214},{648,190},{650,168},{647,151}})
 poly('hairdeep',{{655,146},{665,166},{669,188},{676,210},{681,235},{685,247},{684,262},{678,247},{672,234},{664,216},{659,193},{654,171}})
 line('hairplane',{{664,177},{666,191},{673,214}})
 poly('hairplane',{{693,149},{704,158},{716,173},{724,192},{724,208},{718,187},{708,170}})
 poly('hairdeep',{{741,165},{753,188},{759,211},{757,231},{762,247},{763,261},{772,240},{773,216},{765,195},{753,176}})
 line('hairplane',{{483,159},{476,171},{482,187},{492,198}})
 line('hairplane',{{542,178},{548,172},{554,170}})
 line('hairlight',{{590,207},{594,201},{595,210}})
 line('hairlight',{{603,202},{606,197},{608,204}})
 line('hairplane',{{621,203},{626,197},{626,207}})
 line('hairplane',{{670,190},{675,187},{677,193}})
 line('hair',{{726,144},{739,133},{744,118}})
 checkpoint('a01-hair-clusters')
else
 -- Converted hair already carries source planes. Replace only isolated bright fringe
 -- speckles/edge contamination within the visible hair/tie, not a global filter.
 select('06-crown-fringe')
 line('hairdeep',{{531,272},{538,287},{543,297}})
 line('hair',{{759,288},{765,305},{773,314}})
 line('hairdeep',{{739,326},{737,338},{733,346}})
 select('07-hair-tie');poly('tie',{{488,220},{493,220},{494,230},{493,237},{489,236}})
 checkpoint('b01-hair-cleanup')
end
if limit==1 then s:close();return end
-- Checkpoint 2: separate source-observed lids/gaze and restrained mouth.
if arm=='a' then
 select('08-eyes-brows')
 line('hairdeep',{{620,257},{637,253},{651,252},{663,256}})
 line('hairdeep',{{705,243},{715,240},{726,243}})
 poly('white',{{619,283},{629,278},{646,278},{660,282},{662,305},{650,309},{633,304},{621,296}})
 poly('iris',{{653,279},{664,279},{665,303},{660,309},{654,308}})
 line('feature',{{619,286},{624,279},{638,274},{652,273},{661,276}})
 line('feature',{{660,278},{661,291},{661,301}})
 poly('white',{{708,266},{716,262},{726,262},{728,285},{724,293},{716,291},{710,283}})
 poly('iris',{{720,261},{728,261},{729,283},{725,294},{721,292}})
 line('feature',{{708,266},{715,260},{724,258},{730,261}})
 select('05-face');line('skinshadow',{{711,293},{711,309},{717,313}});line('blush',{{624,318},{635,320},{646,319}})
 select('09-mouth');line('mouth',{{675,337},{679,341},{690,342},{701,341},{707,338}})
 select('03-neck-ear');line('skinshadow',{{573,452},{588,459},{607,463}});line('skinshadow',{{634,466},{648,459},{664,455},{679,445}})
 select('01-jacket');line('jacketdeep',{{565,399},{548,420},{536,439},{543,455},{526,467},{518,503}});line('jacketdeep',{{701,396},{711,414},{699,436},{692,462},{684,484}})
 line('strap',{{796,435},{781,440},{770,455},{767,478},{768,512}})
 checkpoint('a02-expression')
else
 select('08-eyes-brows')
 -- Re-articulate just the lost upper-lid/pupil boundary; preserve sampled eye planes.
 line('feature',{{620,283},{628,277},{640,274},{654,274},{661,277}})
 line('iris',{{657,283},{657,301}})
 line('feature',{{710,265},{718,260},{727,260}})
 select('09-mouth');line('mouth',{{675,338},{679,341},{691,342},{702,341},{707,338}})
 checkpoint('b02-expression')
end
s:close()
