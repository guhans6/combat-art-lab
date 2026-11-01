#!/usr/bin/env python3
"""Verify a duplicate-only one-pixel revision of the delivered idle native."""
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True, help="delivered animation native")
    ap.add_argument("--baseline-png", required=True, help="frozen neutral composite used to infer layer order")
    ap.add_argument("--revision", required=True, help="MCP-saved duplicate with one local edit")
    ap.add_argument("--frame", required=True, type=int, help="1-based native frame containing the edit")
    ap.add_argument("--layer", required=True, help="exact layer name edited in the duplicate")
    ap.add_argument("--x", required=True, type=int)
    ap.add_argument("--y", required=True, type=int)
    ap.add_argument("--expected-baseline-sha256", required=True,
                    help="delivered-native hash captured before making the duplicate")
    ap.add_argument("--fresh-png", required=True, help="PNG exported after fresh reopen of duplicate")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    baseline_path, baseline_png_path, revision_path, fresh_path = map(
        Path, (args.baseline, args.baseline_png, args.revision, args.fresh_png)
    )
    baseline = native_reader.read_aseprite(baseline_path)
    revision = native_reader.read_aseprite(revision_path)
    failures: list[str] = []
    if baseline["canvas"] != revision["canvas"] or baseline["depth"] != revision["depth"]:
        failures.append("duplicate canvas or color depth changed")
    if baseline["layers"] != revision["layers"]:
        failures.append("duplicate layer definitions/order/properties changed")
    if baseline["frame_count"] != revision["frame_count"]:
        failures.append("duplicate frame count changed")
    if baseline["header_tail"] != revision["header_tail"]:
        failures.append("duplicate header metadata changed")
    if [f["duration_ms"] for f in baseline["frames"]] != [f["duration_ms"] for f in revision["frames"]]:
        failures.append("duplicate frame durations changed")
    if [f["non_cel"] for f in baseline["frames"]] != [f["non_cel"] for f in revision["frames"]]:
        failures.append("duplicate tags or other non-cel metadata changed")

    changed: list[dict] = []
    width, height = baseline["canvas"]
    for frame_index in range(baseline["frame_count"]):
        for layer_index, layer in enumerate(baseline["layers"]):
            before = baseline["cels"].get((frame_index, layer_index))
            after = revision["cels"].get((frame_index, layer_index))
            if before is None or after is None:
                failures.append(f"missing resolved cel at frame {frame_index + 1}, layer {layer['name']}")
                continue
            if before["geometry"] != after["geometry"]:
                failures.append(f"cel bounds changed at frame {frame_index + 1}, layer {layer['name']}")
            diffs = native_reader.changed_pixels(before["pixels"], after["pixels"])
            if diffs:
                coords = [[p % width, p // width] for p in diffs]
                changed.append({"frame": frame_index + 1, "layer": layer["name"], "pixels": coords})

    expected = [{"frame": args.frame, "layer": args.layer, "pixels": [[args.x, args.y]]}]
    if changed != expected:
        failures.append(f"native edit scope differs from exactly the declared pixel: observed {changed!r}")
    if digest(baseline_path) != args.expected_baseline_sha256:
        failures.append("delivered baseline native hash changed during proof")

    if not 1 <= args.frame <= revision["frame_count"]:
        failures.append("declared frame is outside the duplicate")
        composite_match = False
    else:
        frame_index = args.frame - 1
        layer_by_name = {layer["name"]: i for i, layer in enumerate(revision["layers"])}
        if args.layer not in layer_by_name:
            failures.append("declared layer does not exist")
            composite_match = False
        else:
            visible_orders = [
                [i for i, layer in enumerate(baseline["layers"]) if layer["flags"] & 1],
                [i for i in reversed(range(len(baseline["layers"]))) if baseline["layers"][i]["flags"] & 1],
            ]

            def composite_at(doc: dict, frame_number: int, order: list[int]) -> Image.Image:
                image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
                for layer_index in order:
                    cel = doc["cels"].get((frame_number, layer_index))
                    if cel is None or cel["pixels"] is None:
                        continue
                    current = Image.frombytes("RGBA", (width, height), cel["pixels"])
                    opacity = doc["layers"][layer_index]["opacity"]
                    if opacity != 255:
                        current.putalpha(current.getchannel("A").point(lambda value: value * opacity // 255))
                    image = Image.alpha_composite(image, current)
                return image

            baseline_png = Image.open(baseline_png_path).convert("RGBA")
            order = next((candidate_order for candidate_order in visible_orders
                          if composite_at(baseline, 0, candidate_order).tobytes() == baseline_png.tobytes()), None)
            if order is None:
                failures.append("neither visible-layer order reproduces the frozen neutral composite")
                order = visible_orders[0]
            composite = composite_at(revision, frame_index, order)
            fresh = Image.open(fresh_path).convert("RGBA")
            composite_match = fresh.size == composite.size and fresh.tobytes() == composite.tobytes()
            if not composite_match:
                failures.append("fresh reopen/export differs from duplicate native composite")

    report = {
        "passed": not failures,
        "failures": failures,
        "baseline_native": str(baseline_path),
        "baseline_sha256": digest(baseline_path),
        "expected_baseline_sha256": args.expected_baseline_sha256,
        "revision_native": str(revision_path),
        "revision_sha256": digest(revision_path),
        "fresh_png": str(fresh_path),
        "fresh_png_sha256": digest(fresh_path),
        "baseline_png_sha256": digest(baseline_png_path),
        "declared_edit": {"frame": args.frame, "layer": args.layer, "pixel": [args.x, args.y]},
        "changed_cels": changed,
        "fresh_reopen_export_matches_revision_composite": composite_match,
        "scope": "MCP-saved duplicate-only local revision proof; delivered native remains unchanged",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
