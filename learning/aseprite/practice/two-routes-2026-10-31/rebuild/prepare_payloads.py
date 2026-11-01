#!/usr/bin/env python3
"""Build deterministic Aseprite grid payloads from the copied pose inputs.

This preparation deliberately creates JSON only.  It never exports PNGs, GIFs, or
native sprite files; the caller decides how to paint these draft cells in Aseprite.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

import PIL
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "inputs"
PAYLOADS = ROOT / "payloads"
MANIFEST = ROOT / "manifest.json"
WIDTH = HEIGHT = 128
SOURCE_SIZE = (1448, 1086)
SCALE_NUMERATOR, SCALE_DENOMINATOR = 3, 32
TX, TY = -4, 8
ALPHA_THRESHOLD = 128
SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcde"
PHASES = ("neutral", "straplift", "grip", "windup", "swing", "recovery")
DURATIONS_MS = (600, 250, 250, 350, 150, 400)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bounds(points: list[tuple[int, int]]) -> list[int] | None:
    if not points:
        return None
    xs, ys = zip(*points)
    return [min(xs), min(ys), max(xs), max(ys)]


def rgba_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def sample_source(image: Image.Image) -> tuple[list[tuple[int, int, int, int]], dict]:
    """Nearest-center sample with one fixed transform for every pose."""
    pixels = image.load()
    sampled: list[tuple[int, int, int, int]] = []
    opaque_points: list[tuple[int, int]] = []
    for y in range(HEIGHT):
        sy = ((y + 0.5 - TY) * SCALE_DENOMINATOR) // SCALE_NUMERATOR
        for x in range(WIDTH):
            sx = ((x + 0.5 - TX) * SCALE_DENOMINATOR) // SCALE_NUMERATOR
            if 0 <= sx < image.width and 0 <= sy < image.height:
                red, green, blue, alpha = pixels[int(sx), int(sy)]
            else:
                red = green = blue = alpha = 0
            if alpha >= ALPHA_THRESHOLD:
                sampled.append((red, green, blue, 255))
                opaque_points.append((x, y))
            else:
                sampled.append((0, 0, 0, 0))
    return sampled, {
        "opaque_pixels": len(opaque_points),
        "alpha_ge_128_bounds_xyxy": bounds(opaque_points),
    }


def source_alpha_stats(image: Image.Image) -> dict:
    points = [
        (x, y)
        for y in range(image.height)
        for x in range(image.width)
        if image.getpixel((x, y))[3] >= ALPHA_THRESHOLD
    ]
    return {
        "opaque_pixels": len(points),
        "alpha_ge_128_bounds_xyxy": bounds(points),
    }


def derive_palette(samples: list[list[tuple[int, int, int, int]]]) -> list[tuple[int, int, int]]:
    pooled_rgb = [pixel[:3] for frame in samples for pixel in frame if pixel[3] == 255]
    if len(pooled_rgb) < 31:
        raise ValueError("Need at least 31 opaque pooled samples for the shared palette")
    pooled = Image.new("RGB", (len(pooled_rgb), 1))
    pooled.putdata(pooled_rgb)
    reduced = pooled.quantize(colors=31, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    # The first 31 palette entries are the MEDIANCUT representative colors.
    raw = reduced.getpalette()[: 31 * 3]
    palette = [tuple(raw[index : index + 3]) for index in range(0, len(raw), 3)]
    if len(palette) != 31 or len(set(palette)) != 31:
        raise ValueError("MEDIANCUT did not produce 31 distinct opaque representative colors")
    return palette


def nearest_palette_index(rgb: tuple[int, int, int], palette: list[tuple[int, int, int]]) -> int:
    return min(
        range(len(palette)),
        key=lambda index: sum((rgb[channel] - palette[index][channel]) ** 2 for channel in range(3)),
    )


def grid_payload(sampled: list[tuple[int, int, int, int]], palette: list[tuple[int, int, int]]) -> tuple[dict, bytes, int]:
    legend = {".": None}
    legend.update({symbol: rgba_hex(color) for symbol, color in zip(SYMBOLS, palette, strict=True)})
    rows: list[str] = []
    rebuilt = bytearray()
    opaque = 0
    for y in range(HEIGHT):
        row: list[str] = []
        for x in range(WIDTH):
            red, green, blue, alpha = sampled[y * WIDTH + x]
            if alpha == 0:
                row.append(".")
                rebuilt.extend((0, 0, 0, 0))
            else:
                index = nearest_palette_index((red, green, blue), palette)
                color = palette[index]
                row.append(SYMBOLS[index])
                rebuilt.extend((*color, 255))
                opaque += 1
        rows.append("".join(row))
    return {"kind": "grid", "x": 0, "y": 0, "legend": legend, "rows": rows, "transparent": "erase"}, bytes(rebuilt), opaque


def main() -> None:
    PAYLOADS.mkdir(parents=True, exist_ok=True)
    input_paths = [INPUTS / f"pose-{number:02d}.png" for number in range(1, 7)]
    source_records: list[dict] = []
    sampled_frames: list[list[tuple[int, int, int, int]]] = []
    sampled_stats: list[dict] = []
    for input_path in input_paths:
        encoded = input_path.read_bytes()
        with Image.open(input_path) as source:
            if source.mode != "RGBA":
                raise ValueError(f"{input_path.name}: expected RGBA input, got {source.mode}")
            image = source.copy()
        if image.size != SOURCE_SIZE:
            raise ValueError(f"{input_path.name}: expected {SOURCE_SIZE}, got {image.size}")
        sampled, destination_stats = sample_source(image)
        sampled_frames.append(sampled)
        sampled_stats.append(destination_stats)
        source_records.append({
            "file": f"inputs/{input_path.name}",
            "sha256": sha256(encoded),
            "dimensions": [image.width, image.height],
            "mode": "RGBA",
            "before_alpha_ge_128": source_alpha_stats(image),
        })

    palette = derive_palette(sampled_frames)
    palette_json = ["#00000000", *[rgba_hex(color) for color in palette]]
    (PAYLOADS / "palette.json").write_text(json.dumps(palette_json, indent=2) + "\n", encoding="utf-8")

    frame_records: list[dict] = []
    for index, (sampled, destination_stats) in enumerate(zip(sampled_frames, sampled_stats, strict=True), start=1):
        payload, canonical_rgba, opaque = grid_payload(sampled, palette)
        payload_name = f"pose-{index:02d}.json"
        (PAYLOADS / payload_name).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        frame_records.append({
            "pose": index,
            "phase": PHASES[index - 1],
            "duration_ms": DURATIONS_MS[index - 1],
            "payload": f"payloads/{payload_name}",
            "after_alpha_ge_128": {
                **destination_stats,
                "draft_pixel_hash_canonical_rgba_sha256": sha256(canonical_rgba),
                "draft_pixel_count": opaque,
            },
        })

    manifest = {
        "format": "aseprite-grid-payload-preparation/v1",
        "purpose": "deterministic automatic draft preparation for later native Aseprite cleanup",
        "inputs": source_records,
        "destination": {"dimensions": [WIDTH, HEIGHT], "mode": "RGBA"},
        "alpha": {
            "threshold": "alpha >= 128 becomes opaque alpha 255; alpha < 128 becomes transparent",
            "rgb_hue_deletion": "none",
            "before": "source alpha >= 128 statistics are recorded per input",
            "after": "post-sample/post-palette canonical RGBA statistics are recorded per frame",
        },
        "transform": {
            "source_to_target_scale": [SCALE_NUMERATOR, SCALE_DENOMINATOR],
            "translation_xy": [TX, TY],
            "sampling": "nearest-center: sx=floor((x+0.5-tx)/s), sy=floor((y+0.5-ty)/s); out-of-bounds transparent",
            "per_frame_fitting": False,
        },
        "shared_palette": {
            "payload": "payloads/palette.json",
            "colors_total": 32,
            "opaque_color_count": 31,
            "native_palette_index_0": "#00000000",
            "recipe": "pooled post-threshold RGB samples from all six destinations; Pillow MEDIANCUT colors=31, no dither; each opaque draft pixel maps to the shared palette by minimum squared RGB distance, lowest index on ties",
            "pillow_version": PIL.__version__,
        },
        "frames": frame_records,
        "study": {
            "kind": "pose study, not a full attack",
            "phases": list(PHASES),
            "durations_ms": list(DURATIONS_MS),
            "scope": "automatic draft only; colored opaque edge artifacts may remain for user cleanup",
            "excluded": ["AI artistic pixel correction", "inbetweens", "game approval", "derived PNG/GIF/sprite export"],
            "study_budget": "one preparation pass plus one parameter repair if wrong",
            "trial_actor": "93-97",
            "supersedes": "draft 183 high is irrelevant to this new trial",
        },
        "rebuild": {
            "command": f"{sys.executable} rebuild/prepare_payloads.py",
            "python": platform.python_version(),
            "outputs": ["payloads/palette.json", *[f"payloads/pose-{number:02d}.json" for number in range(1, 7)], "manifest.json"],
            "exports_images": False,
        },
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
