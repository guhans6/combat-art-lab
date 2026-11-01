#!/usr/bin/env python3
"""Read-only verification for the matched full-character seed comparison."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
PAIR = RUN / "rough-vs-clean-v1"
EXPECTED = {
    ROOT / "assets/references/approved-2026-10-26/character-cutout.png": "4dd54a802798adc994a14349025ab48bc5830e43507d1c1c09822de692c280b8",
    ROOT / "docs/experiments/2026-10-29-clean-cutout-conversion/inputs/clean-generated-cutout-v1.png": "12e971cc9e3cbfa7add2a17a62ff53d1f45b3c55197ce23c336a6447bed1f49e",
    PAIR / "rough-seed-128x192.png": "262dc27498c35cd13fc089149bbe426b4d805118dde38365c1407db4ecd79e5d",
    PAIR / "clean-seed-128x192.png": "aa7dbc1201f80a9908f0174a1145f868132f116b2c984162b8e5af4e83561578",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for path, expected in EXPECTED.items():
        assert sha256(path) == expected, f"hash mismatch: {path}"
    recipe = json.loads((PAIR / "recipe.json").read_text())
    assert recipe["canvas"] == [1024, 1536]
    assert recipe["grid"] == [128, 192]
    assert recipe["resample"] == "BOX" and recipe["dither"] == "none"
    assert recipe["rough"]["transform"]["mode"] == "identity"
    assert recipe["clean"]["transform"]["mode"] == "identity"
    assert recipe["rough"]["alpha"] == {"transparent": 1050098, "partial": 522766, "opaque": 0}
    assert recipe["clean"]["alpha"] == {"transparent": 1051204, "partial": 521660, "opaque": 0}
    for name in ("rough-seed-128x192.png", "clean-seed-128x192.png"):
        image = Image.open(PAIR / name).convert("RGBA")
        assert image.size == (128, 192), f"unexpected dimensions: {name}"
    print("PASS: matched full-character conversion inputs, recipe, seed dimensions, and hashes are unchanged")


if __name__ == "__main__":
    main()
