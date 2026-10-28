"""Scheduled laws checked against explicit history words and physical identities."""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from omega_cosmology.testbed.history import entropy, history_profile, sampled_kernel
from omega_cosmology.testbed.matching import match_physical_moments
from omega_cosmology.testbed.operations import operation_world
from omega_cosmology.testbed.phases import (
    compile_phases,
    continuous_schedule,
    event_then_return,
    projected_schedule_profiles,
    sampled_schedule_profiles,
)
from omega_cosmology.testbed.physics import Condition as C
from omega_cosmology.testbed.physics import Coordinate, EnergyTerm, LocalModel, Rule
from omega_cosmology.testbed.repair import repair_capacity_world
from omega_cosmology.testbed.thermodynamics import audit_equilibrium


def word_entropy(runs, mu, labels):
    words = {(): np.array(mu, dtype=float)}
    for p, length in runs:
        for _ in range(length):
            next_words = {}
            for word, distribution in words.items():
                outgoing = distribution @ p
                for label in set(labels):
                    masked = outgoing * np.array([v == label for v in labels])
                    next_words[word + (label,)] = masked
            words = next_words
    return float(entropy([v.sum() for v in words.values()]))


class PhasedTests(unittest.TestCase):
    def test_history_and_projected_memory_cross_boundary(self):
        p = np.array([[0.6, 0.3, 0.1], [0.2, 0.4, 0.4], [0.1, 0.7, 0.2]])
        q = np.array([[0.1, 0.2, 0.7], [0.7, 0.2, 0.1], [0.3, 0.5, 0.2]])
        runs = [(p, 2), (q, 3)]
        mu = [1, 0, 0]
        full = sampled_schedule_profiles(runs, mu, [5])[5]["ell_bits"]
        self.assertAlmostEqual(full, word_entropy(runs, mu, [0, 1, 2]), places=12)
        exact = word_entropy(runs, mu, [0, 0, 1])
        previous = None
        for memory in range(5):
            bound = projected_schedule_profiles(
                runs, mu, [0, 0, 1], [5], memory=memory
            )[5]
            self.assertLessEqual(bound["lower_bits"], exact + 1e-12)
            self.assertGreaterEqual(bound["upper_bits"], exact - 1e-12)
            if previous:
                self.assertLessEqual(
                    previous["lower_bits"], bound["lower_bits"] + 1e-12
                )
                self.assertGreaterEqual(
                    previous["upper_bits"], bound["upper_bits"] - 1e-12
                )
            previous = bound
        self.assertAlmostEqual(previous["upper_bits"], exact, places=12)
        self.assertAlmostEqual(previous["lower_bits"], exact, places=12)
        # Endpoint entropy omits the history that the adapter must keep.
        end = np.array(mu) @ p @ p @ q @ q @ q
        self.assertGreater(full, entropy(end) + 1)

    def test_split_invariance_full_and_nonmarkov_projection(self):
        p = np.array([[0.6, 0.3, 0.1], [0.2, 0.4, 0.4], [0.1, 0.7, 0.2]])
        a, b = [(p, 7)], [(p, 2), (p, 5)]
        aa = sampled_schedule_profiles(a, [1, 0, 0], [7])[7]
        bb = sampled_schedule_profiles(b, [1, 0, 0], [7])[7]
        self.assertAlmostEqual(aa["ell_bits"], history_profile(p, [1, 0, 0], 7)[-1])
        self.assertEqual(aa["ell_bits"], bb["ell_bits"])
        for m in (0, 1, 2):
            x = projected_schedule_profiles(a, [1, 0, 0], [0, 0, 1], [7], memory=m)[7]
            y = projected_schedule_profiles(b, [1, 0, 0], [0, 0, 1], [7], memory=m)[7]
            self.assertAlmostEqual(x["lower_bits"], y["lower_bits"], places=12)
            self.assertAlmostEqual(x["upper_bits"], y["upper_bits"], places=12)

    def test_union_state_order_and_no_silent_energy_quench(self):
        coords = [Coordinate("x", (0, 1), "test"), Coordinate("y", (0, 1), "test")]
        a = LocalModel(
            "a", coords, [Rule("x", (C("x", "eq", 0),), (("x", 1),), 0.2)], []
        )
        b = LocalModel(
            "b", coords, [Rule("y", (C("y", "eq", 0),), (("y", 1),), 0.3)], []
        )
        compiled = compile_phases([a, b], [(0, 0)], max_states=4)
        self.assertEqual(len(compiled[0].states), 4)
        self.assertEqual(compiled[0].states, compiled[1].states)
        b.energy_terms = (EnergyTerm("1", "x"),)
        with self.assertRaises(ValueError):
            compile_phases([a, b], [(0, 0)])

    def test_projection_caps_and_unknown_root_not_reinterpreted(self):
        p = np.array([[0.8, 0.1, 0.1], [0.2, 0.5, 0.3], [0.1, 0.2, 0.7]])
        with self.assertRaises(ValueError):
            projected_schedule_profiles([(p, 5)], [0.5, 0.5, 0], [0, 0, 1], [5])
        with self.assertRaises(MemoryError):
            projected_schedule_profiles(
                [(p, 5)], [1, 0, 0], [0, 0, 1], [5], memory=4, max_words=4
            )

    def test_paid_damage_contact_fate_and_common_recovery(self):
        base = repair_capacity_world()
        original = base.fingerprint()
        idle = operation_world(base)
        damage = operation_world(base, target="repair.R", stroke_conductance=0.2)
        sham = operation_world(base, stroke_conductance=0.2)
        root = (1, 1, 2, 1, 0, 0, 0)
        phases = compile_phases([damage, idle, sham], [root])
        for compiled in phases:
            self.assertEqual(audit_equilibrium(compiled)["status"], "passed")
        fault, recovery, control = phases
        self.assertEqual(base.fingerprint(), original)
        self.assertEqual(fault.states, recovery.states)
        bound_seen = False
        for i, j, event in fault.ledger:
            if event.rule_id.startswith("operation.stroke"):
                self.assertAlmostEqual(event.delta_energy, event.work - event.heat)
                reverse = [
                    e
                    for x, y, e in fault.ledger
                    if x == j and y == i and e.rule_id == event.rule_id
                ]
                self.assertEqual(len(reverse), 1)
                if event.direction == 1:
                    s, t = fault.states[i], fault.states[j]
                    self.assertEqual(t[0], 0)
                    self.assertEqual(t[2], s[2] - 1)
                    self.assertEqual(t[-1], 1)
                    for c in (4, 5):
                        self.assertEqual(t[c], 0)
                        bound_seen |= s[c] == 1
        self.assertTrue(bound_seen)
        for i, j, e in control.ledger:
            if e.rule_id.startswith("operation.stroke"):
                self.assertEqual(control.states[i][:2], control.states[j][:2])
                self.assertEqual(control.states[i][4:6], control.states[j][4:6])
        mu = np.zeros(len(fault.states))
        mu[fault.index[root]] = 1
        runs = [(fault, 4), (recovery, 12)]
        ledger = continuous_schedule(runs, mu, 0.25, 4)
        self.assertLess(abs(ledger["physical"]["energy_residual"]), 1e-10)
        monitor = event_then_return(
            runs, mu, 0.25, 4, "operation.stroke", lambda s: s[0] == s[1] == 1
        )
        self.assertGreater(monitor["any_forward_operation_probability"], 0)
        self.assertLess(monitor["any_forward_operation_probability"], 1)
        self.assertGreater(monitor["operation_then_functional_return_probability"], 0)
        np.testing.assert_allclose(
            monitor["physical_marginal"], ledger["endpoint"], atol=1e-12
        )
        kernels = [(sampled_kernel(c, 0.25), k) for c, k in runs]
        sampled = sampled_schedule_profiles(kernels, mu, [16])[16]
        np.testing.assert_allclose(sampled["endpoint"], ledger["endpoint"], atol=1e-12)

    def test_event_monitor_analytic_no_operation_probability(self):
        model = LocalModel(
            "switch",
            [Coordinate("x", (0, 1), "test")],
            [Rule("op", (C("x", "eq", 0),), (("x", 1),), 0.4)],
            [],
        )
        (c,) = compile_phases([model], [(0,)])
        mu = np.zeros(len(c.states))
        mu[c.index[(0,)]] = 1
        result = event_then_return([(c, 4)], mu, 0.25, 1, "op", lambda s: s[0] == 0)
        self.assertAlmostEqual(
            result["no_forward_operation_probability"], np.exp(-0.4), places=12
        )

    def test_scheduled_assay_reduces_to_static_history_and_checks_alignment(self):
        from omega_cosmology.testbed.scheduled_study import evaluate_scheduled_case

        model = LocalModel(
            "small-assay",
            [Coordinate("x", (0, 1), "physical_register")],
            [Rule("thermal", (C("x", "eq", 0),), (("x", 1),), 0.3)],
            [EnergyTerm(".25", "x")],
        )
        protocol = {
            "id": "small-assay",
            "present_id": "common",
            "root": [0],
            "energy_per_root": "0",
            "coordinate_order": ["x"],
            "cadence": 0.25,
            "horizons": [0.5, 1],
            "phases": [{"model": model.record(), "duration": 0.5}] * 2,
            "sufficiency": "complete finite physical register, known schedule",
            "boundary_scope": {"bath": "one"},
            "matched": {"endowment": "same"},
            "implementation": "no-change schedule",
            "observables": [{"id": "x", "terms": [["x", 1]]}],
            "functional_conditions": [
                {"coordinate": "x", "operator": "eq", "value": 0}
            ],
            "projected_histories": [{"id": "x", "coordinates": ["x"], "memory": 1}],
            "max_states": 10,
            "max_dense_bytes": 1024**2,
            "max_projection_bytes": 1024**2,
        }
        result = evaluate_scheduled_case(protocol)
        (c,) = compile_phases([model], [(0,)])
        p = sampled_kernel(c, 0.25)
        static = history_profile(p, [1, 0], 4)
        for row in result["rows"]:
            k = round(row["horizon"] / 0.25)
            self.assertAlmostEqual(row["history"]["ell_bits"], static[k], places=12)
            self.assertAlmostEqual(
                row["projected_histories"]["x"]["upper_bits"], static[k], places=12
            )
            self.assertLess(abs(row["physical"]["energy_residual"]), 1e-12)
        protocol["phases"][0] = {"model": model.record(), "duration": 0.3}
        with self.assertRaises(ValueError):
            evaluate_scheduled_case(protocol)

    def test_match_search_separates_feasible_and_unmatched_without_score(self):
        calls = []

        def moments(p):
            calls.append(p)
            return {"activity": p["x"] + p["y"], "work": p["x"] - p["y"]}

        result = match_physical_moments(
            moments, {"activity": 1.2, "work": 0.4}, {"x": [0.01, 1], "y": [0.01, 1]}
        )
        self.assertEqual(result["status"], "matched")
        self.assertTrue(
            all(0.01 - 1e-12 <= v <= 1 + 1e-12 for p in calls for v in p.values())
        )
        self.assertLessEqual(len(calls), 9 + 24)
        missing = match_physical_moments(
            moments, {"activity": 20, "work": 10}, {"x": [0.01, 1], "y": [0.01, 1]}
        )
        self.assertEqual(missing["status"], "not_matched_in_bounded_search")


if __name__ == "__main__":
    unittest.main()
