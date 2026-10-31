"""The J2 physical gate must precede every kernel/history computation."""

import hashlib
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))
runner = importlib.import_module("run_j2_discharge")


class J2GateTests(unittest.TestCase):
    def call_with(self, calibration, *, wrong_hash=False):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "physical").mkdir()
            (out / "frozen").mkdir()
            raw = json.dumps(calibration).encode()
            (out / "physical/CALIBRATION.json").write_bytes(raw)
            (out / "PLAN.json").write_text("{}")
            (out / "frozen/INPUTS.json").write_text("{}")
            with patch(
                "omega_cosmology.testbed.history.sampled_kernel",
                side_effect=AssertionError("must not score"),
            ) as kernel:
                with self.assertRaises(ValueError):
                    runner.history(
                        out, "wrong" if wrong_hash else hashlib.sha256(raw).hexdigest()
                    )
                kernel.assert_not_called()

    def test_no_joint_match_never_scores_reference_or_control(self):
        self.call_with(
            {
                "status": "no_joint_match_in_bounded_search",
                "best": {"qualified_source_fed_load": False},
                "history_permission": False,
            }
        )

    def test_no_physical_payment_never_scores(self):
        self.call_with(
            {
                "status": "qualified_joint_match",
                "best": {"qualified_source_fed_load": False},
                "history_permission": True,
            }
        )

    def test_tampered_calibration_never_scores(self):
        self.call_with({}, wrong_hash=True)


if __name__ == "__main__":
    unittest.main()
