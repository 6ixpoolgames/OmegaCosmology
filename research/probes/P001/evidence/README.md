# Retained P001 evidence

- `FULL_OBJECTS.json`: unchanged exact transition tables and policy-indexed
  occurrence trees from the first local run.
- `EXPECTED.json`: the scientific fields of that run's summary, without the
  previous workspace's path-dependent code hashes or interpreter version.
- `PROVENANCE.json`: original hashes and the precise migration changes.

The workspace check reproduces these objects and summary using the current
code. It records current source hashes, interpreter version and test logs in
a fresh `runs/` directory. A metadata difference is not silently treated as a
scientific difference, or vice versa.
