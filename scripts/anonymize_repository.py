"""Sanitize a publication tree using an ignored, locally supplied identity policy.

Never put real names, addresses or reversible identity maps in this script.
Rebuild checksummed containers bottom-up; do not silently retain stale hashes.
This tool does not publish or overwrite Git history.
"""

import argparse
import io
import json
import re
import subprocess
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path, PurePosixPath
from typing import ClassVar
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def digest(raw):
    return sha256(raw).hexdigest()


def git_files(root):
    names = (
        subprocess.check_output(
            [
                "git",
                "-c",
                "safe.directory=" + root.as_posix(),
                "ls-files",
                "-co",
                "--exclude-standard",
                "-z",
            ],
            cwd=root,
        )
        .decode("utf-8")
        .split("\0")
    )
    return sorted({n for n in names if n and (root / n).is_file()})


@dataclass
class Node:
    name: str
    original: bytes
    raw: bytes
    children: list = field(default_factory=list)
    container: bool = False

    def descendants(self):
        yield self
        for child in self.children:
            yield from child.descendants()


class Sanitizer:
    pdf_cache: ClassVar[dict] = {}

    def __init__(self, policy):
        self.policy = policy
        self.alias = policy.get("attribution", "S. Poole")
        self.source_ids = dict(policy.get("source_ids", {}))
        self.email = policy.get("attribution_email", "author@users.noreply.invalid")
        self.original_names = policy.get("personal_names", [])
        self.handles = policy.get("personal_handles", [])
        self.public_names = policy.get("preserve_public_names", [])
        self.prefixes = sorted(policy.get("path_prefixes", {}), key=len, reverse=True)
        self.id_pattern = None

    def add_source_id(self, value):
        if value and not value.startswith("source-"):
            self.source_ids.setdefault(value, "source-" + digest(value.encode())[:20])

    def discover(self, text):
        for value in re.findall(
            r"https?://(?:drive|docs)\.google\.com/(?:file/d/|document/d/|spreadsheets/d/|presentation/d/|drive/(?:u/\d+/)?folders/)([\w-]+)",
            text,
        ):
            self.add_source_id(value)
        for value in re.findall(r"(?:[?&](?:id|fileId)=)([A-Za-z0-9_-]{20,})", text):
            self.add_source_id(value)

    def prepare(self):
        self.id_pattern = (
            re.compile(
                "|".join(
                    re.escape(k) for k in sorted(self.source_ids, key=len, reverse=True)
                )
            )
            if self.source_ids
            else None
        )

    def text(self, value):
        # Public scientific authors are not the project's owner merely because
        # they share a first name. Preserve their complete names/citations.
        protected = {}
        for public in self.public_names:
            pattern = re.compile(
                r"\b" + re.escape(public).replace(r"\ ", r"\s+") + r"\b", re.IGNORECASE
            )

            def preserve(match):
                key = f"OMEGAPUBLICCITATIONTOKEN{len(protected)}END"
                protected[key] = match[0]
                return key

            value = pattern.sub(preserve, value)
        for old in self.prefixes:
            value = value.replace(old, self.policy["path_prefixes"][old])
        # Decode JSON structurally before this function; normal and doubled
        # path separators are both handled in prose and embedded source code.
        value = re.sub(
            r"(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"'<>]+", "<user-home>", value
        )
        value = re.sub(r"(?<![\w])/(?:Users|home)/[^/\s\"'<>]+", "<user-home>", value)
        for address in self.policy.get("personal_emails", []):
            value = re.sub(re.escape(address), self.email, value, flags=re.IGNORECASE)
        if self.handles:
            handles = "(?:" + "|".join(re.escape(h) for h in self.handles) + ")"
            value = re.sub(
                r"https?://github\.com/" + handles + r"/([^\s\"'<>\]\)]+)",
                r"repository://\1",
                value,
                flags=re.IGNORECASE,
            )
        # Never substitute a new live URL for a removed personal Drive source.
        value = re.sub(
            r"https?://(?:drive|docs)\.google\.com/[^\s\"'<>\]\)]+",
            lambda m: "source://" + self._url_source(m[0]),
            value,
        )
        if self.id_pattern:
            value = self.id_pattern.sub(lambda m: self.source_ids[m[0]], value)
        for name in sorted(self.original_names, key=len, reverse=True):
            # Official ownership notices use the requested pseudonym. Ordinary
            # narrative, decisions and chat speaker labels are de-identified.
            pattern = re.compile(
                r"(?i)(\b(?:originator|author|copyright(?:\s*\(c\))?|copyright holder)\b[^\r\n:]{0,30}:?\s*)\b"
                + re.escape(name)
                + r"\b"
            )
            value = pattern.sub(lambda m: m[1] + self.alias, value)
            value = re.sub(
                r"(?im)^([ \t#>*-]*)" + re.escape(name) + r"\s*:", r"\1User:", value
            )
            value = re.sub(
                r"\b" + re.escape(name) + r"\b",
                "the author",
                value,
                flags=re.IGNORECASE,
            )
        for handle in sorted(self.handles, key=len, reverse=True):
            value = re.sub(
                r"(?im)(copyright[^\r\n]{0,25})\b" + re.escape(handle) + r"\b",
                lambda m: m[1] + self.alias,
                value,
            )
            value = re.sub(
                r"(?<![\w])" + re.escape(handle) + r"(?![\w])",
                "project-owner",
                value,
                flags=re.IGNORECASE,
            )
        # Only XML content is editor metadata; quoted source regexes are not.
        if value.lstrip().startswith("<"):
            value = re.sub(
                r"(<(?:dc:creator|cp:lastModifiedBy|Company|Manager)>)[\s\S]*?(</(?:dc:creator|cp:lastModifiedBy|Company|Manager)>)",
                lambda m: (
                    m[1] + (self.alias if "creator" in m[1] else "Contributor") + m[2]
                ),
                value,
            )
            value = re.sub(r'(w:author=")[^"]*(")', r"\1Contributor\2", value)
        for key, public in protected.items():
            value = value.replace(key, public)
        return value

    def _url_source(self, url):
        for old, alias in self.source_ids.items():
            if old in url:
                return alias
        return "source-" + digest(url.encode())[:20]

    def value(self, value):
        if isinstance(value, str):
            return self.text(value)
        if isinstance(value, list):
            return [self.value(v) for v in value]
        if isinstance(value, dict):
            return {self.text(k): self.value(v) for k, v in value.items()}
        return value

    def parse(self, name, raw, *, depth=0):
        if depth > 8:
            raise ValueError("Nested archive depth exceeds audit bound")
        name = self.text(name)
        node = Node(name, raw, raw)
        if raw.startswith(b"PK\x03\x04"):
            with ZipFile(io.BytesIO(raw)) as z:
                if sum(v.file_size for v in z.infolist()) > 256 * 1024**2:
                    raise ValueError("Archive exceeds uncompressed audit bound")
                for info in z.infolist():
                    path = PurePosixPath(info.filename)
                    if path.is_absolute() or ".." in path.parts or info.flag_bits & 1:
                        raise ValueError(
                            "Unsafe or encrypted archive needs explicit review"
                        )
                    if not info.is_dir():
                        node.children.append(
                            self.parse(info.filename, z.read(info), depth=depth + 1)
                        )
            if len({v.name for v in node.children}) != len(node.children):
                raise ValueError("Anonymization creates duplicate archive names")
            node.container = True
            node.raw = self.pack(node)
        elif raw.startswith(b"%PDF-"):
            node.raw = self.pdf(raw)
        else:
            try:
                text = raw.decode(
                    "utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8"
                )
            except UnicodeDecodeError:
                return node
            if name.lower().endswith(".json"):
                try:
                    old = json.loads(text)
                    new = self.value(old)
                    if new != old:
                        node.raw = (
                            json.dumps(
                                new, indent=2, ensure_ascii=False, allow_nan=False
                            )
                            + "\n"
                        ).encode()
                except json.JSONDecodeError:
                    node.raw = self.text(text).encode()
            else:
                node.raw = self.text(text).encode()
        return node

    @staticmethod
    def pack(node):
        stream = io.BytesIO()
        with ZipFile(stream, "w", compression=ZIP_DEFLATED, compresslevel=6) as z:
            for child in sorted(node.children, key=lambda c: c.name):
                entry = ZipInfo(child.name, date_time=(1980, 1, 1, 0, 0, 0))
                entry.compress_type = ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                z.writestr(entry, child.raw)
        return stream.getvalue()

    def pdf(self, raw):
        key = (digest(raw), digest(json.dumps(self.policy, sort_keys=True).encode()))
        if key in self.pdf_cache:
            return self.pdf_cache[key]
        try:
            from pypdf import PdfReader, PdfWriter
        except ImportError as error:
            raise RuntimeError(
                "PDF privacy audit requires the optional pypdf dependency"
            ) from error
        reader = PdfReader(io.BytesIO(raw))
        for page in reader.pages:
            text = page.extract_text() or ""
            if self.text(text) != text:
                raise ValueError(
                    "PDF visible text contains a privacy target; real content redaction required"
                )
        writer = PdfWriter(clone_from=reader)
        metadata = {
            str(k): self.text(str(v))
            for k, v in (reader.metadata or {}).items()
            if k in ("/Title", "/Subject", "/Keywords")
        }
        metadata["/Author"] = self.alias
        writer.metadata = metadata
        # Drop XMP/editor metadata; embedded files would require their own audit.
        writer.root_object.pop("/Metadata", None)
        if (
            "/Names" in writer.root_object
            and "/EmbeddedFiles" in writer.root_object["/Names"]
        ):
            raise ValueError("PDF attachments need explicit recursive review")
        for page in writer.pages:
            for reference in page.get("/Annots", []):
                annotation = reference.get_object()
                if "/A" in annotation and "/URI" in annotation["/A"]:
                    from pypdf.generic import TextStringObject

                    annotation["/A"]["/URI"] = TextStringObject(
                        self.text(str(annotation["/A"]["/URI"]))
                    )
        stream = io.BytesIO()
        writer.write(stream)
        result = stream.getvalue()
        self.pdf_cache[key] = result
        return result


def repair_references(nodes, *, max_passes=60):
    """Propagate byte hashes/sizes through nested manifests to a fixed point.

    This repairs file-integrity references, never scientific model fingerprints
    unless they actually equal a changed file's byte digest. Cycles are rejected.
    """
    all_nodes = [n for top in nodes for n in top.descendants()]
    replacements = {}

    def changed(before, after):
        if before != after:
            replacements[digest(before)] = (digest(after), len(after))

    for n in all_nodes:
        changed(n.original, n.raw)
    for iteration in range(max_passes):
        progress = False

        def resolve(h):
            seen = set()
            result = None
            while h in replacements:
                if h in seen:
                    raise ValueError("Cyclic digest replacement")
                seen.add(h)
                result = replacements[h]
                h = result[0]
            return result

        resolved = {k: resolve(k) for k in list(replacements)}
        pattern = (
            re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])") if resolved else None
        )

        def values(v, resolved=resolved, pattern=pattern):
            if isinstance(v, dict):
                new = {k: values(x) for k, x in v.items()}
                old_hash = v.get("sha256")
                if old_hash in resolved and "bytes" in new:
                    new["bytes"] = resolved[old_hash][1]
                if (
                    "total_bytes" in new
                    and isinstance(new.get("files"), list)
                    and all(
                        isinstance(r, dict) and isinstance(r.get("bytes"), int)
                        for r in new["files"]
                    )
                ):
                    new["total_bytes"] = sum(r["bytes"] for r in new["files"])
                return new
            if isinstance(v, list):
                return [values(x) for x in v]
            if isinstance(v, str) and pattern:
                return pattern.sub(lambda m: resolved.get(m[0], (m[0], 0))[0], v)
            return v

        for node in reversed(all_nodes):
            old = node.raw
            if node.container:
                new = Sanitizer.pack(node)
            else:
                try:
                    text = old.decode("utf-8")
                except UnicodeDecodeError:
                    continue
                if node.name.lower().endswith(".json"):
                    try:
                        obj = json.loads(text)
                        new_obj = values(obj)
                        new = (
                            (
                                json.dumps(
                                    new_obj,
                                    indent=2,
                                    ensure_ascii=False,
                                    allow_nan=False,
                                )
                                + "\n"
                            ).encode()
                            if new_obj != obj
                            else old
                        )
                    except json.JSONDecodeError:
                        new = (
                            pattern.sub(
                                lambda m, resolved=resolved: resolved.get(
                                    m[0], (m[0], 0)
                                )[0],
                                text,
                            ).encode()
                            if pattern
                            else old
                        )
                else:
                    new = (
                        pattern.sub(
                            lambda m, resolved=resolved: resolved.get(m[0], (m[0], 0))[
                                0
                            ],
                            text,
                        ).encode()
                        if pattern
                        else old
                    )
            if new != old:
                node.raw = new
                changed(old, new)
                progress = True
        if not progress:
            return {"passes": iteration + 1, "digest_replacements": len(replacements)}
    raise ValueError(
        "Integrity references did not stabilize; no tree should be written"
    )


def discover_sources(sanitizer, records):
    """Source IDs are opaque local aliases, including those in archive names."""

    def visit(name, raw):
        if "/files/" in name and name.startswith("archive/drive/"):
            sanitizer.add_source_id(Path(name).stem)
        if raw.startswith(b"PK\x03\x04"):
            with ZipFile(io.BytesIO(raw)) as z:
                for info in z.infolist():
                    if not info.is_dir():
                        visit(info.filename, z.read(info))
        else:
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                return
            sanitizer.discover(text)
            if (
                name.endswith("MANIFEST.json")
                and '"folders"' in text
                and '"roots"' in text
            ):
                data = json.loads(text)
                for collection in ("roots", "folders", "files"):
                    for row in data.get(collection, []):
                        if isinstance(row, dict) and "id" in row:
                            sanitizer.add_source_id(row["id"])

    for name, raw in records.items():
        visit(name, raw)
    sanitizer.prepare()


def sanitize_tree(records, policy):
    sanitizer = Sanitizer(policy)
    discover_sources(sanitizer, records)
    nodes = [sanitizer.parse(name, raw) for name, raw in records.items()]
    if len({n.name for n in nodes}) != len(nodes):
        raise ValueError("Anonymization creates duplicate file names")
    integrity = repair_references(nodes)
    return {n.name: n.raw for n in nodes}, {
        "files": len(nodes),
        "containers_and_members": sum(1 for n in nodes for _ in n.descendants()),
        "changed_payloads": sum(
            n.raw != n.original for top in nodes for n in top.descendants()
        ),
        "source_aliases": len(sanitizer.source_ids),
        **integrity,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument(
        "--policy",
        type=Path,
        required=True,
        help="Ignored local identity policy, never committed",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Fresh private staging tree; original checkout is not overwritten",
    )
    args = parser.parse_args()
    root, out = args.root.resolve(), args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(root / ".local"):
        parser.error("Choose a fresh ignored .local/ destination")
    records = {n: (root / n).read_bytes() for n in git_files(root)}
    result, summary = sanitize_tree(
        records, json.loads(args.policy.read_text(encoding="utf-8"))
    )
    out.mkdir(parents=True)
    for name, raw in result.items():
        target = (out / name).resolve()
        if not target.is_relative_to(out):
            raise ValueError("Unsafe sanitized file path")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
