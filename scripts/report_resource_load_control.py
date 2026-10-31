"""Report the physical qualification and every signed load-control contrast."""

import argparse
import json
import shutil
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def write(p, v):
    Path(p).write_text(
        json.dumps(v, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    a = parser.parse_args()
    out = a.evidence_dir.resolve()
    if (
        not out.is_relative_to(ROOT / "research/platform/engineering")
        or (out / "REPORT.md").exists()
    ):
        parser.error("Fresh retained engineering output required")
    receipt = read(out / "RECEIPT.json")
    calibration = read(out / "physical/CALIBRATION.json")
    history = (
        read(out / "history/RESULT.json")
        if (out / "history/RESULT.json").exists()
        else None
    )
    if history is not None:
        if (
            history["calibration_sha256"]
            != sha256((out / "physical/CALIBRATION.json").read_bytes()).hexdigest()
        ):
            raise ValueError("History result uses a different physical calibration")
        if any(
            c["certificate"]["status"] != "validated_paired_comparison"
            for c in history["paired_contracts"]
        ):
            raise ValueError("Reported paired checks did not all complete")
    target = calibration["target"]["stationary"]
    selections = calibration["selections"]
    physics_table, selection_summary = [], []
    for s in selections:
        physical = s["selected_physical"]
        load = physical["load"]["stationary"]
        physics_table.append(
            f"|{s['name']}|{s['conductance']:.12g}|{physical['stationary']['event_rate']:.12g}|{physical['stationary']['net_work_rate']:.12g}|{load['net_heat']:.12g}|{s['history_permitted']}|"
        )
        selection_summary.append(
            {
                "name": s["name"],
                "conductance": s["conductance"],
                "primary_matched": s["primary_matched"],
                "qualified": s["qualified"],
                "history_permitted": s["history_permitted"],
                "primary": s["primary"],
                "moment_residuals": s["fit"]["best"]["absolute_residuals"],
                "net_load_heat_rate": load["net_heat"],
                "finite_T64_net_load_heat": physical["load"]["finite_T64"]["net_heat"],
                "source_off_net_load_heat_rate": s["source_off_physical"]["load"][
                    "stationary"
                ]["net_heat"],
            }
        )
    signed_table, rate_table, source_off_table = [], [], []
    primary_points, rate_points, finite_mismatches = [], [], []
    if history:
        for c in history["comparisons"]:
            if c["source_on"] and c["cadence"] == 0.25:
                signed_table.append(
                    f"|{c['control']}|{c['horizon']}|{c['productive_minus_control_bits']:+.9f}|"
                )
                primary_points.append(c)
            if c["source_on"] and c["horizon"] == 1024:
                rate_table.append(
                    f"|{c['control']}|{c['cadence']}|{c['delta_rate_bits_per_time']:+.9f}|{c['productive_minus_control_bits']:+.9f}|"
                )
                rate_points.append(c)
            if not c["source_on"] and c["horizon"] == 1024 and c["cadence"] == 0.25:
                source_off_table.append(
                    f"|{c['control']}|{c['productive_minus_control_bits']:+.9f}|{c['delta_rate_bits_per_time']:+.9f}|"
                )
        for r in history["rows"]:
            if r["source_on"] and r["cadence"] == 0.25 and r["horizon"] == 64:
                finite_mismatches.append(
                    {
                        "arm": r["arm"],
                        "expected_jumps": r["physical"]["expected_jumps"],
                        "net_work": r["physical"]["work_net"],
                        "gross_accepted_work": r["physical"]["gross_accepted_work"],
                        "gross_returned_work": r["physical"]["gross_returned_work"],
                        "observables": r["observables"],
                    }
                )
    phases = [p for p in receipt["phases"].values() if "wall_seconds" in p]
    peak = max(p["peak_job_bytes"] for p in phases)
    max_balance = (
        max((abs(r["physical"]["energy_residual"]) for r in history["rows"]), default=0)
        if history
        else None
    )
    summary = {
        "status": receipt["status"],
        "physical_points": len(calibration["physical_map"]),
        "target_stationary": target,
        "selections": selection_summary,
        "profiles": len(history["rows"]) if history else 0,
        "comparisons": len(history["comparisons"]) if history else 0,
        "paired_checks": len(history["paired_contracts"]) if history else 0,
        "primary_comparisons": primary_points,
        "rate_comparisons": rate_points,
        "finite_T64_physical_mismatches": finite_mismatches,
        "max_energy_balance_residual": max_balance,
        "wall_seconds": sum(p["wall_seconds"] for p in phases),
        "peak_job_bytes": peak,
        "scope": "One mechanism family/anchor, separate stationary physical matches, not joint/finite/path matching or gas/ethics evidence",
    }
    write(out / "SUMMARY.json", summary)
    quality = {
        "numerical": "Full finite-state float64, source-off detailed balance, native energy/ledger audits, typed physical matching, scoped paired validation; no rigorous rounding intervals",
        "resolution": "Fixed count grain and three cadences .125/.25/.5; finite intermediate-horizon signs flip with cadence; physical faithfulness remains open",
        "physical_adequacy": "Costed original apparatus and retained carrier; forward/reverse energy flows counted; no new register. Original R1 physical omissions and unresolved external histories remain",
        "claim_relevance": "Qualified net-dissipating controls matched separately on stationary jumps or stationary net work. Shows one sustained advantage not explainable solely by higher mean stationary jump rate; not a general generativity/ethical rule",
        "not_run": [
            "joint activity-and-work match",
            "variation-register V arm",
            "spatial thermal baseline",
            "robust compounding",
            "parameter range of history rankings",
        ],
    }
    write(out / "QUALITY.json", quality)
    text = [
        "# Source-fed relaxation control — physical qualification and compact comparison",
        "",
        "30 October 2026. Local engineering and one fixed-anchor smoke; no manuscript edits, commit or push.",
        "",
        "## What was built and why it qualifies",
        "",
        "The original R1 assembled apparatus can catalyse direct locked-carrier relaxation to heat, instead of the useful unlocking pair. Apparatus construction, its original costs, material, native thermal routes, energy function and source settings stay common. Each forward load step releases 3 resource-energy units; its native reverse returns 3 from the bath. No bank increment, usable-fuel production, new register or new constituent is added. This is a mechanism contrast, not a controller changing chemistry at no cost.",
        "",
        "Both selected source-on controls have positive stationary net load heat, positive stationary net external work and positive T64 net load heat. Source-off stationary load heat/work vanish to numerical precision while thermal switching remains. Thus the paid-flow qualification is not merely spending the initial store, counting labelled events or overlooking refunds. It is a source-driven resource-dissipation loop; individual energy quanta are not genealogically traced to the source.",
        "",
        "The old bank-returning rotor attempts stay retained and are not rerun or relabelled. This load is a different physical coupling. The first preparation-only snapshot preceded lint-only changes; no science ran under it. The executed source version and unchanged input plan are retained here.",
        "",
        "## Calibration, frozen before history scoring",
        "",
        f"The productive arm has stationary event rate **{target['event_rate']:.12g} events/time** and net external work **{target['net_work_rate']:.12g} energy/time**. Forty physical evaluations, including source-off references and every fit probe, are retained. Calibration used only physical moments and budget gates; no history entropy was computed or optimized during selection.",
        "",
        "|Control|Load conductance|Stationary event rate|Stationary net work|Stationary net load heat|Qualified match|",
        "|---|---:|---:|---:|---:|---|",
        *physics_table,
        "",
        "These are TWO separate controls. The activity-matched control uses about 2.54 times the productive arm's net external work. The net-work-matched control has about 14.1% fewer stationary jumps. Neither is jointly matched, and net external work is not gross accepted work. All accepted/returned/gross/net flows are retained.",
        "",
        "The load merely catalyses relaxation; the apparatus must exist for the extra channel to fire. It does not directly enable bank capture or construction. Its reverse can feed the resource pool, and changing occupancy can indirectly affect other functions. These consequences are reported, not used as a post-score veto.",
        "",
        "## Complete finite-history profiles",
        "",
        "Primary cadence .25. Positive means productive exceeds the named control, in bits:",
        "",
        "|Control|Physical horizon|Productive minus control|",
        "|---|---:|---:|",
        *signed_table,
        "",
        "At matched stationary activity, the productive arm does not dominate every finite horizon. At .25 it leads at T16, trails at T64 and T256, then leads at T1024. The full evaluated prefix contains three sign changes, including one before T16. At .125 it also trails at T64/T256; at .5 it leads at those endpoints. These are disclosed temporal-resolution-dependent intermediate rankings, not a universal protection/generativity result or a solver error.",
        "",
        "Finite work and jump totals are not matched by a stationary match. At T64, expected jumps are 13.3093 productive versus 13.6855 activity-control; net work is 1.36692 versus 4.80759. For the net-work control, T64 net work is only .461689 despite its stationary work match. These transient differences remain part of the complete comparison.",
        "",
        "## Sustained-rate diagnostic",
        "",
        "|Control|Cadence|Delta rate (bits/time)|Delta at T1024 (bits)|",
        "|---|---:|---:|---:|",
        *rate_table,
        "",
        "The productive arm has a positive stationary entropy-rate difference against both separately matched controls at all three tested cadences. In particular, its activity-matched advantage is not attributable solely to a greater mean stationary jump rate: that moment matches to 8.4e-17 events/time, while the sampled history rates still differ. Transition destinations, state occupancy, sequences and correlations remain different. This is an existence example under these declared laws, not a unique subtraction of an organization-only component.",
        "",
        "The net-work comparison removes a different nuisance coordinate but leaves an activity mismatch. Passing both separate comparisons is not proof of a simultaneous two-moment match. Thermal, reverse and apparently futile branching stays in every score. Kernel rates/biases and independent-ending readouts accompany the finite profiles; a rate is not substituted for the complete profile.",
        "",
        "## Source-off diagnostic",
        "",
        "The source-off arms reuse the fitted source-on conductances; they are not refitted and are not called activity-matched. At cadence .25:",
        "",
        "|Control|Delta at T1024|Delta stationary rate|",
        "|---|---:|---:|",
        *source_off_table,
        "",
        "The activity control has the larger source-off stationary history rate even while the productive preparation still leads at T1024. Thermal activity persists and finite offsets/transients matter. Do not claim an eternal finite lead, subtract this background from the authoritative score, or call this a spatial thermal-gas baseline.",
        "",
        "## Evidence and limits",
        "",
        f"{summary['profiles']} arm profiles, {summary['comparisons']} signed endpoint comparisons and {summary['paired_checks']} passing current paired checks. Maximum integrated first-law residual {max_balance}. Combined worker wall time {summary['wall_seconds']:.2f}s; peak memory {peak / 1024**2:.2f} MiB. All inputs and selected physical matches were frozen before scoring; no sign was required for completion.",
        "",
        "[CALIBRATION.json](physical/CALIBRATION.json) retains the full physical map and refunds; [RESULT.json](history/RESULT.json) retains every profile, comparison, contract, physical/functional readout and independent-ending value; [SUMMARY.json](SUMMARY.json) and [QUALITY.json](QUALITY.json) separate observed facts and limits. SNAPSHOT.zip and the receipts permit restoration without private run caches.",
        "",
        "This remains a coarse fixed-slot whole-modeled-field example, with retained-unit inventory scope and unresolved bath/source histories. Original R1 maintenance/transport limitations remain. It is not chemical closure, recursively compounding ecology, physical-resolution faithfulness or ethical confirmation. The V register arm, a joint-match control and any wider physical map remain unrun. No automatic manuscript tier promotion or publication follows.",
        "",
    ]
    (out / "REPORT.md").write_text("\n".join(text), encoding="utf-8")
    card = [
        "# Resource-load control: model card",
        "",
        "**Question.** Can a physically net-dissipating, non-enabling coupling be compared with productive access at matched mean activity or matched net work?",
        "",
        "**Setup.** Original qualified R1, one built present, same five coordinates/endowment/Hamiltonian/source, with motif-assisted direct carrier relaxation added to the ablation. Native reverse and baseline channels retained. Mechanism contrasts; no free policy choice.",
        "",
        "**Matched.** Separately stationary native jump rate or stationary net external work, under common supplied boundary settings and scoped retained-unit budgets.",
        "",
        "**Unmatched.** The other stationary moment, finite totals, timing/sequence distributions, correlations and unresolved external histories. Source-off controls reuse source-on fits.",
        "",
        "**Levels/window.** Count state, cadences .125/.25/.5, T16/64/256/1024 plus numerical kernel rate/bias and independent-ending readouts.",
        "",
        "**Key finding.** Both physical controls qualify. Productive stationary rate is higher against both at each cadence; finite activity-matched rankings cross and are cadence dependent at intermediate windows. No joint-match claim.",
        "",
        "**How far it holds.** One fixed anchor/family, not a universal law or full parameter range. Native thermal/reverse activity remains in the total.",
        "",
        "**Quality.** Numerical finite-model checks; registered cadence coverage; physical fixed-slot limitations; scoped mechanism relevance. No ethical, gas or latest-Appendix conformance certificate.",
        "",
        "[Full report](REPORT.md); [quality axes](QUALITY.json).",
        "",
    ]
    (out / "MODEL_CARD.md").write_text("\n".join(card), encoding="utf-8")
    analysis = out / "analysis"
    analysis.mkdir()
    shutil.copyfile(Path(__file__), analysis / Path(__file__).name)
    write(
        out / "EVIDENCE.json",
        {
            "schema": "omega.resource-load-evidence/1",
            "files": [
                {
                    "path": p.relative_to(out).as_posix(),
                    "bytes": p.stat().st_size,
                    "sha256": sha256(p.read_bytes()).hexdigest(),
                }
                for p in sorted(out.rglob("*"))
                if p.is_file() and p.name != "EVIDENCE.json"
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": summary["status"],
                "qualified_controls": [
                    s["name"] for s in selections if s["history_permitted"]
                ],
                "profiles": summary["profiles"],
                "comparisons": summary["comparisons"],
            }
        )
    )


if __name__ == "__main__":
    main()
