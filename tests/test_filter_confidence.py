"""Confidence accounting independent of the sign of a research comparison."""

import math
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.filtering import (
    empirical_bernstein_radius,
    paired_projected_history_estimate,
)


class ConfidenceTests(unittest.TestCase):
    def test_two_tail_constant_and_range_not_observed_range(self):
        r = empirical_bernstein_radius(0, 100, 20, 0.05)
        self.assertAlmostEqual(r, 7 * 20 * math.log(80) / (3 * 99))
        self.assertGreater(r, 0)  # Constant observed samples don't prove zero variance.
        self.assertGreater(empirical_bernstein_radius(0, 100, 20, 0.05 / 6), r)
        with self.assertRaises(ValueError):
            empirical_bernstein_radius(0, 1, 20, 0.05)

    def test_family_coverage_and_zero_step_support(self):
        p = np.array([[0.7, 0.3], [0.2, 0.8]])
        law = p, [1, 0], [0, 1]
        result = paired_projected_history_estimate(
            law, law, [0, 2], samples=32, seed=31, confidence_family_size=6
        )
        self.assertEqual(result[0]["empirical_bernstein_family_interval_bits"], [0, 0])
        self.assertEqual(result[2]["empirical_bernstein_family_size"], 6)
        self.assertEqual(result[2]["bounded_paired_score_support_width_bits"], 4)
        with self.assertRaises(ValueError):
            paired_projected_history_estimate(
                law, law, [1, 2], samples=32, seed=1, confidence_family_size=1
            )
