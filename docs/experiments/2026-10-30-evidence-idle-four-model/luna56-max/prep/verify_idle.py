"""Offline proof packaging for the native Luna56Max idle export.

The sprite and its exports were authored/exported through the dedicated
Aseprite MCP.  This script only reads those outputs and writes derived proof
artifacts: contact sheets and a compact verification report.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageChops, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
FRAME_DIR = ROOT / "frames"
PROOF_DIR = ROOT / "proof"
CONTACT_DIR = ROOT / "contacts"
EXPECTED_DURATIONS = [420, 140, 180, 220, 180, 560]
MATTE = (54, 55, 64, 255)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def alpha_stats(image: Image.Image) -> dict[str, object]:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    opaque = sum(value > 0 for value in alpha.getdata())
    unique = len(set(image.getdata()))
    return {
        "size": list(image.size),
        "opaque_pixels": opaque,
        "alpha_bbox": list(bbox) if bbox else None,
        "unique_rgba": unique,
    }


def flatten(image: Image.Image, size: tuple[int, int] | None = None) -> Image.Image:
    if size is None:
        size = image.size
    background = Image.new("RGBA", size, MATTE)
    return Image.alpha_composite(background, image.convert("RGBA"))


def difference(a: Image.Image, b: Image.Image) -> dict[str, object]:
    if a.size != b.size:
        b = b.resize(a.size, Image.Resampling.NEAREST)
    aa = list(a.convert("RGBA").getdata())
    bb = list(b.convert("RGBA").getdata())
    changed = 0
    total_error = 0
    max_error = 0
    for left, right in zip(aa, bb):
        error = sum(abs(x - y) for x, y in zip(left, right))
        if error:
            changed += 1
            total_error += error
            max_error = max(max_error, error)
    total = len(aa)
    return {
        "changed_pixels": changed,
        "changed_percent": round(changed * 100 / total, 4) if total else 0,
        "mean_channel_abs_error": round(total_error / (total * 4), 6) if total else 0,
        "max_pixel_channel_sum_error": max_error,
    }


def gif_frames(path: Path) -> tuple[Image.Image, list[int]]:
    source = Image.open(path)
    frames: list[Image.Image] = []
    durations: list[int] = []
    index = 0
    while True:
        frames.append(source.convert("RGBA"))
        durations.append(int(source.info.get("duration") or 0))
        index += 1
        try:
            source.seek(index)
        except EOFError:
            break
    return frames, durations


def checkerboard(size: tuple[int, int], cell: int = 8) -> Image.Image:
    image = Image.new("RGBA", size, (48, 49, 58, 255))
    draw = ImageDraw.Draw(image)
    colors = ((48, 49, 58, 255), (60, 61, 70, 255))
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=colors[((x // cell) + (y // cell)) % 2])
    return image


def contact_sheet(frames: list[Image.Image], path: Path, scale: int = 3) -> None:
    frame_w, frame_h = frames[0].size
    label_h = 30
    cell_w, cell_h = frame_w * scale, frame_h * scale + label_h
    sheet = Image.new("RGBA", (cell_w * 3, cell_h * 2), (32, 33, 40, 255))
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(frames):
        x = (index % 3) * cell_w
        y = (index // 3) * cell_h
        background = checkerboard((frame_w * scale, frame_h * scale), cell=max(4, scale * 4))
        enlarged = frame.resize((frame_w * scale, frame_h * scale), Image.Resampling.NEAREST)
        sheet.alpha_composite(background, (x, y))
        sheet.alpha_composite(enlarged, (x, y))
        draw.text((x + 4, y + frame_h * scale + 6), f"F{index + 1}  {EXPECTED_DURATIONS[index]} ms", fill=(242, 239, 226, 255))
    sheet.save(path)


def main() -> None:
    CONTACT_DIR.mkdir(parents=True, exist_ok=True)
    frame_paths = [FRAME_DIR / f"frame-{index}.png" for index in range(6)]
    frames = [rgba(path) for path in frame_paths]
    contact_sheet(frames, CONTACT_DIR / "idle-contact.png", scale=3)
    contact_sheet(frames, CONTACT_DIR / "idle-contact-1x.png", scale=1)

    frame_records = []
    for index, (path, image, duration) in enumerate(zip(frame_paths, frames, EXPECTED_DURATIONS)):
        frame_records.append(
            {
                "native_frame": index + 1,
                "path": str(path.relative_to(ROOT)),
                "duration_ms": duration,
                "sha256": sha256(path),
                **alpha_stats(image),
            }
        )

    gif_records: dict[str, object] = {}
    for label in ("idle-1x.gif", "idle-3x.gif"):
        path = PROOF_DIR / label
        gif, durations = gif_frames(path)
        visible_source = [flatten(frame) for frame in frames]
        comparisons = []
        for index, image in enumerate(gif):
            normalized = flatten(image)
            if image.size != frames[0].size:
                normalized = normalized.resize(frames[0].size, Image.Resampling.NEAREST)
            comparisons.append(difference(visible_source[index], normalized))
        gif_records[label] = {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(path),
            "size": list(gif[0].size),
            "frame_count": len(gif),
            "durations_ms": durations,
            "expected_durations_ms": EXPECTED_DURATIONS,
            "durations_match": durations == EXPECTED_DURATIONS,
            "visible_frame_comparisons_to_native": comparisons,
        }

    reopened = []
    for index, original in enumerate(frames):
        path = PROOF_DIR / f"reopen-frame-{index}.png"
        image = rgba(path)
        reopened.append(
            {
                "native_frame": index + 1,
                "path": str(path.relative_to(ROOT)),
                "sha256": sha256(path),
                "match_exported_frame": difference(original, image),
            }
        )

    revision_source = frames[2]
    revision_path = ROOT / "revision" / "revised-frame-3.png"
    revision_image = rgba(revision_path)

    report = {
        "status": "verified_offline_exports",
        "native_dimensions": [128, 192],
        "expected_durations_ms": EXPECTED_DURATIONS,
        "total_duration_ms": sum(EXPECTED_DURATIONS),
        "frame_count": len(frames),
        "frame_records": frame_records,
        "gif_records": gif_records,
        "fresh_reopen_records": reopened,
        "local_revision_proof": {
            "duplicate_native": "revision/luna56-idle-duplicate.aseprite",
            "revised_frame": "revision/revised-frame-3.png",
            "source_frame_compared": "frames/frame-2.png",
            "changed_composited_pixels": difference(revision_source, revision_image),
            "edit_point": {"x": 55, "y": 39, "layer": "03-shirt", "native_frame": 3},
        },
        "native_validation_boundary": {
            "status": "not_exposed_by_dedicated_server",
            "note": "The preflight feature list advertised validate, but no callable validate tool was exposed in this session; sprite_info, tag/cel lists, read_pixels, look filmstrip/ascii, save/reopen and local export comparisons were used instead.",
        },
        "contacts": ["contacts/idle-contact.png", "contacts/idle-contact-1x.png"],
    }
    (ROOT / "verification.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
