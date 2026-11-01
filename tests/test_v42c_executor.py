"""End-to-end scientific executor on a small, explicitly different reference."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class ExecutorTests(unittest.TestCase):
    def test_small_reference_actual_contracts_accounts_and_scores(self):
        spec = importlib.util.spec_from_file_location(
            "v42c_executor",
            Path(__file__).resolve().parents[1] / "scripts/run_v42c_science.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        world = module.spatial_world

        def root(model):
            values = {"site.0": 1, "site.1": 1, "site.2": 2, "site.3": 2, "bank": 2}
            result = tuple(values.get(c.name, 0) for c in model.coordinates)
            model.validate(result)
            return result

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            with (
                patch.object(module, "spatial_world", lambda: world(columns=2)),
                patch.object(module, "preparation_root", root),
            ):
                module.worker(out, "aa", "short", 0.5, True)
            result = json.loads((out / "RESULT.json").read_text())
            contracts = json.loads((out / "CONTRACTS.json").read_text())
            self.assertEqual(result["states"], 126)
            self.assertTrue(
                all(
                    c["status"] == "validated_paired_comparison"
                    for c in contracts.values()
                )
            )
            self.assertLess(max(result["endpoint_residuals"].values()), 1e-10)
            self.assertGreater(result["ell_bits"]["64"], result["ell_bits"]["16"])
            self.assertTrue((out / "PROFILE.npz").exists())


if __name__ == "__main__":
    unittest.main()
