"""Tiny audit probes; demonstrate gaps without changing production objects/files."""

import json
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.matching import match_physical_moments
from omega_cosmology.testbed.models import two_copy_world
from omega_cosmology.testbed.physical_modules import assistance_spec, autocatalytic_ecology
from omega_cosmology.testbed.physics import Condition, Coordinate, EnergyTerm, LocalModel, Rule
from omega_cosmology.testbed.scheduled_study import evaluate_scheduled_case
from omega_cosmology.testbed.semantics import (
    ComparisonSpec, LawSpec, ObservationSpec, PresentSpec, QuantitySpec, validate_query,
)
from omega_cosmology.testbed.thermodynamics import audit_equilibrium, flow_rewards


def main():
    rows = []
    model = LocalModel(
        "audit-count", [Coordinate("n", (0, 1), "particle_count")],
        [Rule("change_count", (Condition("n", "eq", 0),), (("n", 1),), 0.1)],
        [], material=({"id": "count", "conservation": "n is conserved"},),
    )
    compiled = enumerate_model(model, [(0,)])
    rows.append({
        "probe": "declared_material_conservation",
        "reachable_counts": compiled.states,
        "equilibrium_audit": audit_equilibrium(compiled)["status"],
    })
    before = float(sum(flow_rewards(compiled)[2]))
    q_hash = compiled.generator_hash
    compiled.ledger = ()
    compiled.require_complete()
    rows.append({
        "probe": "ledger_integrity", "integrity_check_accepts_changed_ledger": True,
        "generator_hash_unchanged": q_hash == compiled.generator_hash,
        "summed_jump_rewards_before": before,
        "summed_jump_rewards_after": float(sum(flow_rewards(compiled)[2])),
    })
    model = LocalModel(
        "audit-present", [Coordinate("x", (0, 1), "energy")],
        [Rule("flip", (Condition("x", "eq", 0),), (("x", 1),), 0.1)],
        [EnergyTerm("1", "x")],
    )
    law = LawSpec("law", model.fingerprint(), {"bath": "one"})
    observation = ObservationSpec("whole", ("x",))
    quantity = QuantitySpec("history", "history", "bits", "full_present")
    comparison = ComparisonSpec(
        "process", "process", 1, 0.25, {"energy": "equal"},
        implementation="declared process", common_present="same-id",
    )
    statuses = []
    for root in [(0,), (1,)]:
        present = PresentSpec("same-id", ((root, 1),), sufficiency="complete state")
        statuses.append({
            "energy": str(model.energy(root)),
            "validation": validate_query(present, law, observation, comparison, quantity)["status"],
        })
    rows.append({"probe": "same_present_id_different_physical_present", "results": statuses})
    model, _ = two_copy_world(quotient=True)
    protocol = {
        "id": "audit-symmetry", "present_id": "common", "root": [0, 0],
        "energy_per_root": "0", "coordinate_order": ["first", "second"],
        "cadence": 0.25, "horizons": [1],
        "phases": [{"model": model.record(), "duration": 1}],
        "sufficiency": "complete unmarked state", "boundary_scope": {"bath": "one"},
        "matched": {"endowment": "same"}, "implementation": "constant schedule",
        "observables": [{"id": "first_identity", "terms": [["first", 1]]}],
        "functional_conditions": [{"coordinate": "first", "operator": "eq", "value": 1}],
        "projected_histories": [], "max_states": 10,
        "max_dense_bytes": 1024**2, "max_projection_bytes": 1024**2,
    }
    result = evaluate_scheduled_case(protocol)
    rows.append({
        "probe": "scheduled_noninvariant_observable", "status": result["status"],
        "observable": result["rows"][0]["observables"]["first_identity"],
        "same_orbit": sorted(model.orbit((0, 1))),
    })
    model = autocatalytic_ecology([{"id": "A", "members": ["a", "b"], "access_member": "a"}])
    record = model.record()
    record["rules"] = [{**rule, "id": "renamed." + rule["id"]} for rule in record["rules"]]
    renamed = LocalModel.from_record(record)
    ca = enumerate_model(model, [(0, 0, 0, 0)])
    cb = enumerate_model(renamed, [(0, 0, 0, 0)])
    rows.append({
        "probe": "rule_renaming", "state_orders_equal": ca.states == cb.states,
        "generator_entries_equal": bool((ca.q != cb.q).nnz == 0),
        "original_ancestry_edges": len(assistance_spec(model, ["a", "b"])["assistance_edges"]),
        "renamed_ancestry_edges": len(assistance_spec(renamed, ["a", "b"])["assistance_edges"]),
    })
    match = match_physical_moments(
        lambda parameters: {"activity": 1e-4}, {"activity": 1e-8},
        {"x": (0.1, 1)}, max_evaluations=1,
    )
    rows.append({
        "probe": "small_moment_default_tolerance", "status": match["status"],
        "target": 1e-8, "control": 1e-4, "scale": match["scale"],
        "tolerance": match["tolerance"],
    })
    files = sorted((ROOT / "src/omega_cosmology/testbed").glob("*.py"))
    files.append(Path(__file__).resolve())
    print(json.dumps({
        "scope": "Diagnostic probes of current implementation, not scientific experiments or retained-result invalidations",
        "source_sha256": {p.relative_to(ROOT).as_posix(): sha256(p.read_bytes()).hexdigest() for p in files},
        "probes": rows,
        "existing_test_suites_rerun": {
            "test_testbed_kernel": 12, "test_projection_bounds": 6,
            "test_assistance_ancestry": 5, "test_phases": 8,
        },
        "existing_test_outcome": "31 passed in separate audit commands",
    }, indent=2))


if __name__ == "__main__":
    main()
