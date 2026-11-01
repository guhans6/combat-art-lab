"""Build visual proof only from Aseprite MCP exports; never edits sprite artwork."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PASS = sys.argv[1] if len(sys.argv) > 1 else ""
EXPORTS = ROOT / "exports" / PASS if PASS else ROOT / "exports"
PROOF = ROOT / "proof" / PASS if PASS else ROOT / "proof"
DURATIONS = [600, 350, 550, 600, 50, 80, 50, 250]
BACKGROUND = (55, 57, 66, 255)


def load_series(folder: Path, stem: str) -> list[Image.Image]:
    return [Image.open(folder / f"{stem}-{index}.png").convert("RGBA") for index in range(8)]


def difference(a: Image.Image, b: Image.Image) -> dict[str, object]:
    pa, pb = a.load(), b.load()
    changed = [
        (x, y)
        for y in range(a.height)
        for x in range(a.width)
        if pa[x, y] != pb[x, y]
    ]
    if not changed:
        return {"pixels": 0, "bounds": None}
    xs, ys = zip(*changed)
    return {
        "pixels": len(changed),
        "bounds": [min(xs), min(ys), max(xs) + 1, max(ys) + 1],
    }


def main() -> None:
    frames = load_series(EXPORTS, "frame")
    reopened = load_series(PROOF, "reopened")
    shoes = load_series(PROOF, "shoes")
    denim = load_series(PROOF, "denim")
    face_neck = load_series(PROOF, "face-neck")
    head = load_series(PROOF, "head")
    assert all(image.size == (128, 192) for image in frames)

    # The transparent horizontal strip is a layout of the original native exports.
    strip = Image.new("RGBA", (128 * 8, 192), (0, 0, 0, 0))
    for i, frame in enumerate(frames):
        strip.alpha_composite(frame, (i * 128, 0))
    strip.save(EXPORTS / "idle-transparent-strip.png")

    # A legible review sheet on a neutral matte, enlarged with nearest-neighbour only.
    scale, columns, gap, label_h = 3, 4, 12, 22
    cell_w, cell_h = 128 * scale, 192 * scale
    sheet = Image.new(
        "RGBA",
        (gap + columns * (cell_w + gap), gap + 2 * (cell_h + label_h + gap)),
        BACKGROUND,
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for i, frame in enumerate(frames):
        x = gap + (i % columns) * (cell_w + gap)
        y = gap + (i // columns) * (cell_h + label_h + gap)
        enlarged = frame.resize((cell_w, cell_h), Image.Resampling.NEAREST)
        matte = Image.new("RGBA", enlarged.size, BACKGROUND)
        matte.alpha_composite(enlarged)
        sheet.alpha_composite(matte, (x, y))
        draw.text((x, y + cell_h + 3), f"F{i + 1}  {DURATIONS[i]} ms", fill=(240, 240, 240, 255), font=font)
    sheet.save(PROOF / "contact-sheet-neutral-3x.png")

    # Playback preview from native frame exports and Aseprite-recorded timings.
    enlarged_matte_frames = []
    for frame in frames:
        enlarged = frame.resize((128 * scale, 192 * scale), Image.Resampling.NEAREST)
        matte = Image.new("RGBA", enlarged.size, BACKGROUND)
        matte.alpha_composite(enlarged)
        enlarged_matte_frames.append(matte.convert("RGB"))
    enlarged_matte_frames[0].save(
        EXPORTS / "idle-neutral-3x-preview.gif",
        save_all=True,
        append_images=enlarged_matte_frames[1:],
        duration=DURATIONS,
        loop=0,
        disposal=2,
        optimize=False,
    )

    base = frames[0]
    composite_diffs = [difference(base, frame) for frame in frames]
    alpha_lost = []
    composite_outside_motion = []
    for frame in frames[1:]:
        lost = 0
        outside = 0
        for y in range(192):
            for x in range(128):
                before, after = base.getpixel((x, y)), frame.getpixel((x, y))
                if before[3] and not after[3]:
                    lost += 1
                if before != after:
                    body = 39 <= x < 89 and 42 <= y < 57
                    eyes = (62 <= x < 67 and 20 <= y < 24) or (70 <= x < 73 and 20 <= y < 22)
                    if not body and not eyes:
                        outside += 1
        alpha_lost.append(lost)
        composite_outside_motion.append(outside)
    head_diffs = [difference(head[0], frame) for frame in head]
    outside_eye = []
    for frame in head[1:]:
        changed_outside = 0
        for y in range(192):
            for x in range(128):
                if head[0].getpixel((x, y)) == frame.getpixel((x, y)):
                    continue
                allowed = (62 <= x < 67 and 20 <= y < 24) or (70 <= x < 73 and 20 <= y < 22)
                if not allowed:
                    changed_outside += 1
        outside_eye.append(changed_outside)

    native_name = f"luna6-idle-breath-blink-{PASS}.gif" if PASS else "luna6-idle-breath-blink.gif"
    native_gif = Image.open(EXPORTS / native_name)
    gif_durations = []
    for i in range(native_gif.n_frames):
        native_gif.seek(i)
        gif_durations.append(native_gif.info.get("duration"))

    metrics = {
        "canvas": [128, 192],
        "frameCount": len(frames),
        "timingMs": DURATIONS,
        "totalMs": sum(DURATIONS),
        "nativeGifSize": list(native_gif.size),
        "nativeGifLoop": native_gif.info.get("loop"),
        "nativeGifDurationsMs": gif_durations,
        "reopenedFrameExportsPixelIdentical": all(a.tobytes() == b.tobytes() for a, b in zip(frames, reopened)),
        "compositeAlphaPixelsLostFromFrame1ByFrame2to8": alpha_lost,
        "compositeChangedPixelsOutsideBodyAndEyeMasksByFrame2to8": composite_outside_motion,
        "allShoeLayerFramesPixelIdentical": all(shoes[0].tobytes() == frame.tobytes() for frame in shoes[1:]),
        "allDenimLayerFramesPixelIdentical": all(denim[0].tobytes() == frame.tobytes() for frame in denim[1:]),
        "allFaceNeckLayerFramesPixelIdentical": all(face_neck[0].tobytes() == frame.tobytes() for frame in face_neck[1:]),
        "headLayerDiffsFromFrame1": head_diffs,
        "headChangedPixelsOutsideRegisteredEyeMasksByFrame2to8": outside_eye,
        "compositeDiffsFromFrame1": composite_diffs,
        "transparentStrip": str(EXPORTS / "idle-transparent-strip.png"),
        "neutralContactSheet": str(PROOF / "contact-sheet-neutral-3x.png"),
        "neutralPreviewGif": str(EXPORTS / "idle-neutral-3x-preview.gif"),
    }
    (PROOF / "frame-metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
