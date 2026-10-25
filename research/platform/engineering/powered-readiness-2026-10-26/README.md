# Powered register calibration

The [report](REPORT.md) documents the versioned physical repair, its measured
fidelity, fuel demands and remaining limits. Seven capped cases/53 profiles
passed locally. This completes a calibration, not a broad policy search.

- [Calibration summary](CALIBRATION_SUMMARY.json)
- [Physical specification](../../specs/POWERED_READINESS_CALIBRATION_r1.md)
- [Executed plan](../../models/struggle-readiness/POWERED_CALIBRATION_PLAN.json)
- [Cap receipts](retained/BATCH_RECEIPT.json)
- [Exact worker input snapshot](retained/SNAPSHOT.zip)
- [Quality and reconstruction checks](QUALITY.json)
- [Workspace validation](validation/CHECKS.json)

The initial host-memory refusal is retained separately. No prior model/result
was changed, and nothing was committed, uploaded or pushed.

Restore the execution snapshot with `scripts/restore_research_snapshot.py`
into a fresh ignored run directory. It contains all inputs needed by the native
worker. To replay the separate report script there, also copy the two retained
`analysis_source/scripts/` helpers into that restored root's `scripts/` folder.
All those bytes and original result receipts are covered by EVIDENCE.json.
