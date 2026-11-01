"""Recheck this experiment's RGBA native evidence; not an art-quality test."""
from pathlib import Path
import hashlib
import json
import runpy

from PIL import Image

HERE = Path(__file__).resolve().parent
native = runpy.run_path(str(HERE.parents[2] / "tools/check_native_pilot.py"))


def compare(name, source_suffix, edit_suffix):
    source = HERE / f"{name}{source_suffix}.aseprite"
    edited = HERE / f"{name}{edit_suffix}.aseprite"
    document = native["read"](source)
    expected = [120, 132] if "192" in name else [160, 176]
    assert document["canvas"] == expected
    assert len(document["layers"]) == 7 and len(document["frames"]) == 1
    mask = [False] * (expected[0] * expected[1])
    mask[0] = True
    result = native["compare"](source, edited, ["Back hair"], mask)
    assert sum(row["changed_pixels"] for row in result["layers"]) == 1
    assert sum(row["protected_changed_pixels"] for row in result["layers"]) == 0
    result["source_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    result["native_canvas"] = expected
    result["native_layer_count"] = len(document["layers"])
    return result


raw = {}
normalized = {}
for size in (192, 256):
    for suffix in ("", "-pass02"):
        name = f"study-{size}{suffix}"
        result = compare(name, "", "-edit-proof")
        # Keep the actual strict rejection; never exempt these fields in the reader.
        assert result["failures"] == ["header changed", "frames changed"]
        a = native["read"](HERE / f"{name}.aseprite")
        b = native["read"](HERE / f"{name}-edit-proof.aseprite")
        result["non_cel_chunks_before"] = a["frames"][0]["non_cel_chunks"]
        result["non_cel_chunks_after"] = b["frames"][0]["non_cel_chunks"]
        before_bytes = (HERE / f"{name}.aseprite").read_bytes()
        after_bytes = (HERE / f"{name}-edit-proof.aseprite").read_bytes()
        result["header_color_count_before"] = int.from_bytes(before_bytes[32:34], "little")
        result["header_color_count_after"] = int.from_bytes(after_bytes[32:34], "little")
        result["header_changed_offsets"] = [
            i for i, (x, y) in enumerate(zip(before_bytes[:128], after_bytes[:128])) if x != y
        ]
        raw[name] = result
    name = f"study-{size}-pass02"
    result = compare(name, "-normalized", "-normalized-edit")
    with Image.open(HERE / f"{name}.png") as image:
        original = image.convert("RGBA")
    with Image.open(HERE / f"{name}-normalized.png") as image:
        baseline = image.convert("RGBA")
    with Image.open(HERE / f"{name}-normalized-edit.png") as image:
        edited = image.convert("RGBA")
    result["normalized_export_matches_original"] = (
        original.size == baseline.size and original.tobytes() == baseline.tobytes()
    )
    result["composite_changed_pixels"] = sum(
        x != y for x, y in zip(baseline.get_flattened_data(), edited.get_flattened_data())
    )
    assert result["passed"] and result["normalized_export_matches_original"]
    assert result["composite_changed_pixels"] == 1
    normalized[name] = result

for filename, report in (
    ("independent-native-checks.json", raw),
    ("normalized-native-checks.json", normalized),
):
    (HERE / filename).write_text(json.dumps(report, indent=2) + "\n")
print("Observed four original palette/header rejections; two normalized strict native proofs pass.")
