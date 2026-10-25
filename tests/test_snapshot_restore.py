"""Snapshot bytes, partial-input integrity and safe restoration destinations."""

import json
import sys
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from restore_research_snapshot import restore


class SnapshotTests(unittest.TestCase):
    def test_full_and_partial_snapshot_bytes_and_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "runs").mkdir()
            raw = b"line1\r\nline2\n"
            manifest = {
                "files": [{"path": "src/a.txt", "sha256": sha256(raw).hexdigest()}]
            }
            archive = root / "snapshot.zip"
            with ZipFile(archive, "w") as z:
                z.writestr("MANIFEST.json", json.dumps(manifest))
                z.writestr("src/a.txt", raw)
            restore(archive, root / "runs/full", repository=root)
            self.assertEqual((root / "runs/full/src/a.txt").read_bytes(), raw)
            with ZipFile(archive, "w") as z:
                z.writestr("MANIFEST.json", json.dumps(manifest))
            (root / "src").mkdir()
            (root / "src/a.txt").write_bytes(raw)
            restore(archive, root / "runs/partial", repository=root)
            (root / "src/a.txt").write_bytes(b"changed")
            with self.assertRaises(ValueError):
                restore(archive, root / "runs/bad", repository=root)
            self.assertFalse((root / "runs/bad").exists())

    def test_traversal_and_overwrite_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "runs").mkdir()
            archive = root / "bad.zip"
            with ZipFile(archive, "w") as z:
                z.writestr("../outside", "bad")
            with self.assertRaises(ValueError):
                restore(archive, root / "runs/out", repository=root)
            with self.assertRaises(ValueError):
                restore(archive, root / "runs", repository=root)
