"""Restore a published P0/T evidence package without running a simulation."""

import argparse
import json
from hashlib import sha256
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def archive_bytes(path):
    with ZipFile(path) as z:
        names = z.namelist()
        if (
            len(names) != len(set(names))
            or sum(i.file_size for i in z.infolist()) > 128 * 1024**2
        ):
            raise ValueError("Duplicate or oversized input archive")
        for name in names:
            p = PurePosixPath(name)
            if p.is_absolute() or ".." in p.parts or "\\" in name or ":" in name:
                raise ValueError("Unsafe input archive path")
        return {name: z.read(name) for name in names}


def restore(evidence, out, *, repository=ROOT):
    evidence, out, repository = (
        Path(evidence).resolve(),
        Path(out).resolve(),
        Path(repository).resolve(),
    )
    if out.exists() or not out.is_relative_to(repository / "runs"):
        raise ValueError("Fresh restore directory inside repository runs required")
    provenance = json.loads((evidence / "PROVENANCE.json").read_bytes())
    raw_plan = (evidence / "PLAN.json").read_bytes()
    if sha256(raw_plan).hexdigest() != provenance["plan_sha256"]:
        raise ValueError("Retained plan identity failed")
    plan = json.loads(raw_plan)
    originals = archive_bytes(evidence / "ORIGINAL_SOURCES.zip")
    current = archive_bytes(evidence / "AUDITOR_SNAPSHOT.zip")
    m = json.loads(current["MANIFEST.json"])
    if set(current) != {"MANIFEST.json"} | {r["path"] for r in m["files"]}:
        raise ValueError("Unlisted auditor archive input")
    if m["plan_sha256"] != provenance["plan_sha256"]:
        raise ValueError("Auditor and registered plan disagree")
    for row in m["files"]:
        if sha256(current[row["path"]]).hexdigest() != row["sha256"]:
            raise ValueError("Auditor source identity failed")
    allowed_originals = set()
    for study in plan["studies"]:
        prefix = study["id"] + "/"
        manifest = originals[prefix + "MANIFEST.json"]
        allowed_originals.add(prefix + "MANIFEST.json")
        if sha256(manifest).hexdigest() != study["original_manifest_sha256"]:
            raise ValueError("Original source manifest identity failed")
        for row in json.loads(manifest)["files"]:
            allowed_originals.add(prefix + row["path"])
            raw = originals[prefix + row["path"]]
            if len(raw) != row["bytes"] or sha256(raw).hexdigest() != row["sha256"]:
                raise ValueError("Original source bytes changed")
    if set(originals) != allowed_originals:
        raise ValueError("Unlisted original source archive input")
    files = {"PLAN.json": raw_plan}
    files.update({"original/" + name: raw for name, raw in originals.items()})
    files.update({"current/" + name: raw for name, raw in current.items()})
    for record in plan["input_results"]:
        name = record["path"]
        source = (evidence / "retained" / Path(name).relative_to("jobs")).resolve()
        if not source.is_relative_to(evidence / "retained"):
            raise ValueError("Unsafe retained result path")
        raw = source.read_bytes()
        if sha256(raw).hexdigest() != record["sha256"]:
            raise ValueError("Retained original result identity failed")
        files[name] = raw
    # Validate every destination before writing any byte. No delete/overwrite.
    if any(not (out / name).resolve().is_relative_to(out) for name in files):
        raise ValueError("Unsafe restored destination")
    for name, raw in files.items():
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    return {
        "status": "restored_not_executed",
        "files": len(files),
        "plan_sha256": provenance["plan_sha256"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    a = parser.parse_args()
    print(json.dumps(restore(a.evidence_dir, a.out_dir)))


if __name__ == "__main__":
    main()
