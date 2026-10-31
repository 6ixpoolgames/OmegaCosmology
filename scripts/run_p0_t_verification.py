"""Freeze and execute only the user-authorized representative P0/T package."""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path
from time import perf_counter
from zipfile import ZipFile

from restore_research_snapshot import write_archive

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def write(p, value):
    Path(p).write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def digest(p):
    return sha256(Path(p).read_bytes()).hexdigest()


def selected_studies():
    # Explicit, reviewable choices from the already-published claims. Never
    # select an alternative after comparing fresh scores.
    return [
        {
            "id": "R1",
            "directory": "R1-constructed-access",
            "date": "2026-10-24",
            "protocol_name": "PROTOCOL.json",
            "preparation": "built",
            "laws": ["driven__intact", "driven__ablated"],
            "coefficients": [1, -1],
            "recovery": "r1-constructed-access-20261024-r1",
        },
        {
            "id": "R2",
            "directory": "R2-further-capacity",
            "date": "2026-10-24",
            "protocol_name": "PROTOCOL.json",
            "preparation": "assembly_seed",
            "laws": ["driven__assisted", "driven__sham"],
            "coefficients": [1, -1],
            "recovery": "r2-further-capacity-20261024-r2",
        },
        {
            "id": "E1",
            "directory": "E1-coupled-autocatalysis",
            "date": "2026-10-25",
            "protocol_name": "PROTOCOL.json",
            "preparation": "unassembled",
            "laws": ["S0p12_C1_D0p012__AtoB", "S0p12_C1_D0p012__local"],
            "coefficients": [1, -1],
            "recovery": "e1-coupled-map-20261025-r1",
        },
        {
            "id": "S3",
            "directory": "S3-repair-and-interaction",
            "date": "2026-10-26",
            "protocol_name": "PROTOCOL_INTERACTION.json",
            "preparation": "seed",
            "laws": ["one_way", "local"],
            "coefficients": [1, -1],
            "subfolder": "interaction",
        },
        {
            "id": "S4",
            "directory": "S4-warning-and-obstruction",
            "date": "2026-10-26",
            "protocol_name": "PROTOCOL_OPEN.json",
            "preparation": "present",
            "laws": ["open_TX", "open_T0"],
            "coefficients": [1, -1],
            "subfolder": "open",
        },
        {
            "id": "S4b",
            "directory": "S4b-paid-warning",
            "date": "2026-10-26",
            "protocol_name": "PROTOCOL_OPEN.json",
            "preparation": "present",
            "laws": ["open_TX", "open_T0", "open_RX", "open_R0"],
            "coefficients": [1, -1, -1, 1],
            "pair_indices": [[0, 1], [2, 3]],
            "subfolder": "open",
        },
    ]


def original_inputs(study):
    base = ROOT / "research/studies" / study["directory"]
    results = base / ("results-" + study["date"])
    if "subfolder" in study:
        archive = results / study["subfolder"] / "SNAPSHOT.zip"
        with ZipFile(archive) as z:
            manifest_raw = z.read("MANIFEST.json")
            manifest = json.loads(manifest_raw)
            names = z.namelist()
            if len(names) != len(set(names)):
                raise ValueError("Duplicate archive member")
            raw = {r["path"]: z.read(r["path"]) for r in manifest["files"]}
    else:
        manifest_raw = (results / "SOURCE_MANIFEST.json").read_bytes()
        manifest = json.loads(manifest_raw)
        raw = {}
        for r in manifest["files"]:
            choices = [
                ROOT / "runs" / study["recovery"] / "frozen" / r["path"],
                ROOT / r["path"],
            ]
            source = next(
                (p for p in choices if p.is_file() and digest(p) == r["sha256"]), None
            )
            if source is None:
                raise ValueError("Original source unrecoverable: " + r["path"])
            raw[r["path"]] = source.read_bytes()
    for r in manifest["files"]:
        target = (ROOT / r["path"]).resolve()
        if (
            not target.is_relative_to(ROOT)
            or len(raw[r["path"]]) != r["bytes"]
            or sha256(raw[r["path"]]).hexdigest() != r["sha256"]
        ):
            raise ValueError("Original source manifest failed")
    protocol_path = f"research/studies/{study['directory']}/{study['protocol_name']}"
    if sha256(raw[protocol_path]).hexdigest() != manifest["protocol_sha256"]:
        raise ValueError("Protocol/source manifest disagreement")
    raw["MANIFEST.json"] = manifest_raw
    return results, raw, protocol_path


def prepare(out):
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        raise ValueError("Fresh output inside runs required")
    # Resolve and verify all original inputs before creating the run.
    prepared = [(s, original_inputs(s)) for s in selected_studies()]
    out.mkdir(parents=True)
    plan = {
        "schema": "omega.p0-t-verification/1",
        "date": "2026-10-30",
        "authorization": "user Proceed; P0/T only",
        "max_profile_steps": 65536,
        "job_wall_seconds": 240,
        "job_memory_bytes": 2 * 1024**3,
        "job_output_bytes": 32 * 1024**2,
        "batch_wall_seconds": 2400,
        "batch_output_bytes": 256 * 1024**2,
        "studies": [],
        "input_results": [],
    }
    (out / "jobs").mkdir()
    for study, (results, raw, protocol_path) in prepared:
        original = out / "original" / study["id"]
        for name, data in raw.items():
            dest = (original / name).resolve()
            if not dest.is_relative_to(original):
                raise ValueError("Unsafe source archive member")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        protocol = json.loads(raw[protocol_path])
        public_study = {k: v for k, v in study.items() if k != "recovery"}
        cadence_cases = protocol.get("case_grid")
        cadences = [
            dt
            for dt in protocol["cadences"]
            if cadence_cases is None
            or all([law, dt] in cadence_cases for law in study["laws"])
        ]
        if not cadences:
            raise ValueError("No shared original cadence for selected contrast")
        public_study.update(
            {
                "protocol": protocol_path,
                "cadences": cadences,
                "horizons": protocol["horizons"],
                "original_manifest_sha256": sha256(raw["MANIFEST.json"]).hexdigest(),
            }
        )
        for dt in cadences:
            for name in study["laws"]:
                suffix = name + "__dt" + str(dt).replace(".", "p")
                original_result = (
                    results / study["subfolder"] / suffix / "RESULT.json"
                    if "subfolder" in study
                    else results / "cases" / (suffix + ".json")
                )
                # Verify the retained evidence byte record, not only its existence.
                evidence = read(results / "EVIDENCE.json")
                record = next(
                    r
                    for r in evidence["files"]
                    if r["path"] == original_result.relative_to(results).as_posix()
                )
                if digest(original_result) != record["sha256"]:
                    raise ValueError("Retained result byte manifest failed")
                job = out / "jobs" / (study["id"] + "__" + name + "__" + str(dt))
                job.mkdir()
                shutil.copyfile(original_result, job / "ORIGINAL_RESULT.json")
                plan["input_results"].append(
                    {
                        "path": (job / "ORIGINAL_RESULT.json")
                        .relative_to(out)
                        .as_posix(),
                        "sha256": digest(original_result),
                    }
                )
        plan["studies"].append(public_study)
    write(out / "PLAN.json", plan)
    current = out / "current"
    files = list((ROOT / "src/omega_cosmology/testbed").glob("*.py"))
    files += [
        ROOT / "src/omega_cosmology/__init__.py",
        ROOT / "scripts/p0_t_worker.py",
        Path(__file__).resolve(),
        ROOT / "research/platform/specs/P0_T_VERIFICATION_r1.md",
        ROOT / "tests/test_profile_analysis.py",
    ]
    manifest = {
        "schema": "omega.p0-t-auditor-snapshot/1",
        "plan_sha256": digest(out / "PLAN.json"),
        "files": [],
    }
    for path in files:
        relative = path.relative_to(ROOT)
        target = current / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        manifest["files"].append(
            {
                "path": relative.as_posix(),
                "sha256": digest(path),
                "bytes": path.stat().st_size,
            }
        )
    write(current / "MANIFEST.json", manifest)
    print(
        json.dumps(
            {
                "status": "prepared",
                "native_cases": len(plan["input_results"]),
                "studies": len(plan["studies"]),
                "plan_sha256": manifest["plan_sha256"],
            }
        )
    )


def execute(out):
    from omega_cosmology.testbed.workflow import (
        capped,
        memory_reserve_preflight,
        tree_bytes,
    )

    plan = read(out / "PLAN.json")
    manifest = read(out / "current/MANIFEST.json")
    if digest(out / "PLAN.json") != manifest["plan_sha256"]:
        raise ValueError("Execution plan changed after freeze")
    if (out / "BATCH_RECEIPT.json").exists():
        raise ValueError("Batch already executed; do not overwrite")
    memory_reserve_preflight(plan["job_memory_bytes"])
    started, receipts, status = perf_counter(), [], "passed"
    worker = out / "current/scripts/p0_t_worker.py"

    def dispatch(mode, folder, study=None, dt=None, law=None):
        if (folder / "RECEIPT.json").exists():
            raise ValueError("Job output already exists")
        folder.mkdir(parents=True, exist_ok=True)
        remaining = plan["batch_wall_seconds"] - (perf_counter() - started)
        if remaining <= 0:
            raise TimeoutError("Batch deadline reached")
        command = [
            sys.executable,
            str(worker),
            mode,
            "--run",
            str(out),
            "--out",
            str(folder),
        ]
        if study:
            command += ["--study", study, "--cadence", str(dt)]
        if law:
            command += ["--law", law]
        receipt = capped(
            command,
            folder,
            seconds=min(
                remaining, 60 if mode == "references" else plan["job_wall_seconds"]
            ),
            memory=512 * 1024**2 if mode == "references" else plan["job_memory_bytes"],
            output_cap=8 * 1024**2
            if mode == "references"
            else plan["job_output_bytes"],
            cwd=out / "current",
        )
        write(folder / "RECEIPT.json", receipt)
        receipts.append(
            {
                "mode": mode,
                "study": study,
                "law": law,
                "cadence": dt,
                "folder": folder.relative_to(out).as_posix(),
                "receipt": receipt,
            }
        )
        ok = receipt["exit_code"] == 0 and receipt["cap_reason"] is None
        print(
            json.dumps(
                {
                    "mode": mode,
                    "study": study,
                    "law": law,
                    "cadence": dt,
                    "passed": ok,
                    "seconds": round(receipt["wall_seconds"], 3),
                }
            ),
            flush=True,
        )
        if tree_bytes(out / "jobs") > plan["batch_output_bytes"]:
            raise RuntimeError("Batch output cap reached")
        return ok

    try:
        if not dispatch("references", out / "jobs/T"):
            raise RuntimeError("T reference verification failed; preserve diagnostic")
        for s in plan["studies"]:
            complete = True
            for dt in s["cadences"]:
                for law in s["laws"]:
                    folder = out / "jobs" / (s["id"] + "__" + law + "__" + str(dt))
                    if not dispatch("native", folder, s["id"], dt, law):
                        complete = False
                        break
                if not complete:
                    break
                if not dispatch(
                    "audit",
                    out / "jobs" / (s["id"] + "__audit__" + str(dt)),
                    s["id"],
                    dt,
                ):
                    complete = False
                    break
            if not complete:
                status = "incomplete"
                # Different studies are independent scopes. Do not replace the
                # failed point, but continue the unaffected fixed studies.
    except (RuntimeError, TimeoutError) as exc:
        status = "incomplete"
        write(out / "ERROR.json", {"reason": str(exc)})
    write(
        out / "BATCH_RECEIPT.json",
        {
            "status": status,
            "plan_sha256": digest(out / "PLAN.json"),
            "current_manifest_sha256": digest(out / "current/MANIFEST.json"),
            "wall_seconds": perf_counter() - started,
            "jobs": receipts,
        },
    )
    return status


def retain(out, destination):
    """Keep complete source/inputs/results/receipts; logs never expose paths."""
    if destination.exists() or not destination.is_relative_to(
        ROOT / "research/platform/engineering"
    ):
        raise ValueError("Fresh engineering evidence directory required")
    destination.mkdir(parents=True)
    shutil.copyfile(out / "PLAN.json", destination / "PLAN.json")
    shutil.copyfile(out / "BATCH_RECEIPT.json", destination / "BATCH_RECEIPT.json")
    originals = {}
    for p in (out / "original").rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts:
            originals[p.relative_to(out / "original").as_posix()] = p.read_bytes()
    write_archive(destination / "ORIGINAL_SOURCES.zip", originals)
    current = {
        r["path"]: (out / "current" / r["path"]).read_bytes()
        for r in read(out / "current/MANIFEST.json")["files"]
    }
    current["MANIFEST.json"] = (out / "current/MANIFEST.json").read_bytes()
    write_archive(destination / "AUDITOR_SNAPSHOT.zip", current)
    for p in (out / "jobs").rglob("*"):
        if p.is_file():
            relative = p.relative_to(out / "jobs")
            target = destination / "retained" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if p.suffix == ".log":
                text = (
                    p.read_text(encoding="utf-8")
                    .replace(str(ROOT), "<repo>")
                    .replace(ROOT.as_posix(), "<repo>")
                )
                target.write_text(text, encoding="utf-8")
            else:
                shutil.copyfile(p, target)
    write(
        destination / "PROVENANCE.json",
        {
            "status": read(out / "BATCH_RECEIPT.json")["status"],
            "plan_sha256": digest(out / "PLAN.json"),
            "literal_native_sources_verified": True,
            "latest_appendix_AB_conformance": "not_checked_unavailable_in_supplied_batch",
            "physical_faithfulness": "open",
            "publication": "not_authorized",
        },
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("prepare", "execute", "retain"))
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--evidence-dir", type=Path)
    a = p.parse_args()
    out = a.out_dir.resolve()
    if not out.is_relative_to(ROOT / "runs"):
        p.error("Execution output must remain inside runs")
    if a.mode == "prepare":
        prepare(out)
    elif a.mode == "execute":
        return execute(out) != "passed"
    else:
        retain(out, a.evidence_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
