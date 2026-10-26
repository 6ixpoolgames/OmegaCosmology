"""Privacy transformations preserve science and nested integrity references."""

import io
import json
import sys
import unittest
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from anonymize_repository import Sanitizer, sanitize_tree

POLICY = {
    "personal_names": ["Alex"],
    "personal_handles": ["example-owner"],
    "personal_emails": ["private@example.test"],
    "preserve_public_names": ["Alex Researcher"],
    "attribution": "S. Poole",
}


class AnonymizationTests(unittest.TestCase):
    def test_editor_metadata_does_not_rewrite_source_code(self):
        sanitizer = Sanitizer(POLICY)
        quoted = "pattern = " + repr(r'(w:author=")[^"]*(")')
        self.assertEqual(sanitizer.text(quoted), quoted)
        xml = '<root xmlns:w="urn:word" w:author="Example Editor" />'
        self.assertIn('w:author="Contributor"', sanitizer.text(xml))

    def test_citations_attribution_and_nonattribution_are_distinct(self):
        sanitizer = Sanitizer(POLICY)
        value = sanitizer.text(
            "Author: Alex\nAlex: test\nAlex chose it. Alex Researcher (2001). Copyright 2026 example-owner"
        )
        self.assertIn("Author: S. Poole", value)
        self.assertIn("User: test", value)
        self.assertIn("the author chose it", value)
        self.assertIn("Alex Researcher (2001)", value)
        self.assertIn("Copyright 2026 S. Poole", value)

    def test_json_paths_and_scientific_numbers(self):
        original = {
            "host": "C:" + chr(92) + chr(92).join(("Users", "private", "work")),
            "result": [1.234, 1e-13, -16],
            "email": "private@example.test",
        }
        result, _ = sanitize_tree(
            {"result.json": json.dumps(original).encode()}, POLICY
        )
        after = json.loads(result["result.json"])
        self.assertEqual(original["result"], after["result"])
        self.assertNotIn("private", after["host"])
        self.assertEqual(after["email"], "author@users.noreply.invalid")

    def test_nested_archives_and_transitive_byte_manifests(self):
        payload = b"Alex made this.\n"
        record = {
            "files": [
                {
                    "path": "source.txt",
                    "sha256": sha256(payload).hexdigest(),
                    "bytes": len(payload),
                }
            ]
        }
        buffer = io.BytesIO()
        with ZipFile(buffer, "w") as z:
            z.writestr("source.txt", payload)
            z.writestr("MANIFEST.json", json.dumps(record))
            z.comment = b"private editor"
        outer = buffer.getvalue()
        top = {
            "files": [
                {
                    "path": "snapshot.zip",
                    "sha256": sha256(outer).hexdigest(),
                    "bytes": len(outer),
                }
            ]
        }
        files, _ = sanitize_tree(
            {"snapshot.zip": outer, "EVIDENCE.json": json.dumps(top).encode()}, POLICY
        )
        with ZipFile(io.BytesIO(files["snapshot.zip"])) as z:
            inner = json.loads(z.read("MANIFEST.json"))["files"][0]
            self.assertEqual(inner["sha256"], sha256(z.read("source.txt")).hexdigest())
            self.assertEqual(inner["bytes"], len(z.read("source.txt")))
            self.assertEqual(z.comment, b"")
        outer_row = json.loads(files["EVIDENCE.json"])["files"][0]
        self.assertEqual(outer_row["sha256"], sha256(files["snapshot.zip"]).hexdigest())
        self.assertEqual(outer_row["bytes"], len(files["snapshot.zip"]))

    def test_personal_source_links_use_nonlive_aliases(self):
        identifier = "abcdefghijklmnop" + "1234567890"
        source = "https://" + "drive.google.com/file/d/" + identifier + "/view"
        files, _ = sanitize_tree({"readme.md": source.encode()}, POLICY)
        value = files["readme.md"].decode()
        self.assertTrue(value.startswith("source://source-"))
        self.assertNotIn(identifier, value)
        self.assertEqual(
            Sanitizer(POLICY).text(
                "https://github.com/example-owner/repo/blob/abc/a.md"
            ),
            "repository://repo/blob/abc/a.md",
        )


if __name__ == "__main__":
    unittest.main()
