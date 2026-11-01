from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PASSES = ROOT / "passes"
PROOF = ROOT / "proof"
REVIEWS = ROOT / "reviews"
MATTE = (112, 112, 112, 255)
VARIANTS = ("baseline", "neutral", "subtle-smile", "surprise")
EXPECTED = {
    "neutral": {(68, 27), (69, 27)},
    "subtle-smile": {(68, 27), (69, 27), (70, 27), (69, 28)},
    "surprise": {(64, 20), (70, 20), (69, 27), (69, 28)},
}
MASKS = {
    "neutral": [(66, 26, 71, 29)],
    "subtle-smile": [(66, 26, 71, 29)],
    "surprise": [(61, 18, 74, 24), (66, 26, 71, 29)],
}
NATIVE_LAYER_DIFFS = {
    "neutral": [
        [68, 27, "#ca6a44", "#744c40"],
        [69, 27, "#e48558", "#744c40"],
    ],
    "subtle-smile": [
        [68, 27, "#ca6a44", "#744c40"],
        [69, 27, "#e48558", "#fda977"],
        [70, 27, "#fda977", "#744c40"],
        [69, 28, "#f6a26e", "#744c40"],
    ],
    "surprise": [
        [64, 20, "#d3ada7", "#fef8ee"],
        [70, 20, "#d59672", "#e7d5c7"],
        [69, 27, "#e48558", "#421e16"],
        [69, 28, "#f6a26e", "#421e16"],
    ],
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rgba(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def is_in_masks(point: tuple[int, int], boxes: list[tuple[int, int, int, int]]) -> bool:
    x, y = point
    return any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in boxes)


baseline_path = ROOT / "inputs" / "baseline.png"
baseline = rgba(baseline_path)
reports: dict[str, dict] = {}
for name in ("neutral", "subtle-smile", "surprise"):
    initial = PASSES / f"luna6-{name}.png"
    reopened = PROOF / f"luna6-{name}-reopened.png"
    native = PASSES / f"luna6-{name}.aseprite"
    scale3 = PASSES / f"luna6-{name}-3x.png"
    initial_bytes = initial.read_bytes()
    reopen_bytes = reopened.read_bytes()
    image = rgba(initial)
    reopen_image = rgba(reopened)
    if image.size != (128, 192) or reopen_image.size != (128, 192):
        raise AssertionError(f"Unexpected 1x dimensions for {name}: {image.size}, {reopen_image.size}")
    if image.tobytes() != reopen_image.tobytes():
        raise AssertionError(f"Fresh-reopen pixel mismatch for {name}")
    changed: list[list] = []
    alpha_changes = 0
    for y in range(192):
        for x in range(128):
            before, after = baseline.getpixel((x, y)), image.getpixel((x, y))
            if before != after:
                changed.append([x, y, list(before), list(after)])
                alpha_changes += before[3] != after[3]
                if not is_in_masks((x, y), MASKS[name]):
                    raise AssertionError(f"{name} changed outside mask at {(x, y)}")
    actual_points = {(entry[0], entry[1]) for entry in changed}
    if actual_points != EXPECTED[name]:
        raise AssertionError(f"Unexpected composite diff for {name}: {sorted(actual_points)}")
    if alpha_changes:
        raise AssertionError(f"Alpha changed for {name}: {alpha_changes}")
    scaled = rgba(scale3)
    if scaled.size != (384, 576):
        raise AssertionError(f"Unexpected 3x dimensions for {name}: {scaled.size}")
    if scaled.tobytes() != image.resize((384, 576), Image.Resampling.NEAREST).tobytes():
        raise AssertionError(f"3x nearest-neighbor export differs from its 1x export for {name}")
    reports[name] = {
        "nativeSha256": sha(native),
        "initialPngSha256": sha(initial),
        "reopenedPngSha256": sha(reopened),
        "threeXPngSha256": sha(scale3),
        "reopenedPngByteEqual": initial_bytes == reopen_bytes,
        "reopenedPixelsEqual": image.tobytes() == reopen_image.tobytes(),
        "dimensions1x": list(image.size),
        "dimensions3x": list(scaled.size),
        "compositeChangedPixelCount": len(changed),
        "changedPixels": changed,
        "changedPixelsAllInsideMask": True,
        "alphaChanges": alpha_changes,
        "nativeOwnerLayer": "08-hair-tie-and-hair",
        "nativeOwnerChangedPixels": NATIVE_LAYER_DIFFS[name],
        "nativeOwnerDiffMatchesCompositeCoordinates": actual_points == {(p[0], p[1]) for p in NATIVE_LAYER_DIFFS[name]},
    }

for name, path in (("baseline", baseline_path), ("approvedCloseup", ROOT / "inputs" / "character-closeup.png"), ("approvedScene", ROOT / "inputs" / "character-scene.png")):
    reports[name] = {"sha256": sha(path), "bytes": path.stat().st_size}

# True-scale 1x panels and native 3x nearest-neighbour export panels, composited
# onto a neutral gray matte so transparent RGB cannot create a false edge glow.
font = ImageFont.load_default()

def panel(image: Image.Image, label: str, pad: int) -> Image.Image:
    matte = Image.new("RGBA", image.size, MATTE)
    matte.alpha_composite(image)
    out = Image.new("RGBA", (image.width, image.height + pad), MATTE)
    out.alpha_composite(matte, (0, pad))
    ImageDraw.Draw(out).text((4, 3), label, fill=(255, 255, 255, 255), font=font)
    return out

def sheet(names: tuple[str, ...], images: list[Image.Image], pad: int, gap: int, filename: str) -> None:
    panels = [panel(im, name, pad) for name, im in zip(names, images)]
    height = max(im.height for im in panels)
    width = sum(im.width for im in panels) + gap * (len(panels) - 1)
    canvas = Image.new("RGBA", (width, height), MATTE)
    x = 0
    for im in panels:
        canvas.alpha_composite(im, (x, 0))
        x += im.width + gap
    canvas.convert("RGB").save(REVIEWS / filename)

images1x = [baseline] + [rgba(PASSES / f"luna6-{name}.png") for name in ("neutral", "subtle-smile", "surprise")]
sheet(VARIANTS, images1x, 18, 8, "fullbody-strip-1x-matte.png")
images3x = [baseline.resize((384, 576), Image.Resampling.NEAREST)] + [rgba(PASSES / f"luna6-{name}-3x.png") for name in ("neutral", "subtle-smile", "surprise")]
sheet(VARIANTS, images3x, 24, 18, "fullbody-strip-3x-matte.png")
head_box = (59, 16, 77, 33)
heads = [im.crop(head_box).resize((144, 136), Image.Resampling.NEAREST) for im in images1x]
sheet(VARIANTS, heads, 18, 8, "head-strip-8x-matte.png")
source_face = rgba(ROOT / "reviews" / "approved-closeup-face-sourcecrop.png")
cell_width, cell_height, source_label_pad, cell_gap = 300, 300, 20, 12
source_sheet = Image.new("RGBA", (cell_width * 5 + cell_gap * 4, cell_height + source_label_pad), MATTE)
source_panels = [source_face] + [h for h in heads]
source_labels = ["approved close-up source"] + [f"{name} head 8x" for name in VARIANTS]
for index, (im, label) in enumerate(zip(source_panels, source_labels)):
    x = index * (cell_width + cell_gap)
    panel_canvas = Image.new("RGBA", (cell_width, cell_height + source_label_pad), MATTE)
    panel_canvas.alpha_composite(im, ((cell_width - im.width) // 2, source_label_pad + (cell_height - im.height) // 2))
    ImageDraw.Draw(panel_canvas).text((4, 3), label, fill=(255, 255, 255, 255), font=font)
    source_sheet.alpha_composite(panel_canvas, (x, 0))
source_sheet.convert("RGB").save(REVIEWS / "approved-closeup-vs-heads-8x.png")

report = {
    "baselineSource": str(baseline_path.relative_to(ROOT)),
    "baselineSourceSha256": sha(baseline_path),
    "canvas": [128, 192],
    "nativeMetadataObservedBySpriteInfo": {
        "checkedFiles": [
            "inputs/baseline.aseprite",
            "passes/luna6-neutral.aseprite",
            "passes/luna6-subtle-smile.aseprite",
            "passes/luna6-surprise.aseprite",
        ],
        "size": [128, 192],
        "colorMode": "rgb",
        "frameCount": 1,
        "frameDurationMs": [100],
        "layerCount": 12,
        "layerNames": [
            "guide-source-seed (hidden)", "00-shoes", "01-denim", "02a-jacket-left",
            "02b-jacket-right", "03-shirt", "04-tote", "05-tote-strap",
            "06a-left-hand", "06b-right-hand", "07-face-and-neck", "08-hair-tie-and-hair",
        ],
        "allLayerAttributesEqualToBaseline": True,
        "paletteEntries": 255,
        "paletteEqualToBaseline": True,
    },
    "pixelFormatForExportDiff": "RGBA exact; no color-space conversion beyond Pillow RGBA decoding",
    "variants": reports,
    "reviewImages": {
        "fullbody1x": "reviews/fullbody-strip-1x-matte.png",
        "fullbody3x": "reviews/fullbody-strip-3x-matte.png",
        "head8x": "reviews/head-strip-8x-matte.png",
        "approvedCloseupVsHeads8x": "reviews/approved-closeup-vs-heads-8x.png",
        "matte": "#707070",
    },
}
(PROOF / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({name: {k: v for k, v in data.items() if k in ("reopenedPngByteEqual", "dimensions1x", "dimensions3x", "compositeChangedPixelCount", "changedPixelsAllInsideMask", "alphaChanges", "nativeOwnerDiffMatchesCompositeCoordinates")} for name, data in reports.items() if name in EXPECTED}, indent=2))
