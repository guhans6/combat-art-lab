from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from reference_review import create_review


class ReferenceReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.ref, self.cand = self.root / "original.png", self.root / "candidate.png"
        Image.new("RGBA", (8, 8), "red").save(self.ref)
        Image.new("RGBA", (4, 8), "blue").save(self.cand)
        self.out = self.root / "review.png"

    def test_real_source_and_candidate_pixels_in_separate_panels(self):
        before = [p.read_bytes() for p in (self.ref, self.cand)]
        info = create_review(self.ref, self.cand, self.out, candidate_zoom=2)
        with Image.open(self.out) as image:
            self.assertEqual(image.getpixel((16, 72)), (255, 0, 0))
            self.assertEqual(image.getpixel((48, 72)), (0, 0, 255))
        self.assertEqual([p.read_bytes() for p in (self.ref, self.cand)], before)
        self.assertEqual(info["panels"][0]["sha256"], hashlib.sha256(before[0]).hexdigest())
        self.assertEqual(info["panels"][1]["display_size"], [8, 16])
        self.assertEqual(json.loads(self.out.with_suffix('.json').read_text()), info)

    def test_crop_and_no_reference_resampling_when_sizes_match(self):
        info = create_review(self.ref, self.cand, self.out, [2, 0, 6, 8], candidate_zoom=1)
        self.assertEqual(info["panels"][0]["crop_xyxy_half_open"], [2, 0, 6, 8])
        self.assertEqual(info["panels"][0]["resampling"], "none")

    def test_bad_crop_rejected(self):
        for box in ([0, 0, 9, 8], [-1, 0, 4, 8], [4, 0, 4, 8]):
            with self.subTest(box=box), self.assertRaises(ValueError):
                create_review(self.ref, self.cand, self.out, box)
        self.assertFalse(self.out.exists())

    def test_existing_evidence_and_inputs_protected(self):
        create_review(self.ref, self.cand, self.out)
        for target in (self.out, self.ref, self.cand):
            with self.subTest(target=target), self.assertRaises(FileExistsError):
                create_review(self.ref, self.cand, target)

    def test_one_image_cannot_fill_both_roles(self):
        with self.assertRaises(ValueError):
            create_review(self.ref, self.ref, self.out)

    def test_fractional_candidate_zoom_rejected(self):
        with self.assertRaises(ValueError):
            create_review(self.ref, self.cand, self.out, candidate_zoom=1.5)


if __name__ == "__main__":
    unittest.main()
