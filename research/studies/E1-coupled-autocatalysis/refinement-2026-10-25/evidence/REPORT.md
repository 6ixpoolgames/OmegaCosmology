# E1 projected-history refinement

25 October 2026. Unchanged physical laws, preparations, horizons and state grain.

## Exact-memory benchmark

Donor A, AtoB minus local, T4096 at cadence .25:

| Memory | Assembled interval (bits) | Unassembled interval (bits) |
|---|---:|---:|
| 1 | [-84.6815, 87.2601] | [-84.8839, 86.6518] |
| 2 | [-79.8469, 82.4371] | [-80.0732, 81.8514] |
| 3 | [-75.5786, 78.1819] | [-75.8254, 77.6155] |

All refined bounds enclose the requested quantity analytically, evaluated in float64.
Both levels tighten the earlier intervals but leave donor signs unresolved.
Maximum unchanged whole-history residual: 0 bits.

## Filtering estimates

These estimate the same full projected history using finite hidden-state filtering.
Exact-mean controls improve precision without removing any physical entropy.
The t intervals below are approximate, pointwise statistical intervals; they
are not analytically resolved rankings. Distribution-free intervals are retained
in the machine-readable output even when too wide to decide a sign.

| Preparation | Horizon | Difference estimate (bits) | Approx. 95% t interval | SE / raw SE |
|---|---:|---:|---:|---:|
| assembled | 16 | 0.05786 | [0.03443, 0.08129] | 0.0119 / 0.0309 |
| assembled | 64 | 0.07202 | [-0.02035, 0.16439] | 0.0470 / 0.1600 |
| assembled | 256 | 0.22493 | [0.07209, 0.37776] | 0.0778 / 0.4271 |
| assembled | 1024 | 0.57721 | [0.31137, 0.84306] | 0.1353 / 1.3211 |
| assembled | 4096 | 1.61173 | [1.05478, 2.16868] | 0.2835 / 3.0285 |
| unassembled | 16 | -0.00209 | [-0.00267, -0.00151] | 0.0003 / 0.0004 |
| unassembled | 64 | -0.04775 | [-0.06256, -0.03295] | 0.0075 / 0.0384 |
| unassembled | 256 | -0.14129 | [-0.19824, -0.08435] | 0.0290 / 0.4085 |
| unassembled | 1024 | 0.03955 | [-0.13427, 0.21337] | 0.0885 / 1.2040 |
| unassembled | 4096 | 0.98724 | [0.40639, 1.56808] | 0.2957 / 3.3286 |

## Compute

| Run | Wall seconds | Peak per-job MiB |
|---|---:|---:|
| e1-projection-m2-20261025-r1 | 40.641 | 197.64 |
| e1-projection-m3-20261025-r1 | 276.477 | 517.51 |
| e1-filter-pilot-20261025-r1 | 23.346 | 504.40 |
| e1-filter-control-pilot-20261025-r1 | 23.449 | 505.73 |
| e1-filter-long-20261025-r1 | 122.634 | 160.02 |

All cases passed their declared caps. No failed case was replaced or scientific
parameter/horizon changed. Frozen input manifests and byte-different historical
inputs are retained. No dense matrices or trajectories are retained here.

The four short E1 calibration cases and both pilots remain in ANALYSIS.json.
Agreement at short prefixes does not prove asymptotic statistical coverage.

No private/whole ethical conclusion follows from an estimated donor difference.
A physical donor fuel cost, sequestration, material transfer and irreversible
loss are still absent from this contrast.
