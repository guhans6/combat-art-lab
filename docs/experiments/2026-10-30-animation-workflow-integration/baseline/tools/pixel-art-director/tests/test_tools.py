from __future__ import annotations
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from pixel_checks import check_images, read_mask, mask_from_profile, review_sheet, safe_output, pixel_values
from prepare_run import prepare, verify
import doctor


class PixelChecksTests(unittest.TestCase):
    @patch('doctor.subprocess.run')
    def test_default_aseprite_inventory_never_launches_editor(self, run):
        report = doctor.aseprite_inventory(sys.executable)
        self.assertTrue(report['found'])
        self.assertEqual(report['version_probe'], 'not_run')
        self.assertIn('does not establish headless MCP readiness', report['version_probe_reason'])
        run.assert_not_called()

    @patch('doctor.subprocess.run')
    def test_explicit_aseprite_probe_keeps_direct_diagnostic(self, run):
        run.return_value = type('Result', (), {'returncode': 0, 'stdout': 'Aseprite X', 'stderr': ''})()
        report = doctor.aseprite_inventory(sys.executable, probe_version=True)
        self.assertEqual(report['version_probe'], 'completed')
        self.assertEqual(report['version_output'], 'Aseprite X')
        run.assert_called_once_with([sys.executable, '--version'], capture_output=True,
                                    text=True, timeout=15, check=False)
    def setUp(self):
        self.before = Image.new('RGBA', (8, 8), (0, 0, 0, 0))
        self.before.putpixel((3, 3), (20, 30, 40, 255))
        self.before.putpixel((4, 3), (80, 90, 100, 255))
        self.mask = [False] * 64
        self.mask[27] = True

    def test_in_scope_existing_color_passes(self):
        after = self.before.copy()
        after.putpixel((3, 3), (80, 90, 100, 255))
        report = check_images(self.before, after, self.mask)
        self.assertTrue(report['passed'])
        self.assertEqual(report['changed_pixels'], 1)

    def test_single_protected_pixel_fails(self):
        after = self.before.copy()
        after.putpixel((4, 3), (20, 30, 40, 255))
        report = check_images(self.before, after, self.mask)
        self.assertIn('protected_pixels_changed', report['failures'])
        self.assertEqual(report['outside_mask_changed_pixels'], 1)

    def test_new_color_fails(self):
        after = self.before.copy()
        after.putpixel((3, 3), (3, 4, 5, 255))
        self.assertIn('new_visible_colors', check_images(self.before, after, self.mask)['failures'])

    def test_partial_alpha_fails(self):
        after = self.before.copy()
        after.putpixel((3, 3), (20, 30, 40, 127))
        self.assertIn('partial_alpha', check_images(self.before, after, self.mask)['failures'])

    def test_canvas_change_fails(self):
        self.assertFalse(check_images(self.before, Image.new('RGBA', (9, 8)), self.mask)['passed'])

    def test_noop_not_claimed_as_edit(self):
        self.assertIn('no_visible_change', check_images(self.before, self.before, self.mask)['failures'])
        self.assertTrue(check_images(self.before, self.before, self.mask, require_change=False)['passed'])

    def test_hidden_rgb_not_visible_diff(self):
        after = self.before.copy()
        after.putpixel((0, 0), (255, 0, 0, 0))
        self.assertEqual(check_images(self.before, after, self.mask)['changed_pixels'], 0)

    def test_blank_sprite_fails(self):
        report = check_images(self.before, Image.new('RGBA', (8, 8)), [True] * 64)
        self.assertIn('empty_sprite', report['failures'])

    def test_mask_rejects_gray(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'mask.png'
            m = Image.new('L', (8, 8), 0)
            m.putpixel((3, 3), 128)
            m.save(path)
            with self.assertRaises(ValueError): read_mask(path, (8, 8))

    def test_mask_rejects_all_editable(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'mask.png'
            Image.new('L', (8, 8), 255).save(path)
            with self.assertRaises(ValueError): read_mask(path, (8, 8))

    def test_v03_neck_notch(self):
        profile = json.loads((ROOT / 'assets/combat-art-lab-v03.json').read_text())
        m = mask_from_profile(profile)
        self.assertEqual(m.size, (128, 192))
        self.assertEqual(sum(v == 255 for v in pixel_values(m)), 1316)
        self.assertEqual(m.getpixel((57, 29)), 0)
        self.assertEqual(m.getpixel((65, 30)), 0)
        self.assertEqual(m.getpixel((66, 30)), 255)
        self.assertEqual(m.getpixel((79, 30)), 255)
        self.assertEqual(m.getpixel((80, 30)), 0)

    def test_preview_and_no_input_overwrite(self):
        before_bytes = self.before.tobytes()
        result = review_sheet(self.before, self.before, (2, 2, 6, 6), 8)
        self.assertGreater(result.width, self.before.width)
        self.assertEqual(self.before.tobytes(), before_bytes)
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'source.png'
            with self.assertRaises(ValueError): safe_output(p, [p])


class FrozenRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        # Synthetic bytes test file freezing, NOT Aseprite compatibility.
        (self.repo / 'base.aseprite').write_bytes(b'synthetic-native-placeholder')
        Image.new('RGBA', (8, 8), (1, 2, 3, 255)).save(self.repo / 'base.png')
        Image.new('RGBA', (8, 8), (1, 2, 3, 255)).save(self.repo / 'ref.png')
        self.profile = self.root / 'profile.json'
        self.profile.write_text(json.dumps({
            'task_id': 'synthetic-test', 'canvas': [8, 8],
            'baseline_source': 'base.aseprite', 'baseline_png': 'base.png',
            'references': [{'role': 'primary-face', 'path': 'ref.png'}],
            'editable_region': {'include_rects': [[2, 2, 6, 6]], 'exclude_rects': []},
            'budget': {'max_visual_revision_passes': 3}
        }))

    def tearDown(self):
        self.tmp.cleanup()

    def make_run(self, name='test-01'):
        return prepare(self.repo, self.root / 'runs', name, self.profile, 'test-model', 'test-host', 'pebbly')

    def test_freeze_and_verify(self):
        run = self.make_run()
        self.assertTrue(verify(run)['passed'])
        self.assertEqual(json.loads((run / 'run.json').read_text())['state'], 'prepared_not_executed')
        (run / 'work/candidate.aseprite').write_bytes(b'edited-working-copy')
        self.assertTrue(verify(run)['passed'])

    def test_detect_original_changed(self):
        run = self.make_run()
        (self.repo / 'base.aseprite').write_bytes(b'changed')
        self.assertFalse(verify(run)['passed'])

    def test_detect_copy_changed(self):
        run = self.make_run()
        (run / 'input/baseline.png').write_bytes(b'changed')
        self.assertFalse(verify(run)['passed'])

    def test_duplicate_run_rejected(self):
        self.make_run()
        with self.assertRaises(FileExistsError): self.make_run()

    def test_unsafe_id_rejected(self):
        with self.assertRaises(ValueError): self.make_run('../escape')

    def test_native_resolution_not_rescaled(self):
        Image.new('RGBA', (16, 16)).save(self.repo / 'base.png')
        with self.assertRaises(ValueError): self.make_run()

    def test_custom_profile_brief_uses_its_task_and_reference_roles(self):
        self.profile.write_text(json.dumps({
            'task_id': 'custom-expression-repair', 'canvas': [8, 8],
            'baseline_source': 'base.aseprite', 'baseline_png': 'base.png',
            'references': [{'role': 'expression', 'path': 'ref.png'}],
            'editable_region': {'include_rects': [[1, 1, 7, 7]], 'exclude_rects': []},
            'budget': {'max_visual_revision_passes': 1}
        }))
        brief = (self.make_run('custom-profile') / 'BRIEF.md').read_text()
        self.assertIn('Task: custom-expression-repair', brief)
        self.assertIn('expression: input/reference-00-expression.png', brief)
        self.assertNotIn('standing-v03', brief)
        self.assertNotIn('Keep the neck', brief)


if __name__ == '__main__':
    unittest.main(verbosity=2)
