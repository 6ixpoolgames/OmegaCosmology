"""Attach physical signal diagnostics and byte-exact calibration to signed runs."""

import argparse
import json
import math
import shutil
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

from restore_research_snapshot import write_archive

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def binary_information(s, h, both):
    joint = [both, s - both, h - both, 1 - s - h + both]
    product = [s * h, s * (1 - h), (1 - s) * h, (1 - s) * (1 - h)]
    if min(joint) < -1e-10 or max(joint) > 1 + 1e-10:
        raise ArithmeticError("Invalid physical joint distribution")
    return sum(p * math.log2(p / q) for p, q in zip(joint, product) if p > 0 and q > 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", required=True, type=Path)
    parser.add_argument("--calibration-run", required=True, type=Path)
    args = parser.parse_args()
    study = args.study.resolve()
    results = study / "results-2026-10-26"
    calibration = args.calibration_run.resolve()
    if not study.is_relative_to(ROOT / "research/studies"):
        parser.error("Use a retained study")
    retained = results / "calibration"
    retained.mkdir(exist_ok=True)
    manifest = read(calibration / "frozen/MANIFEST.json")
    sources = {}
    for r in manifest["files"]:
        source = (calibration / "frozen" / r["path"]).resolve()
        if (
            not source.is_relative_to(calibration / "frozen")
            or digest(source) != r["sha256"]
        ):
            raise ValueError("Calibration source mismatch")
        sources[r["path"]] = source.read_bytes()
    sources["MANIFEST.json"] = (calibration / "frozen/MANIFEST.json").read_bytes()
    if not (retained / "SNAPSHOT.zip").exists():
        write_archive(retained / "SNAPSHOT.zip", sources)
    else:
        with ZipFile(retained / "SNAPSHOT.zip") as archive:
            if set(archive.namelist()) != set(sources) or any(
                archive.read(k) != v for k, v in sources.items()
            ):
                raise ValueError("Retained calibration archive changed")
    for name in ("CALIBRATION.json", "CALIBRATION_RECEIPT.json"):
        shutil.copyfile(calibration / name, retained / name)
        if (study / name).read_bytes() != (retained / name).read_bytes():
            raise ValueError("Retained calibration mismatch")
    log = (calibration / "worker.log").read_text(encoding="utf-8")
    (retained / "worker.log").write_text(
        log.replace(str(ROOT), "<repo>").replace(ROOT.as_posix(), "<repo>"),
        encoding="utf-8",
    )
    analysis = read(results / "ANALYSIS.json")
    profiles = []
    raw = []
    for group in ("dynamic", "open"):
        for path in sorted((results / group).glob("*/RESULT.json")):
            raw.extend(read(path)["rows"])
    for r in raw:
        information = {}
        for kind, divisor in [
            ("endpoint", 1),
            ("integrated", r["horizon"]),
            ("stationary", 1),
        ]:
            o = r["observables"]
            information[kind] = binary_information(
                o["signal_on"][kind] / divisor,
                o["exposed_hazard"][kind] / divisor,
                o["signal_and_exposed_hazard"][kind] / divisor,
            )
        ev = r["event_readouts"]
        switches = sum(
            v
            for k, v in ev.items()
            if k.startswith(("signal_write_", "signal_relax_", "signal_reset_"))
        )
        profiles.append(
            {
                "law": r["law"],
                "horizon": r["horizon"],
                "cadence": r["cadence"],
                "signal_exposed_hazard_mi_bits": information,
                "physical_signal_switches": switches,
                "net_effort_heat": 0.5
                * sum(
                    ev.get(k + "_forward", 0) - ev.get(k + "_reverse", 0)
                    for k in ("escape", "blocked_effort")
                ),
                "net_signal_bank_use_energy": ev["signal_write_forward"]
                - ev["signal_write_reverse"]
                + 0.5
                * (
                    ev["signal_upkeep_forward"]
                    - ev["signal_upkeep_reverse"]
                    + ev.get("signal_reset_forward", 0)
                    - ev.get("signal_reset_reverse", 0)
                ),
                "scope": "Information and channel flux diagnostics, never added to/subtracted from lushness",
            }
        )
    write(
        results / "SIGNAL_DIAGNOSTICS.json",
        {
            "profiles": profiles,
            "information_scope": "Dependence on contemporaneous exposed hazard; integrated entry is joint occupancy for a uniformly sampled physical instant, not average per-instant MI",
            "formal_future_breadth_tracking_T": {
                "status": "not_computed",
                "reason": "This is a functional warning proxy, not a certified T-and-D suffering instantiation",
            },
            "learned_helplessness": "not_modeled",
            "phenomenal_valence": "not_modeled",
        },
    )
    primary = [c for c in analysis["comparisons"] if c["cadence"] == 0.25]
    interactions = []
    keys = sorted(
        {
            (c["id"].split(":")[0], c["horizon"], c["cadence"])
            for c in analysis["comparisons"]
        }
    )
    for env, T, dt in keys:
        contrasts = {
            c["id"].split(":")[1]: c
            for c in analysis["comparisons"]
            if c["id"].split(":")[0] == env and c["horizon"] == T and c["cadence"] == dt
        }
        delta = (
            contrasts["TX-minus-T0"]["delta_ell_bits"]
            - contrasts["RX-minus-R0"]["delta_ell_bits"]
        )
        interactions.append(
            {
                "environment": env,
                "horizon": T,
                "cadence": dt,
                "delta_ell_bits": delta,
                "formula": "(TX-T0)-(RX-R0)",
                "scope": "Declared four-mechanism signal/response interaction; two moments matched, not entire sensor histories or bills",
            }
        )
    write(
        results / "SIGNAL_RESPONSE_INTERACTION.json",
        {
            "profiles": interactions,
            "comparison_kind": "factorial mechanism contrast",
            "uncertainty": "whole-model float64",
        },
    )
    lines = [
        "# Warning/response physical diagnostics",
        "",
        "All values below are response-on minus response-off within the same environment.",
        "Whole bits are complete sampled histories; body intervals use non-Markov projected bounds.",
        "",
        "| Environment | T | Whole bits | Body interval | Working time | Sheltered time | Endpoint bank energy |",
        "|---|---:|---:|---|---:|---:|---:|",
    ]
    for c in primary:
        if not c["id"].endswith("TX-minus-T0"):
            continue
        b = c["delta_projected_histories"]["body"]
        lines.append(
            f"| {c['id'].split(':')[0]} | {c['horizon']} | {c['delta_ell_bits']:.6f} | [{b['lower']:.6f}, {b['upper']:.6f}] | "
            f"{c['delta_functional_profiles']['body']['integrated_functional_time']:.6f} | "
            f"{c['delta_observables']['sheltered']['integrated']:.6f} | {c['delta_observables']['bank_energy']['endpoint']:.6f} |"
        )
    lines += [
        "",
        "## Stationary tracking diagnostic",
        "",
        "Mutual information of the bit and contemporaneous exposed hazard; bits. This does not establish the formal future-breadth T test.",
        "",
        "| Law | Signal/exposure MI |",
        "|---|---:|",
    ]
    for p in profiles:
        if p["cadence"] == 0.25 and p["horizon"] == 1024:
            lines.append(
                f"| {p['law']} | {p['signal_exposed_hazard_mi_bits']['stationary']:.9f} |"
            )
    cadence_flips = sum(
        c["strict_sign_flip"] for c in analysis["profiles"]["cadence_audit"]
    )
    horizon_flips = sum(
        c["strict_sign_flip"] for c in analysis["profiles"]["horizon_audit"]
    )
    lines += [
        "",
        "## Signal-response interaction",
        "",
        "(TX-T0)-(RX-R0): change in response value with exposure-linked rather than independent writing/resetting. Two physical moments are matched, not full paths or realized costs.",
        "",
        "| Environment | T | dt0.125 | dt0.25 | dt0.5 |",
        "|---|---:|---:|---:|---:|",
    ]
    for env, T in sorted({(v["environment"], v["horizon"]) for v in interactions}):
        values = [
            next(
                v["delta_ell_bits"]
                for v in interactions
                if v["environment"] == env and v["horizon"] == T and v["cadence"] == dt
            )
            for dt in (0.125, 0.25, 0.5)
        ]
        lines.append(
            f"| {env} | {T} | " + " | ".join(f"{v:.6f}" for v in values) + " |"
        )
    lines += [
        "",
        f"Whole-history cadence flips on the sampled grid: {cadence_flips}; horizon-flip groups: {horizon_flips}.",
        "No claim of no crossing between sampled points, physical faithfulness or subjective suffering follows.",
        "Same-root mechanism contrasts can differ in limiting rate. A stationary rate is not a finite-horizon verdict.",
        "The body can recover through native routes; no permanent death or structural channel closure is present.",
    ]
    (results / "SIGNAL_DIAGNOSTICS.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    write(
        results / "QUALITY.json",
        {
            "schema": "omega.evidence-quality-axes/1",
            "numerical": {
                "kind": "finite exact-state float64, not interval arithmetic",
                "kernel_max_residual": max(
                    c["kernel_residual"] for c in analysis["case_checks"]
                ),
                "max_energy_residual": max(
                    abs(r["physical"]["energy_residual"]) for r in raw
                ),
                "max_history_residual": max(
                    r["validation"]["history_accumulation_residual"] for r in raw
                ),
                "all_cases_passed_equilibrium": all(
                    c["equilibrium_audit"]["status"] == "passed"
                    for c in analysis["case_checks"]
                ),
            },
            "resolution": {
                "cadences": [0.125, 0.25, 0.5],
                "whole_grid_flips": cadence_flips,
                "body_and_merged": "analytic memory bounds in float64; unresolved is not a tie",
                "finest_faithful": "open; records of signal state not explicitly constructed",
            },
            "physical_faithfulness": {
                "model": "stipulated reversible maintained warning/response proxy",
                "unknown": [
                    "physiological calibration",
                    "phenomenal valence",
                    "unresolved bath/source histories",
                ],
            },
            "claim_relevance": {
                "direct": "functional signal-response/access relation",
                "not_established": [
                    "formal T-and-D suffering instantiation",
                    "felt suffering intrinsically narrowing",
                    "learned helplessness",
                    "anaesthesia",
                    "factory farming",
                ],
            },
            "profiles": len(raw),
            "comparisons": len(analysis["comparisons"]),
            "foreclosure": {
                "cross_law": "not_computed",
                "reversible_body_sector": "recovery remains possible; no structural permanent-loss claim",
            },
        },
    )
    shutil.copyfile(__file__, results / Path(__file__).name)
    write(
        results / "EVIDENCE.json",
        {
            "schema": "omega.signed-studies-evidence/1",
            "files": [
                {
                    "path": p.relative_to(results).as_posix(),
                    "sha256": digest(p),
                    "bytes": p.stat().st_size,
                }
                for p in sorted(results.rglob("*"))
                if p.is_file() and p.name != "EVIDENCE.json"
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "profiles": len(raw),
                "cadence_flips": cadence_flips,
                "horizon_flips": horizon_flips,
            }
        )
    )


if __name__ == "__main__":
    main()
