# Reproducing J2

Restore SNAPSHOT.zip with scripts/restore_research_snapshot.py --archive
<snapshot> --out-dir runs/<fresh-name>/frozen; copy PLAN.json from this folder
to runs/<fresh-name>/PLAN.json. The current repository supervisor
scripts/run_j2_discharge.py run --out-dir runs/<fresh-name> dispatches the
exact restored workers, checks plan/source hashes and enforces process caps.
Check supervisor differences against the executed snapshot in a later checkout.
Do not directly bypass the GO gate. Restoration alone runs no science.

The physical plan and selected points are immutable. A history stage is
permitted only after actual joint qualification and its hash-bound physical
gate. The retained original run, including a gated non-run, is authoritative.
Do not substitute a later fit or latest source and call it the same run.
No private manuscript, dense kernel or sampled path is needed for restoration.
