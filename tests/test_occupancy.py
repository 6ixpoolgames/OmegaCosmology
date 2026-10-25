"""Port competition, thermodynamics and passive ancestry in finite chemistry."""

import json
import sys
import unittest
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import expm_multiply

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.ancestry import (
    compile_ancestry_query,
    evaluate_ancestry_query,
)
from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.occupancy import contact_state_bound, occupied_ecology
from omega_cosmology.testbed.physical_modules import assistance_spec
from omega_cosmology.testbed.physics import LocalModel
from omega_cosmology.testbed.thermodynamics import audit_equilibrium


def group(fields=("p", "q")):
    return [{"id": "A", "members": list(fields), "access_member": "p"}]


def state(m, **changes):
    values = {c.name: 0 for c in m.coordinates}
    values.update(changes)
    return tuple(values[c.name] for c in m.coordinates)


class OccupancyTests(unittest.TestCase):
    def test_default_adapter_keeps_published_reciprocal_world(self):
        base = Path(__file__).resolve().parents[1]
        plan = json.loads(
            (
                base
                / "research/platform/models/occupied-assistance/ENGINEERING_PLAN.json"
            ).read_text()
        )
        old = LocalModel.from_record(
            next(c for c in plan["cases"] if c["id"] == "reciprocal_pair")["law"][
                "model"
            ]
        )
        pair = [
            {"id": g, "members": [g + ".x", g + ".y"], "access_member": g + ".x"}
            for g in ("A", "B")
        ]
        current = occupied_ecology(
            pair,
            extra_assistance=[("A.x", "B.y"), ("B.x", "A.y")],
            bank_quantum=".5",
            formation_energy=".5",
            construction_bill_ticks=2,
        )
        self.assertEqual(current.fingerprint(), old.fingerprint())

    def test_port_competition_and_capture_are_native(self):
        m = occupied_ecology(
            group(("p", "q", "r")),
            extra_assistance=[("p", "r")],
            assistance_edges=[("p", "q"), ("p", "r")],
        )
        s = state(m, p=1, carrier=2)
        binds = [
            e for e in m.events(s) if e.rule_id.startswith("bind.") and e.direction == 1
        ]
        self.assertEqual(len(binds), 2)
        bound = binds[0].target
        self.assertFalse(
            any(
                e.rule_id.startswith("bind.") and e.direction == 1
                for e in m.events(bound)
            )
        )
        self.assertFalse(
            any(e.rule_id == "assisted_capture_A" for e in m.events(bound))
        )
        self.assertTrue(
            any(e.rule_id == "capture_A" and e.direction == 1 for e in m.events(bound))
        )
        bad = list(bound)
        bad[m.indices["contact.p_to_r"]] = 1
        self.assertFalse(m.valid(bad))

    def test_release_and_bound_failure_at_every_bank_load(self):
        m = occupied_ecology(group())
        for bank in (0, 1, 2):
            s = state(m, p=1, **{"A.bank": bank, "contact.p_to_q": 1})
            events = list(m.events(s))
            self.assertTrue(
                any(
                    e.rule_id == "bind.contact.p_to_q" and e.direction == -1
                    for e in events
                )
            )
            death = next(
                e
                for e in events
                if e.rule_id == "basal_construct_p.bound.contact.p_to_q"
                and e.direction == -1
            )
            self.assertEqual(death.target[m.indices["p"]], 0)
            self.assertEqual(death.target[m.indices["contact.p_to_q"]], 0)
            birth = next(
                e
                for e in events
                if e.rule_id == "basal_construct_q.bound.contact.p_to_q"
                and e.direction == 1
            )
            self.assertEqual(birth.target[m.indices["q"]], 1)
            self.assertEqual(birth.target[m.indices["contact.p_to_q"]], 0)

    def test_fractional_energy_ledger_and_conversion_reverse(self):
        m = occupied_ecology(
            group(),
            bank_quantum=".25",
            construction_bill_ticks=3,
            bank_capacity=4,
            formation_energy=".5",
        )
        s = state(m, p=1, **{"A.bank": 3, "contact.p_to_q": 1})
        e = next(
            e
            for e in m.events(s)
            if e.rule_id == "assisted_construct_p_to_q" and e.direction == 1
        )
        self.assertAlmostEqual(e.delta_energy, 0)
        self.assertEqual(e.target[m.indices["A.bank"]], 0)
        r = next(
            r
            for r in m.events(e.target)
            if r.rule_id == e.rule_id and r.direction == -1
        )
        self.assertEqual(r.target, s)
        self.assertAlmostEqual(e.work - e.delta_energy, e.heat)

    def test_equilibrium_serialization_and_combinatorial_size(self):
        m = occupied_ecology(group(), driven=False)
        s = state(m, p=1, **{"A.bank": 1})
        restored = LocalModel.from_record(m.record())
        self.assertEqual(restored.fingerprint(), m.fingerprint())
        c = enumerate_model(restored, [s])
        self.assertEqual(len(c.states), contact_state_bound(m))
        self.assertEqual(len(c.states), 54)
        self.assertEqual(audit_equilibrium(c)["status"], "passed")

    def test_native_contact_parent_ancestry_preserves_physical_marginal(self):
        m = occupied_ecology(group(), driven=False)
        s = state(m, p=1, **{"A.bank": 1})
        c = enumerate_model(m, [s])
        mu = np.zeros(len(c.states))
        mu[c.index[s]] = 1
        spec = assistance_spec(m, ["p", "q"], depth_cap=2)
        self.assertEqual(len(spec["assistance_edges"]), 2)
        query = compile_ancestry_query(c, spec, mu, max_query_states=10000)
        endpoint = expm_multiply(c.q.T * 4, mu)
        result = evaluate_ancestry_query(query, 4, endpoint)
        self.assertLess(result["physical_marginal_residual"], 1e-9)


if __name__ == "__main__":
    unittest.main()
