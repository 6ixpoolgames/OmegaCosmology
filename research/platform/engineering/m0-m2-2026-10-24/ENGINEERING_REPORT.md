# M0–M2 first engineering report

24 October 2026. **PASS for the implemented finite classical engineering slice.**
No new scientific survey, ethical conclusion or r20 conformance is claimed.
The preparation archive was already pushed at e2da4f1; this implementation and
its evidence are local and uncommitted.

## Scope delivered

Six serializable semantic records, one local reversible physical kernel,
explicit finite symmetries, complete reachable enumeration, shared-law event
sampling, channel-resolved work/heat, full sampled-history queries, finite
projected word propagation, structural support, named-refinement diagnostics
and small irreducible rate/offset calculations. R1 and R2 are concrete same-
grammar construction examples, not scientific demonstrations of compounding.

## Capped source-frozen execution

- Worker wall time: 7.688 seconds; supervised wall time: 7.910 seconds.
- Reported peak job commitment: 173.00 MiB under a 2-GiB limit.
- Wall budget: 120 seconds. Output budget: 32 MiB; measured output including snapshot: 256,485 bytes.
- Timeout probe terminated the process tree. The 64-MiB memory probe refused
  further allocation after retaining 40 MiB of payload.
  Windows peak commitment counters can include refused allocation attempts;
  they are not resident-set measurements.
- 20 frozen inputs verified before/after execution; current input bytes match: **True**.
- Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1.

The launcher/cap helper matched the snapshot before launch; the calibration
worker imported its implementation from that snapshot. Signed transfer plans,
machine credentials and home paths are not included in the retained evidence.

## Numerical and physical checks

| World | Reachable states | Directed mechanism events | ell at T16, dt=.25 (bits) | First-law residual |
|---|---:|---:|---:|---:|
| R0 | 18 | 80 | 20.208795658 | 2.22e-16 |
| R1 | 75 | 486 | 25.605238829 | -3.33e-16 |
| R2 | 180 | 1304 | 26.047145390 | -1.89e-15 |

R0 has 30 nominal configurations but 18 in the root's conserved bank-parity
sector. R1/R2 contain 75/180 admissible reachable states. These rows have
different laws and material inventories; they are **not** an organized-versus-
disordered or capability ranking.

All source-off Gibbs/detailed-balance checks pass. Independent dense block
exponentials agree with sparse endpoint/occupation propagation; maximum
occupation residual is 2.40e-14. Direct short-word entropy agrees with the
chain rule, maximum residual 3.33e-16. All sampled supports are positive
on their enumerated sectors. Unresolved degeneracy creates no extra histories.

Each world has 1,000 seeded trajectories checked against exact endpoint and
expected-jump predictions, with the declared six-sigma calibration envelopes;
every sampled path closes its energy account. This is statistical sampler
validation, not a sampled history-entropy estimator or proof of exactness.

The calibration also records 12 finite reference cases. Focused tests add
same-law rate/offset checks, mid-history identity invariance, support under
exponential underflow, mutable-compilation rejection and invalid-projection
rejection. See the [formal map](../../../../formal/verification/reference-suite-r1.md)
for inspected source versions, guarantees and pending cases.

## Profile

| World | Enumeration + symmetry (s) | Sampled kernel + support (s) | Continuous propagation (s) | Entropy + word audit (s) | 1,000 paths (s) |
|---|---:|---:|---:|---:|---:|
| R0 | 0.0138 | 0.0010 | 0.0026 | 0.0021 | 0.9466 |
| R1 | 0.1162 | 0.0104 | 0.0020 | 0.0218 | 2.3190 |
| R2 | 0.3447 | 0.0601 | 0.0023 | 0.1338 | 3.0018 |

The summary additionally separates root rule-matching and canonicalization
microbenchmarks, equilibrium and other physical audits. Enumeration includes
its matching/symmetry work; these columns are not a disjoint call-graph profile.
At this size repeated event matching in the sampler dominates. For larger
worlds dense sampled kernels scale quadratically in storage, and projected
word enumeration can grow exponentially in horizon. Faster hardware does not
remove either limitation. No large-state scaling claim follows from this run.

## What remains outside this slice

Full workspace check passed: 32 unit tests, archive/source/link integrity, retained finite baseline and exact P001 reproduction. See [WORKSPACE_CHECK.json](WORKSPACE_CHECK.json) and [TESTS.txt](TESTS.txt). Local interpreter/repository paths are redacted, with the original receipt hash retained.

Sufficiency and physical faithfulness are declared assumptions, not empirical
certificates. Baths/sources have accounting but unresolved histories, so the
scope is the whole modeled field with no exterior cancellation claim. Numerical
results are float64 with checked residuals, not rigorous interval certificates.

Not yet implemented: general stoichiometric conservation sectors, spatial or
delayed transport, generic graph matching, dynamic population ecology,
three-generation path witnesses, optimizer/controller physics, large projected
entropy bounds, reducible-class asymptotics, quantum record families and
arbitrary present sections. Process-comparison metadata is an example contract,
not an implemented policy search. These remain explicit expansion points.

## Next step and reconstruction

The [R1 proposal](../../../studies/R1-constructed-access-PROPOSAL.md) compares
costed access and reconstruction against explicitly declared baselines. It has
not been launched. The [engineering decisions](ENGINEERING_DECISIONS.md) and
[worked models](../../models/README.md) justify the foundation.

From the repository root, install `.[testbed]`, rebuild model JSON with
`python scripts/write_testbed_fixtures.py`, and run
`python scripts/run_testbed_calibration.py --out-dir runs/calibration-fresh`.
Promote a verified run with `scripts/summarize_testbed_calibration.py`.
Exact bytes/hashes of this run are in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json),
[RECEIPT.json](RECEIPT.json) and [SUMMARY.json](SUMMARY.json). Numerical results
should agree within declared tolerances across supported libraries; timing and
allocation counters need not match. Full ignored snapshot: `runs/m0-m2-calibration-20261024-r4/frozen`.

No commit, push, broad science run or external upload follows automatically.
