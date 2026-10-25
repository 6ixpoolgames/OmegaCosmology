"""Independent cue-statistic checks and native mark-ledger completeness."""

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))
from report_readiness_fidelity import cue_metrics
from write_readiness_fidelity import pilot_protocol

from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.monitors import event_rewards
from omega_cosmology.testbed.readiness import POLICIES, readiness_root, readiness_world


class FidelityTests(unittest.TestCase):
    def test_association_and_base_rate_are_separate(self):
        independent = cue_metrics([[0.72, 0.08], [0.18, 0.02]])
        self.assertAlmostEqual(independent["mutual_information_bits"], 0)
        self.assertAlmostEqual(independent["balanced_accuracy"], 0.5)
        perfect = cue_metrics([[0.75, 0], [0, 0.25]])
        self.assertAlmostEqual(perfect["positive_predictive_value"], 1)
        self.assertAlmostEqual(perfect["balanced_accuracy"], 1)
        self.assertGreater(perfect["mutual_information_bits"], 0.8)
        constant = cue_metrics([[0.9, 0.1], [0, 0]])
        self.assertIsNone(constant["positive_predictive_value"])
        self.assertAlmostEqual(constant["accuracy"], constant["always_closed_accuracy"])
        with self.assertRaises(ValueError):
            cue_metrics([[0.9, 0.9], [0, 0]])

    def test_mark_drift_matches_generator_for_every_native_state(self):
        for policy in POLICIES:
            model = readiness_world(policy, opening_rate=None)
            protocol = pilot_protocol(model, policy=policy, quantum=".5", effort=".5")
            compiled = enumerate_model(model, [readiness_root(model)], max_states=3000)
            compiled.require_complete()
            rewards = event_rewards(compiled, protocol["event_readouts"])
            births = sum(
                rewards[k]
                for k in (
                    "marks_failed_attempt",
                    "marks_reverse_clear",
                    "marks_thermal",
                )
            )
            deaths = sum(
                rewards[k]
                for k in ("marks_undo_attempt", "marks_cleared", "marks_relaxed")
            )
            marks = np.array(
                [s[model.indices["body.failures"]] for s in compiled.states]
            )
            np.testing.assert_allclose(compiled.q @ marks, births - deaths, atol=1e-12)
            if policy == "conserve":
                np.testing.assert_array_equal(rewards["marks_failed_attempt"], 0)
                self.assertGreater(max(rewards["marks_thermal"]), 0)


if __name__ == "__main__":
    unittest.main()
