from pathlib import Path
import json,shutil
P=Path('/private/tmp/atmospheric-idle-sample-r04');shutil.copy2(P/'keys/key-0.png',P/'source-rest.png')
evidence=[{'role':'candidate native structural keys','path':'keys/connected-keys.aseprite'},{'role':'immutable baseline native','path':'baseline-r03.aseprite'},{'role':'native/export and protected lower-owner readback','path':'keys/checks.json'},{'role':'frozen proposal and source observations','path':'observations.md'},{'role':'MCP drawing inputs','path':'key-ops.json'}]
for p in sorted((P/'keys').glob('*.png')):
 if not p.name.startswith('drawing-data'):evidence.append({'role':'actual native-derived structural key/owner/hide/landmark evidence','path':str(p.relative_to(P))})
spec={'baseline_role':'retained exact r03 REST appearance; diagnostic traveler only; user approval absent','registration':'same96x160 canvas and world root; no per-frame fitting; REST lower-owner coordinates protected','required_frame_ids':['K0','K1','K2'],'evidence':evidence,'frames':[{'id':f'K{f}','before':'source-rest.png','after':f'keys/key-{f}.png','mask':'editable-upper-frozen.png','regions':[{'name':'skull-neck-collar-shoulder','crop':[28,6,66,49]},{'name':'torso-upper-sleeve-elbow','crop':[28,35,66,70]},{'name':'forearm-wrist-waist-skirt-overlap','crop':[28,58,66,97]}]}for f in range(3)],'zoom':4}
json.dump(spec,open(P/'comparison-keys.json','w'),indent=2)
