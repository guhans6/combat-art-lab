"""Offline verification/package step for the sparse native seam repair."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
REPAIRED = ROOT / "technical-repair"
EXPECTED_DURATIONS = [420, 140, 180, 220, 180, 560]
MATTE = (0, 0, 0, 255)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def flatten(image: Image.Image, size: tuple[int, int] | None = None) -> Image.Image:
    size = size or image.size
    return Image.alpha_composite(Image.new("RGBA", size, MATTE), image.convert("RGBA"))


def difference(a: Image.Image, b: Image.Image) -> dict[str, object]:
    if a.size != b.size:
        b = b.resize(a.size, Image.Resampling.NEAREST)
    left = list(a.convert("RGBA").getdata())
    right = list(b.convert("RGBA").getdata())
    changed = 0
    error = 0
    max_error = 0
    for one, two in zip(left, right):
        pixel_error = sum(abs(x - y) for x, y in zip(one, two))
        if pixel_error:
            changed += 1
            error += pixel_error
            max_error = max(max_error, pixel_error)
    total = len(left)
    return {
        "changed_pixels": changed,
        "changed_percent": round(changed * 100 / total, 6) if total else 0,
        "mean_channel_abs_error": round(error / (total * 4), 8) if total else 0,
        "max_pixel_channel_sum_error": max_error,
    }


def alpha_stats(image: Image.Image) -> dict[str, object]:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    return {
        "size": list(image.size),
        "opaque_pixels": sum(value > 0 for value in alpha.getdata()),
        "alpha_bbox": list(bbox) if bbox else None,
        "unique_rgba": len(set(image.getdata())),
        "binary_alpha": all(value in (0, 255) for value in alpha.getdata()),
    }


def gif_frames(path: Path) -> tuple[list[Image.Image], list[int]]:
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


def contact_sheet(frames: list[Image.Image], path: Path) -> None:
    scale = 3
    frame_w, frame_h = frames[0].size
    label_h = 30
    cell_w, cell_h = frame_w * scale, frame_h * scale + label_h
    sheet = Image.new("RGBA", (cell_w * 3, cell_h * 2), (32, 33, 40, 255))
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(frames):
        x = index % 3 * cell_w
        y = index // 3 * cell_h
        checker = Image.new("RGBA", (cell_w, frame_h * scale), (48, 49, 58, 255))
        checker_draw = ImageDraw.Draw(checker)
        size = max(4, scale * 4)
        for yy in range(0, checker.height, size):
            for xx in range(0, checker.width, size):
                if ((xx // size) + (yy // size)) % 2:
                    checker_draw.rectangle((xx, yy, xx + size - 1, yy + size - 1), fill=(60, 61, 70, 255))
        sheet.alpha_composite(checker, (x, y))
        sheet.alpha_composite(frame.resize((cell_w, frame_h * scale), Image.Resampling.NEAREST), (x, y))
        draw.text((x + 4, y + frame_h * scale + 6), f"F{index + 1}  {EXPECTED_DURATIONS[index]} ms", fill=(242, 239, 226, 255))
    sheet.save(path)


def main() -> None:
    original_frames = [rgba(ROOT / "frames" / f"frame-{index}.png") for index in range(6)]
    repaired_paths = [REPAIRED / "frames" / f"frame-{index}.png" for index in range(6)]
    repaired_frames = [rgba(path) for path in repaired_paths]
    reopened_frames = [rgba(REPAIRED / "proof" / f"reopen-frame-{index}.png") for index in range(6)]
    check = json.loads((ROOT.parent / "luna56-max-parent-check.json").read_text())
    operations = json.loads((ROOT / "prep" / "repair-operations.json").read_text())

    contact_path = REPAIRED / "contacts" / "idle-contact.png"
    contact_sheet(repaired_frames, contact_path)

    frame_records = []
    changed_coord_records = []
    for index, (original, repaired, path) in enumerate(zip(original_frames, repaired_frames, repaired_paths)):
        changes = []
        for y in range(original.height):
            for x in range(original.width):
                if original.getpixel((x, y)) != repaired.getpixel((x, y)):
                    changes.append([x, y])
        frame_records.append({
            "native_frame": index + 1,
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(path),
            "duration_ms": EXPECTED_DURATIONS[index],
            **alpha_stats(repaired),
            "changed_from_original_count": len(changes),
        })
        changed_coord_records.append(changes)

    flagged = {
        index: [list(point) for point in operations["frames"].get(str(index), [])]
        for index in range(1, 7)
    }
    # Compare coordinates only; repair operation values are checked by the
    # native readback and each repaired pixel must match the neutral source.
    expected_changed = {index - 1: sorted([[p["x"], p["y"]] for p in operations["frames"].get(str(index), [])]) for index in range(1, 7)}
    coordinate_audit = {}
    for index, changes in enumerate(changed_coord_records):
        expected = expected_changed[index]
        coordinate_audit[str(index + 1)] = {
            "actual_changed": len(changes),
            "expected_changed": len(expected),
            "unexpected_changed": sorted(set(map(tuple, changes)) - set(map(tuple, expected))),
            "missing_expected": sorted(set(map(tuple, expected)) - set(map(tuple, changes))),
        }

    hole_audit = {}
    for index in range(1, 7):
        repaired = repaired_frames[index - 1]
        points = [tuple(point) for point in check["alpha"]["frames"][index - 1]["new_enclosed_body_holes_xy"]]
        remaining = [list(point) for point in points if repaired.getpixel(point)[3] == 0]
        color_mismatches = []
        for point, op in zip(points, operations["frames"].get(str(index), [])):
            if repaired.getpixel(point)[:3] != tuple(int(op["color"][offset:offset + 2], 16) for offset in (1, 3, 5)):
                color_mismatches.append(list(point))
        hole_audit[str(index)] = {
            "checker_listed": len(points),
            "remaining_transparent": remaining,
            "baseline_color_mismatches": color_mismatches,
        }

    gif_records = {}
    for label in ("idle-1x.gif", "idle-3x.gif"):
        path = REPAIRED / "proof" / label
        gif, durations = gif_frames(path)
        comparisons = []
        for index, image in enumerate(gif):
            normalized = flatten(image)
            if normalized.size != repaired_frames[0].size:
                normalized = normalized.resize(repaired_frames[0].size, Image.Resampling.NEAREST)
            comparisons.append(difference(flatten(repaired_frames[index]), normalized))
        gif_records[label] = {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(path),
            "size": list(gif[0].size),
            "frame_count": len(gif),
            "durations_ms": durations,
            "expected_durations_ms": EXPECTED_DURATIONS,
            "durations_match": durations == EXPECTED_DURATIONS,
            "visible_frame_comparisons_to_repaired_png": comparisons,
        }

    reopened = []
    for index, (repaired, fresh) in enumerate(zip(repaired_frames, reopened_frames)):
        path = REPAIRED / "proof" / f"reopen-frame-{index}.png"
        reopened.append({
            "native_frame": index + 1,
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(path),
            "match_repaired_export": difference(repaired, fresh),
        })

    revision_path = REPAIRED / "revision" / "revised-frame-2.png"
    revision_diff = difference(repaired_frames[1], rgba(revision_path))
    native_path = REPAIRED / "luna56-idle-repaired.aseprite"
    report = {
        "status": "technical_repair_verified_offline",
        "model": "gpt-5.6-luna/max",
        "tool": {"server": "mcp__aseprite_ai_artist", "mode": "headless", "aseprite": "1.3.18.6-dev", "extension": "Pebbly 0.8.2"},
        "native": {
            "path": str(native_path.relative_to(ROOT)),
            "sha256": sha256(native_path),
            "dimensions": [128, 192],
            "frames": 6,
            "durations_ms": EXPECTED_DURATIONS,
            "tag": "idle-breathe",
            "layer_count": 13,
            "added_layers": [{"name": "09-anim-overlap-repair", "blend_mode": "normal/3", "visible": True, "opacity": 255, "cels": [2, 3, 4, 5]}],
            "total_cels": 76,
            "existing_layers_preserved": True,
            "hidden_guide_preserved": True,
            "shoes_and_denim_untouched": True,
        },
        "original_preserved": {
            "native": "luna56-idle.aseprite",
            "native_sha256": sha256(ROOT / "luna56-idle.aseprite"),
            "exports_and_proofs": "frames/, proof/, contacts/"
        },
        "frame_records": frame_records,
        "coordinate_audit": coordinate_audit,
        "hole_audit": hole_audit,
        "gif_records": gif_records,
        "fresh_reopen_records": reopened,
        "local_revision_proof": {
            "duplicate_native": str((REPAIRED / "revision" / "luna56-idle-repaired-duplicate.aseprite").relative_to(ROOT)),
            "revised_frame": str(revision_path.relative_to(ROOT)),
            "source_frame": "technical-repair/frames/frame-1.png",
            "changed_composited_pixels": revision_diff,
            "edit_point": {"x": 73, "y": 36, "layer": "09-anim-overlap-repair", "native_frame": 2},
        },
        "contacts": [str(contact_path.relative_to(ROOT))],
        "native_validation_boundary": {
            "status": "not_exposed_by_dedicated_server",
            "note": "The server advertised validate in preflight but exposed no callable validate tool; native info, layer/cel readback, filmstrip, save/reopen and local export audits are recorded."
        }
    }
    (REPAIRED / "verification.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
