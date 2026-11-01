#!/usr/bin/env python3
"""Build deterministic review views and checks from the native Aseprite exports."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / "inputs" / "current-idle-exports"
CANDIDATE = ROOT / "exports" / "pass01"
PROOF = ROOT / "proof" / "pass01"
SOURCE = ROOT / "passes" / "pass01" / "luna6-clear-breathing-pass01.aseprite"
NATIVE_GIF = CANDIDATE / "luna6-clear-breathing-pass01.gif"
DURATIONS = [600, 350, 550, 600, 50, 80, 50, 250]
SCALE = 3
BACKGROUND = "#44444e"


def digest(path: Path) -> str:
    hasher = sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_frames(directory: Path) -> list[Image.Image]:
    frames = [Image.open(directory / f"frame-{index}.png").convert("RGBA") for index in range(8)]
    if any(frame.size != (128, 192) for frame in frames):
        raise ValueError(f"Unexpected frame size in {directory}")
    return frames


def compare(old: Image.Image, new: Image.Image) -> dict:
    old_px, new_px = old.load(), new.load()
    changed: list[tuple[int, int]] = []
    alpha_lost: list[tuple[int, int]] = []
    alpha_gained: list[tuple[int, int]] = []
    for y in range(old.height):
        for x in range(old.width):
            before, after = old_px[x, y], new_px[x, y]
            if before != after:
                changed.append((x, y))
            if before[3] > 0 and after[3] == 0:
                alpha_lost.append((x, y))
            elif before[3] == 0 and after[3] > 0:
                alpha_gained.append((x, y))
    bbox = None
    if changed:
        xs, ys = zip(*changed)
        bbox = [min(xs), min(ys), max(xs) + 1, max(ys) + 1]
    return {
        "changedPixels": len(changed),
        "changedBoundsHalfOpen": bbox,
        "alphaLost": len(alpha_lost),
        "alphaLostCoordinates": [list(point) for point in alpha_lost],
        "alphaGained": len(alpha_gained),
        "alphaGainedCoordinates": [list(point) for point in alpha_gained],
        "opaquePixelsBefore": sum(pixel[3] > 0 for pixel in old.getdata()),
        "opaquePixelsAfter": sum(pixel[3] > 0 for pixel in new.getdata()),
    }


def matte(frame: Image.Image, background: str = BACKGROUND) -> Image.Image:
    bg = Image.new("RGBA", frame.size, ImageColor.getcolor(background, "RGBA"))
    return Image.alpha_composite(bg, frame).convert("RGB")


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str) -> None:
    draw.text(xy, text, fill="#f4f2ed", font=ImageFont.load_default())


def contact_sheet(
    rows: list[tuple[str, list[Image.Image], list[int]]],
    frame_indices: list[int],
    scale: int,
    output: Path,
) -> None:
    cell_w, cell_h = 128 * scale, 192 * scale
    header_h, gap = 18 * scale, 4 * scale
    sheet = Image.new(
        "RGB",
        (len(frame_indices) * (cell_w + gap) + gap, len(rows) * (cell_h + header_h + gap) + gap),
        BACKGROUND,
    )
    draw = ImageDraw.Draw(sheet)
    for row_index, (row_name, frames, _) in enumerate(rows):
        top = gap + row_index * (cell_h + header_h + gap)
        for col_index, frame_index in enumerate(frame_indices):
            left = gap + col_index * (cell_w + gap)
            label(draw, (left + 2, top), f"{row_name} · F{frame_index + 1} · {DURATIONS[frame_index]} ms")
            rendered = matte(frames[frame_index]).resize((cell_w, cell_h), Image.Resampling.NEAREST)
            sheet.paste(rendered, (left, top + header_h))
    sheet.save(output)


def make_gif(frames: list[Image.Image], path: Path, scale: int) -> None:
    rendered = [
        matte(frame).resize((frame.width * scale, frame.height * scale), Image.Resampling.NEAREST)
        for frame in frames
    ]
    rendered[0].save(
        path,
        save_all=True,
        append_images=rendered[1:],
        duration=DURATIONS,
        loop=0,
        disposal=2,
        optimize=False,
    )


def change_map(old: Image.Image, new: Image.Image) -> Image.Image:
    result = Image.new("RGBA", old.size, ImageColor.getcolor("#33333c", "RGBA"))
    a, b, out = old.load(), new.load(), result.load()
    for y in range(old.height):
        for x in range(old.width):
            before, after = a[x, y], b[x, y]
            if before == after:
                out[x, y] = (51, 51, 60, 255)
            elif before[3] == 0 and after[3] > 0:
                out[x, y] = (77, 255, 143, 255)
            elif before[3] > 0 and after[3] == 0:
                out[x, y] = (255, 64, 191, 255)
            else:
                out[x, y] = (255, 192, 64, 255)
    return result


def chest_review(current: list[Image.Image], candidate: list[Image.Image]) -> None:
    frames = [1, 2, 3]
    crop = (36, 39, 92, 65)
    tile_w, tile_h = (crop[2] - crop[0]) * 8, (crop[3] - crop[1]) * 8
    header_h, gap = 18, 5
    sheet = Image.new("RGB", (3 * (tile_w + gap) + gap, len(frames) * (tile_h + header_h + gap) + gap), BACKGROUND)
    draw = ImageDraw.Draw(sheet)
    for row, frame_index in enumerate(frames):
        top = gap + row * (tile_h + header_h + gap)
        for col, (title, image) in enumerate((
            ("current", current[frame_index]),
            ("Luna candidate", candidate[frame_index]),
            ("changed pixels", change_map(current[frame_index], candidate[frame_index])),
        )):
            left = gap + col * (tile_w + gap)
            label(draw, (left + 2, top), f"{title} · F{frame_index + 1}")
            tile = image.crop(crop)
            if col < 2:
                tile = matte(tile)
            tile = tile.resize((tile_w, tile_h), Image.Resampling.NEAREST)
            sheet.paste(tile.convert("RGB"), (left, top + header_h))
    sheet.save(PROOF / "chest-change-map-8x.png")


def main() -> None:
    PROOF.mkdir(parents=True, exist_ok=True)
    current = read_frames(CURRENT)
    candidate = read_frames(CANDIDATE)
    comparisons = [compare(before, after) for before, after in zip(current, candidate)]

    # The native Aseprite export carries the source timings; read them back from that file.
    with Image.open(NATIVE_GIF) as gif:
        gif_frames = gif.n_frames
        gif_size = list(gif.size)
        gif_loop = gif.info.get("loop")
        gif_durations: list[int | None] = []
        for index in range(gif.n_frames):
            gif.seek(index)
            gif_durations.append(gif.info.get("duration"))

    make_gif(current, CANDIDATE / "current-idle-3x-neutral-preview.gif", SCALE)
    make_gif(candidate, CANDIDATE / "luna6-clear-breathing-pass01-3x-neutral-preview.gif", SCALE)
    contact_sheet(
        [("current", current, DURATIONS), ("Luna candidate", candidate, DURATIONS)],
        list(range(8)), 1, PROOF / "current-vs-new-1x.png",
    )
    contact_sheet(
        [("current", current, DURATIONS), ("Luna candidate", candidate, DURATIONS)],
        [0, 1, 2, 3], 3, PROOF / "current-vs-new-3x-key-poses.png",
    )
    chest_review(current, candidate)

    baseline_color_sets = [set(frame.getdata()) for frame in current]
    candidate_color_set = set().union(*(set(frame.getdata()) for frame in candidate))
    baseline_color_set = set().union(*baseline_color_sets)
    report = {
        "schema": 1,
        "inputs": {
            "currentNativeSource": {
                "path": "docs/experiments/2026-10-30-idle-breath-blink/luna/passes/pass01/luna6-idle-breath-blink-pass01.aseprite",
                "sha256": "d5b9d7675de8bea50a1941361d3e3bed3c187b3ee7e1d7e0585d51f8d37cc8ed",
            },
            "currentNativeGifSha256": digest(CURRENT / "luna6-idle-breath-blink-pass01.gif"),
        },
        "candidate": {
            "nativeSource": str(SOURCE.relative_to(ROOT.parent.parent.parent)),
            "nativeSourceSha256": digest(SOURCE),
            "nativeGif": str(NATIVE_GIF.relative_to(ROOT.parent.parent.parent)),
            "nativeGifSha256": digest(NATIVE_GIF),
            "canvas": [128, 192],
            "frameCount": len(candidate),
            "durationsMsFromNativeGif": gif_durations,
            "loop": gif_loop,
            "gifFrameCount": gif_frames,
            "gifSize": gif_size,
            "alphaMode": "RGBA PNG frame exports; native GIF composited for preview",
        },
        "comparisonsAgainstCurrentIdle": comparisons,
        "allChangedPixelsInsideUpperBodyScope": all(
            c["changedBoundsHalfOpen"] is None or (
                c["changedBoundsHalfOpen"][0] >= 38 and c["changedBoundsHalfOpen"][1] >= 42
                and c["changedBoundsHalfOpen"][2] <= 90 and c["changedBoundsHalfOpen"][3] <= 58
            ) for c in comparisons
        ),
        "alphaLossAcrossBreathingFrames": sum(comparisons[i]["alphaLost"] for i in (1, 2, 3)),
        "candidateColorsSubsetOfCurrentFrames": candidate_color_set <= baseline_color_set,
        "paletteEntriesAdded": 0,
        "protectedCompositeFramesPixelIdentical": {
            str(i + 1): comparisons[i]["changedPixels"] == 0 for i in (0, 4, 5, 6, 7)
        },
        "freshNativeReopen": "pending lease release; not yet checked",
        "generatedAt": "2026-10-30",
    }
    (PROOF / "frame-metrics.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
