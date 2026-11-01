"""Small resolved-site chemistry; rules feed the existing audited event engine."""

from itertools import combinations, product

from .physics import Condition as C
from .physics import Coordinate, LocalModel, Rule
from .physics import EnergyTerm as E


def ladder_edges(columns):
    if type(columns) is not int or columns < 2:
        raise ValueError("At least two columns required")
    return tuple(
        [
            (r * columns + c, r * columns + c + 1)
            for r in range(2)
            for c in range(columns - 1)
        ]
        + [(c, c + columns) for c in range(columns)]
    )


def spatial_world(columns=3):
    """Two particles/species, matching bonds and a rapidly mixed chemical medium.

    No selector or operation apparatus. Unmarked same-species particles are
    encoded by site occupancy; absolute sites remain resolved.
    """
    edges = ladder_edges(columns)
    n = 2 * columns
    sites = [f"site.{i}" for i in range(n)]
    bonds = [f"bond.{i}.{j}" for i, j in edges]
    incident = {i: [k for k, e in enumerate(edges) if i in e] for i in range(n)}
    coordinates = (
        [Coordinate(s, (0, 1, 2), "site_occupancy") for s in sites]
        + [Coordinate(b, (0, 1), "structural_bond") for b in bonds]
        + [
            Coordinate("carrier", (0, 1, 2), "chemical_conformation"),
            Coordinate("bank", (0, 1, 2), "charged_storage_count"),
        ]
    )
    forbidden = []
    for k, (i, j) in enumerate(edges):
        for v in (i, j):
            forbidden.append((C(bonds[k], "eq", 1), C(sites[v], "eq", 0)))
    for v in range(n):
        for a, b in combinations(incident[v], 2):
            forbidden.append((C(bonds[a], "eq", 1), C(bonds[b], "eq", 1)))
    rules = []
    for k, (i, j) in enumerate(edges):
        for species in (1, 2):
            guards = (C(sites[i], "eq", species), C(sites[j], "eq", 0))
            guards += tuple(C(bonds[b], "eq", 0) for b in incident[i])
            rules.append(
                Rule(
                    f"hop.{k}.{species}",
                    guards,
                    ((sites[i], -species), (sites[j], species)),
                    0.08,
                    roles=("motion.monomer",),
                )
            )
        for si, sj in product((1, 2), repeat=2):
            guard = (
                C(sites[i], "eq", si),
                C(sites[j], "eq", sj),
                C(bonds[k], "eq", 0),
                C("bank", "ge", 1),
            )
            changes = ((bonds[k], 1), ("bank", -1))
            rules.append(
                Rule(
                    f"assemble.{k}.{si}.{sj}",
                    guard,
                    changes,
                    0.003,
                    roles=("construction.basal",),
                    child=bonds[k],
                )
            )
            if si == sj == 2:
                for a, (u, v) in enumerate(edges):
                    if {u, v} & {i, j}:
                        continue
                    contact = any(
                        tuple(sorted((x, y))) in edges for x in (u, v) for y in (i, j)
                    )
                    if contact:
                        helper = (
                            C(sites[u], "eq", 1),
                            C(sites[v], "eq", 1),
                            C(bonds[a], "eq", 1),
                        )
                        rules.append(
                            Rule(
                                f"assist.{a}.{k}",
                                guard + helper,
                                changes,
                                0.15,
                                roles=("construction.assisted",),
                                parent=bonds[a],
                                child=bonds[k],
                            )
                        )
            if si == sj == 2:
                rules.append(
                    Rule(
                        f"capture.B.{k}",
                        (
                            C(sites[i], "eq", 2),
                            C(sites[j], "eq", 2),
                            C(bonds[k], "eq", 1),
                            C("carrier", "eq", 2),
                            C("bank", "le", 1),
                        ),
                        (("carrier", -2), ("bank", 1)),
                        0.12,
                        roles=("capture.enabled",),
                    )
                )
    # Translate both endpoints by one grid edge; newly occupied sites must be empty.
    # Store one representative per reversible spatial transition, including species.
    seen = set()
    for k, (i, j) in enumerate(edges):
        for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            targets = [(v // columns + dr, v % columns + dc) for v in (i, j)]
            if not all(0 <= r < 2 and 0 <= c < columns for r, c in targets):
                continue
            u, v = (r * columns + c for r, c in targets)
            new_edge = tuple(sorted((u, v)))
            a = edges.index(new_edge)
            for si, sj in product((1, 2), repeat=2):
                before = {x: 0 for x in {i, j, u, v}}
                after = dict(before)
                before.update({i: si, j: sj})
                after.update({u: si, v: sj})
                pair = tuple(
                    sorted(
                        (
                            (k, tuple(sorted(before.items()))),
                            (a, tuple(sorted(after.items()))),
                        )
                    )
                )
                if pair in seen:
                    continue
                seen.add(pair)
                guards = tuple(C(sites[x], "eq", value) for x, value in before.items())
                touched = sorted({b for x in before for b in incident[x]})
                guards += tuple(C(bonds[b], "eq", int(b == k)) for b in touched)
                changes = tuple(
                    (sites[x], after[x] - before[x])
                    for x in before
                    if after[x] != before[x]
                )
                changes += ((bonds[k], -1), (bonds[a], 1))
                rules.append(
                    Rule(
                        f"translate.{len(seen)}",
                        guards,
                        changes,
                        0.04,
                        roles=("motion.dimer",),
                    )
                )
    rules += [
        Rule(
            "source",
            (C("carrier", "eq", 0),),
            (("carrier", 1),),
            0.08,
            "3",
            "work_source",
            roles=("source",),
        ),
        Rule("bath.locked", (C("carrier", "eq", 0),), (("carrier", 1),), 0.002),
        Rule("bath.usable", (C("carrier", "eq", 0),), (("carrier", 2),), 0.002),
        Rule("unlock", (C("carrier", "eq", 1),), (("carrier", 1),), 0.04),
        Rule(
            "capture.basal",
            (C("carrier", "eq", 2), C("bank", "le", 1)),
            (("carrier", -2), ("bank", 1)),
            0.004,
            roles=("capture.basal",),
        ),
    ]
    energy = [E(".5", b) for b in bonds] + [
        E("3", conditions=(C("carrier", "eq", 1),)),
        E("2", conditions=(C("carrier", "eq", 2),)),
        E("1", "bank"),
    ]
    material = [
        {
            "id": f"species.{code}",
            "inventory": [
                {
                    "coefficient": "1",
                    "conditions": [{"coordinate": s, "operator": "eq", "value": code}],
                }
                for s in sites
            ],
        }
        for code in (1, 2)
    ]
    material += [
        {"id": "carrier_molecule", "inventory": [{"coefficient": "1"}]},
        {"id": "storage_molecule", "inventory": [{"coefficient": "1"}]},
    ]
    return LocalModel(
        f"spatial.ladder{columns}.v1",
        coordinates,
        rules,
        energy,
        forbidden=forbidden,
        material=material,
        relations=[
            {
                "id": "geometry",
                "edges": [list(e) for e in edges],
                "chemical_medium": "rapidly_mixed",
            }
        ],
    )


def spatial_root(model, *, bank=2):
    n = sum(c.role == "site_occupancy" for c in model.coordinates)
    columns = n // 2
    values = {f"site.{i}": 0 for i in range(n)}
    values.update(
        {
            "site.0": 1,
            f"site.{columns}": 1,
            f"site.{columns - 1}": 2,
            f"site.{n - 1}": 2,
            "bank": bank,
        }
    )
    root = tuple(values.get(c.name, 0) for c in model.coordinates)
    model.validate(root)
    return root
