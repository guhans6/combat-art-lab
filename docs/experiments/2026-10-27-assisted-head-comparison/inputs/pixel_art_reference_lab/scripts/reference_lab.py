#!/usr/bin/env python3
"""Offline reference preparation, not an image generator or native sprite author.

Requires Pillow. Commands inspect pixels, build conversion seeds, or normalize
explicitly registered frames. Source images are never modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

from PIL import Image, __version__ as PILLOW_VERSION

FILTERS = {name: getattr(Image.Resampling, name) for name in ('NEAREST', 'BOX', 'BILINEAR', 'BICUBIC', 'LANCZOS')}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def positive_size(value: Any, name: str = 'size') -> tuple[int, int]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f'{name} must contain width and height')
    if any(isinstance(v, bool) or not isinstance(v, int) or v <= 0 for v in value):
        raise ValueError(f'{name} must contain positive integers')
    w, h = value
    if w > 8192 or h > 8192 or w * h > 16_777_216:
        raise ValueError(f'{name} is too large for this bounded helper')
    return w, h


def point(value: Any, name: str) -> tuple[float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f'{name} must contain x and y')
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in value):
        raise ValueError(f'{name} must contain finite numbers')
    return float(value[0]), float(value[1])


def load_rgba(path: Path) -> Image.Image:
    if not path.is_file():
        raise FileNotFoundError(f'Image not found: {path}')
    with Image.open(path) as src:
        if getattr(src, 'n_frames', 1) != 1:
            raise ValueError('Supply individual PNG frames, not an animated input')
        # Do not silently rotate/orient input; coordinates refer to stored pixels.
        return src.convert('RGBA')


def crop_box(image: Image.Image, box: Any) -> tuple[int, int, int, int]:
    if box is None:
        return 0, 0, image.width, image.height
    if not isinstance(box, (list, tuple)) or len(box) != 4:
        raise ValueError('Crop must be [left, top, right, bottom]')
    if any(isinstance(v, bool) or not isinstance(v, int) for v in box):
        raise ValueError('Crop coordinates must be integers')
    l, t, r, b = box
    if not (0 <= l < r <= image.width and 0 <= t < b <= image.height):
        raise ValueError('Crop is empty or outside the source image')
    return l, t, r, b


def resize_rgba(image: Image.Image, size: tuple[int, int], method: str) -> Image.Image:
    if method not in FILTERS:
        raise ValueError(f'Unsupported method: {method}')
    if method == 'NEAREST':
        return image.resize(size, FILTERS[method])
    # Premultiply before filtering: hidden RGB must not bleed into visible edges.
    return image.convert('RGBa').resize(size, FILTERS[method]).convert('RGBA')


def image_stats(image: Image.Image) -> dict[str, Any]:
    rgba = image.convert('RGBA')
    histogram = rgba.getchannel('A').histogram()
    counts = rgba.getcolors(maxcolors=rgba.width * rgba.height) or []
    colors = {color[:3] for _, color in counts if color[3] > 0}
    return {
        'dimensions': list(rgba.size),
        'alpha_bbox_xyxy': rgba.getchannel('A').getbbox(),
        'visible_rgb_colors': len(colors),
        'fully_transparent_pixels': histogram[0],
        'fully_opaque_pixels': histogram[255],
        'partial_alpha_pixels': sum(histogram[1:255]),
    }


def inspect_image(path: Path) -> dict[str, Any]:
    image = load_rgba(path)
    return {'path': str(path), 'sha256': sha256(path), **image_stats(image)}


def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def reserve_output(path: Path) -> None:
    # Refuse existing directories as well as files. No overwrite flag is provided.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.mkdir(exist_ok=False)


def build_palette(image: Image.Image, colors: int) -> tuple[Image.Image, list[tuple[int, int, int]]]:
    if not 2 <= colors <= 256:
        raise ValueError('Palette size must be between 2 and 256')
    pixel_reader = getattr(image, 'get_flattened_data', None)
    pixels = pixel_reader() if pixel_reader is not None else image.getdata()
    visible = [p[:3] for p in pixels if p[3] > 0]
    if not visible:
        raise ValueError('Cannot derive a palette from a fully transparent crop')
    samples = Image.new('RGB', (len(visible), 1))
    samples.putdata(visible)
    reduced = samples.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    table = reduced.getpalette()
    used = sorted(index for _, index in reduced.getcolors(maxcolors=256))
    entries = [tuple(table[index * 3:index * 3 + 3]) for index in used]
    # Fill unused palette slots with an existing color, not unintended black.
    extended = entries + [entries[0]] * (256 - len(entries))
    palette = Image.new('P', (1, 1))
    palette.putpalette([component for entry in extended for component in entry])
    return palette, entries


def map_palette(image: Image.Image, palette: Image.Image) -> Image.Image:
    result = image.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
    result.putalpha(image.getchannel('A'))
    return result


def make_seeds(source: Path, out: Path, sizes: list[tuple[int, int]],
               crop: Any = None, method: str = 'BOX', colors: int | None = None,
               mask_path: Path | None = None, alpha_threshold: int | None = None) -> dict[str, Any]:
    if out.exists():
        raise FileExistsError(f'Use a new output directory: {out}')
    original = load_rgba(source)
    box = crop_box(original, crop)
    working = original.copy()
    mask_record = None
    if mask_path is not None:
        with Image.open(mask_path) as m:
            mask = m.convert('L')
        if mask.size != original.size:
            raise ValueError('Mask must match full source dimensions; white=keep, black=remove')
        # Multiply coverage; do not silently erase existing source alpha.
        from PIL import ImageChops
        working.putalpha(ImageChops.multiply(working.getchannel('A'), mask))
        mask_record = {'path': str(mask_path), 'sha256': sha256(mask_path)}
    working = working.crop(box)
    if working.getchannel('A').getbbox() is None:
        raise ValueError('Crop/mask contains no visible pixels')
    if alpha_threshold is not None and not 1 <= alpha_threshold <= 255:
        raise ValueError('Alpha threshold must be 1..255, or omitted to preserve coverage')
    if not sizes or len(set(sizes)) != len(sizes):
        raise ValueError('Provide one or more distinct target sizes')
    for size in sizes:
        w, h = positive_size(size)
        if w * working.height != h * working.width:
            raise ValueError('Target aspect ratio differs from crop; crop/pad explicitly instead of stretching')
    palette, entries = build_palette(working, colors) if colors is not None else (None, None)
    prepared = []
    for size in sizes:
        result = resize_rgba(working, size, method)
        if palette is not None:
            result = map_palette(result, palette)
        if alpha_threshold is not None:
            result.putalpha(result.getchannel('A').point(lambda v: 255 if v >= alpha_threshold else 0))
        prepared.append((f'seed_{size[0]}x{size[1]}.png', result))
    record = {
        'schema': 1, 'operation': 'diagnostic_conversion_seeds', 'Pillow_version': PILLOW_VERSION,
        'source': {'path': str(source), 'sha256': sha256(source), 'dimensions': list(original.size)},
        'crop_xyxy': list(box), 'mask': mask_record, 'method': method,
        'palette_requested_colors': colors, 'palette_rgb': entries, 'dithering': 'none',
        'alpha_threshold': alpha_threshold, 'outputs': [],
        'limits': ['Not native Aseprite construction', 'No automatic background removal or semantic segmentation',
                   'No likeness or production-readiness judgment', 'No EXIF orientation or color-profile conversion'],
    }
    reserve_output(out)
    working.save(out / 'source_crop.png')
    for name, image in prepared:
        image.save(out / name)
        record['outputs'].append({'file': name, 'sha256': sha256(out / name), **image_stats(image)})
    save_json(out / 'processing.json', record)
    return record


def normalize_frames(config_path: Path, out: Path) -> dict[str, Any]:
    if out.exists():
        raise FileExistsError(f'Use a new output directory: {out}')
    config = json.loads(config_path.read_text(encoding='utf-8'))
    canvas = positive_size(config.get('canvas'), 'canvas')
    scale = config.get('scale')
    if isinstance(scale, bool) or not isinstance(scale, (int, float)) or not math.isfinite(scale) or scale <= 0:
        raise ValueError('scale must be one finite positive number shared across all frames')
    target = point(config.get('target_anchor'), 'target_anchor')
    method = config.get('resampling', 'NEAREST')
    if method not in FILTERS:
        raise ValueError('Unsupported resampling method')
    frames = config.get('frames')
    if not isinstance(frames, list) or not 1 <= len(frames) <= 64:
        raise ValueError('Provide 1..64 explicit frame entries')
    prepared = []
    ids: set[str] = set()
    for frame in frames:
        name = frame.get('id')
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_-]+', name) or name in ids:
            raise ValueError('Frame ids must be unique simple names (letters, digits, underscore, dash)')
        ids.add(name)
        raw_path = frame.get('path')
        if not isinstance(raw_path, str) or not raw_path:
            raise ValueError('Each frame requires an actual input path')
        source = (config_path.parent / raw_path).resolve()
        original = load_rgba(source)
        box = crop_box(original, frame.get('crop'))
        image = original.crop(box)
        stats = image_stats(image)
        if stats['alpha_bbox_xyxy'] is None:
            raise ValueError(f'{name}: empty frame')
        if config.get('require_transparent', False) and not stats['fully_transparent_pixels']:
            raise ValueError(f'{name}: no fully transparent pixels; mask/extract and review first')
        anchor = point(frame.get('source_anchor'), 'source_anchor')
        if not (0 <= anchor[0] <= original.width and 0 <= anchor[1] <= original.height):
            raise ValueError(f'{name}: source anchor must be within source-image edge coordinates')
        offset = point(frame.get('motion_offset', [0, 0]), 'motion_offset')
        duration = frame.get('duration_ms')
        if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
            raise ValueError('Every frame needs a positive integer duration_ms')
        size = positive_size([max(1, round(image.width * scale)), max(1, round(image.height * scale))])
        scaled = resize_rgba(image, size, method)
        # Use the actual integer-resize ratio for pivot mapping; record tiny rounding distortion.
        sx, sy = size[0] / image.width, size[1] / image.height
        mapped_anchor = ((anchor[0] - box[0]) * sx, (anchor[1] - box[1]) * sy)
        tx = round(target[0] + offset[0] - mapped_anchor[0])
        ty = round(target[1] + offset[1] - mapped_anchor[1])
        bounds = scaled.getchannel('A').getbbox()
        if bounds is None:
            raise ValueError(f'{name}: visible content disappeared during resampling')
        visible = [bounds[0] + tx, bounds[1] + ty, bounds[2] + tx, bounds[3] + ty]
        if visible[0] < 0 or visible[1] < 0 or visible[2] > canvas[0] or visible[3] > canvas[1]:
            raise ValueError(f'{name}: visible content would be clipped; expand canvas/review anchors')
        result = Image.new('RGBA', canvas, (0, 0, 0, 0))
        result.paste(scaled, (tx, ty))
        info = {
            'id': name, 'source_path': str(source), 'source_sha256': sha256(source), 'source_crop_xyxy': list(box),
            'source_anchor': list(anchor), 'scale_requested': scale, 'effective_xy_scale': [sx, sy],
            'motion_offset': list(offset), 'translation_xy': [tx, ty], 'duration_ms': duration,
            'realized_anchor': [tx + mapped_anchor[0], ty + mapped_anchor[1]],
            'output_file': name + '.png', **image_stats(result),
        }
        prepared.append((result, info))
    # A bounded contact sheet is data packaging, not an animation-quality preview.
    columns = min(8, len(prepared))
    rows = math.ceil(len(prepared) / columns)
    sheet_size = positive_size([canvas[0] * columns, canvas[1] * rows], 'sheet size')
    sheet = Image.new('RGBA', sheet_size, (0, 0, 0, 0))
    record = {
        'schema': 1, 'operation': 'explicit_frame_normalization', 'Pillow_version': PILLOW_VERSION,
        'config_sha256': sha256(config_path), 'canvas': list(canvas), 'scale': scale, 'method': method,
        'target_anchor': list(target), 'sheet_columns': columns, 'frames': [],
        'limits': ['No frame/pose generation or anatomy correction', 'No automatic pivots or source-scale inference',
                   'No background removal, palette unification, or native layers',
                   'Motion offsets are supplied data, not inferred movement', 'Not proof of animation or runtime quality'],
    }
    reserve_output(out)
    for index, (image, info) in enumerate(prepared):
        path = out / info['output_file']
        image.save(path)
        info['output_sha256'] = sha256(path)
        record['frames'].append(info)
        sheet.paste(image, ((index % columns) * canvas[0], (index // columns) * canvas[1]))
    sheet.save(out / 'sheet.png')
    save_json(out / 'processing.json', record)
    return record


def parse_size(text: str) -> tuple[int, int]:
    try:
        w, h = map(int, text.lower().split('x'))
        return positive_size([w, h])
    except (ValueError, TypeError):
        raise argparse.ArgumentTypeError('Use WIDTHxHEIGHT, e.g. 84x63')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    audit = sub.add_parser('inspect', help='Read dimensions, hashes and alpha/color statistics')
    audit.add_argument('images', nargs='+', type=Path)
    seeds = sub.add_parser('seeds', help='Create diagnostic conversion seeds, never final native art')
    seeds.add_argument('source', type=Path)
    seeds.add_argument('--out', type=Path, required=True)
    seeds.add_argument('--sizes', type=parse_size, nargs='+', required=True)
    seeds.add_argument('--crop', nargs=4, type=int)
    seeds.add_argument('--colors', type=int)
    seeds.add_argument('--mask', type=Path)
    seeds.add_argument('--method', choices=list(FILTERS), default='BOX')
    seeds.add_argument('--alpha-threshold', type=int)
    norm = sub.add_parser('normalize', help='Normalize explicitly registered frames at one common scale')
    norm.add_argument('config', type=Path)
    norm.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'inspect':
            result = [inspect_image(path) for path in args.images]
        elif args.command == 'seeds':
            result = make_seeds(args.source, args.out, args.sizes, args.crop, args.method,
                                args.colors, args.mask, args.alpha_threshold)
        else:
            result = normalize_frames(args.config, args.out)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
