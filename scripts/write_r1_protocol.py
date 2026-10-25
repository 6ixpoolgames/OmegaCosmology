"""Materialize the R1 batch inputs without evaluating a lushness ranking."""

import copy
import itertools
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main():
    from omega_cosmology.testbed.physics import LocalModel

    fixture = json.loads(
        (ROOT / "research/platform/models/R1.json").read_text(encoding="utf-8")
    )
    model = LocalModel.from_record(fixture["model"])
    seed, unassembled = (1, 1, 1, 1, 2), (0, 0, 0, 1, 3)
    energy = model.energy(seed)
    assert model.energy(unassembled) == energy
    shell = [
        s
        for s in itertools.product(*(c.domain for c in model.coordinates))
        if model.valid(s) and model.energy(s) == energy
    ]
    weights = [math.exp(model.log_degeneracy(s)) for s in shell]
    total = sum(weights)
    preparations = [
        {"id": "built", "roots": [[seed, 1.0]], "conditioning": "full_present"},
        {
            "id": "unassembled",
            "roots": [[unassembled, 1.0]],
            "conditioning": "full_present",
        },
        {
            "id": "equal_energy_reference",
            "roots": [[s, w / total] for s, w in zip(shell, weights)],
            "conditioning": "root_conditioned_average",
            "interpretation": "Degeneracy-weighted same-energy coarse reference; drawing the root adds no entropy; not microscopic gas",
        },
    ]
    laws = []
    for driven, assisted in [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ]:
        name = ("driven" if driven else "source_off") + (
            "__intact" if assisted else "__ablated"
        )
        record = copy.deepcopy(fixture["model"])
        record["id"] = "R1." + name
        record["rules"] = [
            r
            for r in record["rules"]
            if (assisted or r["id"] != "unlock_motif")
            and (driven or r["boundary"] == "native")
        ]
        laws.append(
            {"id": name, "driven": driven, "assisted": assisted, "model": record}
        )
    protocol = {
        "schema": "omega.r1-protocol/1",
        "id": "R1-constructed-access-r1",
        "question": "How does costed constructed access affect the full continuation, resource use and reconstruction?",
        "status": "Execution inputs, not a prediction or favorable-outcome gate",
        "energy_per_root": str(energy),
        "preparations": preparations,
        "laws": laws,
        "horizons": [16, 64, 256, 1024],
        "cadences": [0.125, 0.25, 0.5],
        "primary_cadence": 0.25,
        "coordinate_order": [c.name for c in model.coordinates],
        "reference_time": 1.0,
        "numerical": {
            "sign_deadband_bits": 1e-7,
            "independent_history_tolerance": 1e-7,
            "kernel_agreement_tolerance": 1e-12,
            "basis": "Conservative float64 validation allowance for up to 8192 accumulated steps; not a rigorous interval certificate",
        },
        "caps": {
            "case_wall_seconds": 120,
            "job_memory_bytes": 2 * 1024**3,
            "case_output_bytes": 32 * 1024**2,
            "batch_wall_seconds": 300,
            "batch_output_bytes": 128 * 1024**2,
        },
        "monitor": {
            "first": ["binding", -1],
            "second": ["binding", 1],
            "meaning": "At least one dissolution followed by re-binding, unconditionally over paths; no lineage/generation claim",
        },
        "bank_bills": {
            "paid_activate_a.active": 1.0,
            "paid_activate_b.active": 1.0,
            "upkeep": 0.5,
        },
        "comparisons": {
            "preparation": "Built minus unassembled/reference under the identical law",
            "mechanism": "Intact minus paired assisted-path ablation at the identical preparation",
            "boundary": "Driven minus source off; a different physical boundary law, not equal absorbed work",
        },
        "scope": "Whole modeled field. Bath/source histories unresolved, temporal faithfulness open, no controller or policy search. No predictions scored as theory failures.",
    }
    out = ROOT / "research/studies/R1-constructed-access"
    out.mkdir(parents=True, exist_ok=True)
    (out / "PROTOCOL.json").write_text(
        json.dumps(protocol, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "laws": len(laws),
                "preparations": len(preparations),
                "energy_shell_roots": len(shell),
                "law_cadence_cases": len(laws) * 3,
                "profile_rows": len(laws) * 3 * len(preparations) * 4,
            }
        )
    )


if __name__ == "__main__":
    main()
