"""Reanalyse retained R2 with explicit structural and functional diagnostics.

No new law, parameter selection or history-score run. Original evidence stays
byte-for-byte intact. Added functional queries replay the retained native law.
"""

import argparse
import json
import shutil
import sys
from hashlib import sha256
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from omega_cosmology.testbed.analysis import comparison_profiles
from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.ecology import (
    compile_functional_query,
    evaluate_functional_query,
)
from omega_cosmology.testbed.history import distributions_and_occupation
from omega_cosmology.testbed.physics import LocalModel
from omega_cosmology.testbed.structure import paired_state_probe, transition_audit


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def condition(field, op, value):
    return {"coordinate": field, "operator": op, "value": value}


def main():
    if sys.stdin.readline().strip() != "GO":
        raise RuntimeError("Run under the capped supervisor with a GO handshake")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    out = args.out_dir.resolve()
    if out.exists() or not out.is_relative_to(ROOT / "runs"):
        parser.error("Choose a fresh output directory under runs/")
    retained = ROOT / "research/studies/R2-further-capacity/results-2026-10-24"
    evidence = json.loads((retained / "EVIDENCE.json").read_text())
    for f in evidence["files"]:
        if digest(retained / f["path"]) != f["sha256"]:
            raise RuntimeError("Retained evidence changed")
    protocol = json.loads((retained / "PROTOCOL.json").read_text())
    analysis = json.loads((retained / "ANALYSIS.json").read_text())
    profiles = comparison_profiles(
        analysis["comparisons"], analysis["sign_deadband_bits"]
    )
    functional_spec = {
        "id": "bound_assembly",
        "definition": "Both constituents joined by the native bond",
        "coordinates": ["bond"],
        "functional_any_of": [[condition("bond", "eq", 1)]],
    }
    diagnostic_specs, audits, functions = {}, [], []
    for law in protocol["laws"]:
        model = LocalModel.from_record(law["model"])
        roots = [tuple(s) for p in protocol["preparations"] for s, _ in p["roots"]]
        c = enumerate_model(model, roots, max_states=1000)
        retained_case = json.loads(
            (retained / f"cases/{law['id']}__dt0p25.json").read_text()
        )
        if (
            c.model_hash != retained_case["model_hash"]
            or c.generator_hash != retained_case["generator_hash"]
        ):
            raise RuntimeError("Reconstructed law differs from retained generator")
        store_rules = [r.id for r in model.rules if r.id.startswith("build_store")]
        route_specs = [
            {
                "id": "store_dissolution_with_loaded_bank",
                "when": [condition("store.built", "eq", 1), condition("bank", "ge", 3)],
                "selector": {"rules": store_rules, "direction": -1},
            },
            {
                "id": "capture_without_active_apparatus",
                "when": [
                    condition("a.active", "eq", 0),
                    condition("b.active", "eq", 0),
                    condition("carrier", "eq", 2),
                    condition("bank", "le", 2),
                ],
                "selector": {"rules": ["capture"], "direction": 1},
            },
            {
                "id": "direct_deactivation_while_bound",
                "when": [condition("bond", "eq", 1)],
                "selector": {
                    "rules": [
                        "basal_activate_a.active",
                        "basal_activate_b.active",
                        "paid_activate_a.active",
                        "paid_activate_b.active",
                    ],
                    "direction": -1,
                },
            },
        ]
        probe_specs = [
            {
                "id": "unlock_with_without_bond",
                "when": [condition("bond", "eq", 1), condition("carrier", "eq", 1)],
                "replace": {"bond": 0},
                "selector": {"rules": ["unlock_basal", "unlock_motif"], "direction": 1},
            },
        ]
        diagnostic_specs[law["id"]] = {
            "transition_audits": route_specs,
            "paired_state_probes": probe_specs,
        }
        audits.append(
            {
                "law": law["id"],
                "transition_audits": [transition_audit(c, s) for s in route_specs],
                "paired_state_probes": [paired_state_probe(c, s) for s in probe_specs],
            }
        )
        query = compile_functional_query(c, functional_spec)
        for prep in protocol["preparations"]:
            mu = np.zeros(len(c.states))
            for state, weight in prep["roots"]:
                mu[c.index[tuple(state)]] += weight
            for T in protocol["horizons"]:
                endpoint, occupation = distributions_and_occupation(c, mu, T)
                functions.append(
                    {
                        "law": law["id"],
                        "preparation": prep["id"],
                        **evaluate_functional_query(query, mu, T, endpoint, occupation),
                    }
                )
    result = {
        "schema": "omega.structural-reanalysis/1",
        "date": "2026-10-25",
        "source_evidence_sha256": digest(retained / "EVIDENCE.json"),
        "interpretation_status": "posthoc_explanatory_audit",
        "new_law_runs": 0,
        "profiles": profiles,
        "structural_audits": audits,
        "functional_profiles": functions,
        "functional_query_spec": functional_spec,
        "structural_query_specs": diagnostic_specs,
        "limits": "No enabling ancestry, intervention experiment, repair necessity or microscopic faithfulness established",
    }
    cadence_flips = sum(r["strict_sign_flip"] for r in profiles["cadence_audit"])
    horizon_flips = sum(r["strict_sign_flip"] for r in profiles["horizon_audit"])
    selected = [
        r
        for r in profiles["horizon_audit"]
        if r["cadence"] == 0.25 and r["strict_sign_flip"]
    ]
    lines = ["| Comparison | T16 | T64 | T256 | T1024 |", "|---|---:|---:|---:|---:|"]
    for r in selected:
        lines.append(
            "| "
            + r["id"]
            + " | "
            + " | ".join(f"{p['delta_ell_bits']:+.6f}" for p in r["points"])
            + " |"
        )
    function_lines = [
        "| Law | Initial function | Endpoint | Never lost | Lost and returned | Returned and functional now | Entries | Exits |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in functions:
        if r["preparation"] == "assembly_seed" and r["horizon"] == 1024:
            keys = [
                "initial_functional_probability",
                "endpoint_functional_probability",
                "uninterrupted_initial_function_probability",
                "initial_function_lost_then_returned_probability",
                "returned_and_functional_at_deadline_probability",
                "expected_entries",
                "expected_exits",
            ]
            function_lines.append(
                "| " + r["law"] + " | " + " | ".join(f"{r[k]:.6g}" for k in keys) + " |"
            )
    report = f"""# R2 structural reanalysis — 25 October 2026

Post-hoc audit of unchanged retained physics and scores. No new parameter/law
study and no new empirical replication. Original numerical reports remain sealed.
New functional queries run on generators verified against the retained hashes.

## Cadence and horizon are separate axes

{cadence_flips} strict cadence flips; {horizon_flips} comparison/cadence groups
with horizon sign changes. At cadence .25:

{chr(10).join(lines)}

Brackets locate sign changes only between sampled horizons; no exact roots or
absence of other crossings is certified. Interval accumulation differences are
in ANALYSIS.json, separate from stationary rates.

## Structural audit findings

- Store dissolution via the paired refund routes is absent at bank ticks 3–6.
  Charging therefore protects the store against these routes. Spill is absent.
- Capture occurs with both apparatus constituents inactive. Unlocking has a
  basal route: assembly increases its rate, rather than being strictly necessary.
- Active constituents cannot deactivate while bound; they must first unbind.
  Upkeep changes only the bank and does not preserve or restore function.
- The first-episode monitor accepts basal construction and native capture. It
  establishes event ordering, not enabling ancestry or autocatalytic closure.
- The prebuilt root reallocates .5 bank energy to store energy. Actual building
  spends 1 and dissipates .5; it is not the paid outcome from the assembly root.

Structural counts are counts of reachable states, not occupancy probabilities.
Paired state probes do not enact removal or claim matched energy. All native
thermal routes stay in the physical total.

## Function has several distinct profiles

Function here means bound assembly. Probabilities below are unconditional.
Initially nonfunctional paths cannot count as loss-and-return of initial function.
Re-entry is not proof of paid repair, genealogy or retained identity.
Assembly-seed preparation, T1024:

{chr(10).join(function_lines)}

The ledger preserves all original lushness differences. The corrected claim is
bounded capacity use under the stipulated rules, with the highlighted physical
limits; it does not establish self-maintenance necessity or recursive ancestry.
"""
    out.mkdir(parents=True)
    (out / "ANALYSIS.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n"
    )
    (out / "REPORT.md").write_text(report, encoding="utf-8")
    sources = sorted((ROOT / "src/omega_cosmology/testbed").glob("*.py")) + [
        Path(__file__).resolve()
    ]
    for source in sources:
        target = out / "source" / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    files = [
        {
            "path": p.relative_to(out).as_posix(),
            "sha256": digest(p),
            "bytes": p.stat().st_size,
        }
        for p in sorted(out.rglob("*"))
        if p.is_file()
    ]
    (out / "EVIDENCE.json").write_text(
        json.dumps(
            {
                "schema": "omega.reanalysis-evidence/1",
                "source_evidence_sha256": result["source_evidence_sha256"],
                "files": files,
            },
            indent=2,
        )
        + "\n"
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "cadence_flips": cadence_flips,
                "horizon_flip_groups": horizon_flips,
                "functional_queries": len(functions),
                "max_marginal_residual": max(
                    r["physical_marginal_residual"] for r in functions
                ),
            }
        )
    )


if __name__ == "__main__":
    main()
