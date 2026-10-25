"""Independent checks of the shared assay and R2 causal readout contracts."""

import copy
import json
import sys
import unittest
from math import exp, factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
try:
    import numpy as np
except ImportError:
    np = None


@unittest.skipIf(np is None, "Install testbed extra")
class FiniteStudyTests(unittest.TestCase):
    def test_symmetry_queries_reject_unmarked_identity_and_unverified_marks(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.finite_study import evaluate_case
        from omega_cosmology.testbed.models import two_copy_world
        from omega_cosmology.testbed.monitors import compile_monitor

        model, _ = two_copy_world(quotient=True)
        compiled = enumerate_model(model, [(1, 0)])
        with self.assertRaises(ValueError):
            compile_monitor(
                compiled,
                {
                    "id": "unmarked",
                    "stages": [
                        {
                            "name": "first",
                            "advance": [{"rules": ["flip_first"], "direction": 1}],
                        }
                    ],
                },
            )
        p = {
            "id": "unmarked",
            "preparations": [
                {"id": "root", "roots": [[[1, 0], 1.0]], "conditioning": "full_present"}
            ],
            "energy_per_root": "0",
            "coordinate_order": ["first", "second"],
            "horizons": [1],
            "cadences": [0.25],
            "numerical": {
                "kernel_agreement_tolerance": 1e-12,
                "independent_history_tolerance": 1e-7,
            },
            "sufficiency": "Full unmarked state",
            "boundary_scope": {"bath": "one"},
            "conserved": ["two unmarked slots"],
            "observables": [{"id": "sum", "terms": [["first", 1], ["second", 1]]}],
            "event_readouts": [],
            "monitors": [],
            "scope": "Finite unmarked reference",
        }
        law = {"id": "unmarked", "model": model.record()}
        result = evaluate_case(p, law, 0.25)
        self.assertEqual(result["states"], 3)
        p["observables"] = [{"id": "identity", "terms": [["first", 1]]}]
        with self.assertRaises(ValueError):
            evaluate_case(p, law, 0.25)

    def test_ordered_four_event_monitor_matches_poisson_tail(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.monitors import compile_monitor, evaluate_monitor
        from omega_cosmology.testbed.physics import (
            Condition,
            Coordinate,
            LocalModel,
            Rule,
        )

        m = LocalModel(
            "switch",
            [Coordinate("bit", (0, 1), "record")],
            [Rule("flip", (Condition("bit", "eq", 0),), (("bit", 1),), 0.2)],
            [],
        )
        c = enumerate_model(m, [(0,)])
        spec = {
            "id": "four",
            "stages": [
                {
                    "name": str(i),
                    "advance": [
                        {"rules": ["flip"], "direction": 1 if i % 2 == 0 else -1}
                    ],
                }
                for i in range(4)
            ],
        }
        result = evaluate_monitor(compile_monitor(c, spec), np.array([1.0, 0]), 3)
        self.assertAlmostEqual(
            result["completed_probability"],
            1 - exp(-0.6) * sum(0.6**k / factorial(k) for k in range(4)),
            places=12,
        )
        self.assertAlmostEqual(
            result["physical_marginal"][0], 0.5 * (1 + exp(-1.2)), places=12
        )

    def test_monitor_abort_is_absorbing_without_restart(self):
        from omega_cosmology.testbed.backends import enumerate_model
        from omega_cosmology.testbed.monitors import compile_monitor, evaluate_monitor
        from omega_cosmology.testbed.physics import (
            Condition,
            Coordinate,
            LocalModel,
            Rule,
        )

        m = LocalModel(
            "switch",
            [Coordinate("bit", (0, 1), "record")],
            [Rule("flip", (Condition("bit", "eq", 0),), (("bit", 1),), 0.2)],
            [],
        )
        c = enumerate_model(m, [(0,)])
        spec = {
            "id": "abort",
            "stages": [
                {"name": "first", "advance": [{"rules": ["flip"], "direction": 1}]},
                {
                    "name": "second",
                    "advance": [{"rules": ["absent_in_this_law"], "direction": 1}],
                    "abort": [{"rules": ["flip"], "direction": -1}],
                },
            ],
        }
        result = evaluate_monitor(compile_monitor(c, spec), np.array([1.0, 0]), 3)
        self.assertEqual(result["completed_probability"], 0)
        self.assertAlmostEqual(
            result["failed_probability"], 1 - exp(-0.6) * (1 + 0.6), places=12
        )

    def protocol(self):
        return json.loads(
            (ROOT / "research/studies/R2-further-capacity/PROTOCOL.json").read_text(
                encoding="utf-8"
            )
        )

    def test_preparations_and_ablations_preserve_declared_accounting(self):
        from omega_cosmology.testbed.physics import LocalModel

        p = self.protocol()
        base = {r["id"]: r for r in p["laws"][0]["model"]["rules"]}
        for law in p["laws"]:
            m = LocalModel.from_record(law["model"])
            for prep in p["preparations"]:
                for state, _ in prep["roots"]:
                    m.validate(tuple(state))
                    self.assertEqual(str(m.energy(tuple(state))), p["energy_per_root"])
            rules = {r["id"]: r for r in law["model"]["rules"]}
            expected = ({"source"} if not law["driven"] else set()) | (
                {"build_store_assisted"} if law["mode"] == "basal" else set()
            )
            self.assertEqual(set(base) - set(rules), expected)
            self.assertTrue(all(rule == base[name] for name, rule in rules.items()))

    def test_expanded_capture_really_requires_the_new_capacity(self):
        from omega_cosmology.testbed.monitors import event_matches, state_value
        from omega_cosmology.testbed.physics import LocalModel

        p = self.protocol()
        m = LocalModel.from_record(p["laws"][0]["model"])
        capture = p["event_readouts"][0]["selectors"][0]
        for bank in (3, 4):
            source = (1, 1, 1, 2, bank, 1)
            event = next(
                e
                for e in m.events(source)
                if e.rule_id == "capture" and e.direction == 1
            )
            self.assertTrue(event_matches(m, source, event, capture))
            shadow_source = (*source[:-1], 0)
            shadow_target = (*event.target[:-1], 0)
            self.assertTrue(m.valid(shadow_source))
            self.assertFalse(m.valid(shadow_target))
        amount = p["event_readouts"][-1]["amount"]
        self.assertEqual(state_value(m, (0, 1, 0, 1, 5, 1), amount), 0.5)
        self.assertEqual(state_value(m, (0, 1, 0, 1, 6, 1), amount), 1.0)

    def test_sham_keeps_construction_and_blocks_only_extra_bank_capacity(self):
        from omega_cosmology.testbed.physics import LocalModel

        p = self.protocol()
        full = LocalModel.from_record(p["laws"][0]["model"])
        sham = LocalModel.from_record(
            next(l for l in p["laws"] if l["id"] == "driven__sham")["model"]
        )
        self.assertTrue(full.valid((1, 1, 1, 1, 5, 1)))
        self.assertFalse(sham.valid((1, 1, 1, 1, 5, 1)))
        source = (1, 1, 1, 1, 2, 0)
        for model in (full, sham):
            self.assertTrue(
                any(
                    e.rule_id == "build_store_assisted" and e.direction == 1
                    for e in model.events(source)
                )
            )

    def test_shared_assay_reproduces_retained_r1_profile(self):
        from omega_cosmology.testbed.finite_study import evaluate_case

        p = copy.deepcopy(
            json.loads(
                (
                    ROOT / "research/studies/R1-constructed-access/PROTOCOL.json"
                ).read_text(encoding="utf-8")
            )
        )
        p["horizons"] = [16]
        p["sufficiency"] = "Full declared local state"
        p["boundary_scope"] = {"bath": "one", "source": "declared"}
        p["conserved"] = ["fixed slots", "one carrier"]
        p["observables"] = [{"id": "bound", "terms": [["bond", 1]]}]
        p["event_readouts"] = []
        p["monitors"] = []
        actual = evaluate_case(p, p["laws"][0], 0.25)
        retained = json.loads(
            (
                ROOT
                / "research/studies/R1-constructed-access/results-2026-10-24/cases/driven__intact__dt0p25.json"
            ).read_text(encoding="utf-8")
        )
        for row in actual["rows"]:
            expected = next(
                v
                for v in retained["rows"]
                if v["preparation"] == row["preparation"] and v["horizon"] == 16
            )
            self.assertAlmostEqual(
                row["history"]["ell_bits"], expected["history"]["ell_bits"], places=10
            )
            self.assertAlmostEqual(
                row["physical"]["work_net"], expected["physical"]["work_net"], places=10
            )
            self.assertAlmostEqual(
                row["observables"]["bound"]["endpoint"],
                expected["function"]["bound_probability"],
                places=10,
            )


if __name__ == "__main__":
    unittest.main()
