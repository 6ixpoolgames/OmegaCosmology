"""Adversarial regressions for the October27 machinery audit."""

import copy
import sys
import unittest
from dataclasses import replace
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.backends import enumerate_model, trajectory
from omega_cosmology.testbed.finite_study import evaluate_case
from omega_cosmology.testbed.history import (
    EvaluationContext,
    history_profile,
    irreducible_asymptotics,
)
from omega_cosmology.testbed.matching import MomentSpec, match_physical_moments
from omega_cosmology.testbed.models import two_copy_world
from omega_cosmology.testbed.phases import compile_phases
from omega_cosmology.testbed.physical_modules import (
    assistance_spec,
    autocatalytic_ecology,
)
from omega_cosmology.testbed.physics import Condition as C
from omega_cosmology.testbed.physics import Coordinate, EnergyTerm, LocalModel, Rule
from omega_cosmology.testbed.scheduled_study import evaluate_scheduled_case
from omega_cosmology.testbed.semantics import (
    ComparisonSpec,
    LawSpec,
    ObservationSpec,
    PresentSpec,
    QuantitySpec,
    validate_comparison,
    validate_query,
)
from omega_cosmology.testbed.thermodynamics import flow_rewards


def switch(material=(), energy=False):
    return LocalModel(
        "switch",
        [Coordinate("x", (0, 1), "state")],
        [Rule("flip", (C("x", "eq", 0),), (("x", 1),), 0.2)],
        [EnergyTerm("1", "x")] if energy else [],
        material=material,
    )


class ContractHardeningTests(unittest.TestCase):
    def test_executable_material_rejects_creation_in_both_backends(self):
        with self.assertRaisesRegex(ValueError, "executable inventory"):
            switch(({"id": "matter", "conserved": "yes"},))
        m = switch(
            ({"id": "matter", "inventory": [{"coefficient": "1", "coordinate": "x"}]},)
        )
        with self.assertRaisesRegex(ValueError, "violates material"):
            enumerate_model(m, [(0,)])
        with self.assertRaisesRegex(ValueError, "violates material"):
            trajectory(m, (0,), 1, np.random.default_rng(1))

    def test_declared_boundary_exchange_is_reversible(self):
        m = switch()
        r = m.record()
        r["rules"][0]["boundary"] = "feed"
        r["material"] = [
            {
                "id": "matter",
                "inventory": [{"coefficient": "1", "coordinate": "x"}],
                "exchange_by_rule": {"flip": "1"},
            }
        ]
        c = enumerate_model(LocalModel.from_record(r), [(0,)])
        self.assertEqual(len(c.ledger), 2)
        self.assertEqual({e.direction for _, _, e in c.ledger}, {-1, 1})
        phases = compile_phases(
            [LocalModel.from_record(r), LocalModel.from_record(r)], [(0,)]
        )
        self.assertEqual(phases[0].ledger, phases[1].ledger)
        r["rules"][0]["boundary"] = "native"
        with self.assertRaisesRegex(ValueError, "boundary rule"):
            LocalModel.from_record(r)

    def test_legacy_material_is_readable_but_not_certified(self):
        r = switch().record()
        r["material"] = ({"id": "old", "conservation": "prose"},)
        m = LocalModel.from_record(r)
        self.assertEqual(m.record(), r)
        self.assertEqual(m.material_status, "legacy_unverified")
        self.assertEqual(
            LocalModel.from_record(m.record()).fingerprint(), m.fingerprint()
        )

    def test_ledger_and_energy_marks_are_integrity_checked(self):
        c = enumerate_model(switch(), [(0,)])
        c.ledger = ()
        with self.assertRaises(ValueError):
            flow_rewards(c)
        c = enumerate_model(switch(), [(0,)])
        i, j, e = c.ledger[0]
        with self.assertRaisesRegex(ValueError, "energy ledger"):
            replace(c, ledger=((i, j, replace(e, work=1)), *c.ledger[1:]))
        with self.assertRaisesRegex(ValueError, "aggregate"):
            replace(c, ledger=())

    def test_present_identity_is_content_not_name(self):
        m = switch(energy=True)
        p = PresentSpec("same", (((0,), 1),), sufficiency="complete")
        comparison = ComparisonSpec(
            "choice",
            "process",
            1,
            0.25,
            {"energy": "same"},
            implementation="physical",
            common_present=p.id,
            common_present_hash=p.content_fingerprint(),
        )
        args = (
            LawSpec("law", m.fingerprint(), {"bath": 1}),
            ObservationSpec("whole", ("x",)),
            comparison,
            QuantitySpec("H", "history", "bits", "full_present"),
        )
        validate_query(p, *args)
        with self.assertRaisesRegex(ValueError, "content hash"):
            validate_query(replace(p, roots=(((1,), 1),)), *args)

    def test_paired_validation_checks_executed_endowment_and_window(self):
        m = switch(energy=True)
        c = enumerate_model(m, [(0,)])
        p = PresentSpec("root", (((0,), 1),), sufficiency="complete")
        cmp = ComparisonSpec("pair", "preparation", 1, 0.25, {"energy": "same"})
        arm = {
            "compiled": c,
            "present": p,
            "law": LawSpec("law", m.fingerprint(), {"bath": 1}),
            "observation": ObservationSpec("all", ("x",)),
            "comparison": cmp,
            "quantity": QuantitySpec("H", "history", "bits", "full_present"),
        }
        self.assertEqual(
            validate_comparison(cmp, arm, arm)["status"], "validated_paired_comparison"
        )
        for bad in (
            dict(arm, present=replace(p, roots=(((1,), 1),))),
            dict(arm, comparison=replace(cmp, horizon=2)),
            dict(arm, law=replace(arm["law"], boundary={"bath": 2})),
            dict(arm, law=replace(arm["law"], physical_model_hash="false")),
        ):
            with self.assertRaises(ValueError):
                validate_comparison(cmp, arm, bad)

    def test_scheduled_symmetry_queries_match_static_contract(self):
        model, _ = two_copy_world(quotient=True)
        protocol = {
            "id": "symmetry",
            "present_id": "common",
            "root": [0, 0],
            "energy_per_root": "0",
            "coordinate_order": ["first", "second"],
            "cadence": 0.25,
            "horizons": [1],
            "phases": [{"model": model.record(), "duration": 1}],
            "sufficiency": "complete unmarked state",
            "boundary_scope": {"bath": "one"},
            "matched": {"endowment": "same"},
            "implementation": "constant schedule",
            "observables": [{"id": "sum", "terms": [["first", 1], ["second", 1]]}],
            "functional_conditions": [],
            "projected_histories": [],
            "max_states": 10,
            "max_dense_bytes": 1024**2,
            "max_projection_bytes": 1024**2,
        }
        self.assertEqual(evaluate_scheduled_case(protocol)["status"], "passed")
        for key, value in (
            ("observables", [{"id": "identity", "terms": [["first", 1]]}]),
            (
                "functional_conditions",
                [{"coordinate": "first", "operator": "eq", "value": 1}],
            ),
        ):
            with self.assertRaises(ValueError):
                evaluate_scheduled_case({**protocol, key: value})

    def test_assistance_survives_rule_renaming_and_guard_reordering(self):
        m = autocatalytic_ecology(
            [{"id": "A", "members": ["a", "b"], "access_member": "a"}]
        )
        r = m.record()
        for rule in r["rules"]:
            rule["id"] = "new." + rule["id"]
            rule["guards"] = tuple(reversed(rule["guards"]))
        renamed = LocalModel.from_record(r)
        a, b = (
            enumerate_model(m, [(0, 0, 0, 0)]),
            enumerate_model(renamed, [(0, 0, 0, 0)]),
        )
        self.assertEqual(a.states, b.states)
        self.assertEqual((a.q != b.q).nnz, 0)
        old, new = assistance_spec(m, ["a", "b"]), assistance_spec(renamed, ["a", "b"])
        self.assertEqual(len(old["assistance_edges"]), 2)
        self.assertEqual(len(new["assistance_edges"]), 2)
        bad = copy.deepcopy(r)
        next(v for v in bad["rules"] if v.get("parent"))["parent"] = "carrier"
        with self.assertRaises(ValueError):
            LocalModel.from_record(bad)

    def test_tiny_moment_is_not_a_match_by_default(self):
        fit = match_physical_moments(
            lambda _: {"activity": 1e-4},
            {"activity": 1e-8},
            {"x": (0.1, 1)},
            max_evaluations=1,
        )
        self.assertNotEqual(fit["status"], "matched")
        for scale, unit in ((1, "events"), (1000, "millievents")):
            fit = match_physical_moments(
                lambda _, scale=scale: {"activity": scale * 1.0005},
                {"activity": scale},
                {"x": (0.1, 1)},
                max_evaluations=1,
                moment_specs={
                    "activity": MomentSpec(
                        "activity",
                        unit,
                        16,
                        "continuous_integral",
                        absolute_tolerance=scale * 1e-12,
                    )
                },
            )
            self.assertEqual(fit["status"], "matched")

    def test_cache_matches_uncached_and_rejects_foreign_law(self):
        c = enumerate_model(switch(), [(0,)])
        context = EvaluationContext(c, 0.25)
        np.testing.assert_allclose(
            context.profile([1, 0], 8), history_profile(context.kernel, [1, 0], 8)
        )
        a = irreducible_asymptotics(c, 0.25, [1, 0])
        b = irreducible_asymptotics(c, 0.25, [1, 0], context=context)
        self.assertEqual(a, b)
        with self.assertRaises(ValueError):
            context.require(enumerate_model(switch(), [(0,)]), 0.25)
        with self.assertRaises(ValueError):
            context.require(c, 0.5)
        with self.assertRaises(ValueError):
            context.kernel[0, 0] = 0

    def test_matching_keeps_feasible_probe_despite_lower_infeasible_l2(self):
        fit = match_physical_moments(
            lambda p: {"a": 0.9 if p["x"] > 2 else 1.1, "b": 0.9 if p["x"] > 2 else 0},
            {"a": 0, "b": 0},
            {"x": (1, 4)},
            max_evaluations=1,
            moment_specs={
                k: MomentSpec(
                    k,
                    "events",
                    1,
                    "continuous_integral",
                    absolute_tolerance=1,
                    relative_tolerance=0,
                )
                for k in ("a", "b")
            },
        )
        self.assertEqual(fit["status"], "matched")
        self.assertGreater(fit["best"]["parameters"]["x"], 2)

    def test_finite_assay_accepts_reducibility_without_faking_asymptotics(self):
        m = LocalModel("two_sectors", [Coordinate("x", (0, 1), "static")], [], [])
        p = {
            "id": "sectors",
            "preparations": [
                {"id": str(i), "roots": [[[i], 1]], "conditioning": "full_present"}
                for i in (0, 1)
            ],
            "energy_per_root": "0",
            "coordinate_order": ["x"],
            "horizons": [1],
            "sufficiency": "full",
            "boundary_scope": {"bath": "one"},
            "conserved": [],
            "observables": [],
            "event_readouts": [],
            "scope": "test",
            "numerical": {
                "kernel_agreement_tolerance": 1e-12,
                "independent_history_tolerance": 1e-7,
            },
        }
        for mode in ("dense_reference", "sampled_endpoint_crosscheck"):
            r = evaluate_case(
                {**p, "validation_mode": mode}, {"id": "law", "model": m.record()}, 0.25
            )
            for row in r["rows"]:
                self.assertEqual(row["history"]["ell_bits"], 0)
                self.assertEqual(
                    row["asymptotic"]["status"], "unsupported_reducible_asymptotics"
                )
                self.assertIsNone(
                    row["horizon_diagnostics"]["rate_offset_profile_residual_bits"]
                )


if __name__ == "__main__":
    unittest.main()
