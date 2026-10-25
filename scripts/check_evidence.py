"""Check retained research evidence against its byte-level manifests."""

import json
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check(root=ROOT):
    errors = []
    files = 0
    manifests = sorted((root / "research").rglob("EVIDENCE.json"))
    for manifest in manifests:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for row in data["files"]:
            target = (manifest.parent / row["path"]).resolve()
            label = manifest.relative_to(root).as_posix() + ":" + row["path"]
            if not target.is_relative_to(manifest.parent.resolve()):
                errors.append({"entry": label, "error": "outside evidence folder"})
                continue
            try:
                raw = target.read_bytes()
            except OSError:
                errors.append({"entry": label, "error": "missing evidence"})
                continue
            files += 1
            if sha256(raw).hexdigest() != row["sha256"]:
                errors.append({"entry": label, "error": "SHA256 mismatch"})
            if "bytes" in row and len(raw) != row["bytes"]:
                errors.append({"entry": label, "error": "size mismatch"})
    return {
        "status": "passed" if not errors else "failed",
        "manifests": len(manifests),
        "files": files,
        "errors": errors,
    }


if __name__ == "__main__":
    result = check()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "passed" else 1)
