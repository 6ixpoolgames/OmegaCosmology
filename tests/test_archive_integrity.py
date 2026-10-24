"""Concrete intake risks: path escape, changed source bytes and fake exports."""
from hashlib import sha256
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_archive import verify_rows


class ArchiveIntegrityTest(unittest.TestCase):
    def test_rejects_changed_bytes_and_duplicate_entries(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / 'archive').mkdir()
            target = root / 'archive/source.md'
            target.write_bytes(b'original')
            row = {'path': 'archive/source.md', 'bytes': 8, 'sha256': sha256(b'original').hexdigest()}
            self.assertEqual(verify_rows(root, [row], ('archive',)), [])
            self.assertTrue(verify_rows(root, [row, row], ('archive',)))
            target.write_bytes(b'changed!')
            self.assertTrue(verify_rows(root, [row], ('archive',)))

    def test_rejects_scope_escape_and_non_docx_export(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / 'archive').mkdir()
            row = {'path': 'archive/../outside.md', 'bytes': 0, 'sha256': sha256(b'').hexdigest()}
            self.assertTrue(verify_rows(root, [row], ('archive',)))
            target = root / 'archive/fake.docx'
            target.write_bytes(b'not a document container')
            row = {'path': 'archive/fake.docx', 'bytes': target.stat().st_size,
                   'sha256': sha256(target.read_bytes()).hexdigest(), 'representation': 'docx_export'}
            self.assertTrue(verify_rows(root, [row], ('archive',)))


if __name__ == '__main__':
    unittest.main()
