"""Analytic and adversarial checks of ecological analysis, independent of rankings."""

import copy
import json
import sys
import unittest
from math import exp
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np

from omega_cosmology.testbed.analysis import comparison_profiles, interaction_effects
from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.ecology import (
    compile_functional_query,
    evaluate_functional_query,
)
from omega_cosmology.testbed.history import distributions_and_occupation
from omega_cosmology.testbed.models import enabling_world, two_copy_world
from omega_cosmology.testbed.physics import Condition as C
from omega_cosmology.testbed.physics import Coordinate, LocalModel, Rule
from omega_cosmology.testbed.structure import paired_state_probe, transition_audit


def condition(name, op, value):
    return {"coordinate": name, "operator": op, "value": value}


class StructuralAnalysisTests(unittest.TestCase):
    def test_signed_factorial_intervals_are_conservative(self):
        from omega_cosmology.testbed.analysis import linear_interval

        result = linear_interval([(1, 10, 12), (-1, 4, 6), (-1, 2, 3), (1, 1, 2)])
        self.assertEqual(result, {"lower": 2, "upper": 8})
        with self.assertRaises(ValueError):
            linear_interval([(1, 3, 2)])

    def switch(self):
        model = LocalModel(
            "switch",
            [Coordinate("bit", (0, 1), "physical")],
            [Rule("flip", (C("bit", "eq", 0),), (("bit", 1),), 0.2)],
            [],
        )
        compiled = enumerate_model(model, [(1,)])
        spec = {
            "id": "function",
            "definition": "bit is on",
            "coordinates": ["bit"],
            "functional_any_of": [[condition("bit", "eq", 1)]],
        }
        return compiled, compile_functional_query(compiled, spec)

    def test_return_survival_and_endpoint_are_distinct_analytic_quantities(self):
        compiled, query = self.switch()
        mu = np.zeros(2)
        mu[compiled.index[(1,)]] = 1
        endpoint, occupation = distributions_and_occupation(compiled, mu, 3)
        result = evaluate_functional_query(query, mu, 3, endpoint, occupation)
        self.assertAlmostEqual(
            result["endpoint_functional_probability"], 0.5 * (1 + exp(-1.2))
        )
        self.assertAlmostEqual(
            result["uninterrupted_initial_function_probability"], exp(-0.6)
        )
        self.assertAlmostEqual(
            result["initial_function_lost_then_returned_probability"],
            1 - exp(-0.6) * 1.6,
        )
        self.assertAlmostEqual(
            result["returned_and_functional_at_deadline_probability"],
            0.5 * (1 + exp(-1.2)) - exp(-0.6),
        )
        self.assertAlmostEqual(
            result["expected_entries"] - result["expected_exits"],
            result["endpoint_functional_probability"] - 1,
        )
        self.assertLess(result["physical_marginal_residual"], 1e-12)

    def test_initially_absent_paths_are_not_counted_as_recovered_survivors(self):
        compiled, query = self.switch()
        mu = np.zeros(2)
        mu[compiled.index[(0,)]] = 1
        endpoint, occupation = distributions_and_occupation(compiled, mu, 3)
        result = evaluate_functional_query(query, mu, 3, endpoint, occupation)
        self.assertAlmostEqual(result["ever_functional_probability"], 1 - exp(-0.6))
        self.assertEqual(result["initial_function_lost_then_returned_probability"], 0)
        self.assertEqual(result["uninterrupted_initial_function_probability"], 0)

    def test_functional_query_handles_absorbing_single_state_and_budget(self):
        model = LocalModel("constant", [Coordinate("bit", (0, 1), "physical")], [], [])
        compiled = enumerate_model(model, [(1,)])
        spec = {
            "id": "on",
            "definition": "on",
            "coordinates": ["bit"],
            "functional_any_of": [[condition("bit", "eq", 1)]],
        }
        query = compile_functional_query(compiled, spec)
        result = evaluate_functional_query(query, [1], 5, [1], [5])
        self.assertEqual(result["uninterrupted_initial_function_probability"], 1)
        self.assertEqual(result["expected_exits"], 0)
        with self.assertRaises(MemoryError):
            compile_functional_query(compiled, spec, max_query_states=3)

    def test_unmarked_individual_function_rejected(self):
        model, root = two_copy_world(quotient=True)
        c = enumerate_model(model, [root])
        with self.assertRaises(ValueError):
            compile_functional_query(
                c,
                {
                    "id": "one",
                    "definition": "first only",
                    "coordinates": ["first"],
                    "functional_any_of": [[condition("first", "eq", 1)]],
                },
            )

    def test_local_probe_distinguishes_acceleration_from_required_support(self):
        model, _ = enabling_world(expansion=True)
        c = enumerate_model(model, [(1, 1, 1, 1, 2, 0)])
        result = paired_state_probe(
            c,
            {
                "id": "unlock",
                "when": [condition("bond", "eq", 1), condition("carrier", "eq", 1)],
                "replace": {"bond": 0},
                "selector": {"rules": ["unlock_basal", "unlock_motif"], "direction": 1},
            },
        )
        self.assertGreater(result["counts"]["faster_in_original"], 0)
        self.assertEqual(result["counts"]["enabled_only_in_original"], 0)
        self.assertTrue(all(x["counterpart_rate"] > 0 for x in result["examples"]))
        bad = {
            "id": "invalid",
            "when": [condition("bond", "eq", 1)],
            "replace": {"a.active": 0},
            "selector": {"rules": ["unlock_basal"], "direction": 1},
        }
        invalid = paired_state_probe(c, bad)
        self.assertEqual(invalid["counts"]["paired"], 0)
        self.assertGreater(invalid["counts"]["invalid_counterpart"], 0)

    def test_audit_exposes_refund_lock_without_declaring_physical_impossibility(self):
        model, _ = enabling_world(expansion=True)
        c = enumerate_model(model, [(1, 1, 1, 1, 2, 0)])
        spec = {
            "id": "dissolution",
            "when": [condition("store.built", "eq", 1), condition("bank", "ge", 3)],
            "selector": {
                "rules": ["build_store", "build_store_assisted"],
                "direction": -1,
            },
        }
        result = transition_audit(c, spec)
        self.assertGreater(result["eligible_states"], 0)
        self.assertEqual(result["route_absent_states"], result["eligible_states"])
        spec["selector"]["rules"] = ["typo"]
        with self.assertRaises(ValueError):
            transition_audit(c, spec)

    def test_horizon_changes_are_not_cadence_changes(self):
        rows = [
            {"id": "pair", "horizon": t, "cadence": dt, "delta_ell_bits": v}
            for dt in (0.125, 0.25)
            for t, v in [(1, -1), (2, 2), (3, -3)]
        ]
        report = comparison_profiles(rows, 1e-9)
        self.assertFalse(any(r["strict_sign_flip"] for r in report["cadence_audit"]))
        self.assertTrue(
            all(len(r["sign_change_brackets"]) == 2 for r in report["horizon_audit"])
        )
        self.assertEqual(
            report["horizon_audit"][0]["intervals"][1]["mean_delta_bits_per_time"], -5
        )
        with self.assertRaises(ValueError):
            comparison_profiles(rows + rows[:1], 1e-9)

    def test_retained_r2_has_nine_horizon_groups_with_changes_and_no_cadence_flips(
        self,
    ):
        retained = json.loads(
            (
                ROOT
                / "research/studies/R2-further-capacity/results-2026-10-24/ANALYSIS.json"
            ).read_text()
        )
        report = comparison_profiles(retained["comparisons"], 1e-7)
        self.assertEqual(sum(r["strict_sign_flip"] for r in report["cadence_audit"]), 0)
        self.assertEqual(sum(r["strict_sign_flip"] for r in report["horizon_audit"]), 9)

    def test_interaction_effects_preserve_metric_disagreement_and_unresolved_bounds(
        self,
    ):
        base = {
            "contrast_id": "enable-A",
            "source": "A",
            "target": "B",
            "metric": "function_time",
            "units": "time",
            "comparison_kind": "mechanism",
            "scope": "B",
            "conditioning": "full_present",
            "evidence": "reference-case",
            "horizon": 10,
            "lower": -2,
            "upper": -1,
            "tolerance": 1e-8,
        }
        breadth = {
            **base,
            "metric": "history.projected_given_full_present",
            "units": "bits",
            "lower": 1,
            "upper": 3,
        }
        unresolved = {**base, "target": "whole", "lower": -1, "upper": 2}
        result = interaction_effects([base, breadth, unresolved])
        self.assertEqual(
            [r["resolved_sign"] for r in result["effects"]],
            ["negative", "positive", "unresolved"],
        )
        process = {**base, "comparison_kind": "process"}
        with self.assertRaises(ValueError):
            interaction_effects([process])

    def test_sequence_monitor_cannot_be_relabelled_ancestry(self):
        from omega_cosmology.testbed.monitors import compile_monitor

        compiled, _ = self.switch()
        with self.assertRaises(ValueError):
            compile_monitor(
                compiled,
                {"id": "false", "evidence_kind": "causal_ancestry", "stages": []},
            )

    def test_shared_assay_exposes_optional_functional_profiles(self):
        from omega_cosmology.testbed.finite_study import evaluate_case

        p = json.loads(
            (ROOT / "research/studies/R2-further-capacity/PROTOCOL.json").read_text()
        )
        p["horizons"] = [1]
        p["preparations"] = p["preparations"][:1]
        p["monitors"] = []
        p["structural_analysis"] = {
            "organizations": [
                {
                    "id": "assembly",
                    "definition": "bound",
                    "coordinates": ["bond"],
                    "functional_any_of": [[condition("bond", "eq", 1)]],
                }
            ]
        }
        p["structural_analysis"]["ancestry"] = [
            {
                "id": "bond_to_store",
                "presence_coordinates": ["bond", "store.built"],
                "depth_cap": 3,
                "identity_definition": "Native constructed contact and store instances",
                "assistance_edges": [
                    {
                        "rule": "build_store_assisted",
                        "parent": "bond",
                        "child": "store.built",
                    }
                ],
            }
        ]
        a = evaluate_case(p, p["laws"][0], 0.25)
        plain = copy.deepcopy(p)
        del plain["structural_analysis"]
        b = evaluate_case(plain, plain["laws"][0], 0.25)
        self.assertEqual(
            a["rows"][0]["history"]["ell_bits"], b["rows"][0]["history"]["ell_bits"]
        )
        self.assertIn("assembly", a["rows"][0]["functional_profiles"])
        ancestry = a["rows"][0]["assistance_ancestry"]["bond_to_store"]
        self.assertGreater(ancestry["expected_assisted_births_by_depth"]["1"], 0)
        self.assertEqual(ancestry["ever_reached_depth_probability"], 0)


if __name__ == "__main__":
    unittest.main()
