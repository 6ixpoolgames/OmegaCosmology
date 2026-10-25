# E1 local-history precision follow-up

25 October 2026. Completed locally after the platform/E1 push. No physical
parameter or score was changed. Publication is included in the user's subsequent
scoped-sprint instruction to push on completion.

- [Interpretation and limits](INTERPRETATION.md).
- [Numerical tables](evidence/REPORT.md).
- [Full analysis](evidence/ANALYSIS.json).
- [Evidence hashes](evidence/EVIDENCE.json).
- [Plan and sequence](PLAN.md).
- [Validation](VALIDATION.md).
- [Estimator contract](../../../../formal/contracts/projected-filter-estimator-r1.md).

Reconstruct into fresh ignored run directories, using the retained inputs:

```text
python scripts/run_finite_study.py --protocol research/studies/E1-coupled-autocatalysis/refinement-2026-10-25/PROTOCOL_m2.json --out-dir runs/e1-memory2-fresh
python scripts/run_finite_study.py --protocol research/studies/E1-coupled-autocatalysis/refinement-2026-10-25/PROTOCOL_m3.json --out-dir runs/e1-memory3-fresh
python scripts/run_projection_filter.py --plan research/studies/E1-coupled-autocatalysis/refinement-2026-10-25/FILTER_PILOT_PLAN.json --out-dir runs/e1-filter-pilot-fresh
python scripts/run_projection_filter.py --plan research/studies/E1-coupled-autocatalysis/refinement-2026-10-25/FILTER_CONTROL_PILOT_PLAN.json --out-dir runs/e1-filter-control-pilot-fresh
python scripts/run_projection_filter.py --plan research/studies/E1-coupled-autocatalysis/refinement-2026-10-25/FILTER_LONG_PLAN.json --out-dir runs/e1-filter-long-fresh
```

The report builder takes those two memory runs and three filter runs, in order:

```text
python scripts/report_projection_refinement.py --memory-runs runs/e1-memory2-fresh runs/e1-memory3-fresh --filter-runs runs/e1-filter-pilot-fresh runs/e1-filter-control-pilot-fresh runs/e1-filter-long-fresh --out-dir research/studies/E1-coupled-autocatalysis/refinement-2026-10-25/evidence-fresh
```

The evidence stores byte-exact runtime/query inputs in each run's
`RUNTIME.zip`; RECONSTRUCTION.json maps them to their original paths.
The only referenced inputs are the unchanged original E1 protocol and case
evidence, published at55db381. Restore the recorded input versions before
attempting exact historical reconstruction after future code changes.

Use `python scripts/restore_research_snapshot.py --archive <RUNTIME.zip> --manifest <run/MANIFEST.json> --out-dir runs/refinement-restore`.
The restorer copies missing immutable inputs only if their recorded hashes
match, and restores all archived runtime bytes. Each archive was byte-verified
and restored before publication; evidence/PACKAGING.json records the storage
change made to avoid Windows Git path-length limits.
Timing and process memory need not reproduce exactly. Fixed seeds/sample plans
reproduce numerical estimates with the recorded runtime/library conventions;
platform/BLAS differences can alter rounding. No dense arrays or trajectories
need to be retained. Approximate intervals remain approximate after reproduction.
