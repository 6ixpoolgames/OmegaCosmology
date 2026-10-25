"""Shared evidence packaging and signed comparison report for configured studies."""

import argparse
import json
import shutil
import sys
from collections import Counter
from hashlib import sha256
from pathlib import Path

from restore_research_snapshot import write_archive

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from omega_cosmology.testbed.analysis import (
    comparison_profiles,
    linear_interval,
    numerical_sign,
)


def read(p):
    return json.loads(p.read_text(encoding="utf-8"))


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def write(p, v):
    p.write_text(json.dumps(v, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def retain_run(run, folder, *, complete=True):
    run = run.resolve()
    folder.mkdir(parents=True)
    receipt = read(run / "BATCH_RECEIPT.json")
    manifest_path = run / "frozen/MANIFEST.json"
    manifest = read(manifest_path)
    if complete and receipt["status"] != "passed":
        raise ValueError("Complete passing batch required")
    if receipt.get("manifest_sha256", receipt.get("source_manifest_sha256")) != digest(
        manifest_path
    ):
        raise ValueError("Manifest/receipt mismatch")
    archived = {}
    for r in manifest["files"]:
        source = (run / "frozen" / r["path"]).resolve()
        if not source.is_relative_to(run / "frozen") or digest(source) != r["sha256"]:
            raise ValueError("Frozen input changed")
        archived[r["path"]] = source.read_bytes()
    write_archive(
        folder / "SNAPSHOT.zip",
        archived | {"MANIFEST.json": manifest_path.read_bytes()},
    )
    shutil.copyfile(run / "BATCH_RECEIPT.json", folder / "BATCH_RECEIPT.json")
    records = []
    for c in receipt["cases"]:
        name = c.get("case", c.get("id"))
        target = folder / name
        target.mkdir()
        source = run / name / "RESULT.json"
        if source.exists():
            if digest(source) != c["result_sha256"]:
                raise ValueError("Case receipt mismatch")
            shutil.copyfile(source, target / "RESULT.json")
            records.append(read(source))
        log = run / name / "worker.log"
        if log.exists():
            text = (
                log.read_text(encoding="utf-8")
                .replace(str(ROOT), "<repo>")
                .replace(ROOT.as_posix(), "<repo>")
            )
            (target / "worker.log").write_text(text, encoding="utf-8")
    return receipt, records, manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--run", action="append", required=True, help="study-key=run-directory"
    )
    p.add_argument("--extra-run", action="append", default=[])
    p.add_argument("--analysis-plan", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    a = p.parse_args()
    out = a.out_dir.resolve()
    plan = read(a.analysis_plan)
    if out.exists() or not out.is_relative_to(ROOT / "research/studies"):
        p.error("Fresh output under research/studies required")
    out.mkdir(parents=True)
    shutil.copyfile(a.analysis_plan, out / "ANALYSIS_PLAN.json")
    summary = {}
    comparisons = []
    cases = []
    all_foreclosure = []
    row_count = 0
    for item in a.run:
        key, name = item.split("=", 1)
        run = Path(name)
        receipt, records, manifest = retain_run(run, out / key)
        protocol = read(run / "frozen" / manifest["protocol"])
        shutil.copyfile(
            run / "frozen" / manifest["protocol"],
            out / (key.upper() + "_PROTOCOL.json"),
        )
        lookup = {
            (r["law"], r["preparation"], r["cadence"], r["horizon"]): r
            for d in records
            for r in d["rows"]
        }
        if len(lookup) != sum(len(d["rows"]) for d in records):
            raise ValueError("Duplicate profile keys")
        row_count += len(lookup)
        for c in plan["comparisons"][key]:
            first, second = tuple(c["first"]), tuple(c["second"])
            for dt in protocol["cadences"]:
                for T in protocol["horizons"]:
                    aa = lookup.get((*first, dt, T))
                    bb = lookup.get((*second, dt, T))
                    if aa is None or bb is None:
                        continue
                    delta = aa["history"]["ell_bits"] - bb["history"]["ell_bits"]
                    parts = {}
                    for part, quantity in plan["projected_scopes"][key].items():
                        x, y = [r["projected_histories"][quantity] for r in (aa, bb)]
                        interval = linear_interval(
                            [
                                (1, x["lower_bits"], x["upper_bits"]),
                                (-1, y["lower_bits"], y["upper_bits"]),
                            ]
                        )
                        interval["resolved_sign"] = (
                            1
                            if interval["lower"] > plan["tolerance_bits"]
                            else -1
                            if interval["upper"] < -plan["tolerance_bits"]
                            else None
                        )
                        parts[part] = interval
                    functions = {
                        org: {
                            f: aa["functional_profiles"][org][f]
                            - bb["functional_profiles"][org][f]
                            for f in [
                                "endpoint_functional_probability",
                                "integrated_functional_time",
                                "ever_functional_probability",
                                "expected_entries",
                                "expected_exits",
                                "uninterrupted_initial_function_probability",
                                "initial_function_lost_then_returned_probability",
                                "structural_closure_by_deadline_probability",
                            ]
                        }
                        for org in aa["functional_profiles"]
                    }
                    comparisons.append(
                        {
                            "study": key,
                            **c,
                            "cadence": dt,
                            "horizon": T,
                            "delta_ell_bits": delta,
                            "sign": numerical_sign(delta, plan["tolerance_bits"]),
                            "delta_projected_histories": parts,
                            "delta_functional_profiles": functions,
                            "delta_observables": {
                                k: {
                                    f: aa["observables"][k][f] - bb["observables"][k][f]
                                    for f in ["endpoint", "integrated", "stationary"]
                                }
                                for k in aa["observables"]
                            },
                            "delta_work_accepted": aa["physical"]["work_accepted_gross"]
                            - bb["physical"]["work_accepted_gross"],
                            "delta_event_readouts": {
                                k: aa["event_readouts"][k] - bb["event_readouts"][k]
                                for k in aa["event_readouts"]
                            },
                            "delta_coordinate_shares_bits": {
                                k: aa["coordinate_shares_bits"][k]
                                - bb["coordinate_shares_bits"][k]
                                for k in aa["coordinate_shares_bits"]
                            },
                            "delta_work_net": aa["physical"]["work_net"]
                            - bb["physical"]["work_net"],
                            "delta_expected_jumps": aa["activity"]["expected_jumps"]
                            - bb["activity"]["expected_jumps"],
                            "delta_finite_coefficient_bits": aa["activity"][
                                "finite_coefficient_bits"
                            ]
                            - bb["activity"]["finite_coefficient_bits"],
                            "delta_rate_bits_per_time": aa["asymptotic"][
                                "rate_bits_per_time"
                            ]
                            - bb["asymptotic"]["rate_bits_per_time"],
                            "delta_offset_bits": aa["asymptotic"]["offset_bits"]
                            - bb["asymptotic"]["offset_bits"],
                        }
                    )
        for d in records:
            all_foreclosure.extend(
                {"study": key, **r} for r in d.get("foreclosure_comparisons", [])
            )
            cases.append(
                {
                    "study": key,
                    "law": d["law"],
                    "cadence": d["cadence"],
                    "states": d["states"],
                    "full_positive_sampled_support": d["full_positive_sampled_support"],
                    "kernel_residual": d["kernel_residual"],
                    "equilibrium_audit": d["equilibrium_audit"],
                }
            )
        summary[key] = {
            "profiles": len(lookup),
            "cases": len(records),
            "wall_seconds": receipt["wall_seconds"],
            "max_job_mib": max(c["receipt"]["peak_job_bytes"] for c in receipt["cases"])
            / 1024**2,
            "output_bytes": receipt["output_bytes"],
            "primary_cadence": protocol["primary_cadence"],
            "max_energy_residual": max(
                abs(r["physical"]["energy_residual"]) for r in lookup.values()
            ),
            "max_rate_offset_residual_bits": max(
                abs(r["horizon_diagnostics"]["rate_offset_profile_residual_bits"])
                for r in lookup.values()
            ),
        }
    for name in a.extra_run:
        retain_run(Path(name), out / "engineering" / Path(name).name, complete=False)
    write(
        out / "ANALYSIS.json",
        {
            "schema": "omega.signed-studies-analysis/1",
            "summary": summary,
            "profile_rows": row_count,
            "comparisons": comparisons,
            "profiles": comparison_profiles(comparisons, plan["tolerance_bits"]),
            "case_checks": cases,
            "foreclosure_comparisons": all_foreclosure,
        },
    )
    lines = [
        "# " + plan.get("title", "S3 repair and occupied-interaction results"),
        "",
        "All signed comparisons are retained; no outcome was an acceptance criterion.",
        "",
        "| Study | Cases | Profiles | Wall s | Peak MiB |",
        "|---|---:|---:|---:|---:|",
    ]
    for key, s in summary.items():
        lines.append(
            f"| {key} | {s['cases']} | {s['profiles']} | {s['wall_seconds']:.3f} | {s['max_job_mib']:.2f} |"
        )
    lines += [
        "",
        "## Last registered horizon at the primary cadence",
        "",
        "| Study/contrast | T | Whole delta bits | Projected intervals |",
        "|---|---:|---:|---|",
    ]
    last = {
        key: max(r["horizon"] for r in comparisons if r["study"] == key)
        for key in summary
    }
    for r in comparisons:
        if (
            r["cadence"] == summary[r["study"]]["primary_cadence"]
            and r["horizon"] == last[r["study"]]
        ):
            parts = "; ".join(
                f"{k}[{v['lower']:.4f},{v['upper']:.4f}]"
                for k, v in r["delta_projected_histories"].items()
            )
            lines.append(
                f"| {r['study']}/{r['id']} | {r['horizon']} | {r['delta_ell_bits']:.6f} | {parts} |"
            )
    counts = Counter(r["structurally_certified_zero"] for r in all_foreclosure)
    lines += [
        "",
        "## Guarantees and scope",
        "",
        f"Integrated foreclosure rows: {len(all_foreclosure)}; structural-zero counts: {dict(counts)}.",
        "Structural zeros follow from native Boolean support; nonzero reference weights would be float64 numerical values.",
        "Constituent recovery, graph closure and history entropy are separate outputs. No tiny reverse route was removed.",
        *plan.get(
            "physical_scope_notes",
            [
                "The intact repair root has0.5 more formation energy; only repair-fault versus access-fault is the equal-energy fault contrast.",
                "All interaction arms retain the same six contacts; only paired conversions or declared physical conductances change.",
            ],
        ),
        "Analytic local inequalities are evaluated in float64; unresolved intervals are not ties or midpoint verdicts.",
        "Bath/source histories are unresolved. Work and activity differ, so these are not matched-throughput/activity attribution tests.",
        *plan.get(
            "comparison_scope_notes",
            [
                "Same-law preparation rates agree; offsets can remain. Rate does not replace a finite-horizon comparison.",
                "No permanent destruction, interacting valuers, optimizer, gas, population expansion or ethical correspondence is claimed.",
            ],
        ),
        "",
        "## Reconstruction",
        "",
        "Each study/run folder contains raw case results, capped receipts and a byte-exact SNAPSHOT.zip.",
        "Restore with scripts/restore_research_snapshot.py into a fresh ignored directory and execute the retained supervisor/plan there.",
        plan.get(
            "engineering_note",
            "Engineering repetitions and the incomplete ancestry-query configuration attempt are retained separately; no physical parameter changed in that repair.",
        ),
        "No dense matrices or sampled paths are retained. All physical randomness remains in the total.",
    ]
    (out / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    shutil.copyfile(__file__, out / "report_signed_studies.py")
    write(
        out / "EVIDENCE.json",
        {
            "schema": "omega.signed-studies-evidence/1",
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
                "profiles": row_count,
                "comparisons": len(comparisons),
                "summary": summary,
            }
        )
    )


if __name__ == "__main__":
    main()
