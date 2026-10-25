# S4b: paid write-and-reset warning

A second version of the chapter18 functional warning/response assay, following
the [kinetic sensor audit](../S4-warning-and-obstruction/INTERPRETATION_r1.md).
S4/S4b are study identifiers, not completion claims for the ecology roadmap's
reserved S4 niche/population stage.

- [Specification](SPECIFICATION_r1.md): changed chemistry and unchanged questions.
- [Calibration](CALIBRATION.json): matched register moments, physical information diagnostics.
- [Dynamic/blocked protocol](PROTOCOL_DYNAMIC.json), [open protocol](PROTOCOL_OPEN.json).
- [Analysis plan](ANALYSIS_PLAN.json).
- [Interpretation](INTERPRETATION_r1.md), [results](results-2026-10-26/RESULTS.md),
  [physical diagnostics](results-2026-10-26/SIGNAL_DIAGNOSTICS.md).
- [Chapter18 evidence handoff](CHAPTER_18_EVIDENCE.md), [validation](VALIDATION.md).

Generate inputs with `scripts/write_s4_plan.py --sensor push_pull --out-dir
runs/<fresh-calibration>`. Retained calibration is never overwritten silently.
Use the normal source-frozen finite-study supervisor for each protocol, serially.
No science result is inferred merely from passing the smoke or fitting moments.
No suffering reward, free sensor work or randomness subtraction is introduced.
