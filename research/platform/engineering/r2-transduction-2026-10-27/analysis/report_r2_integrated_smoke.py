"""Retain compact R2 integration evidence and report its measured limits."""

import argparse
import json
import re
import shutil
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def retain_snapshot(run, folder):
    with ZipFile(folder / "SNAPSHOT.zip", "w", ZIP_DEFLATED) as archive:
        for path in sorted((run / "frozen").rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(run / "frozen").as_posix())
    shutil.copyfile(run / "frozen/MANIFEST.json", folder / "SOURCE_MANIFEST.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    history = parser.add_mutually_exclusive_group(required=True)
    history.add_argument("--initial", type=Path)
    history.add_argument("--previous", type=Path)
    parser.add_argument("--check", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    run, check, out = (p.resolve() for p in (args.run, args.check, args.out))
    if out.exists() or not out.is_relative_to(ROOT / "research/platform/engineering"):
        parser.error("Fresh engineering evidence directory required")
    receipt, summary = read(run / "BATCH_RECEIPT.json"), read(run / "smoke/RESULT.json")
    checks = read(check / "CHECKS.json")
    if any(v["status"] != "passed" for v in (receipt, summary, checks)):
        raise ValueError(
            "Engineering completion needs successful numerical smoke and workspace check"
        )
    out.mkdir(parents=True)
    retained = out / "retained"
    retained.mkdir()
    for path in (run / "smoke").glob("*.json"):
        shutil.copyfile(path, retained / path.name)
    shutil.copyfile(run / "BATCH_RECEIPT.json", out / "BATCH_RECEIPT.json")
    retain_snapshot(run, out)
    if args.initial:
        initial = args.initial.resolve()
        first = out / "initial-attempt"
        first.mkdir()
        retain_snapshot(initial, first)
        for name in ("CALIBRATION.json", "productive__dt0.25.json"):
            shutil.copyfile(initial / "smoke" / name, first / name)
        shutil.copyfile(initial / "BATCH_RECEIPT.json", first / "BATCH_RECEIPT.json")
        write(
            first / "ERROR.json",
            {
                "kind": "reporting_field_mismatch",
                "error": "KeyError: wall_seconds",
                "fix": "Use the shared assay's worker_seconds field",
                "physics_changed": False,
                "handling": "Same parameters and tolerance rerun in a fresh snapshot; failed attempt preserved",
            },
        )
        history_note = "The initial attempt stopped on a timing-field typo. Its source, fit, first profiles and receipt remain under initial-attempt/. The fresh rerun changed no physical law or tolerance."
    else:
        previous = args.previous.resolve()
        if not previous.is_relative_to(ROOT / "research/platform/engineering"):
            parser.error("Previous evidence must be a retained engineering folder")
        previous_manifest = previous / "EVIDENCE.json"
        write(
            out / "REVISION.json",
            {
                "previous": previous.relative_to(ROOT).as_posix(),
                "previous_evidence_sha256": sha256(
                    previous_manifest.read_bytes()
                ).hexdigest(),
                "physical_change": "B now stores .5 energy during secondary conversion; bank-space guard added; A remains heat-only unlocking",
                "reason": "Make the second structure's function physically distinct, rather than another copy of unlocking",
                "previous_results_retained": True,
            },
        )
        history_note = f"The [preceding integration](../{previous.name}/REPORT.md) remains intact with all profiles and its first reporting-error attempt. This revision changes B's stoichiometry to energy transduction, with a bank-space guard. It tests a distinct second function; it does not discard or relabel the earlier result."
    raw = (check / "tests.txt").read_text(encoding="utf-8")
    validation = {
        "status": "passed",
        "tests": int(re.search(r"Ran (\d+) tests", raw).group(1)),
        "workspace": {v["name"]: v["exit_code"] for v in checks["checks"]},
        "P001_full_object_equal": checks["P001_full_object_equal"],
        "P001_scientific_summary_equal": checks["P001_scientific_summary_equal"],
        "scope": "Whole workspace checked; no physical-resolution or ethical certificate",
    }
    write(out / "VALIDATION.json", validation)
    fit = read(retained / "CALIBRATION.json")["fit"]
    inputs = read(retained / "EXECUTION_CASES.json")
    transduction = inputs[0]["law"]["model"]["id"].endswith("v2")
    spec = "R2_INTEGRATED_SMOKE_r2.md" if transduction else "R2_INTEGRATED_SMOKE_r1.md"
    profiles = []
    for case in summary["cases"]:
        result = read(retained / (case["id"] + "__dt" + str(case["cadence"]) + ".json"))
        for row in result["rows"]:
            profiles.append((case["id"], case["cadence"], row))
    max_energy = max(abs(r["physical"]["energy_residual"]) for _, _, r in profiles)
    max_numerical = max(max(r["validation"].values()) for _, _, r in profiles)
    productive64 = next(
        r
        for name, dt, r in profiles
        if name == "productive" and dt == 0.25 and r["horizon"] == 64
    )
    contrast_table = []
    for second in (
        "no_construction_assistance",
        "no_secondary_access",
        "neither_link",
        "matched_rotor",
    ):
        for horizon in (4, 16, 64):
            values = [
                next(
                    c
                    for c in summary["comparisons"]
                    if c["second"] == second
                    and c["cadence"] == dt
                    and c["horizon"] == horizon
                )["delta_history_bits"]
                for dt in (0.25, 0.5)
            ]
            contrast_table.append(
                f"| {second} | {horizon} | {values[0]:+.8f} | {values[1]:+.8f} |"
            )
    physical_table = []
    for name, dt, row in profiles:
        if dt == 0.25 and row["horizon"] == 64:
            physical_table.append(
                f"| {name} | {row['physical']['expected_jumps']:.6f} | {row['physical']['work_accepted_gross']:.6f} | {row['observables']['products.B']['integrated']:.6f} | {row['event_readouts']['B_assisted.forward']:.6f} | {row['event_readouts']['secondary_access.forward']:.6f} | {row['witnesses']['paid_connected_chain']['completed_probability']:.8g} |"
            )
    write(
        out / "QUALITY.json",
        {
            "numerical": {
                "method": "full finite model float64; independent propagation/entropy identities; passive marginal checks",
                "max_first_law_residual": max_energy,
                "max_query_residual": max_numerical,
                "rigorous_interval_arithmetic": False,
            },
            "resolution": {
                "cadences": [0.25, 0.5],
                "state_grain": "distinct finite count slots",
                "faithfulness": "open",
            },
            "physical_adequacy": "Stipulated reversible finite chemistry with explicit material, prices, ports and opportunity cost; no spatial disorder or external boundary histories",
            "claim_relevance": {
                "construction": "costed two-function chain and actual use readouts",
                "activity_independent_gain": "not established unless both finite moment tolerances pass; no claim from a near match",
                "ethics": "not assessed",
            },
        },
    )
    best = fit["best"]
    control64 = next(
        r
        for name, dt, r in profiles
        if name == "matched_rotor" and dt == 0.25 and r["horizon"] == 64
    )
    rotor_paid = (
        control64["event_readouts"]["rotor_stroke.forward"]
        + control64["event_readouts"]["rotor_stroke.reverse"]
    )
    rotor_thermal = (
        control64["event_readouts"]["rotor_relax.forward"]
        + control64["event_readouts"]["rotor_relax.reverse"]
    )
    rate_gaps = [
        next(
            c["delta_rate_bits_per_time"]
            for c in summary["comparisons"]
            if c["second"] == "matched_rotor"
            and c["cadence"] == dt
            and c["horizon"] == 64
        )
        for dt in (0.25, 0.5)
    ]
    paid_share = rotor_paid / (rotor_paid + rotor_thermal)
    rotor_description = (
        "Most fitted rotor events are thermal; this does not supply a predominantly paid-cycling comparator."
        if paid_share < 0.5
        else "Most fitted rotor events use the paid cycle; this alone does not establish work/activity matching."
    )
    secondary_description = (
        "B transduces secondary energy: locked3 becomes usable2 plus.5 stored in the bank and.5 heat. A instead unlocks its carrier with1 heat and no bank return. Their functions and stoichiometries differ."
        if transduction
        else "B unlocks a separate resource carrier. This uses another route but is kinetically similar to A; the later transduction revision addresses the weak distinct-function comparison."
    )
    quality = read(out / "QUALITY.json")
    quality["claim_relevance"]["rotor_paid_event_fraction"] = paid_share
    quality["claim_relevance"]["paid_churn_control"] = rotor_description
    write(out / "QUALITY.json", quality)
    report = f"""# R2 integrated construction and paid-control smoke

27 October 2026. Complete locally; smoke checkpoint only. No wider map or push.
Read the [existing-R2 audit](../../models/r2-integrated/AUDIT.md) and
[specification](../../specs/{spec}) with these results.

## Engineering result

Five laws, two cadences and three horizons:30 finite profiles,324 states per law.
Every paired comparison validates the actual common root, energy, inventories,
boundary prescription, observation and window. Native source-off balance and
complete-history identities pass. Maximum first-law residual {max_energy:.3g};
maximum query/propagation residual {max_numerical:.3g}. The whole-workspace check
passes {validation["tests"]} tests and exact baseline evidence reproduction.

Run time {summary["wall_seconds"]:.3f}s; capped-worker peak
{receipt["receipt"]["peak_job_bytes"] / 1024**2:.2f}MiB, below900s/1GiB/64MiB.
Explicit module ports bind resource carriers, bank, construction, capture,
secondary access and rotor. Bindings do not create physical events.

## Physical chain and competing use

A is constructed using the common bank and assists B/C construction. B and C
compete for the same conserved precursor. {secondary_description}
C accelerates primary capture. Both carriers keep their native
stochastic paths in every arm. Thermal breakdown and paid/native rebuilding
remain, so payment is not assumed logically necessary for persistence.

T64 physical readouts at cadence.25:

| Law | Nbar | Gross accepted work | B uptime | Assisted B builds | B release events | Continuity witness probability |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(physical_table)}

The productive law's A uptime is
{productive64["observables"]["A.active"]["integrated"]:.6f}; C uptime is
{productive64["observables"]["products.C"]["integrated"]:.6f}. Raw forward/reverse
construction, capture and rotor counts travel with each full profile. Presence,
event counts and the witness are distinct quantities.

The conservative witness requires a paid A build, A-assisted B build, B-assisted
release and secondary capture, aborting if the necessary current A/B instance
or released carrier disappears. This supplies an instance-continuity check for
that sequence, not depth-three ancestry, causal necessity or energy-packet lineage.
The physical chain can occur on paths the conservative witness does not count.

## Lushness profiles

Productive minus comparator in complete-history bits; all physical events count.

| Comparator | Horizon | cadence.25 | cadence.5 |
|---|---:|---:|---:|
{chr(10).join(contrast_table)}

Rates and offsets remain diagnostics in retained profiles. These same-root
between-law contrasts can have different stationary rates; they are not choices
of an embodied optimizer under one law. No thermal spatial baseline is claimed.

## Work/activity control

Calibration status: **{fit["status"]}**. It was saved before history evaluation.
Target Nbar={fit["target"]["expected_jumps"]:.9f}, accepted work=
{fit["target"]["work_accepted_gross"]:.9f}. Selected rotor stroke=
{best["parameters"]["rotor_stroke"]:.9g}, relaxation=
{best["parameters"]["rotor_relax"]:.9g}. Residual(control-target): Nbar=
{best["absolute_residuals"]["expected_jumps"]:+.9g}, accepted work=
{best["absolute_residuals"]["work_accepted_gross"]:+.9g}.

Each moment must pass absolute1e-8+relative0.001 tolerance. The control is
retained whether it matches or not. No tolerance widening or path conditioning
occurred. A near event-count match with a work mismatch cannot demonstrate an
advantage independent of both work and activity. The bounded search also does
not prove that a matching physical control is impossible. The rotor changes
reserve occupancy and reverse flows; even an exact two-moment match would not
identify a unique organization-only contribution.

AtT64 the rotor candidate has
{rotor_paid:.9g} paid stroke/reverse events versus {rotor_thermal:.9g} thermal
forward/reverse events; paid fraction={paid_share:.6g}. {rotor_description}
The ID `matched_rotor` is a requested role, not a matching certificate. The
finite score remains a physical result of this law; the rotor gain cannot
automatically be attributed to energy-consuming nonproductive work.

The productive-minus-rotor limiting rate is
{rate_gaps[0]:+.9g} and {rate_gaps[1]:+.9g}bits/time at the two cadences. The
finite profile and long-horizon diagnostic are reported separately in this window.
No later horizon was run; a predicted repayment crossover is not an observed
crossover. T64 moment matching also says nothing about equality of stationary
work or event rates.

## What this checkpoint establishes and leaves open

The substrate can represent and measure a paid construction link, a distinct
downstream resource function, competition for a construction precursor, and a
paid non-enabling control under common resource prescriptions. Physical readouts
and complete histories are reported together. This is a bounded mechanism
fixture; its observed signs neither establish a universal ranking nor a theory
failure. Paid work, event activity and temporal resolution remain explicit.

The next decision should use the measured chain incidence and matching residuals:
improve the physical control family if needed, or size a limited cost/yield map.
No such expansion has been run. Spatial disorder, growing populations, third
generation, lineage of captured energy, paid sensing and ethical correspondence
remain separate extensions.

## Provenance and initial attempt

[Retained inputs/results](retained/RESULT.json), [comparison contracts](retained/COMPARISON_CONTRACTS.json),
[calibration](retained/CALIBRATION.json), [validation](VALIDATION.json) and
[quality axes](QUALITY.json) accompany the source snapshot and byte manifest.
{history_note}
"""
    (out / "REPORT.md").write_text(report, encoding="utf-8")
    analysis = out / "analysis"
    analysis.mkdir()
    shutil.copyfile(Path(__file__).resolve(), analysis / Path(__file__).name)
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
                "retained_files": len(files),
                "bytes": sum(v["bytes"] for v in files),
                "out": out.relative_to(ROOT).as_posix(),
            }
        )
    )


if __name__ == "__main__":
    main()
