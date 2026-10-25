"""Projected support memory and LP diagnostics against independent references."""

import sys
import unittest
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.foreclosure import (
    projected_foreclosure_profiles,
    suppression_profile,
)
from omega_cosmology.testbed.history import observed_history_law


class ForeclosureTests(unittest.TestCase):
    def test_projected_subset_matches_exhaustive_non_markov_words(self):
        p = np.array([[0.4, 0.2, 0.4], [0.1, 0.5, 0.4], [0.4, 0.5, 0.1]])
        q = np.array([[0.5, 0.5, 0], [0, 1, 0], [1, 0, 0.0]])
        labels = [0, 1, 0]
        mu = np.array([1.0, 0, 0])
        result = projected_foreclosure_profiles(
            p, p > 0, mu, q > 0, mu.astype(bool), labels, labels, [0, 1, 3, 5]
        )
        for n, row in result.items():
            ref = observed_history_law(p, mu, labels, n)
            cand = observed_history_law(q, mu, labels, n)
            exact = sum(v for k, v in ref.items() if k not in cand)
            self.assertAlmostEqual(row["reference_weight"], exact, places=12)
        self.assertGreater(result[5]["reference_weight"], 0)

    def test_structural_zero_does_not_use_numeric_cutoff(self):
        p = np.eye(2)
        full = np.ones((2, 2), bool)
        mu = np.array([1.0, 0])
        r = projected_foreclosure_profiles(
            p, full, mu, full, mu.astype(bool), [0, 1], [0, 1], [100000]
        )
        self.assertTrue(r[100000]["structurally_certified_zero"])
        self.assertEqual(r[100000]["reference_weight"], 0)

    def test_projection_can_hide_foreclosure_and_caps_are_explicit(self):
        p = np.full((2, 2), 0.5)
        q = np.eye(2, dtype=bool)
        mu = np.array([1.0, 0])
        full = projected_foreclosure_profiles(
            p, p > 0, mu, q, mu.astype(bool), [0, 1], [0, 1], [3]
        )
        merged = projected_foreclosure_profiles(
            p, p > 0, mu, q, mu.astype(bool), [0, 0], [0, 0], [3]
        )
        self.assertGreater(full[3]["reference_weight"], merged[3]["reference_weight"])
        with self.assertRaises(MemoryError):
            projected_foreclosure_profiles(
                p,
                p > 0,
                mu,
                q,
                mu.astype(bool),
                [0, 1],
                [0, 1],
                [3],
                max_workspace_bytes=1,
            )
        with self.assertRaises(ValueError):
            projected_foreclosure_profiles(
                p, p > 0, mu, q.astype(float), mu.astype(bool), [0, 1], [0, 1], [3]
            )

    def test_suppression_matches_independent_linear_program(self):
        reference = {"a": 0.4, "b": 0.4, "c": 0.2}
        candidate = {"a": 0, "b": 0.2, "c": 0.8}
        budgets = [0, 0.01, 0.2, 0.5, 1]
        rows = suppression_profile(reference, candidate, budgets)
        for e, row in zip(budgets, rows):
            lp = linprog(
                -np.array(list(reference.values())),
                A_ub=[list(candidate.values())],
                b_ub=[e],
                bounds=(0, 1),
                method="highs",
            )
            self.assertTrue(lp.success)
            self.assertAlmostEqual(row["max_reference_mass"], -lp.fun, places=12)
        diagonal = suppression_profile(reference, reference, budgets)
        for e, row in zip(budgets, diagonal):
            self.assertAlmostEqual(e, row["max_reference_mass"])
