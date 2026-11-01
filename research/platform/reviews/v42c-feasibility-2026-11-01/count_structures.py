"""Count a candidate state alphabet, not reachable states or history scores."""

import json
from itertools import combinations
from pathlib import Path


def count(columns):
    n = 2 * columns
    edges = [
        (r * columns + c, r * columns + c + 1)
        for r in range(2)
        for c in range(columns - 1)
    ] + [(c, c + columns) for c in range(columns)]
    placements = states = both = contact = 0
    for a_sites in combinations(range(n), 2):
        for b_sites in combinations([i for i in range(n) if i not in a_sites], 2):
            species = dict.fromkeys(a_sites, 1) | dict.fromkeys(b_sites, 2)
            placements += 1
            active = [e for e in edges if all(i in species for i in e)]
            for mask in range(1 << len(active)):
                chosen = [e for j, e in enumerate(active) if mask >> j & 1]
                ends = [i for e in chosen for i in e]
                if len(ends) != len(set(ends)):
                    continue
                states += 1
                if any(species[i] == species[j] == 1 for i, j in chosen) and any(
                    species[i] == species[j] == 2 for i, j in chosen
                ):
                    both += 1
                    contact += any(species[i] != species[j] for i, j in active)
    full = states * 3 * 3
    return {
        "grid": f"2x{columns}",
        "placements": placements,
        "position_and_matching_bond_states": states,
        "both_homotypic_dimers": both,
        "both_dimers_with_neighbor_contact": contact,
        "alphabet_with_carrier3_bank3": full,
        "one_float64_dense_matrix_bytes": 8 * full**2,
        "current_four_array_kernel_guard_bytes": 32 * full**2,
    }


if __name__ == "__main__":
    result = {
        "status": "combinatorial_alphabet_only_not_physical_enumeration",
        "assumptions": [
            "two indistinguishable particles of each of two distinct species",
            "one particle per fixed resolved site; no spatial symmetry quotient",
            "any nearest-neighbor bond; at most one bond per particle",
            "one three-state well-mixed carrier and one three-level shared bank",
            "no selector, actuator, source state or localized fuel positions",
        ],
        "cases": [count(c) for c in (2, 3, 4)],
    }
    path = Path(__file__).with_name("STRUCTURAL_COUNTS.json")
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
