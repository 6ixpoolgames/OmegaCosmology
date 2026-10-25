"""Independent analytic checks for passive readouts used by R1."""

import json
import sys
import unittest
from itertools import pairwise
from math import exp, log2
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
try:
    import numpy as np
except ImportError:
    np = None


@unittest.skipIf(np is None, "Install testbed extra")
class ReadoutTests(unittest.TestCase):
    def symmetric_switch(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.physics import (
            Condition,
            Coordinate,
            LocalModel,
            Rule,
        )

        m = LocalModel(
            "switch",
            [Coordinate("bit", (0, 1), "record")],
            [Rule("flip", (Condition("bit", "eq", 0),), (("bit", 1),), 0.2)],
            [],
        )
        c = enumerate_model(m, [(0,)])
        mu = np.zeros(len(c.states))
        mu[c.index[(0,)]] = 1
        return c, mu

    def test_ordered_witness_is_poisson_tail_and_preserves_physical_marginal(self):
        from omega_cosmology.testbed.readouts import two_event_monitor

        c, mu = self.symmetric_switch()
        result = two_event_monitor(c, mu, 3, ("flip", 1), ("flip", -1))
        self.assertAlmostEqual(
            result["completed_probability"], 1 - exp(-0.6) * (1 + 0.6), places=12
        )
        self.assertAlmostEqual(
            result["physical_marginal"][c.index[(0,)]], 0.5 * (1 + exp(-1.2)), places=12
        )

    def test_activity_coefficients_and_fine_cadence_limit(self):
        from omega_cosmology.testbed.history import (
            distributions_and_occupation,
            history_profile,
            sampled_kernel,
        )
        from omega_cosmology.testbed.readouts import activity_coefficients

        c, mu = self.symmetric_switch()
        _, occ = distributions_and_occupation(c, mu, 4)
        result = activity_coefficients(c, occ)
        self.assertAlmostEqual(result["expected_jumps"], 0.8, places=12)
        self.assertAlmostEqual(
            result["finite_coefficient_bits"], 0.8 * log2(exp(1) / 0.2), places=12
        )
        errors = []
        for dt in (0.125, 0.03125, 0.0078125):
            score = history_profile(sampled_kernel(c, dt), mu, round(4 / dt))[-1]
            errors.append(
                abs(score - (0.8 * log2(1 / dt) + result["finite_coefficient_bits"]))
            )
        self.assertTrue(all(a > b for a, b in pairwise(errors)))

    def test_correlated_coordinate_chain_rule(self):
        from omega_cosmology.testbed.readouts import (
            coordinate_entropy_rewards,
            cumulative_sampled_rewards,
        )

        # Each next state is either 00 or 11: first coordinate supplies the bit,
        # second is conditionally determined. No double counting correlation.
        p = np.array([[0.5, 0.5], [0.5, 0.5]])
        shares = coordinate_entropy_rewards(p, [(0, 0), (1, 1)], (0, 1))
        self.assertTrue(np.allclose(shares, [[1, 0], [1, 0]]))
        total = cumulative_sampled_rewards(p, np.array([1.0, 0]), shares, 4)
        self.assertTrue(np.allclose(total[-1], [4, 0]))

    def test_protocol_has_equal_endowment_and_only_declared_pair_ablations(self):
        from omega_cosmology.testbed.physics import LocalModel

        protocol = json.loads(
            (ROOT / "research/studies/R1-constructed-access/PROTOCOL.json").read_text(
                encoding="utf-8"
            )
        )
        base = protocol["laws"][0]
        base_rules = {r["id"]: r for r in base["model"]["rules"]}
        for law in protocol["laws"]:
            m = LocalModel.from_record(law["model"])
            for prep in protocol["preparations"]:
                self.assertAlmostEqual(sum(w for _, w in prep["roots"]), 1)
                for state, _ in prep["roots"]:
                    m.validate(tuple(state))
                    self.assertEqual(
                        str(m.energy(tuple(state))), protocol["energy_per_root"]
                    )
            rules = {r["id"]: r for r in law["model"]["rules"]}
            removed = set(base_rules) - set(rules)
            expected = ({"source"} if not law["driven"] else set()) | (
                {"unlock_motif"} if not law["assisted"] else set()
            )
            self.assertEqual(removed, expected)
            self.assertTrue(
                all(rule == base_rules[name] for name, rule in rules.items())
            )


if __name__ == "__main__":
    unittest.main()
