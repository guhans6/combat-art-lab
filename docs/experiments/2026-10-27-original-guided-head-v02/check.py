"""Verify the saved study through independent RGBA/native checks, not art scoring."""
from pathlib import Path
import hashlib
import json
import runpy
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
native = runpy.run_path(str(ROOT / 'tools/check_native_pilot.py'))
allowed = ['01-tied-hair-back', '04-neck-and-ear', '05-face-plane',
           '06-crown-and-fringe', '07-pale-hair-tie', '08-face-features']
mask = [True] * (120 * 112)
reports = {}
for name in ['pass-01-hair', 'pass-02-face', 'pass-03-refined']:
    targets = ['01-tied-hair-back', '06-crown-and-fringe', '07-pale-hair-tie'] if name == 'pass-01-hair' else allowed
    result = native['compare'](HERE / 'baseline.aseprite', HERE / f'{name}.aseprite', targets, mask)
    assert result['passed'], result
    with Image.open(HERE / f'{name}.png') as a, Image.open(HERE / f'{name}-reopened.png') as b:
        assert a.size == b.size == (120, 112)
        assert a.convert('RGBA').tobytes() == b.convert('RGBA').tobytes()
        alpha = set(a.convert('RGBA').getchannel('A').get_flattened_data())
        assert alpha == {0, 255}
        result['visible_rgb_count'] = len({px[:3] for px in a.convert('RGBA').get_flattened_data() if px[3]})
    result['fresh_reopen_export_match'] = True
    result['source_sha256'] = hashlib.sha256((HERE / f'{name}.aseprite').read_bytes()).hexdigest()
    reports[name] = result

source = native['read'](HERE / 'pass-03-refined.aseprite')
assert source['canvas'] == [120, 112] and len(source['layers']) == 10 and len(source['frames']) == 1
baseline = native['read'](HERE / 'baseline.aseprite')
ear_index = next(i for i, l in enumerate(source['layers']) if l['name'] == '04-neck-and-ear')
assert source['cels'][(0, ear_index)]['image'].getchannel('A').tobytes() == baseline['cels'][(0, ear_index)]['image'].getchannel('A').tobytes()
tie_index = next(i for i, l in enumerate(source['layers']) if l['name'] == '07-pale-hair-tie')
tie_mask = [px[3] > 0 for px in source['cels'][(0, tie_index)]['image'].get_flattened_data()]
result = native['compare'](HERE / 'pass-03-refined.aseprite', HERE / 'tie-edit-proof.aseprite', ['07-pale-hair-tie'], tie_mask)
assert result['passed'], result
assert sum(row['changed_pixels'] for row in result['layers']) > 0
with Image.open(HERE / 'tie-edit-proof.png') as a, Image.open(HERE / 'tie-edit-proof-reopened.png') as b:
    assert a.tobytes() == b.tobytes()
reports['tie-edit-proof'] = result
with Image.open(ROOT / 'docs/experiments/2026-10-27-reference-drift-audit/head-shoulders-features.png') as a, Image.open(HERE / 'baseline.png') as b:
    assert a.tobytes() == b.tobytes()
reports['baseline_preparation_visual_change'] = False
frozen = json.loads((HERE / 'frozen-inputs.json').read_text())
for entry in [frozen['baseline_original'], *frozen['approved_references']]:
    assert hashlib.sha256((ROOT / entry['path']).read_bytes()).hexdigest() == entry['sha256']
(HERE / 'native-checks.json').write_text(json.dumps(reports, indent=2) + '\n')
print('PASS: three native passes, stable palette/metadata, protected clothing, exact reopened exports, scoped tie edit, original-input hashes.')
