"""Restoration rejects changed evidence and unlisted executable inputs."""

import json
import sys
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from restore_p0_t_verification import restore
from restore_research_snapshot import write_archive


def raw(value):
    return json.dumps(value, sort_keys=True).encode()


def digest(value):
    return sha256(value).hexdigest()


class RestoreTests(unittest.TestCase):
    def fixture(self, root, *, extra=False):
        evidence = root / "evidence"
        evidence.mkdir()
        source = b"original native program\n"
        original_manifest = raw(
            {
                "files": [
                    {
                        "path": "source.py",
                        "bytes": len(source),
                        "sha256": digest(source),
                    }
                ]
            }
        )
        result = b'{"ell_bits":1}\n'
        plan = raw(
            {
                "studies": [
                    {"id": "X", "original_manifest_sha256": digest(original_manifest)}
                ],
                "input_results": [
                    {"path": "jobs/X/ORIGINAL_RESULT.json", "sha256": digest(result)}
                ],
            }
        )
        current_source = b"current independent auditor\n"
        current_manifest = raw(
            {
                "plan_sha256": digest(plan),
                "files": [{"path": "auditor.py", "sha256": digest(current_source)}],
            }
        )
        write_archive(
            evidence / "ORIGINAL_SOURCES.zip",
            {"X/MANIFEST.json": original_manifest, "X/source.py": source},
        )
        current = {"MANIFEST.json": current_manifest, "auditor.py": current_source}
        if extra:
            current["unlisted.py"] = b"unaudited input\n"
        write_archive(evidence / "AUDITOR_SNAPSHOT.zip", current)
        (evidence / "PLAN.json").write_bytes(plan)
        (evidence / "PROVENANCE.json").write_bytes(raw({"plan_sha256": digest(plan)}))
        (evidence / "retained/X").mkdir(parents=True)
        (evidence / "retained/X/ORIGINAL_RESULT.json").write_bytes(result)
        return evidence

    def test_complete_restore_without_execution(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            evidence = self.fixture(root)
            out = root / "runs/new"
            report = restore(evidence, out, repository=root)
            self.assertEqual(report["status"], "restored_not_executed")
            self.assertEqual(
                (out / "original/X/source.py").read_bytes(),
                b"original native program\n",
            )
            self.assertFalse((out / "BATCH_RECEIPT.json").exists())
            with self.assertRaises(ValueError):
                restore(evidence, out, repository=root)

    def test_changed_result_rejected_before_any_write(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            evidence = self.fixture(root)
            (evidence / "retained/X/ORIGINAL_RESULT.json").write_text(
                "changed", encoding="utf-8"
            )
            out = root / "runs/new"
            with self.assertRaises(ValueError):
                restore(evidence, out, repository=root)
            self.assertFalse(out.exists())

    def test_unlisted_auditor_input_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            evidence = self.fixture(root, extra=True)
            with self.assertRaises(ValueError):
                restore(evidence, root / "runs/new", repository=root)

    def test_changed_plan_and_outside_destination_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            evidence = self.fixture(root)
            with self.assertRaises(ValueError):
                restore(evidence, root / "outside", repository=root)
            (evidence / "PLAN.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(ValueError):
                restore(evidence, root / "runs/new", repository=root)


if __name__ == "__main__":
    unittest.main()
