"""Independent finite-history checks and counterexamples to unsafe verdicts."""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from omega_cosmology.testbed.history import history_profile
from omega_cosmology.testbed.profile_analysis import (
    contrast_tail,
    geometric_total,
    kernel_profile,
    state_dependent_stop,
    uniform_total,
)


def delayed_coin(delay=2):
    """Two absorbing bit outcomes; branch after delay deterministic steps."""
    p = np.zeros((delay + 3, delay + 3))
    for k in range(delay):
        p[k, k + 1] = 1
    p[delay, -2:] = 0.5
    p[-2, -2] = p[-1, -1] = 1
    return p


class ProfileTests(unittest.TestCase):
    def test_decomposition_does_not_alias_mutable_input(self):
        p = np.array([[0.5, 0.5], [0.5, 0.5]])
        profile = kernel_profile(p)
        p[0] = [1, 0]
        self.assertAlmostEqual(profile.at([1, 0], 2)["ell_bits"], 2)
        with self.assertRaises(ValueError):
            profile.p[0, 0] = 1
        with self.assertRaises(ValueError):
            profile.bias[0] = 100

    def test_reducible_bias_identity_and_independent_endings(self):
        p = delayed_coin()
        mu = np.eye(len(p))[0]
        profile = kernel_profile(p)
        direct = history_profile(p, mu, 30)
        for n, value in enumerate(direct):
            self.assertAlmostEqual(value, profile.at(mu, n)["ell_bits"], places=12)
        self.assertEqual(profile.closed_classes, 2)
        self.assertAlmostEqual(profile.coordinates(mu)["bias_offset_bits"], 1)
        self.assertAlmostEqual(
            uniform_total(profile, mu, 30)["ell_expected_bits"], direct.mean()
        )
        for mean in (0, 1, 10, 1000):
            rho = mean / (mean + 1)
            # Branch occurs on step3, so E[ell_N] = P(N>=3).
            self.assertAlmostEqual(
                geometric_total(profile, mu, mean)["ell_expected_bits"], rho**3
            )

    def test_periodic_offset_does_not_converge(self):
        p = np.array([[0, 0.5, 0.5], [1, 0, 0], [1, 0, 0]])
        mu = np.array([1, 0, 0])
        profile = kernel_profile(p)
        self.assertAlmostEqual(profile.coordinates(mu)["rate_bits_per_step"], 0.5)
        for n in range(20):
            self.assertAlmostEqual(profile.at(mu, n)["ell_bits"], (n + 1) // 2)
        self.assertGreater(abs(profile.at(mu, 20)["remainder_bits"]), 0.2)

    def test_multiple_recurrent_rates_use_absorption_weights(self):
        p = np.array(
            [[0, 0.25, 0.375, 0.375], [0, 1, 0, 0], [0, 0, 0.5, 0.5], [0, 0, 0.5, 0.5]]
        )
        mu = np.array([1, 0, 0, 0])
        profile = kernel_profile(p)
        self.assertAlmostEqual(profile.coordinates(mu)["rate_bits_per_step"], 0.75)
        self.assertAlmostEqual(
            profile.at(mu, 10)["ell_bits"], history_profile(p, mu, 10)[-1]
        )

    def test_line_crossing_not_unique_crossing(self):
        # A branches once immediately, waits, then generates one bit/step.
        p = np.zeros((12, 12))
        p[0, 1:3] = 0.5
        for i in range(1, 9):
            p[i, i + 2] = 1
        p[9:, 10:] = 0.5
        a = kernel_profile(p)
        # B gets two bits at steps2/3, then no more.
        q = np.zeros((8, 8))
        q[0, 1] = 1
        q[1, 2:4] = 0.5
        q[2:4, 4:8] = 0.25  # two bits here; makes intermediate reversal clear.
        for i in range(4, 8):
            q[i, i] = 1
        b = kernel_profile(q)
        ma, mb = np.eye(12)[0], np.eye(8)[0]
        delta = history_profile(p, ma, 30) - history_profile(q, mb, 30)
        signs = np.sign(delta[abs(delta) > 1e-8])
        self.assertEqual(np.count_nonzero(signs[1:] != signs[:-1]), 2)
        tail = contrast_tail(a, ma, b, mb)
        self.assertGreater(delta[tail["eventual_sign_from_step"]], 0)

    def test_positive_rate_bound_covers_every_later_step(self):
        p = np.array([[0.5, 0.5], [0.5, 0.5]])
        q = delayed_coin(0)
        a, b = kernel_profile(p), kernel_profile(q)
        ma, mb = np.array([1, 0]), np.array([1, 0, 0])
        start = contrast_tail(a, ma, b, mb)["eventual_sign_from_step"]
        for n in range(start, start + 20):
            self.assertGreater(a.at(ma, n)["ell_bits"] - b.at(mb, n)["ell_bits"], 0)

    def test_state_dependent_stopping_counts_termination(self):
        p = np.array([[0, 0.5, 0.5], [0, 1, 0], [0, 0, 1]])
        mu = np.array([1, 0, 0])
        # Half stop immediately; remainder branch, then certainly stop.
        result = state_dependent_stop(p, mu, [0.5, 1, 1])
        self.assertAlmostEqual(result["expected_transition_surprisal_bits"], 0.5)
        self.assertAlmostEqual(result["stopped_record_entropy_bits"], 1.5)
        self.assertAlmostEqual(result["expected_steps"], 0.5)
        self.assertFalse(result["independent_ending_formula_applicable"])

    def test_equal_endpoint_is_not_profile_dominance(self):
        p = delayed_coin(2)
        a = history_profile(p, np.eye(5)[0], 3)
        b = history_profile(p, np.eye(5)[2], 3)
        self.assertEqual(a[-1], b[-1])
        self.assertLess(a[1], b[1])
        # Positive mass at n=0 alone cannot make the earlier option strict.
        self.assertEqual(a[0], b[0])

    def test_invalid_inputs_and_non_stopping_class_rejected(self):
        for p in (
            np.array([[0.9]]),
            np.array([[float("nan")]]),
            np.array([[-0.1, 1.1], [1, 0]]),
        ):
            with self.assertRaises(ValueError):
                kernel_profile(p)
        p = np.eye(2)
        with self.assertRaises(ValueError):
            kernel_profile(p, structural_support=np.zeros((2, 2), dtype=bool))
        with self.assertRaises(MemoryError):
            kernel_profile(p, max_states=1)
        with self.assertRaises(ValueError):
            state_dependent_stop(p, [1, 0], [0, 1])
        with self.assertRaises(ValueError):
            uniform_total(kernel_profile(p), [1, 0], -1)


if __name__ == "__main__":
    unittest.main()
