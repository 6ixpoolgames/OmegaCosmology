import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
try:
    import numpy as np
except ImportError:
    np = None


@unittest.skipIf(np is None, "Install testbed extra")
class QueryTests(unittest.TestCase):
    def test_numeric_probability_is_not_a_structural_support_certificate(self):
        from omega_cosmology.testbed.history import entropy, full_state_foreclosure

        with self.assertRaises(ValueError):
            full_state_foreclosure(
                np.eye(2), np.eye(2), np.array([1.0, 0]), np.array([True, False]), 2
            )
        with self.assertRaises(ArithmeticError):
            entropy([float("nan"), 1.0])

    def test_projection_cannot_resolve_unmarked_copy_identity(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.history import evaluate_history
        from omega_cosmology.testbed.models import two_copy_world
        from omega_cosmology.testbed.semantics import (
            ComparisonSpec,
            LawSpec,
            ObservationSpec,
            PresentSpec,
            QuantitySpec,
        )

        model, root = two_copy_world(quotient=True)
        compiled = enumerate_model(model, [root])
        with self.assertRaises(ValueError):
            evaluate_history(
                compiled,
                PresentSpec("p", ((root, 1.0),), sufficiency="Full unmarked state"),
                LawSpec("law", model.fingerprint(), {"bath": "one"}),
                ObservationSpec("bad", ("first",), scope="projected_history"),
                ComparisonSpec("q", "single_query", 1, 0.25, {"law": "one"}),
                QuantitySpec("h", "history entropy", "bits", "full_present"),
            )

    def test_mutated_compilation_cannot_silently_change_the_queried_law(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.models import calibration_world

        m, root = calibration_world()
        c = enumerate_model(m, [root])
        c.q.data[0] += 0.01
        with self.assertRaises(ValueError):
            c.require_complete()

    def test_reference_suite(self):
        from omega_cosmology.testbed.conformance import run_reference_cases

        self.assertEqual(len(run_reference_cases()), 12)

    def test_query_contract_binds_executing_law_and_scope(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.history import evaluate_history
        from omega_cosmology.testbed.models import calibration_world
        from omega_cosmology.testbed.semantics import (
            ComparisonSpec,
            LawSpec,
            ObservationSpec,
            PresentSpec,
            QuantitySpec,
        )

        m, root = calibration_world()
        c = enumerate_model(m, [root])
        p = PresentSpec(
            "root", ((root, 1.0),), sufficiency="All declared dependencies retained"
        )
        law = LawSpec("r0", m.fingerprint(), {"bath": "single", "source": "maintained"})
        obs = ObservationSpec("all", tuple(x.name for x in m.coordinates))
        cmp = ComparisonSpec("one", "single_query", 1, 0.25, {"law": "self"})
        qty = QuantitySpec("history.full", "H(X1,...,Xn|X0)", "bits", "full_present")
        result = evaluate_history(c, p, law, obs, cmp, qty)
        self.assertGreater(result["ell_bits"], 0)
        with self.assertRaises(ValueError):
            evaluate_history(c, p, law, ObservationSpec("bad", ("bank",)), cmp, qty)
        with self.assertRaises(ValueError):
            evaluate_history(
                c, p, LawSpec("bad", "wrong", {"source": "same"}), obs, cmp, qty
            )

    def test_mixture_query_does_not_add_root_entropy_twice(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.history import evaluate_history
        from omega_cosmology.testbed.physics import Coordinate, LocalModel
        from omega_cosmology.testbed.semantics import (
            ComparisonSpec,
            LawSpec,
            ObservationSpec,
            PresentSpec,
            QuantitySpec,
        )

        m = LocalModel("frozen", [Coordinate("x", (0, 1), "record")], [], [])
        c = enumerate_model(m, [(0,), (1,)])
        law = LawSpec("frozen", m.fingerprint(), {"source": "none"})
        cmp = ComparisonSpec("one", "single_query", 1, 0.25, {"law": "self"})
        for conditioning, expected in [
            ("root_conditioned_average", 0),
            ("unobserved_root_mixture", 1),
        ]:
            p = PresentSpec(
                "p",
                (((0,), 0.5), ((1,), 0.5)),
                conditioning=conditioning,
                sufficiency="Frozen full state",
            )
            o = ObservationSpec("all", ("x",), conditioning=conditioning)
            q = QuantitySpec(
                "history." + conditioning, "future history", "bits", conditioning
            )
            self.assertAlmostEqual(
                evaluate_history(c, p, law, o, cmp, q)["ell_bits"], expected
            )

    def test_unresolved_degeneracy_is_not_history_entropy(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.history import history_profile, sampled_kernel
        from omega_cosmology.testbed.physics import Coordinate, EnergyTerm, LocalModel

        m = LocalModel(
            "unresolved",
            [Coordinate("x", (0,), "record")],
            [],
            [],
            degeneracy=[EnergyTerm("10")],
        )
        c = enumerate_model(m, [(0,)])
        self.assertEqual(
            history_profile(sampled_kernel(c, 0.25), np.ones(1), 10)[-1], 0
        )

    def test_support_is_about_words_not_only_endpoints(self):
        from omega_cosmology.testbed.history import (
            foreclosure,
            full_state_foreclosure,
            observed_history_law,
        )

        p = np.array([[0.5, 0.5], [0, 1.0]])
        a = np.array([[0, 1.0], [1.0, 0]])
        mu = np.array([1.0, 0])
        reference = observed_history_law(p, mu, [0, 1], 2)
        candidate = observed_history_law(a, mu, [0, 1], 2)
        direct = foreclosure(reference, candidate)["reference_weight"]
        dp = full_state_foreclosure(p, a.astype(bool), mu, np.array([True, False]), 2)
        self.assertAlmostEqual(direct, dp)
        self.assertGreater(direct, 0)

    def test_sampled_support_uses_graph_even_when_exponential_underflows(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.history import sampled_kernel, sampled_support
        from omega_cosmology.testbed.physics import (
            Condition,
            Coordinate,
            LocalModel,
            Rule,
        )

        m = LocalModel(
            "tiny-rates",
            [Coordinate("x", (0, 1, 2), "record")],
            [
                Rule("first", (Condition("x", "eq", 0),), (("x", 1),), 1e-180),
                Rule("second", (Condition("x", "eq", 1),), (("x", 1),), 1e-180),
            ],
            [],
        )
        c = enumerate_model(m, [(0,)])
        self.assertEqual(sampled_kernel(c, 0.25)[c.index[(0,)], c.index[(2,)]], 0)
        self.assertTrue(sampled_support(c).all())

    def test_same_law_preparations_have_rate_tie_and_bounded_offset(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.history import (
            history_profile,
            irreducible_asymptotics,
            sampled_kernel,
        )
        from omega_cosmology.testbed.physics import (
            Condition,
            Coordinate,
            EnergyTerm,
            LocalModel,
            Rule,
        )

        m = LocalModel(
            "relaxation",
            [Coordinate("x", (0, 1), "record")],
            [Rule("flip", (Condition("x", "eq", 0),), (("x", 1),), 0.2)],
            [EnergyTerm("1", "x")],
        )
        c = enumerate_model(m, [(0,)])
        p = sampled_kernel(c, 0.25)
        roots = [np.eye(2)[c.index[(v,)]] for v in (0, 1)]
        a, b = [irreducible_asymptotics(c, 0.25, mu) for mu in roots]
        self.assertEqual(a["rate_bits_per_time"], b["rate_bits_per_time"])
        gap = (
            history_profile(p, roots[0], 1000)[-1]
            - history_profile(p, roots[1], 1000)[-1]
        )
        self.assertAlmostEqual(gap, a["offset_bits"] - b["offset_bits"], places=9)


if __name__ == "__main__":
    unittest.main()
