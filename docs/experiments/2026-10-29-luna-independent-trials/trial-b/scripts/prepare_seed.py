#!/usr/bin/env python3
"""Build a binary-alpha, palette-reduced 128x192 seed from the frozen source."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


REPO = Path(__file__).resolve().parents[5]
TRIAL = Path(__file__).resolve().parents[1]
INPUT_DIR = TRIAL / "input"
PREP_DIR = TRIAL / "prep"
SOURCE = REPO / "docs/experiments/2026-10-29-clean-cutout-conversion/inputs/clean-generated-cutout-v1.png"
SCENE = REPO / "assets/references/approved-2026-10-26/character-scene.png"
CLOSEUP = REPO / "assets/references/approved-2026-10-26/character-closeup.png"

EXPECTED_HASHES = {
    "source-cutout.png": "12e971cc9e3cbfa7add2a17a62ff53d1f45b3c55197ce23c336a6447bed1f49e",
    "character-scene.png": "a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae",
    "character-closeup.png": "0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7",
}

CANVAS = (128, 192)
SOURCE_ALPHA_THRESHOLD = 32
AREA_COVERAGE_THRESHOLD = 128
PALETTE_SIZE = 40


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_frozen_inputs() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    copies = {
        "source-cutout.png": SOURCE,
        "character-scene.png": SCENE,
        "character-closeup.png": CLOSEUP,
    }
    for name, original in copies.items():
        actual = sha256(original)
        if actual != EXPECTED_HASHES[name]:
            raise SystemExit(f"Input hash changed for {original}: {actual}")
        destination = INPUT_DIR / name
        if destination.exists() and sha256(destination) != actual:
            raise SystemExit(f"Refusing to overwrite changed frozen input: {destination}")
        if not destination.exists():
            shutil.copyfile(original, destination)


def build_seed() -> dict[str, object]:
    PREP_DIR.mkdir(parents=True, exist_ok=True)
    source = Image.open(INPUT_DIR / "source-cutout.png").convert("RGBA")
    if source.size != (1024, 1536):
        raise SystemExit(f"Unexpected source dimensions: {source.size}")

    # Preserve the source's full framing. Remove only its faint alpha fringe,
    # area-sample 8:1 in premultiplied-alpha space, then make coverage binary.
    source_mask = source.getchannel("A").point(
        lambda value: 255 if value >= SOURCE_ALPHA_THRESHOLD else 0
    )
    thresholded = source.copy()
    thresholded.putalpha(source_mask)
    resized_premultiplied = thresholded.convert("RGBa").resize(
        CANVAS, Image.Resampling.BOX
    )
    resized = resized_premultiplied.convert("RGBA")
    coverage = source_mask.resize(CANVAS, Image.Resampling.BOX)
    binary_alpha = coverage.point(
        lambda value: 255 if value >= AREA_COVERAGE_THRESHOLD else 0
    )

    # Median-cut is used without dithering so the export stays cluster-based.
    # Transparent pixels do not participate in palette selection or output.
    resized_rgb = resized.convert("RGB")
    visible_rgb = [
        color
        for color, alpha in zip(resized_rgb.getdata(), binary_alpha.getdata())
        if alpha == 255
    ]
    sample = Image.new("RGB", (len(visible_rgb), 1))
    sample.putdata(visible_rgb)
    palette = sample.quantize(
        colors=PALETTE_SIZE,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )
    quantized = resized_rgb.quantize(palette=palette, dither=Image.Dither.NONE).convert("RGB")
    seed = quantized.convert("RGBA")
    seed.putalpha(binary_alpha)
    seed_path = PREP_DIR / "seed-128x192.png"
    seed.save(seed_path)

    zoom = seed.resize((CANVAS[0] * 4, CANVAS[1] * 4), Image.Resampling.NEAREST)
    zoom.save(PREP_DIR / "seed-128x192-4x.png")

    opaque = binary_alpha.histogram()[255]
    report: dict[str, object] = {
        "method": "source-assisted reconstruction seed",
        "inputs": {
            "source": "input/source-cutout.png",
            "source_sha256": sha256(INPUT_DIR / "source-cutout.png"),
            "scene_reference": "input/character-scene.png",
            "scene_sha256": sha256(INPUT_DIR / "character-scene.png"),
            "closeup_reference": "input/character-closeup.png",
            "closeup_sha256": sha256(INPUT_DIR / "character-closeup.png"),
        },
        "canvas": list(CANVAS),
        "source_crop": [0, 0, 1024, 1536],
        "source_alpha_threshold": SOURCE_ALPHA_THRESHOLD,
        "resampling": "8:1 BOX in premultiplied-alpha space",
        "native_alpha": f"binary; area coverage >= {AREA_COVERAGE_THRESHOLD}",
        "palette": {
            "method": "Pillow MEDIANCUT",
            "colors": PALETTE_SIZE,
            "dither": "none",
        },
        "seed_path": "prep/seed-128x192.png",
        "seed_sha256": sha256(seed_path),
        "visible_pixels": opaque,
        "visible_bbox": binary_alpha.getbbox(),
    }
    (PREP_DIR / "recipe.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main() -> None:
    copy_frozen_inputs()
    print(json.dumps(build_seed(), indent=2))


if __name__ == "__main__":
    main()
