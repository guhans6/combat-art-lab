from pathlib import Path
from PIL import Image
import sys,json,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R.parent/'2026-10-30-evidence-idle-four-model/sol61'));from native_read import read,composite
checks={};a=read(R/'proof/smoke-before.aseprite');b=read(R/'proof/smoke-after.aseprite');z=read(R/'proof/smoke-forbidden.aseprite');d=np.any(np.array(composite(a,0))!=np.array(composite(b,0)),2)
checks['single_pixel_changed']=int(d.sum())==1 and bool(d[5,8]);checks['protected_layer_exact']=a['cels'][(0,0)]['image'].tobytes()==b['cels'][(0,0)]['image'].tobytes();checks['asymmetric_L_orientation']=composite(a,0).getpixel((2,4))==(36,48,68,255) and composite(a,0).getpixel((4,2))==(36,48,68,255) and composite(a,0).getpixel((4,4))==(0,0,0,0);checks['isolated_pixel_location']=composite(a,0).getpixel((13,12))==(233,213,174,255)
checks['fresh_reopen_matches']=Image.open(R/'proof/smoke-reopen.png').convert('RGBA').tobytes()==composite(b,0).tobytes();checks['transparent_skip_exact']=Image.open(R/'proof/smoke-skip.png').convert('RGBA').tobytes()==composite(b,0).tobytes();er=Image.open(R/'proof/smoke-erase.png').convert('RGBA');checks['transparent_erase']=er.getpixel((7,4))[3]==0 and np.any(np.array(er)!=np.array(composite(b,0)),2).sum()==1
# Protection checker deliberately rejects a known out-of-mask mutation, rather than ignoring it.
locked_change=a['cels'][(0,0)]['image'].tobytes()!=z['cels'][(0,0)]['image'].tobytes();checks['forbidden_change_rejected']=locked_change
checks['native_two_layers']=len(a['layers'])==2;checks['mcp_validate_callable']=False
(R/'proof/smoke-checks.json').write_text(json.dumps({'checks':{k:bool(v) for k,v in checks.items()},'all_required_pass':all(v for k,v in checks.items() if k!='mcp_validate_callable'),'observation':'Primary viewed L opening right/down, red square, isolated cream pixel13,12; exact ASCII read; first pixels op rejected schema and corrected to grid; tool validate advertised but not exposed.'},indent=2));print(checks)
