"""Inputs, reverses and calibration semantics for fuel-powered registers."""

import sys
import unittest
from math import exp
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from report_powered_readiness import calibration_diagnostics
from write_powered_readiness_calibration import calibration_case

from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.readiness import POLICIES, readiness_root, readiness_world
from omega_cosmology.testbed.readiness_v2 import powered_readiness_world
from omega_cosmology.testbed.registers import RegisterPayment
from omega_cosmology.testbed.thermodynamics import audit_equilibrium


def state(model, **changes):
    result = list(readiness_root(model))
    for key, value in changes.items():
        result[
            model.indices[key.replace("_", ".", 1) if key.startswith("body_") else key]
        ] = value
    return tuple(result)


class PoweredReadinessTests(unittest.TestCase):
    def test_reporting_uses_initial_memory_and_separates_first_from_current(self):
        obs = {
            "failure_marks": {"endpoint": 1.5},
            "memory_saturated": {"endpoint": 0.4},
            "empty_bank": {"integrated": 0.5},
        }
        for i, values in enumerate(((0.8, 0), (0.2, 0))):
            for j, value in enumerate(values):
                obs[f"cue_joint_{i}_{j}"] = {
                    k: value for k in ("endpoint", "integrated", "stationary")
                }
        events = dict.fromkeys(
            (
                "marks_failed_attempt",
                "marks_reverse_clear",
                "marks_thermal",
                "marks_undo_attempt",
                "marks_cleared",
                "marks_relaxed",
                "register_fuel_forward",
                "register_fuel_reverse",
            ),
            0.0,
        )
        events["marks_cleared"] = 0.5
        row = {
            "observables": obs,
            "event_readouts": events,
            "horizon": 1,
            "preparation": "marked",
            "history": {"ell_bits": 3},
            "physical": {"work_accepted_gross": 0},
            "projected_histories": {"body_full.m0": {"width_bits": 1}},
            "horizon_diagnostics": {},
            "functional_profiles": {
                "correct_cue": {
                    "ever_functional_probability": 0.9,
                    "endpoint_functional_probability": 0.8,
                }
            },
        }
        result = calibration_diagnostics(row, initial_marks=2)
        self.assertEqual(result["marks"]["drift_ledger_residual"], 0)
        self.assertEqual(result["first_correct_probability"], 0.9)
        self.assertEqual(result["current_correct_probability"], 0.8)
        self.assertIsNone(result["cue"]["endpoint"]["balanced_accuracy"])
        with self.assertRaises(ArithmeticError):
            calibration_diagnostics(row, initial_marks=0)

    def test_empty_bank_cue_consumes_existing_fuel_and_has_exact_reverse(self):
        model = powered_readiness_world("reengage")
        s = state(model, body_bank=0, carrier=1, barrier=1)
        event = next(
            e
            for e in model.events(s)
            if e.rule_id == "cue_write_1" and e.direction == 1
        )
        self.assertEqual(event.target[model.indices["carrier"]], 0)
        self.assertEqual(event.target[model.indices["body.bank"]], 0)
        self.assertEqual(event.delta_energy, -1.25)
        self.assertEqual(event.heat, 1.25)
        self.assertEqual(event.work, 0)
        reverse = next(
            e
            for e in model.events(event.target)
            if e.rule_id == event.rule_id and e.direction == -1
        )
        self.assertEqual(reverse.target, s)
        self.assertEqual(reverse.heat, -event.heat)
        self.assertAlmostEqual(event.rate / reverse.rate, exp(2.5))
        unfunded = state(model, body_bank=0, carrier=0, barrier=1)
        self.assertFalse(
            any(
                e.rule_id == "cue_write_1" and e.direction == 1
                for e in model.events(unfunded)
            )
        )

    def test_clearing_has_two_real_inputs_and_refunds_them_on_reverse(self):
        model = powered_readiness_world("reengage")
        s = state(model, body_failures=1, body_cue=1, carrier=1)
        event = next(
            e
            for e in model.events(s)
            if e.rule_id == "cue_clear_1" and e.direction == 1
        )
        self.assertEqual(event.target[model.indices["body.failures"]], 0)
        self.assertEqual(event.target[model.indices["body.bank"]], 2)
        self.assertEqual(event.target[model.indices["carrier"]], 0)
        self.assertEqual(event.heat, 2.125)
        reverse = next(
            e
            for e in model.events(event.target)
            if e.rule_id == event.rule_id and e.direction == -1
        )
        self.assertEqual(reverse.target, s)
        for unfunded in (
            state(model, body_failures=1, body_cue=1, carrier=0),
            state(model, body_failures=1, body_cue=1, carrier=1, body_bank=0),
        ):
            self.assertFalse(
                any(
                    e.rule_id == "cue_clear_1" and e.direction == 1
                    for e in model.events(unfunded)
                )
            )

    def test_bank_configuration_recovers_old_native_pairs(self):
        model = powered_readiness_world(
            "reengage",
            cue_write=RegisterPayment(".5"),
            cue_reset=RegisterPayment(".5"),
            memory_clear=RegisterPayment(".5"),
        )
        old = readiness_world("reengage")
        self.assertEqual(model.coordinates, old.coordinates)
        self.assertEqual(model.energy_terms, old.energy_terms)
        new_rules = {r.id: r for r in model.rules}
        self.assertEqual(set(new_rules), {r.id for r in old.rules})
        for rule in old.rules:
            new = new_rules[rule.id]
            self.assertEqual(set(new.guards), set(rule.guards))
            self.assertEqual(dict(new.changes), dict(rule.changes))
            self.assertAlmostEqual(new.conductance, rule.conductance)
            self.assertEqual((new.work, new.boundary), (rule.work, rule.boundary))

    def test_bills_selectivity_and_errors_are_independent(self):
        base = powered_readiness_world("reengage")
        altered = powered_readiness_world(
            "reengage",
            cue_write=RegisterPayment(".5", True),
            cue_selectivity=8,
            cue_relaxation=0.001,
        )
        a, b = ({r.id: r for r in model.rules} for model in (base, altered))
        self.assertEqual(a["cue_clear_1"], b["cue_clear_1"])
        self.assertEqual(a["cue_write_1"].conductance / 2, b["cue_write_1"].conductance)
        self.assertNotEqual(a["cue_write_1"].changes, b["cue_write_1"].changes)
        self.assertEqual(a["cue_relax"].conductance * 10, b["cue_relax"].conductance)
        for payment in (
            RegisterPayment("0"),
            RegisterPayment(".3"),
            RegisterPayment("2"),
        ):
            with self.assertRaises(ValueError):
                payment.terms(base, ".5")

    def test_common_endowment_and_source_off_equilibrium(self):
        models = [powered_readiness_world(p) for p in POLICIES]
        for model in models:
            self.assertEqual(model.coordinates, models[0].coordinates)
            self.assertEqual(model.energy_terms, models[0].energy_terms)
            self.assertEqual(model.energy(readiness_root(model)), 2.5)
        off = powered_readiness_world("reengage", source_enabled=False)
        self.assertTrue(all(r.boundary == "native" for r in off.rules))
        for model in (models[-1], off):
            compiled = enumerate_model(model, [readiness_root(model)], max_states=2000)
            compiled.require_complete()
            self.assertEqual(audit_equilibrium(compiled)["status"], "passed")

    def test_calibration_roots_declare_energy_and_no_attempt_control(self):
        case = calibration_case("test", held=False, memory_control=True)
        self.assertEqual(
            [p["id"] for p in case["protocol"]["preparations"]], ["unmarked", "marked"]
        )
        self.assertNotEqual(
            *[p["energy_per_root"] for p in case["protocol"]["preparations"]]
        )
        self.assertFalse(
            any(
                r["id"].startswith(("escape_", "blocked_effort_", "effort_damage_"))
                for r in case["law"]["model"]["rules"]
            )
        )
        self.assertTrue(
            any(r["id"].startswith("cue_clear_") for r in case["law"]["model"]["rules"])
        )


if __name__ == "__main__":
    unittest.main()
