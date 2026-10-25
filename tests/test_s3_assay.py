"""End-to-end semantics for unequal intact roots and matched damaged roots."""

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "src")]
from write_s3_protocols import repair_protocol

from omega_cosmology.testbed.finite_study import evaluate_case
from omega_cosmology.testbed.repair import repair_capacity_world


class S3AssayTests(unittest.TestCase):
    def test_declared_energy_and_foreclosure_integrate_without_proxy(self):
        m = repair_capacity_world()
        p = repair_protocol(m, horizons=(0.25, 0.5))
        result = evaluate_case(p, {"id": "repair", "model": m.record()}, 0.25)
        self.assertEqual(len(result["rows"]), 6)
        self.assertEqual(len(result["foreclosure_comparisons"]), 18)
        self.assertTrue(
            all(
                r["structurally_certified_zero"]
                for r in result["foreclosure_comparisons"]
            )
        )
        self.assertTrue(
            all(
                r["functional_profiles"]["repair"]["structural_closure_state_count"]
                == 0
                for r in result["rows"]
            )
        )
        damaged = next(r for r in result["rows"] if r["preparation"] == "repair_fault")
        self.assertEqual(
            damaged["functional_profiles"]["repair"]["initial_functional_probability"],
            0,
        )
        self.assertGreater(
            damaged["functional_profiles"]["repair"]["ever_functional_probability"], 0
        )
        bad = copy.deepcopy(p)
        bad["preparations"][0].pop("energy_per_root")
        with self.assertRaises(ValueError):
            evaluate_case(bad, {"id": "repair", "model": m.record()}, 0.25)
