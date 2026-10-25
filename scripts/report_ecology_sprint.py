"""Retain compact capped S2/S1 evidence and byte-exact runtime snapshots."""

import argparse
import json
import shutil
from hashlib import sha256
from pathlib import Path

from restore_research_snapshot import write_archive

ROOT = Path(__file__).resolve().parents[1]


def read(p):
    return json.loads(p.read_text(encoding="utf-8"))


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def write(p, v):
    p.write_text(json.dumps(v, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke-run", type=Path, required=True)
    parser.add_argument("--confidence-run", type=Path, action="append", required=True)
    parser.add_argument("--failed-smoke-run", type=Path, action="append", default=[])
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "research/platform/engineering"):
        parser.error("Choose fresh engineering evidence directory")
    out.mkdir(parents=True)
    analysis = {
        "schema": "omega.ecology-sprint-analysis/1",
        "runs": {},
        "confidence_rows": [],
        "redacted_logs": [],
        "reconstruction": [],
    }
    all_runs = (
        [(args.smoke_run, "smoke", True)]
        + [(p, "confidence", True) for p in args.confidence_run]
        + [(p, "failed_setup", False) for p in args.failed_smoke_run]
    )
    for run, kind, must_pass in all_runs:
        run = run.resolve()
        if not run.is_relative_to(ROOT / "runs"):
            raise ValueError("Expected a retained local run")
        receipt = read(run / "BATCH_RECEIPT.json")
        if must_pass and receipt["status"] != "passed":
            raise ValueError("Unsuccessful capped run")
        target = out / run.name
        target.mkdir()
        shutil.copyfile(run / "BATCH_RECEIPT.json", target / "BATCH_RECEIPT.json")
        snapshot = run / "frozen"
        manifest_path = snapshot / "MANIFEST.json"
        manifest = read(manifest_path)
        if receipt.get(
            "source_manifest_sha256", receipt.get("manifest_sha256")
        ) != digest(manifest_path):
            raise ValueError("Receipt/source mismatch")
        for row in manifest["files"]:
            path = (snapshot / row["path"]).resolve()
            if not path.is_relative_to(snapshot) or digest(path) != row["sha256"]:
                raise ValueError("Frozen runtime input changed")
        frozen_out = target / "SNAPSHOT.zip"
        write_archive(
            frozen_out,
            {r["path"]: (snapshot / r["path"]).read_bytes() for r in manifest["files"]}
            | {"MANIFEST.json": manifest_path.read_bytes()},
        )
        analysis["reconstruction"].append(
            {
                "run": run.name,
                "snapshot_archive": frozen_out.relative_to(out).as_posix(),
                "command": "Restore with scripts/restore_research_snapshot.py, then run its supervisor with the retained plan",
                "note": "Snapshot is a full original path hierarchy; code must execute from that root, not the current package",
            }
        )
        for item in receipt["cases"]:
            folder = target / item["id"]
            folder.mkdir()
            result_path = run / item["id"] / "RESULT.json"
            if result_path.exists():
                if digest(result_path) != item["result_sha256"]:
                    raise ValueError("Result differs from receipt")
                shutil.copyfile(result_path, folder / "RESULT.json")
                result = read(result_path)
                if kind == "smoke":
                    plan = read(snapshot / manifest["plan"])
                    spec = next(c for c in plan["cases"] if c["id"] == item["id"])
                    if (
                        result["states"]
                        != spec["protocol"]["legal_state_count_reference"]
                    ):
                        raise ValueError(
                            "Reachable and combinatorial state count differ"
                        )
                if kind == "confidence":
                    plan = next(
                        read(snapshot / r["path"])
                        for r in manifest["files"]
                        if r["path"].endswith(".json")
                        and "/projected-confidence/PLAN_" in r["path"]
                    )
                    for row in result["rows"]:
                        lo, hi = row["empirical_bernstein_family_interval_bits"]
                        analysis["confidence_rows"].append(
                            {
                                "cadence": plan["cadence"],
                                **row,
                                "finite_sample_resolved_sign": 1
                                if lo > 0
                                else -1
                                if hi < 0
                                else None,
                                "rigorous_numerical_certificate": False,
                            }
                        )
            log = run / item["id"] / "worker.log"
            if log.exists():
                text = log.read_text(encoding="utf-8")
                text = text.replace(str(ROOT), "<repo>").replace(
                    ROOT.as_posix(), "<repo>"
                )
                (folder / "worker.log").write_text(text, encoding="utf-8")
                analysis["redacted_logs"].append(
                    {
                        "path": (folder / "worker.log").relative_to(out).as_posix(),
                        "original_sha256": digest(log),
                        "redaction": "local checkout prefix",
                    }
                )
        analysis["runs"][run.name] = {"kind": kind, **receipt}
    write(out / "ANALYSIS.json", analysis)
    lines = [
        "# Ecology sprint: capped engineering and precision feasibility",
        "",
        "25 October 2026. Source-frozen inputs and unchanged raw results accompany this report.",
        "",
        "## Occupied assistance smoke",
        "",
        "| Case | States | Wall s | Peak MiB |",
        "|---|---:|---:|---:|",
    ]
    smoke = analysis["runs"][args.smoke_run.name]
    for item in smoke["cases"]:
        result = read(out / args.smoke_run.name / item["id"] / "RESULT.json")
        lines.append(
            f"| {item['id']} | {result['states']} | {item['receipt']['wall_seconds']:.3f} | {item['receipt']['peak_job_bytes'] / 1024**2:.2f} |"
        )
    lines += [
        "",
        "Six cases passed. Two profiles per case, T4/16, cadence.25.",
        "Port competition, release, bound failure and thermodynamics were engineering checks, not ranking targets.",
        "Ancestry is queried on the two small cases; larger cases explicitly omit the ancestry product.",
        "Local histories use member/bank projections and finite-memory bounds. Contacts remain in whole history.",
        "",
        "## Projected donor confidence",
        "",
        "Candidate-minus-reference is AtoB-minus-local from the unassembled E1 root.",
        "Family intervals cover six requested comparisons under ideal iid/exact-arithmetic assumptions.",
        "Float64 kernel/filter error is not rigorously enclosed. Approximate t intervals are separate.",
        "",
        "| Cadence | T | Estimate bits | Finite-sample family interval | Approx. pointwise t interval |",
        "|---:|---:|---:|---|---|",
    ]
    for row in analysis["confidence_rows"]:
        lo, hi = row["empirical_bernstein_family_interval_bits"]
        a, b = row["approximate_t_interval_bits"]
        lines.append(
            f"| {row['cadence']} | {row['horizon']} | {row['difference_estimate_bits']:.6f} | [{lo:.6f},{hi:.6f}] | [{a:.6f},{b:.6f}] |"
        )
    lines += [
        "",
        "No certified donor sign is claimed. Report unresolved signs rather than increasing sampling until a desired sign appears.",
        "A second cadence is an audit; it does not establish a finest faithful temporal grain.",
        "",
        "## Setup corrections and reconstruction",
        "",
        "Failed smoke setup1 assigned component-root values to similarly named contact coordinates; no profile was computed.",
        "Setup2 reached the fixed dense-kernel workspace gate. No physics was reduced: the plan now declares128MiB kernel workspace.",
        "The dense occupation reference has a separate512MiB gate. Old default kernel caps remain32MiB.",
        "Both failed attempts, their logs and byte-exact source snapshots are retained.",
        "",
        "Full runtime snapshots live in each run's SNAPSHOT.zip. No dense arrays or sampled paths are retained.",
        "Each snapshot contains its plan, scripts and MANIFEST.json. Run from that snapshot root with a fresh output directory.",
        "An assembly's occupancy is represented physically; query ancestry labels add no entropy.",
        "No S3 interaction campaign, policy optimization, domination test or ethical verdict was run.",
    ]
    (out / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    shutil.copyfile(__file__, out / "report_ecology_sprint.py")
    write(
        out / "EVIDENCE.json",
        {
            "schema": "omega.ecology-sprint-evidence/1",
            "files": [
                {
                    "path": p.relative_to(out).as_posix(),
                    "sha256": digest(p),
                    "bytes": p.stat().st_size,
                }
                for p in sorted(out.rglob("*"))
                if p.is_file()
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "confidence_comparisons": len(analysis["confidence_rows"]),
            }
        )
    )


if __name__ == "__main__":
    main()
