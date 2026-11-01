"""Verify this audit's recorded sources and native edit proof, not likeness."""
from pathlib import Path
import json
import runpy

from PIL import Image

HERE = Path(__file__).resolve().parent
native = runpy.run_path(str(HERE.parents[2] / 'tools/check_native_pilot.py'))
source = HERE / 'head-shoulders-features.aseprite'
edit = HERE / 'head-shoulders-tie-edit-proof.aseprite'
doc = native['read'](source)
assert doc['canvas'] == [120, 112] and len(doc['layers']) == 10 and len(doc['frames']) == 1
index = next(i for i, layer in enumerate(doc['layers']) if layer['name'] == '07-pale-hair-tie')
mask = [p[3] > 0 for p in doc['cels'][(0, index)]['image'].get_flattened_data()]
result = native['compare'](source, edit, ['07-pale-hair-tie'], mask)
assert sum(row['changed_pixels'] for row in result['layers']) == 15
assert sum(row['protected_changed_pixels'] for row in result['layers']) == 0
# Preserve the strict reader's rejection; no palette/header exemption is added.
assert result['failures'] == ['header changed', 'frames changed']
for name, reopened in (
    ('head-shoulders-features', 'head-shoulders-features-reopen'),
    ('head-shoulders-tie-edit-proof', 'head-shoulders-tie-edit-proof-reopen'),
):
    with Image.open(HERE / f'{name}.png') as a, Image.open(HERE / f'{reopened}.png') as b:
        assert a.size == b.size == (120, 112)
        assert a.convert('RGBA').tobytes() == b.convert('RGBA').tobytes()
with Image.open(HERE / 'head-shoulders-features.png') as image:
    assert set(image.getchannel('A').get_flattened_data()) == {0, 255}
with Image.open(HERE / 'head-shoulders-blockout.png') as image:
    assert image.getchannel('A').getbbox() is None
before, after = source.read_bytes(), edit.read_bytes()
result.update({
    'fresh_reopen_exports_match': True,
    'source_canvas': [120, 112], 'source_layer_count': 10, 'source_frame_count': 1,
    'header_color_count_before': int.from_bytes(before[32:34], 'little'),
    'header_color_count_after': int.from_bytes(after[32:34], 'little'),
    'technical_edit_boundary': '15 tie-layer pixels only; native palette/header preservation fails',
    'artistic_assessment': 'rejected for likeness by agent; no user approval',
    'blank_first_export': 'detected and retained as rejected technical failure',
})
(HERE / 'native-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print('Reopen exports exact; only 15 tie pixels differ. Strict palette/header rejection retained. No likeness verdict automated.')
