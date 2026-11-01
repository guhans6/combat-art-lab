"""Check native placement exports and make an integer-scale presentation PNG."""
from pathlib import Path
from PIL import Image
import hashlib
import json

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'assets/export/street-preview-v01'
PREVIEW=ROOT/'assets/previews/street-preview-v01'
scene=Image.open(OUT/'street-scene-native.png').convert('RGBA')
reopened=Image.open(OUT/'street-scene-reopened.png').convert('RGBA')
assert scene.size==(352,264) and scene.tobytes()==reopened.tobytes()
character=Image.open(ROOT/'assets/export/standing-v04/standing.png').convert('RGBA')
expected=Image.new('RGBA',scene.size,(0,0,0,0))
expected.alpha_composite(character,(84,61))
placed=Image.open(OUT/'character-placement-only.png').convert('RGBA')
assert expected.tobytes()==placed.tobytes()
bg=Image.open(OUT/'background-native.png').convert('RGBA')
shadow=Image.open(OUT/'ground-shadow.png').convert('RGBA')
composed=bg.copy();composed.alpha_composite(shadow);composed.alpha_composite(placed)
rounding=[]
for y in range(264):
    for x in range(352):
        a,b=composed.getpixel((x,y)),scene.getpixel((x,y))
        if a!=b:
            assert shadow.getpixel((x,y))[3] and not placed.getpixel((x,y))[3]
            delta=max(abs(p-q) for p,q in zip(a,b));assert delta<=1
            rounding.append(delta)
baseline=json.loads((ROOT/'docs/experiments/2026-10-26-shoe-detail/checks.json').read_text())
assert hashlib.sha256((ROOT/'assets/source/standing-v04/standing.aseprite').read_bytes()).hexdigest()==baseline['nativeSHA256']
assert hashlib.sha256((ROOT/'assets/export/standing-v04/standing.png').read_bytes()).hexdigest()==baseline['exportSHA256']
scene.resize((1408,1056),Image.Resampling.NEAREST).save(PREVIEW/'street-scene-4x.png')
report={
    'canvas':[352,264],'preview':[1408,1056],'characterOffset':[84,61],
    'characterPlacementExactRGBA':True,'v04SourceAndPNGUnchanged':True,
    'nativeReopenExportIdentical':True,'layers':14,
    'backgroundMethod':'One built-in imagegen edit removed original figure; explicit nearest-neighbor sampling for scene grid',
    'backgroundStructure':'One flat raster layer; environment objects not separately editable',
    'backgroundOutsideRemovalNotClaimedPixelIdentical':True,
    'shadowLayerSeparate':True,'independentCompositionMatchesOutsideShadow':True,
    'shadowRendererRoundingDifferentPixels':len(rounding),'shadowRoundingMaxChannelDelta':max(rounding,default=0),
    'nativeSHA256':hashlib.sha256((ROOT/'assets/source/street-preview-v01/street-scene.aseprite').read_bytes()).hexdigest(),
    'exportSHA256':hashlib.sha256((OUT/'street-scene-native.png').read_bytes()).hexdigest(),
    'GodotPlayback':'not performed','userVisualAcceptance':'pending',
}
(ROOT/'docs/experiments/2026-10-26-street-preview/checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
