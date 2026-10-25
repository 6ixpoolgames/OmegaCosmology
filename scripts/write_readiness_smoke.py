"""Materialize paid-readiness engineering inputs; do not run a scientific map."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from write_coupled_smoke_plan import case, cond

from omega_cosmology.testbed.physics import rational
from omega_cosmology.testbed.readiness import POLICIES, readiness_root, readiness_world


def protocol(model, *, policy, quantum, effort):
    root = readiness_root(model)
    p = case("readiness." + policy, model, root, [])["protocol"]
    p["max_states"] = 2000
    p["max_dense_bytes"] = 128 * 1024**2
    p["max_occupation_dense_bytes"] = 1024**3
    p["boundary_scope"]["bath_beta"] = model.beta
    p["sufficiency"] = (
        "Body, energetic warning/failure/cue registers, bank, carrier, hazard and native opportunity barrier retained"
    )
    p["scope"] = (
        "Engineering readiness only; noisy physical mechanisms, recoverable damage, no learned optimum, mortality or phenomenal suffering"
    )
    bill_ratio = rational(effort) / rational(quantum)
    if bill_ratio.denominator != 1:
        raise ValueError("Readiness query requires the model's exact effort bill")
    bank_ticks = int(bill_ratio)
    full_body = [c.name for c in model.coordinates if c.owner == "body"]
    p["projected_histories"] = [
        {
            "id": "body_full.m0",
            "coordinates": full_body,
            "conditioning": "full_present",
            "memory": 0,
            "max_workspace_bytes": 32 * 1024**2,
        },
        {
            "id": "body_core.m1",
            "coordinates": [
                "body.working",
                "body.bank",
                "body.location",
                "body.signal",
            ],
            "conditioning": "full_present",
            "memory": 1,
            "max_workspace_bytes": 128 * 1024**2,
        },
    ]
    p["structural_analysis"] = {
        "ancestry": [],
        "max_functional_query_states": 8000,
        "organizations": [
            {
                "id": "working",
                "definition": "Working apparatus irrespective of response registers",
                "coordinates": ["body.working"],
                "functional_any_of": [[cond("body.working", "eq", 1)]],
            },
            {
                "id": "sheltered",
                "definition": "Body at sheltered location, via any native route",
                "coordinates": ["body.location"],
                "functional_any_of": [[cond("body.location", "eq", 1)]],
            },
        ],
    }
    p["observables"] = [
        {"id": "bank_energy", "terms": [["body.bank", float(quantum)]]},
        {"id": "failure_marks", "terms": [["body.failures", 1]]},
    ]
    predicates = {
        "empty_bank": [cond("body.bank", "eq", 0)],
        "repair_unfunded": [cond("body.bank", "le", int(1 / float(quantum)) - 1)],
        "ready": [cond("body.working", "eq", 1), cond("body.bank", "ge", bank_ticks)],
        "memory_saturated": [
            cond(
                "body.failures",
                "eq",
                max(model.domains[model.indices["body.failures"]]),
            )
        ],
        "cue_on": [cond("body.cue", "eq", 1)],
        "cue_and_open": [cond("body.cue", "eq", 1), cond("barrier", "eq", 1)],
        "barrier_open": [cond("barrier", "eq", 1)],
        "cue_and_closed": [cond("body.cue", "eq", 1), cond("barrier", "eq", 0)],
    }
    p["observables"] += [
        {"id": name, "constant": 1, "conditions": cs} for name, cs in predicates.items()
    ]
    groups = {
        "escape": [r.id for r in model.rules if r.id.startswith("escape_")],
        "blocked_effort": [
            r.id for r in model.rules if r.id.startswith("blocked_effort_")
        ],
        "effort_damage": [
            r.id for r in model.rules if r.id.startswith("effort_damage_")
        ],
        "cue_clear": [r.id for r in model.rules if r.id.startswith("cue_clear_")],
        "memory_relax": [
            r.id for r in model.rules if r.id.startswith("failure_relax_")
        ],
        "cue_write": [r.id for r in model.rules if r.id.startswith("cue_write_")],
        "cue_reset": [r.id for r in model.rules if r.id.startswith("cue_reset_")],
        "low_reserve_damage": ["low_reserve_damage"],
        "paid_restore": ["paid_restore"],
        "capture": ["capture_0", "capture_1"],
    }
    p["event_readouts"] = [
        {
            "id": name + ("_forward" if direction == 1 else "_reverse"),
            "selectors": [{"rules": ids, "direction": direction}] if ids else [],
        }
        for name, ids in groups.items()
        for direction in (1, -1)
    ]
    if any(r.id == "barrier_toggle" for r in model.rules):
        for name, direction, conditions in [
            ("openings", 1, []),
            ("openings_ready", 1, predicates["ready"]),
            ("closings_exposed", -1, [cond("body.location", "eq", 0)]),
            (
                "closings_exposed_unfunded",
                -1,
                [
                    cond("body.location", "eq", 0),
                    cond("body.bank", "le", bank_ticks - 1),
                ],
            ),
        ]:
            p["event_readouts"].append(
                {
                    "id": name,
                    "selectors": [
                        {
                            "rules": ["barrier_toggle"],
                            "direction": direction,
                            "source": conditions,
                        }
                    ],
                }
            )
    return p


def main():
    cases = []
    # Largest opening/re-engagement model first, before the control cases.
    for policy in ("reengage", "always", "conserve", "stop"):
        m = readiness_world(policy)
        cases.append(
            {
                "id": "short_openings_" + policy,
                "law": {"id": policy, "model": m.record()},
                "protocol": protocol(m, policy=policy, quantum=".5", effort=".5"),
            }
        )
    m = readiness_world(
        "stop", opening_rate=None, bank_quantum=".25", effort_bill=".25"
    )
    cases.append(
        {
            "id": "quarter_bill_blocked",
            "law": {"id": "quarter_bill_blocked", "model": m.record()},
            "protocol": protocol(m, policy="stop", quantum=".25", effort=".25"),
        }
    )
    assert set(POLICIES) == {c["law"]["id"] for c in cases[:4]}
    plan = {
        "schema": "omega.coupled-engineering-plan/1",
        "date": "2026-10-26",
        "cases": cases,
        "spec": "research/platform/specs/STRUGGLE_READINESS_SPEC_r1.md",
        "snapshot_files": [
            "scripts/write_readiness_smoke.py",
            "tests/test_readiness.py",
        ],
        "caps": {
            "case_seconds": 300,
            "job_memory_bytes": 2 * 1024**3,
            "case_output_bytes": 16 * 1024**2,
            "batch_seconds": 1200,
            "batch_output_bytes": 64 * 1024**2,
        },
    }
    out = ROOT / "research/platform/models/struggle-readiness/ENGINEERING_PLAN.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "written", "cases": len(cases), "scope": "smoke only"}))


if __name__ == "__main__":
    main()
