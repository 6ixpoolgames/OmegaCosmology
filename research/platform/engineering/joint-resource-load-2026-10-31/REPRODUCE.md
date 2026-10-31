# Reproducing J's physical pilot

Restore SNAPSHOT.zip with scripts/restore_research_snapshot.py --archive
<SNAPSHOT.zip> --out-dir runs/<fresh-name>/frozen. Copy PLAN.json from this
evidence folder to runs/<fresh-name>/PLAN.json, preserving the manifest-bound
hash. Run the repository supervisor with python scripts/joint_resource_load_pilot.py
run --out-dir runs/<fresh-name>. It dispatches the exact restored frozen worker.
The Windows process-tree cap and GO gate are required. Do not call the worker
directly. Verify the supervisor against its retained source in a later checkout.
Restoration alone executes no physical calculation.

The snapshot contains INPUTS.json, all native engine sources and the exact
pilot script/spec/tests; no private manuscripts or trajectory caches. Source
hashes and plan are checked before dispatch. The worker repeats physics only,
up to the retained fixed budget; no history-scoring mode exists. Floating
solver details may vary by numerical library: compare residuals, model hashes,
gates and stopping scope rather than invent bit-exact fitting guarantees.
Use the retained CALIBRATION/PHYSICAL_MAP for the original evaluated points.
