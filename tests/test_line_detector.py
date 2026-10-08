import sys
from pathlib import Path
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'demo'))
from line_detector import detect_line, direction
from make_samples import sample


class LineDetectorTests(unittest.TestCase):
    def test_left(self):
        result, _ = detect_line(sample('left'))
        self.assertEqual((result.status, direction(result)), ('ok', 'LEFT'))
        self.assertAlmostEqual(result.error, -0.5)

    def test_center(self):
        result, _ = detect_line(sample('center'))
        self.assertEqual((result.status, direction(result)), ('ok', 'STRAIGHT'))
        self.assertAlmostEqual(result.error, 0.0)

    def test_right(self):
        result, _ = detect_line(sample('right'))
        self.assertEqual(direction(result), 'RIGHT')
        self.assertAlmostEqual(result.error, 0.5)

    def test_missing_line_has_no_numeric_error(self):
        result, _ = detect_line(sample('no_line'))
        self.assertEqual((result.status, result.error, direction(result)), ('no_line', None, 'STOP'))

    def test_multiple_lines(self):
        result, _ = detect_line(sample('two_lines'))
        self.assertEqual((result.status, result.error, direction(result)), ('ambiguous', None, 'STOP'))

    def test_large_shadow(self):
        result, _ = detect_line(sample('shadow'))
        self.assertEqual((result.status, direction(result)), ('ambiguous', 'STOP'))

    def test_threshold_experiment(self):
        image = sample('dark_background')
        low, _ = detect_line(image, 80)
        high, _ = detect_line(image, 160)
        self.assertEqual((low.status, high.status), ('ok', 'ambiguous'))

    def test_small_noise_is_ignored(self):
        image = sample('center')
        image[180:182, 10:12] = 20
        result, _ = detect_line(image)
        self.assertEqual(direction(result), 'STRAIGHT')

    def test_roi_excludes_upper_object(self):
        image = sample('center')
        image[:80, :120] = 20
        result, _ = detect_line(image)
        self.assertEqual(direction(result), 'STRAIGHT')

    def test_invalid_inputs(self):
        for image in [None, np.zeros((4, 4), dtype=np.uint8), np.zeros((20, 20), dtype=float)]:
            with self.subTest(image_type=type(image)), self.assertRaises(ValueError):
                detect_line(image)


if __name__ == '__main__':
    unittest.main()
