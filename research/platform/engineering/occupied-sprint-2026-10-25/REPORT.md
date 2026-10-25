# Ecology sprint: capped engineering and precision feasibility

25 October 2026. Source-frozen inputs and unchanged raw results accompany this report.

## Occupied assistance smoke

| Case | States | Wall s | Peak MiB |
|---|---:|---:|---:|
| reciprocal_pair | 1215 | 25.194 | 609.75 |
| single_cycle | 54 | 0.913 | 115.54 |
| competing_port | 108 | 1.114 | 118.32 |
| local_pair | 972 | 14.522 | 433.42 |
| one_way_pair | 1080 | 18.961 | 507.07 |
| source_off_pair | 1215 | 24.901 | 611.32 |

Six cases passed. Two profiles per case, T4/16, cadence.25.
Port competition, release, bound failure and thermodynamics were engineering checks, not ranking targets.
Ancestry is queried on the two small cases; larger cases explicitly omit the ancestry product.
Local histories use member/bank projections and finite-memory bounds. Contacts remain in whole history.

## Projected donor confidence

Candidate-minus-reference is AtoB-minus-local from the unassembled E1 root.
Family intervals cover six requested comparisons under ideal iid/exact-arithmetic assumptions.
Float64 kernel/filter error is not rigorously enclosed. Approximate t intervals are separate.

| Cadence | T | Estimate bits | Finite-sample family interval | Approx. pointwise t interval |
|---:|---:|---:|---|---|
| 0.25 | 16 | -0.001841 | [-1.616443,1.612761] | [-0.002151,-0.001531] |
| 0.25 | 64 | -0.038504 | [-6.503588,6.426580] | [-0.043468,-0.033540] |
| 0.25 | 256 | -0.100513 | [-25.962649,25.761624] | [-0.121373,-0.079652] |
| 0.5 | 16 | -0.001739 | [-0.809419,0.805940] | [-0.002105,-0.001373] |
| 0.5 | 64 | -0.039211 | [-3.277036,3.198614] | [-0.044640,-0.033782] |
| 0.5 | 256 | -0.094713 | [-13.037356,12.847930] | [-0.111600,-0.077826] |

No certified donor sign is claimed. Report unresolved signs rather than increasing sampling until a desired sign appears.
A second cadence is an audit; it does not establish a finest faithful temporal grain.

## Setup corrections and reconstruction

Failed smoke setup1 assigned component-root values to similarly named contact coordinates; no profile was computed.
Setup2 reached the fixed dense-kernel workspace gate. No physics was reduced: the plan now declares128MiB kernel workspace.
The dense occupation reference has a separate512MiB gate. Old default kernel caps remain32MiB.
Both failed attempts, their logs and byte-exact source snapshots are retained.

Full runtime snapshots live in each run's SNAPSHOT.zip. No dense arrays or sampled paths are retained.
Each snapshot contains its plan, scripts and MANIFEST.json. Run from that snapshot root with a fresh output directory.
An assembly's occupancy is represented physically; query ancestry labels add no entropy.
No S3 interaction campaign, policy optimization, domination test or ethical verdict was run.
