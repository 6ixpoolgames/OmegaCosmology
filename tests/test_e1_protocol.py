"""Matching, factor isolation, case-plan and backward-compatibility checks."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from omega_cosmology.testbed.physical_modules import autocatalytic_ecology
from omega_cosmology.testbed.physics import LocalModel
from scripts.run_finite_study import study_cases
from scripts.write_e1_protocol import build_protocol


class E1ProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = build_protocol()

    def test_inventory_energies_and_state_space_are_matched(self):
        for law in self.protocol["laws"]:
            m = LocalModel.from_record(law["model"])
            self.assertEqual(len(m.coordinates), 7)
            for prep in self.protocol["preparations"]:
                state = tuple(prep["roots"][0][0])
                m.validate(state)
                self.assertEqual(m.energy(state), 2)
            self.assertEqual(m.coordinates[2].domain, (0, 1, 2))
            self.assertEqual(m.coordinates[5].domain, (0, 1, 2))

    def test_cost_change_does_not_change_capacity_or_capture_yield(self):
        models = {}
        for law in self.protocol["laws"]:
            if (
                law["mechanism"] == "local"
                and law["regime"]["source"] == 0.02
                and law["regime"]["turnover"] == 0.001
            ):
                models[law["regime"]["bill_ticks"]] = LocalModel.from_record(
                    law["model"]
                )
        for bill, m in models.items():
            source = (1, 0, 2, 1, 0, 2, 0)
            e = next(
                e
                for e in m.events(source)
                if e.rule_id == "assisted_construct_A.x_to_A.y" and e.direction == 1
            )
            self.assertEqual(e.target[2], 2 - bill)
            self.assertAlmostEqual(e.heat, 0.5 * bill - 0.5)
        a, b = models[1], models[2]
        self.assertEqual(a.coordinates, b.coordinates)
        self.assertEqual(a.energy_terms, b.energy_terms)
        captures = lambda m: {r.id: r for r in m.rules if "capture" in r.id}
        self.assertEqual(captures(a), captures(b))

    def test_ablation_removes_only_paired_catalytic_routes(self):
        grouped = {}
        for law in self.protocol["laws"]:
            grouped.setdefault(law["regime"]["id"], {})[law["mechanism"]] = law
        for family in grouped.values():
            full = {r["id"]: r for r in family["local"]["model"]["rules"]}
            ablated = {r["id"]: r for r in family["ablation"]["model"]["rules"]}
            self.assertEqual(
                ablated,
                {k: v for k, v in full.items() if not k.startswith("assisted_")},
            )
            self.assertEqual(
                family["ablation"]["model"]["energy_terms"],
                family["local"]["model"]["energy_terms"],
            )
            self.assertEqual(family["ablation"]["structural_analysis"]["ancestry"], [])

    def test_grid_and_subset_cadence_audit_are_explicit(self):
        p = self.protocol
        cases = study_cases(p)
        self.assertEqual(len(p["laws"]), 45)
        self.assertEqual(len(cases), 65)
        self.assertEqual(cases[0][1], 0.125)
        self.assertEqual(len(cases) * len(p["preparations"]) * len(p["horizons"]), 650)
        self.assertEqual(len({k for k, dt in cases if dt == 0.125}), 10)
        bad = {**p, "case_grid": [["unknown", 0.25]]}
        with self.assertRaises(ValueError):
            study_cases(bad)
        default = {k: v for k, v in p.items() if k != "case_grid"}
        self.assertEqual(
            study_cases(default)[0], (p["laws"][0]["id"], p["cadences"][0])
        )

    def test_existing_smoke_defaults_are_unchanged(self):
        p = json.loads(
            (
                ROOT
                / "research/platform/models/coupled-autocatalysis/ENGINEERING_PLAN.json"
            ).read_text()
        )
        retained = next(
            c["law"]["model"] for c in p["cases"] if c["id"] == "shared_pair"
        )
        groups = [
            {"id": g, "members": [g + ".x", g + ".y"], "access_member": g + ".x"}
            for g in ("A", "B")
        ]
        self.assertEqual(
            autocatalytic_ecology(groups).fingerprint(),
            LocalModel.from_record(retained).fingerprint(),
        )


if __name__ == "__main__":
    unittest.main()
