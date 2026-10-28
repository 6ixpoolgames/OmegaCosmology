# Restoring the replay

Extract SNAPSHOT.zip into a fresh ignored runs/ directory. It restores legacy/
with both original manifests, inputs, results and native source, and frozen/
with the auditor, cap wrapper, focused tests and scope specification. Verify
the external EVIDENCE.json before extraction. NumPy and SciPy are required.

The scientific worker needs no mutable legacy checkout. Launch it with the
retained cap wrapper, for example from the repository root:

```python
import importlib.util
import sys
from pathlib import Path

restored = Path("runs/c7-restored").resolve()  # fresh extraction destination
path = restored / "frozen/src/omega_cosmology/testbed/workflow.py"
spec = importlib.util.spec_from_file_location("restored_caps", path)
caps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(caps)
receipt = caps.capped(
    [sys.executable, "-B", str(restored / "frozen/scripts/replay_c7.py"),
     "--worker", str(restored)],
    restored, seconds=240, memory=512 * 1024**2, output_cap=32 * 1024**2,
    cwd=restored / "frozen",
)
print(receipt)
```

The cap wrapper supplies the required GO handshake. The worker verifies frozen
hashes and writes fresh output/ files. Compare these to retained/ from this
package. Do not extract into an existing execution or overwrite its results.
The parent script's legacy-root option is for locating original historical
bundles, not needed for an archive restoration. A successful restore reproduces
the same declared historical contrast; it grants no extra physical certificate.
