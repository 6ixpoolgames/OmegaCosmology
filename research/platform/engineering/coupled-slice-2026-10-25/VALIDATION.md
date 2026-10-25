# Validation and reproducibility

25 October 2026. [71 unit tests passed](validation/TESTS.txt).
The [full workspace check](validation/WORKSPACE_CHECK.json) also passes source/
archive integrity, repository links, dependency checks, the inherited 233 finite
checks and exact P001 reproduction. Ruff and diff whitespace checks pass.
The validation receipt has local interpreter/repository paths redacted; its
original hash is retained. No scientific sign is used as an engineering criterion.

The [final smoke report](REPORT.md) and sealed evidence come from
`runs/coupled-smoke-20261025-r2`. A preliminary identical-physics pass remains
under ignored runs/; final source improves the projected lower bound by retaining
observed memory as well as an older hidden boundary state. The second pass
validates the updated analysis, not a second independent empirical result.

Input plan and original case results are retained here. SOURCE_MANIFEST.json
identifies frozen source bytes. The complete snapshot remains in the ignored
run directory. No dense operators, trajectories or augmented query-state arrays
are retained. Reproduction from the repository root uses fresh output paths:

```text
python scripts/write_coupled_smoke_plan.py
python scripts/run_coupled_smoke.py --out-dir runs/coupled-smoke-fresh
python scripts/report_coupled_smoke.py --run-dir runs/coupled-smoke-fresh --out-dir research/platform/engineering/coupled-smoke-fresh
```

The Windows supervisor enforces the declared caps. Generated engineering plan
changes are visible source changes, not an excuse to overwrite prior evidence.
Original R2-v1 results and interpretation history are preserved. No full
scientific parameter run, commit, push or upload was performed.
