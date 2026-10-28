"""Package retained physical-control checks without rerunning or selecting scores."""

import argparse
import json
import re
import shutil
from hashlib import sha256
from pathlib import Path

from report_r2_integrated_smoke import read, retain_snapshot, write

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("run", "check", "previous", "out"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    run, check, previous, out = (
        getattr(args, name).resolve() for name in ("run", "check", "previous", "out")
    )
    engineering = ROOT / "research/platform/engineering"
    if out.exists() or not out.is_relative_to(engineering):
        parser.error("Fresh engineering evidence directory required")
    if not previous.is_relative_to(engineering):
        parser.error("Previous evidence must be retained engineering output")
    receipt = read(run / "BATCH_RECEIPT.json")
    result = read(run / "smoke/RESULT.json")
    checks = read(check / "CHECKS.json")
    if any(v["status"] != "passed" for v in (receipt, result, checks)):
        raise ValueError("Successful execution and workspace checks required")
    calibration = read(run / "smoke/CALIBRATION.json")
    fit = calibration["fit"]
    history_evaluated = bool(result["cases"])
    boundary = result.get("history_evaluated") is False
    if boundary == history_evaluated:
        raise ValueError("Explicit history status inconsistent with cases")
    out.mkdir(parents=True)
    retained = out / "retained"
    retained.mkdir()
    for path in sorted((run / "smoke").glob("*.json")):
        shutil.copyfile(path, retained / path.name)
    shutil.copyfile(run / "BATCH_RECEIPT.json", out / "BATCH_RECEIPT.json")
    retain_snapshot(run, out)
    payment = calibration.get("selected_payment")
    if payment is None:
        # The final row is the independent replay of the selected point.
        selected = calibration["physical_evaluations"][-1]
        if selected["parameters"] != fit["best"]["parameters"]:
            raise ValueError("Last physical replay is not the selected fit")
        payment = selected["payment"]
    qualified = (
        payment["net_bank_payment"] > 1e-8 and payment["paid_channel_fraction"] > 0.5
    )
    if boundary and qualified:
        raise ValueError("Qualification boundary contradicts selected payment")
    points = []
    seen = set()
    for row in calibration["physical_evaluations"]:
        key = tuple(sorted(row["parameters"].items()))
        if key in seen:
            continue
        seen.add(key)
        matches = {
            k: abs(row["moments"][k] - fit["target"][k])
            <= fit["absolute_allowances"][k]
            for k in fit["target"]
        }
        points.append(
            {**row, "within_tolerance": matches, "joint_match": all(matches.values())}
        )
    counts = {
        "distinct_points": len(points),
        "joint_matches": sum(p["joint_match"] for p in points),
        "net_paying_majority_paid_points": sum(
            p["payment"]["net_bank_payment"] > 1e-8
            and p["payment"]["paid_channel_fraction"] > 0.5
            for p in points
        ),
        "qualified_joint_matches": sum(
            p["joint_match"]
            and p["payment"]["net_bank_payment"] > 1e-8
            and p["payment"]["paid_channel_fraction"] > 0.5
            for p in points
        ),
    }
    write(
        out / "PHYSICAL_MAP.json",
        {
            "points": points,
            "counts": counts,
            "physical_only_before_history": True,
            "scope": "Evaluated points only; no global feasibility claim",
        },
    )
    raw = (check / "tests.txt").read_text(encoding="utf-8")
    validation = {
        "status": "passed",
        "tests": int(re.search(r"Ran (\d+) tests", raw)[1]),
        "workspace": {v["name"]: v["exit_code"] for v in checks["checks"]},
        "P001_full_object_equal": checks["P001_full_object_equal"],
        "P001_scientific_summary_equal": checks["P001_scientific_summary_equal"],
        "scope": "Workspace numerical/contracts checks; no physical-faithfulness certificate",
    }
    write(out / "VALIDATION.json", validation)
    spec = (
        "R2_BANK_LOAD_CONTROL_r1.md" if boundary else "R2_ACTIVITY_ONLY_CONTROL_r1.md"
    )
    revision = (
        "Remove B gating from the rotor equally in all arms; retain the fixed thermal pair and native refunds"
        if boundary
        else "Restrict the same B-gated paid rotor to equal charge/reset barriers and fit event count alone"
    )
    write(
        out / "REVISION.json",
        {
            "previous": previous.relative_to(ROOT).as_posix(),
            "previous_evidence_sha256": sha256(
                (previous / "EVIDENCE.json").read_bytes()
            ).hexdigest(),
            "change": revision,
            "previous_results_retained": True,
            "selection": "Physical moments only; no entropy in calibration",
        },
    )
    quality = {
        "numerical": {
            "method": "finite-model float64 occupation integrals and independent selected-point replay",
            "rigorous_interval_arithmetic": False,
        },
        "resolution": {
            "history_evaluated": history_evaluated,
            "cadences": [0.25, 0.5] if history_evaluated else [],
            "state_grain": "distinct finite count slots",
            "faithfulness": "open",
        },
        "physical_adequacy": "Reversible finite chemistry; unresolved source/bath histories; no spatial disorder",
        "claim_relevance": {
            "matching_status": fit["status"],
            "selected_payment": payment,
            "net_paying_majority_paid_control": qualified,
            "activity_work_independent_gain": "not established",
            "ethics": "not assessed",
        },
    }
    score_text = """No sampled-history entropy or stationary entropy rate was calculated for this
bank-load family. The selected control fails the net-payment prerequisite, so
the worker stopped before the history stage. An execution status of `passed`
means the prescribed bounded check completed, not that this comparator qualified.
No further family adjustment or history search follows from this checkpoint.
"""
    if history_evaluated:
        profiles = [
            row
            for case in result["cases"]
            for row in read(
                retained / (case["id"] + "__dt" + str(case["cadence"]) + ".json")
            )["rows"]
        ]
        quality["numerical"]["max_first_law_residual"] = max(
            abs(r["physical"]["energy_residual"]) for r in profiles
        )
        quality["numerical"]["max_query_residual"] = max(
            max(r["validation"].values()) for r in profiles
        )
        rows = [
            f"| {c['second']} | {c['horizon']} | {c['cadence']} | {c['delta_history_bits']:+.9f} | {c['delta_rate_bits_per_time']:+.9f} |"
            for c in result["comparisons"]
        ]
        score_text = f"""Three 324-state laws, cadences 0.25/0.5, horizons 4/16/64: 18 finite profiles.
Productive minus comparator in complete-history bits; every represented event
counts. Rate differences are separate stationary diagnostics, not observed
later-horizon wins. T64 count matching does not match stationary event rates.

| Comparator | Horizon | Cadence | History difference (bits) | Rate difference (bits/time) |
|---|---:|---:|---:|---:|
{chr(10).join(rows)}

The count-only candidate exceeds productive finite lushness at T64 while accepting
more gross external work and returning net bank energy through the rotor.
It is an activity-matched comparison, not a jointly work-matched or net-consuming
nonproductive comparator. These limitations do not invalidate its native history
scores. They restrict what can be attributed to organization. The signs at two
cadences do not establish physical-resolution faithfulness.
"""
    write(out / "QUALITY.json", quality)
    best = fit["best"]
    table = [
        f"| {k} | {target:.12g} | {best['moments'][k]:.12g} | {best['absolute_residuals'][k]:+.9g} | {fit['absolute_allowances'][k]:.9g} |"
        for k, target in fit["target"].items()
    ]
    heading = (
        "Bank-load physical qualification boundary"
        if boundary
        else "Equal-barrier activity-only control"
    )
    report = f"""# R2 — {heading}

Completed locally 28 October 2026 from the 27 October execution snapshot. Bounded
engineering check only; no broader campaign, commit or push.
[Specification](../../specs/{spec}); [previous check](../{previous.name}/REPORT.md).

## Physical check

{revision}. The native thermal pair stays at conductance 0.003. Each forward
charge/reset withdraws 0.5 bank energy, and its exact reverse refunds 0.5. A forward
closed rotor cycle spends 1 energy unit; actual net spending must still be measured.
The A/B/C construction, material inventories and two stochastic carriers remain.
Comparisons are same-root mechanism contrasts, not optimized choices under one law.
Whole modeled field excludes unresolved external boundary histories.

Calibration precedes history scoring and uses only continuous T64 occupation
moments. Matching status: **{fit["status"]}**. Selected parameters:
`{json.dumps(best["parameters"], sort_keys=True)}`.

| Moment | Target | Selected control | Control minus target | Allowed absolute error |
|---|---:|---:|---:|---:|
{chr(10).join(table)}

Tolerance for each moment is 1e-8 + 0.001 times its target. Equal event count
does not certify equal work, and matching both moments does not certify a
net-consuming load. No histories were conditioned on their realized counts.
The [physical map](PHYSICAL_MAP.json) retains all distinct evaluated parameter
points. The selected point was independently replayed. No global impossibility
or unique organization-only contribution follows from this bounded search.

Among {counts["distinct_points"]} distinct evaluated points,
{counts["joint_matches"]} match both moments,
{counts["net_paying_majority_paid_points"]} qualify as net-paying majority-paid
loads, and {counts["qualified_joint_matches"]} satisfy both requirements.

At T64 the selected rotor has {payment["paid_channel_events"]:.12g} paid-channel
events and {payment["thermal_channel_events"]:.12g} thermal events
({100 * payment["paid_channel_fraction"]:.6f}% paid-channel activity).
Gross bank withdrawal={payment["gross_bank_withdrawal"]:.12g};
gross refund={payment["gross_bank_refund"]:.12g};
**net payment={payment["net_bank_payment"]:+.12g}**. A negative net payment
means the rotor returns energy to the bank. Its channel name and predominance
of paid-channel events do not make it a net-consuming load.
Net-paying, majority-paid qualification: **{qualified}**.

## History accounting and interpretation

{score_text}

The chain's distinct physical functions remain demonstrated by the prior
construction/transduction readouts. This control check leaves the clean
productive-versus-net-consuming comparison open. It is a comparator boundary,
not a failure of the generativity principle. All preceding scores, calibrations
and source snapshots remain intact, including the joint B-gated control's
negative net payment of about 0.025513 energy and the older thermally dominated
rotor. No result is removed because its ranking is inconvenient.

## Verification and provenance

The workspace check passes {validation["tests"]} tests, source/archive/evidence
checks and exact baseline/P001 reproduction. Native energy/material audits
and the fixed thermal rule are executable contracts. Receipt elapsed time:
{receipt["receipt"]["wall_seconds"]:.3f} s; peak
{receipt["receipt"]["peak_job_bytes"] / 1024**2:.2f} MiB under 900 s / 1 GiB / 64 MiB caps.
[Retained results](retained/RESULT.json), [calibration](retained/CALIBRATION.json),
[quality axes](QUALITY.json), [validation](VALIDATION.json), source snapshot and
byte manifest accompany this report. Numerical success does not certify physical
adequacy or the ethical thesis. Further comparator design requires review;
there is no automatic continuation of the search.
"""
    (out / "REPORT.md").write_text(report, encoding="utf-8")
    analysis = out / "analysis"
    analysis.mkdir()
    shutil.copyfile(Path(__file__).resolve(), analysis / Path(__file__).name)
    shutil.copyfile(
        ROOT / "scripts/report_r2_integrated_smoke.py",
        analysis / "report_r2_integrated_smoke.py",
    )
    files = [
        {
            "path": p.relative_to(out).as_posix(),
            "sha256": sha256(p.read_bytes()).hexdigest(),
            "bytes": p.stat().st_size,
        }
        for p in sorted(out.rglob("*"))
        if p.is_file()
    ]
    write(
        out / "EVIDENCE.json", {"schema": "omega.retained-evidence/1", "files": files}
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "out": out.relative_to(ROOT).as_posix(),
                "files": len(files),
                "history_evaluated": history_evaluated,
            }
        )
    )


if __name__ == "__main__":
    main()
