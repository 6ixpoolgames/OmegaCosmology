"""Build signed, scope-qualified cards from the fixed P0/T replay artifacts."""

import argparse
import json
import shutil
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def write(p, value):
    Path(p).write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def signed_bounds(audit, horizon):
    coefficients = audit["contrast"]["coefficients"]
    result = {}
    for law, arm in audit["arms"].items():
        row = next(r for r in arm["projected_histories"] if r["horizon"] == horizon)
        for scope, values in row["bounds"].items():
            result.setdefault(scope, [0.0, 0.0])
            c = coefficients[law]
            lo, hi = values["lower_bits"], values["upper_bits"]
            result[scope][0] += c * (lo if c > 0 else hi)
            result[scope][1] += c * (hi if c > 0 else lo)
    return result


def ending_comparisons(audit):
    coefficients = audit["contrast"]["coefficients"]
    geometric = []
    for k, duration in enumerate((10, 100, 1000, 10000)):
        geometric.append(
            {
                "mean_physical_duration": duration,
                "delta_expected_log_lushness_bits": sum(
                    c * audit["arms"][law]["geometric_endings"][k]["ell_expected_bits"]
                    for law, c in coefficients.items()
                ),
            }
        )
    uniform = sum(
        c * audit["arms"][law]["uniform_ending"]["ell_expected_bits"]
        for law, c in coefficients.items()
    )
    return {
        "cadence": audit["cadence"],
        "independent_geometric": geometric,
        "independent_uniform": {
            "max_steps": audit["contrast"]["evaluated_steps"],
            "delta_expected_log_lushness_bits": uniform,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    a = parser.parse_args()
    out = a.evidence_dir.resolve()
    if (
        not out.is_relative_to(ROOT / "research/platform/engineering")
        or (out / "REPORT.md").exists()
    ):
        parser.error("Existing fresh retained evidence folder without report required")
    plan, receipt = read(out / "PLAN.json"), read(out / "BATCH_RECEIPT.json")
    audits = [
        read(p) for p in sorted((out / "retained").glob("*__audit__*/AUDIT.json"))
    ]
    reference_path = out / "retained/T/REFERENCES.json"
    references = read(reference_path) if reference_path.exists() else None
    limits = {
        "R1": "Fixed-slot access/reconstruction. Descriptive legacy material declaration is not an executable inventory. Unmatched realized activity/work; no thermal or ethical comparison.",
        "R2": "Original capacity-use law, not its repaired successors. Sham removes loaded-bank states; a matched ambient-state mapping is absent. Original maintenance/spill/ancestry audit limits remain.",
        "E1": "Coupled catalytic mechanism from an unassembled preparation. Original selected configuration exists only at cadence .25. Projected donor intervals are not made rigorous by replay.",
        "S3": "Occupied one-way versus local assistance; this reproduces the early donor/whole opposition, not enacted or irreversible damage. Long-run donor signs can remain unresolved.",
        "S4": "Original kinetic warning model, with its known weak-sensor limitation. Reproducing TX minus T0 does not establish useful information or suffering.",
        "S4b": "Paid-warning four-arm interaction, not a pure information attribution. Preserve the separate blocked-effort contrary result. No felt-valence or enduring suffering claim.",
    }
    rows, cards = [], []
    original_rows, native_max, independent_max, physics_max, projection_max = (
        0,
        0.0,
        0.0,
        0.0,
        0.0,
    )
    peak = max(
        (j["receipt"].get("peak_job_bytes") or 0 for j in receipt["jobs"]), default=0
    )
    for study in plan["studies"]:
        cases = [v for v in audits if v["study"] == study["id"]]
        primary = next((v for v in cases if v["cadence"] == 0.25), None)
        profiles = []
        for audit in cases:
            for point in audit["contrast"]["original_horizons"]:
                profiles.append(
                    {
                        "cadence": audit["cadence"],
                        **point,
                        "part_intervals_bits": signed_bounds(audit, point["horizon"]),
                    }
                )
            for arm in audit["arms"].values():
                original_rows += arm["native_rows_replayed"]
                native_max = max(native_max, arm["native_reproduction_max_bits"])
                independent_max = max(
                    independent_max, arm["independent_profile_reproduction_max_bits"]
                )
                projection_max = max(
                    projection_max, arm["native_projection_reproduction_max_bits"]
                )
                physics_max = max(
                    physics_max, *(abs(v["energy_residual"]) for v in arm["physical"])
                )
        status = (
            "reproduced_selected_contrast"
            if len(cases) == len(study["cadences"])
            else "incomplete_selected_verification"
        )
        certificates = [v for case in cases for v in case["paired_contracts"]]
        reasons = sorted({v.get("reason", v["status"]) for v in certificates})
        summary = {
            "study": study["id"],
            "status": status,
            "cadences": [v["cadence"] for v in cases],
            "paired_contracts": certificates,
            "profile_map": profiles,
            "limits": limits[study["id"]],
            "analytical_tail": [
                {
                    "cadence": v["cadence"],
                    **{
                        k: v["contrast"][k]
                        for k in (
                            "delta_rate_bits_per_time",
                            "delta_bias_offset_bits",
                            "remainder_bound_bits",
                            "line_crossing_steps",
                            "eventual_sign_bound_from_step",
                            "evaluated_steps",
                            "cap_limited",
                            "observed_crossings",
                            "classification",
                        )
                    },
                }
                for v in cases
            ],
            "ending_law_comparisons": [ending_comparisons(v) for v in cases],
        }
        rows.append(summary)
        if primary:
            delta64 = next(
                (
                    v["delta_bits"]
                    for v in primary["contrast"]["original_horizons"]
                    if v["horizon"] == 64
                ),
                None,
            )
            delta1024 = next(
                (
                    v["delta_bits"]
                    for v in primary["contrast"]["original_horizons"]
                    if v["horizon"] == 1024
                ),
                None,
            )
            cards.append(
                f"|{study['id']}|{delta64:+.9f}|{delta1024:+.9f}|{primary['contrast']['delta_rate_bits_per_time']:+.9f}|{'; '.join(reasons)}|"
            )
        text = [
            f"# {study['id']} selected replay card",
            "",
            "30 October 2026. Literal original source replay plus separate current-platform audit.",
            "",
            f"**Question and setup.** Reproduce `{study['preparation']}` under the frozen laws "
            + ", ".join(f"`{n}`" for n in study["laws"])
            + ".",
            "",
            "**Comparison.** A mechanism contrast, or a difference of two mechanism contrasts for S4b. No act was substituted for a preparation and no new controller chose these mechanisms.",
            "",
            f"**Status.** {status}. Original cadences: {study['cadences']}; original horizons: {study['horizons']}.",
            "",
            "**Matched/unmatched.** Original physical inputs retained. The paired-validator outcomes below concern the current executable contract; they do not erase numerical reproduction or establish physical faithfulness.",
            "",
            *["- " + reason for reason in reasons],
            "",
            "**Findings.** Signed full profile and projected intervals are retained in [SUMMARY.json](SUMMARY.json), alongside all original result bytes. No whole-parameter-map replication follows.",
            "",
            "**Limits.** " + limits[study["id"]],
            "",
            "| Evidence axis | Assessment |",
            "|---|---|",
            "|Numerical|Native finite profiles and current independent propagation/Poisson accounting agree within frozen float64 tolerances; not interval arithmetic.|",
            "|Resolution|Only the original selected cadences, one declared count grain. Physical faithfulness remains open.|",
            "|Physical adequacy|Native generator/event energy and integrated work/heat checked. Legacy material inventories remain unverified where declared descriptively; exterior histories unresolved.|",
            "|Claim relevance|Selected mechanism only; no general ethical conclusion or automatic manuscript tier promotion.|",
            "",
        ]
        (out / (study["id"] + "_CARD.md")).write_text("\n".join(text), encoding="utf-8")
    summary = {
        "status": receipt["status"],
        "studies": rows,
        "native_replayed_rows": original_rows,
        "headline_contrast_rows": sum(len(v["profile_map"]) for v in rows),
        "native_history_max_difference_bits": native_max,
        "current_history_max_difference_bits": independent_max,
        "native_projection_max_difference_bits": projection_max,
        "integrated_first_law_max_residual": physics_max,
        "jobs": len(receipt["jobs"]),
        "batch_wall_seconds": receipt["wall_seconds"],
        "peak_job_bytes": peak,
        "T_status": references["status"] if references else "missing",
    }
    write(out / "SUMMARY.json", summary)
    report = [
        "# P0/T representative verification — results",
        "",
        "30 October 2026. Completed local verification; no manuscript edits, commit or push.",
        "",
        f"**Execution: {receipt['status']}.** Six fixed study contrasts; {len(audits)} current-audit cases and {sum(j['mode'] == 'native' for j in receipt['jobs'])} original native cases. {original_rows} native arm/preparation/horizon rows replayed; {summary['headline_contrast_rows']} selected signed contrast rows. These are correlated profiles, not independent experiments.",
        "",
        f"Maximum native history difference: **{native_max:.3g} bits**. Independent current history difference: **{independent_max:.3g} bits**. Native projected-bound difference: **{projection_max:.3g} bits**. Integrated first-law residual: **{physics_max:.3g}**.",
        "",
        "## What survives, and what does not get certified",
        "",
        "The selected historical numerical results reproduce. This does not make their literal old input declarations pass today's paired validator. Numerical reproduction and paired-contract applicability remain separate statuses. No inventories, state-space mappings, boundaries or costs were changed to secure a certificate.",
        "",
        "These are reproductions and cross-checks within the same research environment, not replications by an independent research group. Original native sources and the current auditor are retained separately.",
        "",
        "Primary cadence .25; finite differences in bits, rates in bits per physical time:",
        "",
        "|Study|Delta at T64|Delta at T1024|Delta stationary rate|Current paired-contract reason/status|",
        "|---|---:|---:|---:|---|",
        *cards,
        "",
        "R2's useful-capacity and sham worlds have different allowed bank states: its sham forbids bank >=5 even when a store is built. That was part of the original scientific contrast. The current matched-grammar validator requires an explicit ambient-state mapping that this old input does not supply. Other literal-input failures involving descriptive material declarations remain unaltered. These are applicability boundaries, not reversals of the numerical findings.",
        "",
        "## Profiles, rates and ending laws",
        "",
        "The S4b four-arm interaction has TWO observed sign changes at every tested cadence. At cadence .25 it changes positive-to-negative between physical times 11 and 11.25, then negative-to-positive between 193 and 193.25. Its original T16/T64 values are negative and T256/T1024 values positive. The newly resolved very-short-window sign does not contradict those original endpoints. No unique repayment time is inferred from rate and bias alone.",
        "",
        "R2's conservative tail threshold lies beyond the 65,536-step window at cadence .125. At .25/.5 the threshold is reached, but the requested threefold overshoot is cap-limited. Preserve these distinctions rather than declaring a tail violation or increasing the scope to find a sign.",
        "",
        "Each arm includes a log-spaced profile, numerical kernel rate and normalized bias, exact-in-real-arithmetic Poisson identity checks, and its remainder norm. Original profile horizons are reproduced. Additional analysis extends only the same frozen laws, capped at 65,536 sampled steps; there is no parameter search. Detailed tail thresholds, cap-limited windows and observed crossings appear in SUMMARY.json and each AUDIT.json. A line crossing is not called the unique crossover. No float64 tail evaluation is promoted to a verified all-horizon rounding certificate.",
        "",
        "Independent geometric endings use the same mean *physical durations* 10,100,1000,10000 across cadences, converting to step counts. Uniform endings use 0 through each evaluated window. These are expected log-lushness, not expected perplexity, entropy at the mean ending, or stopped-record entropy. Asymptotic bias/offset for projected histories remains unsupported; their original analytic finite-memory bounds are reproduced rather than replaced by a quotient Markov approximation.",
        "",
        "## T mathematical verification",
        "",
        f"Reference status: **{references['status'] if references else 'missing'}**. Maximum identity residual: **{references['max_identity_residual_bits'] if references else None} bits**.",
        "",
        "The reference suite checks early/late branching with actual profile dominance, equal-rate cases with different offsets and with equal offsets but different transients, single and multiple crossings, a periodic bias remainder, and state-dependent termination. Geometric totals are checked against analytic survival probabilities; uniform totals against direct profile averages. State-dependent termination has its own joint law and separately counts stopping uncertainty. The kernels are mathematical references, not paid chemical models or new empirical evidence for an ethical claim.",
        "",
        "## Quality, resources and provenance",
        "",
        f"Batch wall time {receipt['wall_seconds']:.2f} seconds; peak job memory {peak / 1024**2:.2f} MiB. Jobs use enforced wall/RAM/output caps with the shared reserve. The first preparation-only attempt stopped when E1's selected point was found to have only cadence .25 in its original case grid. The final frozen plan uses that existing cadence; no missing cadences or substitute parameter points were invented and no score had been computed in that preparation attempt.",
        "",
        "[PLAN.json](PLAN.json), [PROVENANCE.json](PROVENANCE.json), original source archive, frozen auditor, original results, native replay results, current audits and all receipts accompany this report. Six study cards separate numerical confidence, resolution coverage, physical adequacy and claim relevance. Latest Appendix A/B conformance is unverified because those source revisions were not supplied. Existing contrary findings and causal-audit limits are preserved.",
        "",
        "The missing work/activity-qualified physical comparator, irreversible damage, spatial disorder, retained deeper genealogy, blocking and stronger paid-information worlds remain separate proposals. This bounded verification does not launch them or make them prerequisites for manuscript publication.",
        "",
        "Final workspace checks and restoration/privacy verification are recorded separately in VALIDATION.json when completed; they do not promote scientific or physical adequacy claims.",
        "",
    ]
    (out / "REPORT.md").write_text("\n".join(report), encoding="utf-8")
    analysis = out / "analysis"
    analysis.mkdir()
    shutil.copyfile(Path(__file__), analysis / Path(__file__).name)
    shutil.copyfile(
        ROOT / "scripts/restore_p0_t_verification.py",
        analysis / "restore_p0_t_verification.py",
    )
    (out / "REPRODUCE.md").write_text(
        "# Reproduce the bounded P0/T verification\n\n"
        "Use the repository testbed Python environment (NumPy/SciPy) on Windows. "
        "No ignored historical run cache is required: both source archives and "
        "all selected original result bytes are retained here.\n\n"
        "First restore into a fresh ignored directory, without execution:\n\n"
        "```powershell\npython scripts/restore_p0_t_verification.py --evidence-dir "
        "research/platform/engineering/p0-t-verification-2026-10-30 "
        "--out-dir runs/p0-t-restored\n```\n\n"
        "Restoration checks the registered plan, every original source and auditor "
        "file, and each retained original result. It rejects overwrites and unlisted "
        "archive inputs. Verify the repository driver matches its hash in the "
        "restored current/MANIFEST.json before executing it:\n\n"
        "```powershell\npython scripts/run_p0_t_verification.py execute "
        "--out-dir runs/p0-t-restored\n```\n\n"
        "The driver invokes only the frozen worker/native sources under the "
        "retained plan and caps. A cap/provenance failure stays incomplete; do not "
        "substitute a point or broaden the map. One study point is not its full "
        "parameter sweep. Latest Appendix A/B conformance and physical faithfulness "
        "are outside this reproduction.\n",
        encoding="utf-8",
    )
    write(
        out / "EVIDENCE.json",
        {
            "schema": "omega.p0-t-verification-evidence/1",
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
                "native_rows": original_rows,
                "contrasts": summary["headline_contrast_rows"],
                "peak_MiB": peak / 1024**2,
            }
        )
    )


if __name__ == "__main__":
    main()
