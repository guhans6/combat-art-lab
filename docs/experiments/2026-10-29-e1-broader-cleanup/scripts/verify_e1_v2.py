"""Read-only E1-v2 evidence check."""
from pathlib import Path
import json
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
a = Image.open(ROOT / "inputs/control-a.png").convert("RGBA")
b = Image.open(ROOT / "outputs/candidate-b.png").convert("RGBA")
r = Image.open(ROOT / "outputs/candidate-normalized-reopened.png").convert("RGBA")
ledger = json.loads((ROOT / "change-ledger.json").read_text())["changes"]
assert len(ledger) == 392
assert sum(x != y for x, y in zip(a.get_flattened_data(), b.get_flattened_data())) == 392
assert Image.open(ROOT / "outputs/candidate-b.png").convert("RGBA").tobytes() == r.tobytes()
assert json.loads((ROOT / "raw-strict-check.json").read_text())["passed"]
assert json.loads((ROOT / "normalized-strict-check.json").read_text())["passed"]
print("PASS: 392 ledgered changes, raw/normalized strict checks, and reopened export")
