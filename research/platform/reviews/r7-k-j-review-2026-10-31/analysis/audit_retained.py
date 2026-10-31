"""Read-only figure checks on retained evidence; no simulator or scorer imports.

Private manuscript text is never copied into the output. Locations in the
review are manual review annotations, not an automatic claim-extraction proof.
"""

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[5]
EXPECTED_PACKET_SHA256 = "60abeb79ffaedbe8268a8ca14b7a53ecc1fb6c9e74d111dce7f03131f7b83db6"
STUDIES = {
    "R1": "R1-constructed-access/results-2026-10-24",
    "R2": "R2-further-capacity/results-2026-10-24",
    "E1": "E1-coupled-autocatalysis/results-2026-10-25",
    "S3": "S3-repair-and-interaction/results-2026-10-26",
    "S4": "S4-warning-and-obstruction/results-2026-10-26",
    "S4b": "S4b-paid-warning/results-2026-10-26",
}
P0 = "research/platform/engineering/p0-t-verification-2026-10-30"
PQ = "research/platform/engineering/paired-qualification-2026-10-30-r2"
A = "research/platform/engineering/resource-load-control-2026-10-30"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise ValueError("Use a fresh output directory")
    if sha(args.packet.read_bytes()) != EXPECTED_PACKET_SHA256:
        raise ValueError("Packet changed; this manual figure registry needs a new review")
    sources, checks = {}, []

    def load(name):
        path = ROOT / name
        raw = path.read_bytes()
        record = {"path": name, "sha256": sha(raw), "bytes": len(raw)}
        # Check the nearest retained evidence manifest, not just a new checksum.
        for parent in path.parents:
            if parent == ROOT:
                break
            manifest = parent / "EVIDENCE.json"
            if not manifest.is_file():
                continue
            m = json.loads(manifest.read_text(encoding="utf-8"))
            rows = m.get("files", [])
            relative = path.relative_to(parent).as_posix()
            match = [r for r in rows if r.get("path") == relative]
            if match:
                if match[0]["sha256"] != sha(raw):
                    raise ValueError("Retained source hash mismatch: " + name)
                record["retained_manifest"] = manifest.relative_to(ROOT).as_posix()
                record["retained_manifest_sha256"] = sha(manifest.read_bytes())
                break
        if "retained_manifest" not in record:
            raise ValueError("Source lacks a matching retained manifest: " + name)
        sources[name] = record
        return json.loads(raw)

    def check(label, actual, expected, tolerance, source, selector):
        passed = abs(actual - expected) <= tolerance
        checks.append(
            {
                "id": label,
                "actual": actual,
                "printed_or_count_value": expected,
                "absolute_tolerance": tolerance,
                "status": "consistent" if passed else "mismatch",
                "source": source,
                "selector": selector,
                "scope": "Retained-value/count/rounding check, not a new numerical certificate",
            }
        )

    with ZipFile(args.packet) as z:
        members = [
            {"member": n, "bytes": len(z.read(n)), "sha256": sha(z.read(n))}
            for n in z.namelist()
            if not n.endswith("/")
        ]
        private = [r for r in members if "/for_audit/" in "/" + r["member"]]
        if len(private) != 10:
            raise ValueError("Expected ten private audit drafts")
    packet = {
        "filename": args.packet.name,
        "sha256": sha(args.packet.read_bytes()),
        "members": members,
        "private_text_in_output": False,
    }

    analyses = {}
    for study, rel in STUDIES.items():
        path = "research/studies/" + rel + "/ANALYSIS.json"
        analyses[study] = load(path)
        profiles = {"R1": 144, "R2": 216, "E1": 650, "S3": 168, "S4": 192, "S4b": 192}
        comparisons = {
            "R1": 240,
            "R2": 396,
            "E1": 1935,
            "S3": 254,
            "S4": 192,
            "S4b": 192,
        }
        check(
            study + ".profiles",
            analyses[study]["profile_rows"],
            profiles[study],
            0,
            path,
            "/profile_rows",
        )
        rows = analyses[study]["comparisons"]
        check(
            study + ".contrasts",
            len(rows),
            comparisons[study],
            0,
            path,
            "/comparisons length",
        )

    # Derive counts from signed rows, rather than trusting a report's totals.
    for study, kind, count in [
        ("R1", "mechanism", 72),
        ("R2", "functional_capacity", 72),
        ("R2", "construction_assistance", 72),
    ]:
        p = "research/studies/" + STUDIES[study] + "/ANALYSIS.json"
        rows = [r for r in analyses[study]["comparisons"] if r["kind"] == kind]
        check(
            study + "." + kind + ".count",
            len(rows),
            count,
            0,
            p,
            "comparisons filtered by kind=" + kind,
        )
        check(
            study + "." + kind + ".positive",
            sum(r["sign"] == 1 for r in rows),
            count,
            0,
            p,
            "same selection; sign=1",
        )
    for study, expected_flips in [("R1", 1), ("R2", 0)]:
        p = "research/studies/" + STUDIES[study] + "/ANALYSIS.json"
        check(
            study + ".cadence_flips",
            sum(r["strict_sign_flip"] for r in analyses[study]["corridor"]),
            expected_flips,
            0,
            p,
            "/corridor strict_sign_flip count",
        )
    # R2's nine horizon-flip groups are distinct from the cadence audit.
    groups = defaultdict(set)
    for r in analyses["R2"]["comparisons"]:
        groups[(r["id"], r["cadence"])].add(r["sign"])
    check(
        "R2.horizon_flips",
        sum(1 in v and -1 in v for v in groups.values()),
        9,
        0,
        "research/studies/" + STUDIES["R2"] + "/ANALYSIS.json",
        "group by comparison id,cadence; both signs across horizons",
    )

    e = analyses["E1"]
    ep = "research/studies/" + STUDIES["E1"] + "/ANALYSIS.json"
    for kind, count in [
        ("catalysis", 18),
        ("cross_assistance", 90),
        ("preparation", 45),
        ("factorial_interaction", 18),
    ]:
        rows = [
            r
            for r in e["comparisons"]
            if r["kind"] == kind and r["horizon"] == 4096 and r["cadence"] == 0.25
        ]
        check(
            "E1." + kind + ".count", len(rows), count, 0, ep, f"kind={kind},T4096,dt.25"
        )
        counts = Counter(r["sign"] for r in rows)
        for sign, expected in (
            {
                "catalysis": {1: 18},
                "cross_assistance": {1: 90},
                "preparation": {1: 30, -1: 15},
                "factorial_interaction": {1: 6, -1: 12},
            }[kind]
        ).items():
            check(
                f"E1.{kind}.sign{sign}",
                counts[sign],
                expected,
                0,
                ep,
                f"same selection; sign={sign}",
            )
        if kind in ("catalysis", "cross_assistance"):
            counts = Counter(
                q["resolved_sign"]
                for r in rows
                for q in r["delta_projected_histories"].values()
            )
            for sign, expected in (
                {"catalysis": {1: 36}, "cross_assistance": {1: 108, 0: 72}}[kind]
            ).items():
                check(
                    f"E1.{kind}.local_sign{sign}",
                    counts[sign],
                    expected,
                    0,
                    ep,
                    f"same selection; count A/B interval resolved_sign={sign}",
                )
    for study, cadence_flips, horizon_flips in [
        ("E1", 1, 44),
        ("S4", 0, 24),
        ("S4b", 11, 23),
    ]:
        d = analyses[study]
        audits = d.get("profiles", d.get("comparison_profiles"))
        p = "research/studies/" + STUDIES[study] + "/ANALYSIS.json"
        check(
            study + ".full_cadence_flips",
            sum(r["strict_sign_flip"] for r in audits["cadence_audit"]),
            cadence_flips,
            0,
            p,
            "cadence_audit strict_sign_flip count",
        )
        # Horizon audit entries expose brackets rather than a strict flag.
        check(
            study + ".full_horizon_flips",
            sum(bool(r["sign_change_brackets"]) for r in audits["horizon_audit"]),
            horizon_flips,
            0,
            p,
            "horizon_audit nonempty sign_change_brackets count",
        )

    s3 = analyses["S3"]
    sp = "research/studies/" + STUDIES["S3"] + "/ANALYSIS.json"
    fault = [
        r
        for r in s3["comparisons"]
        if r["study"] == "repair" and "-minus-intact" in r["id"]
    ]
    check(
        "S3.fault_intact_rows",
        len(fault),
        80,
        0,
        sp,
        "repair comparisons id contains -minus-intact",
    )
    check(
        "S3.fault_intact_positive",
        sum(r["sign"] == 1 for r in fault),
        80,
        0,
        sp,
        "same selection; sign=1",
    )
    check(
        "S3.foreclosure_rows",
        len(s3["foreclosure_comparisons"]),
        360,
        0,
        sp,
        "/foreclosure_comparisons length",
    )
    check(
        "S3.foreclosure_zero",
        sum(r["reference_weight"] == 0 for r in s3["foreclosure_comparisons"]),
        360,
        0,
        sp,
        "reference_weight == 0",
    )
    for source, printed in [
        ("S0p02_feedback", 0.459),
        ("S0p12_feedback", 0.351),
        ("S0p02_no_feedback", -2.326),
        ("S0p12_no_feedback", -3.717),
    ]:
        r = next(
            r
            for r in s3["comparisons"]
            if r["id"] == source + ":repair_fault-minus-access_fault"
            and r["cadence"] == 0.25
            and r["horizon"] == 4096
        )
        check(
            "S3.repair_contrast." + source,
            r["delta_ell_bits"],
            printed,
            0.0005,
            sp,
            source + ":repair_fault-minus-access_fault,T4096,dt.25",
        )
    r = next(
        r
        for r in s3["comparisons"]
        if r["id"] == "one_way-minus-local"
        and r["cadence"] == 0.25
        and r["horizon"] == 16
    )
    check(
        "S3.whole_early",
        r["delta_ell_bits"],
        0.926,
        0.0005,
        sp,
        "one_way-minus-local,T16,dt.25",
    )
    for part, values in [("A", [-0.656, -0.060]), ("B", [0.794, 1.357])]:
        for bound, printed in zip(["lower", "upper"], values):
            check(
                "S3." + part + "." + bound,
                r["delta_projected_histories"][part][bound],
                printed,
                0.0005,
                sp,
                f"one_way-minus-local,T16,dt.25,part={part},{bound}",
            )

    for study, blocked in [("S4", 9.49), ("S4b", 18.45)]:
        path = "research/studies/" + STUDIES[study] + "/ANALYSIS.json"
        d = analyses[study]
        for suffix in ["TX-minus-T0", "RX-minus-R0"]:
            rows = [r for r in d["comparisons"] if r["id"].endswith(suffix)]
            check(
                study + "." + suffix + ".positive",
                sum(r["sign"] == 1 for r in rows),
                48,
                0,
                path,
                suffix + ", all declared arms/cadences/horizons",
            )
        r = next(
            r
            for r in d["comparisons"]
            if r["id"] == "blocked:TX-minus-T0"
            and r["cadence"] == 0.25
            and r["horizon"] == 1024
        )
        check(
            study + ".blocked_response",
            r["delta_ell_bits"],
            blocked,
            0.005,
            path,
            "blocked:TX-minus-T0,T1024,dt.25",
        )
    bp = "research/studies/" + STUDIES["S4b"] + "/SIGNAL_RESPONSE_INTERACTION.json"
    bi = load(bp)
    for environment, printed in [
        ("blocked", -1.57),
        ("slow", 1.30),
        ("fast", 2.71),
        ("open", 5.70),
    ]:
        r = next(
            r
            for r in bi["profiles"]
            if r["environment"] == environment
            and r["horizon"] == 1024
            and r["cadence"] == 0.25
        )
        check(
            "S4b.interaction." + environment,
            r["delta_ell_bits"],
            printed,
            0.005,
            bp,
            environment + ",T1024,dt.25",
        )

    p0 = load(P0 + "/SUMMARY.json")
    for k, v in [
        ("native_replayed_rows", 252),
        ("headline_contrast_rows", 61),
        ("native_history_max_difference_bits", 0),
        ("current_history_max_difference_bits", 0),
        ("native_projection_max_difference_bits", 0),
    ]:
        check("P0." + k, p0[k], v, 0, P0 + "/SUMMARY.json", "/" + k)
    printed = {
        "R1": [5.8, 11.2, 140.9],
        "R2": [0.03, 2.01, 27.94],
        "E1": [1.19, 7.47, 102.66],
        "S3": [0.93, 3.51, 29.82],
        "S4": [0.94, 2.57, 10.16],
        "S4b": [-0.07, -0.89, 5.70],
    }
    rates = {
        "R1": 0.136,
        "R2": 0.0102,
        "E1": 0.098,
        "S3": 0.0245,
        "S4": 0.0050,
        "S4b": 0.0057,
    }
    tails = {}
    for s in p0["studies"]:
        study = s["study"]
        for t, value in zip([16, 64, 1024], printed[study]):
            r = next(
                r
                for r in s["profile_map"]
                if r["cadence"] == 0.25 and r["horizon"] == t
            )
            check(
                study + ".replay.T" + str(t),
                r["delta_bits"],
                value,
                0.05 if study == "R1" else 0.005,
                P0 + "/SUMMARY.json",
                f"study={study},profile_map,T{t},dt.25",
            )
        tail = next(r for r in s["analytical_tail"] if r["cadence"] == 0.25)
        check(
            study + ".replay_rate",
            tail["delta_rate_bits_per_time"],
            rates[study],
            0.0005 if study in ["R1", "E1"] else 0.00005,
            P0 + "/SUMMARY.json",
            f"study={study},analytical_tail,dt.25",
        )
        tails[study] = s["analytical_tail"]
    pq = load(PQ + "/SUMMARY.json")
    check(
        "PQ.paired_checks",
        sum(s["paired_checks"] for s in pq["studies"]),
        14,
        0,
        PQ + "/SUMMARY.json",
        "/studies paired_checks sum",
    )

    result = load(A + "/history/RESULT.json")
    summary = load(A + "/SUMMARY.json")
    calibration = load(A + "/physical/CALIBRATION.json")
    check(
        "A.rows", len(result["rows"]), 96, 0, A + "/history/RESULT.json", "/rows length"
    )
    check(
        "A.contrasts",
        len(result["comparisons"]),
        72,
        0,
        A + "/history/RESULT.json",
        "/comparisons length",
    )
    check(
        "A.paired",
        sum(
            r["certificate"]["status"] == "validated_paired_comparison"
            for r in result["paired_contracts"]
        ),
        72,
        0,
        A + "/history/RESULT.json",
        "/paired_contracts status count",
    )
    for control, values in [
        ("activity_matched", [1.21, -0.02, -0.47, 10.41]),
        ("net_work_matched", [5.63, 10.71, 34.09, 134.95]),
    ]:
        for t, printed_value in zip([16, 64, 256, 1024], values):
            r = next(
                r
                for r in result["comparisons"]
                if r["control"] == control
                and r["source_on"]
                and r["cadence"] == 0.25
                and r["horizon"] == t
            )
            check(
                f"A.{control}.T{t}",
                r["productive_minus_control_bits"],
                printed_value,
                0.005,
                A + "/history/RESULT.json",
                f"{control},source_on,dt.25,T{t}",
            )
        for dt, printed_value in zip(
            [0.125, 0.25, 0.5],
            {
                "activity_matched": [0.013, 0.014, 0.016],
                "net_work_matched": [0.159, 0.131, 0.101],
            }[control],
        ):
            r = next(
                r
                for r in result["comparisons"]
                if r["control"] == control and r["source_on"] and r["cadence"] == dt
            )
            check(
                f"A.{control}.rate.{dt}",
                r["delta_rate_bits_per_time"],
                printed_value,
                0.0005,
                A + "/history/RESULT.json",
                f"{control},source_on,dt{dt},rate",
            )
    source_off = next(
        r
        for r in result["comparisons"]
        if r["control"] == "activity_matched"
        and not r["source_on"]
        and r["cadence"] == 0.25
        and r["horizon"] == 1024
    )
    check(
        "A.source_off.T1024",
        source_off["productive_minus_control_bits"],
        30.7,
        0.05,
        A + "/history/RESULT.json",
        "activity_matched,source_off,dt.25,T1024",
    )
    check(
        "A.source_off.rate",
        source_off["delta_rate_bits_per_time"],
        -0.014,
        0.0005,
        A + "/history/RESULT.json",
        "same selection,rate",
    )
    # Preserve contrary profile information as observations, not failed checks.
    activity_profiles = []
    for dt in [0.125, 0.25, 0.5]:
        r = next(
            r
            for r in result["comparisons"]
            if r["control"] == "activity_matched"
            and r["source_on"]
            and r["cadence"] == dt
        )
        intervals = r["observed_crossing_step_intervals"]
        activity_profiles.append(
            {
                "cadence": dt,
                "step_brackets": intervals,
                "physical_time_brackets": [[dt * a, dt * b] for a, b in intervals],
                "positive_at_four_headline_endpoints": all(
                    q["productive_minus_control_bits"] > 0
                    for q in result["comparisons"]
                    if q["control"] == "activity_matched"
                    and q["source_on"]
                    and q["cadence"] == dt
                ),
            }
        )
    # R1 preparation values cited in chapter 18 and the common bank account.
    rp = "research/studies/" + STUDIES["R1"] + "/ANALYSIS.json"
    for t, printed_value in [(16, 5.78), (1024, 33.26)]:
        r = next(
            r
            for r in analyses["R1"]["comparisons"]
            if r["context"] == "driven__intact:built-minus-unassembled"
            and r["horizon"] == t
            and r["cadence"] == 0.25
        )
        check(
            "R1.preparation.T" + str(t),
            r["delta_ell_bits"],
            printed_value,
            0.005,
            rp,
            f"driven__intact:built-minus-unassembled,T{t},dt.25",
        )
    rawpath = "research/studies/" + STUDIES["R1"] + "/cases/driven__intact__dt0p25.json"
    raw = load(rawpath)
    built = next(
        r for r in raw["rows"] if r["preparation"] == "built" and r["horizon"] == 1024
    )
    r1_function = built["function"]
    # S3's offset range needs an explicit cadence qualifier in prose.
    s3_ranges = {}
    for dt in [0.125, 0.25, 0.5]:
        vals = [
            r["delta_ell_bits"]
            for r in fault
            if r["horizon"] == 4096 and r["cadence"] == dt
        ]
        s3_ranges[str(dt)] = {
            "rows": len(vals),
            "minimum_bits": min(vals),
            "maximum_bits": max(vals),
        }
    # Version-scope counts: distinguish unique laws from law/cadence cases.
    r1m = analyses["R1"]["case_metadata"]
    r2m = analyses["R2"]["case_metadata"]
    structural_counts = {
        "R1_laws": len({r["law"] for r in r1m}),
        "R2_laws": len({r["law"] for r in r2m}),
        "S3_repair_unique_laws": len(
            {r["law"] for r in s3["case_checks"] if r["study"] == "repair"}
        ),
        "S3_repair_law_cadence_cases": sum(
            r["study"] == "repair" for r in s3["case_checks"]
        ),
    }
    ep = "research/studies/" + STUDIES["E1"] + "/PROTOCOL.json"
    protocol = load(ep)
    for label, actual, expected in [
        ("laws", len(protocol["laws"]), 45),
        ("law_cadence_cases", len(protocol["case_grid"]), 65),
        (
            "source_off_laws",
            sum(r["regime"]["source"] == 0 for r in protocol["laws"]),
            5,
        ),
    ]:
        check("E1.protocol." + label, actual, expected, 0, ep, label)
    sp4 = "research/studies/" + STUDIES["S4"] + "/OPEN_PROTOCOL.json"
    prot4 = load(sp4)
    rules = {r["id"]: r for r in prot4["laws"][0]["model"]["rules"]}
    check(
        "S4.exposed_write_multiplier",
        rules["signal_write_0_1"]["conductance"]
        / rules["signal_write_0_0"]["conductance"],
        15,
        0,
        sp4,
        "tracking law exposed/nonexposed write conductance ratio",
    )
    for label, expected in [
        ("S3_repair_unique_laws", 4),
        ("S3_repair_law_cadence_cases", 8),
    ]:
        check(
            label,
            structural_counts[label],
            expected,
            0,
            sp,
            "/case_checks, distinct laws versus law/cadence cases",
        )
    for study in ["S4", "S4b"]:
        dp = "research/studies/" + STUDIES[study] + "/SIGNAL_DIAGNOSTICS.json"
        diag = load(dp)
        values = [
            r["signal_exposed_hazard_mi_bits"]["stationary"]
            for r in diag["profiles"]
            if r["law"].endswith("T0")
        ]
        structural_counts[study + "_tracking_MI_range_bits"] = [
            min(values),
            max(values),
        ]
    ap = A + "/history/RESULT.json"
    for row in activity_profiles:
        check(
            "A.activity_crossing_count." + str(row["cadence"]),
            len(row["step_brackets"]),
            3,
            0,
            ap,
            f"activity_matched,source_on,dt{row['cadence']},observed_crossing_step_intervals",
        )
    paired_profiles = {
        p["arm"]: {r["physical_duration"]: r["ell_bits"] for r in p["profile"]}
        for p in result["profiles"]
        if p["cadence"] == 0.5
        and p["source_on"]
        and p["arm"] in ["productive", "activity_matched"]
    }
    negative_witness = (
        paired_profiles["productive"][124.0]
        - paired_profiles["activity_matched"][124.0]
    )
    check(
        "A.coarse_intermediate_negative_witness",
        negative_witness,
        -0.102226,
        0.0000005,
        ap,
        "profiles,dt.5,T124,productive-minus-activity_matched",
    )
    args.out.mkdir(parents=True)

    def write(name, value):
        (args.out / name).write_text(
            json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
            encoding="utf-8",
        )

    write(
        "SOURCE_INPUTS.json",
        {"packet": packet, "retained_sources": list(sources.values())},
    )
    write(
        "NUMERICAL_CHECKS.json",
        {
            "checks": checks,
            "count": len(checks),
            "mismatches": [r for r in checks if r["status"] == "mismatch"],
        },
    )
    write(
        "PROFILE_SCOPE.json",
        {
            "activity_contrasts": activity_profiles,
            "source_off": source_off,
            "s3_offset_ranges": s3_ranges,
            "structural_counts": structural_counts,
            "coarse_intermediate_negative_witness_bits": negative_witness,
            "r1_built_T1024_function": r1_function,
            "p0_tail_records": tails,
            "original_A_max_first_law_residual": summary["max_energy_balance_residual"],
            "original_A_matching_targets": calibration["target"]["stationary"],
            "scope": "Read-only retained data, no rescoring; not a rounding, physical-faithfulness or all-horizon certificate",
        },
    )
    print(
        json.dumps(
            {
                "checks": len(checks),
                "mismatches": sum(r["status"] == "mismatch" for r in checks),
                "source_files": len(sources),
                "private_drafts": len(private),
                "simulation_started": False,
            }
        )
    )


    if any(r["status"] == "mismatch" for r in checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
