# Machinery repairs — 27 October 2026

Status: implemented locally; validation recorded in VALIDATION.json. No scientific
campaign, historical result rewrite, commit or publication is part of this pass.
ASSESSMENT.md and PROBES.json remain the original audit, not regenerated results.

Validation: all 155 tests pass, including 12 new adversarial regressions. Full
workspace source/archive/evidence checks and exact P001 reproduction pass. Lint
and diff whitespace checks pass. E1/occupied-adapter compatibility is checked
against retained native physics, not by updating expected numerical outputs.

## What changed

| Audit item | Implemented protection | Verification |
|---|---|---|
| A1: descriptive conservation | New material declarations require exact rational inventory functions. Every native forward/reverse pair checks the inventory delta against a declared boundary exchange. Negative inventories and symmetry-changing inventories are rejected. | Illegal creation rejected by exact enumeration and trajectory sampling; paid boundary exchange and phase composition accepted. |
| A2: common-present identity | Presents have content hashes. Process queries require them. A paired validator checks actual compiled models, roots, conditioning, observations, windows, boundary prescriptions and energy/material distributions. | Same ID with a different root rejected; differing windows, boundaries and model hashes rejected. |
| A3: mutable ledger | Compilation records a marked-event hash. Integrity checks include it; construction checks ledger aggregation against Q and first-law accounting. Flow and event-reward queries require integrity. | Empty/mutated ledger and inconsistent energy marks rejected. |
| A4: evaluator symmetry mismatch | Shared orbit validation for ordinary/scheduled observables and functional predicates. Marked queries require distinct identities until equivariance is implemented. | Scheduled invariant sum accepted; individual unmarked identity and predicate rejected. |
| A5: implicit scientific roles | Construction/capture/response/register/operation roles are explicit metadata. Parent and child are checked against transitions. Assistance discovery no longer depends on rule prefix or guard order. | Renamed/reordered rules preserve Q and assistance discovery; invalid parent declaration rejected. |
| A6: implicit moment tolerance | MomentSpec states quantity, units, horizon, convention and separate absolute/relative tolerances. Default small-target matching no longer uses a unit floor. | Original tiny-target false match rejected; unit conversion with converted tolerance preserves acceptance. |

Additional repairs:

- Missing marked-query rule IDs require an explicit `absent_rules` declaration;
  finite study law records supply `absent_query_rules`. A typo no longer quietly
  means zero. An empty rule list is rejected rather than interpreted as all rules.
- Moment matching retains an evaluated feasible control even when an infeasible
  control has a smaller sum of squared residuals. Feasibility is per quantity.
- Quotient histories retain their full score, but named-coordinate attribution
  is unavailable when canonical slots are unmarked. Canonical coordinates do not
  acquire constituent identities through reporting.
- Finite history and physical balances survive disconnected/reducible worlds.
  Unsupported asymptotic/availability quantities carry explicit statuses and
  null values; no recurrent class is silently selected.
- EvaluationContext shares a validated sampled kernel, accumulated profiles and
  irreducible rate/bias solve across queries. It is bound to compilation identity
  and cadence. Numerical arrays are read-only and kernel integrity is checked.
- Dense occupation validation streams one horizon operator instead of retaining
  one per horizon. `sampled_endpoint_crosscheck` is an explicit lower-memory mode;
  it does not claim the independent dense occupation check that it omits.
- The shared finite assay now rejects hidden-root conditioning upfront. The
  lower-level history evaluator still supports it; the assay's coordinate shares
  and independent accumulators presently implement known-root conditioning.

## Contracts and migration

Material descriptor example:

```json
{"id":"constituents","inventory":[
  {"coefficient":"1","coordinate":"precursor"},
  {"coefficient":"1","coordinate":"product"}
],"exchange_by_rule":{"feed":"1"}}
```

For an interior rule the inventory delta must be zero. `feed` must be a declared
boundary rule; its forward delta is one and its reverse delta is minus one.
Fixed-slot models use a constant inventory for the constituents present in every
slot, including unassembled states. Such a declaration certifies that inventory,
not an unrepresented chemistry or the adequacy of a construction price.

Historical serialized prose inventories remain readable and hash-stable, with
`legacy_unverified` status. They cannot establish paired material matching.
Current builders add executable inventories and role metadata: their full model
fingerprints therefore change. Compatibility tests compare the native rule
records, enumerated state order, numerical generator and full marked ledger.
They do not overwrite old fingerprints or silently weaken historical checks.

Single-query validation is explicitly **not** paired-comparison validation.
`validate_comparison` takes both executable arms. It currently requires a common
coordinate grammar; relabelled or otherwise different representations need an
explicit future mapping adapter. A process root and matching resources alone do
not prove physically embodied intervention: process enactment remains declared
and requires the encompassing-process audit. Exterior cancellation and physical
faithfulness are not certified by this validator.

Legacy scalar matching tolerance remains an explicitly labelled compatibility
option. The enacted-damage worker now expresses its retained plan's same numerical
allowances through per-moment units, horizon and absolute tolerance. This does not
retroactively improve or change the retained calibration result. No new fit ran.

Old ablation protocols must declare deliberately absent rule references when
replayed on the strict evaluator. Old operation snapshots without role metadata
must give explicit `operation_rules`. Migrations belong in a new execution input,
not in retained evidence bytes. Never infer an intended ablation from a misspelling.

## What is still an architectural boundary

These fixes harden the current engine; they do not make it feature complete.

- Inventory functions and roles are executable contracts, not a universal module
  port/binding system. Several adapters still use named bank/carrier conventions.
  Introduce explicit port bindings before arbitrary niches/populations rather
  than claiming those combinations are already generic.
- Distinct-slot ancestry is supported. Quotient-equivariant genealogy, general
  resource lineage and causal intervention attribution remain separate work.
- The compiled object remains guarded, not deeply immutable. Alterations are
  detected at query boundaries. Arbitrary external construction of a forged
  ledger is not authenticated against a separately reconstructed native law.
- Unsupported asymptotics are reported, not implemented. Source-off sector weights
  and general reducible long-run expansions still need dedicated query support.
- Dense sampled kernels remain a finite-model limit. Streaming occupation checks
  reduce retained memory, but can recompute references across preparations.
  Larger worlds need separately validated sparse/estimator backends.
- Existing scientific report scripts have not all been migrated to the paired
  validator. Historical evidence does not receive a new comparison certificate.

Before the integrated R2 successor, use these contracts for the actual paired
inputs and physical control calibration. Keep measured activity, accepted work,
finite profiles and explicit matching residuals together. None of this subtracts
churn, adds an organization bonus or establishes an ethical correspondence.
