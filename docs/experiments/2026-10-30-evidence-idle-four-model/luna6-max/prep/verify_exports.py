#!/usr/bin/env python3
"""Read-only checks for native frame exports and fresh Aseprite reopen exports."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("native_reader", HERE / "check_native_candidate.py")
native_reader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(native_reader)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def open_rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def composite_native(doc: dict, frame_index: int, order: list[int]) -> Image.Image:
    width, height = doc["canvas"]
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for layer_index in order:
        layer = doc["layers"][layer_index]
        if not (layer["flags"] & 1):
            continue
        cel = doc["cels"].get((frame_index, layer_index))
        if not cel or cel["pixels"] is None:
            continue
        current = Image.frombytes("RGBA", (width, height), cel["pixels"])
        if layer["opacity"] != 255:
            alpha = current.getchannel("A").point(lambda value: value * layer["opacity"] // 255)
            current.putalpha(alpha)
        image = Image.alpha_composite(image, current)
    return image


def frame_path(folder: Path, index: int) -> Path:
    return folder / f"idle-{index:02d}.png"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--baseline-png", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--frames", required=True)
    parser.add_argument("--fresh", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    baseline_path = Path(args.baseline)
    baseline_png_path = Path(args.baseline_png)
    candidate_path = Path(args.candidate)
    frames_dir = Path(args.frames)
    fresh_dir = Path(args.fresh)
    doc = native_reader.read_aseprite(candidate_path)
    baseline_png = open_rgba(baseline_png_path)
    width, height = doc["canvas"]
    failures: list[str] = []
    if doc["frame_count"] != 10:
        failures.append("native frame count is not 10")
    visible_orders = [
        [i for i, layer in enumerate(doc["layers"]) if layer["flags"] & 1],
        [i for i in reversed(range(len(doc["layers"]))) if doc["layers"][i]["flags"] & 1],
    ]
    composition_order = None
    for order in visible_orders:
        if composite_native(doc, 0, order).tobytes() == baseline_png.tobytes():
            composition_order = order
            break
    if composition_order is None:
        failures.append("no native layer order reproduces the frozen neutral PNG")
        composition_order = visible_orders[0]

    frame_reports = []
    source_colors: set[tuple[int, int, int, int]] = set()
    alpha_coverage: list[dict] = []
    for index in range(doc["frame_count"]):
        prior_path = frame_path(frames_dir, index)
        fresh_path = frame_path(fresh_dir, index)
        prior = open_rgba(prior_path)
        fresh = open_rgba(fresh_path)
        native = composite_native(doc, index, composition_order)
        if prior.size != (width, height) or fresh.size != (width, height):
            failures.append(f"frame {index + 1} export dimensions differ from native canvas")
        if prior.tobytes() != fresh.tobytes():
            failures.append(f"frame {index + 1} pre/post-reopen exports differ")
        if native.tobytes() != fresh.tobytes():
            failures.append(f"frame {index + 1} export differs from native cel composite")
        pixels = list(fresh.get_flattened_data())
        colors = set(pixels)
        source_colors.update(colors)
        partial_alpha = sum(1 for p in pixels if p[3] not in (0, 255))
        transparent = sum(1 for p in pixels if p[3] == 0)
        opaque = sum(1 for p in pixels if p[3] == 255)
        alpha_coverage.append({"frame": index + 1, "transparent": transparent, "opaque": opaque,
                               "partial_alpha": partial_alpha})
        frame_reports.append({"frame": index + 1, "pre_reopen_sha256": digest(prior_path),
                              "fresh_reopen_sha256": digest(fresh_path),
                              "native_composite_matches": native.tobytes() == fresh.tobytes(),
                              "unique_rgba": len(colors)})
    if open_rgba(frame_path(frames_dir, 0)).size != baseline_png.size:
        failures.append("rest frame dimensions differ from neutral export")
    if open_rgba(frame_path(frames_dir, 0)).tobytes() != baseline_png.tobytes():
        failures.append("rest frame is not pixel-identical to frozen neutral PNG")
    if any(row["partial_alpha"] for row in alpha_coverage):
        failures.append("partial alpha found in one or more candidate frames")

    report = {
        "passed": not failures,
        "failures": failures,
        "baseline_sha256": digest(baseline_path),
        "baseline_png_sha256": digest(baseline_png_path),
        "candidate_sha256": digest(candidate_path),
        "canvas": [width, height],
        "native_layer_composition_order": [doc["layers"][i]["name"] for i in composition_order],
        "distinct_rgba_across_candidate_frames": len(source_colors),
        "alpha_coverage": alpha_coverage,
        "frames": frame_reports,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
