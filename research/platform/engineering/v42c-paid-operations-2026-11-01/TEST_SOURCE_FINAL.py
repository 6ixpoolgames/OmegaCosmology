import unittest
from itertools import product

import numpy as np

from omega_cosmology.testbed.history import entropy
from omega_cosmology.testbed.phases import sampled_schedule_profiles
from omega_cosmology.testbed.spatial import spatial_world
from omega_cosmology.testbed.spatial_operations import (
    preparation_model,
    preparation_root,
)
from omega_cosmology.testbed.stream_schedule import stream_schedule


class OperationTests(unittest.TestCase):
    def test_common_present_and_paid_native_inverse(self):
        models = [preparation_model(spatial_world(), x) for x in ("idle", "aa", "ab")]
        roots = [preparation_root(m) for m in models]
        self.assertTrue(all(r == roots[0] for r in roots))
        self.assertTrue(all(m.energy(r) == 2 for m, r in zip(models, roots)))
        self.assertTrue(
            all(
                m.inventory(r) == models[0].inventory(roots[0])
                for m, r in zip(models, roots)
            )
        )
        for model, root in zip(models[1:], roots[1:]):
            strokes = [e for e in model.events(root) if e.rule_id.startswith("stroke.")]
            self.assertTrue(strokes)
            for e in strokes:
                self.assertEqual(e.delta_energy, -1.25)
                self.assertEqual(e.heat, 1.25)
                self.assertEqual(e.target[model.indices["bank"]], 0)
                reverse = next(
                    v
                    for v in model.events(e.target)
                    if v.rule_id == e.rule_id and v.direction == -1
                )
                self.assertEqual(reverse.target, root)
                self.assertEqual(reverse.delta_energy, 1.25)
                self.assertEqual(reverse.heat, -1.25)
                thermal = next(
                    v for v in model.events(e.target) if v.rule_id == "actuator.thermal"
                )
                self.assertEqual(thermal.heat, 0.25)
        self.assertTrue(
            any(e.rule_id == "actuator.thermal" for e in models[0].events(roots[0]))
        )

    def test_streamed_history_matches_words_and_retained_schedule(self):
        p = np.array([[0.7, 0.3], [0.2, 0.8]])
        q = np.array([[0.4, 0.6], [0.1, 0.9]])
        matrices = [p, p, q, q]
        probs = []
        for word in product(range(2), repeat=4):
            last, probability = 0, 1.0
            for matrix, x in zip(matrices, word):
                probability *= matrix[last, x]
                last = x
            probs.append(probability)
        result = stream_schedule(
            [(lambda: p.copy(), 2), (lambda: q.copy(), 2)], [1, 0], {0, 2, 4}
        )
        retained = sampled_schedule_profiles([(p, 2), (q, 2)], [1, 0], {0, 2, 4})
        self.assertAlmostEqual(
            result["checkpoints"][4]["ell_bits"], float(entropy(probs))
        )
        for t in (0, 2, 4):
            np.testing.assert_allclose(
                result["checkpoints"][t]["endpoint"], retained[t]["endpoint"]
            )
            self.assertAlmostEqual(
                result["checkpoints"][t]["ell_bits"], retained[t]["ell_bits"]
            )
        # Boundary endpoint entropy is not substituted for prefix history entropy.
        self.assertGreater(
            result["checkpoints"][4]["ell_bits"], entropy(retained[4]["endpoint"])
        )

    def test_no_score_and_invalid_schedule(self):
        p = np.array([[0.5, 0.5], [0.5, 0.5]])
        result = stream_schedule([(lambda: p, 1)], [1, 0], {1}, score_history=False)
        self.assertIsNone(result["checkpoints"][1]["ell_bits"])
        with self.assertRaises(ValueError):
            stream_schedule([(lambda: p, 0)], [1, 0], {0})
        with self.assertRaises(ValueError):
            stream_schedule([(lambda: p * 2, 1)], [1, 0], {1})

    def test_long_schedule_releases_kernel_and_meets_proposed_allowance(self):
        import weakref

        reference = []

        def first():
            p = np.array([[.3, .7], [.3, .7]])
            reference.append(weakref.ref(p))
            return p

        def second():
            self.assertIsNone(reference[0]())
            return np.array([[.3, .7], [.3, .7]])

        steps = 32768
        result = stream_schedule([(first, 128), (second, steps - 128)], [1, 0], {steps})
        expected = steps * float(entropy([.3, .7]))
        error = abs(result["checkpoints"][steps]["ell_bits"] - expected)
        self.assertLess(error, 1e-7 + 1e-9 * steps)


if __name__ == "__main__":
    unittest.main()
