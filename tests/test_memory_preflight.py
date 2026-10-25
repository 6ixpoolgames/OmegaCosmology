"""Preflight enforces planned caps rather than relying on a printed warning."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.workflow import memory_reserve_preflight


class MemoryTests(unittest.TestCase):
    def test_low_available_memory_rejects_cap_but_smaller_job_fits(self):
        gib = 1024**3
        with self.assertRaises(MemoryError):
            memory_reserve_preflight(4 * gib, available_bytes=7 * gib)
        r = memory_reserve_preflight(2 * gib, available_bytes=7 * gib)
        self.assertEqual(r["reserve_bytes"], 4 * gib)

    def test_aggregate_commitment_and_quarter_reserve(self):
        gib = 1024**3
        r = memory_reserve_preflight(6 * gib, available_bytes=20 * gib)
        self.assertEqual(r["reserve_bytes"], 5 * gib)
        with self.assertRaises(MemoryError):
            memory_reserve_preflight(16 * gib, available_bytes=20 * gib)
