"""Paid response memory, reserve constraints and native physical compatibility."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.readiness import POLICIES, readiness_root, readiness_world
from omega_cosmology.testbed.signals import warning_world
from omega_cosmology.testbed.thermodynamics import audit_equilibrium


def state(model, **values):
    s = list(readiness_root(model))
    for key, value in values.items():
        s[
            model.indices[key.replace("_", ".", 1) if key.startswith("body_") else key]
        ] = value
    return tuple(s)


def forward(model, s, prefix):
    return [
        e for e in model.events(s) if e.direction == 1 and e.rule_id.startswith(prefix)
    ]


class ReadinessTests(unittest.TestCase):
    def test_functional_query_budget_is_enforced_without_a_fallback(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
        from write_readiness_smoke import protocol

        from omega_cosmology.testbed.finite_study import evaluate_case

        m = readiness_world("conserve", opening_rate=None)
        p = protocol(m, policy="conserve", quantum=".5", effort=".5")
        p["structural_analysis"]["max_functional_query_states"] = 100
        with self.assertRaises(MemoryError):
            evaluate_case(p, {"id": "capped", "model": m.record()}, 0.25)
        p["structural_analysis"]["max_functional_query_states"] = 0
        with self.assertRaises(ValueError):
            evaluate_case(p, {"id": "invalid", "model": m.record()}, 0.25)

    def test_common_hardware_and_root_endowment(self):
        models = [readiness_world(p) for p in POLICIES]
        for m in models:
            self.assertEqual(m.coordinates, models[0].coordinates)
            self.assertEqual(m.energy_terms, models[0].energy_terms)
            self.assertEqual(m.energy(readiness_root(m)), 2.5)
        common = [
            {
                r.id: r
                for r in m.rules
                if not r.id.startswith(
                    ("escape_", "blocked_effort_", "effort_damage_", "cue_clear_")
                )
            }
            for m in models
        ]
        self.assertTrue(all(v == common[0] for v in common))

    def test_paid_failure_writes_a_physical_mark_and_can_reverse(self):
        m = readiness_world("stop")
        s = state(m, body_signal=1)
        event = forward(m, s, "blocked_effort_")[0]
        self.assertEqual(event.target[m.indices["body.bank"]], 1)
        self.assertEqual(event.target[m.indices["body.failures"]], 1)
        self.assertAlmostEqual(event.heat, 0.875)
        reverse = [
            e
            for e in m.events(event.target)
            if e.rule_id == event.rule_id and e.direction == -1
        ]
        self.assertEqual(reverse[0].target, s)
        self.assertEqual(reverse[0].heat, -event.heat)

    def test_threshold_and_paid_cue_reengagement(self):
        for policy in POLICIES:
            m = readiness_world(policy)
            s = state(m, body_signal=1, body_failures=2, barrier=1)
            self.assertEqual(bool(forward(m, s, "escape_")), policy == "always")
            cued = state(m, body_signal=1, body_failures=2, body_cue=1, barrier=1)
            clear = forward(m, cued, "cue_clear_")
            self.assertEqual(bool(clear), policy == "reengage")
            if clear:
                self.assertEqual(clear[0].target[m.indices["body.bank"]], 2)
                self.assertAlmostEqual(clear[0].heat, 0.625)
                self.assertTrue(forward(m, clear[0].target, "escape_"))

    def test_quarter_energy_bill_is_not_rounded(self):
        m = readiness_world("always", bank_quantum=".25", effort_bill=".25")
        s = state(m, body_signal=1, barrier=1)
        event = forward(m, s, "escape_")[0]
        self.assertEqual(
            s[m.indices["body.bank"]] - event.target[m.indices["body.bank"]], 1
        )
        self.assertEqual(event.heat, 0.25)
        blocked = forward(m, state(m, body_signal=1), "blocked_effort_")[0]
        self.assertEqual(blocked.target[m.indices["body.bank"]], 3)
        self.assertAlmostEqual(blocked.heat, 0.625)
        with self.assertRaises(ValueError):
            readiness_world("stop", bank_quantum=".5", effort_bill=".25")

    def test_empty_bank_cannot_pay_forward_response_or_clearing(self):
        m = readiness_world("reengage")
        s = state(m, body_signal=1, body_bank=0, body_cue=1, body_failures=1)
        for prefix in (
            "escape_",
            "blocked_effort_",
            "effort_damage_",
            "cue_clear_",
            "paid_restore",
        ):
            self.assertFalse(forward(m, s, prefix))
        # Thermal reverse credits are still physical, not forbidden by the test.

    def test_opportunity_pair_and_explicit_damage(self):
        m = readiness_world("always")
        s = readiness_root(m)
        opening = forward(m, s, "barrier_toggle")[0]
        self.assertAlmostEqual(opening.rate, 0.02)
        reverse = next(
            e for e in m.events(opening.target) if e.rule_id == "barrier_toggle"
        )
        self.assertAlmostEqual(reverse.rate, 0.25)
        funded = state(m, body_signal=1)
        damage = forward(m, funded, "effort_damage_")[0]
        self.assertEqual(damage.target[m.indices["body.working"]], 0)
        self.assertEqual(damage.work - damage.heat, damage.delta_energy)

    def test_native_equilibrium_and_legacy_fingerprint_unchanged(self):
        original = warning_world(sensor="push_pull").fingerprint()
        for policy in POLICIES:
            m = readiness_world(policy, opening_rate=None)
            c = enumerate_model(m, [readiness_root(m)], max_states=500)
            c.require_complete()
            self.assertEqual(len(c.states), 384)
            self.assertEqual(audit_equilibrium(c)["status"], "passed")
        self.assertEqual(original, warning_world(sensor="push_pull").fingerprint())


if __name__ == "__main__":
    unittest.main()
