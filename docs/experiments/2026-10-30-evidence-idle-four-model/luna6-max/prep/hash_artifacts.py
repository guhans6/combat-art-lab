#!/usr/bin/env python3
"""Hash this candidate's deliverables and the frozen inputs it references."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="luna6-max folder")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    input_paths = [
        "../inputs/neutral.aseprite", "../inputs/neutral.png",
        "../inputs/blink-source.aseprite", "../inputs/character-scene.png",
        "../inputs/character-closeup.png", "../inputs/evidence-pack.zip",
        "../inputs/video-evidence/pixel-idle-evidence-pack/motion-evidence/01-core-poses.mp4",
        "../inputs/video-evidence/pixel-idle-evidence-pack/motion-evidence/02-chest-subpixel.mp4",
        "../inputs/video-evidence/pixel-idle-evidence-pack/motion-evidence/03-arms-delay.mp4",
        "../inputs/video-evidence/pixel-idle-evidence-pack/motion-evidence/04-hair-settle.mp4",
        "../inputs/video-evidence/pixel-idle-evidence-pack/motion-evidence/05-leg-shading.mp4",
        "../inputs/video-evidence/pixel-idle-evidence-pack/motion-evidence/06-breathe-tag.mp4",
    ]
    artifacts = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.name == "artifact-hashes.json":
            continue
        artifacts[path.relative_to(root).as_posix()] = sha256(path)
    inputs = {}
    for relative in input_paths:
        path = (root / relative).resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        inputs[relative] = sha256(path)
    report = {
        "sha256": "SHA-256",
        "artifacts_relative_to_root": artifacts,
        "frozen_inputs_relative_to_root": inputs,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"artifacts": len(artifacts), "inputs": len(inputs), "out": str(out)}, indent=2))


if __name__ == "__main__":
    main()
