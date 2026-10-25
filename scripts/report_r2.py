"""Verify finite-study evidence and render the R2 capacity-analysis layout."""

import argparse
import json
import shutil
import sys
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from omega_cosmology.testbed.analysis import comparison_profiles


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


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
        parser.error("Use a run under runs/ and a fresh study output directory")
    receipt = json.loads((run / "BATCH_RECEIPT.json").read_text(encoding="utf-8"))
    manifest_path = run / "frozen/MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    protocol_path = run / "frozen" / manifest["protocol"]
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    if (
        receipt["status"] != "passed"
        or receipt["feasibility_only"]
        or receipt["manifest_sha256"] != digest(manifest_path)
        or receipt["protocol_sha256"] != digest(protocol_path)
    ):
        raise RuntimeError("A complete verified batch is required")
    for entry in manifest["files"]:
        if digest(run / "frozen" / entry["path"]) != entry["sha256"]:
            raise RuntimeError("Frozen source mismatch")
    rows = {}
    bank_accounts = []
    case_metadata = []
    preparations = {p["id"]: p for p in protocol["preparations"]}
    bank = protocol["bank_account"]
    bank_index = protocol["coordinate_order"].index(bank["coordinate"])
    for case in receipt["cases"]:
        path = run / case["case"] / "RESULT.json"
        if not case["validated"] or digest(path) != case["result_sha256"]:
            raise RuntimeError("Case hash mismatch")
        result = json.loads(path.read_text(encoding="utf-8"))
        if result["manifest_sha256"] != receipt["manifest_sha256"]:
            raise RuntimeError("Case source mismatch")
        case_metadata.append({k: v for k, v in result.items() if k != "rows"})
        for row in result["rows"]:
            key = (row["law"], row["preparation"], row["cadence"], row["horizon"])
            if key in rows or row["history"]["model_hash"] != result["model_hash"]:
                raise RuntimeError("Duplicate or mismatched physical row")
            counts = row["physical"]["integrated_channels"]
            capture = sum(
                counts.get(r + ".forward", 0) - counts.get(r + ".reverse", 0)
                for r in bank["capture_rules"]
            )
            spend = sum(
                bill * (counts.get(r + ".forward", 0) - counts.get(r + ".reverse", 0))
                for r, bill in bank["spend_rules"].items()
            )
            initial = sum(
                bank["quantum"] * s[bank_index] * w
                for s, w in preparations[row["preparation"]]["roots"]
            )
            endpoint = row["observables"]["bank_energy"]["endpoint"]
            residual = endpoint - initial - capture + spend
            if abs(residual) > 1e-8:
                raise ArithmeticError("Independent bank ledger failed")
            bank_accounts.append(
                {
                    "law": key[0],
                    "preparation": key[1],
                    "cadence": key[2],
                    "horizon": key[3],
                    "initial": initial,
                    "endpoint": endpoint,
                    "net_capture": capture,
                    "net_internal_spend": spend,
                    "residual": residual,
                }
            )
            rows[key] = row
    expected = {
        (l["id"], p["id"], dt, T)
        for l in protocol["laws"]
        for p in protocol["preparations"]
        for dt in protocol["cadences"]
        for T in protocol["horizons"]
    }
    if set(rows) != expected or len(receipt["cases"]) != len(protocol["laws"]) * len(
        protocol["cadences"]
    ):
        raise RuntimeError("Incomplete result grid")
    eps = protocol["numerical"]["sign_deadband_bits"]

    def sign(x):
        return 1 if x > eps else -1 if x < -eps else 0

    comparisons = []
    for spec in protocol["comparisons"]:
        for dt in protocol["cadences"]:
            for T in protocol["horizons"]:
                a, b = [
                    rows[law, prep, dt, T]
                    for law, prep in (spec["first"], spec["second"])
                ]
                value = a["history"]["ell_bits"] - b["history"]["ell_bits"]
                shares = {
                    k: a["coordinate_shares_bits"][k] - b["coordinate_shares_bits"][k]
                    for k in protocol["coordinate_order"]
                }
                if abs(sum(shares.values()) - value) > eps:
                    raise ArithmeticError("Contrast coordinate shares do not close")
                comparisons.append(
                    {
                        "id": spec["id"],
                        "kind": spec["kind"],
                        "cadence": dt,
                        "horizon": T,
                        "delta_ell_bits": value,
                        "sign": sign(value),
                        "delta_rate_bits_per_time": a["asymptotic"][
                            "rate_bits_per_time"
                        ]
                        - b["asymptotic"]["rate_bits_per_time"],
                        "delta_offset_bits": a["asymptotic"]["offset_bits"]
                        - b["asymptotic"]["offset_bits"],
                        "delta_observables": {
                            key: {
                                field: a["observables"][key][field]
                                - b["observables"][key][field]
                                for field in ("endpoint", "integrated", "stationary")
                            }
                            for key in a["observables"]
                        },
                        "delta_event_readouts": {
                            key: a["event_readouts"][key] - b["event_readouts"][key]
                            for key in a["event_readouts"]
                        },
                        "delta_completed_witnesses": {
                            key: a["witnesses"][key]["completed_probability"]
                            - b["witnesses"][key]["completed_probability"]
                            for key in a["witnesses"]
                        },
                        "delta_net_external_work": a["physical"]["work_net"]
                        - b["physical"]["work_net"],
                        "delta_gross_accepted_work": a["physical"][
                            "work_accepted_gross"
                        ]
                        - b["physical"]["work_accepted_gross"],
                        "delta_expected_jumps": a["activity"]["expected_jumps"]
                        - b["activity"]["expected_jumps"],
                        "delta_finite_coefficient_bits": a["activity"][
                            "finite_coefficient_bits"
                        ]
                        - b["activity"]["finite_coefficient_bits"],
                        "coordinate_share_differences_bits": shares,
                    }
                )
    groups = defaultdict(list)
    for item in comparisons:
        groups[item["id"], item["horizon"]].append(item)
    corridor = [
        {
            "id": id,
            "horizon": T,
            "strict_sign_flip": any(v["sign"] == 1 for v in values)
            and any(v["sign"] == -1 for v in values),
            "signs": sorted({v["sign"] for v in values}),
        }
        for (id, T), values in groups.items()
    ]
    counts = {
        kind: dict(Counter(str(v["sign"]) for v in comparisons if v["kind"] == kind))
        for kind in dict.fromkeys(v["kind"] for v in comparisons)
    }
    profiles = comparison_profiles(comparisons, eps)
    horizon_flips = sum(v["strict_sign_flip"] for v in profiles["horizon_audit"])
    metrics = {
        "max_bank_residual": max(abs(v["residual"]) for v in bank_accounts),
        "max_first_law_residual": max(
            abs(v["physical"]["energy_residual"]) for v in rows.values()
        ),
        **{
            key: max(v["validation"][key] for v in rows.values())
            for key in next(iter(rows.values()))["validation"]
        },
    }
    primary = protocol["primary_cadence"]
    Tmax = max(protocol["horizons"])
    focus = protocol["preparations"][0]["id"]
    primary_contrasts = [
        v for v in comparisons if v["cadence"] == primary and v["horizon"] == Tmax
    ]
    table = "\n".join(
        f"| {v['id']} | {v['delta_ell_bits']:+.6f} | {v['delta_rate_bits_per_time']:+.9f} |"
        for v in primary_contrasts
    )
    observable_names = [d["id"] for d in protocol["observables"]]
    physical_tables = []
    for prep in preparations:
        header = (
            "| Law | " + " | ".join(observable_names) + " |" + " Witness probability |"
        )
        rule = "|---|" + "---:|" * (len(observable_names) + 1)
        lines = [header, rule]
        for law in protocol["laws"]:
            r = rows[law["id"], prep, primary, Tmax]
            witness = (
                next(iter(r["witnesses"].values()))["completed_probability"]
                if r["witnesses"]
                else 0
            )
            lines.append(
                "| "
                + law["id"]
                + " | "
                + " | ".join(
                    f"{r['observables'][name]['endpoint']:.6g}"
                    for name in observable_names
                )
                + f" | {witness:.6g} |"
            )
        physical_tables.append("### " + prep + "\n\n" + "\n".join(lines))
    usage = "\n".join(
        f"| {l['id']} | {rows[l['id'], focus, primary, Tmax]['event_readouts']['expanded_capture_forward']:.6g} | "
        f"{rows[l['id'], focus, primary, Tmax]['event_readouts']['expanded_capture_reverse']:.6g} | "
        f"{rows[l['id'], focus, primary, Tmax]['event_readouts']['high_bank_paid_activation']:.6g} | "
        f"{rows[l['id'], focus, primary, Tmax]['event_readouts']['high_bank_repair_energy_above_old_cap']:.6g} |"
        for l in protocol["laws"]
    )
    peak = max(c["receipt"]["peak_job_bytes"] for c in receipt["cases"])
    count_table = "\n".join(
        f"| {kind} | {values.get('1', 0)} | {values.get('-1', 0)} | {values.get('0', 0)} |"
        for kind, values in counts.items()
    )
    out.mkdir(parents=True)
    (out / "cases").mkdir()
    for case in receipt["cases"]:
        shutil.copyfile(
            run / case["case"] / "RESULT.json", out / "cases" / (case["case"] + ".json")
        )
    for name, path in [
        ("SOURCE_MANIFEST.json", manifest_path),
        ("PROTOCOL.json", protocol_path),
        ("BATCH_RECEIPT.json", run / "BATCH_RECEIPT.json"),
    ]:
        shutil.copyfile(path, out / name)
    analysis = {
        "schema": "omega.finite-study-analysis/1",
        "study": protocol["id"],
        "profile_rows": len(rows),
        "comparison_rows": len(comparisons),
        "sign_deadband_bits": eps,
        "sign_counts": counts,
        "corridor": corridor,
        "comparison_profiles": profiles,
        "comparisons": comparisons,
        "bank_accounts": bank_accounts,
        "validation": metrics,
        "case_metadata": case_metadata,
        "wall_seconds": receipt["wall_seconds"],
        "max_job_memory_bytes": peak,
        "scope": protocol["scope"],
    }
    (out / "ANALYSIS.json").write_text(
        json.dumps(analysis, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    report = f"""# {protocol["id"]}: numerical report

24 October 2026. Complete batch, {len(rows)} finite-history profiles and
{len(receipt["cases"])} validated law/cadence cases. The computational pass is
independent of favorable scientific signs. Interpretation is a separate document.

## Question and mechanism

{protocol["question"]}

Every arm has the same constituent slots/carrier and each root has energy
{protocol["energy_per_root"]}. Native/basal construction remains available.
{protocol["controls"]}

Comparisons are preparation, construction-assistance, functional-capacity and
boundary-law contrasts. They are not choices from one common present. All
represented thermal, construction and other physical randomness remains in
complete sampled-history lushness. The quantities below are log lushness in bits.

## Rankings

| Contrast family | Positive | Negative | Within numerical deadband |
|---|---:|---:|---:|
{count_table}

There are {sum(v["strict_sign_flip"] for v in corridor)} strict cadence sign flips
among {len(corridor)} comparison/horizon groups. Separately, {horizon_flips}
comparison/cadence groups change sign across the measured horizons. These are
grid brackets, not exact crossover locations. Full profiles and interval
accumulation differences are in ANALYSIS.json.
Sign tolerance is {eps:g} bits, a numerical validation allowance, not a rigorous
interval certificate or physical-faithfulness proof. Cadences are .125,.25,.5;
horizons are 16,64,256,1024. Rate/offset are diagnostics of the finite profile.

Primary cadence {primary}, horizon {Tmax}:

| Contrast | Delta ell (bits) | Delta rate (bits/time) |
|---|---:|---:|
{table}

All same-law preparation rates tie. Mechanism and boundary contrasts may
change limiting rates. Matched source prescription does not imply matched
accepted/net work or activity; those differences are recorded separately.

## Actual capacity use and return to function

Endpoint observables at T{Tmax}, cadence {primary}:

{chr(10).join(physical_tables)}

The report also stores integrated and true stationary observables, so finite
endpoint differences are not mistaken for asymptotic physical differences.
For preparation `{focus}` at T{Tmax}:

| Law | Expanded-only capture forward | Expanded capture reverse | High-bank paid activations | Above-old-cap energy spent on activation |
|---|---:|---:|---:|---:|
{usage}

An expanded-only capture starts with bank 3/4 and ends with bank 5/6 ticks;
that target is impossible without the added storage capacity. The energy
readout counts only the .5/1 units stored above the old two-energy-unit limit
that a high-bank paid activation consumes. Repair is also possible at lower
bank levels; this does not assert the new store is necessary for every repair.

The passive witness follows the first new store construction, an expanded-only
capture, high-bank paid activation restoring both constituents, then re-binding.
It aborts if that store is lost, if the extra energy is lost before repair, or
if the restored constituents fail before binding. Aborts are absorbing and
never quietly restart. Initial prebuilt storage is not credited as a new
construction. Upkeep-only heat dissipation cannot complete the repair stage.
This is an ordered event-sequence witness. It does not establish enabling
ancestry: the initial store can be built basally and captured energy can come
through native pathways. It is not proof of autocatalytic closure or a count of generations.
It contributes no physical state or entropy to the scored law.

## Accounting, validation and scope

The bank audit includes capture, activation, upkeep, both storage-construction
channels and all reverse refunds. Maximum bank residual:
{metrics["max_bank_residual"]:.2e}; first-law residual:
{metrics["max_first_law_residual"]:.2e}; independent history accumulation:
{metrics["history_accumulation_residual"]:.2e}; monitor physical marginal:
{metrics["monitor_marginal_residual"]:.2e}. Independent exponentials, coordinate
chain rule, Gibbs/source-off detailed balance and complete reachability pass.
No dense kernels, augmented monitor histories or trajectories are retained.

First full fine-cadence/T1024 case: {receipt["cases"][0]["receipt"]["wall_seconds"]:.3f}s.
Total supervised execution: {receipt["wall_seconds"]:.3f}s; peak job commitment
{peak / 1024**2:.2f} MiB; run output {receipt["output_bytes"]:,} bytes. Per-case
caps: {protocol["caps"]["case_wall_seconds"]}s, 2 GiB, 32 MiB. Batch caps:
{protocol["caps"]["batch_wall_seconds"]}s, 128 MiB. Sources and original case
hashes are preserved in SOURCE_MANIFEST.json and BATCH_RECEIPT.json.

{protocol["scope"]}

Additional physical limits: fixed contact/slots, memoryless resource,
unresolved bath/source histories, no spatial transport or controller. Storage
dissolution follows the declared coupled refund pair. With three or more bank
ticks it is blocked, since the refund cannot fit after capacity is removed.
An independent spill/dissolution pathway is not represented. Upkeep is a
reversible bank-relaxation route, not a demonstrated maintenance requirement. Construction
and heat-loss rates are stipulated toy kinetics, with physical grain
faithfulness open. No claim is made about three-link recursive compounding.

## Standard report form

- Mechanism: paid construction changes physically admissible storage/capture.
- Ranking: finite-history totals and every declared contrast, without a success-sign filter.
- Relationship: capacity use, energy spent on actual reconstruction, and history/rate changes.
- Comparison kind: explicitly preparation or changed mechanism/boundary law.
- Horizon: the four finite windows and three cadences above.
- Challenge: whether further enabling does more than paid construction churn.

Reproduce using the protocol writer and `scripts/run_finite_study.py`, then
`scripts/report_r2.py` with fresh run/output paths. Raw source snapshot:
`{run.relative_to(ROOT).as_posix()}/frozen` (ignored). No commit, push or upload performed.
"""
    (out / "RESULTS.md").write_text(report, encoding="utf-8")
    evidence = {
        "schema": "omega.study-evidence/1",
        "status": "verified",
        "study": protocol["id"],
        "report_generator_sha256": digest(Path(__file__)),
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
        json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": "verified",
                "profiles": len(rows),
                "sign_counts": counts,
                "cadence_flips": sum(v["strict_sign_flip"] for v in corridor),
                "horizon_flip_groups": horizon_flips,
                "peak_mib": peak / 1024**2,
                "primary_assistance": next(
                    v
                    for v in primary_contrasts
                    if v["id"] == "driven:assisted-minus-basal:" + focus
                ),
                "primary_capacity": next(
                    v
                    for v in primary_contrasts
                    if v["id"] == "driven:assisted-minus-sham:" + focus
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
