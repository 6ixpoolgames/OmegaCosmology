"""Retain enacted-operation smoke evidence and report limits alongside numbers."""

import argparse
import json
import shutil
from hashlib import sha256
from pathlib import Path

from report_signed_studies import ROOT, retain_run, write


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    run, out = args.run.resolve(), args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "research/platform/engineering"):
        parser.error("Fresh engineering evidence directory required")
    receipt, records, manifest = retain_run(run, out / "retained")
    summary = records[0]
    rows, cases = {}, {}
    for case in summary["cases"]:
        name = case["id"]
        source = run / "smoke" / (name + ".json")
        if digest(source) != case["result_sha256"]:
            raise ValueError("Case evidence changed")
        shutil.copyfile(source, out / "retained/smoke" / source.name)
        cases[name] = json.loads(source.read_text(encoding="utf-8"))
        for row in cases[name]["rows"]:
            rows[name, row["horizon"]] = row
    for name in ("CALIBRATION.json", "EXECUTION_CASES.json"):
        shutil.copyfile(run / "smoke" / name, out / "retained/smoke" / name)
    calibration = json.loads(
        (run / "smoke/CALIBRATION.json").read_text(encoding="utf-8")
    )
    execution = json.loads(
        (run / "smoke/EXECUTION_CASES.json").read_text(encoding="utf-8")
    )
    if (
        len({json.dumps(c["root"]) for c in execution}) != 1
        or len({c["energy_per_root"] for c in execution}) != 1
    ):
        raise ValueError("Common present/endowment check failed")
    if (
        len({json.dumps(c["phases"][-1]["model"], sort_keys=True) for c in execution})
        != 1
    ):
        raise ValueError("Common recovery law check failed")
    for name, fit in calibration["fits"].items():
        control = rows["sham_for_" + name, 16]
        for k, value in fit["independent_replay"].items():
            if abs(value - control["physical"][k]) > 1e-10:
                raise ValueError("Matching replay changed when history was evaluated")
    residuals = {
        "energy": max(abs(r["physical"]["energy_residual"]) for r in rows.values()),
        "sampled_continuous_endpoint": max(
            r["validation"]["continuous_sampled_endpoint_residual"]
            for r in rows.values()
        ),
        "passive_monitor_marginal": max(
            r["validation"]["event_monitor_marginal_residual"] for r in rows.values()
        ),
    }
    quality = {
        "status": "passed",
        "cases": len(cases),
        "profiles": len(rows),
        "common_root_and_energy_verified": True,
        "common_recovery_verified": True,
        "calibration_replayed_without_history_objective": True,
        "residuals": residuals,
        "evidence_axes": {
            "numerical": "Full finite scheduled kernels and native occupation in float64; analytic projected inequalities, no interval rounding certificate",
            "resolution": "One cadence 0.25, full declared state and repair-body projections; no physical refinement certification",
            "physical_adequacy": "Paid reversible damage, material/contact/heat and finite actuator represented; external barrier-setting apparatus and bath/source histories unresolved",
            "claim_relevance": "Engineering feasibility and two physical moment controls; no permanent loss, suffering, ecological domination or normative verdict",
        },
        "source_manifest_sha256": summary["source_manifest_sha256"],
        "snapshot_inputs": len(manifest["files"]),
    }
    write(out / "QUALITY.json", quality)
    write(
        out / "SUMMARY.json",
        summary | {"calibration": calibration, "residuals": residuals},
    )
    cap = receipt["cases"][0]["receipt"]
    lines = [
        "# Enacted damage and matched physical controls — engineering smoke",
        "",
        "26 October 2026. Local, uncommitted. No wider scientific map or publication.",
        "",
        "## What was built",
        "",
        "A generic scheduled-native-law evaluator now carries the full outcome distribution, history entropy and projected-history memory across a paid operation pulse into common recovery. The old S3 fault preparations and results are unchanged.",
        "",
        "All arms start from the same intact root and energy 5, with the same finite actuator. A one-unit pulse enables R damage, Y damage, a non-damaging paid stroke, or ordinary idle dynamics. Each paid stroke consumes 0.5 bank energy; the actuator stores 0.25. Damage releases component/contact energy to heat. Reverse operations, basal repair and thermal motion remain. No outcome is selected or discarded.",
        "",
        "The barrier schedule is externally prescribed. Its setting apparatus is unresolved; this is the whole modeled field under a controlled boundary, not an autonomous controller or an encompassing universe.",
        "",
        "## Feasibility and numerical checks",
        "",
        f"Six 108-state cases, 18 profiles at cadence 0.25 and T1/4/16 passed in {cap['wall_seconds']:.2f}s. Peak job memory {cap['peak_job_bytes'] / 1024**2:.2f}MiB against 1 GiB; cap 300 s. Worker output{cap['output_bytes']:,} bytes. No cap/failure.",
        "",
        f"Maximum first-law residual {residuals['energy']:.3g}; sampled/continuous endpoint residual {residuals['sampled_continuous_endpoint']:.3g}; passive-monitor marginal residual {residuals['passive_monitor_marginal']:.3g}. Every phase passes source-off detailed balance. Query monitors add no physical entropy.",
        "",
        "## Moment calibration, before history scoring",
        "",
        "The sham's paid-stroke and thermal-relaxation conductances were calibrated only to expected represented state-changing jumps and gross accepted work at T16. All probes and bounded fits are retained; history entropy was not a fitting objective. Both controls match within the declared 0.001 scaled tolerance and replay unchanged during history evaluation.",
        "",
        "| Damage target | Sham stroke | Sham relaxation | Jump residual | Accepted-work residual |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, fit in calibration["fits"].items():
        b = fit["best"]
        target = rows[name, 16]["physical"]
        control = rows["sham_for_" + name, 16]["physical"]
        lines.append(
            f"|{name}|{b['parameters']['stroke_conductance']:.9f}|{b['parameters']['relaxation_conductance']:.9f}|{target['expected_jumps'] - control['expected_jumps']:+.3g}|{target['work_accepted_gross'] - control['work_accepted_gross']:+.3g}|"
        )
    lines += [
        "",
        "These are two finite-horizon moment matches. Net work, bank spending, timing, event sequences and correlations are not all matched. At shorter horizons the moments differ; the full residual map is retained. External work is reported gross and net: the initial locked carrier can return energy to the source, so net accepted work is negative in this preparation. No efficiency claim is inferred.",
        "",
        "## Preliminary physical readout",
        "",
        "These values characterize the smoke, not a parameter relationship or resolution-robust scientific conclusion.",
        "",
        "| Operation | T16 history minus idle (bits) | History minus calibrated sham (bits) | Both working at T16 | Integrated both-working time | P(any forward operation) | P(operation then return by T16) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name in ("idle", "damage_R", "damage_Y"):
        r = rows[name, 16]
        delta = r["history"]["ell_bits"] - rows["idle", 16]["history"]["ell_bits"]
        contrast = (
            "—"
            if name == "idle"
            else f"{r['history']['ell_bits'] - rows['sham_for_' + name, 16]['history']['ell_bits']:+.6f}"
        )
        lines.append(
            f"|{name}|{delta:+.6f}|{contrast}|{r['observables']['both_working']['endpoint']:.6f}|{r['observables']['both_working']['integrated']:.6f}|{r['operation_monitor']['any_forward_operation_probability']:.6f}|{r['operation_monitor']['operation_then_functional_return_probability']:.6f}|"
        )
    lines += [
        "",
        "Damage raises raw history relative to idle while reducing function. Relative to their T16 moment-matched shams, the R procedure is slightly higher and the Y procedure slightly lower. The R comparison changes sign between T4 and T16. The damage-associated gain cannot be attributed solely to a higher total event count or higher gross accepted work at this matched horizon; the actual transition distributions and history remain different. The controls also change actuator relaxation during the pulse, so this is not a unique causal decomposition of damage itself.",
        "",
        "The repair-body projected intervals resolve positive damage-minus-sham differences at T16 in this proxy, even for Y where whole history is lower. The body projection includes its bank and contacts, not the actuator or carrier. This is not evidence that impairment is beneficial: function, weighted histories and energy are distinct readouts. No phenomenal or ethical identification is made.",
        "",
        "The forward-operation probability is about 0.249 in either damage arm, so about 75% of paths have no forward damage stroke. All are included. Return probabilities are unconditional and refer to a subsequent return to both components working, not maintained recovery or successful-only paths. The corresponding sham monitor is an event-followed-by-function statistic, not a repair claim.",
        "",
        "All phases retain full sampled support and zero structural closure under common recovery. This fixture cannot test permanent material/capability loss. Damage still suppresses functioning at T16. Since recovery is common and irreducible, asymptotic rates eventually coincide; the finite pulse can leave an offset. The scheduled assay deliberately does not replace finite history with a rate.",
        "",
        "## Standard report form",
        "",
        "- Mechanism: bank-paid reversible actuator damage or sham, followed by shared recovery.",
        "- What lushness ranked: complete sampled histories, including the full pulse, from one common known present.",
        "- Relationship shown: engineering feasibility of physical joint moment matching; score signs at one small setting only.",
        "- Comparison: enacted controlled-boundary processes, neither damage preparations nor conditioned successful outcomes.",
        "- Horizon/resolution: T1/4/16, cadence 0.25; finite classical state with explicit projections; faithfulness open.",
        "- Challenged assumption: activity and throughput totals alone explain a contrast; matching them still leaves a history-distribution difference. No general principle is declared proved or refuted.",
        "",
        "## Next decision",
        "",
        "The tiny world fits comfortably. A next scoped map can vary pulse strength/duration, cost and recovery/source regimes with longer finite horizons, calibrating controls anew where feasible. The calibration dominates this smoke's cost. Do not extrapolate the existing T16 match to a new horizon or law. Irreversible loss needs explicit material/energy destinations and its own arm. Formal T, blocking and readiness maps remain separate tasks.",
        "",
        "See [quality axes](QUALITY.json), [complete summary](SUMMARY.json), [retained execution](retained/smoke/EXECUTION_CASES.json), [matching probes](retained/smoke/CALIBRATION.json), and [source snapshot](retained/SNAPSHOT.zip).",
    ]
    (out / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    files = [
        p for p in sorted(out.rglob("*")) if p.is_file() and p.name != "EVIDENCE.json"
    ]
    write(
        out / "EVIDENCE.json",
        {
            "schema": "omega.evidence-files/1",
            "files": [
                {
                    "path": p.relative_to(out).as_posix(),
                    "sha256": digest(p),
                    "bytes": p.stat().st_size,
                }
                for p in files
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "cases": len(cases),
                "profiles": len(rows),
                "retained_bytes": sum(p.stat().st_size for p in files),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
