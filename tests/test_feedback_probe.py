"""Concrete P001 risks: physical maps, causal policy semantics, scope and transport."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from omega_cosmology.feedback_probe import Model, POLICIES, packing_size


class FeedbackProbeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = Model.read(ROOT / "research/probes/P001/fixture.json")

    def test_feedback_agrees_with_archived_quantum_matrix(self):
        # Compile without creating a __pycache__ inside the source snapshot.
        source = ROOT / "sources/quantum_continuation/10_FINITE_QUANTUM_CONTINUATION_VERIFY.py"
        module = types.ModuleType("p001_archived_quantum")
        module.__file__ = str(source)
        sys.modules[module.__name__] = module
        exec(compile(source.read_text(encoding="utf-8"), str(source), "exec"), module.__dict__)
        for i in range(8):
            s = tuple(module.bits(i, 3)) + (0, 0, 0)
            target = self.model.gate("feedback", s)
            for j in range(8):
                expected = module.ONE if j == module.index(target[:3]) else module.Z0
                self.assertEqual(module.TOFFOLI[j][i], expected)

    def test_every_gate_is_reversible_on_full_state_space(self):
        states = set(product((0, 1), repeat=6))
        for gate in self.model.fixture["gates"]:
            self.assertEqual({self.model.gate(gate, s) for s in states}, states)
            for s in states:
                self.assertEqual(self.model.gate(gate, self.model.gate(gate, s)), s)

    def test_all_causal_policies_normalize_and_match_independent_formula(self):
        for mode, p in product((0, 1), POLICIES):
            for scope in ("full", "actuator"):
                self.assertEqual(sum(self.model.law(mode, p, scope).values()), 1)
            for r in (0, 1):
                branch = self.model.branch(mode, r, p)
                b1, b2 = branch["controls"]
                a1, a2 = branch["actuator_records"]
                self.assertEqual((a1, a2), (mode * (r ^ b1), mode * b2))
                self.assertEqual(self.model.canonical(branch["states"][-1]),
                                 (r ^ b1 ^ b2, mode, a2, r, a1, a2))
                self.assertEqual(branch["weight"], Fraction(1, 2))
                self.assertEqual(self.model.value(branch["states"][2], "actuator"), 0)

    def test_later_policy_cannot_change_prior_record(self):
        for mode, r, first in product((0, 1), (0, 1), product((0, 1), repeat=2)):
            prefixes = {self.model.branch(mode, r, first + later)["states"][:4]
                        for later in product((0, 1), repeat=4)}
            self.assertEqual(len(prefixes), 1)

    def test_equal_full_geometry_but_unequal_control_responses(self):
        for mode in (0, 1):
            matrix, _ = self.model.metric(mode, "full")
            self.assertEqual(matrix, [[0, 1], [1, 0]])
            self.assertEqual(packing_size(matrix, Fraction(0))[0], 2)
            self.assertEqual(packing_size(matrix, Fraction(999, 1000))[0], 2)
            self.assertEqual(packing_size(matrix, Fraction(1))[0], 1)
            for r in (0, 1):
                reachable = {self.model.branch(mode, r, p)["actuator_records"] for p in POLICIES}
                self.assertEqual(reachable, {(0, 0)} if mode == 0 else set(product((0, 1), repeat=2)))
        p = (1, 0, 1, 1, 1, 1)
        self.assertEqual(self.model.law(0, p, "actuator"), {(0, 0): Fraction(1)})
        self.assertEqual(self.model.law(1, p, "actuator"), {(1, 1): Fraction(1)})

    def test_bounded_scope_changes_geometry_and_duplicate_names_do_not(self):
        self.assertEqual(self.model.metric(0, "actuator")[0], [[0, 0], [0, 0]])
        self.assertEqual(self.model.metric(1, "actuator")[0], [[0, 1], [1, 0]])
        for m, scope in product((0, 1), ("full", "actuator")):
            self.assertEqual(self.model.metric(m, scope), self.model.metric(m, scope, POLICIES * 2))

    def test_presentation_transport_of_maps_and_all_policy_responses(self):
        transported = self.model.transported()
        for name, s in product(self.model.fixture["gates"], product((0, 1), repeat=6)):
            self.assertEqual(transported.gate(name, tuple(reversed(s))),
                             tuple(reversed(self.model.gate(name, s))))
        for mode, p, r in product((0, 1), POLICIES, (0, 1)):
            a, b = self.model.branch(mode, r, p), transported.branch(mode, r, p)
            self.assertEqual(a["history"], b["history"])
            self.assertEqual(a["weight"], b["weight"])
            self.assertEqual(a["states"], tuple(tuple(reversed(s)) for s in b["states"]))
            for scope in ("full", "actuator"):
                self.assertEqual(self.model.law(mode, p, scope, r), transported.law(mode, p, scope, r))

    def test_same_working_state_does_not_erase_occurrence_records(self):
        # f(r)=r, g=0 gives identical terminal SMA but different actual R0 records.
        p = (0, 1, 0, 0, 0, 0)
        a, b = (self.model.branch(1, r, p) for r in (0, 1))
        self.assertEqual(a["states"][-1][:3], b["states"][-1][:3])
        self.assertNotEqual(a["states"][-1], b["states"][-1])
        self.assertNotEqual(a["history"], b["history"])
        self.assertEqual(len(self.model.law(1, p, "full")), 2)


if __name__ == "__main__":
    unittest.main()
