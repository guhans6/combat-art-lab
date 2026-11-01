-- Technical scratch proof only: preserve original studies, freeze a saved/exported
-- palette state, then test one scoped native edit without weakening the checker.
local dir = assert(app.params.out)
for _, size in ipairs({192, 256}) do
  local name = 'study-' .. size .. '-pass02'
  local sprite = app.open(dir .. '/' .. name .. '.aseprite')
  sprite:saveCopyAs(dir .. '/' .. name .. '-normalized.png')
  sprite:saveAs(dir .. '/' .. name .. '-normalized.aseprite')
  sprite:close()
  sprite = app.open(dir .. '/' .. name .. '-normalized.aseprite')
  local image = sprite.layers[1]:cel(1).image
  image:drawPixel(0, 0, app.pixelColor.rgba(255, 0, 255, 255))
  sprite:saveAs(dir .. '/' .. name .. '-normalized-edit.aseprite')
  sprite:saveCopyAs(dir .. '/' .. name .. '-normalized-edit.png')
  sprite:close()
end
