"""Retain all J2 outcomes, including a physically gated non-run of histories."""

import argparse
import json
import shutil
from hashlib import sha256
from pathlib import Path

from restore_research_snapshot import write_archive

ROOT = Path(__file__).resolve().parents[1]


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def write(p, v):
    Path(p).write_text(
        json.dumps(v, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-dir", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    a = p.parse_args()
    run = a.run_dir.resolve()
    out = a.out_dir.resolve()
    if (
        out.exists()
        or not run.is_relative_to(ROOT / "runs")
        or not out.is_relative_to(ROOT / "research/platform/engineering")
    ):
        raise ValueError("Fresh engineering output and ignored source run required")
    manifest = read(run / "frozen/MANIFEST.json")
    _plan = read(run / "PLAN.json")
    receipt = read(run / "RECEIPT.json")
    if sha256((run / "PLAN.json").read_bytes()).hexdigest() != manifest["plan_sha256"]:
        raise ValueError("Plan changed")
    files = {
        r["path"]: (run / "frozen" / r["path"]).read_bytes() for r in manifest["files"]
    }
    if any(
        sha256(files[r["path"]]).hexdigest() != r["sha256"] for r in manifest["files"]
    ):
        raise ValueError("Executed source changed")
    cal = (
        read(run / "physical/CALIBRATION.json")
        if (run / "physical/CALIBRATION.json").exists()
        else None
    )
    hist = (
        read(run / "history/RESULT.json")
        if (run / "history/RESULT.json").exists()
        else None
    )
    out.mkdir(parents=True)
    for n in ["PLAN.json", "RECEIPT.json"]:
        shutil.copyfile(run / n, out / n)
    write_archive(
        out / "SNAPSHOT.zip",
        files | {"MANIFEST.json": (run / "frozen/MANIFEST.json").read_bytes()},
    )
    for mode in ["physical", "history"]:
        if (run / mode).is_dir():
            (out / mode).mkdir()
            for path in (run / mode).iterdir():
                if not path.is_file():
                    continue
                if path.suffix == ".log":
                    text = (
                        path.read_text(encoding="utf-8")
                        .replace(str(ROOT), "<repo>")
                        .replace(ROOT.as_posix(), "<repo>")
                    )
                    (out / mode / path.name).write_text(text, encoding="utf-8")
                else:
                    shutil.copyfile(path, out / mode / path.name)
    rows = cal["all_physical_rows"] if cal else []
    status = cal["status"] if cal else "incomplete_physical_qualification"
    summary = {
        "status": status,
        "execution_status": receipt["status"],
        "physical_evaluations": len(rows),
        "state_counts": sorted({r["states"] for r in rows}),
        "history_computed": hist is not None,
        "history_status": receipt["stages"].get("history", {}),
        "plan_sha256": manifest["plan_sha256"],
        "new_source_grammar": "shared categorical carrier conformation code3 energy1.5; native rates.002 in all arms",
        "source_on_physical_qualified_evaluations": sum(
            r["qualified_source_fed_load"] for r in rows
        ),
        "max_first_law_residual": max(
            (abs(r["finite_T64"]["energy_residual"]) for r in rows), default=None
        ),
        "max_stationary_residual": max(
            (r["stationary_residual"] for r in rows), default=None
        ),
        "max_source_off_load_heat": max(
            (
                abs(v["stationary"]["net_heat"])
                for r in rows
                if not r["source_on"]
                for v in r["loads"].values()
            ),
            default=None,
        ),
        "physical_worker": receipt["stages"]["physical"],
        "scope": "One stipulated finite model/anchor and bounded physical search; no global infeasibility or ethical certificate",
    }
    table = ""
    remarks = "Physical qualification did not complete."
    if cal:
        summary.update(
            {
                "target": cal["target"]["stationary"],
                "selected": cal["best"]["stationary"],
                "parameters": cal["best"]["parameters"],
                "absolute_residuals": cal["absolute_residuals"],
                "scaled_residuals": cal["scaled_residuals"],
                "allowances": cal["allowances"],
                "selected_physical_qualified": cal["best"]["qualified_source_fed_load"],
                "solver": cal["solver"],
                "target_function": cal["target"]["function"],
                "selected_function": cal["best"]["function"],
            }
        )
        table = "|Stationary quantity|New productive target|Selected control|Relative mismatch|\n|---|---:|---:|---:|\n"
        for key in ["event_rate", "net_work_rate"]:
            target = cal["target"]["stationary"][key]
            actual = cal["best"]["stationary"][key]
            table += f"|{key}|{target:.12g}|{actual:.12g}|{100 * (actual - target) / target:+.4f}%|\n"
        remarks = {
            "qualified_joint_match": "A control qualifies at the two stationary tolerances; see the actual history stage below. Qualification alone is not a lushness ranking.",
            "joint_match_physical_qualification_failed": "Two moments match but physical payment qualification fails. No unqualified control is scored.",
            "no_joint_match_in_bounded_search": "No evaluated point matches both stationary moments within the .1% relative allowances. This two-start bounded search does not prove global infeasibility. No new lushness conclusion follows.",
        }[status]
    if hist:
        summary["history_rows"] = len(hist["rows"])
        summary["paired_checks"] = len(hist["paired_contracts"])
        headline = [
            r
            for r in hist["comparisons"]
            if r["source_on"] and r["control"] == "control" and r["cadence"] == 0.25
        ]
        htext = (
            "|Horizon|Productive minus joint control (bits)|\n|---|---:|\n"
            + "".join(f"|{r['horizon']}|{r['delta_bits']:+.9f}|\n" for r in headline)
        )
        htext += "\nAll cadences, full-prefix crossings, rates/biases, ending laws and source-off diagnostics are retained in history/RESULT.json. Source-off is not refitted or called jointly matched. Float64 diagnostics are not verified all-horizon certificates."
    elif cal and status == "qualified_joint_match":
        htext = "Physical qualification passed, but the history stage did not produce a completed RESULT.json. See the execution receipt for the actual stop/cap/error. No completed history comparison is claimed."
    else:
        htext = "**Not run:** no qualified joint match was available. No new log-lushness, stationary entropy rate, bias, cadence ordering or ending-law total is reported. These quantities are not zero; they were not computed. The conditional history path was not exercised by this scientific run."
    write(out / "SUMMARY.json", summary)
    report = f"""# J2 — shared-intermediate qualification-gated run

31 October 2026. The user's “Run it all and then push” authorizes this run
and publication. Prior reports retain their own delivery status. Physical
outcome: **{status}**; execution: **{receipt["status"]}**.

## Outcome

{remarks}

{table}

The new productive targets were recomputed. They are not the old 75-state
J targets, and a smaller residual here is not a replay or a direct improvement
of the old comparison. All arms now include a thermally active intermediate.

Selected parameters: `{cal["best"]["parameters"] if cal else None}`.
Selected physical payment gate: {cal["best"]["qualified_source_fed_load"] if cal else None}.
The detailed solver starts and every physical point remain in
[CALIBRATION.json](physical/CALIBRATION.json). Successful numerical termination
does not establish matching. A start stopped at its evaluation budget is
explicitly identified, not treated as proof that no solution exists.

## Actual history stage

{htext}

## Physical model

The same retained carrier has four conformations with integer codes0/1/2/3
and energies0/3/2/1.5. All arms share the additional native locked↔intermediate
and spent↔intermediate pairs at conductance .002, plus every old native bath,
basal unlocking/capture, construction and upkeep route. Temperature, source.08,
and root energy4.5 stay common. The source and bath histories remain unresolved.

The control ablates motif unlocking and adds bond-gated locked->intermediate
and intermediate->spent discharge. Each forward leg exports1.5 heat, changes
no bank and has zero direct work; each reverse consumes1.5 heat. Native
thermal motion remains when apparatus is absent. The intermediate is an
explicit energetic state with physical residence, not an event label or clock.
Physical faithfulness to a microscopic carrier remains an assumption.

This is a new common finite grammar, not a silent correction or a refinement
certificate for older evidence. Construction and maintenance retain R1's
known limitations. Captured energy and bath fluctuations both remain in the
ledger; no event class is removed from the score.

## Resources and limits

{len(rows)} physical evaluations; state counts{summary["state_counts"]};
{summary["source_on_physical_qualified_evaluations"]} evaluated source-on points
pass the physical payment gate, which is distinct from moment matching.
The physical worker took{receipt["stages"]["physical"]["wall_seconds"]:.2f}s,
peaked at{receipt["stages"]["physical"]["peak_job_bytes"] / 1024**2:.2f}MiB and
wrote{receipt["stages"]["physical"]["output_bytes"] / 1024**2:.2f}MiB, within
300s/1GiB/64MiB/132-evaluation caps. No parameter box, source strength or
desired sign was changed after examining outcomes.

Maximum finite first-law residual{summary["max_first_law_residual"]};
stationary residual{summary["max_stationary_residual"]}; source-off per-load
net heat residual{summary["max_source_off_load_heat"]}.

The source-on intermediate's stationary occupation and mean residence are
retained for every evaluated point, as are finite T64 occupation and exit
counts. Full source gross/returned/net work and per-leg refunds are retained.
Positive forward bills are never substituted for net consumption.

## Interpretation

This is a result about the construction and qualification of one comparator
family. No failed design guess becomes a theory failure, no unqualified point
becomes evidence for organization winning or losing, and no global
impossibility follows from the bounded search. The prior separate-moment
lushness results remain unchanged and keep their limitations.

See [MODEL_CARD.md](MODEL_CARD.md), [QUALITY.json](QUALITY.json),
[VALIDATION.json](VALIDATION.json), [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md)
and [REPRODUCE.md](REPRODUCE.md). Private manuscripts are not included.
"""
    (out / "REPORT.md").write_text(report, encoding="utf-8")
    (out / "MODEL_CARD.md").write_text(
        f"""# J2 — shared energetic intermediate

**Mechanism.** The common carrier gains a fourth conformation; control adds
two reversible apparatus-gated heat-release legs. Same material/root/source
within the expanded grammar; no independent register or free selector.

**Claim/test.** Simultaneous stationary physical activity/net-source-work
matching, before history scoring. {remarks}

{table}

**Horizon/grain.** Physical T64 accounting and stationary flows; fixed count
grain, actual state counts{summary["state_counts"]}. History stage:
{summary["history_status"]}. No claim of a finest faithful physical resolution.

**Matched/unmatched.** Common endowment/boundary/grammar; physical moments
only when actually qualified. Finite work, gross input and path laws are not
implied matched. This version changes the old background, so old targets
are not reused. Comparisons are between mechanism laws, not enacted choices.

**What was challenged.** Whether an explicit two-step dissipative route can
supply a qualified activity/work comparator. No desired lushness sign and
no thermodynamic-normalized replacement for lushness was introduced.
See REPORT.md and QUALITY.json for source, numerical and physical limits.
""",
        encoding="utf-8",
    )
    write(
        out / "QUALITY.json",
        {
            "numerical": "Complete finite float64 physical flows; energy, stationary and source-off checks, not verified rounding enclosures or global optimization",
            "resolution": "Common expanded count grain; no physical-resolution certification",
            "physical": "Explicit energetic carrier state, native reverses/common baths; stipulated kinetics and inherited R1 limitations; unresolved exterior histories",
            "claim_relevance": remarks,
            "history_computed": hist is not None,
        },
    )
    (out / "REPRODUCE.md").write_text(
        """# Reproducing J2

Restore SNAPSHOT.zip with scripts/restore_research_snapshot.py --archive
<snapshot> --out-dir runs/<fresh-name>/frozen; copy PLAN.json from this folder
to runs/<fresh-name>/PLAN.json. The current repository supervisor
scripts/run_j2_discharge.py run --out-dir runs/<fresh-name> dispatches the
exact restored workers, checks plan/source hashes and enforces process caps.
Check supervisor differences against the executed snapshot in a later checkout.
Do not directly bypass the GO gate. Restoration alone runs no science.

The physical plan and selected points are immutable. A history stage is
permitted only after actual joint qualification and its hash-bound physical
gate. The retained original run, including a gated non-run, is authoritative.
Do not substitute a later fit or latest source and call it the same run.
No private manuscript, dense kernel or sampled path is needed for restoration.
""",
        encoding="utf-8",
    )
    (out / "analysis").mkdir()
    shutil.copyfile(Path(__file__), out / "analysis/report_j2_discharge.py")
    executed = files["scripts/run_j2_discharge.py"]
    current = (ROOT / "scripts/run_j2_discharge.py").read_bytes()
    notes = f"""# Source versions and evidence boundary

Executed runner SHA256: {sha256(executed).hexdigest()}.
Current runner SHA256: {sha256(current).hexdigest()}.

After the physical outcome, the unexecuted conditional history path gained
a stricter independent physical preflight before scoring even the reference
arm. It does not change the model, plan, physical fit or retained numbers.
Three targeted tests check rejection of no-match, unpaid and tampered
calibrations without invoking a sampled kernel. No physical point or history
was rerun to improve a result. SNAPSHOT.zip retains the exact executed source;
the current tested implementation is a distinct source version.

Conditional scoring is not validated by claiming it ran in this study when
the physical qualification gate was closed. Check VALIDATION.json for the
actual tested scope. No current physical faithfulness or ethical certification
is inferred from unit tests.
"""
    (out / "IMPLEMENTATION_NOTES.md").write_text(notes, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": status,
                "history_computed": hist is not None,
                "retained": out.relative_to(ROOT).as_posix(),
            }
        )
    )


if __name__ == "__main__":
    main()
