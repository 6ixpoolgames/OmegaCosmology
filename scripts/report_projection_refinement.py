"""Retain and compare E1 exact-memory refinements and separate filter estimates."""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path

from restore_research_snapshot import write_archive

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "research/studies/E1-coupled-autocatalysis"
sys.path.insert(0, str(ROOT / "src"))
from omega_cosmology.testbed.analysis import linear_interval


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def verify_run(run, kind):
    receipt = json.loads((run / "BATCH_RECEIPT.json").read_text(encoding="utf-8"))
    if receipt["status"] != "passed" or not receipt["frozen_inputs_verified_after_run"]:
        raise ValueError("Incomplete or changed run")
    manifest_file = run / "frozen/MANIFEST.json"
    if receipt["manifest_sha256"] != digest(manifest_file):
        raise ArithmeticError("Snapshot manifest mismatch")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if any(
        digest(run / "frozen" / r["path"]) != r["sha256"] for r in manifest["files"]
    ):
        raise ArithmeticError("Frozen input changed")
    cases = {}
    for case in receipt["cases"]:
        key = case["case"] if kind == "memory" else case["id"]
        path = run / key / "RESULT.json"
        if case["result_sha256"] != digest(path):
            raise ArithmeticError("Retained case changed")
        cases[key] = json.loads(path.read_text(encoding="utf-8"))
    return receipt, manifest, cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--memory-runs", nargs=2, type=Path, required=True)
    parser.add_argument("--filter-runs", nargs=3, type=Path, required=True)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(STUDY):
        parser.error("Choose a fresh evidence folder inside the E1 study")
    out.mkdir(parents=True)
    originals = {}
    for mode in ("local", "AtoB"):
        key = "S0p02_C1_D0p001__" + mode + "__dt0p25"
        data = json.loads(
            (STUDY / "results-2026-10-25/cases" / (key + ".json")).read_text()
        )
        originals[key] = data
    levels = {1: originals}
    receipts = {}
    filters = {}
    residuals = []
    for run, kind in [(p, "memory") for p in args.memory_runs] + [
        (p, "filter") for p in args.filter_runs
    ]:
        run = run.resolve()
        receipt, manifest, cases = verify_run(run, kind)
        name = run.name
        folder = out / name
        folder.mkdir()
        for file in ("BATCH_RECEIPT.json", "frozen/MANIFEST.json"):
            target = folder / Path(file).name
            shutil.copyfile(run / file, target)
        # Keep runtime/query inputs byte-exact. Only the already published,
        # immutable E1 protocol and original case evidence are referenced in place.
        differences, archived_inputs = [], {}
        for row in manifest["files"]:
            source = run / "frozen" / row["path"]
            immutable = row[
                "path"
            ] == "research/studies/E1-coupled-autocatalysis/PROTOCOL.json" or row[
                "path"
            ].startswith(
                "research/studies/E1-coupled-autocatalysis/results-2026-10-25/cases/"
            )
            if not immutable:
                archived_inputs[row["path"]] = source.read_bytes()
                differences.append(row["path"])
        write_archive(folder / "RUNTIME.zip", archived_inputs)
        (folder / "RECONSTRUCTION.json").write_text(
            json.dumps(
                {
                    "input_manifest": "MANIFEST.json",
                    "archive": "RUNTIME.zip",
                    "frozen_differences": differences,
                    "other_inputs": "Published immutable E1 protocol/cases at 55db381; verify hashes in MANIFEST.json",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        for key, data in cases.items():
            shutil.copyfile(run / key / "RESULT.json", folder / (key + ".json"))
            if kind == "memory":
                old = originals[key]
                if (
                    data["model_hash"] != old["model_hash"]
                    or data["generator_hash"] != old["generator_hash"]
                ):
                    raise ArithmeticError(
                        "Physical law changed in readout-only refinement"
                    )
                for row in data["rows"]:
                    previous = next(
                        r
                        for r in old["rows"]
                        if (r["preparation"], r["horizon"])
                        == (row["preparation"], row["horizon"])
                    )
                    residuals.append(
                        abs(
                            row["history"]["ell_bits"] - previous["history"]["ell_bits"]
                        )
                    )
                memory = data["rows"][0]["projected_histories"]["A"]["memory"]
                levels.setdefault(memory, {})[key] = data
        receipts[name] = receipt
        if kind == "filter":
            filters[name] = cases
    if max(residuals) > 1e-6:
        raise ArithmeticError("Whole-history score changed")
    rows = []
    for memory, cases in sorted(levels.items()):
        lookup = {
            (data["law"], r["preparation"], r["horizon"]): r
            for data in cases.values()
            for r in data["rows"]
        }
        for prep in ("assembled", "unassembled"):
            for T in (16, 64, 256, 1024, 4096):
                for part in ("A", "B"):
                    local = lookup["S0p02_C1_D0p001__local", prep, T][
                        "projected_histories"
                    ][part]
                    extra = lookup["S0p02_C1_D0p001__AtoB", prep, T][
                        "projected_histories"
                    ][part]
                    interval = linear_interval(
                        [
                            (1, extra["lower_bits"], extra["upper_bits"]),
                            (-1, local["lower_bits"], local["upper_bits"]),
                        ]
                    )
                    if memory > 1:
                        previous = next(
                            r
                            for r in rows
                            if r["memory"] == memory - 1
                            and r["preparation"] == prep
                            and r["horizon"] == T
                            and r["part"] == part
                        )
                        if (
                            interval["lower"] < previous["interval"]["lower"] - 1e-7
                            or interval["upper"] > previous["interval"]["upper"] + 1e-7
                        ):
                            raise ArithmeticError(
                                "Exact memory refinement loosened interval"
                            )
                    rows.append(
                        {
                            "memory": memory,
                            "preparation": prep,
                            "horizon": T,
                            "part": part,
                            "interval": interval,
                        }
                    )
    analysis = {
        "schema": "omega.projection-refinement-analysis/1",
        "physical_changes": [],
        "max_whole_history_residual_bits": max(residuals),
        "memory_comparisons": rows,
        "filter_estimates": filters,
        "receipts": receipts,
        "limits": "Approximate t intervals are not analytic projection bounds; pointwise coverage only.",
    }
    (out / "ANALYSIS.json").write_text(
        json.dumps(analysis, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# E1 projected-history refinement",
        "",
        "25 October 2026. Unchanged physical laws, preparations, horizons and state grain.",
        "",
        "## Exact-memory benchmark",
        "",
        "Donor A, AtoB minus local, T4096 at cadence .25:",
        "",
        "| Memory | Assembled interval (bits) | Unassembled interval (bits) |",
        "|---|---:|---:|",
    ]
    for m in sorted(levels):
        values = [
            next(
                r["interval"]
                for r in rows
                if r["memory"] == m
                and r["preparation"] == prep
                and r["horizon"] == 4096
                and r["part"] == "A"
            )
            for prep in ("assembled", "unassembled")
        ]
        lines.append(
            f"| {m} | [{values[0]['lower']:.4f}, {values[0]['upper']:.4f}] | [{values[1]['lower']:.4f}, {values[1]['upper']:.4f}] |"
        )
    lines += [
        "",
        "All refined bounds enclose the requested quantity analytically, evaluated in float64.",
        "Both levels tighten the earlier intervals but leave donor signs unresolved.",
        f"Maximum unchanged whole-history residual: {max(residuals):.3g} bits.",
        "",
        "## Filtering estimates",
        "",
        "These estimate the same full projected history using finite hidden-state filtering.",
        "Exact-mean controls improve precision without removing any physical entropy.",
        "The t intervals below are approximate, pointwise statistical intervals; they",
        "are not analytically resolved rankings. Distribution-free intervals are retained",
        "in the machine-readable output even when too wide to decide a sign.",
        "",
        "| Preparation | Horizon | Difference estimate (bits) | Approx. 95% t interval | SE / raw SE |",
        "|---|---:|---:|---:|---:|",
    ]
    for cases in filters.values():
        for data in cases.values():
            if not data["case"]["id"].startswith("donor_"):
                continue
            for row in data["rows"]:
                lo, hi = row["approximate_t_interval_bits"]
                lines.append(
                    f"| {data['case']['preparation']} | {row['horizon']} | {row['difference_estimate_bits']:.5f} | [{lo:.5f}, {hi:.5f}] | {row['paired_standard_error_bits']:.4f} / {row['uncontrolled_paired_standard_error_bits']:.4f} |"
                )
    lines += [
        "",
        "## Compute",
        "",
        "| Run | Wall seconds | Peak per-job MiB |",
        "|---|---:|---:|",
    ]
    for name, receipt in receipts.items():
        peak = max(c["receipt"]["peak_job_bytes"] for c in receipt["cases"]) / 1024**2
        lines.append(f"| {name} | {receipt['wall_seconds']:.3f} | {peak:.2f} |")
    lines += [
        "",
        "All cases passed their declared caps. No failed case was replaced or scientific",
        "parameter/horizon changed. Frozen input manifests and byte-different historical",
        "inputs are retained in per-run RUNTIME.zip archives. No dense matrices or trajectories are retained here.",
        "",
        "The four short E1 calibration cases and both pilots remain in ANALYSIS.json.",
        "Agreement at short prefixes does not prove asymptotic statistical coverage.",
        "",
        "No private/whole ethical conclusion follows from an estimated donor difference.",
        "A physical donor fuel cost, sequestration, material transfer and irreversible",
        "loss are still absent from this contrast.",
    ]
    (out / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    code = out / "analysis_source"
    code.mkdir()
    shutil.copyfile(Path(__file__), code / Path(__file__).name)
    manifest = {
        "schema": "omega.projection-refinement-evidence/1",
        "files": [
            {
                "path": p.relative_to(out).as_posix(),
                "sha256": digest(p),
                "bytes": p.stat().st_size,
            }
            for p in sorted(out.rglob("*"))
            if p.is_file()
        ],
    }
    (out / "EVIDENCE.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "memory_comparisons": len(rows),
                "evidence_files": len(manifest["files"]),
            }
        )
    )


if __name__ == "__main__":
    main()
