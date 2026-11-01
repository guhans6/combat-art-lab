from pathlib import Path
import json
import sys
import subprocess
import tempfile
import unittest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from comparison_review import build_packet, verify_packet


class ComparisonReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.before = Image.new('RGBA', (8, 8), 'red')
        self.before.putpixel((7, 7), (0, 0, 255, 255))
        self.after = self.before.copy()
        self.after.putpixel((1, 1), (0, 0, 255, 255))
        self.after.putpixel((6, 6), (0, 0, 255, 255))
        self.before.save(self.root / 'before.png')
        self.after.save(self.root / 'after.png')
        mask = Image.new('L', (8, 8), 0)
        mask.putpixel((1, 1), 255)
        mask.save(self.root / 'mask.png')
        self.spec = {'baseline_role': 'test diagnostic', 'registration': 'same authored grid',
                     'required_frame_ids': ['F1'], 'frames': [
                         {'id': 'F1', 'before': 'before.png', 'after': 'after.png',
                          'mask': 'mask.png', 'regions': [{'name': 'target', 'crop': [0, 0, 3, 3]}]}],
                     'zoom': 2}

    def build(self, name='packet'):
        spec = self.root / f'{name}-spec.json'
        spec.write_text(json.dumps(self.spec))
        return build_packet(spec, self.root / name)

    def test_remote_edit_fails_scope_and_close_review_coverage(self):
        report = self.build()
        self.assertFalse(report['mechanical_passed'])
        frame = report['frames'][0]
        self.assertEqual(frame['checks']['outside_mask_changed_pixels'], 1)
        self.assertEqual(frame['uncovered_changes']['count'], 1)
        self.assertEqual(frame['uncovered_changes']['examples_xy'], [[6, 6]])
        self.assertEqual(report['visual_acceptance'], 'pending')

    def test_freshness_checks_sources_spec_evidence_and_generated_sheets(self):
        evidence = self.root / 'native-proof.txt'
        evidence.write_text('opaque test evidence; no native validity claim')
        self.spec['evidence'] = [{'role': 'test evidence', 'path': evidence.name}]
        report = self.build()
        packet = self.root / 'packet/packet.json'
        self.assertTrue(verify_packet(packet)['fresh'])
        paths = [self.root / 'after.png', self.root / 'packet-spec.json', evidence,
                 Path(report['sheets'][0]['path'])]
        for path in paths:
            old = path.read_bytes()
            path.write_bytes(old + b'changed')
            with self.subTest(path=path):
                check = verify_packet(packet)
                self.assertFalse(check['fresh'])
                self.assertIn(str(path), [f['path'] for f in check['stale_files']])
            path.write_bytes(old)

    def test_allowed_remote_change_still_needs_coverage_and_never_approves_art(self):
        with Image.open(self.root / 'mask.png') as im:
            mask = im.copy()
        mask.putpixel((6, 6), 255)
        mask.save(self.root / 'mask.png')
        narrow = self.build('narrow')
        self.assertTrue(narrow['frames'][0]['checks']['passed'])
        self.assertFalse(narrow['mechanical_passed'])
        self.spec['frames'][0]['regions'].append({'name': 'remote', 'crop': [5, 5, 8, 8]})
        complete = self.build('complete')
        self.assertTrue(complete['mechanical_passed'])
        self.assertEqual(complete['visual_acceptance'], 'pending')
        self.assertEqual(complete['user_approval'], 'pending')
        self.assertEqual(verify_packet(self.root / 'complete/packet.json')['visual_acceptance'], 'pending')

    def test_noop_is_not_improvement_and_invisible_rgb_still_invalidates_evidence(self):
        self.before.putpixel((0, 0), (1, 2, 3, 0))
        self.before.save(self.root / 'before.png')
        self.before.save(self.root / 'after.png')
        report = self.build()
        self.assertTrue(report['mechanical_passed'])
        self.assertEqual(report['frames'][0]['checks']['changed_pixels'], 0)
        changed = self.before.copy()
        changed.putpixel((0, 0), (4, 5, 6, 0))
        changed.save(self.root / 'after.png')
        self.assertFalse(verify_packet(self.root / 'packet/packet.json')['fresh'])

    def test_missing_frame_canvas_mismatch_and_invalid_crop_refuse_packet(self):
        self.spec['required_frame_ids'].append('F2')
        with self.assertRaises(ValueError):
            self.build('missing')
        self.spec['required_frame_ids'] = ['F1']
        self.spec['frames'][0]['regions'][0]['crop'] = [0, 0, 9, 8]
        with self.assertRaises(ValueError):
            self.build('crop')
        self.spec['frames'][0]['regions'][0]['crop'] = [0, 0, 3, 3]
        Image.new('RGBA', (9, 8), 'red').save(self.root / 'after.png')
        with self.assertRaisesRegex(ValueError, 'canvas mismatch'):
            self.build('canvas')
        for name in ('missing', 'crop', 'canvas'):
            self.assertFalse((self.root / name).exists())

    def test_existing_packet_is_preserved(self):
        self.build()
        packet = self.root / 'packet/packet.json'
        old = packet.read_bytes()
        with self.assertRaises(FileExistsError):
            build_packet(self.root / 'packet-spec.json', packet.parent)
        self.assertEqual(packet.read_bytes(), old)

    def test_cli_distinguishes_incomplete_build_freshness_and_invalid_spec(self):
        spec = self.root / 'cli-spec.json'
        spec.write_text(json.dumps(self.spec))
        script = Path(__file__).resolve().parents[1] / 'scripts/comparison_review.py'
        result = subprocess.run([sys.executable, str(script), 'build', '--spec', str(spec),
                                 '--out', str(self.root / 'cli')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        result = subprocess.run([sys.executable, str(script), 'verify', '--packet',
                                 str(self.root / 'cli/packet.json')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)['mechanical_passed'])
        self.assertEqual(json.loads(result.stdout)['visual_acceptance'], 'pending')
        self.spec['required_frame_ids'].append('missing')
        spec.write_text(json.dumps(self.spec))
        result = subprocess.run([sys.executable, str(script), 'build', '--spec', str(spec),
                                 '--out', str(self.root / 'invalid')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.root / 'invalid').exists())


if __name__ == '__main__':
    unittest.main()
