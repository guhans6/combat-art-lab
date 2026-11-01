import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

SPEC = importlib.util.spec_from_file_location('reference_lab', Path(__file__).parents[1] / 'scripts/reference_lab.py')
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


class ReferenceLabTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / 'source.png'
        image = Image.new('RGBA', (8, 8), (0, 0, 0, 0))
        for y in range(2, 6):
            for x in range(2, 6):
                image.putpixel((x, y), (180 + 10 * (x % 2), 70 + 10 * (y % 2), 20, 255))
        image.save(self.source)
        self.original_sha = lab.sha256(self.source)

    def tearDown(self):
        self.assertEqual(lab.sha256(self.source), self.original_sha)
        self.temp.cleanup()

    def config(self, **changes):
        config = {'canvas': [12, 12], 'scale': 1, 'target_anchor': [6, 6], 'require_transparent': True,
                  'frames': [{'id': 'one', 'path': 'source.png', 'source_anchor': [4, 4],
                              'motion_offset': [0, 0], 'duration_ms': 100}]}
        config.update(changes)
        p = self.root / 'layout.json'
        p.write_text(json.dumps(config))
        return p

    def test_inspect_alpha_and_bounds(self):
        data = lab.inspect_image(self.source)
        self.assertEqual(data['dimensions'], [8, 8])
        self.assertEqual(data['fully_transparent_pixels'], 48)
        self.assertEqual(data['alpha_bbox_xyxy'], (2, 2, 6, 6))

    def test_seeds_dimensions(self):
        data = lab.make_seeds(self.source, self.root / 'seeds', [(4, 4), (2, 2)], colors=2)
        self.assertEqual([x['dimensions'] for x in data['outputs']], [[4, 4], [2, 2]])
        self.assertTrue(all(x['visible_rgb_colors'] <= 2 for x in data['outputs']))

    def test_existing_output_rejected(self):
        out = self.root / 'already'; out.mkdir()
        with self.assertRaises(FileExistsError):
            lab.make_seeds(self.source, out, [(4, 4)])
        self.assertEqual(list(out.iterdir()), [])

    def test_aspect_distortion_rejected(self):
        with self.assertRaises(ValueError):
            lab.make_seeds(self.source, self.root / 'bad', [(4, 3)])
        self.assertFalse((self.root / 'bad').exists())

    def test_out_of_bounds_crop_rejected(self):
        with self.assertRaises(ValueError):
            lab.make_seeds(self.source, self.root / 'bad', [(4, 4)], crop=[0, 0, 9, 9])

    def test_duplicate_sizes_rejected(self):
        with self.assertRaises(ValueError):
            lab.make_seeds(self.source, self.root / 'bad', [(4, 4), (4, 4)])

    def test_wrong_mask_size_rejected(self):
        mask = self.root / 'mask.png'; Image.new('L', (4, 4), 255).save(mask)
        with self.assertRaises(ValueError):
            lab.make_seeds(self.source, self.root / 'bad', [(4, 4)], mask_path=mask)

    def test_mask_coverage_applied(self):
        mask = self.root / 'mask.png'
        im = Image.new('L', (8, 8), 0)
        for y in range(8):
            for x in range(4): im.putpixel((x, y), 255)
        im.save(mask)
        data = lab.make_seeds(self.source, self.root / 'masked', [(8, 8)], mask_path=mask, method='NEAREST')
        self.assertEqual(data['outputs'][0]['fully_opaque_pixels'], 8)

    def test_empty_mask_rejected(self):
        mask = self.root / 'empty.png'; Image.new('L', (8, 8), 0).save(mask)
        with self.assertRaises(ValueError):
            lab.make_seeds(self.source, self.root / 'bad', [(4, 4)], mask_path=mask)

    def test_premultiplied_filter_avoids_hidden_blue(self):
        im = Image.new('RGBA', (2, 1)); im.putdata([(255, 0, 0, 255), (0, 0, 255, 0)])
        result = lab.resize_rgba(im, (1, 1), 'BOX').getpixel((0, 0))
        self.assertEqual(result[:3], (255, 0, 0))
        self.assertIn(result[3], (127, 128))

    def test_threshold_is_explicit_binary(self):
        p = self.root / 'partial.png'; Image.new('RGBA', (8, 8), (120, 80, 60, 100)).save(p)
        data = lab.make_seeds(p, self.root / 'threshold', [(4, 4)], alpha_threshold=128)
        self.assertEqual(data['outputs'][0]['fully_transparent_pixels'], 16)
        self.assertEqual(data['outputs'][0]['partial_alpha_pixels'], 0)

    def test_partial_alpha_preserved_by_default(self):
        p = self.root / 'partial.png'; Image.new('RGBA', (8, 8), (120, 80, 60, 100)).save(p)
        data = lab.make_seeds(p, self.root / 'partial-out', [(4, 4)])
        self.assertEqual(data['outputs'][0]['partial_alpha_pixels'], 16)

    def test_shared_palette_budget(self):
        data = lab.make_seeds(self.source, self.root / 'palette', [(8, 8), (4, 4)], colors=3)
        palette = {tuple(c) for c in data['palette_rgb']}
        for item in data['outputs']:
            im = Image.open(self.root / 'palette' / item['file'])
            reader = getattr(im, 'get_flattened_data', None)
            pixels = reader() if reader is not None else im.getdata()
            self.assertTrue({p[:3] for p in pixels if p[3]}.issubset(palette))

    def test_normalization_anchor(self):
        result = lab.normalize_frames(self.config(), self.root / 'norm')
        self.assertEqual(result['frames'][0]['realized_anchor'], [6.0, 6.0])
        self.assertEqual(result['frames'][0]['alpha_bbox_xyxy'], (4, 4, 8, 8))

    def test_motion_offsets_not_erased(self):
        frames = [{'id': 'one', 'path': 'source.png', 'source_anchor': [4, 4], 'duration_ms': 100},
                  {'id': 'two', 'path': 'source.png', 'source_anchor': [4, 4],
                   'motion_offset': [2, -2], 'duration_ms': 120}]
        result = lab.normalize_frames(self.config(frames=frames), self.root / 'motion')
        self.assertEqual(result['frames'][1]['realized_anchor'], [8.0, 4.0])
        self.assertEqual(result['frames'][1]['alpha_bbox_xyxy'], (6, 2, 10, 6))

    def test_common_scale_does_not_fit_independent_boxes(self):
        narrow = self.root / 'narrow.png'; im = Image.open(self.source).copy()
        for y in range(8):
            for x in range(4, 8): im.putpixel((x, y), (0, 0, 0, 0))
        im.save(narrow)
        frames = [{'id': 'a', 'path': 'source.png', 'source_anchor': [4, 4], 'duration_ms': 100},
                  {'id': 'b', 'path': 'narrow.png', 'source_anchor': [4, 4], 'duration_ms': 100}]
        result = lab.normalize_frames(self.config(frames=frames), self.root / 'common')
        bounds = [f['alpha_bbox_xyxy'] for f in result['frames']]
        self.assertEqual([b[2]-b[0] for b in bounds], [4, 2])

    def test_visible_clipping_rejected_before_write(self):
        path = self.config(target_anchor=[0, 0])
        with self.assertRaises(ValueError): lab.normalize_frames(path, self.root / 'bad')
        self.assertFalse((self.root / 'bad').exists())

    def test_opaque_frame_rejected_when_requested(self):
        opaque = self.root / 'opaque.png'; Image.new('RGBA', (8, 8), 'red').save(opaque)
        frames = [{'id': 'a', 'path': 'opaque.png', 'source_anchor': [4, 4], 'duration_ms': 100}]
        with self.assertRaises(ValueError): lab.normalize_frames(self.config(frames=frames), self.root / 'bad')

    def test_invalid_duration_rejected(self):
        frames = [{'id': 'a', 'path': 'source.png', 'source_anchor': [4, 4], 'duration_ms': 0}]
        with self.assertRaises(ValueError): lab.normalize_frames(self.config(frames=frames), self.root / 'bad')

    def test_source_anchor_coordinates_after_crop(self):
        frames = [{'id': 'a', 'path': 'source.png', 'crop': [2, 2, 6, 6],
                   'source_anchor': [4, 4], 'duration_ms': 100}]
        result = lab.normalize_frames(self.config(frames=frames, require_transparent=False), self.root / 'cropped')
        self.assertEqual(result['frames'][0]['realized_anchor'], [6.0, 6.0])

    def test_unsafe_id_rejected(self):
        frames = [{'id': '../escape', 'path': 'source.png', 'source_anchor': [4, 4], 'duration_ms': 100}]
        with self.assertRaises(ValueError): lab.normalize_frames(self.config(frames=frames), self.root / 'bad')

    def test_invalid_scale_rejected(self):
        with self.assertRaises(ValueError): lab.normalize_frames(self.config(scale=0), self.root / 'bad')

    def test_frame_output_overwrite_rejected(self):
        config = self.config(); out = self.root / 'out'; out.mkdir()
        with self.assertRaises(FileExistsError): lab.normalize_frames(config, out)

    def test_empty_frame_rejected(self):
        p = self.root / 'empty.png'; Image.new('RGBA', (8, 8)).save(p)
        frames = [{'id': 'a', 'path': 'empty.png', 'source_anchor': [4, 4], 'duration_ms': 100}]
        with self.assertRaises(ValueError): lab.normalize_frames(self.config(frames=frames), self.root / 'bad')


if __name__ == '__main__':
    unittest.main()
