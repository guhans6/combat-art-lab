"""Reproduce diagnostic seeds from the included reference crop.

Requires Pillow. Run: python reproduce_seeds.py
These are image-processing seeds, not finished pixel-art assets.
"""
from pathlib import Path
from PIL import Image


def main() -> None:
    root = Path(__file__).resolve().parent
    source = root / 'source_head_crop.png'
    if not source.is_file():
        raise FileNotFoundError(f'Missing reference crop: {source}')
    with Image.open(source) as opened:
        crop = opened.convert('RGB')
    if crop.size != (420, 315):
        raise ValueError(f'Expected the supplied 420x315 crop; got {crop.size}')
    output = root / 'reproduced'
    output.mkdir(exist_ok=True)
    palette = crop.quantize(colors=32, method=Image.Quantize.MEDIANCUT)
    for width, height in [(56, 42), (84, 63), (112, 84)]:
        result = crop.resize((width, height), Image.Resampling.BOX)
        result = result.quantize(palette=palette, dither=Image.Dither.NONE).convert('RGB')
        result.save(output / f'conversion_seed_{width}x{height}_32colors.png')
    for index, (resampling, quantize) in enumerate([
        (Image.Resampling.NEAREST, False),
        (Image.Resampling.BOX, False),
        (Image.Resampling.BOX, True),
        (Image.Resampling.LANCZOS, True),
    ], 1):
        result = crop.resize((56, 42), resampling)
        if quantize:
            result = result.quantize(palette=palette, dither=Image.Dither.NONE).convert('RGB')
        result.save(output / f'method_{index}_56x42.png')
    print(f'Recreated diagnostic PNGs in {output}')


if __name__ == '__main__':
    main()
