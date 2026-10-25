"""Hidden-history filter identities and sampling against independent exact words."""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from omega_cosmology.testbed.filtering import (
    ProjectedFilter,
    memory1_entropy_control,
    paired_projected_history_estimate,
)
from omega_cosmology.testbed.history import entropy, observed_history_law


class FilterTests(unittest.TestCase):
    def setUp(self):
        self.p = np.array([[0.6, 0.3, 0.1], [0.2, 0.4, 0.4], [0.1, 0.7, 0.2]])
        self.q = np.array([[0.5, 0.3, 0.2], [0.2, 0.3, 0.5], [0.15, 0.65, 0.2]])
        self.labels = [0, 0, 1]
        self.mu = [1, 0, 0]

    def test_expected_predictive_sum_equals_exhaustive_nonmarkov_entropy(self):
        f = ProjectedFilter(
            self.p, self.mu, self.labels, (0, 1), max_workspace_bytes=100000
        )
        obs, belief = f.start(1)
        prefixes = [(1.0, obs, belief, 0.0)]
        for _ in range(5):
            following = []
            for mass, obs, belief, reward in prefixes:
                probabilities = f.predict(obs, belief)
                updated = reward + float(entropy(probabilities[0]))
                for y, probability in enumerate(probabilities[0]):
                    if probability:
                        next_obs = np.array([y])
                        posterior = f.condition(obs, belief, next_obs, probabilities)
                        following.append(
                            (mass * probability, next_obs, posterior, updated)
                        )
            prefixes = following
        expected = sum(mass * reward for mass, _, _, reward in prefixes)
        exact = entropy(
            list(observed_history_law(self.p, self.mu, self.labels, 5).values())
        )
        self.assertAlmostEqual(expected, exact, places=12)
        self.assertAlmostEqual(sum(mass for mass, *_ in prefixes), 1, places=12)

    def test_identical_laws_have_zero_paired_variance_and_reproduce_seed(self):
        args = ((self.p, self.mu, self.labels),) * 2 + ([0, 1, 5],)
        result = paired_projected_history_estimate(*args, samples=128, seed=91)
        self.assertEqual(
            result, paired_projected_history_estimate(*args, samples=128, seed=91)
        )
        for row in result.values():
            self.assertEqual(row["difference_estimate_bits"], 0)
            self.assertEqual(row["paired_standard_error_bits"], 0)
            self.assertEqual(row["approximate_t_interval_bits"], [0, 0])
        self.assertGreater(result[5]["distribution_free_hoeffding_interval_bits"][1], 0)

    def test_distinct_laws_estimate_exact_difference_and_report_uncertainty(self):
        result = paired_projected_history_estimate(
            (self.p, self.mu, self.labels),
            (self.q, self.mu, self.labels),
            [1, 3, 5],
            samples=8192,
            seed=812,
            batch_size=128,
        )
        for k, row in result.items():
            exact = sum(
                sign
                * entropy(
                    list(observed_history_law(p, self.mu, self.labels, k).values())
                )
                for sign, p in ((1, self.q), (-1, self.p))
            )
            self.assertLess(
                abs(row["difference_estimate_bits"] - exact),
                6 * row["paired_standard_error_bits"] + 1e-12,
            )
            self.assertEqual(row["samples"], 8192)
            self.assertIn("not_analytic", row["guarantee"])
            lo, hi = row["distribution_free_hoeffding_interval_bits"]
            self.assertLessEqual(lo, exact)
            self.assertGreaterEqual(hi, exact)

    def test_permuted_hidden_states_and_observation_names_preserve_pair(self):
        permutation = [2, 0, 1]
        q = self.p[np.ix_(permutation, permutation)]
        labels = [self.labels[i] for i in permutation]
        mu = np.array(self.mu)[permutation]
        row = paired_projected_history_estimate(
            (self.p, self.mu, self.labels),
            (q, mu, labels),
            [9],
            samples=64,
            seed=2,
        )[9]
        self.assertAlmostEqual(row["difference_estimate_bits"], 0, places=12)

    def test_caps_and_conditioning_rejected_without_changing_question(self):
        law = (self.p, self.mu, self.labels)
        with self.assertRaises(ValueError):
            paired_projected_history_estimate(
                law, law, [20], samples=100, seed=1, max_sample_steps=100
            )
        with self.assertRaises(MemoryError):
            paired_projected_history_estimate(
                law, law, [3], samples=100, seed=1, max_workspace_bytes=100
            )
        with self.assertRaises(ValueError):
            paired_projected_history_estimate(
                law, (self.p, [0.5, 0.5, 0], self.labels), [3], samples=100, seed=1
            )

    def test_control_mean_is_exact_observed_memory_upper_not_a_markov_claim(self):
        from omega_cosmology.testbed.projections import projected_history_bounds

        _, means = memory1_entropy_control(self.p, self.mu, self.labels, (0, 1), 8)
        bound = projected_history_bounds(self.p, self.mu, self.labels, 8, memory=1)
        self.assertAlmostEqual(means[8], bound["upper_bits"], places=12)
        exact = entropy(
            list(observed_history_law(self.p, self.mu, self.labels, 5).values())
        )
        self.assertGreater(means[5], exact)
        result = paired_projected_history_estimate(
            (self.p, self.mu, self.labels),
            (self.q, self.mu, self.labels),
            [5],
            samples=8192,
            seed=812,
            control_variate="memory1_exact_mean",
        )[5]
        difference = (
            entropy(
                list(observed_history_law(self.q, self.mu, self.labels, 5).values())
            )
            - exact
        )
        self.assertLess(
            abs(result["difference_estimate_bits"] - difference),
            6 * result["paired_standard_error_bits"] + 1e-12,
        )
        self.assertLess(
            result["paired_standard_error_bits"],
            result["uncontrolled_paired_standard_error_bits"],
        )


if __name__ == "__main__":
    unittest.main()
