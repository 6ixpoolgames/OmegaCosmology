"""Physical conformance for warning/response contrasts, without expected wins."""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.physics import LocalModel
from omega_cosmology.testbed.signals import warning_root, warning_world
from omega_cosmology.testbed.thermodynamics import audit_equilibrium


class SignalTests(unittest.TestCase):
    def test_push_pull_pays_for_writing_and_resetting(self):
        m = warning_world(sensor="push_pull", off_conductance=0.008)
        self.assertEqual(
            m.fingerprint(), warning_world(sensor="push_pull").fingerprint()
        )
        write = next(
            e
            for e in m.events(warning_root())
            if e.rule_id == "signal_write_0_1" and e.direction == 1
        )
        self.assertEqual(write.heat, 0.5)
        self.assertEqual(write.delta_energy, -0.5)
        reset = next(
            e
            for e in m.events(write.target)
            if e.rule_id == "signal_reset_0_1" and e.direction == 1
        )
        self.assertEqual(reset.heat, 1)
        self.assertEqual(reset.target[1], 0)
        for response in (False, True):
            c = enumerate_model(
                warning_world(sensor="push_pull", response=response), [warning_root()]
            )
            self.assertEqual(audit_equilibrium(c)["status"], "passed")

    def test_response_ablation_keeps_signal_and_costs(self):
        a = warning_world()
        b = warning_world(response=False)
        self.assertEqual(a.coordinates, b.coordinates)
        self.assertEqual(a.energy_terms, b.energy_terms)
        self.assertEqual(a.energy(warning_root()), b.energy(warning_root()))
        self.assertEqual(
            {r.id for r in a.rules} - {r.id for r in b.rules},
            {"escape", "blocked_effort"},
        )
        self.assertEqual(
            {r.id: r for r in b.rules},
            {r.id: r for r in a.rules if r.id not in {"escape", "blocked_effort"}},
        )

    def test_blocked_effort_changes_reserve_but_never_location(self):
        m = warning_world(barrier_conductance=None)
        root = list(warning_root())
        root[-1] = 1
        events = list(m.events(tuple(root)))
        attempt = next(e for e in events if e.rule_id == "blocked_effort")
        self.assertEqual(attempt.target[1], root[1] - 1)
        self.assertEqual(attempt.target[2], root[2])
        self.assertEqual(attempt.heat, 0.5)
        self.assertFalse(any(e.rule_id == "escape" for e in events))
        # Identical physical outcomes aggregate; there is no entropy of labels.
        compiled = enumerate_model(m, [tuple(root)])
        i = compiled.index[tuple(root)]
        j = compiled.index[attempt.target]
        total = sum(e.rate for e in events if e.target == attempt.target)
        self.assertAlmostEqual(compiled.q[i, j], total)
        self.assertGreater(total, attempt.rate)

    def test_native_reverse_cost_and_equilibrium(self):
        for barrier, opened in [(None, False), (None, True), (0.02, False)]:
            for response in (False, True):
                m = warning_world(barrier_conductance=barrier, response=response)
                c = enumerate_model(
                    m, [warning_root(open_barrier=opened)], max_states=300
                )
                c.require_complete()
                self.assertEqual(audit_equilibrium(c)["status"], "passed")
                for i, j, e in c.ledger:
                    self.assertAlmostEqual(e.work - e.heat, e.delta_energy)
                    reverse = [
                        r
                        for r in m.events(c.states[j])
                        if r.rule_id == e.rule_id
                        and r.direction == -e.direction
                        and r.target == c.states[i]
                    ]
                    self.assertEqual(len(reverse), 1)

    def test_paid_write_and_positive_upkeep(self):
        m = warning_world()
        event = next(
            e
            for e in m.events(warning_root())
            if e.rule_id == "signal_write_0_1" and e.direction == 1
        )
        self.assertEqual(event.target[1], 1)
        self.assertEqual(event.target[-1], 1)
        upkeep = next(
            e
            for e in m.events(event.target)
            if e.rule_id == "signal_upkeep" and e.direction == 1
        )
        self.assertEqual(upkeep.heat, 0.5)
        empty = list(warning_root())
        empty[1] = 0
        self.assertFalse(
            any(
                e.rule_id.startswith("signal_write") and e.direction == 1
                for e in m.events(tuple(empty))
            )
        )

    def test_sensor_coupling_and_nontracking_control(self):
        for tracking in (False, True):
            m = warning_world(tracking=tracking)
            s = list(warning_root())
            rates = []
            for z in (0, 1):
                s[3] = z
                rates.append(
                    sum(
                        e.rate
                        for e in m.events(tuple(s))
                        if e.rule_id.startswith("signal_write") and e.direction == 1
                    )
                )
            self.assertAlmostEqual(rates[1] / rates[0], 15 if tracking else 1)

    def test_record_roundtrip_and_sector_sizes(self):
        for barrier, opened, expected in [
            (None, False, 64),
            (None, True, 128),
            (0.02, False, 256),
        ]:
            m = warning_world(barrier_conductance=barrier)
            restored = LocalModel.from_record(m.record())
            self.assertEqual(m.fingerprint(), restored.fingerprint())
            c = enumerate_model(restored, [warning_root(open_barrier=opened)])
            self.assertEqual(len(c.states), expected)
            self.assertTrue(np.allclose(np.asarray(c.q.sum(axis=1)).ravel(), 0))


if __name__ == "__main__":
    unittest.main()
