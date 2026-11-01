from pathlib import Path
import sys
import unittest
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import pixel_checks

class AlphaCoverageTests(unittest.TestCase):
    def test_actual_cuff_fixture_fails(self):
        image = Image.open(Path(__file__).parent / "fixtures/denim-hole-3x3.png")
        report = pixel_checks.check_alpha_coverage(image)
        self.assertFalse(report["passed"])
        self.assertEqual(report["hole_pixels_xy"], [[1, 1]])

    def test_repaired_fixture_passes(self):
        image = Image.open(Path(__file__).parent / "fixtures/denim-hole-3x3.png").convert("RGBA")
        image.putpixel((1, 1), (55, 50, 54, 255))
        self.assertTrue(pixel_checks.check_alpha_coverage(image)["passed"])

    def test_leg_gap_connected_to_exterior_is_allowed(self):
        image = Image.new("RGBA", (7, 7), (90, 90, 108, 255))
        for y in range(3, 7): image.putpixel((3, y), (0, 0, 0, 0))
        self.assertTrue(pixel_checks.check_alpha_coverage(image)["passed"])

    def test_exact_reviewed_hole_is_allowed(self):
        image = Image.open(Path(__file__).parent / "fixtures/denim-hole-3x3.png")
        self.assertTrue(pixel_checks.check_alpha_coverage(image, allowed_holes={(1, 1)})["passed"])

    def test_roi_does_not_turn_external_gap_into_hole(self):
        image = Image.new("RGBA", (7, 7), (90, 90, 108, 255))
        for y in range(3, 7): image.putpixel((3, y), (0, 0, 0, 0))
        self.assertTrue(pixel_checks.check_alpha_coverage(image, region=(1, 1, 6, 6))["passed"])

    def test_solid_mask_catches_open_edge_loss(self):
        image = Image.new("RGBA", (4, 4), (90, 90, 108, 255))
        image.putpixel((0, 2), (0, 0, 0, 0))
        mask = Image.new("L", image.size, 0)
        mask.putpixel((0, 2), 255)
        self.assertEqual(pixel_checks.check_alpha_coverage(image, solid_mask=mask)["missing_solid_pixels_xy"], [[0, 2]])

    def test_region_and_mask_dimensions_are_validated(self):
        image = Image.new("RGBA", (4, 4), (90, 90, 108, 255))
        with self.assertRaises(ValueError): pixel_checks.check_alpha_coverage(image, region=(0, 0, 5, 4))
        with self.assertRaises(ValueError): pixel_checks.check_alpha_coverage(image, solid_mask=Image.new("L", (3, 3)))

    def test_colored_background_cannot_hide_alpha_damage(self):
        image = Image.open(Path(__file__).parent / "fixtures/denim-hole-3x3.png")
        for color in [(255, 0, 255, 255), (206, 129, 40, 255)]:
            display = Image.new("RGBA", image.size, color)
            display.alpha_composite(image.convert("RGBA"))
            self.assertFalse(pixel_checks.check_alpha_coverage(image)["passed"])

if __name__ == "__main__": unittest.main()
