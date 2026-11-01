"""Parent's read-only technical audit. Never authors or repairs sprite pixels."""
from pathlib import Path
import hashlib
import importlib.util
import json
import zipfile
from PIL import Image
from tools.check_native_pilot import read

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
ARTISTS = ['luna56-max', 'luna6-max', 'terra56', 'sol61']


def coverage(frames, baseline):
    spec = importlib.util.spec_from_file_location('director_pixels', ROOT / 'tools/pixel-art-director/scripts/pixel_checks.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    region = (0, 34, 128, 192)
    inherited = module.check_alpha_coverage(baseline, region=region)['hole_pixels_xy']
    checks = []
    for f, im in enumerate(frames):
        report = module.check_alpha_coverage(im, region=region, allowed_holes=inherited)
        alphas = set(im.getchannel('A').get_flattened_data())
        checks.append({'frame_1based': f + 1, 'binary_alpha': alphas <= {0, 255},
                       'new_enclosed_body_holes_xy': report['hole_pixels_xy']})
    return {'passed': all(r['binary_alpha'] and not r['new_enclosed_body_holes_xy'] for r in checks),
            'frames': checks, 'inherited_body_holes_xy': inherited,
            'limits': 'Enclosed body-hole/binary-alpha check only; moving silhouette and intentional head/hair gaps need scoped review.'}


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def compose(data, frame):
    im = Image.new('RGBA', tuple(data['canvas']))
    for i, layer in enumerate(data['layers']):
        assert layer['type'] == 0 and layer['level'] == 0, 'Unsupported native layer structure'
        if layer['flags'] & 1:
            assert layer['blend'] == 0 and layer['opacity'] == 255, 'Unsupported compositing'
            cel = data['cels'].get((frame, i))
            if cel:
                assert cel['opacity'] == 255 and cel['z'] == 0, 'Unsupported cel compositing'
                im.alpha_composite(cel['image'])
    return im


def palette_chunks(data):
    return [c for frame in data['frames'] for c in frame['non_cel_chunks'] if c['type'] == '0x2019']


def path_in(folder, relative):
    p = (folder / relative).resolve()
    assert p.is_relative_to(folder.resolve()) and p.is_file(), relative
    return p


def gif_check(path, frames, times, scale):
    gif = Image.open(path)
    decoded, gif_times = [], []
    for f in range(gif.n_frames):
        gif.seek(f)
        decoded.append(gif.convert('RGB').copy())
        gif_times.append(gif.info['duration'])
    assert all(im.size == (128 * scale, 192 * scale) for im in decoded)
    bg = decoded[0].getpixel((0, 0))
    expected = []
    for im in frames:
        matte = Image.new('RGBA', im.size, (*bg, 255))
        matte.alpha_composite(im)
        expected.append(matte.convert('RGB').resize((128 * scale, 192 * scale), Image.Resampling.NEAREST))
    # GIF may merge identical neighboring holds. Compare pixels throughout the
    # combined timeline instead of requiring an identical encoded frame count.
    assert sum(times) == sum(gif_times), 'GIF cycle duration differs'
    a = b = elapsed_a = elapsed_b = 0
    exact = True
    while a < len(expected) and b < len(decoded):
        exact &= expected[a].tobytes() == decoded[b].tobytes()
        step = min(times[a] - elapsed_a, gif_times[b] - elapsed_b)
        assert step > 0
        elapsed_a += step
        elapsed_b += step
        if elapsed_a == times[a]:
            a += 1
            elapsed_a = 0
        if elapsed_b == gif_times[b]:
            b += 1
            elapsed_b = 0
    assert exact and a == len(expected) and b == len(decoded), 'GIF pixels differ on timeline'
    return {'sha256': digest(path), 'encoded_frames': len(decoded), 'durations_ms': gif_times,
            'cycle_ms': sum(gif_times), 'loop': gif.info.get('loop'), 'matte_rgb': bg,
            'timeline_equals_native': True}


def check_artist(name, base):
    folder = OUT / name
    manifest = folder / 'delivery.json'
    if not manifest.exists():
        return {'status': 'not_delivered'}
    delivery = json.loads(manifest.read_text())
    if not delivery.get('native'):
        return {'status': 'not_delivered', 'note': 'Preparation manifest only'}
    native = path_in(folder, delivery['native'])
    data = read(native)
    assert data['canvas'] == base['canvas'] == [128, 192]
    original_names = [layer['name'] for layer in base['layers']]
    new_names = [layer['name'] for layer in data['layers']]
    assert len(new_names) == len(set(new_names)), 'Duplicate layer names'
    retained = [layer for layer in data['layers'] if layer['name'] in original_names]
    assert retained == base['layers'], 'Existing native layer metadata/order differs'
    additions = [layer['name'] for layer in data['layers'] if layer['name'] not in original_names]
    declared = delivery.get('added_layers', [])
    assert set(additions) == set(declared), 'Added layers must be declared'
    assert palette_chunks(data) == palette_chunks(base), 'Native palette chunks differ'
    assert len(data['frames']) == len(delivery['frames']) == len(delivery['durations_ms'])
    times = [f['duration_ms'] for f in data['frames']]
    assert times == delivery['durations_ms'] and all(t > 0 for t in times)
    baseline = compose(base, 0)
    frames = [compose(data, f) for f in range(len(times))]
    export_exact = []
    for f, relative in enumerate(delivery['frames']):
        export = Image.open(path_in(folder, relative)).convert('RGBA')
        export_exact.append(export.tobytes() == frames[f].tobytes())
    assert all(export_exact), 'Native/export disagreement'
    rest_frames = [i + 1 for i, im in enumerate(frames) if im.tobytes() == baseline.tobytes()]
    assert rest_frames, 'Original rest composite not retained'
    alpha = coverage(frames, baseline)
    for layer_index, meta in enumerate(base['layers']):
        if meta['name'] == '00-shoes' or not meta['flags'] & 1:
            current_index = new_names.index(meta['name'])
            for f in range(len(times)):
                cel = data['cels'].get((f, current_index))
                if cel is None:
                    assert not meta['flags'] & 1 and f > 0
                    continue
                assert cel['image'].tobytes() == base['cels'][(0, layer_index)]['image'].tobytes(), (meta['name'], f)
    selected = delivery.get('gif_frame_indices', list(range(len(frames))))
    assert selected and all(isinstance(i, int) and 0 <= i < len(frames) for i in selected)
    gifs = {f'{scale}x': gif_check(path_in(folder, delivery[f'gif_{scale}x']),
                                 [frames[i] for i in selected], [times[i] for i in selected], scale)
            for scale in [1, 3]}
    for key in ['verification', 'record']:
        path_in(folder, delivery[key])
    # A worker's reopen/protection/local-edit report remains worker evidence until
    # its actual fields/artifacts are inspected; this audit does not fabricate it.
    return {'status': 'technical_delivery_pass' if alpha['passed'] else 'alpha_review_required',
            'native': str(native.relative_to(OUT)),
            'native_sha256': digest(native), 'frame_count': len(times), 'durations_ms': times,
            'cycle_ms': sum(times[i] for i in selected), 'gif_native_frame_indices_0based': selected,
            'native_export_exact': export_exact,
            'rest_frames_1based': rest_frames, 'native_palette_and_existing_layer_metadata_exact': True,
            'declared_added_layers': additions,
            'shoes_and_hidden_guide_preserved': True, 'gifs': gifs,
            'alpha': alpha,
            'record': str(path_in(folder, delivery['record']).relative_to(OUT)),
            'verification': str(path_in(folder, delivery['verification']).relative_to(OUT)),
            'limits': 'No automatic artistic verdict, temporal observation, or engine proof.'}


def main():
    base = read(OUT / 'inputs/neutral.aseprite')
    result = {'artists': {}}
    for name in ARTISTS:
        try:
            result['artists'][name] = check_artist(name, base)
        except Exception as error:
            result['artists'][name] = {'status': 'technical_delivery_failed', 'error': str(error)}
    original = json.loads((OUT / 'protected-before.json').read_text())
    changed = [p for p, sha in original.items() if not (ROOT / p).exists() or digest(ROOT / p) != sha]
    common = json.loads((OUT / 'input-manifest.json').read_text())['inputs']
    common_changed = [r['name'] for r in common if digest(Path(r['frozen'])) != r['sha256']]
    extracted_changed = []
    extracted_count = 0
    with zipfile.ZipFile(OUT / 'inputs/evidence-pack.zip') as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            extracted_count += 1
            actual = OUT / 'inputs/video-evidence' / info.filename
            if not actual.exists() or digest(actual) != hashlib.sha256(z.read(info)).hexdigest():
                extracted_changed.append(info.filename)
    result['preservation'] = {'protected_files': len(original), 'changed': changed,
                              'common_frozen_inputs_changed': common_changed,
                              'extracted_evidence_files_checked': extracted_count,
                              'extracted_evidence_files_changed': extracted_changed}
    (OUT / 'parent-technical-checks.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
