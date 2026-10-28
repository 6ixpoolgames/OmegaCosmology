"""Reject altered provenance, parameters and refunds in the fixed C.7 audit."""

import json
import math
import sys
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from scipy.sparse import csr_matrix

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from replay_c7 import audit_events, check_pair, fingerprint, verify_original_bundle


class C7ReplayTests(unittest.TestCase):
    def test_source_tampering_rejected_after_valid_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "source").mkdir()
            raw = b"frozen physical law\n"
            (root / "source/law.py").write_bytes(raw)
            sources = [
                {"path": "law.py", "sha256": sha256(raw).hexdigest(), "bytes": len(raw)}
            ]
            m = {
                "schema_version": "omega-frozen-bundle/1",
                "config": {},
                "sources": sources,
                "source_hash": fingerprint(sources),
            }
            m["input_hash"] = fingerprint(m)
            (root / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
            self.assertEqual(verify_original_bundle(root), m)
            (root / "source/law.py").write_bytes(b"changed physical law\n")
            with self.assertRaisesRegex(ValueError, "source bytes"):
                verify_original_bundle(root)

    def test_different_source_is_reported_without_boundary_certificate(self):
        left = {
            "mechanism": "loop",
            "target_number": 2,
            "target": 0.1,
            "parameters": {"capacity": 4, "supply_rate": 0.04, "quantum": 0.5},
        }
        right = {
            **left,
            "mechanism": "basal",
            "parameters": {**left["parameters"], "supply_rate": 0.05},
        }
        audit = check_pair(left, right)
        self.assertFalse(audit["identical_boundaries"])
        self.assertEqual(
            audit["current_identical_boundary_certificate"], "inapplicable"
        )
        right["parameters"]["quantum"] = 1
        with self.assertRaisesRegex(ValueError, "parameter difference"):
            check_pair(left, right)

    @staticmethod
    def bank_world(refund):
        states = ((0, 0, 0), (1, 0, 0))
        reverse = math.exp(-3)

        def events(s):
            forward = s[0] == 1
            return [
                SimpleNamespace(
                    target=states[0 if forward else 1],
                    rate=1 if forward else reverse,
                    family="bank_leak" if forward else "leak_reverse",
                    work=0,
                    increments={"leak_bank_debit": 0.5}
                    if forward
                    else {"leak_bath_import": refund},
                )
            ]

        world = SimpleNamespace(
            modules=[SimpleNamespace(id="bank", events=events)],
            energy=lambda s: 0.5 * s[0],
        )
        return {
            "world": world,
            "states": states,
            "index": {s: i for i, s in enumerate(states)},
            "Q": csr_matrix([[-reverse, reverse], [1, -1]]),
            "flows": {
                "bath_heat": np.array([-0.5 * reverse, 0.5]),
                "resource_work": np.zeros(2),
            },
        }

    def test_actual_reverse_refund_audited_against_bank_state(self):
        params = SimpleNamespace(capacity=4, quantum=0.5, beta=6)
        audit_events(self.bank_world(0.5), params)
        with self.assertRaisesRegex(ArithmeticError, "accounting failed"):
            audit_events(self.bank_world(0.6), params)

    def test_altered_generator_rejected_even_with_valid_events(self):
        compiled = self.bank_world(0.5)
        compiled["Q"] = compiled["Q"] * 2
        with self.assertRaisesRegex(ArithmeticError, "accounting failed"):
            audit_events(compiled, SimpleNamespace(capacity=4, quantum=0.5, beta=6))


if __name__ == "__main__":
    unittest.main()
