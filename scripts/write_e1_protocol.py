"""Define a small coupled-autocatalysis map; no ranking or kinetic fitting."""

import copy
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from omega_cosmology.testbed.physical_modules import (
    assistance_spec,
    autocatalytic_ecology,
)


def condition(name, op, value):
    return {"coordinate": name, "operator": op, "value": value}


def build_protocol():
    groups = [
        {"id": g, "members": [g + ".x", g + ".y"], "access_member": g + ".x"}
        for g in ("A", "B")
    ]
    mechanisms = {
        "ablation": [],
        "local": [],
        "AtoB": [("A.x", "B.y")],
        "BtoA": [("B.x", "A.y")],
        "reciprocal": [("A.x", "B.y"), ("B.x", "A.y")],
    }
    regimes = []
    for supply, bill, turnover in itertools.product(
        [0.02, 0.12], [1, 2], [0.001, 0.012]
    ):
        ident = (
            "S"
            + str(supply).replace(".", "p")
            + "_C"
            + str(bill)
            + "_D"
            + str(turnover).replace(".", "p")
        )
        regimes.append(
            {"id": ident, "source": supply, "bill_ticks": bill, "turnover": turnover}
        )
    regimes.append(
        {"id": "source_off_anchor", "source": 0, "bill_ticks": 1, "turnover": 0.001}
    )
    laws = []
    for regime in regimes:
        for mechanism, extra in mechanisms.items():
            model = autocatalytic_ecology(
                groups,
                extra_assistance=extra,
                bank_quantum=".5",
                formation_energy=".5",
                construction_bill_ticks=regime["bill_ticks"],
                basal_conductance=regime["turnover"],
                source_conductance=regime["source"] or 0.02,
                driven=bool(regime["source"]),
            )
            record = model.record()
            name = regime["id"] + "__" + mechanism
            record["id"] = "E1." + name
            if mechanism == "ablation":
                record["rules"] = [
                    r for r in record["rules"] if not r["id"].startswith("assisted_")
                ]
            structural = {
                "organizations": [],
                "ancestry": [],
                "max_ancestry_query_states": 20000,
            }
            for g in groups:
                structural["organizations"].append(
                    {
                        "id": g["id"],
                        "definition": "Both local members constructed",
                        "coordinates": g["members"],
                        "functional_any_of": [
                            [condition(k, "eq", 1) for k in g["members"]]
                        ],
                    }
                )
                if mechanism != "ablation":
                    spec = assistance_spec(model, g["members"])
                    spec["id"] = g["id"] + ".depth"
                    structural["ancestry"].append(spec)
            # Specific queries can depend on which marked channels exist, but do
            # not change the model or score. The common predicates remain identical.
            laws.append(
                {
                    "id": name,
                    "regime": copy.deepcopy(regime),
                    "mechanism": mechanism,
                    "model": record,
                    "structural_analysis": structural,
                }
            )
    corners = [regimes[0]["id"], regimes[-2]["id"]]
    grid = [(law["id"], 0.25) for law in laws]
    grid += [
        (law["id"], dt)
        for law in laws
        if law["regime"]["id"] in corners
        for dt in (0.125, 0.5)
    ]
    gate = (regimes[-2]["id"] + "__reciprocal", 0.125)
    grid.remove(gate)
    grid.insert(0, gate)
    projections = [
        {
            "id": g["id"],
            "coordinates": g["members"] + [g["id"] + ".bank"],
            "conditioning": "full_present",
            "memory": 1,
        }
        for g in groups
    ]
    obs = []
    for g in groups:
        obs += [
            {"id": g["id"] + ".active", "terms": [[k, 1] for k in g["members"]]},
            {"id": g["id"] + ".bank_energy", "terms": [[g["id"] + ".bank", 0.5]]},
        ]
    protocol = {
        "schema": "omega.finite-study-protocol/1",
        "id": "E1-coupled-autocatalysis-r1",
        "question": "How do costed catalytic relations change local and whole continuations under supply, cost and native turnover?",
        "laws": laws,
        "regimes": regimes,
        "mechanisms": list(mechanisms),
        "case_grid": grid,
        "preparations": [
            {
                "id": "assembled",
                "roots": [[[1, 1, 0, 1, 1, 0, 0], 1.0]],
                "conditioning": "full_present",
            },
            {
                "id": "unassembled",
                "roots": [[[0, 0, 2, 0, 0, 2, 0], 1.0]],
                "conditioning": "full_present",
            },
        ],
        "energy_per_root": "2",
        "coordinate_order": ["A.x", "A.y", "A.bank", "B.x", "B.y", "B.bank", "carrier"],
        "cadences": [0.125, 0.25, 0.5],
        "primary_cadence": 0.25,
        "horizons": [16, 64, 256, 1024, 4096],
        "projected_histories": projections,
        "observables": obs,
        "event_readouts": [],
        "monitors": [],
        "sufficiency": "All constructed slots, banks, finite shared carrier and rate dependencies explicit",
        "conserved": ["four distinct component slots", "one shared carrier"],
        "boundary_scope": {
            "bath_beta": 1,
            "source": "Matched reversible offered drive within each mechanism/preparation comparison",
            "unresolved": "External bath/source histories; no cancellation asserted",
        },
        "max_states": 1000,
        "reference_time": 1.0,
        "numerical": {
            "sign_deadband_bits": 1e-6,
            "independent_history_tolerance": 1e-6,
            "kernel_agreement_tolerance": 1e-12,
        },
        "caps": {
            "case_wall_seconds": 240,
            "job_memory_bytes": 2 * 1024**3,
            "case_output_bytes": 16 * 1024**2,
            "batch_wall_seconds": 1800,
            "batch_output_bytes": 128 * 1024**2,
        },
        "execution": {"max_workers": 3},
        "source_inputs": [
            "scripts/write_e1_protocol.py",
            "tests/test_e1_protocol.py",
            "research/studies/E1-coupled-autocatalysis/SPECIFICATION_r1.md",
        ],
        "scope": "Exploratory finite chemical map; no optimizer, spatial gas, full community pedigree, irreversible closure or ethical verdict.",
    }
    return protocol


def main():
    p = build_protocol()
    out = ROOT / "research/studies/E1-coupled-autocatalysis/PROTOCOL.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(p, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "laws": len(p["laws"]),
                "cases": len(p["case_grid"]),
                "profiles": len(p["case_grid"])
                * len(p["preparations"])
                * len(p["horizons"]),
            }
        )
    )


if __name__ == "__main__":
    main()
