"""Inspect real Aseprite exports and build comparison boards; never draws the sprite.

Requires Pillow, available in this machine's bundled Codex Python runtime.
Reference reduction is used only in clearly labeled comparison panels.
"""
from pathlib import Path
from collections import deque
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
EXPORT = ROOT / "assets/export/standing-v02"
PREVIEW = ROOT / "assets/previews/standing-v02"
RECORD = ROOT / "docs/experiments/2026-10-26-standing-refinement"
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"

def font(size):
    return ImageFont.truetype(FONT_PATH, size)

def backed(im, color="#343342"):
    bg = Image.new("RGBA", im.size, color)
    bg.alpha_composite(im)
    return bg.convert("RGB")

sprite = Image.open(EXPORT / "standing.png").convert("RGBA")
reopened = Image.open(EXPORT / "standing-reopened.png").convert("RGBA")
revision = Image.open(EXPORT / "standing-tote-revision-test.png").convert("RGBA")
assert sprite.size == (128, 192) and sprite.tobytes() == reopened.tobytes()
assert set(sprite.getchannel("A").tobytes()) == {0, 255}

# Native header plus actual Aseprite reopen evidence in source-checks.json.
native = ROOT / "assets/source/standing-v02/standing.aseprite"
raw = native.read_bytes()
assert int.from_bytes(raw[:4], "little") == len(raw)
assert int.from_bytes(raw[4:6], "little") == 0xA5E0
assert int.from_bytes(raw[6:8], "little") == 1
assert int.from_bytes(raw[8:10], "little") == 128
assert int.from_bytes(raw[10:12], "little") == 192

ref = Image.open(ROOT / "assets/references/approved-2026-10-26/character-cutout.png").convert("RGBA")
# Threshold only the analysis/preview reference, never change the approved input.
ref.putalpha(ref.getchannel("A").point(lambda a: 255 if a > 180 else 0))
refsmall = ref.resize(sprite.size, Image.Resampling.NEAREST)
refmask = refsmall.getchannel("A")
# Ignore disconnected extraction debris for the silhouette comparison only.
remaining = {(x, y) for y in range(192) for x in range(128) if refmask.getpixel((x, y))}
components = []
while remaining:
    seed = remaining.pop()
    component = {seed}
    queue = deque([seed])
    while queue:
        x, y = queue.popleft()
        for point in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if point in remaining:
                remaining.remove(point)
                component.add(point)
                queue.append(point)
    components.append(component)
reference_shape = max(components, key=len)
for y in range(192):
    for x in range(128):
        if (x, y) not in reference_shape:
            refsmall.putpixel((x, y), (0, 0, 0, 0))
drawn_shape = {(x,y) for y in range(192) for x in range(128) if sprite.getpixel((x,y))[3]}
iou = len(reference_shape & drawn_shape) / len(reference_shape | drawn_shape)
changed = {(x,y) for y in range(192) for x in range(128) if sprite.getpixel((x,y)) != revision.getpixel((x,y))}
tote = Image.open(PREVIEW / "layers/02-tote-body.png").convert("RGBA")
assert changed and all(tote.getpixel(p)[3] for p in changed)

board = Image.new("RGB", (1120, 870), "#242633")
d = ImageDraw.Draw(board)
d.text((24, 14), "Approved reference", fill="#f1dfcb", font=font(24))
d.text((584, 14), "Aseprite reconstruction", fill="#f1dfcb", font=font(24))
d.text((24, 45), "Reduced only for this comparison", fill="#bdc1ce", font=font(17))
d.text((584, 45), "128 x 192 canvas | nearest-neighbor 4x", fill="#bdc1ce", font=font(17))
for x, im in ((24, refsmall), (584, sprite)):
    board.paste(backed(im).resize((512, 768), Image.Resampling.NEAREST), (x, 78))
board.save(PREVIEW / "comparison.png")
backed(sprite).resize((512, 768), Image.Resampling.NEAREST).save(PREVIEW / "standing-4x.png")
sizeboard = Image.new("RGB", (344, 250), "#343342")
d = ImageDraw.Draw(sizeboard)
d.text((16, 10), "Reference 1x", fill="white", font=font(16))
d.text((188, 10), "Drawing 1x", fill="white", font=font(16))
sizeboard.paste(backed(refsmall), (16, 40))
sizeboard.paste(backed(sprite), (188, 40))
sizeboard.save(PREVIEW / "at-size.png")

face = Image.new("RGB", (848, 425), "#343342")
d = ImageDraw.Draw(face)
for x, im, label in ((0, refsmall, "Reference face / hair"), (424, sprite, "Drawn face / hair")):
    d.text((x+12, 8), label, fill="white", font=font(20))
    face.paste(backed(im.crop((30, 0, 82, 46))).resize((416, 368), Image.Resampling.NEAREST), (x, 45))
face.save(PREVIEW / "face-comparison.png")

metadata = json.loads((RECORD / "source-checks.json").read_text())
sheet = Image.new("RGB", (1024, 1224), "#282b37")
d = ImageDraw.Draw(sheet)
for i, entry in enumerate(metadata["layers"]):
    x, y = (i % 4) * 256, (i // 4) * 408
    d.text((x+6, y+7), entry["name"], fill="#f5dfc4", font=font(16))
    im = Image.open(PREVIEW / "layers" / (entry["name"] + ".png")).convert("RGBA")
    sheet.paste(backed(im).resize((256, 384), Image.Resampling.NEAREST), (x, y+24))
sheet.save(PREVIEW / "source-layers.png")

revisionboard = Image.new("RGB", (640, 490), "#343342")
d = ImageDraw.Draw(revisionboard)
for x, im, label in ((32, sprite, "MAIN: cream tote"), (352, revision, "EDIT TEST: sage tote")):
    d.text((x, 12), label, fill="white", font=font(18))
    revisionboard.paste(backed(im).resize((256,384), Image.Resampling.NEAREST), (x, 44))
d.text((32, 448), f"{len(changed)} visible pixels changed; all other pixels identical", fill="#e6d0b5", font=font(18))
revisionboard.save(PREVIEW / "revision-proof.png")

results = {
    "native_reopen_export_identical": True,
    "binary_alpha_only": True,
    "canvas": list(sprite.size),
    "drawn_bounds": sprite.getbbox(),
    "visible_palette_colors": len({sprite.getpixel(p) for p in drawn_shape}),
    "visible_tote_revision_pixels": len(changed),
    "all_visible_revision_pixels_inside_tote_layer": True,
    "native_sha256": hashlib.sha256(raw).hexdigest(),
    "export_sha256": hashlib.sha256((EXPORT / "standing.png").read_bytes()).hexdigest(),
    "silhouette_iou_at_common_grid": round(iou, 4),
    "metric_limit": "Unregistered pixel-mask overlap after reference alpha cleanup; not face/color/style fidelity or human approval.",
    "reference_preview_processing": "Nearest-neighbor 128x192, alpha>180, retain largest connected component; original untouched",
    "godot_playback": "not performed",
}
(RECORD / "export-checks.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
