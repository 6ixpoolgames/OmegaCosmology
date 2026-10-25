"""Restore a byte-exact research snapshot into a fresh ignored run directory.

Partial historical archives can take immutable missing inputs from this checkout,
only when their manifest hash matches. No simulation is run by this command.
"""

import argparse
import json
from hashlib import sha256
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]


def write_archive(target, files):
    """Deterministic compressed storage; original paths and bytes are preserved."""
    target = Path(target)
    if target.exists():
        raise ValueError("Snapshot archive already exists")
    with ZipFile(target, "w", compression=ZIP_DEFLATED, compresslevel=6) as z:
        for name, raw in sorted(files.items()):
            entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            z.writestr(entry, raw)
    with ZipFile(target) as z:
        if set(z.namelist()) != set(files) or any(
            z.read(k) != v for k, v in files.items()
        ):
            raise ArithmeticError("Snapshot compression changed input bytes")


def restore(archive, out, *, manifest_path=None, repository=ROOT):
    repository, out = Path(repository).resolve(), Path(out).resolve()
    if out.exists() or not out.is_relative_to(repository / "runs"):
        raise ValueError("Choose a fresh output directory inside runs")
    with ZipFile(archive) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        if (
            len(set(names)) != len(names)
            or sum(i.file_size for i in infos) > 128 * 1024**2
        ):
            raise ValueError("Duplicate names or oversized snapshot archive")
        for name in names:
            relative = PurePosixPath(name)
            if (
                relative.is_absolute()
                or ".." in relative.parts
                or "\\" in name
                or ":" in name
            ):
                raise ValueError("Unsafe snapshot path")
        raw_manifest = (
            Path(manifest_path).read_bytes()
            if manifest_path
            else z.read("MANIFEST.json")
        )
        manifest = json.loads(raw_manifest)
        records = manifest["files"]
        allowed = {r["path"] for r in records} | {"MANIFEST.json"}
        if len(allowed) != len(records) + 1 or set(names) - allowed:
            raise ValueError("Archive and input manifest disagree")
        restored = {}
        for row in records:
            name = row["path"]
            relative = PurePosixPath(name)
            path = (out / name).resolve()
            source = (repository / name).resolve()
            if (
                relative.is_absolute()
                or ".." in relative.parts
                or "\\" in name
                or ":" in name
                or not path.is_relative_to(out)
                or not source.is_relative_to(repository)
            ):
                raise ValueError("Unsafe manifest path")
            raw = z.read(name) if name in names else source.read_bytes()
            if sha256(raw).hexdigest() != row["sha256"]:
                raise ValueError("Snapshot input hash mismatch: " + name)
            restored[name] = raw
    # Validate all inputs before creating any output. No overwrite or deletion.
    out.mkdir(parents=True)
    for name, raw in {**restored, "MANIFEST.json": raw_manifest}.items():
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    return {
        "status": "passed",
        "restored_inputs": len(restored),
        "manifest_sha256": sha256(raw_manifest).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--manifest", type=Path)
    a = parser.parse_args()
    print(json.dumps(restore(a.archive, a.out_dir, manifest_path=a.manifest)))


if __name__ == "__main__":
    main()
