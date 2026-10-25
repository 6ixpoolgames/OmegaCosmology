"""Matched repair faults and explicit feedback ablation; no desired entropy sign."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.repair import repair_capacity_world
from omega_cosmology.testbed.thermodynamics import audit_equilibrium


class RepairTests(unittest.TestCase):
    def test_closure_is_not_a_long_recovery_time(self):
        import numpy as np
        from scipy.sparse import csr_matrix

        from omega_cosmology.testbed.ecology import structural_closure_mask

        irreversible = csr_matrix([[-1.0, 1.0], [0, 0]])
        slow_recovery = csr_matrix([[-1.0, 1.0], [1e-100, -1e-100]])
        self.assertEqual(
            structural_closure_mask(irreversible, [True, False]).tolist(), [False, True]
        )
        self.assertFalse(np.any(structural_closure_mask(slow_recovery, [True, False])))

    def test_equal_fault_loss_and_distinct_consequences(self):
        m = repair_capacity_world()
        intact = (1, 1, 2, 1, 0, 0)
        r_loss = (0, 1, 2, 1, 0, 0)
        y_loss = (1, 0, 2, 1, 0, 0)
        self.assertEqual(m.energy(r_loss), m.energy(y_loss))
        self.assertEqual(m.energy(intact) - m.energy(r_loss), 0.5)

        def forward_ids(s):
            usable = list(s)
            usable[3] = 2
            usable[2] = 1
            return {e.rule_id for e in m.events(tuple(usable)) if e.direction == 1}

        self.assertIn("bind.contact.repair.R_to_repair.Y", forward_ids(y_loss))
        self.assertNotIn("bind.contact.repair.R_to_repair.Y", forward_ids(r_loss))
        self.assertIn("assisted_capture_repair", forward_ids(r_loss))
        self.assertNotIn("assisted_capture_repair", forward_ids(y_loss))

    def test_feedback_control_removes_only_paid_conversion_pair(self):
        a = repair_capacity_world()
        b = repair_capacity_world(feedback=False)
        self.assertEqual(a.coordinates, b.coordinates)
        self.assertEqual(a.energy_terms, b.energy_terms)
        self.assertEqual(
            {r.id for r in a.rules} - {r.id for r in b.rules},
            {"assisted_construct_repair.Y_to_repair.R"},
        )
        self.assertEqual(
            {r.id: r for r in b.rules},
            {r.id: r for r in a.rules if r.id in {x.id for x in b.rules}},
        )
        self.assertIn("bind.contact.repair.Y_to_repair.R", {r.id for r in b.rules})
        c = enumerate_model(b, [(1, 1, 2, 1, 0, 0)])
        self.assertEqual(len(c.states), 54)
        self.assertEqual(audit_equilibrium(c)["status"], "passed")
