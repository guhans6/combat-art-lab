import json
from pathlib import Path
import sys

grids = json.loads((Path(__file__).resolve().parents[1] / "prep/semantic/draw-grids.json").read_text())
print(json.dumps(grids[sys.argv[1]], separators=(",", ":")))
