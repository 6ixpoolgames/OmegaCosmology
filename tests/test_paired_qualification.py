"""Counterexamples against inventory laundering and permissive state mappings."""

import sys
import unittest
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.history import (
    entropy,
    observed_history_law,
    sampled_kernel,
)
from omega_cosmology.testbed.inventory_witness import (
    InventoryWitness,
    RetainedSlot,
    interpret_retained_slots,
)
from omega_cosmology.testbed.physics import Condition as C
from omega_cosmology.testbed.physics import Coordinate, EnergyTerm, LocalModel, Rule
from omega_cosmology.testbed.semantics import (
    ComparisonSpec,
    LawSpec,
    ObservationSpec,
    PresentSpec,
    QuantitySpec,
    validate_comparison,
)
from omega_cosmology.testbed.state_mapping import (
    ConstraintStateMapping,
    constraint_identity,
)


def model(sham=False):
    record = LocalModel(
        "test_capacity",
        [
            Coordinate("component", (0, 1), "material_state"),
            Coordinate("bank", (0, 1, 2), "energy"),
        ],
        [
            Rule("activate", (C("component", "eq", 0),), (("component", 1),), 0.1),
            Rule("charge", (C("bank", "le", 1),), (("bank", 1),), 0.1, "1", "source"),
        ],
        [EnergyTerm(".5", "component"), EnergyTerm(".5", "bank")],
        forbidden=[(C("component", "eq", 0), C("bank", "eq", 2))]
        + ([(C("bank", "eq", 2),)] if sham else []),
    ).record()
    record["material"] = [
        {
            "id": "slot",
            "quantity": 1,
            "conservation": "same retained unit, precursor or working",
        }
    ]
    return LocalModel.from_record(record)


def witness():
    return InventoryWitness(
        "slot",
        (RetainedSlot("component", ((0, "precursor"), (1, "working"))),),
        "A declared physical unit persists through activation and deactivation",
    )


def mapping(a, b):
    left = {constraint_identity(v) for v in a.model.record()["forbidden"]}
    right = {constraint_identity(v) for v in b.model.record()["forbidden"]}
    return ConstraintStateMapping(
        a.model_hash,
        b.model_hash,
        a.state_order_hash,
        b.state_order_hash,
        tuple(sorted(left - right)),
        tuple(sorted(right - left)),
    )


def arms(a, b, kind="mechanism"):
    root = PresentSpec(
        "p",
        ((((0, 0)), 1),),
        sufficiency="All fixed-slot and energy dependencies included",
    )
    comparison = ComparisonSpec(
        "c",
        kind,
        1,
        0.25,
        {"retained_slots": "same declared units"},
        common_present=root.id,
        implementation="test physical coupling" if kind == "process" else "",
        common_present_hash=root.content_fingerprint(),
    )

    def one(c):
        return {
            "compiled": c,
            "present": root,
            "comparison": comparison,
            "law": LawSpec("law", c.model_hash, {"source": "same"}),
            "observation": ObservationSpec("whole", ("component", "bank")),
            "quantity": QuantitySpec(
                "h", "conditional sampled history", "bits", "full_present"
            ),
        }

    return comparison, one(a), one(b)


class QualificationTests(unittest.TestCase):
    def compiled(self, sham=False):
        m, _ = interpret_retained_slots(model(sham), [witness()])
        return enumerate_model(m, [(0, 0)])

    def test_inventory_interpretation_preserves_native_law(self):
        original = model()
        before = original.record()
        changed, receipt = interpret_retained_slots(original, [witness()])
        a, b = enumerate_model(original, [(0, 0)]), enumerate_model(changed, [(0, 0)])
        self.assertEqual(original.record(), before)
        self.assertEqual(a.states, b.states)
        np.testing.assert_array_equal(a.q.toarray(), b.q.toarray())
        self.assertEqual(a.ledger, b.ledger)
        self.assertEqual(changed.material_status, "executable")
        self.assertNotEqual(original.fingerprint(), changed.fingerprint())
        self.assertIn("not_chemical_closure", changed.material[0]["inventory_scope"])
        self.assertEqual(receipt["changed_fields"], ["id", "material"])
        for state in b.states:
            self.assertEqual(changed.inventory(state), {"slot": "1"})

    def test_witness_cannot_drop_declarations_or_use_partial_partitions(self):
        with self.assertRaises(ValueError):
            interpret_retained_slots(model(), [])
        with self.assertRaises(ValueError):
            interpret_retained_slots(
                model(),
                [
                    replace(
                        witness(), slots=(RetainedSlot("component", ((1, "working"),)),)
                    )
                ],
            )
        with self.assertRaises(ValueError):
            RetainedSlot("component", ((0, "precursor"), (0, "duplicate")))

    def test_energy_cannot_be_relabelled_as_retained_material(self):
        bad = replace(
            witness(),
            slots=(RetainedSlot("bank", ((0, "empty"), (1, "one"), (2, "two"))),),
        )
        with self.assertRaisesRegex(ValueError, "Energy"):
            interpret_retained_slots(model(), [bad])

    def test_duplicate_slots_and_wrong_quantity_rejected(self):
        w = witness()
        with self.assertRaises(ValueError):
            interpret_retained_slots(model(), [replace(w, slots=w.slots * 2)])
        record = model().record()
        record["material"][0]["quantity"] = 2
        with self.assertRaises(ValueError):
            interpret_retained_slots(LocalModel.from_record(record), [w])

    def test_existing_material_constraint_cannot_be_weakened(self):
        record = model().record()
        record["material"][0]["inventory"] = [
            {"coefficient": "1", "coordinate": "component"}
        ]
        with self.assertRaisesRegex(ValueError, "existing executable"):
            interpret_retained_slots(LocalModel.from_record(record), [witness()])

    def test_mapping_required_and_missing_symbols_add_no_entropy(self):
        a, b = self.compiled(), self.compiled(True)
        args = arms(a, b)
        with self.assertRaisesRegex(ValueError, "explicit mapping"):
            validate_comparison(*args, require_material=True)
        state_map = mapping(a, b)
        result = validate_comparison(
            *args, state_mapping=state_map, require_material=True
        )
        self.assertEqual(result["status"], "validated_paired_comparison")
        self.assertEqual(result["state_mapping"]["left_only_states"], 1)
        for side, compiled in (("left", a), ("right", b)):
            p = sampled_kernel(compiled, 0.25)
            mu = np.eye(len(p))[compiled.index[(0, 0)]]
            endpoint = mu @ p
            embedded = state_map.embed_distribution(a, b, side, endpoint)
            self.assertAlmostEqual(entropy(endpoint), entropy(embedded))
            native = observed_history_law(p, mu, list(compiled.states), 3)
            alphabet = {
                s: i for i, s in enumerate(sorted(set(a.states) | set(b.states)))
            }
            relabelled = observed_history_law(
                p, mu, [alphabet[s] for s in compiled.states], 3
            )
            self.assertEqual(sorted(native.values()), sorted(relabelled.values()))

    def test_mapping_rejects_wrong_law_and_unlisted_constraints(self):
        a, b = self.compiled(), self.compiled(True)
        m = mapping(a, b)
        for bad in (
            replace(m, left_model_hash="wrong"),
            replace(m, added_constraints=()),
        ):
            with self.assertRaises(ValueError):
                validate_comparison(
                    *arms(a, b), state_mapping=bad, require_material=True
                )

    def test_mapping_cannot_change_hamiltonian_or_inventory(self):
        a, b = self.compiled(), self.compiled(True)
        for field in ("energy_terms", "material"):
            record = deepcopy(b.model.record())
            if field == "energy_terms":
                record[field][0]["coefficient"] = "1"
            else:
                record[field][0]["inventory_scope"] = "other"
            changed = enumerate_model(LocalModel.from_record(record), [(0, 0)])
            with self.assertRaisesRegex(ValueError, "grammar"):
                validate_comparison(
                    *arms(a, changed),
                    state_mapping=mapping(a, changed),
                    require_material=True,
                )

    def test_mapping_does_not_bypass_boundary_or_present_checks(self):
        a, b = self.compiled(), self.compiled(True)
        c, left, right = arms(a, b)
        bad = dict(right, law=replace(right["law"], boundary={"source": "different"}))
        with self.assertRaisesRegex(ValueError, "Boundary"):
            validate_comparison(
                c, left, bad, state_mapping=mapping(a, b), require_material=True
            )
        bad = dict(right, present=replace(right["present"], roots=(((1, 0), 1),)))
        with self.assertRaisesRegex(ValueError, "same physical present"):
            validate_comparison(
                c, left, bad, state_mapping=mapping(a, b), require_material=True
            )
        with self.assertRaisesRegex(ValueError, "full-state mechanism"):
            validate_comparison(*arms(a, b, "process"), state_mapping=mapping(a, b))

    def test_empty_material_is_not_a_material_certificate(self):
        record = self.compiled().model.record()
        record["material"] = []
        c = enumerate_model(LocalModel.from_record(record), [(0, 0)])
        args = arms(c, c)
        with self.assertRaisesRegex(ValueError, "nonempty executable"):
            validate_comparison(*args, require_material=True)
        result = validate_comparison(*args)
        self.assertEqual(result["material_endowment"], "not_declared_not_certified")

    def test_mapping_cannot_bypass_resolution_matching(self):
        a, b = self.compiled(), self.compiled(True)
        c, left, right = arms(a, b)
        obs = replace(right["observation"], resolution={"faithfulness": "established"})
        with self.assertRaisesRegex(ValueError, "observations/quantities differ"):
            validate_comparison(
                c,
                left,
                dict(right, observation=obs),
                state_mapping=mapping(a, b),
                require_material=True,
            )

    def test_empty_term_sets_and_aliasing_native_states_rejected(self):
        record = self.compiled().model.record()
        record["material"][0]["inventory"] = []
        c = enumerate_model(LocalModel.from_record(record), [(0, 0)])
        with self.assertRaisesRegex(ValueError, "nonempty executable"):
            validate_comparison(*arms(c, c), require_material=True)
        a, b = self.compiled(), self.compiled(True)
        # Test the mapping's alphabet invariant independently of compiler
        # enumeration: two native symbols cannot silently merge into one.
        proxy = SimpleNamespace(
            require_complete=lambda: None,
            model=a.model,
            model_hash=a.model_hash,
            state_order_hash=a.state_order_hash,
            states=(*a.states, a.states[0]),
        )
        with self.assertRaisesRegex(ValueError, "Noninjective"):
            mapping(a, b).verify(proxy, b)


if __name__ == "__main__":
    unittest.main()
