"""Thermodynamic and structural checks, independent of favorable lushness signs."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.physical_modules import (
    assistance_spec,
    autocatalytic_ecology,
    repaired_capacity_world,
)
from omega_cosmology.testbed.physics import LocalModel
from omega_cosmology.testbed.thermodynamics import audit_equilibrium


def groups():
    return [
        {"id": s, "members": [s + ".x", s + ".y"], "access_member": s + ".x"}
        for s in ("A", "B")
    ]


class CoupledPhysicsTests(unittest.TestCase):
    def test_store_breakdown_is_possible_at_every_load_without_refund_space(self):
        m, _ = repaired_capacity_world()
        for load in range(7):
            state = (1, 1, 1, 0, load, 1)
            e = next(
                e
                for e in m.events(state)
                if e.rule_id == f"store_spill_{load}" and e.direction == 1
            )
            self.assertEqual(e.target[-1], 0)
            self.assertEqual(e.target[4], 0)
            self.assertAlmostEqual(e.heat, 0.5 + 0.5 * load)
            reverse = next(
                r
                for r in m.events(e.target)
                if r.rule_id == e.rule_id and r.direction == -1
            )
            self.assertEqual(reverse.target, state)
            self.assertAlmostEqual(e.work - e.delta_energy, e.heat)

    def test_bound_damage_and_paid_repair_are_physical_at_empty_and_full_bank(self):
        m, _ = repaired_capacity_world()
        self.assertNotIn("upkeep", [r.id for r in m.rules])
        for bank in (0, 6):
            state = (1, 1, 1, 0, bank, 1)
            e = next(
                e
                for e in m.events(state)
                if e.rule_id == "bound_damage_a.active" and e.direction == 1
            )
            self.assertEqual(e.target[0], 0)
            self.assertEqual(e.target[2], 0)
        damaged = (0, 1, 0, 0, 2, 1)
        e = next(
            e
            for e in m.events(damaged)
            if e.rule_id == "paid_activate_a.active" and e.direction == 1
        )
        self.assertEqual(e.target, (1, 1, 0, 0, 0, 1))
        self.assertAlmostEqual(e.heat, 0.5)
        empty = (0, 1, 0, 0, 0, 1)
        self.assertFalse(
            any(
                e.rule_id == "paid_activate_a.active" and e.direction == 1
                for e in m.events(empty)
            )
        )

    def test_repaired_world_retains_source_off_equilibrium(self):
        m, root = repaired_capacity_world()
        c = enumerate_model(m, [root])
        self.assertEqual(audit_equilibrium(c)["status"], "passed")

    def test_capture_competes_for_shared_resource_and_pays_reconstruction(self):
        m = autocatalytic_ecology(groups())
        # A.x, A.y, A.bank, B.x, B.y, B.bank, carrier
        state = (1, 0, 0, 1, 0, 0, 2)
        captures = [
            e for e in m.events(state) if e.direction == 1 and "capture" in e.rule_id
        ]
        self.assertEqual(len(captures), 4)
        for e in captures:
            self.assertEqual(e.target[-1], 0)
            self.assertFalse(
                any(
                    x.direction == 1 and "capture" in x.rule_id
                    for x in m.events(e.target)
                )
            )
        state = (1, 0, 1, 1, 0, 0, 0)
        e = next(
            e
            for e in m.events(state)
            if e.rule_id == "assisted_construct_A.x_to_A.y" and e.direction == 1
        )
        self.assertEqual(e.target[:3], (1, 1, 0))
        self.assertAlmostEqual(e.delta_energy, -0.5)
        self.assertAlmostEqual(e.heat, 0.5)

    def test_all_constituents_have_independent_breakdown_at_full_bank(self):
        m = autocatalytic_ecology(groups())
        state = tuple(c.domain[-1] for c in m.coordinates)
        for field in ["A.x", "A.y", "B.x", "B.y"]:
            e = next(
                e
                for e in m.events(state)
                if e.rule_id == "basal_construct_" + field and e.direction == -1
            )
            self.assertEqual(e.target[m.indices[field]], 0)
            self.assertEqual(e.target[m.indices[field.split(".")[0] + ".bank"]], 2)

    def test_cross_assistance_uses_recipient_bank_and_preserves_parent(self):
        m = autocatalytic_ecology(groups(), extra_assistance=[("A.x", "B.y")])
        state = (1, 0, 0, 0, 0, 1, 0)
        e = next(
            e
            for e in m.events(state)
            if e.rule_id == "assisted_construct_A.x_to_B.y" and e.direction == 1
        )
        self.assertEqual(e.target, (1, 0, 0, 0, 1, 0, 0))
        self.assertEqual(assistance_spec(m, ["A.x", "A.y"])["depth_cap"], 3)
        m = LocalModel.from_record(m.record())
        c = enumerate_model(m, [state])
        self.assertEqual(audit_equilibrium(c)["status"], "passed")

    def test_generic_group_composition_and_fractional_costs(self):
        g = [{"id": "niche", "members": ["p", "q", "r"], "access_member": "p"}]
        m = autocatalytic_ecology(
            g, bank_quantum=".75", formation_energy=".25", driven=False
        )
        self.assertNotIn("source", [r.id for r in m.rules])
        e = next(
            e
            for e in m.events((1, 0, 0, 1, 0))
            if e.rule_id == "assisted_construct_p_to_q" and e.direction == 1
        )
        self.assertAlmostEqual(e.heat, 0.5)
        self.assertEqual(
            len(assistance_spec(m, ["p", "q", "r"])["assistance_edges"]), 3
        )


if __name__ == "__main__":
    unittest.main()
