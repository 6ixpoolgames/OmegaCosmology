"""Conservation, explicit ports and consequential construction contracts."""

import sys
import unittest
from dataclasses import replace
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.construction_chain import construction_chain
from omega_cosmology.testbed.modules import Binding, Module, Port, compose
from omega_cosmology.testbed.physics import Condition as C
from omega_cosmology.testbed.physics import Coordinate, EnergyTerm, Rule
from omega_cosmology.testbed.thermodynamics import audit_equilibrium


class BindingTests(unittest.TestCase):
    def test_ports_require_exact_roles_domains_and_energy(self):
        store = Module(
            "bank",
            (Coordinate("ticks", (0, 1, 2), "energy"),),
            energy=(EnergyTerm(".5", "ticks"),),
        )
        user = Module("user", ports=(Port("fuel", "energy", (0, 1, 2), ".5"),))
        compose(
            "valid",
            [
                Binding(store, "reserve", {}),
                Binding(user, "consumer", {"fuel": "reserve.ticks"}),
            ],
        )
        for bad in (
            {},
            {"fuel": "missing"},
            {"fuel": "reserve.ticks", "extra": "reserve.ticks"},
        ):
            with self.assertRaises(ValueError):
                compose(
                    "bad",
                    [Binding(store, "reserve", {}), Binding(user, "consumer", bad)],
                )
        for bad in (
            Port("fuel", "resource", (0, 1, 2)),
            Port("fuel", "energy", (0, 1)),
            Port("fuel", "energy", (0, 1, 2), "1"),
        ):
            with self.assertRaises(ValueError):
                compose(
                    "bad",
                    [
                        Binding(store, "reserve", {}),
                        Binding(
                            replace(user, ports=(bad,)),
                            "consumer",
                            {"fuel": "reserve.ticks"},
                        ),
                    ],
                )

    def test_namespace_renaming_preserves_native_law(self):
        fragment = Module(
            "switch",
            (Coordinate("x", (0, 1), "state"),),
            rules=(Rule("flip", (C("x", "eq", 0),), (("x", 1),), 0.2),),
        )
        a = enumerate_model(compose("a", [Binding(fragment, "one", {})]), [(0,)])
        b = enumerate_model(compose("b", [Binding(fragment, "other", {})]), [(0,)])
        np.testing.assert_array_equal(a.q.toarray(), b.q.toarray())
        self.assertEqual(a.states, b.states)

    def test_chain_conserves_precursor_and_keeps_thermal_baseline(self):
        m, root, _ = construction_chain()
        c = enumerate_model(m, [root], max_states=400)
        self.assertEqual(len(c.states), 324)
        self.assertEqual(str(m.energy(root)), "7")
        self.assertEqual(audit_equilibrium(c)["status"], "passed")
        for s in c.states:
            self.assertEqual(
                sum(
                    s[m.indices[k]]
                    for k in ("products.precursor", "products.B", "products.C")
                ),
                1,
            )
            self.assertEqual(m.inventory(s)["products.shared_precursor"], "1")
        for i, j, e in c.ledger:
            if e.rule_id == "products.assisted_B" and e.direction == 1:
                a, b = c.states[i], c.states[j]
                self.assertEqual(a[m.indices["A.active"]], 1)
                self.assertEqual(b[m.indices["A.active"]], 1)
                self.assertEqual(
                    b[m.indices["bank.ticks"]] - a[m.indices["bank.ticks"]], -2
                )
        n, start, _ = construction_chain(assist=False, access=False)
        ablated = enumerate_model(n, [start], max_states=400)
        self.assertEqual(set(c.states), set(ablated.states))
        self.assertEqual(len(n.rules), len(m.rules) - 3)
        for name in (
            "primary.locked_bath",
            "secondary.locked_bath",
            "primary.usable_bath",
            "secondary.usable_bath",
            "rotor.relax",
        ):
            self.assertEqual(
                next(r for r in m.rules if r.id == name),
                next(r for r in n.rules if r.id == name),
            )

    def test_second_interface_changes_native_access_and_alternative_competes(self):
        m, root, _ = construction_chain()
        values = list(root)
        values[m.indices["products.precursor"]] = 0
        values[m.indices["products.B"]] = 1
        values[m.indices["bank.ticks"]] = 1
        b = tuple(values)
        self.assertTrue(
            any(
                e.rule_id == "secondary_access.transduce" and e.direction == 1
                for e in m.events(b)
            )
        )
        event = next(
            e
            for e in m.events(b)
            if e.rule_id == "secondary_access.transduce" and e.direction == 1
        )
        self.assertEqual(
            event.target[m.indices["bank.ticks"]] - b[m.indices["bank.ticks"]], 1
        )
        self.assertAlmostEqual(event.heat, 0.5)
        self.assertFalse(
            any(
                e.rule_id.endswith("assisted_C") and e.direction == 1
                for e in m.events(b)
            )
        )
        values[m.indices["products.B"]] = 0
        values[m.indices["products.C"]] = 1
        c = tuple(values)
        self.assertFalse(
            any(e.rule_id == "secondary_access.transduce" for e in m.events(c))
        )
        broken = list(b)
        broken[m.indices["products.C"]] = 1
        with self.assertRaises(ValueError):
            m.validate(tuple(broken))


if __name__ == "__main__":
    unittest.main()
