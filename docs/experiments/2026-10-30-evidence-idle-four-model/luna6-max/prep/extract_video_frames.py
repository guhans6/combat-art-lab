#!/usr/bin/env python3
"""Extract selected stills from the frozen idle workflow evidence clips.

This is read-only with respect to the shared input pack. Outputs are kept in this
artist's prep folder and are observations only; they are not sprite source pixels.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "inputs" / "video-evidence" / "pixel-idle-evidence-pack"
OUT = Path(__file__).parent / "video-frames"

# clip file, evidence ID, absolute source interval start, selected clip-relative times
SAMPLES = [
    ("01-core-poses.mp4", "clip-01-core-poses", 304, [1.0, 5.0, 10.0]),
    ("02-chest-subpixel.mp4", "clip-02-chest-subpixel", 414, [3.0, 11.0, 20.0]),
    ("03-arms-delay.mp4", "clip-03-arms-delay", 614, [4.0, 12.0]),
    ("04-hair-settle.mp4", "clip-04-hair-settle", 727, [5.0, 15.0]),
    ("05-leg-shading.mp4", "clip-05-leg-shading", 866, [4.0, 14.0]),
    ("06-breathe-tag.mp4", "clip-06-breathe-tag", 946, [4.0, 18.0]),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for filename, evidence_id, source_start, offsets in SAMPLES:
        clip = PACK / "motion-evidence" / filename
        for offset in offsets:
            out = OUT / f"{evidence_id}-local-{offset:05.1f}s.jpg"
            subprocess.run(
                [
                    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-i", str(clip), "-ss", f"{offset:.3f}", "-frames:v", "1",
                    "-fps_mode", "passthrough", "-q:v", "2", str(out),
                ],
                check=True,
            )
            records.append(
                {
                    "evidence_id": evidence_id,
                    "source_clip": str(clip.relative_to(ROOT)),
                    "clip_relative_seconds": offset,
                    "source_video_seconds": source_start + offset,
                    "still": str(out.relative_to(ROOT)),
                    "sha256": sha256(out),
                }
            )
    (OUT / "index.json").write_text(
        json.dumps(
            {
                "purpose": "visual preparation only; extracted from re-encoded source excerpts",
                "samples": records,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
