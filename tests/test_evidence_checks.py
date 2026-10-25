"""The byte check must catch the line-ending corruption seen on publication."""

import json
import sys
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_evidence import check


class EvidenceCheckTests(unittest.TestCase):
    def test_line_ending_rewrite_is_detected_without_changing_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "research/study"
            folder.mkdir(parents=True)
            raw = b"physical result\r\n"
            target = folder / "data.txt"
            target.write_bytes(raw)
            (folder / "EVIDENCE.json").write_text(
                json.dumps(
                    {
                        "files": [
                            {
                                "path": "data.txt",
                                "sha256": sha256(raw).hexdigest(),
                                "bytes": len(raw),
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(check(root)["status"], "passed")
            target.write_bytes(raw.replace(b"\r\n", b"\n"))
            self.assertEqual(check(root)["status"], "failed")


if __name__ == "__main__":
    unittest.main()
