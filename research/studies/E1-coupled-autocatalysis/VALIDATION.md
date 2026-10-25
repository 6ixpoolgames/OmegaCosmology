# Validation and reconstruction

25 October 2026. [78 unit tests passed](validation-2026-10-25/TESTS.txt).
[Full workspace checks](validation-2026-10-25/WORKSPACE_CHECK.json) passed source/
archive integrity, repository links, dependencies, the inherited233 finite
checks and exact P001 reproduction. Ruff and diff whitespace checks pass.

The new tests isolate cost from bank capacity/capture yield, verify matched
initial endowments and exact catalytic ablations, preserve the old smoke defaults,
check explicit cadence grids, validate multi-horizon projection traversal
against independent single-window calculations, and test signed interval sums.
Previous physical, ancestry and exhaustive hidden-Markov reference checks remain.

Run: `runs/e1-coupled-map-20261025-r1`. The frozen protocol/source preceded all
physical outcomes. Largest full T4096/.125 case gated three capped workers.
All65 cases passed;650 profiles. Wall367.646s, maximum per-job commitment
199.23MiB, output9,774,820bytes. Job caps240s/2GiB/16MiB; monitored batch caps
1800s/128MiB. No failed/replaced scientific cases or parameter retuning.

The [evidence manifest](results-2026-10-25/EVIDENCE.json) hashes retained compact
case results, protocol, receipts, numerical analysis and post-processing source.
Frozen calculation sources are identified separately in SOURCE_MANIFEST.json
and retained in the ignored run snapshot. Report construction was separate
post-processing; it did not recompute or change physical history scores.

The shareable validation receipt redacts local interpreter/repository paths and
retains the original receipt hash. Source/archive inputs and earlier R1/R2/smoke
evidence are preserved. No dense kernels, trajectories or augmented genealogy
arrays are retained in the study. No commit, push or upload occurred.

See [study reconstruction commands](README.md). New scientific or methodological
extensions use fresh directories and versioned interpretations. An unresolved
local interval or remaining long transient is retained, not converted into
a favorable sign, a numerical failure or a theory failure.
