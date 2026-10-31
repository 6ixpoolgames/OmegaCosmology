"""Analytic source/load budgets and parallel-channel history invariance."""

import sys
import unittest
from math import exp
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.history import history_profile, sampled_kernel
from omega_cosmology.testbed.physics import Condition as C
from omega_cosmology.testbed.physics import Coordinate, EnergyTerm, LocalModel, Rule
from omega_cosmology.testbed.resource_load import attach_resource_load, load_rewards
from omega_cosmology.testbed.thermodynamics import audit_equilibrium, flow_rewards


def base(*, driven=True, helper=1, bath=0.002):
    rules = [Rule("bath", (C("fuel", "eq", 0),), (("fuel", 1),), bath)]
    if driven:
        rules.append(
            Rule(
                "source",
                (C("fuel", "eq", 0),),
                (("fuel", 1),),
                0.08,
                "3",
                "work_source",
            )
        )
    return LocalModel(
        "two_state_fixture",
        [
            Coordinate("device", (0, 1), "material_state"),
            Coordinate("fuel", (0, 1), "resource"),
        ],
        rules,
        [EnergyTerm("3", "fuel"), EnergyTerm(".5", "device")],
        material=({"id": "carrier", "inventory": [{"coefficient": "1"}]},),
    ), (helper, 0)


def load(model, k=0.1):
    return attach_resource_load(
        model,
        resource="fuel",
        charged=1,
        spent=0,
        helper_conditions=(C("device", "eq", 1),),
        conductance=k,
    )


class ResourceLoadTests(unittest.TestCase):
    def stationary(self, c):
        q = c.q.toarray()
        system = q.T.copy()
        system[-1] = 1
        rhs = np.zeros(len(q))
        rhs[-1] = 1
        return np.linalg.solve(system, rhs)

    def test_actual_heat_and_reverse_are_three_energy_units(self):
        m, root = base()
        m = load(m)
        charged = (1, 1)
        forward = next(e for e in m.events(charged) if e.rule_id == "resource_load")
        reverse = next(e for e in m.events(root) if e.rule_id == "resource_load")
        self.assertEqual((forward.work, forward.heat, forward.delta_energy), (0, 3, -3))
        self.assertEqual((reverse.work, reverse.heat, reverse.delta_energy), (0, -3, 3))
        self.assertAlmostEqual(forward.rate / reverse.rate, exp(3))

    def test_stationary_budget_matches_closed_form(self):
        m, root = base()
        c = enumerate_model(load(m), [root])
        pi = self.stationary(c)
        charged = (0.08 + 0.102 * exp(-1.5)) / (0.16 + 0.102 * (exp(1.5) + exp(-1.5)))
        self.assertAlmostEqual(pi[c.index[(1, 1)]], charged)
        rewards, audit = load_rewards(c)
        net = 3 * 0.1 * (charged * exp(1.5) - (1 - charged) * exp(-1.5))
        self.assertAlmostEqual(pi @ rewards["net_heat"], net)
        self.assertGreater(net, 0)
        self.assertTrue(audit["no_forward_energy_gain"])
        work, heat, _, _ = flow_rewards(c)
        self.assertAlmostEqual(pi @ work, pi @ heat)
        self.assertGreater(pi @ work, 0)

    def test_source_off_retains_thermal_activity_without_net_payment(self):
        m, root = base(driven=False)
        c = enumerate_model(load(m), [root])
        pi = self.stationary(c)
        rewards, _ = load_rewards(c)
        self.assertAlmostEqual(pi @ rewards["net_heat"], 0, places=12)
        self.assertGreater(pi @ rewards["forward_events"], 0)
        self.assertGreater(pi @ rewards["reverse_events"], 0)
        self.assertEqual(audit_equilibrium(c)["status"], "passed")

    def test_no_working_helper_means_no_extra_channel(self):
        m, root = base(helper=0)
        c = enumerate_model(load(m), [root])
        self.assertFalse(any(e.rule_id == "resource_load" for _, _, e in c.ledger))
        with self.assertRaisesRegex(ValueError, "no reachable forward"):
            load_rewards(c)

    def test_parallel_labels_do_not_inflate_history_entropy(self):
        m, root = base()
        a = enumerate_model(load(m), [root])
        # The same physical transition pair, one combined conductance.
        combined, _ = base(bath=0.102)
        b = enumerate_model(combined, [root])
        np.testing.assert_allclose(a.q.toarray(), b.q.toarray(), atol=1e-15)
        initial = np.eye(len(a.states))[a.index[root]]
        np.testing.assert_allclose(
            history_profile(sampled_kernel(a, 0.25), initial, 32),
            history_profile(sampled_kernel(b, 0.25), initial, 32),
            atol=1e-12,
        )

    def test_factory_cannot_change_grammar_or_duplicate_rule(self):
        m, _ = base()
        new = load(m)
        for field, value in m.record().items():
            if field not in ("id", "rules"):
                self.assertEqual(new.record()[field], value)
        with self.assertRaises(ValueError):
            load(new)
        with self.assertRaises(ValueError):
            attach_resource_load(
                m,
                resource="device",
                charged=1,
                spent=0,
                helper_conditions=(C("fuel", "eq", 1),),
                conductance=0.1,
            )


if __name__ == "__main__":
    unittest.main()
