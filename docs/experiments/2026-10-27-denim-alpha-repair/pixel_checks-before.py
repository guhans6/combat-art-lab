#!/usr/bin/env python3
"""Deterministic PNG checks and nearest-neighbor review sheets, not art scoring."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from PIL import Image, ImageDraw


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixel_values(image: Image.Image):
    """Support both older and newer Pillow pixel iterators."""
    getter = getattr(image, 'get_flattened_data', None)
    return getter() if getter else image.getdata()


def canonical_pixels(image: Image.Image) -> list[tuple[int, int, int, int]]:
    # Invisible RGB does not alter the rendered sprite. File hashes still detect it.
    return [(r, g, b, a) if a else (0, 0, 0, 0)
            for r, g, b, a in pixel_values(image.convert('RGBA'))]


def read_mask(path: Path, size: tuple[int, int]) -> list[bool]:
    with Image.open(path) as image:
        if image.size != size:
            raise ValueError('Mask dimensions do not match the native canvas.')
        if image.mode not in ('1', 'L'):
            raise ValueError('Mask must be a binary grayscale PNG (mode L or 1).')
        values = list(pixel_values(image.convert('L')))
    if set(values) != {0, 255}:
        raise ValueError('Mask must contain both protected black and editable white, with no gray.')
    return [v == 255 for v in values]


def mask_from_profile(profile: dict[str, Any]) -> Image.Image:
    w, h = profile['canvas']
    if not isinstance(w, int) or not isinstance(h, int) or w <= 0 or h <= 0:
        raise ValueError('Canvas dimensions must be positive integers.')
    out = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(out)
    for name, value in [('include_rects', 255), ('exclude_rects', 0)]:
        for rect in profile['editable_region'].get(name, []):
            if len(rect) != 4 or not all(isinstance(v, int) for v in rect):
                raise ValueError('Mask rectangles need four integer coordinates.')
            x0, y0, x1, y1 = rect
            if not (0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h):
                raise ValueError('Mask rectangle is outside the canvas or empty.')
            draw.rectangle((x0, y0, x1 - 1, y1 - 1), fill=value)
    if set(pixel_values(out)) != {0, 255}:
        raise ValueError('A scoped edit needs both editable and protected pixels.')
    return out


def check_images(before: Image.Image, after: Image.Image, allowed: list[bool],
                 *, allow_new_colors: bool = False,
                 allow_partial_alpha: bool = False,
                 require_change: bool = True) -> dict[str, Any]:
    if before.size != after.size:
        return {'passed': False, 'failures': ['canvas_changed'],
                'before_size': list(before.size), 'after_size': list(after.size)}
    width, height = before.size
    if len(allowed) != width * height:
        raise ValueError('Mask pixel count does not match the canvas.')
    bp, ap = canonical_pixels(before), canonical_pixels(after)
    changed = [i for i, (a, b) in enumerate(zip(bp, ap)) if a != b]
    outside = [i for i in changed if not allowed[i]]
    bc = {p[:3] for p in bp if p[3]}
    ac = {p[:3] for p in ap if p[3]}
    new_colors = sorted(ac - bc)
    partial = sum(0 < p[3] < 255 for p in ap)
    visible = sum(p[3] > 0 for p in ap)
    failures = []
    if outside: failures.append('protected_pixels_changed')
    if new_colors and not allow_new_colors: failures.append('new_visible_colors')
    if partial and not allow_partial_alpha: failures.append('partial_alpha')
    if not visible: failures.append('empty_sprite')
    if require_change and not changed: failures.append('no_visible_change')
    bbox = None
    if changed:
        xs, ys = [i % width for i in changed], [i // width for i in changed]
        bbox = [min(xs), min(ys), max(xs) + 1, max(ys) + 1]
    return {
        'passed': not failures, 'failures': failures,
        'canvas': [width, height], 'changed_pixels': len(changed),
        'outside_mask_changed_pixels': len(outside),
        'outside_mask_examples_xy': [[i % width, i // width] for i in outside[:20]],
        'changed_bbox_half_open': bbox,
        'visible_colors_before': len(bc), 'visible_colors_after': len(ac),
        'new_visible_rgb_colors': [list(c) for c in new_colors],
        'partial_alpha_pixels': partial, 'visible_pixels': visible,
        'silhouette_changed_pixels': sum(bool(a[3]) != bool(b[3]) for a, b in zip(bp, ap)),
        'alpha_changed_pixels': sum(a[3] != b[3] for a, b in zip(bp, ap)),
        'boundary': 'PNG checks only; native layers, likeness and user approval are not certified.'
    }


def check_files(before: Path, after: Path, mask: Path, **kwargs: Any) -> dict[str, Any]:
    with Image.open(before) as b, Image.open(after) as a:
        allowed = read_mask(mask, b.size)
        result = check_images(b, a, allowed, **kwargs)
    result['sha256'] = {'before': sha256(before), 'after': sha256(after), 'mask': sha256(mask)}
    return result


def difference_image(before: Image.Image, after: Image.Image) -> Image.Image:
    if before.size != after.size:
        raise ValueError('Cannot compare different canvas sizes.')
    out = Image.new('L', before.size)
    out.putdata([255 if b != a else 0 for b, a in zip(canonical_pixels(before), canonical_pixels(after))])
    return out


def checkerboard(size: tuple[int, int]) -> Image.Image:
    image = Image.new('RGBA', size, (49, 49, 61, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], 8):
        for x in range(0, size[0], 8):
            if (x // 8 + y // 8) % 2:
                draw.rectangle((x, y, x + 7, y + 7), fill=(61, 61, 73, 255))
    return image


def review_sheet(before: Image.Image, after: Image.Image,
                 crop: tuple[int, int, int, int], scale: int = 8) -> Image.Image:
    if before.size != after.size or scale < 1:
        raise ValueError('Equal canvas sizes and a positive integer zoom are required.')
    x0, y0, x1, y1 = crop
    if not (0 <= x0 < x1 <= before.width and 0 <= y0 < y1 <= before.height):
        raise ValueError('Review crop is outside the canvas.')
    labels = ['Baseline', 'Candidate', 'Difference (white = changed)']
    images = [before.convert('RGBA'), after.convert('RGBA'), difference_image(before, after).convert('RGBA')]
    cw = max(before.width, (x1 - x0) * scale, 220) + 24
    top = 30
    bottom_y = top + before.height + 30
    out = Image.new('RGB', (cw * 3, bottom_y + (y1 - y0) * scale + 20), (38, 38, 49))
    draw = ImageDraw.Draw(out)
    for col, (label, image) in enumerate(zip(labels, images)):
        x = col * cw + 12
        draw.text((x, 8), label, fill='white')
        tile = checkerboard(image.size)
        tile.alpha_composite(image)
        out.paste(tile.convert('RGB'), (x, top))
        detail = tile.crop(crop).resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.Resampling.NEAREST)
        draw.text((x, bottom_y - 18), f'Head crop, {scale}x nearest-neighbor', fill='white')
        out.paste(detail.convert('RGB'), (x, bottom_y))
    return out


def safe_output(path: Path, inputs: list[Path]) -> None:
    if path.resolve() in {p.resolve() for p in inputs}:
        raise ValueError('Output must not overwrite an input.')
    if path.exists():
        raise FileExistsError(f'Output already exists: {path}. Use a new pass directory.')
    path.parent.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    mask = sub.add_parser('mask')
    mask.add_argument('--profile', type=Path, required=True)
    mask.add_argument('--out', type=Path, required=True)
    check = sub.add_parser('check')
    for key in ('before', 'after', 'mask', 'out'):
        check.add_argument('--' + key, type=Path, required=True)
    check.add_argument('--allow-new-colors', action='store_true')
    check.add_argument('--allow-partial-alpha', action='store_true')
    check.add_argument('--allow-noop', action='store_true')
    preview = sub.add_parser('preview')
    for key in ('before', 'after', 'out'):
        preview.add_argument('--' + key, type=Path, required=True)
    preview.add_argument('--crop', type=int, nargs=4, required=True, metavar=('X0', 'Y0', 'X1', 'Y1'))
    preview.add_argument('--scale', type=int, default=8)
    args = parser.parse_args()
    try:
        if args.command == 'mask':
            image = mask_from_profile(json.loads(args.profile.read_text()))
            safe_output(args.out, [args.profile])
            image.save(args.out, 'PNG')
            return 0
        if args.command == 'check':
            result = check_files(args.before, args.after, args.mask,
                                 allow_new_colors=args.allow_new_colors,
                                 allow_partial_alpha=args.allow_partial_alpha,
                                 require_change=not args.allow_noop)
            safe_output(args.out, [args.before, args.after, args.mask])
            args.out.write_text(json.dumps(result, indent=2) + '\n')
            print(json.dumps(result, indent=2))
            return 0 if result['passed'] else 1
        with Image.open(args.before) as b, Image.open(args.after) as a:
            sheet = review_sheet(b, a, tuple(args.crop), args.scale)
        safe_output(args.out, [args.before, args.after])
        sheet.save(args.out, 'PNG')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'pixel_checks: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
