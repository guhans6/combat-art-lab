from PIL import Image,ImageDraw
from pathlib import Path
import json
O=Path('/private/tmp/fighter-user-variants-r01/native-work')
# Reviewed outer contours authored from original RGB row diagnostics. Preserve every
# interior source pixel, including colors identical to background; no global key/holes.
righttop={
'01':[(43,65),(46,67),(49,69),(52,68),(55,70),(58,73),(61,75),(64,76),(67,76),(70,76),(73,76),(76,76),(79,76),(82,76),(85,76),(88,76),(91,78),(94,78)],
'03':[(43,66),(46,68),(49,70),(52,69),(55,72),(58,75),(61,77),(64,78),(67,77),(70,78),(73,79),(76,78),(79,78),(82,79),(85,79),(88,79),(91,79),(94,80)],
'04':[(43,65),(46,68),(49,67),(52,69),(55,72),(58,74),(61,75),(64,77),(67,77),(70,77),(73,77),(76,77),(79,77),(82,77),(85,78),(88,78),(91,79),(94,79)]}
rightlower={'01':[(171,83),(175,81),(178,80),(181,80),(184,80),(187,79),(190,79),(193,78),(196,78),(199,78),(202,78),(205,78),(208,78),(211,78),(214,78),(217,78),(220,78),(223,78),(226,77),(229,76),(232,79),(235,78),(238,80)],'03':[(171,81),(175,81),(178,82),(181,82),(184,81),(187,80),(190,79),(193,79),(196,78),(199,78),(202,78),(205,78),(208,78),(211,78),(214,79),(217,79),(220,79),(223,77),(226,78),(229,78),(232,79),(235,79),(238,79)],'04':[(171,81),(175,81),(178,81),(181,80),(184,80),(187,78),(190,78),(193,78),(196,78),(199,78),(202,78),(205,77),(208,76),(211,76),(214,76),(217,77),(220,77),(223,78),(226,77),(229,76),(232,76),(235,78),(238,78)]}
for i in ['01','03','04','05']:
 D=O/f'variant-{i}';mask=Image.open(D/'source-spatial-mask-native.png').convert('L');d=ImageDraw.Draw(mask);base='03' if i=='05' else i
 for rows in [righttop[base],rightlower[base]]:
  # Change only declared exterior band. Restore collar pixels on the source-backed
  # inner side where the initial coarse outline cut too far inward.
  for (y0,x0),(y1,x1) in zip(rows,rows[1:]):
   for y in range(y0,y1+1):
    edge=round(x0+(x1-x0)*(y-y0)/(y1-y0));d.line((edge+1,y,100,y),fill=0)
    if y<95:d.line((64,y,edge,y),fill=255)
 source=Image.open(O/f'preparation/source-grid-{i}.png').convert('RGBA');source.putalpha(mask);source.putdata([p if p[3] else (0,0,0,0) for p in source.getdata()]);source.save(D/'raw-unquantized.png');mask.save(D/'source-spatial-mask-native.png')
 r=json.loads((D/'recipe.json').read_text());r['pass01_reviewed_right_contour_top_yx']=righttop[base];r['pass01_reviewed_right_contour_lower_yx']=rightlower[base];r['cleanup']='pass01 source-quality repair: source-RGB medoid palette, source-backed hair restoration and reviewed exterior contour traces';(D/'recipe.json').write_text(json.dumps(r,indent=2))
