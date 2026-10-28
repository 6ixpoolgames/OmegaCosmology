"""Paid-cycle physics, thermal invariance, and v2 compatibility."""

import json
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.construction_chain import construction_chain
from omega_cosmology.testbed.history import distributions_and_occupation
from omega_cosmology.testbed.matching import MomentSpec, match_one_physical_moment
from omega_cosmology.testbed.monitors import compile_monitor, evaluate_monitor
from omega_cosmology.testbed.paid_cycle import THERMAL_CONDUCTANCE, paid_cycle_chain
from omega_cosmology.testbed.physics import LocalModel
from omega_cosmology.testbed.thermodynamics import audit_equilibrium


class PaidCycleTests(unittest.TestCase):
    def test_bank_load_removes_only_gate_and_still_pays(self):
        a, root, _ = paid_cycle_chain(gated=True)
        b, other, _ = paid_cycle_chain(gated=False)
        self.assertEqual(root, other)
        self.assertEqual(a.energy_terms, b.energy_terms)
        self.assertEqual(a.material, b.material)
        self.assertFalse(
            any(
                e.rule_id == "rotor.stroke" and e.direction == 1 for e in a.events(root)
            )
        )
        event = next(
            e
            for e in b.events(root)
            if e.rule_id == "rotor.stroke" and e.direction == 1
        )
        self.assertEqual(
            event.target[b.indices["bank.ticks"]], root[b.indices["bank.ticks"]] - 1
        )
        self.assertAlmostEqual(event.heat, 0.25)
        self.assertEqual(
            next(r for r in a.rules if r.id == "rotor.relax"),
            next(r for r in b.rules if r.id == "rotor.relax"),
        )

    def test_activity_match_cannot_certify_mismatched_work(self):
        specs = {
            k: MomentSpec(
                k, "events" if k == "N" else "energy", 1, "continuous_integral"
            )
            for k in ("N", "W")
        }
        fit = match_one_physical_moment(
            lambda p: {"N": p["rate"], "W": 2 * p["rate"]},
            {"N": 2, "W": 2},
            {"rate": (1, 4)},
            primary="N",
            moment_specs=specs,
        )
        self.assertEqual(fit["status"], "primary_moment_matched_only")
        self.assertAlmostEqual(fit["best"]["moments"]["N"], 2)
        self.assertGreater(fit["best"]["absolute_residuals"]["W"], 1.9)

    def test_unbracketed_activity_does_not_imply_infeasibility(self):
        spec = MomentSpec("N", "events", 1, "continuous_integral")
        fit = match_one_physical_moment(
            lambda p: {"N": p["rate"]},
            {"N": 8},
            {"rate": (1, 4)},
            primary="N",
            moment_specs={"N": spec},
        )
        self.assertEqual(fit["status"], "not_matched_in_bounded_search")
        self.assertEqual(fit["termination"], "no_sign_bracket")

    def test_old_chain_default_fingerprint_stays_retained_v2(self):
        cases = json.loads(
            (
                ROOT
                / "research/platform/engineering/r2-transduction-2026-10-27/retained/EXECUTION_CASES.json"
            ).read_text()
        )
        old = LocalModel.from_record(cases[0]["law"]["model"])
        new, _, _ = construction_chain()
        self.assertEqual(old.fingerprint(), new.fingerprint())

    def test_cycle_draws_one_energy_and_reverses_refund(self):
        m, root, _ = paid_cycle_chain()
        s = list(root)
        for name, value in {
            "products.precursor": 0,
            "products.B": 1,
            "bank.ticks": 2,
        }.items():
            s[m.indices[name]] = value
        s = tuple(s)
        a = next(
            e for e in m.events(s) if e.rule_id == "rotor.stroke" and e.direction == 1
        )
        b = next(
            e
            for e in m.events(a.target)
            if e.rule_id == "rotor.reset" and e.direction == 1
        )
        self.assertAlmostEqual(a.heat, 0.25)
        self.assertAlmostEqual(b.heat, 0.75)
        self.assertEqual(
            b.target[m.indices["rotor.state"]], s[m.indices["rotor.state"]]
        )
        self.assertEqual(m.energy(s) - m.energy(b.target), 1)
        reverse_b = next(
            e
            for e in m.events(b.target)
            if e.rule_id == "rotor.reset" and e.direction == -1
        )
        reverse_a = next(
            e
            for e in m.events(reverse_b.target)
            if e.rule_id == "rotor.stroke" and e.direction == -1
        )
        self.assertEqual(reverse_a.target, s)

    def test_only_paid_barriers_change_across_calibration(self):
        a, root, _ = paid_cycle_chain(access=False)
        b, _, _ = paid_cycle_chain(access=False, charge=0.4, reset=0.2)
        first, second = {r.id: r for r in a.rules}, {r.id: r for r in b.rules}
        for id, rule in first.items():
            if "churn.paid" not in rule.roles:
                self.assertEqual(rule, second[id])
        self.assertEqual(first["rotor.relax"].conductance, THERMAL_CONDUCTANCE)
        self.assertEqual(a.energy_terms, b.energy_terms)
        self.assertEqual(a.material, b.material)
        for model in (a, b):
            self.assertEqual(
                audit_equilibrium(enumerate_model(model, [root], max_states=400))[
                    "status"
                ],
                "passed",
            )

    def test_cycle_witness_preserves_native_marginal(self):
        from write_r2_paid_cycle_plan import protocol

        m, root, _ = paid_cycle_chain()
        c = enumerate_model(m, [root], max_states=400)
        mu = np.zeros(len(c.states))
        mu[c.index[root]] = 1
        spec = next(
            s for s in protocol(m, root)[0]["monitors"] if s["id"] == "first_paid_cycle"
        )
        result = evaluate_monitor(compile_monitor(c, spec), mu, 4)
        endpoint, _ = distributions_and_occupation(c, mu, 4)
        np.testing.assert_allclose(result["physical_marginal"], endpoint, atol=1e-12)
        self.assertGreaterEqual(result["completed_probability"], 0)


if __name__ == "__main__":
    unittest.main()
