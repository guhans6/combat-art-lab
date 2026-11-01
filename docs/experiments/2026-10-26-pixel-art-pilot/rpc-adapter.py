import json,sys,time
from pathlib import Path
p=Path('docs/experiments/2026-10-26-pixel-art-pilot/backend-session')
q=json.load(sys.stdin);(p/'response.json').unlink(missing_ok=True);assert not (p/'request.json').exists();(p/'request.json').write_text(json.dumps(q))
for _ in range(500):
 if (p/'response.json').exists():
  r=json.loads((p/'response.json').read_text())
  for i in r:
   print(json.dumps(i))
  break
 time.sleep(.1)
else: raise TimeoutError('MCP batch still pending; inspect before retrying')
