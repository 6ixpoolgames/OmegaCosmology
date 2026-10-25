"""Native marked genealogy checks; the worlds are engineering references only."""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from omega_cosmology.testbed.ancestry import (
    compile_ancestry_query,
    evaluate_ancestry_query,
)
from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.history import (
    distributions_and_occupation,
    history_profile,
    sampled_kernel,
)
from omega_cosmology.testbed.physics import Condition as C
from omega_cosmology.testbed.physics import Coordinate, LocalModel, Rule


def reference(edges, fields):
    rules = [Rule("basal_" + f, (C(f, "eq", 0),), ((f, 1),), 0.1) for f in fields]
    descriptors = []
    for parent, child in edges:
        name = parent + "_builds_" + child
        rules.append(
            Rule(name, (C(parent, "eq", 1), C(child, "eq", 0)), ((child, 1),), 0.2)
        )
        descriptors.append({"rule": name, "parent": parent, "child": child})
    model = LocalModel(
        "labelled-reference",
        [Coordinate(f, (0, 1), "component") for f in fields],
        rules,
        [],
    )
    root = tuple(int(f == "a") for f in fields)
    compiled = enumerate_model(model, [root])
    mu = np.zeros(len(compiled.states))
    mu[compiled.index[root]] = 1
    spec = {
        "id": "ancestry",
        "presence_coordinates": fields,
        "depth_cap": 3,
        "identity_definition": "Distinct physical slots; loss ends this construction instance",
        "assistance_edges": descriptors,
    }
    return compiled, mu, spec


class AncestryTests(unittest.TestCase):
    def test_three_unconnected_assisted_births_are_not_depth_three(self):
        c, mu, spec = reference(
            [("a", "b"), ("a", "c"), ("a", "d")], ["a", "b", "c", "d"]
        )
        query = compile_ancestry_query(c, spec, mu)
        endpoint, _ = distributions_and_occupation(c, mu, 10)
        r = evaluate_ancestry_query(query, 10, endpoint)
        self.assertGreater(r["expected_assisted_births_by_depth"]["1"], 0)
        self.assertEqual(r["expected_assisted_births_by_depth"]["2"], 0)
        self.assertEqual(r["ever_reached_depth_probability"], 0)

    def test_cyclic_connected_births_reach_depth_three_and_preserve_physics(self):
        c, mu, spec = reference([("a", "b"), ("b", "c"), ("c", "a")], ["a", "b", "c"])
        original_hash = c.generator_hash
        score = history_profile(sampled_kernel(c, 0.25), mu, 40)[-1]
        query = compile_ancestry_query(c, spec, mu)
        self.assertIn((c.index[(1, 1, 1)], (3, 1, 2), True), query["states"])
        endpoint, _ = distributions_and_occupation(c, mu, 10)
        r = evaluate_ancestry_query(query, 10, endpoint)
        self.assertGreater(r["ever_reached_depth_probability"], 0)
        self.assertGreaterEqual(
            r["expected_assisted_births_by_depth"]["3"],
            r["ever_reached_depth_probability"],
        )
        self.assertLess(r["physical_marginal_residual"], 1e-12)
        self.assertEqual(c.generator_hash, original_hash)
        self.assertEqual(history_profile(sampled_kernel(c, 0.25), mu, 40)[-1], score)

    def test_basal_replacement_resets_depth_without_erasing_past_completion(self):
        c, mu, spec = reference([("a", "b"), ("b", "c"), ("c", "a")], ["a", "b", "c"])
        query = compile_ancestry_query(c, spec, mu)
        states = {key: i for i, key in enumerate(query["states"])}
        # The depth-3 A was lost. Its next unassisted birth has depth zero,
        # while the historical success marker remains true.
        source = (c.index[(0, 1, 1)], (-1, 1, 2), True)
        target = (c.index[(1, 1, 1)], (0, 1, 2), True)
        self.assertGreater(query["q"][states[source], states[target]], 0)
        self.assertIn((c.index[(1, 1, 1)], (3, 1, 2), True), states)

    def test_query_budget_and_nonphysical_assistance_are_rejected(self):
        c, mu, spec = reference([("a", "b"), ("b", "c"), ("c", "a")], ["a", "b", "c"])
        with self.assertRaises(MemoryError):
            compile_ancestry_query(c, spec, mu, max_query_states=2)
        spec["assistance_edges"][0]["rule"] = "basal_b"
        with self.assertRaises(ValueError):
            compile_ancestry_query(c, spec, mu)

    def test_equivalent_but_unmarked_units_need_identity_audit(self):
        from omega_cosmology.testbed.models import two_copy_world

        model, root = two_copy_world(quotient=True)
        c = enumerate_model(model, [root])
        mu = np.zeros(len(c.states))
        mu[c.index[root]] = 1
        with self.assertRaises(ValueError):
            compile_ancestry_query(c, {}, mu)


if __name__ == "__main__":
    unittest.main()
