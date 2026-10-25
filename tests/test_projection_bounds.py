"""Projection inequalities checked against exhaustive finite hidden-Markov words."""

import sys
import unittest
from itertools import pairwise
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from omega_cosmology.testbed.history import (
    entropy,
    history_profile,
    observed_history_law,
)
from omega_cosmology.testbed.projections import projected_history_bounds


class ProjectionBoundTests(unittest.TestCase):
    def test_memory_bounds_enclose_exact_nonmarkov_history_and_tighten(self):
        p = np.array([[0.6, 0.3, 0.1], [0.2, 0.4, 0.4], [0.1, 0.7, 0.2]])
        mu = np.array([1.0, 0, 0])
        labels = [0, 0, 1]
        exact = entropy(list(observed_history_law(p, mu, labels, 5).values()))
        bounds = [
            projected_history_bounds(p, mu, labels, 5, memory=m) for m in range(5)
        ]
        for r in bounds:
            self.assertLessEqual(r["lower_bits"], exact + 1e-12)
            self.assertGreaterEqual(r["upper_bits"], exact - 1e-12)
        self.assertTrue(
            all(a["upper_bits"] >= b["upper_bits"] - 1e-12 for a, b in pairwise(bounds))
        )
        self.assertTrue(
            all(a["lower_bits"] <= b["lower_bits"] + 1e-12 for a, b in pairwise(bounds))
        )
        self.assertAlmostEqual(bounds[-1]["lower_bits"], exact, places=12)
        self.assertAlmostEqual(bounds[-1]["upper_bits"], exact, places=12)
        self.assertGreater(bounds[0]["width_bits"], 0)

    def test_lumpable_projection_memory_one_is_exact(self):
        p = np.array([[0.5, 0.3, 0.2], [0.1, 0.7, 0.2], [0.3, 0.3, 0.4]])
        mu = np.array([1.0, 0, 0])
        labels = [0, 0, 1]
        exact = entropy(list(observed_history_law(p, mu, labels, 4).values()))
        r = projected_history_bounds(p, mu, labels, 4, memory=1)
        self.assertAlmostEqual(r["lower_bits"], exact, places=12)
        self.assertAlmostEqual(r["upper_bits"], exact, places=12)

    def test_full_projection_matches_whole_and_constant_projection_is_zero(self):
        p = np.array([[0.8, 0.2], [0.3, 0.7]])
        mu = np.array([1.0, 0])
        r = projected_history_bounds(p, mu, [0, 1], 12)
        self.assertEqual(r["lower_bits"], history_profile(p, mu, 12)[-1])
        z = projected_history_bounds(p, mu, [0, 0], 12)
        self.assertAlmostEqual(z["upper_bits"], 0)
        self.assertEqual(projected_history_bounds(p, mu, [0, 0], 0)["upper_bits"], 0)

    def test_caps_and_conditioning_are_not_silently_changed(self):
        p = np.array([[0.6, 0.3, 0.1], [0.2, 0.4, 0.4], [0.1, 0.7, 0.2]])
        with self.assertRaises(MemoryError):
            projected_history_bounds(p, [1, 0, 0], [0, 0, 1], 10, memory=5, max_words=4)
        with self.assertRaises(ValueError):
            projected_history_bounds(p, [0.5, 0.5, 0], [0, 0, 1], 10)

    def test_shared_assay_projection_matches_exhaustive_short_history(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.finite_study import evaluate_case
        from omega_cosmology.testbed.history import sampled_kernel
        from omega_cosmology.testbed.physical_modules import autocatalytic_ecology

        model = autocatalytic_ecology(
            [{"id": "A", "members": ["a", "b"], "access_member": "a"}]
        )
        root = (1, 0, 1, 1)
        fields = ["a", "b", "A.bank"]
        protocol = {
            "id": "projected-assay-test",
            "preparations": [
                {"id": "seed", "roots": [[root, 1]], "conditioning": "full_present"}
            ],
            "energy_per_root": str(model.energy(root)),
            "coordinate_order": [c.name for c in model.coordinates],
            "horizons": [0.5],
            "sufficiency": "Full declared Markov state",
            "boundary_scope": {"bath": "one"},
            "conserved": ["fixed slots"],
            "observables": [],
            "event_readouts": [],
            "scope": "test",
            "numerical": {
                "kernel_agreement_tolerance": 1e-12,
                "independent_history_tolerance": 1e-7,
            },
            "projected_histories": [
                {"id": "local", "coordinates": fields, "memory": 1}
            ],
        }
        result = evaluate_case(protocol, {"id": "test", "model": model.record()}, 0.25)
        compiled = enumerate_model(model, [root])
        mu = np.zeros(len(compiled.states))
        mu[compiled.index[root]] = 1
        labels = [tuple(s[model.indices[k]] for k in fields) for s in compiled.states]
        exact = entropy(
            list(
                observed_history_law(
                    sampled_kernel(compiled, 0.25), mu, labels, 2
                ).values()
            )
        )
        bound = result["rows"][0]["projected_histories"]["local"]
        self.assertAlmostEqual(bound["lower_bits"], exact, places=12)
        self.assertAlmostEqual(bound["upper_bits"], exact, places=12)
        self.assertEqual(bound["conditioning"], "full_present")

    def test_multi_horizon_traversal_matches_individual_queries(self):
        from omega_cosmology.testbed.projections import projected_history_profiles

        p = np.array([[0.6, 0.3, 0.1], [0.2, 0.4, 0.4], [0.1, 0.7, 0.2]])
        profile = projected_history_profiles(
            p, [1, 0, 0], [0, 0, 1], [0, 1, 3, 7], memory=2
        )
        for steps, value in profile.items():
            single = projected_history_bounds(p, [1, 0, 0], [0, 0, 1], steps, memory=2)
            self.assertAlmostEqual(value["lower_bits"], single["lower_bits"], places=12)
            self.assertAlmostEqual(value["upper_bits"], single["upper_bits"], places=12)


if __name__ == "__main__":
    unittest.main()
