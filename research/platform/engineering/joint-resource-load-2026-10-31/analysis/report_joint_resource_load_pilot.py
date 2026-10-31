"""Outcome-neutral retention/report for J's physical-only pilot."""

import argparse
import json
import shutil
from hashlib import sha256
from pathlib import Path

from restore_research_snapshot import write_archive

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    run, out = args.run_dir.resolve(), args.out_dir.resolve()
    if (
        out.exists()
        or not run.is_relative_to(ROOT / "runs")
        or not out.is_relative_to(ROOT / "research/platform/engineering")
    ):
        raise ValueError("Fresh engineering evidence folder and ignored run required")
    manifest = read(run / "frozen/MANIFEST.json")
    if sha256((run / "PLAN.json").read_bytes()).hexdigest() != manifest["plan_sha256"]:
        raise ValueError("Plan differs from frozen version")
    files = {
        r["path"]: (run / "frozen" / r["path"]).read_bytes() for r in manifest["files"]
    }
    if any(
        sha256(files[r["path"]]).hexdigest() != r["sha256"] for r in manifest["files"]
    ):
        raise ValueError("Source snapshot changed")
    receipt = read(run / "RECEIPT.json")
    calibration_path = run / "physical/CALIBRATION.json"
    calibration = read(calibration_path) if calibration_path.exists() else None
    progress = (
        read(run / "physical/PHYSICAL_MAP.json")
        if (run / "physical/PHYSICAL_MAP.json").exists()
        else {"rows": []}
    )
    rows = calibration["all_physical_rows"] if calibration else progress["rows"]
    completed = (
        receipt["status"] == "completed_physical_pilot" and calibration is not None
    )
    status = calibration["status"] if completed else "incomplete_physical_pilot"
    if calibration and (
        calibration["history_computed"] or calibration["history_permission"]
    ):
        raise ValueError(
            "Physical-only handoff cannot contain history permission/scoring"
        )
    out.mkdir(parents=True)
    for name in ["PLAN.json", "RECEIPT.json"]:
        shutil.copyfile(run / name, out / name)
    write_archive(
        out / "SNAPSHOT.zip",
        files | {"MANIFEST.json": (run / "frozen/MANIFEST.json").read_bytes()},
    )
    for path in (run / "physical").iterdir():
        if path.is_file():
            target = out / "physical" / path.name
            target.parent.mkdir(exist_ok=True)
            if path.suffix == ".log":
                text = (
                    path.read_text(encoding="utf-8")
                    .replace(str(ROOT), "<repo>")
                    .replace(ROOT.as_posix(), "<repo>")
                )
                target.write_text(text, encoding="utf-8")
            else:
                shutil.copyfile(path, target)
    source_on = [r for r in rows if r["kind"] == "control" and r["source_on"]]
    source_off = [r for r in rows if not r["source_on"]]
    summary = {
        "status": status,
        "engineering_complete": completed,
        "history_computed": False,
        "history_authorized": False,
        "plan_sha256": manifest["plan_sha256"],
        "calibration_sha256": sha256(calibration_path.read_bytes()).hexdigest()
        if calibration
        else None,
        "physical_evaluations": len(rows),
        "state_counts": sorted({r["states"] for r in rows}),
        "source_on_control_evaluations": len(source_on),
        "source_on_physical_qualified_evaluations": sum(
            r["qualified_source_fed_load"] for r in source_on
        ),
        "net_importer_evaluations": sum(
            any(v["stationary"]["net_heat"] < -1e-8 for v in r["loads"].values())
            for r in source_on
        ),
        "max_integrated_first_law_residual": max(
            (abs(r["finite_T64"]["energy_residual"]) for r in rows), default=None
        ),
        "max_stationary_residual": max(
            (r["stationary_residual"] for r in rows), default=None
        ),
        "max_source_off_load_heat": max(
            (
                abs(v["stationary"]["net_heat"])
                for r in source_off
                for v in r["loads"].values()
            ),
            default=None,
        ),
        "wall_seconds": receipt["worker"]["wall_seconds"],
        "peak_job_bytes": receipt["worker"]["peak_job_bytes"],
        "output_bytes": receipt["worker"]["output_bytes"],
        "cap_reason": receipt["worker"]["cap_reason"],
        "scope": "One fixed physical family/anchor, bounded search; no global infeasibility or lushness conclusion",
    }
    table = ""
    if calibration:
        target, best = calibration["target"], calibration["best"]
        summary.update(
            {
                "target": target["stationary"],
                "selected_parameters": best["parameters"],
                "selected": best["stationary"],
                "absolute_residuals": calibration["absolute_residuals"],
                "scaled_residuals": calibration["scaled_residuals"],
                "allowances": calibration["allowances"],
                "selected_physical_qualified": best["qualified_source_fed_load"],
                "solver": calibration["solver"],
                "sensitivity": calibration["sensitivity"],
                "target_in_sampled_moment_convex_hull": calibration[
                    "target_inside_sampled_moment_convex_hull"
                ],
            }
        )
        lines = [
            "|Stationary quantity|Productive target|Selected control|Absolute residual|Allowed absolute error|",
            "|---|---:|---:|---:|---:|",
        ]
        for key in ["event_rate", "net_work_rate"]:
            lines.append(
                f"|{key}|{target['stationary'][key]:.12g}|{best['stationary'][key]:.12g}|{calibration['absolute_residuals'][key]:+.12g}|{calibration['allowances'][key]:.12g}|"
            )
        table = "\n".join(lines)
    write(out / "SUMMARY.json", summary)
    conclusions = {
        "qualified_joint_match": "One evaluated control meets both stationary moment tolerances and the declared physical load gate. This authorizes no history run by itself.",
        "joint_match_physical_qualification_failed": "The named moments match in one evaluated control, but its physical payment gate does not. Do not history-score or describe it as a qualified paid comparator.",
        "no_joint_match_in_bounded_search": "No evaluated control meets both moment tolerances. This bounded one-start search does not establish impossibility elsewhere in the same family, still less in other families. No history scoring follows.",
        "incomplete_physical_pilot": "The physical pilot stopped incomplete. Retain its rows and cap/error receipt; no joint-match conclusion or history scoring is available.",
    }
    selected_text = ""
    if calibration:
        best = calibration["best"]
        heats = ", ".join(
            f"{k}: {v['stationary']['net_heat']:.12g}" for k, v in best["loads"].items()
        )
        selected_text = f"""
Selected conductances: `{best["parameters"]}`. Per-route stationary net heat
(energy/time): {heats}. Selected physical payment qualification:
**{best["qualified_source_fed_load"]}**. Finite T64 and gross/refunded flows are
retained in full, including source-off at these unchanged conductances.

The solver's termination is `{calibration["solver"]["termination"]}`; solver
success is not the simultaneous physical-match criterion. The target is
inside the convex hull of sampled moment pairs:
**{calibration["target_inside_sampled_moment_convex_hull"]}**. This is not proof
that one static physical model attains it. A random mixture or switching among
laws is not silently substituted for a single control: a physical selector
would need its own state, energy accounting and changed continuation law.

The local dimensionless stationary sensitivity condition number is
{calibration["sensitivity"]["condition_number"]}; its aligned affine-generator
identity residual is {calibration["sensitivity"]["aligned_affine_generator_residual"]:.4g}.
The responses are locally distinct, but this does not prove global feasibility
or optimality of the selected point. Matrices were aligned by physical states
before differencing; no new sensitivity probe models were needed.
"""
    boundary_comment = ""
    if calibration and status == "no_joint_match_in_bounded_search":
        relative = {
            k: calibration["absolute_residuals"][k]
            / calibration["target"]["stationary"][k]
            for k in ["event_rate", "net_work_rate"]
        }
        boundary_comment = f"""
## Interpretation of the physical boundary

Selected event-rate mismatch: {100 * relative["event_rate"]:+.2f}%; selected
net-work mismatch: {100 * relative["net_work_rate"]:+.2f}%, against the frozen
.1% relative allowances. The selected conductances and each route's heat
above make negligible or importing routes visible. No evaluated point met
both moment tolerances. This is not a failed lushness prediction: no lushness
comparison was run.

Adjustability of each moment somewhere does not guarantee simultaneous
attainability in one static physical model. A local full-rank response and
the sampled convex-hull diagnostic do not settle this nonlinear family's
global moment surface. This one-start bounded search supplies no global
impossibility proof. Before another search, review energy per event and the
physical attainable surface. Any multistep load or selector would be a new
costed construction, not a silent extra knob in this completed pilot.
"""
    report = f"""# J — joint resource-load physical pilot

31 October 2026. Completed locally at the user's “Ok go next”; no commit,
push or manuscript application. Engineering status: **{status}**.

## Outcome

{conclusions[status]}

{table}

{selected_text}

{boundary_comment}

## Physical construction and scope

The fixed source-.08 R1 anchor retains its built root,75-state grammar,
Hamiltonian, temperature, material, baths, basal routes and construction/capture
costs. The control ablates only motif unlocking and adds two bond-gated
resource-to-heat channels: locked1->spent0 releases3 energy; usable2->spent0
releases2. Both native reverses remain. There is no new bank, register,
constituent or source. Original native rules are checked unchanged, loads
change only the carrier, and their individual bills/refunds stay visible.
Parallel outcomes aggregate normally; event labels are not added futures.

The two parameters were calibrated only on stationary event count and net
external work. Gross work, finite T64 totals, occupancy and path laws are
not jointly matched. Direct dissipation does not imply absence of indirect
access effects. No history entropy, entropy rate, bias or desired ranking
entered the objective. Original single-load, rotor and manuscript-audit
records are unchanged. No control family, common noise or source was retuned
after seeing the outcome.

## Budget and validation

{len(rows)} compiled physical evaluations; state counts {summary["state_counts"]}.
Source-on control evaluations {len(source_on)}, of which
{summary["source_on_physical_qualified_evaluations"]} meet the physical payment
gate; net importer count {summary["net_importer_evaluations"]}. Physical
qualification alone is not moment matching.

Runtime {summary["wall_seconds"]:.2f}s; peak process-tree memory
{summary["peak_job_bytes"] / 1024**2:.2f}MiB; worker output
{summary["output_bytes"] / 1024**2:.2f}MiB. Declared caps300s/1GiB/64MiB,
132 evaluations and 200 states; cap reason {summary["cap_reason"]}.
Integrated first-law residual {summary["max_integrated_first_law_residual"]};
stationary residual {summary["max_stationary_residual"]}; source-off load
net heat residual {summary["max_source_off_load_heat"]}.

The frozen plan is {manifest["plan_sha256"]}. See
[CALIBRATION.json](physical/CALIBRATION.json), [SUMMARY.json](SUMMARY.json),
[QUALITY.json](QUALITY.json), [RECEIPT.json](RECEIPT.json),
[VALIDATION.json](VALIDATION.json) and [REPRODUCE.md](REPRODUCE.md).
All grid/fit points and the source snapshot are retained. No physical grain
faithfulness, chemical closure, global impossibility or ethical result is
claimed. Stop at this physical report; no history stage was executed.
"""
    # Incomplete runs need not have a calibration file.
    if not calibration:
        report = report.replace("[CALIBRATION.json](physical/CALIBRATION.json),", "")
    (out / "REPORT.md").write_text(report, encoding="utf-8")
    write(
        out / "QUALITY.json",
        {
            "numerical": "Finite float64 physical solves, per-event/finite/stationary energy and equilibrium checks; no rigorous rounding enclosure",
            "resolution": "No history/resolution comparison at this stage; original fixed count grammar only",
            "physical": "Declared reversible apparatus-gated dissipation; retained-unit scope, unresolved source/bath histories and original R1 maintenance limitations",
            "claim_relevance": conclusions[status],
            "history_computed": False,
        },
    )
    (out / "REPRODUCE.md").write_text(
        """# Reproducing J's physical pilot

Restore SNAPSHOT.zip with scripts/restore_research_snapshot.py --archive
<SNAPSHOT.zip> --out-dir runs/<fresh-name>/frozen. Copy PLAN.json from this
evidence folder to runs/<fresh-name>/PLAN.json, preserving the manifest-bound
hash. Run the repository supervisor with python scripts/joint_resource_load_pilot.py
run --out-dir runs/<fresh-name>. It dispatches the exact restored frozen worker.
The Windows process-tree cap and GO gate are required. Do not call the worker
directly. Verify the supervisor against its retained source in a later checkout.
Restoration alone executes no physical calculation.

The snapshot contains INPUTS.json, all native engine sources and the exact
pilot script/spec/tests; no private manuscripts or trajectory caches. Source
hashes and plan are checked before dispatch. The worker repeats physics only,
up to the retained fixed budget; no history-scoring mode exists. Floating
solver details may vary by numerical library: compare residuals, model hashes,
gates and stopping scope rather than invent bit-exact fitting guarantees.
Use the retained CALIBRATION/PHYSICAL_MAP for the original evaluated points.
""",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": status,
                "retained": out.relative_to(ROOT).as_posix(),
                "history_computed": False,
            }
        )
    )


if __name__ == "__main__":
    main()
