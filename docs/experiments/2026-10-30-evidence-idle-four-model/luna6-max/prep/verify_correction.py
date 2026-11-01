#!/usr/bin/env python3
"""Confirm the separate artistic correction changed only the declared shirt fold."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("native_reader", HERE / "check_native_candidate.py")
native_reader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(native_reader)

EXPECTED = [[60, 53], [61, 53], [60, 54], [61, 54]]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rgba_at(pixels: bytes, canvas_width: int, x: int, y: int) -> list[int]:
    i = (y * canvas_width + x) * 4
    return list(pixels[i:i + 4])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pass01", required=True)
    ap.add_argument("--corrected", required=True)
    ap.add_argument("--expected-pass01-sha256", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    pass01_path, corrected_path = Path(args.pass01), Path(args.corrected)
    before = native_reader.read_aseprite(pass01_path)
    after = native_reader.read_aseprite(corrected_path)
    failures: list[str] = []
    if before["canvas"] != after["canvas"] or before["depth"] != after["depth"]:
        failures.append("canvas or color depth changed")
    if before["layers"] != after["layers"]:
        failures.append("layer order/properties changed")
    if [f["duration_ms"] for f in before["frames"]] != [f["duration_ms"] for f in after["frames"]]:
        failures.append("frame durations changed")
    if [f["non_cel"] for f in before["frames"]] != [f["non_cel"] for f in after["frames"]]:
        failures.append("tags or other non-cel metadata changed")
    width = before["canvas"][0]
    changed_cels = []
    for frame_index in range(before["frame_count"]):
        for layer_index, layer in enumerate(before["layers"]):
            old = before["cels"].get((frame_index, layer_index))
            new = after["cels"].get((frame_index, layer_index))
            if old is None or new is None:
                failures.append(f"missing cel at frame {frame_index + 1}, layer {layer['name']}")
                continue
            if old["geometry"] != new["geometry"]:
                failures.append(f"cel geometry changed at frame {frame_index + 1}, layer {layer['name']}")
            diffs = native_reader.changed_pixels(old["pixels"], new["pixels"])
            if diffs:
                coords = [[p % width, p // width] for p in diffs]
                changed_cels.append({
                    "frame": frame_index + 1,
                    "layer": layer["name"],
                    "pixels": coords,
                    "before_rgba": [rgba_at(old["pixels"], width, x, y) for x, y in coords],
                    "after_rgba": [rgba_at(new["pixels"], width, x, y) for x, y in coords],
                })
                if frame_index != 3 or layer["name"] != "03-shirt" or coords != EXPECTED:
                    failures.append(f"unexpected correction scope: frame {frame_index + 1}, layer {layer['name']}, {coords}")
    if len(changed_cels) != 1 or changed_cels[0].get("pixels") != EXPECTED:
        failures.append("correction did not change exactly the four declared pixels in F4")
    pass01_hash = digest(pass01_path)
    if pass01_hash != args.expected_pass01_sha256:
        failures.append("pass01 hash differs from its pre-correction hash")
    report = {
        "passed": not failures,
        "failures": failures,
        "pass01_native": str(pass01_path),
        "pass01_sha256": pass01_hash,
        "expected_pass01_sha256": args.expected_pass01_sha256,
        "corrected_native": str(corrected_path),
        "corrected_sha256": digest(corrected_path),
        "changed_cels": changed_cels,
        "correction": "At inhale peak F4, lift the existing two-pixel rose-gray shirt crease by one pixel; reuse existing palette colors.",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
