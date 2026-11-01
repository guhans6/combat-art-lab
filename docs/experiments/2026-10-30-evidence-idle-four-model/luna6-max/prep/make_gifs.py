#!/usr/bin/env python3
"""Build exact-palette neutral-matte 1x/3x GIF proofs from MCP-exported PNGs.

This reads only PNG exports, writes proof GIFs, and never reads or writes Aseprite
sources. GIF's 256-color limit is checked before encoding. Consecutive identical
frames may be merged by the encoder; verification compares the visible timeline
after coalescing identical holds.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import PIL
from PIL import Image


def coalesce(frames: list[bytes], durations: list[int]) -> tuple[list[bytes], list[int]]:
    out_frames: list[bytes] = []
    out_durations: list[int] = []
    for frame, duration in zip(frames, durations):
        if out_frames and out_frames[-1] == frame:
            out_durations[-1] += duration
        else:
            out_frames.append(frame)
            out_durations.append(duration)
    return out_frames, out_durations


def to_indexed(frames: list[bytes], size: tuple[int, int], palette_colors: list[tuple[int, int, int]]) -> list[Image.Image]:
    palette = [channel for color in palette_colors for channel in color]
    palette.extend([0] * (768 - len(palette)))
    lookup = {color: i for i, color in enumerate(palette_colors)}
    indexed = []
    for rgb in frames:
        indices = bytes(lookup[tuple(rgb[i:i + 3])] for i in range(0, len(rgb), 3))
        image = Image.frombytes("P", size, indices)
        image.putpalette(palette)
        indexed.append(image)
    return indexed


def build_and_verify(paths: list[Path], durations: list[int], output: Path,
                     matte_rgb: tuple[int, int, int], scale: int) -> dict:
    source_rgb: list[bytes] = []
    dimensions = None
    for path in paths:
        with Image.open(path) as source:
            rgba = source.convert("RGBA")
        if dimensions is None:
            dimensions = rgba.size
        if rgba.size != dimensions:
            raise ValueError(f"frame size mismatch at {path}: {rgba.size} != {dimensions}")
        background = Image.new("RGBA", rgba.size, matte_rgb + (255,))
        background.alpha_composite(rgba)
        source_rgb.append(background.convert("RGB").tobytes())
    assert dimensions is not None
    source_palette = sorted({tuple(frame[i:i + 3]) for frame in source_rgb for i in range(0, len(frame), 3)})
    if len(source_palette) > 256:
        raise ValueError(f"exact GIF proof needs {len(source_palette)} colors, exceeding the 256-color limit")

    width, height = dimensions
    scaled_size = (width * scale, height * scale)
    scaled_frames = []
    for rgb in source_rgb:
        image = Image.frombytes("RGB", dimensions, rgb)
        if scale != 1:
            image = image.resize(scaled_size, Image.Resampling.NEAREST)
        scaled_frames.append(image.tobytes())
    palette_colors = sorted({tuple(frame[i:i + 3]) for frame in scaled_frames for i in range(0, len(frame), 3)})
    if len(palette_colors) != len(source_palette):
        raise ValueError("integer enlargement unexpectedly changed the visible color set")
    indexed = to_indexed(scaled_frames, scaled_size, palette_colors)
    output.parent.mkdir(parents=True, exist_ok=True)
    indexed[0].save(
        output,
        save_all=True,
        append_images=indexed[1:],
        duration=durations,
        loop=0,
        optimize=False,
        disposal=2,
    )

    with Image.open(output) as gif:
        actual_frames = []
        actual_durations = []
        for i in range(gif.n_frames):
            gif.seek(i)
            actual_frames.append(gif.convert("RGB").tobytes())
            actual_durations.append(int(gif.info.get("duration", 0)))
    expected_coalesced = coalesce(scaled_frames, durations)
    actual_coalesced = coalesce(actual_frames, actual_durations)
    pixels_equal = actual_coalesced[0] == expected_coalesced[0]
    timing_equal = actual_coalesced[1] == expected_coalesced[1]
    if not pixels_equal or not timing_equal:
        raise ValueError({
            "scale": scale,
            "pixels_equal": pixels_equal,
            "timing_equal": timing_equal,
            "expected_durations_after_identical_hold_merge": expected_coalesced[1],
            "actual_durations_after_identical_hold_merge": actual_coalesced[1],
            "expected_frame_count_after_merge": len(expected_coalesced[0]),
            "actual_frame_count_after_merge": len(actual_coalesced[0]),
        })
    decoded_palette = {tuple(actual_frames[j][i:i + 3]) for j in range(len(actual_frames))
                       for i in range(0, len(actual_frames[j]), 3)}
    if decoded_palette != set(source_palette):
        raise ValueError(f"decoded GIF color table does not preserve exact visible colors at {scale}x")
    return {
        "gif": str(output),
        "dimensions": list(scaled_size),
        "source_frame_count": len(paths),
        "decoded_frame_count": len(actual_frames),
        "decoded_frame_count_after_identical_hold_merge": len(actual_coalesced[0]),
        "decoded_durations_ms_after_identical_hold_merge": actual_coalesced[1],
        "visible_color_count": len(source_palette),
        "decoded_pixels_exact": True,
        "decoded_timeline_exact_after_hold_merge": True,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames-json", required=True, help="JSON array of ordered MCP-exported PNG paths")
    ap.add_argument("--durations-json", required=True, help="JSON array of ordered millisecond durations")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--matte", default="808080", help="neutral matte RGB as six hex digits")
    ap.add_argument("--report", required=True)
    args = ap.parse_args()
    paths = [Path(p) for p in json.loads(Path(args.frames_json).read_text())]
    durations = json.loads(Path(args.durations_json).read_text())
    if not paths or len(paths) != len(durations):
        raise ValueError("frame paths and durations must be non-empty arrays of equal length")
    if any(d <= 0 or d % 10 for d in durations):
        raise ValueError("GIF durations must be positive multiples of 10 ms")
    matte_hex = args.matte.lstrip("#")
    if len(matte_hex) != 6:
        raise ValueError("matte must contain exactly six hex digits")
    matte_rgb = tuple(int(matte_hex[i:i + 2], 16) for i in (0, 2, 4))
    out_dir = Path(args.out_dir)
    report = {
        "input_frames": [str(p) for p in paths],
        "durations_ms": durations,
        "matte_rgb": list(matte_rgb),
        "pillow_version": PIL.__version__,
        "scales": {},
    }
    for scale in (1, 3):
        report["scales"][str(scale)] = build_and_verify(
            paths, durations, out_dir / f"idle-neutral-{scale}x.gif", matte_rgb, scale
        )
    Path(args.report).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
