"""Deterministic review sheets; source scaling is labelled preview-only."""
from pathlib import Path
from PIL import Image, ImageDraw

RUN = Path(__file__).resolve().parents[1]
I, P, R = RUN / "inputs", RUN / "passes", RUN / "reviews"
R.mkdir(exist_ok=True)

def panel(label, image, scale=4):
    image = image.convert("RGBA")
    result = Image.new("RGBA", (image.width * scale, image.height * scale + 18), "#20242c")
    result.alpha_composite(image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST), (0, 18))
    ImageDraw.Draw(result).text((3, 3), label, fill="white")
    return result

def join(images):
    result = Image.new("RGBA", (sum(i.width for i in images) + 4 * (len(images) - 1), max(i.height for i in images)), "#111319")
    x = 0
    for image in images:
        result.alpha_composite(image, (x, 0)); x += image.width + 4
    return result

seed = Image.open(I / "source-only-converted-seed.png")
automatic = Image.open(P / "candidate-b-structured.png")
finish = Image.open(P / "pass-01-fullbody-finish.png")
join([panel("seed 1x", seed, 1), panel("automatic 1x", automatic, 1), panel("finish 1x", finish, 1)]).save(R / "fullbody-1x-seed-automatic-finish.png")
join([panel("seed 4x", seed), panel("automatic 4x", automatic), panel("finish 4x", finish)]).save(R / "fullbody-4x-seed-automatic-finish.png")
join([panel("seed 4x", seed), panel("candidate B verified 4x", automatic), panel("pass-01 rejected 4x", finish)]).save(R / "fullbody-4x-all-candidates.png")
box = (48, 7, 84, 39)
join([panel("seed head 1x", seed.crop(box), 1), panel("automatic head 1x", automatic.crop(box), 1), panel("finish head 1x", finish.crop(box), 1)]).save(R / "head-1x-seed-automatic-finish.png")
join([panel("seed head 16x", seed.crop(box), 16), panel("automatic head 16x", automatic.crop(box), 16), panel("finish head 16x", finish.crop(box), 16)]).save(R / "head-16x-seed-automatic-finish.png")
join([panel("seed head 16x", seed.crop(box), 16), panel("candidate B verified 16x", automatic.crop(box), 16), panel("pass-01 rejected 16x", finish.crop(box), 16)]).save(R / "head-16x-all-candidates.png")
scene = Image.open(I / "character-scene.png").convert("RGBA")
close = Image.open(I / "character-closeup.png").convert("RGBA")
scene.crop((430, 205, 765, 1017)).resize((168, 406), Image.Resampling.LANCZOS).save(R / "authoritative-scene-character-preview.png")
close.crop((395, 80, 865, 500)).resize((282, 252), Image.Resampling.LANCZOS).save(R / "authoritative-closeup-head-preview.png")
