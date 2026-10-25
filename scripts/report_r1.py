"""Verify compact R1 evidence and report comparisons without changing the score."""

import argparse
import json
import shutil
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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
        parser.error(
            "Use a run under runs/ and a fresh output directory under research/studies/"
        )
    receipt = json.loads((run / "BATCH_RECEIPT.json").read_text(encoding="utf-8"))
    manifest = json.loads((run / "frozen/MANIFEST.json").read_text(encoding="utf-8"))
    protocol_path = run / "frozen/research/studies/R1-constructed-access/PROTOCOL.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    if (
        receipt["status"] != "passed"
        or receipt["feasibility_only"]
        or receipt["manifest_sha256"] != digest(run / "frozen/MANIFEST.json")
        or receipt["protocol_sha256"] != digest(protocol_path)
    ):
        raise RuntimeError("A complete verified scientific batch is required")
    for entry in manifest["files"]:
        if digest(run / "frozen" / entry["path"]) != entry["sha256"]:
            raise RuntimeError("Snapshot changed")
    if len(receipt["cases"]) != len(protocol["laws"]) * len(protocol["cadences"]):
        raise RuntimeError("Missing cases")
    rows = {}
    case_records = []
    bank_residuals = []
    eps = protocol["numerical"]["sign_deadband_bits"]

    def sign(value):
        return 1 if value > eps else -1 if value < -eps else 0

    preparations = {p["id"]: p for p in protocol["preparations"]}
    for case in receipt["cases"]:
        path = run / case["case"] / "RESULT.json"
        if not case["validated"] or digest(path) != case["result_sha256"]:
            raise RuntimeError("Case receipt mismatch")
        result = json.loads(path.read_text(encoding="utf-8"))
        if result["manifest_sha256"] != receipt["manifest_sha256"]:
            raise RuntimeError("Case source mismatch")
        case_records.append({k: v for k, v in result.items() if k != "rows"})
        for row in result["rows"]:
            key = (row["law"], row["preparation"], row["cadence"], row["horizon"])
            if key in rows or row["history"]["model_hash"] != result["model_hash"]:
                raise RuntimeError("Duplicate row or inconsistent physical identity")
            physical = row["physical"]
            counts = physical["integrated_channels"]
            capture = counts.get("capture.forward", 0) - counts.get(
                "capture.reverse", 0
            )
            spending = sum(
                bill
                * (counts.get(name + ".forward", 0) - counts.get(name + ".reverse", 0))
                for name, bill in protocol["bank_bills"].items()
            )
            initial = sum(
                0.5 * state[-1] * w
                for state, w in preparations[row["preparation"]]["roots"]
            )
            residual = row["function"]["stored_energy"] - initial - capture + spending
            if abs(residual) > 1e-8:
                raise ArithmeticError("Independent bank account does not close")
            bank_residuals.append(abs(residual))
            row["bank_audit"] = {
                "initial_energy": initial,
                "captured_net_energy": capture,
                "internal_spend_net": spending,
                "balance_residual": residual,
            }
            rows[key] = row
    expected = {
        (l["id"], p["id"], dt, T)
        for l in protocol["laws"]
        for p in protocol["preparations"]
        for dt in protocol["cadences"]
        for T in protocol["horizons"]
    }
    if set(rows) != expected:
        raise RuntimeError("Incomplete declared result grid")
    comparisons = []

    def comparison(kind, context, a, b):
        gap = a["history"]["ell_bits"] - b["history"]["ell_bits"]
        shares = {
            k: a["coordinate_shares_bits"][k] - b["coordinate_shares_bits"][k]
            for k in protocol["coordinate_order"]
        }
        if abs(sum(shares.values()) - gap) > eps:
            raise ArithmeticError("Comparison decomposition failed")
        item = {
            "kind": kind,
            "context": context,
            "cadence": a["cadence"],
            "horizon": a["horizon"],
            "delta_ell_bits": gap,
            "sign": sign(gap),
            "delta_rate_bits_per_time": a["asymptotic"]["rate_bits_per_time"]
            - b["asymptotic"]["rate_bits_per_time"],
            "delta_offset_bits": a["asymptotic"]["offset_bits"]
            - b["asymptotic"]["offset_bits"],
            "delta_bound_probability": a["function"]["bound_probability"]
            - b["function"]["bound_probability"],
            "delta_active_units": a["function"]["active_units"]
            - b["function"]["active_units"],
            "delta_net_external_work": a["physical"]["work_net"]
            - b["physical"]["work_net"],
            "delta_accepted_external_work": a["physical"]["work_accepted_gross"]
            - b["physical"]["work_accepted_gross"],
            "delta_expected_jumps": a["activity"]["expected_jumps"]
            - b["activity"]["expected_jumps"],
            "delta_finite_coefficient_bits": a["activity"]["finite_coefficient_bits"]
            - b["activity"]["finite_coefficient_bits"],
            "coordinate_share_differences_bits": shares,
        }
        comparisons.append(item)

    for law in protocol["laws"]:
        for dt in protocol["cadences"]:
            for T in protocol["horizons"]:
                a = rows[law["id"], "built", dt, T]
                for reference in ("unassembled", "equal_energy_reference"):
                    comparison(
                        "preparation",
                        law["id"] + ":built-minus-" + reference,
                        a,
                        rows[law["id"], reference, dt, T],
                    )
    for prefix in ("driven", "source_off"):
        for prep in preparations:
            for dt in protocol["cadences"]:
                for T in protocol["horizons"]:
                    comparison(
                        "mechanism",
                        prefix + ":intact-minus-ablated:" + prep,
                        rows[prefix + "__intact", prep, dt, T],
                        rows[prefix + "__ablated", prep, dt, T],
                    )
    for suffix in ("intact", "ablated"):
        for prep in preparations:
            for dt in protocol["cadences"]:
                for T in protocol["horizons"]:
                    comparison(
                        "boundary",
                        suffix + ":driven-minus-source_off:" + prep,
                        rows["driven__" + suffix, prep, dt, T],
                        rows["source_off__" + suffix, prep, dt, T],
                    )
    interaction = []
    for prep in preparations:
        for dt in protocol["cadences"]:
            for T in protocol["horizons"]:

                def ell(name, prep=prep, dt=dt, T=T):
                    return rows[name, prep, dt, T]["history"]["ell_bits"]

                value = (
                    ell("driven__intact")
                    - ell("driven__ablated")
                    - ell("source_off__intact")
                    + ell("source_off__ablated")
                )
                interaction.append(
                    {
                        "preparation": prep,
                        "cadence": dt,
                        "horizon": T,
                        "interaction_bits": value,
                        "sign": sign(value),
                        "meaning": "Factorial explanatory contrast; the four unmodified lushness totals remain primary",
                    }
                )
    groups = defaultdict(list)
    for item in comparisons:
        groups[item["kind"], item["context"], item["horizon"]].append(item)
    corridor = []
    for (kind, context, T), items in groups.items():
        signs = {x["sign"] for x in items}
        corridor.append(
            {
                "kind": kind,
                "context": context,
                "horizon": T,
                "signs": sorted(signs),
                "strict_sign_flip": 1 in signs and -1 in signs,
                "same_resolved_sign_at_all_cadences": len(signs) == 1
                and 0 not in signs,
            }
        )
    counts = {
        kind: dict(Counter(str(r["sign"]) for r in comparisons if r["kind"] == kind))
        for kind in ("preparation", "mechanism", "boundary")
    }
    count_table = "\n".join(
        f"| {kind} | {values.get('1', 0)} | {values.get('-1', 0)} | {values.get('0', 0)} |"
        for kind, values in counts.items()
    )
    peak = max(c["receipt"]["peak_job_bytes"] for c in receipt["cases"])
    primary = protocol["primary_cadence"]

    def at(law, prep, T=1024, dt=primary):
        return rows[law, prep, dt, T]

    def delta(kind, context, T=1024, dt=primary):
        return next(
            c
            for c in comparisons
            if c["kind"] == kind
            and c["context"] == context
            and c["horizon"] == T
            and c["cadence"] == dt
        )

    prep_table = "\n".join(
        f"| {T} | {delta('preparation', 'driven__intact:built-minus-unassembled', T)['delta_ell_bits']:+.6f} | {delta('preparation', 'driven__intact:built-minus-equal_energy_reference', T)['delta_ell_bits']:+.6f} |"
        for T in protocol["horizons"]
    )
    mechanism_table = "\n".join(
        f"| {prep} | {T} | {delta('mechanism', 'driven:intact-minus-ablated:' + prep, T)['delta_ell_bits']:+.6f} | {delta('mechanism', 'driven:intact-minus-ablated:' + prep, T)['delta_bound_probability']:+.6f} | {delta('mechanism', 'driven:intact-minus-ablated:' + prep, T)['delta_net_external_work']:+.6f} |"
        for prep in preparations
        for T in (64, 1024)
    )
    rate_table = "\n".join(
        f"| {l['id']} | {at(l['id'], 'built')['asymptotic']['rate_bits_per_time']:.9f} | {at(l['id'], 'built')['function']['bound_probability']:.6f} |"
        for l in protocol["laws"]
    )
    function_table = "\n".join(
        f"| {p} | {at('driven__intact', p)['function']['bound_probability']:.6f} | {at('driven__intact', p)['function']['active_units']:.6f} | {at('driven__intact', p)['function']['dissolution_then_rebinding']['completed_probability']:.6f} | {at('driven__intact', p)['bank_audit']['captured_net_energy']:.6f} | {at('driven__intact', p)['bank_audit']['internal_spend_net']:.6f} |"
        for p in preparations
    )
    metrics = {
        "max_bank_balance_residual": max(bank_residuals),
        "max_history_accumulation_residual": max(
            r["validation"]["history_accumulation_residual"] for r in rows.values()
        ),
        "max_coordinate_share_residual": max(
            r["validation"]["share_sum_residual"] for r in rows.values()
        ),
        "max_monitor_marginal_residual": max(
            r["validation"]["monitor_marginal_residual"] for r in rows.values()
        ),
        "max_first_law_residual": max(
            abs(r["physical"]["energy_residual"]) for r in rows.values()
        ),
    }
    out.mkdir(parents=True)
    (out / "cases").mkdir()
    for case in receipt["cases"]:
        shutil.copyfile(
            run / case["case"] / "RESULT.json", out / "cases" / (case["case"] + ".json")
        )
    for name, source in [
        ("SOURCE_MANIFEST.json", run / "frozen/MANIFEST.json"),
        ("BATCH_RECEIPT.json", run / "BATCH_RECEIPT.json"),
        ("PROTOCOL.json", protocol_path),
    ]:
        shutil.copyfile(source, out / name)
    analysis = {
        "schema": "omega.r1-analysis/1",
        "profile_rows": len(rows),
        "comparison_rows": len(comparisons),
        "sign_deadband_bits": eps,
        "sign_counts": counts,
        "corridor": corridor,
        "comparisons": comparisons,
        "source_access_interaction": interaction,
        "validation": metrics,
        "case_metadata": case_records,
        "scope": protocol["scope"],
        "max_job_memory_bytes": peak,
        "wall_seconds": receipt["wall_seconds"],
    }
    (out / "ANALYSIS.json").write_text(
        json.dumps(analysis, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    report = f"""# R1: constructed access and costed reconstruction

24 October 2026. Complete finite modeled-world batch: {len(rows)} profiles,
{len(receipt["cases"])} law/cadence cases; all numerical/physical validations passed.
The computational status does not require a favorable scientific contrast.

## Question, mechanism and comparator

An assembled local interface assists reversible carrier unlocking. Capture can
fill a bank used for activation and upkeep, with basal reconstruction retained.
The preparation contrast uses one law and equal constituents/carrier/energy
(4.5 units), allocated differently. The mechanism contrast removes only the
paired assisted-unlock path. The source-off contrast changes the boundary law.
The same-energy reference averages {len(preparations["equal_energy_reference"]["roots"])} known roots; drawing a root contributes no entropy.
This is a coarse fixed-slot model, not gas or microscopic chemistry.

## What lushness ranks

Finite sampled-history entropy is log lushness. Positive values below favor
the first arm. These are numerical comparisons with a {eps:g}-bit deadband,
not formal certificates of physical temporal faithfulness.

Driven intact law, primary cadence {primary}:

| Horizon | Built minus unassembled (bits) | Built minus equal-energy reference (bits) |
|---|---:|---:|
{prep_table}

| Contrast kind | Positive | Negative | Within numerical deadband |
|---|---:|---:|---:|
{count_table}

There are
{sum(c["strict_sign_flip"] for c in corridor)} strict temporal sign reversals across
{len(corridor)} comparison/horizon groups. Every contrast is retained in ANALYSIS.json.
All same-law preparation rates tie; offsets and finite profiles carry that
comparison. Neither a positive nor a negative offset is relabeled a theory verdict.

## Access mechanism and material consequences

Intact minus ablated, driven law, primary cadence:

| Preparation | Horizon | Delta ell (bits) | Delta bound probability | Delta net external work |
|---|---:|---:|---:|---:|
{mechanism_table}

Accepted and returned work are reported separately in each case. These arms
have the same supplied boundary prescription, not necessarily equal absorbed
work or equal event counts. The source-off factorial interaction is reported
as an explanatory contrast; it does not replace any total or subtract noise
from lushness. Native thermal activity remains in every arm.

## Long-horizon diagnostics and structural account

| Law | Rate at primary cadence (bits/time) | Bound probability at T1024, built root |
|---|---:|---:|
{rate_table}

Driven intact at T1024, primary cadence:

| Preparation | Bound probability | Active units | Dissolution then re-binding probability | Net captured bank energy | Net internal bank spend |
|---|---:|---:|---:|---:|---:|
{function_table}

The witness is an unconditional ordered event probability. Re-binding alone
can occur without synthesizing new material or a paid activation. It is not
offspring, depth-three compounding or a claim of damage robustness. The monitor
does not restart, is never scored, and its physical marginal is checked against
the original process. Paid and basal activation, reversals and upkeep are
separate ledger entries. Stock and cumulative event flux are distinct readouts.

All laws retain paths to a functional interface; no state is permanently
closed in this model. Long-run rates therefore describe continuing finite
reconstruction/turnover rather than irreversible loss. Coordinate shares use
the frozen order {protocol["coordinate_order"]}; they are explanatory and order
dependent. Nbar and F expose fine-cadence activity, with the finite-cadence
remainder retained. No event class is removed from the total.

Availability is reported both for the preparation ensemble distribution and
averaged conditional on its known root. This keeps mixing information separate
from the root-conditioned history score. Available free energy is a benchmark,
not guaranteed extractable work through the current controls.

## Execution, validation and scope

The first complete T1024/fine-cadence case passed in
{receipt["cases"][0]["receipt"]["wall_seconds"]:.3f} seconds before the other cases launched.
Total supervised time {receipt["wall_seconds"]:.3f} seconds; maximum job commitment
{peak / 1024**2:.2f} MiB; measured run output {receipt["output_bytes"]:,} bytes.
Caps were 120 seconds/2 GiB/32 MiB per case, 300 seconds/128 MiB per batch.

Independent exponential kernels, binary-power history accumulation, coordinate
chain rule, dense/sparse propagation, passive monitor marginals, first law,
source-off detailed balance and the independent bank ledger all pass.
Maximum absolute bank residual {metrics["max_bank_balance_residual"]:.2e};
history-accumulation residual {metrics["max_history_accumulation_residual"]:.2e};
monitor marginal residual {metrics["max_monitor_marginal_residual"]:.2e}.

The stipulated physics has fixed slots, one contact and carrier, one bath,
maintained work exchange, and no independently embodied controller or spatial
transport. Bath/source histories are unresolved. The three cadences audit the
toy temporal profile; physical grain faithfulness remains open. This does not
test interpersonal ethics, microscopic thermal baselines or open-ended growth.

## Standard report form and reconstruction

- Mechanism: constructed paired unlocking plus paid/basal reconstruction.
- Ranking: the full finite profiles and every declared contrast above/in ANALYSIS.json.
- Relationship: preparation effects versus sustained mechanism and source effects;
  accepted work, activity and function are reported independently.
- Comparison kind: preparation, mechanism, and boundary-law contrasts; no chosen histories.
- Horizon: 16,64,256,1024 at cadences .125,.25,.5; rate/offset diagnostic only.
- Challenge: whether the implemented access pathway changes continuation and
  reconstruction under matched physical endowment, without a favorable-outcome requirement.

Run `python scripts/write_r1_protocol.py`, then
`python scripts/run_r1_batch.py --out-dir runs/r1-fresh`.
Use `scripts/report_r1.py` with `--run-dir` and a fresh `--out-dir` to verify and
promote compact evidence. SOURCE_MANIFEST.json binds the frozen input bytes;
BATCH_RECEIPT.json binds each original case result under cases/.
Full source snapshot is `{run.relative_to(ROOT).as_posix()}/frozen` (ignored).
No dense kernels/trajectories are retained. No commit, push or upload performed.
"""
    (out / "RESULTS.md").write_text(report, encoding="utf-8")
    evidence = {
        "schema": "omega.study-evidence/1",
        "study": protocol["id"],
        "status": "verified",
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
                "rows": len(rows),
                "comparison_sign_counts": counts,
                "temporal_flips": sum(c["strict_sign_flip"] for c in corridor),
                "max_memory_mib": peak / 1024**2,
                "primary_preparation_T1024": delta(
                    "preparation", "driven__intact:built-minus-unassembled"
                ),
                "primary_mechanism_T1024": delta(
                    "mechanism", "driven:intact-minus-ablated:built"
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
