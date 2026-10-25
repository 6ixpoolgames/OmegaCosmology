"""A host-memory refusal must leave a reproducible failed engineering receipt."""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import run_coupled_smoke


class SupervisorTests(unittest.TestCase):
    def test_host_refusal_is_recorded_without_starting_or_shrinking(self):
        with tempfile.TemporaryDirectory(
            dir=ROOT / "runs", prefix="supervisor-test-"
        ) as tmp:
            out = Path(tmp) / "new"
            argv = [
                "run_coupled_smoke.py",
                "--plan",
                "research/platform/models/struggle-readiness/FIDELITY_PLAN.json",
                "--out-dir",
                str(out),
            ]
            with (
                patch.object(sys, "argv", argv),
                patch(
                    "omega_cosmology.testbed.workflow.capped",
                    side_effect=MemoryError("test host reserve"),
                ) as worker,
                patch("builtins.print"),
                self.assertRaises(SystemExit) as error,
            ):
                run_coupled_smoke.main()
            self.assertEqual(error.exception.code, 1)
            worker.assert_called_once()
            receipt = json.loads((out / "BATCH_RECEIPT.json").read_text())
            self.assertEqual(receipt["status"], "failed")
            self.assertEqual(len(receipt["cases"]), 1)
            case = receipt["cases"][0]
            self.assertFalse(case["passed"])
            self.assertFalse(case["receipt"]["worker_started"])
            self.assertEqual(case["receipt"]["cap_reason"], "host_memory_preflight")
            self.assertIsNone(case["result_sha256"])
            self.assertTrue((out / "frozen/MANIFEST.json").is_file())
            self.assertFalse((out / case["id"] / "RESULT.json").exists())


if __name__ == "__main__":
    unittest.main()
