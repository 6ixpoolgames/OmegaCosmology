"""A real shared carrier intermediate, with reversible energy destinations."""

import sys
import unittest
from itertools import product
from math import exp
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.physics import Condition as C
from omega_cosmology.testbed.physics import Coordinate, EnergyTerm, LocalModel, Rule
from omega_cosmology.testbed.resource_conformation import add_resource_conformation
from omega_cosmology.testbed.resource_load import attach_resource_load, load_rewards
from omega_cosmology.testbed.thermodynamics import audit_equilibrium


def base():
    return LocalModel(
        "categorical_carrier",
        [
            Coordinate("tool", (0, 1), "material_state"),
            Coordinate("fuel", (0, 1, 2), "resource"),
        ],
        [
            Rule("bath1", (C("fuel", "eq", 0),), (("fuel", 1),), 0.002),
            Rule("bath2", (C("fuel", "eq", 0),), (("fuel", 2),), 0.002),
        ],
        [
            EnergyTerm("3", conditions=(C("fuel", "eq", 1),)),
            EnergyTerm("2", conditions=(C("fuel", "eq", 2),)),
        ],
        material=({"id": "carrier", "inventory": [{"coefficient": "1"}]},),
    )


def expanded():
    return add_resource_conformation(
        base(), resource="fuel", value=3, energy="3/2", links=(1, 0), conductance=0.002
    )


def controlled(helper=1):
    m = expanded()
    for a, b, n in [(1, 3, "entry"), (3, 0, "exit")]:
        m = attach_resource_load(
            m,
            resource="fuel",
            charged=a,
            spent=b,
            helper_conditions=(C("tool", "eq", 1),),
            conductance=0.1,
            rule_id=n,
        )
    return m, (helper, 3)


class ConformationTests(unittest.TestCase):
    def test_old_energies_rules_and_material_survive_extension(self):
        a, b = base(), expanded()
        self.assertEqual(b.rules[: len(a.rules)], a.rules)
        for s in product([0, 1], [0, 1, 2]):
            self.assertEqual(a.energy(s), b.energy(s))
            self.assertEqual(a.inventory(s), b.inventory(s))
        self.assertEqual(float(b.energy((1, 3))), 1.5)
        self.assertEqual(b.inventory((1, 3)), a.inventory((1, 0)))

    def test_each_leg_releases_half_and_reverse_returns_half(self):
        m, _ = controlled()
        for state, name in [(1, "entry"), (3, "exit")]:
            forward = next(
                e
                for e in m.events((1, state))
                if e.rule_id == name and e.direction == 1
            )
            reverse = next(
                e
                for e in m.events(forward.target)
                if e.rule_id == name and e.direction == -1
            )
            self.assertEqual(
                (forward.heat, forward.work, forward.delta_energy), (1.5, 0, -1.5)
            )
            self.assertEqual(
                (reverse.heat, reverse.work, reverse.delta_energy), (-1.5, 0, 1.5)
            )
            self.assertAlmostEqual(forward.rate / reverse.rate, exp(1.5))

    def test_equilibrium_keeps_real_intermediate_switching_without_net_heat(self):
        m, root = controlled()
        c = enumerate_model(m, [root])
        pi = np.array([exp(-float(m.energy(s))) for s in c.states])
        pi /= pi.sum()
        self.assertEqual(len(c.states), 4)
        self.assertEqual(audit_equilibrium(c)["status"], "passed")
        for name in ["entry", "exit"]:
            r, _ = load_rewards(c, rule_ids=(name,))
            self.assertAlmostEqual(pi @ r["net_heat"], 0, places=13)
            self.assertGreater(pi @ r["forward_events"], 0)
            self.assertGreater(pi @ r["reverse_events"], 0)

    def test_no_tool_does_not_freeze_the_intermediate(self):
        m, root = controlled(helper=0)
        events = list(m.events(root))
        self.assertTrue(any(e.target[1] != 3 for e in events))
        self.assertFalse(any(e.rule_id in ["entry", "exit"] for e in events))

    def test_invalid_extension_and_linear_code_energy_are_rejected(self):
        for kw in [
            {"value": 2, "links": (1, 0)},
            {"value": 3, "links": (4, 0)},
            {"value": 3, "links": (1, 1)},
        ]:
            with self.assertRaises(ValueError):
                add_resource_conformation(
                    base(), resource="fuel", energy="1.5", conductance=0.002, **kw
                )
        r = base().record()
        r["energy_terms"] = [
            {"coefficient": "1", "coordinate": "fuel", "conditions": []}
        ]
        with self.assertRaises(ValueError):
            add_resource_conformation(
                LocalModel.from_record(r),
                resource="fuel",
                value=3,
                energy="1.5",
                links=(1, 0),
                conductance=0.002,
            )


if __name__ == "__main__":
    unittest.main()
