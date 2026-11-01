"""Fail-closed, read-only E0 replay evidence verifier."""
from pathlib import Path
from hashlib import sha256
import json, runpy
from PIL import Image

root = Path(__file__).resolve().parents[1]
repo = root.parents[2]
recipe = json.loads((root / "recipe.json").read_text())
assert sha256((repo / recipe["source"]["path"]).read_bytes()).hexdigest() == recipe["source"]["sha256"]
rgba = lambda p: Image.open(p).convert("RGBA")
paths = [root / "run-a/replay-2/b00-separated-seed.png", root / "run-b/replay-2/b00-separated-seed.png", root / "run-a/replay-2/b00-separated-seed-reopened.png", root / "run-b/replay-2/b00-separated-seed-reopened.png", root / "inputs/historical-b00-seed.png"]
assert len({rgba(p).tobytes() for p in paths}) == 1
assert rgba(root / "run-b/replay-2/b00-normalized.png").tobytes() == rgba(paths[0]).tobytes()
native = runpy.run_path(str(repo / "tools/check_native_pilot.py"))
mask = [False] * (120 * 112); mask[38 * 120 + 26] = True
result = native["compare"](root / "run-b/replay-2/b00-normalized.aseprite", root / "run-b/replay-2/b00-normalized-tie-edit.aseprite", ["07-hair-tie"], mask)
assert result["passed"], result
assert rgba(root / "run-b/replay-2/b00-normalized-tie-edit.png").tobytes() == rgba(root / "run-b/replay-2/b00-normalized-tie-edit-reopened.png").tobytes()
print("PASS: source, two B00 replays/reopens, normalized strict edit, and edited reopen verified")
