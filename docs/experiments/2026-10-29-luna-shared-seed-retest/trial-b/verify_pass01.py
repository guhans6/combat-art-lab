#!/usr/bin/env python3
"""Check pass 1's native cels, exported RGBA, frozen palette, and localized diff."""
from __future__ import annotations

import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from verify_inputs import read_aseprite  # noqa: E402

BASELINE_NATIVE = ROOT / "input" / "seed-baseline.aseprite"
BASELINE_PNG = ROOT / "input" / "seed-baseline.png"
INPUT_MANIFEST = ROOT / "input" / "input-verification.json"
CANDIDATE_NATIVE = ROOT / "pass-01" / "character-pass-01.aseprite"
CANDIDATE_PNG = ROOT / "pass-01" / "character-pass-01.png"
OUTPUT = ROOT / "pass-01" / "verification.json"
EXPECTED_DIFFS = {(68, 28), (70, 28), (69, 29)}
SMILE_RGBA = (0x74, 0x44, 0x33, 255)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def layer_name(payload: bytes) -> str:
    size = struct.unpack_from("<H", payload, 16)[0]
    return payload[18 : 18 + size].decode("utf-8")


def decode_image_cel(payload: bytes, canvas: tuple[int, int]) -> tuple[int, Image.Image]:
    layer_index, x, y, opacity, cel_type, _z = struct.unpack_from("<HhhBHh", payload, 0)
    if cel_type != 2:
        raise AssertionError(f"Expected compressed image cel; got cel type {cel_type}")
    width, height = struct.unpack_from("<HH", payload, 16)
    raw = zlib.decompress(payload[20:])
    if len(raw) != width * height * 4:
        raise AssertionError("Cel RGBA byte count does not match its dimensions")
    cel = Image.frombytes("RGBA", (width, height), raw)
    full = Image.new("RGBA", canvas, (0, 0, 0, 0))
    left, top = max(0, x), max(0, y)
    right, bottom = min(canvas[0], x + width), min(canvas[1], y + height)
    if left < right and top < bottom:
        full.paste(cel.crop((left - x, top - y, right - x, bottom - y)), (left, top))
    return layer_index, full


def parse(path: Path) -> tuple[dict, list[str], bytes, dict[int, Image.Image]]:
    parsed = read_aseprite(path)
    if (parsed["width"], parsed["height"], parsed["depth"], parsed["frame_count"]) != (128, 192, 32, 1):
        raise AssertionError(f"Unexpected native canvas/depth/frame count: {path}")
    chunks = parsed["frames"][0]["chunks"]
    palettes = [p for kind, p in chunks if kind == 0x2019]
    layers = [p for kind, p in chunks if kind == 0x2004]
    cels = [p for kind, p in chunks if kind == 0x2005]
    if len(palettes) != 1:
        raise AssertionError(f"Expected one palette chunk, got {len(palettes)}")
    names = [layer_name(p) for p in layers]
    decoded_cels = dict(decode_image_cel(p, (128, 192)) for p in cels)
    if len(decoded_cels) != len(cels):
        raise AssertionError("Multiple cels unexpectedly target the same layer")
    return parsed, names, palettes[0], decoded_cels


def main() -> None:
    manifest = json.loads(INPUT_MANIFEST.read_text(encoding="utf-8"))
    baseline = Image.open(BASELINE_PNG).convert("RGBA")
    exported = Image.open(CANDIDATE_PNG).convert("RGBA")
    if baseline.size != exported.size or exported.size != (128, 192):
        raise AssertionError(f"Unexpected PNG dimensions: baseline={baseline.size}, candidate={exported.size}")

    base_native, base_names, base_palette, base_cels = parse(BASELINE_NATIVE)
    candidate_native, candidate_names, candidate_palette, candidate_cels = parse(CANDIDATE_NATIVE)
    if base_names != ["shared-source-seed"]:
        raise AssertionError(f"Unexpected baseline layers: {base_names}")
    if candidate_names != ["character-pixels"]:
        raise AssertionError(f"Unexpected candidate layer order: {candidate_names}")

    input_palette_sha = manifest["native_baseline"]["palette_chunk_sha256"]
    if sha(base_palette) != input_palette_sha or sha(candidate_palette) != input_palette_sha:
        raise AssertionError("The original ordered palette payload changed")
    if len(base_cels) != 1 or len(candidate_cels) != 1:
        raise AssertionError("Unexpected baseline/candidate cel count")
    source_layer = candidate_cels[0]

    before, after = list(baseline.get_flattened_data()), list(exported.get_flattened_data())
    diff = [
        {"x": i % 128, "y": i // 128, "before": list(a), "after": list(b)}
        for i, (a, b) in enumerate(zip(before, after))
        if a != b
    ]
    diff_coords = {(p["x"], p["y"]) for p in diff}
    if diff_coords != EXPECTED_DIFFS:
        raise AssertionError(f"Candidate changed pixels outside the 3-pixel face mask: {diff}")
    if any(p["before"][3] != 255 or p["after"] != list(SMILE_RGBA) for p in diff):
        raise AssertionError("The mouth edit changed alpha or did not use #744433")
    source_diff = [
        (x, y)
        for y in range(192)
        for x in range(128)
        if source_layer.getpixel((x, y)) != baseline.getpixel((x, y))
    ]
    if set(source_diff) != EXPECTED_DIFFS:
        raise AssertionError(f"Native source cel differs beyond the three-pixel face mask: {source_diff}")
    if any(source_layer.getpixel(p) != SMILE_RGBA for p in EXPECTED_DIFFS):
        raise AssertionError("The native face edit does not use frozen palette color #744433")
    if source_layer.tobytes() != exported.tobytes():
        raise AssertionError("Aseprite native cel does not match its exported PNG")

    alpha_values = sorted(set(exported.getchannel("A").get_flattened_data()))
    visible_count = sum(a != 0 for a in exported.getchannel("A").get_flattened_data())
    visible_colors = len({p[:3] for p in exported.get_flattened_data() if p[3] != 0})
    baseline_alpha = sorted(set(baseline.getchannel("A").get_flattened_data()))
    if alpha_values != baseline_alpha or alpha_values != [0, 255]:
        raise AssertionError(f"Unexpected alpha values: {alpha_values}")
    if visible_count != sum(a != 0 for a in baseline.getchannel("A").get_flattened_data()):
        raise AssertionError("Visible-pixel count changed")
    if exported.getchannel("A").getbbox() != baseline.getchannel("A").getbbox():
        raise AssertionError("Visible bounds changed")

    result = {
        "verification": "PASS",
        "method": "Python binary parsing of the saved Aseprite file plus Pillow RGBA comparison",
        "native_candidate": {
            "sha256": sha(CANDIDATE_NATIVE.read_bytes()),
            "dimensions": [128, 192],
            "depth": 32,
            "frames": 1,
            "layers_top_to_bottom": candidate_names,
            "layer_coverage": {"character-pixels": "full static sprite; source seed retained as a separate exact input, with only the three recorded mouth pixels revised"},
            "palette_chunk_sha256": sha(candidate_palette),
            "palette_matches_frozen_input": True,
        },
        "candidate_png": {
            "sha256": sha(CANDIDATE_PNG.read_bytes()),
            "rgba_sha256": sha(exported.tobytes()),
            "dimensions": list(exported.size),
            "alpha_values": alpha_values,
            "visible_pixel_count": visible_count,
            "visible_rgb_color_count": visible_colors,
            "visible_bounds": list(exported.getchannel("A").getbbox()),
            "native_cel_matches_export": True,
        },
        "baseline_png": {
            "sha256": sha(BASELINE_PNG.read_bytes()),
            "rgba_sha256": sha(baseline.tobytes()),
            "alpha_values": baseline_alpha,
        },
        "diff": {"changed_pixel_count": len(diff), "pixels": diff, "outside_mask_count": 0},
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
