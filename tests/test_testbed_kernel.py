"""Independent checks of the physical grammar, reference queries and contracts."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

try:
    import numpy as np
    from scipy.linalg import expm
except ImportError:
    np = None


@unittest.skipIf(
    np is None, "Install the testbed extra to execute numerical conformance"
)
class KernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.models import calibration_world

        cls.model, cls.root = calibration_world()
        cls.compiled = enumerate_model(cls.model, [cls.root])

    def test_rule_record_roundtrip_and_motif_consequence(self):
        from omega_cosmology.testbed.physics import LocalModel

        model = LocalModel.from_record(json.loads(json.dumps(self.model.record())))
        self.assertEqual(model.fingerprint(), self.model.fingerprint())
        unbound = list(model.events((0, 1, 0)))
        bound = list(model.events((1, 1, 0)))
        self.assertFalse(any(e.rule_id == "unlock_motif" for e in unbound))
        self.assertTrue(any(e.rule_id == "unlock_motif" for e in bound))
        # The same motif at another bank state has the same local assisted rate.
        self.assertEqual(
            next(e.rate for e in bound if e.rule_id == "unlock_motif"),
            next(
                e.rate for e in model.events((1, 1, 2)) if e.rule_id == "unlock_motif"
            ),
        )

    def test_rate_dependencies_include_undeclared_energy_and_constraints(self):
        from omega_cosmology.testbed.physics import (
            Condition,
            Coordinate,
            EnergyTerm,
            LocalModel,
            Rule,
        )

        m = LocalModel(
            "coupled",
            [Coordinate("x", (0, 1), "material"), Coordinate("y", (0, 1), "record")],
            [Rule("change", (Condition("x", "eq", 0),), (("x", 1),), 0.1)],
            [EnergyTerm("1", "y", (Condition("x", "eq", 1),))],
        )
        first = next(m.events((0, 0)))
        second = next(m.events((0, 1)))
        self.assertEqual(first.support, ("x", "y"))
        self.assertNotEqual(first.rate, second.rate)

    def test_pair_ratios_and_first_law_independent(self):
        from omega_cosmology.testbed.physics import rational

        m = self.model
        for state in self.compiled.states:
            for event in m.events(state):
                reverse = next(
                    e
                    for e in m.events(event.target)
                    if e.rule_id == event.rule_id
                    and e.direction == -event.direction
                    and e.target == state
                )
                de = float(m.energy(event.target) - m.energy(state))
                self.assertAlmostEqual(event.work - event.heat, de, places=12)
                expected = (
                    m.log_degeneracy(event.target)
                    - m.log_degeneracy(state)
                    + m.beta * (event.work - de)
                )
                self.assertAlmostEqual(
                    np.log(event.rate / reverse.rate), expected, places=12
                )
        self.assertEqual(rational(".125") * 8, 1)

    def test_parallel_mechanisms_aggregate_but_ledgers_remain(self):
        c = self.compiled
        source = c.index[(0, 0, 0)]
        target = c.index[(0, 1, 0)]
        events = [e for i, j, e in c.ledger if i == source and j == target]
        self.assertEqual(len(events), 2)
        self.assertAlmostEqual(c.q[source, target], sum(e.rate for e in events))
        self.assertNotEqual(events[0].work, events[1].work)

    def test_source_off_reference_and_driven_energy_balance(self):
        from omega_cosmology.testbed.history import distributions_and_occupation
        from omega_cosmology.testbed.thermodynamics import audit_equilibrium, balance

        c = self.compiled
        self.assertEqual(audit_equilibrium(c)["status"], "passed")
        mu = np.zeros(len(c.states))
        mu[c.index[self.root]] = 1
        endpoint, occ = distributions_and_occupation(c, mu, 16)
        b = balance(c, mu, endpoint, occ)
        self.assertLess(abs(b["energy_residual"]), 1e-10)
        self.assertLess(b["availability_identity_residual"], 1e-11)
        self.assertGreaterEqual(b["entropy_production"], 0)

    def test_cap_is_incomplete_not_a_modified_law(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.history import sampled_kernel

        partial = enumerate_model(self.model, [self.root], max_states=2)
        self.assertFalse(partial.complete)
        self.assertIsNone(partial.q)
        self.assertTrue(partial.frontier)
        with self.assertRaises(ValueError):
            sampled_kernel(partial, 0.25)
        with self.assertRaises(MemoryError):
            sampled_kernel(self.compiled, 0.25, max_dense_bytes=8)

    def test_r1_r2_use_same_grammar_and_paid_capacity(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.models import enabling_world
        from omega_cosmology.testbed.thermodynamics import audit_equilibrium

        for expanded in (False, True):
            m, root = enabling_world(expansion=expanded)
            c = enumerate_model(m, [root], max_states=1000)
            self.assertTrue(c.complete)
            self.assertEqual(audit_equilibrium(c)["status"], "passed")
            if expanded:
                self.assertTrue(any(s[m.indices["bank"]] > 4 for s in c.states))
                self.assertTrue(
                    all(
                        s[m.indices["store.built"]] == 1
                        for s in c.states
                        if s[m.indices["bank"]] > 4
                    )
                )
                self.assertFalse(m.valid((1, 1, 1, 0, 5, 0)))
                build = next(
                    e
                    for e in m.events((1, 1, 1, 1, 2, 0))
                    if e.rule_id == "build_store_assisted" and e.direction == 1
                )
                self.assertEqual(build.target[m.indices["bank"]], 0)

    def test_symmetry_quotient_matches_observed_labelled_history(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.history import (
            entropy,
            history_profile,
            observed_history_law,
            sampled_kernel,
        )
        from omega_cosmology.testbed.models import two_copy_world
        from omega_cosmology.testbed.thermodynamics import audit_equilibrium

        a, root = two_copy_world(quotient=False)
        b, _ = two_copy_world(quotient=True)
        ca, cb = enumerate_model(a, [root]), enumerate_model(b, [root])
        self.assertEqual((len(ca.states), len(cb.states)), (4, 3))
        pa, pb = sampled_kernel(ca, 0.25), sampled_kernel(cb, 0.25)
        ma = np.zeros(4)
        ma[ca.index[root]] = 1
        mb = np.zeros(3)
        mb[cb.index[root]] = 1
        observed = observed_history_law(pa, ma, [sum(s) for s in ca.states], 4)
        self.assertAlmostEqual(
            float(entropy(list(observed.values()))),
            history_profile(pb, mb, 4)[-1],
            places=11,
        )
        self.assertEqual(b.canonical((1, 0)), b.canonical((0, 1)))
        self.assertEqual(audit_equilibrium(cb)["status"], "passed")

    def test_sampler_matches_exact_endpoint_and_path_energy(self):
        from omega_cosmology.testbed.backends import trajectory

        c = self.compiled
        exact = expm(c.q.toarray() * 2)[c.index[self.root]]
        rng = np.random.default_rng(1704)
        sample = np.zeros(len(c.states))
        for _ in range(1600):
            path = trajectory(self.model, self.root, 2, rng)
            self.assertTrue(path["complete"])
            sample[c.index[path["endpoint"]]] += 1
            de = float(
                self.model.energy(path["endpoint"]) - self.model.energy(self.root)
            )
            self.assertAlmostEqual(de, path["work"] - path["heat"], places=11)
        # Coordinate-wise six-sigma envelope, with binomial rare-bin allowance.
        allowed = 6 * np.sqrt(exact * (1 - exact) / 1600) + 6 / 1600
        self.assertTrue(np.all(abs(sample / 1600 - exact) < allowed))

    def test_unmarked_permutation_mid_history_adds_no_events(self):
        from omega_cosmology.testbed.backends import enumerate_model, trajectory
        from omega_cosmology.testbed.physics import (
            Condition,
            Coordinate,
            LocalModel,
            Rule,
        )

        m = LocalModel(
            "unmarked-swap",
            [Coordinate("a", (0, 1), "id"), Coordinate("b", (0, 1), "id")],
            [
                Rule(
                    "swap",
                    (Condition("a", "eq", 1), Condition("b", "eq", 0)),
                    (("a", -1), ("b", 1)),
                    0.1,
                )
            ],
            [],
            symmetry=((0, 1), (1, 0)),
        )
        c = enumerate_model(m, [(1, 0)])
        self.assertEqual(len(c.states), 1)
        self.assertEqual(float(c.q[0, 0]), 0)
        path = trajectory(m, (1, 0), 10, np.random.default_rng(1))
        self.assertEqual(path["jumps"], 0)

    def test_hidden_dissipative_permutation_rejected_consistently(self):
        from omega_cosmology.testbed.backends import enumerate_model, trajectory
        from omega_cosmology.testbed.physics import (
            Condition,
            Coordinate,
            LocalModel,
            Rule,
        )

        m = LocalModel(
            "bad-hidden-work",
            [Coordinate("a", (0, 1), "id"), Coordinate("b", (0, 1), "id")],
            [
                Rule(
                    "swap",
                    (Condition("a", "eq", 1), Condition("b", "eq", 0)),
                    (("a", -1), ("b", 1)),
                    0.1,
                    "1",
                )
            ],
            [],
            symmetry=((0, 1), (1, 0)),
        )
        with self.assertRaises(ValueError):
            enumerate_model(m, [(1, 0)])
        with self.assertRaises(ValueError):
            trajectory(m, (1, 0), 1, np.random.default_rng(1))


class ContractTests(unittest.TestCase):
    def test_metadata_roundtrip_and_invalid_combinations(self):
        from omega_cosmology.testbed.semantics import (
            ComparisonSpec,
            ObservationSpec,
            PresentSpec,
        )

        p = PresentSpec(
            "p", (((0,), 1.0),), sufficiency="All dependencies represented by one state"
        )
        self.assertEqual(
            PresentSpec(**json.loads(json.dumps(p.record()))).fingerprint(),
            p.fingerprint(),
        )
        with self.assertRaises(ValueError):
            PresentSpec(
                "p", (((0,), 1.0),), conditioning="own_present", sufficiency="state"
            )
        with self.assertRaises(ValueError):
            ComparisonSpec("x", "process", 1, 0.25, {"energy": "matched"})
        with self.assertRaises(ValueError):
            ObservationSpec(
                "x",
                ("a",),
                resolution={
                    "faithfulness": "open",
                    "certification": [{"refinement": "x"}],
                },
            )


if __name__ == "__main__":
    unittest.main()
