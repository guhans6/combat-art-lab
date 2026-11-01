#!/usr/bin/env python3
"""Build registered edit evidence and check freshness; never judge artistic quality."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image
from pixel_checks import canonical_pixels, check_files, review_sheet


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def describe(points):
    return {'count': len(points), 'examples_xy': [list(p) for p in points[:20]],
            'bbox_half_open': [min(x for x, y in points), min(y for x, y in points),
                               max(x for x, y in points) + 1, max(y for x, y in points) + 1]
            if points else None}


def build_packet(spec_path, out):
    spec_path, out = Path(spec_path).resolve(), Path(out).resolve()
    if out.exists():
        raise FileExistsError('Preserve earlier evidence; choose a new packet directory.')
    spec = json.loads(spec_path.read_text())
    for key in ('baseline_role', 'registration'):
        if not isinstance(spec.get(key), str) or not spec[key].strip():
            raise ValueError(f'{key} must state the role or same-grid provenance.')
    zoom = spec.get('zoom', 4)
    if type(zoom) is not int or not 1 <= zoom <= 16:
        raise ValueError('zoom must be an integer from 1 through 16.')
    frames = spec['frames']
    required = spec['required_frame_ids']
    ids = [f['id'] for f in frames]
    if (not required or not all(isinstance(i, str) and i.strip() for i in required + ids)
            or len(set(required)) != len(required) or len(set(ids)) != len(ids)
            or set(required) != set(ids)):
        raise ValueError('Frame inventory must exactly match unique required_frame_ids.')
    sources = []

    def bind(relative, role):
        path = (spec_path.parent / relative).resolve()
        sources.append({'path': str(path), 'role': role, 'sha256': sha(path)})
        return path

    sources.append({'path': str(spec_path), 'role': 'spec', 'sha256': sha(spec_path)})
    for evidence in spec.get('evidence', []):
        bind(evidence['path'], evidence['role'])
    prepared = []
    # Validate every frame before producing evidence; equal dimensions do not prove registration.
    for f in frames:
        before = bind(f['before'], f"{f['id']} baseline")
        after = bind(f['after'], f"{f['id']} candidate")
        mask = bind(f['mask'], f"{f['id']} allowed edit mask")
        with Image.open(before) as image:
            b = image.convert('RGBA')
        with Image.open(after) as image:
            a = image.convert('RGBA')
        if b.size != a.size:
            raise ValueError('Unregistered canvas mismatch: use a labeled reference comparison instead.')
        regions = f['regions']
        if not regions:
            raise ValueError('At least one named close-review region is required.')
        names = set()
        for region in regions:
            name, crop = region['name'], region['crop']
            if not isinstance(name, str) or not name.strip() or name in names:
                raise ValueError('Close-review regions need unique nonempty names.')
            names.add(name)
            if len(crop) != 4 or not all(type(v) is int for v in crop):
                raise ValueError('Crop needs four integer coordinates.')
            x0, y0, x1, y1 = crop
            if not 0 <= x0 < x1 <= b.width or not 0 <= y0 < y1 <= b.height:
                raise ValueError('Crop must be nonempty and inside the source canvas.')
            if (max(b.width, (x1-x0)*zoom, 220)+24)*3*(b.height+(y1-y0)*zoom+80) > 20_000_000:
                raise ValueError('Review sheet too large; use a smaller zoom or crop.')
        checks = check_files(before, after, mask, require_change=False,
                             allow_new_colors=spec.get('allow_new_colors', False),
                             allow_partial_alpha=spec.get('allow_partial_alpha', False))
        changed = [(i % b.width, i // b.width) for i, (p, q) in
                   enumerate(zip(canonical_pixels(b), canonical_pixels(a))) if p != q]
        uncovered = [(x, y) for x, y in changed if not any(
            r['crop'][0] <= x < r['crop'][2] and r['crop'][1] <= y < r['crop'][3]
            for r in regions)]
        prepared.append((f, b, a, checks, describe(uncovered)))
    out.mkdir(parents=True)
    results, artifacts = [], []
    for index, (f, b, a, checks, uncovered) in enumerate(prepared):
        sheets = []
        for ri, region in enumerate(f['regions']):
            path = out / f'frame-{index:03d}-region-{ri:02d}.png'
            review_sheet(b, a, tuple(region['crop']), zoom).save(path)
            artifacts.append({'path': str(path), 'sha256': sha(path)})
            sheets.append({'name': region['name'], 'crop_xyxy_half_open': region['crop'],
                           'path': str(path)})
        results.append({'id': f['id'], 'checks': checks, 'uncovered_changes': uncovered,
                        'regions': sheets, 'mechanical_passed': checks['passed'] and not uncovered['count']})
    report = {'schema_version': 1, 'baseline_role': spec['baseline_role'],
              'registration_claim': spec['registration'], 'sources': sources, 'sheets': artifacts,
              'frames': results, 'zoom': zoom, 'resampling': 'integer nearest-neighbor',
              'matte': 'checkerboard RGB49,49,61 / 61,61,73',
              'mechanical_passed': all(f['mechanical_passed'] for f in results),
              'visual_acceptance': 'pending', 'user_approval': 'pending',
              'limits': 'Coverage means pixels are available for inspection. Scope/coverage cannot judge '
                        'anatomy, occlusion, grip or improvement. Registration and affected-frame inventory '
                        'are caller declarations. Bound native/report hashes do not prove export correspondence '
                        'or hidden-layer integrity. Source or packet changes require fresh review.'}
    (out / 'packet.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def verify_packet(packet):
    """Check file identity only. A fresh failed packet remains mechanically failed."""
    report = json.loads(Path(packet).read_text())
    stale = []
    for item in report['sources'] + report['sheets']:
        path = Path(item['path'])
        if not path.is_file() or sha(path) != item['sha256']:
            stale.append({'path': str(path), 'reason': 'missing or changed'})
    return {'fresh': not stale, 'stale_files': stale,
            'mechanical_passed': report['mechanical_passed'],
            'visual_acceptance': 'pending', 'user_approval': 'pending',
            'limits': 'Freshness is not inspection or artistic acceptance; bind manual review to packet SHA256.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    build = sub.add_parser('build')
    build.add_argument('--spec', type=Path, required=True)
    build.add_argument('--out', type=Path, required=True)
    verify = sub.add_parser('verify')
    verify.add_argument('--packet', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'verify':
            result = verify_packet(args.packet)
            print(json.dumps(result, indent=2))
            return 0 if result['fresh'] else 1
        report = build_packet(args.spec, args.out)
        print(json.dumps({'mechanical_passed': report['mechanical_passed'],
                          'visual_acceptance': report['visual_acceptance']}))
        return 0 if report['mechanical_passed'] else 1
    except (ValueError, KeyError, OSError, TypeError) as error:
        parser.exit(2, f'{error}\n')


if __name__ == '__main__':
    raise SystemExit(main())
