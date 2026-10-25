"""Verify E1 evidence and map physical, local and whole-field relationships."""

import argparse
import json
import shutil
import sys
from collections import Counter
from hashlib import sha256
from math import fsum
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from omega_cosmology.testbed.analysis import (
    comparison_profiles,
    linear_interval,
    numerical_sign,
)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def build_analysis(protocol, rows):
    eps = protocol["numerical"]["sign_deadband_bits"]
    lookup = {(l["regime"]["id"], l["mechanism"]): l["id"] for l in protocol["laws"]}
    available = {}
    for law, dt in protocol["case_grid"]:
        available.setdefault(law, set()).add(dt)
    comparisons = []

    def add(name, kind, terms, dt, T, meta):
        values = [(a, rows[law, prep, dt, T]) for a, law, prep in terms]
        whole = fsum(a * r["history"]["ell_bits"] for a, r in values)
        local = {}
        for part in ("A", "B"):
            interval = linear_interval(
                [
                    (
                        a,
                        r["projected_histories"][part]["lower_bits"],
                        r["projected_histories"][part]["upper_bits"],
                    )
                    for a, r in values
                ]
            )
            interval["resolved_sign"] = (
                1 if interval["lower"] > eps else -1 if interval["upper"] < -eps else 0
            )
            local[part] = interval
        obs = {
            key: {
                field: fsum(a * r["observables"][key][field] for a, r in values)
                for field in ("endpoint", "integrated", "stationary")
            }
            for key in values[0][1]["observables"]
        }
        function = {
            part: {
                field: fsum(
                    a * r["functional_profiles"][part][field] for a, r in values
                )
                for field in (
                    "endpoint_functional_probability",
                    "integrated_functional_time",
                    "uninterrupted_initial_function_probability",
                    "initial_function_lost_then_returned_probability",
                )
            }
            for part in ("A", "B")
        }
        rate = fsum(a * r["asymptotic"]["rate_bits_per_time"] for a, r in values)
        offset = fsum(a * r["asymptotic"]["offset_bits"] for a, r in values)
        comparisons.append(
            {
                "id": name,
                "kind": kind,
                "cadence": dt,
                "horizon": T,
                "terms": [[a, law, prep] for a, law, prep in terms],
                "metadata": meta,
                "delta_ell_bits": whole,
                "sign": numerical_sign(whole, eps),
                "delta_projected_histories": local,
                "delta_observables": obs,
                "delta_functional_profiles": function,
                "delta_rate_bits_per_time": rate,
                "delta_offset_bits": offset,
                "asymptotic_crossover_estimate": (
                    -offset / rate if abs(rate) > 1e-12 else None
                ),
                "delta_activity": {
                    key: fsum(a * r["activity"][key] for a, r in values)
                    for key in ("expected_jumps", "finite_coefficient_bits")
                },
                "delta_work": {
                    key: fsum(a * r["physical"][key] for a, r in values)
                    for key in (
                        "work_net",
                        "work_accepted_gross",
                        "work_returned_gross",
                    )
                },
            }
        )

    for law, dt in protocol["case_grid"]:
        for T in protocol["horizons"]:
            add(
                law + ":assembled-minus-unassembled",
                "preparation",
                [(1, law, "assembled"), (-1, law, "unassembled")],
                dt,
                T,
                {"comparison_kind": "preparation"},
            )
    recipes = [
        ("local-minus-ablation", "catalysis", [("local", 1), ("ablation", -1)]),
        ("AtoB-minus-local", "cross_assistance", [("AtoB", 1), ("local", -1)]),
        ("BtoA-minus-local", "cross_assistance", [("BtoA", 1), ("local", -1)]),
        (
            "reciprocal-minus-local",
            "cross_assistance",
            [("reciprocal", 1), ("local", -1)],
        ),
        (
            "reciprocal-minus-AtoB",
            "cross_assistance",
            [("reciprocal", 1), ("AtoB", -1)],
        ),
        (
            "reciprocal-minus-BtoA",
            "cross_assistance",
            [("reciprocal", 1), ("BtoA", -1)],
        ),
        (
            "cross-edge-interaction",
            "factorial_interaction",
            [("reciprocal", 1), ("AtoB", -1), ("BtoA", -1), ("local", 1)],
        ),
    ]
    for regime in protocol["regimes"]:
        for title, kind, recipe in recipes:
            cadences = set.intersection(
                *(available[lookup[regime["id"], m]] for m, a in recipe)
            )
            for prep in ("assembled", "unassembled"):
                for dt in sorted(cadences):
                    for T in protocol["horizons"]:
                        add(
                            regime["id"] + ":" + title + ":" + prep,
                            kind,
                            [(a, lookup[regime["id"], m], prep) for m, a in recipe],
                            dt,
                            T,
                            {
                                "comparison_kind": "mechanism",
                                "regime": regime["id"],
                                "preparation": prep,
                                "contrast": title,
                            },
                        )
    regimes = [r for r in protocol["regimes"] if r["source"] > 0]
    for factor in ("source", "bill_ticks", "turnover"):
        others = [f for f in ("source", "bill_ticks", "turnover") if f != factor]
        for a in regimes:
            for b in regimes:
                if a[factor] <= b[factor] or any(a[f] != b[f] for f in others):
                    continue
                for mechanism in protocol["mechanisms"]:
                    la, lb = lookup[a["id"], mechanism], lookup[b["id"], mechanism]
                    for dt in sorted(available[la] & available[lb]):
                        for prep in ("assembled", "unassembled"):
                            for T in protocol["horizons"]:
                                add(
                                    factor
                                    + ":"
                                    + a["id"]
                                    + "-minus-"
                                    + b["id"]
                                    + ":"
                                    + mechanism
                                    + ":"
                                    + prep,
                                    "factor_effect",
                                    [(1, la, prep), (-1, lb, prep)],
                                    dt,
                                    T,
                                    {
                                        "comparison_kind": "mechanism",
                                        "changed_axis": "boundary"
                                        if factor == "source"
                                        else "kinetics_or_bill",
                                        "factor": factor,
                                        "higher": a,
                                        "lower": b,
                                        "mechanism": mechanism,
                                        "preparation": prep,
                                    },
                                )
    dark = next(r for r in protocol["regimes"] if r["source"] == 0)
    for regime in regimes:
        if (
            regime["bill_ticks"] != dark["bill_ticks"]
            or regime["turnover"] != dark["turnover"]
        ):
            continue
        for mechanism in protocol["mechanisms"]:
            la, lb = lookup[regime["id"], mechanism], lookup[dark["id"], mechanism]
            for dt in sorted(available[la] & available[lb]):
                for prep in ("assembled", "unassembled"):
                    for T in protocol["horizons"]:
                        add(
                            regime["id"]
                            + ":driven-minus-dark:"
                            + mechanism
                            + ":"
                            + prep,
                            "source_anchor",
                            [(1, la, prep), (-1, lb, prep)],
                            dt,
                            T,
                            {
                                "comparison_kind": "mechanism",
                                "changed_axis": "boundary",
                                "regime": regime["id"],
                                "mechanism": mechanism,
                                "preparation": prep,
                            },
                        )
    profiles = comparison_profiles(comparisons, eps)
    counts = {
        kind: dict(Counter(str(r["sign"]) for r in comparisons if r["kind"] == kind))
        for kind in dict.fromkeys(r["kind"] for r in comparisons)
    }
    primary = [r for r in comparisons if r["cadence"] == 0.25]
    conflicts = []
    for r in primary:
        if r["kind"] not in ("catalysis", "cross_assistance"):
            continue
        for part in ("A", "B"):
            if r["sign"] * r["delta_projected_histories"][part]["resolved_sign"] == -1:
                conflicts.append(
                    {
                        "id": r["id"],
                        "cadence": r["cadence"],
                        "horizon": r["horizon"],
                        "part": part,
                        "whole_delta_bits": r["delta_ell_bits"],
                        "local_interval": r["delta_projected_histories"][part],
                    }
                )
    return {
        "schema": "omega.E1-analysis/1",
        "comparisons": comparisons,
        "comparison_profiles": profiles,
        "sign_counts_all_queries": counts,
        "primary_local_whole_opposite_signs": conflicts,
        "interpretation": "Exploratory physical relations; interval overlap unresolved; no optimizer or ethical verdict",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    run = args.run_dir.resolve()
    out = args.out_dir.resolve()
    if (
        not run.is_relative_to(ROOT / "runs")
        or not out.is_relative_to(ROOT / "research/studies")
        or out.exists()
    ):
        parser.error("Use a complete run and a fresh study-results directory")
    receipt = json.loads((run / "BATCH_RECEIPT.json").read_text())
    manifest_path = run / "frozen/MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    protocol_path = run / "frozen" / manifest["protocol"]
    protocol = json.loads(protocol_path.read_text())
    if (
        receipt["status"] != "passed"
        or receipt["feasibility_only"]
        or digest(manifest_path) != receipt["manifest_sha256"]
        or digest(protocol_path) != receipt["protocol_sha256"]
    ):
        raise RuntimeError("Complete frozen batch required")
    for f in manifest["files"]:
        if digest(run / "frozen" / f["path"]) != f["sha256"]:
            raise RuntimeError("Snapshot changed")
    rows = {}
    for case in receipt["cases"]:
        path = run / case["case"] / "RESULT.json"
        result = json.loads(path.read_text())
        if (
            not case["validated"]
            or digest(path) != case["result_sha256"]
            or result["manifest_sha256"] != receipt["manifest_sha256"]
        ):
            raise RuntimeError("Case provenance mismatch")
        for row in result["rows"]:
            key = (row["law"], row["preparation"], row["cadence"], row["horizon"])
            if key in rows:
                raise RuntimeError("Duplicate physical row")
            rows[key] = row
    expected = {
        (law, p["id"], dt, T)
        for law, dt in protocol["case_grid"]
        for p in protocol["preparations"]
        for T in protocol["horizons"]
    }
    if set(rows) != expected:
        raise RuntimeError("Missing or unexpected physical profiles")
    analysis = build_analysis(protocol, rows)
    analysis["profile_rows"] = len(rows)
    analysis["comparison_rows"] = len(analysis["comparisons"])
    primary = [
        r
        for r in analysis["comparisons"]
        if r["cadence"] == 0.25 and r["horizon"] == 4096
    ]
    selected = [
        r
        for r in primary
        if r["kind"] in ("catalysis", "cross_assistance", "factorial_interaction")
    ]
    tables = [
        "| Regime / contrast / root | Whole delta bits | A interval | B interval |",
        "|---|---:|---:|---:|",
    ]
    for r in selected:
        a, b = [r["delta_projected_histories"][p] for p in ("A", "B")]
        tables.append(
            f"| {r['id']} | {r['delta_ell_bits']:+.5f} | [{a['lower']:+.4f}, {a['upper']:+.4f}] | [{b['lower']:+.4f}, {b['upper']:+.4f}] |"
        )
    summary = {}
    for kind in analysis["sign_counts_all_queries"]:
        values = [r for r in primary if r["kind"] == kind]
        summary[kind] = dict(Counter(str(r["sign"]) for r in values))
    diagnostics = [
        r["horizon_diagnostics"] for r in rows.values() if r["horizon"] == 4096
    ]
    cadence_profiles = analysis["comparison_profiles"]["cadence_audit"]
    audited = [r for r in cadence_profiles if len(r["points"]) > 1]
    horizon_profiles = analysis["comparison_profiles"]["horizon_audit"]
    analysis["summary"] = {
        "primary_T4096_sign_counts": summary,
        "max_T4096_total_variation": max(
            r["endpoint_total_variation_to_stationary"] for r in diagnostics
        ),
        "max_T4096_abs_rate_offset_residual_bits": max(
            abs(r["rate_offset_profile_residual_bits"]) for r in diagnostics
        ),
        "cadence_audited_groups": len(audited),
        "cadence_flip_groups": sum(r["strict_sign_flip"] for r in audited),
        "horizon_flip_groups": sum(r["strict_sign_flip"] for r in horizon_profiles),
        "primary_resolved_opposite_local_whole": len(
            analysis["primary_local_whole_opposite_signs"]
        ),
    }
    out.mkdir(parents=True)
    (out / "cases").mkdir()
    for case in receipt["cases"]:
        shutil.copyfile(
            run / case["case"] / "RESULT.json", out / "cases" / (case["case"] + ".json")
        )
    for name, path in [
        ("PROTOCOL.json", protocol_path),
        ("SOURCE_MANIFEST.json", manifest_path),
        ("BATCH_RECEIPT.json", run / "BATCH_RECEIPT.json"),
    ]:
        shutil.copyfile(path, out / name)
    (out / "ANALYSIS.json").write_text(
        json.dumps(analysis, indent=2, allow_nan=False) + "\n"
    )
    text = f"""# E1 coupled autocatalysis — numerical map

25 October 2026. {len(rows)} complete profiles from {len(receipt["cases"])}
validated law/cadence cases. Nine regimes (eight supplied and one dark anchor),
five mechanism arms, two equal-energy preparations. Full configuration and
source snapshots are retained. Completion is independent of scientific signs.

This is a finite chemical mechanism map, not a policy search or an ethical verdict.
The unassembled preparation can self-assemble; it is not microscopic gas.
Source-off remains thermally active. Costs are changed at fixed bank quantum,
capacity, capture yield and formation energy. Native turnover changes construction
AND breakdown. Catalysts accelerate forward and reverse together. Shared physical
opportunity is matched within each comparison; absorbed work/activity can differ.

## Summary

```json
{json.dumps(analysis["summary"], indent=2)}
```

The sign counts above are at cadence .25 and T4096, not independent replications.
The complete surface has {len(analysis["comparisons"])} contrasts, with horizon
and cadence audits kept separate. Single-cadence groups are unaudited, not proven
stable. Numerical deadband is1e-6 bits; local intervals are float64 evaluations
of analytic entropy inequalities, not rigorous numerical certificates. Overlap
remains unresolved. Coordinate shares are not subject entropy.

Every raw profile retains function, state stocks, ancestry, work/heat, expected
events, N/F activity coefficients, full history, rate/offset and convergence.
See ANALYSIS.json for factor effects, factorial cross-edge interactions, source
anchor comparisons, horizon sign brackets and finite accumulation intervals.
Asymptotic crossover estimates are estimates, not verified finite-profile roots.

## Mechanisms at T4096, cadence .25

{chr(10).join(tables)}

Local vs ablation removes both assisted capture and assisted construction pairs.
One-way and reciprocal comparisons add the named cross-construction channels;
their recipient pays. Full factorial interaction uses all four cross-edge laws.
An increase in history breadth is not automatically an improvement in function,
and a one-way helper route is not automatically parasitism or beneficial help.

## Limits and execution

Full modeled field includes the shared carrier, all banks and all component
states. Bath/source histories remain unresolved. Each local projection contains
that group's slots/bank conditioned on the full present; projections are not
summed to obtain the whole. Native channels and all random activity stay counted.
Ancestry is within-group native marked construction, not full community or
resource-packet provenance. Irreducibility precludes permanent structural closure.
Four slots preclude unbounded expansion or a general population result.

No comparator is a physically enacted choice from one common present. Same-law
preparation rates tie; they differ in finite profiles and offsets. Matched
endowments do not make a preparation contrast a costed construction decision.
Cadence audit uses two fixed corners only; temporal faithfulness stays open.
Model coefficients and count grain are stipulated rather than microscopic.

Wall time {receipt["wall_seconds"]:.2f}s, up to {receipt.get("max_workers", 1)} workers;
maximum per-job commitment {max(c["receipt"]["peak_job_bytes"] for c in receipt["cases"]) / 1024**2:.2f} MiB.
Per-job caps240s/2GiB/16MiB; batch1800s/128MiB monitored output. Sources and compact
results are preserved without dense kernels or trajectories. No commit/push/upload.
"""
    (out / "RESULTS.md").write_text(text, encoding="utf-8")
    for p in (
        Path(__file__).resolve(),
        ROOT / "src/omega_cosmology/testbed/analysis.py",
    ):
        target = out / "analysis_source" / p.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
    evidence = {
        "schema": "omega.E1-evidence/1",
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
    (out / "EVIDENCE.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": "verified",
                "profiles": len(rows),
                "comparisons": len(analysis["comparisons"]),
                **analysis["summary"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
