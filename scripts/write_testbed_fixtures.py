"""Rebuild the reviewed engineering configurations from data-level model builders."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main():
    from omega_cosmology.testbed.models import calibration_world, enabling_world
    from omega_cosmology.testbed.semantics import (
        ComparisonSpec,
        EvidenceSpec,
        LawSpec,
        ObservationSpec,
        PresentSpec,
        QuantitySpec,
    )

    out = ROOT / "research/platform/models"
    out.mkdir(parents=True, exist_ok=True)
    for name, builder in [
        ("R0", calibration_world),
        ("R1", enabling_world),
        ("R2", lambda: enabling_world(expansion=True)),
    ]:
        model, root = builder()
        present = PresentSpec(
            name + ".present",
            ((root, 1.0),),
            sufficiency="All local domains, energy, guards, constraints and Markov boundary variables retained; no delayed callback",
        )
        law = LawSpec(
            name + ".law",
            model.fingerprint(),
            {
                "bath": {"beta": 1.0, "heat_sign": "positive out"},
                "source": {
                    "pair": "spent-to-locked",
                    "forward_work": "3",
                    "reverse_work": "-3",
                },
                "unresolved": "Bath/source histories; no exterior cancellation asserted",
            },
            conserved=("fixed constituent slots", "one carrier")
            + (("bank tick parity",) if name == "R0" else ()),
        )
        observation = ObservationSpec(
            name + ".whole", tuple(c.name for c in model.coordinates)
        )
        comparison = ComparisonSpec(
            name + ".engineering",
            "single_query",
            16,
            0.25,
            {
                "kind": "one law and one exact root; no comparative scientific conclusion"
            },
        )
        quantity = QuantitySpec(
            "history.full_given_present",
            "H(X_1,...,X_n | X_0=x)",
            "bits",
            "full_present",
        )
        evidence = EvidenceSpec(
            name + ".numerical",
            "Complete reachable enumeration, matrix exponentials, direct short-word cross-check",
            "numerical_full_model",
            ("Appendix A r19 targeted definitions", "foundations r4"),
            {
                "arithmetic": "float64",
                "identity_tolerance": 1e-10,
                "faithfulness": "open",
            },
            "Finite modeled field; thermodynamic bath/source histories unresolved",
        )
        data = {
            "schema": "omega.engineering-fixture/1",
            "id": name,
            "model": model.record(),
            "present": present.record(),
            "law": law.record(),
            "observation": observation.record(),
            "comparison": comparison.record(),
            "quantity": quantity.record(),
            "evidence": evidence.record(),
        }
        (out / (name + ".json")).write_text(
            json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8"
        )
    # These declare semantics and round-trip behavior, not executed comparative studies.
    examples = {
        "scope": "Serializable contract examples only; no rankings or executed option comparison",
        "full_present": PresentSpec(
            "one", (((0, 0), 1.0),), sufficiency="Both physical coordinates retained"
        ).record(),
        "own_present": PresentSpec(
            "part",
            (((0, 0), 0.5), ((0, 1), 0.5)),
            conditioning="own_present",
            sufficiency="Full two-coordinate hidden state retained in dynamics",
            hidden_root_provenance="Explicit fair conditional law over coordinate 2 given observed coordinate 1=0",
        ).record(),
        "own_observation": ObservationSpec(
            "part.own",
            ("observed",),
            scope="projected_history",
            conditioning="own_present",
        ).record(),
        "mechanism_comparison": ComparisonSpec(
            "mechanism",
            "mechanism",
            16,
            0.25,
            {
                "endowment": "Must be matched explicitly",
                "boundary": "Same prescribed source, accepted work reported",
            },
            implementation="Enabling pair present versus ablated; this is a between-law contrast",
        ).record(),
        "preparation_comparison": ComparisonSpec(
            "preparations",
            "preparation",
            16,
            0.25,
            {
                "law": "Identical",
                "endowment": "Material, energy and boundary matched; correlations stated",
            },
        ).record(),
        "process_comparison": ComparisonSpec(
            "process",
            "process",
            16,
            0.25,
            {
                "law": "Common encompassing controlled law",
                "endowment": "One common present",
            },
            common_present="one",
            implementation="Requires an explicitly represented paid actuator and its command paths; not yet a scientific fixture",
        ).record(),
        "process_status": "Metadata validation example only. R0–R2 have no optimized controller; no process contrast is evaluated.",
    }
    (out / "SEMANTIC_EXAMPLES.json").write_text(
        json.dumps(examples, indent=2) + "\n", encoding="utf-8"
    )
    print("Wrote R0, R1, R2 and semantic examples")


if __name__ == "__main__":
    main()
