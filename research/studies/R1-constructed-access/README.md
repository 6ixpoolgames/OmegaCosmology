# R1 constructed access

Status: completed first finite modeled-world batch, 24 October 2026; published
on 25 October. The earlier [proposal](../R1-constructed-access-PROPOSAL.md) defines
the question; [PROTOCOL.json](PROTOCOL.json) fixes the executed inputs.

- [Results and resource profile](results-2026-10-24/RESULTS.md).
- [Interpretation r1](INTERPRETATION_r1.md): mechanism, scope and next question.
- [Full contrast map](results-2026-10-24/ANALYSIS.json).
- [Evidence hashes](results-2026-10-24/EVIDENCE.json), original compact case
  results, source manifest and cap receipts are retained with the report.
- [Workspace validation](validation-2026-10-24/WORKSPACE_CHECK.json) and
  [36 passing tests](validation-2026-10-24/TESTS.txt), including inherited evidence reproduction.

Four laws × three cadences × three preparations × four horizons = 144 profiles.
The source-on/off and assisted/ablated laws use the same grammar, energies and
native background. Only the declared paired channels change. The equal-energy
reference averages nine known roots without adding a random-root entropy bonus.

Reusable passive measurements live in testbed/readouts.py. They do not introduce
a private physical engine or a replacement definition of lushness. The R1
scripts orchestrate the shared compiler, history queries, thermodynamics,
snapshot supervisor and report receipts.

Regenerate inputs with `python scripts/write_r1_protocol.py`, execute with
`python scripts/run_r1_batch.py --out-dir runs/r1-fresh`, and use
`python scripts/report_r1.py --run-dir runs/r1-fresh --out-dir research/studies/R1-constructed-access/results-fresh`.
The supervisor gates the other cases on the completed longest-horizon,
fine-cadence intact case. A feasibility-only invocation is also available.
No scientific result is selected by a favorable-sign requirement.
