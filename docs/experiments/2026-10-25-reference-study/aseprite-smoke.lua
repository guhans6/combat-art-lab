-- Tool integration check only; these swatches are not a character or art candidate.
-- Run with --batch --script-param output=<absolute directory> --script <this file>.
local out = assert(app.params["output"], "output parameter required")
local function path(name) return app.fs.joinPath(out, name) end
local sprite = Sprite(32, 16, ColorMode.RGB)
local base = sprite.layers[1]
base.name = "base-cool-shadow"
local cool = app.pixelColor.rgba(35, 48, 70, 255)
local warm = app.pixelColor.rgba(224, 154, 75, 255)
local revised = app.pixelColor.rgba(80, 180, 165, 255)
local image = Image(32, 16, ColorMode.RGB)
for y = 0, 15 do
  for x = 0, 31 do image:drawPixel(x, y, cool) end
end
sprite.cels[1].image = image
local accent = sprite:newLayer()
accent.name = "editable-accent"
local function accentImage(color)
  local img = Image(32, 16, ColorMode.RGB)
  for y = 4, 11 do
    for x = 20, 27 do img:drawPixel(x, y, color) end
  end
  return img
end
sprite:newCel(accent, 1, accentImage(warm), Point(0, 0))
sprite:saveAs(path("swatches-before.aseprite"))
sprite:saveCopyAs(path("swatches-before.png"))
sprite:close()

local reopened = app.open(path("swatches-before.aseprite"))
assert(reopened.width == 32 and reopened.height == 16)
assert(#reopened.layers == 2 and #reopened.frames == 1)
assert(reopened.layers[1].name == "base-cool-shadow")
assert(reopened.layers[2].name == "editable-accent")
assert(reopened.layers[1]:cel(1).image:getPixel(0, 0) == cool)
reopened.layers[2]:cel(1).image = accentImage(revised)
reopened:saveAs(path("swatches-after.aseprite"))
reopened:saveCopyAs(path("swatches-after.png"))
reopened:close()

local after = app.open(path("swatches-after.aseprite"))
assert(#after.layers == 2 and #after.frames == 1)
assert(after.layers[1]:cel(1).image:getPixel(0, 0) == cool)
assert(after.layers[2]:cel(1).image:getPixel(20, 4) == revised)
print("PASS: 32x16 native file reopened; two named layers retained; accent revised; base sample unchanged; PNG exports saved")
after:close()
