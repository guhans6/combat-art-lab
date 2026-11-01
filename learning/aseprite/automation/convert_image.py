#!/usr/bin/env python3
"""Deterministic PNG preparation. No network, model, drawing or native-file writes."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from PIL import Image, __version__ as pillow_version


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(recipe_path, output):
    recipe_path = recipe_path.resolve()
    config = json.loads(recipe_path.read_text())
    source = (recipe_path.parent / config['source']).resolve()
    with Image.open(source) as opened:
        image = opened.convert('RGBA')
    inputs = {'source': {'path': str(source), 'sha256': digest(source)}}
    # A supplied mask is a previously reviewed decision, not inferred anatomy.
    if config.get('mask'):
        mask_path = (recipe_path.parent / config['mask']).resolve()
        with Image.open(mask_path) as opened:
            mask = opened.convert('L')
        if mask.size != image.size:
            raise ValueError('mask dimensions must match source')
        mask = mask.point(lambda value: 255 if value >= 128 else 0)
        inputs['mask'] = {'path': str(mask_path), 'sha256': digest(mask_path)}
    else:
        threshold = config.get('alpha_threshold', 160)
        if not 1 <= threshold <= 255:
            raise ValueError('alpha_threshold must be 1..255')
        mask = image.getchannel('A').point(lambda value: 255 if value >= threshold else 0)
    # Never turn transparent source pixels into paint, even with an explicit mask.
    mask.putdata([m if a else 0 for m, a in zip(mask.get_flattened_data(), image.getchannel('A').get_flattened_data())])
    bounds = mask.getbbox()
    if not bounds:
        raise ValueError('empty foreground')
    image.putalpha(mask)
    crop = image.crop(bounds)
    if 'scale' in config:
        scale = float(config['scale'])
        if not 0 < scale < float('inf'):
            raise ValueError('scale must be finite and positive')
        height = max(1, round(crop.height * scale))
    else:
        height = int(config['height'])
        if height <= 0:
            raise ValueError('height must be positive')
        scale = height / crop.height
    size = (max(1, round(crop.width * scale)), height)
    resized = crop.resize(size, Image.Resampling.NEAREST)
    sx, sy = config['source_anchor']
    tx, ty = config['target_anchor']
    offset = (round(tx - (sx - bounds[0]) * size[0] / crop.width),
              round(ty - (sy - bounds[1]) * size[1] / crop.height))
    canvas = tuple(config['canvas'])
    x, y = offset
    if x < 0 or y < 0 or x + size[0] > canvas[0] or y + size[1] > canvas[1]:
        raise ValueError('foreground would be clipped; adjust canvas or anchor')
    result = Image.new('RGBA', canvas)
    result.paste(resized, offset)
    # Normalize hidden RGB only; every visible RGB is sampled from the source.
    result.putdata([p if p[3] else (0, 0, 0, 0) for p in result.get_flattened_data()])
    source_colors = {p[:3] for p in image.get_flattened_data() if p[3]}
    output_colors = {p[:3] for p in result.get_flattened_data() if p[3]}
    if not output_colors <= source_colors:
        raise RuntimeError("conversion introduced a visible RGB color")
    output.mkdir(parents=True, exist_ok=False)
    result.save(output / 'converted.png')
    preview = result.resize((canvas[0] * 3, canvas[1] * 3), Image.Resampling.NEAREST)
    preview.save(output / 'preview-3x.png')
    report = {'inputs': inputs, 'recipe': config, 'recipe_sha256': digest(recipe_path),
              'pillow': pillow_version, 'python': sys.version, 'script_sha256': digest(Path(__file__)), 'source_bounds': bounds, 'placed_size': size,
              'offset': offset, 'visible_colors': len(output_colors),
              'visible_colors_are_source_samples': True,
              'output_rgba_sha256': hashlib.sha256(result.tobytes()).hexdigest(),
              'limits': 'Flat conversion seed; no anatomical cleanup or semantic layers. Existing mask is a reviewed input.'}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipe', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True, help='new directory; existing directories refused')
    args = parser.parse_args()
    prepare(args.recipe, args.out)
