"""Synthetic checks only: do not open benchmark outcomes in unit tests."""
import unittest
import numpy as np
from scipy.stats import pearsonr

class MetricOrientationTest(unittest.TestCase):
    def test_identical_delta_has_best_correlation(self):
        a = np.array([1.0, 0.0, -1.0, 2.0])
        self.assertAlmostEqual(float(pearsonr(a, a).statistic), 1.0)
        self.assertAlmostEqual(float(pearsonr(a, -a).statistic), -1.0)

if __name__ == '__main__':
    unittest.main()
