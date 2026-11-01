import unittest
from itertools import combinations

from omega_cosmology.testbed.backends import enumerate_model
from omega_cosmology.testbed.spatial import spatial_root, spatial_world
from omega_cosmology.testbed.thermodynamics import audit_equilibrium


class SpatialTests(unittest.TestCase):
    def test_tiny_alphabet_and_equilibrium(self):
        model = spatial_world(2)
        roots = []
        for a in combinations(range(4), 2):
            roots.append(
                tuple(
                    (1 if i in a else 2) if i < 4 else 0
                    for i in range(len(model.coordinates))
                )
            )
        compiled = enumerate_model(model, roots, max_states=400)
        compiled.require_complete()
        self.assertEqual(len(compiled.states), 378)
        self.assertEqual(audit_equilibrium(compiled)["status"], "passed")
        self.assertTrue(
            all(
                model.inventory(s)["species.1"] == "2"
                and model.inventory(s)["species.2"] == "2"
                for s in compiled.states
            )
        )

    def test_local_assistance_is_paid_and_reversible(self):
        model = spatial_world()
        values = {
            "site.0": 1,
            "site.3": 1,
            "site.1": 2,
            "site.4": 2,
            "bond.0.3": 1,
            "bank": 1,
        }
        root = tuple(values.get(c.name, 0) for c in model.coordinates)
        events = [e for e in model.events(root) if e.rule_id.startswith("assist.")]
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event.delta_energy, -0.5)
        self.assertEqual(event.heat, 0.5)
        self.assertEqual(event.target[model.indices["bank"]], 0)
        reverse = next(
            e
            for e in model.events(event.target)
            if e.rule_id == event.rule_id and e.direction == -1
        )
        self.assertEqual(reverse.target, root)
        self.assertAlmostEqual(event.rate / reverse.rate, 1.6487212707001282)
        missing = list(root)
        missing[model.indices["bond.0.3"]] = 0
        self.assertFalse(
            any(e.rule_id.startswith("assist.") for e in model.events(tuple(missing)))
        )

    def test_dimer_motion_preserves_bond_material_and_energy(self):
        model = spatial_world()
        values = {
            "site.0": 1,
            "site.1": 1,
            "site.3": 2,
            "site.4": 2,
            "bond.0.1": 1,
            "bank": 2,
        }
        root = tuple(values.get(c.name, 0) for c in model.coordinates)
        events = [e for e in model.events(root) if e.rule_id.startswith("translate.")]
        self.assertTrue(events)
        for event in events:
            self.assertEqual(event.delta_energy, 0)
            self.assertEqual(model.inventory(event.target), model.inventory(root))
            self.assertEqual(
                sum(
                    event.target[model.indices[c.name]]
                    for c in model.coordinates
                    if c.role == "structural_bond"
                ),
                1,
            )

    def test_capture_and_initial_charge_are_physical(self):
        model = spatial_world()
        self.assertEqual(float(model.energy(spatial_root(model))), 2)
        self.assertEqual(float(model.energy(spatial_root(model, bank=0))), 0)
        values = {
            "site.0": 1,
            "site.3": 1,
            "site.1": 2,
            "site.4": 2,
            "bond.1.4": 1,
            "carrier": 2,
        }
        root = tuple(values.get(c.name, 0) for c in model.coordinates)
        e = next(e for e in model.events(root) if e.rule_id.startswith("capture.B."))
        self.assertEqual(e.target[model.indices["bank"]], 1)
        self.assertEqual(e.heat, 1)
        self.assertEqual(e.work, 0)

    def test_reflection_preserves_aggregated_physics(self):
        model = spatial_world()

        def reflect(state):
            result = list(state)

            def site(i):
                return i // 3 * 3 + 2 - i % 3

            for c in model.coordinates:
                if c.name.startswith("site."):
                    mapped = f"site.{site(int(c.name.split('.')[1]))}"
                elif c.name.startswith("bond."):
                    i, j = sorted(site(int(x)) for x in c.name.split(".")[1:])
                    mapped = f"bond.{i}.{j}"
                else:
                    mapped = c.name
                result[model.indices[mapped]] = state[model.indices[c.name]]
            return tuple(result)

        root = spatial_root(model)

        def rates(state, transform):
            result = {}
            for event in model.events(state):
                key = transform(event.target)
                result[key] = result.get(key, 0) + event.rate
            return result

        expected = rates(root, reflect)
        actual = rates(reflect(root), lambda s: s)
        self.assertEqual(expected.keys(), actual.keys())
        for target in expected:
            self.assertAlmostEqual(expected[target], actual[target])


if __name__ == "__main__":
    unittest.main()
