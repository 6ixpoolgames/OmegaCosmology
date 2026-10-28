"""Compatibility checks that separate new contracts from retained physics."""

from omega_cosmology.testbed.backends import enumerate_model


def assert_metadata_only_upgrade(test, current, retained):
    def native_record(model):
        record = model.record()
        record.pop("material")  # checked independently as an executable contract
        for rule in record["rules"]:
            for key in ("roles", "parent", "child"):
                rule.pop(key, None)
        return record

    test.assertEqual(native_record(current), native_record(retained))
    test.assertEqual(current.material_status, "executable")
    root = tuple(c.domain[0] for c in current.coordinates)
    a = enumerate_model(current, [root])
    b = enumerate_model(retained, [root])
    a.require_complete()
    b.require_complete()
    test.assertEqual(a.states, b.states)
    test.assertEqual((a.q != b.q).nnz, 0)
    test.assertEqual(a.ledger, b.ledger)
