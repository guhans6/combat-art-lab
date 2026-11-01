"""Read-only verification for the bounded E1 candidate."""
from hashlib import sha256
import json
from pathlib import Path
import runpy
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
FREEZE = json.loads((ROOT / "freeze.json").read_text())

def rgba(path):
    return Image.open(path).convert("RGBA")

for item in FREEZE["frozen_inputs"]:
    path = REPO / item["path"]
    assert sha256(path.read_bytes()).hexdigest() == item["sha256"], path

control = rgba(ROOT / "inputs/control-a.png")
candidate = rgba(ROOT / "outputs/candidate-b-normalized.png")
reopened = rgba(ROOT / "outputs/candidate-b-normalized-reopened.png")
assert candidate.tobytes() == reopened.tobytes()
assert control.size == candidate.size == (120, 112)
changed = []
for i, (before, after) in enumerate(zip(control.get_flattened_data(), candidate.get_flattened_data())):
    assert before[3] == after[3], f"alpha changed at index {i}"
    if before != after:
        changed.append([i % 120, i // 120])
assert changed == FREEZE["candidate"]["allowed_coordinates_zero_based"], changed

checker = runpy.run_path(str(REPO / "tools/check_native_pilot.py"))
profile = json.loads((ROOT / "strict-profile.json").read_text())
mask = list(Image.open(ROOT / "candidate-allowed-mask.png").convert("L").get_flattened_data())
normalized = checker["compare"](
    ROOT / "outputs/control-a-normalized.aseprite",
    ROOT / "outputs/candidate-b-normalized.aseprite",
    profile["editable_layers"], mask,
)
assert normalized["passed"], normalized
raw = checker["compare"](
    ROOT / "inputs/control-a.aseprite",
    ROOT / "outputs/candidate-b.aseprite",
    profile["editable_layers"], mask,
)
assert not raw["passed"] and raw["failures"] == ["header changed", "frames changed"], raw
print("PASS: frozen E0 inputs unchanged; exactly four opaque jacket pixels changed; reopened export and normalized strict proof pass")
