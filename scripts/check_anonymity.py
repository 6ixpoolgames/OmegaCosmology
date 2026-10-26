"""Audit publication files and nested containers without printing private matches.

Use --policy for the ignored local identity list. Generic checks can run in CI;
absence of findings is not a guarantee against contextual re-identification.
"""

import argparse
import io
import json
import re
from pathlib import Path
from zipfile import ZipFile

from anonymize_repository import Sanitizer, git_files


def inspect(records, policy=None):
    sanitizer = Sanitizer(policy or {})
    sanitizer.prepare()
    findings = []
    count = 0

    def text_issues(text):
        issues = []
        if re.search(
            r"(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"'<>]+|(?<![\w])/(?:Users|home)/[^/\s\"'<>]+",
            text,
        ):
            issues.append("workstation_home_path")
        if re.search(r"https?://(?:drive|docs)\.google\.com/", text):
            issues.append("personal_source_url")
        emails = re.findall(r"[A-Za-z0-9_.+%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        if any(
            not v.endswith((".invalid", ".test", "@example.org", "@example.com"))
            and not "@np." in v
            for v in emails
        ):
            issues.append("contact_address_review")
        if policy and sanitizer.text(text) != text:
            issues.append("known_identity_or_editor_metadata")
        return issues

    def visit(name, raw, depth=0):
        nonlocal count
        if depth > 8:
            raise ValueError("Nested audit depth exceeded")
        count += 1
        issues = text_issues(name)
        if raw.startswith(b"PK\x03\x04"):
            with ZipFile(io.BytesIO(raw)) as z:
                if z.comment or any(i.comment or i.extra for i in z.infolist()):
                    issues.append("container_metadata_review")
                for info in z.infolist():
                    if not info.is_dir():
                        visit(name + "!" + info.filename, z.read(info), depth + 1)
        elif raw.startswith(b"%PDF-"):
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(raw))
            issues += text_issues(
                json.dumps({str(k): str(v) for k, v in (reader.metadata or {}).items()})
            )
            for page in reader.pages:
                issues += text_issues(page.extract_text() or "")
                for ref in page.get("/Annots", []):
                    issues += text_issues(str(ref.get_object().get("/A", {})))
        else:
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                text = ""
            if name.endswith(".json"):
                try:
                    # JSON escaping must not hide a host path from the audit.
                    text = json.dumps(json.loads(text), ensure_ascii=False).replace(
                        "\\\\", "\\"
                    )
                except json.JSONDecodeError:
                    pass
            issues += text_issues(text)
        if issues:
            findings.append({"path": name, "categories": sorted(set(issues))})

    for name, raw in records.items():
        visit(name, raw)
    return {
        "status": "passed" if not findings else "failed",
        "files": len(records),
        "files_and_container_members": count,
        "findings": findings,
        "scope": "Known supplied identifiers and generic contact/path/source-link metadata; context and hosting account can still identify authors",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--policy", type=Path)
    p.add_argument(
        "--file-list",
        type=Path,
        help="Relative path inventory for a staging tree without its own .git",
    )
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    root = args.root.resolve()
    names = (
        json.loads(args.file_list.read_text(encoding="utf-8"))
        if args.file_list
        else git_files(root)
    )
    policy = (
        json.loads(args.policy.read_text(encoding="utf-8")) if args.policy else None
    )
    result = inspect({n: (root / n).read_bytes() for n in names}, policy)
    raw = json.dumps(result, indent=2) + "\n"
    if args.out:
        args.out.write_text(raw, encoding="utf-8")
    print(raw)
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
