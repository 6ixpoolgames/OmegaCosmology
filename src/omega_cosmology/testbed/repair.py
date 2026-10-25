"""Small occupied repair/access motif, composed from native physical modules."""

from .occupancy import occupied_ecology


def repair_capacity_world(*, feedback=True, **settings):
    """R assists Y restoration; Y captures and assists reconstruction of R.

    Basal/unassisted paid construction and bank-independent breakdown stay.
    All damage is recoverable; no irreversible destruction is implied.
    """
    groups = [
        {
            "id": "repair",
            "members": ["repair.R", "repair.Y"],
            "access_member": "repair.Y",
        }
    ]
    defaults = {
        "bank_quantum": ".5",
        "formation_energy": ".5",
        "construction_bill_ticks": 2,
    }
    defaults.update(settings)
    if not feedback:
        defaults["converting_edges"] = [("repair.R", "repair.Y")]
    return occupied_ecology(groups, **defaults)
