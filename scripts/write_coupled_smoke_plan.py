"""Materialize the bounded coupled-autocatalysis engineering plan; no evaluation."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from omega_cosmology.testbed.physical_modules import (
    assistance_spec,
    autocatalytic_ecology,
    repaired_capacity_world,
)


def cond(k, op, v):
    return {"coordinate": k, "operator": op, "value": v}


def case(name, model, state, groups):
    organizations, ancestry, projections = [], [], []
    for group in groups:
        fields = group["members"]
        organizations.append(
            {
                "id": group["id"],
                "definition": "All declared component slots constructed",
                "coordinates": fields,
                "functional_any_of": [[cond(k, "eq", 1) for k in fields]],
            }
        )
        query = assistance_spec(model, fields)
        query["id"] = group["id"] + ".construction_depth"
        ancestry.append(query)
        for memory in (1, 2):
            projections.append(
                {
                    "id": group["id"] + f".m{memory}",
                    "coordinates": fields + [group["id"] + ".bank"],
                    "conditioning": "full_present",
                    "memory": memory,
                }
            )
    if not groups:
        organizations = [
            {
                "id": "bound",
                "definition": "Bound apparatus",
                "coordinates": ["bond"],
                "functional_any_of": [[cond("bond", "eq", 1)]],
            }
        ]
    return {
        "id": name,
        "law": {"id": name, "model": model.record()},
        "protocol": {
            "id": "coupled-engineering." + name,
            "preparations": [
                {
                    "id": "seed",
                    "roots": [[list(state), 1.0]],
                    "conditioning": "full_present",
                }
            ],
            "energy_per_root": str(model.energy(state)),
            "coordinate_order": [c.name for c in model.coordinates],
            "horizons": [4, 16],
            "cadences": [0.25],
            "primary_cadence": 0.25,
            "max_states": 1000,
            "reference_time": 1.0,
            "numerical": {
                "kernel_agreement_tolerance": 1e-12,
                "independent_history_tolerance": 1e-7,
            },
            "sufficiency": "All modeled slots, bank, shared carrier and native rate dependencies retained",
            "boundary_scope": {
                "bath_beta": 1.0,
                "source": "Explicit reversible carrier-work pair when present",
                "unresolved": "Bath/source histories; no cancellation asserted",
            },
            "conserved": [m["id"] for m in model.material],
            "observables": [
                {"id": "bank_" + g["id"], "terms": [[g["id"] + ".bank", 1]]}
                for g in groups
            ],
            "event_readouts": [],
            "monitors": [],
            "projected_histories": projections,
            "structural_analysis": {
                "organizations": organizations,
                "ancestry": ancestry,
                "max_ancestry_query_states": 20000,
            },
            "scope": "Engineering smoke only; fixed slots and contacts, no spatial ecology, optimizer or ethical comparison",
        },
    }


def main():
    pair = [
        {"id": g, "members": [g + ".x", g + ".y"], "access_member": g + ".x"}
        for g in ("A", "B")
    ]
    root = (1, 0, 1, 1, 0, 1, 1)
    shared = autocatalytic_ecology(pair)
    repaired, _ = repaired_capacity_world()
    single = [{"id": "A", "members": ["A.x", "A.y", "A.z"], "access_member": "A.x"}]
    triple = autocatalytic_ecology(single)
    help_model = autocatalytic_ecology(
        pair, extra_assistance=[("A.x", "B.y"), ("B.x", "A.y")]
    )
    off = autocatalytic_ecology(pair, driven=False)
    cases = [
        case("shared_pair", shared, root, pair),
        case("repaired_capacity", repaired, (1, 1, 1, 1, 2, 0), []),
        case("three_member_cycle", triple, (1, 0, 0, 1, 1), single),
        case("cross_assistance_pair", help_model, root, pair),
        case("source_off_pair", off, root, pair),
    ]
    plan = {
        "schema": "omega.coupled-engineering-plan/1",
        "date": "2026-10-25",
        "cases": cases,
        "spec": "research/platform/specs/COUPLED_AUTOCATALYTIC_SLICE_SPEC_r1.md",
        "caps": {
            "case_seconds": 150,
            "job_memory_bytes": 3 * 1024**3,
            "case_output_bytes": 32 * 1024**2,
            "batch_seconds": 600,
            "batch_output_bytes": 128 * 1024**2,
        },
    }
    for item in cases:
        model = item["law"]["model"]
        print(
            item["id"],
            len(model["coordinates"]),
            "coordinates, energy",
            item["protocol"]["energy_per_root"],
        )
    out = ROOT / "research/platform/models/coupled-autocatalysis/ENGINEERING_PLAN.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, indent=2, allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
