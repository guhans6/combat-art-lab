#!/usr/bin/env python3
"""Confirm the isolated one-pixel local revision touched only its editable layer."""
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
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--fresh-png", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    baseline_path, revision_path, fresh_path = map(Path, (args.baseline, args.revision, args.fresh_png))
    baseline = native_reader.read_aseprite(baseline_path)
    revision = native_reader.read_aseprite(revision_path)
    failures = []
    if baseline["canvas"] != revision["canvas"] or baseline["layers"] != revision["layers"]:
        failures.append("scratch canvas or layer definitions changed")
    changed_by_layer = {}
    for index, layer in enumerate(baseline["layers"]):
        before = baseline["cels"][(0, index)]["pixels"]
        after = revision["cels"][(0, index)]["pixels"]
        diffs = native_reader.changed_pixels(before, after)
        changed_by_layer[layer["name"]] = [[p % baseline["canvas"][0], p // baseline["canvas"][0]] for p in diffs]
    if changed_by_layer.get("protected"):
        failures.append("protected layer changed")
    if changed_by_layer.get("editable") != [[12, 3]]:
        failures.append("editable layer did not change at exactly the intended one-pixel coordinate")

    width, height = baseline["canvas"]
    composite = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for index in reversed(range(len(revision["layers"]))):
        raw = revision["cels"][(0, index)]["pixels"]
        composite = Image.alpha_composite(composite, Image.frombytes("RGBA", (width, height), raw))
    fresh = Image.open(fresh_path).convert("RGBA")
    if composite.tobytes() != fresh.tobytes():
        failures.append("fresh reopen/export does not match native revision composite")

    report = {
        "passed": not failures,
        "failures": failures,
        "baseline_sha256": digest(baseline_path),
        "revision_sha256": digest(revision_path),
        "fresh_png_sha256": digest(fresh_path),
        "changed_pixels_by_layer": changed_by_layer,
        "fresh_reopen_export_matches_revision_composite": not any("fresh reopen" in f for f in failures),
        "scope": "isolated MCP capability proof; not an art deliverable",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
